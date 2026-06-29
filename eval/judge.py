"""
LLM-as-judge for open-ended inferred-preference answers.

Design (verified prior art):
  * Reference-guided pointwise grading + CoT steps   G-Eval (arXiv:2303.16634)
  * Strict output format "[[k]]" for deterministic parse   MT-Bench/FastChat (arXiv:2306.05685)
  * Position-bias control: for pairwise, swap order & require agreement (FastChat)
  * Per-constraint satisfaction extraction for the Reasoning Score

Bias controls baked in:
  - non-self judge (configure a different model family than the agent)
  - verbosity guard ("do not let length influence you")
  - optional N-sample-and-average (G-Eval) via `samples`
"""
from __future__ import annotations

import json
import re
from typing import Dict, List, Optional

from assomem.llm import LLM
from assomem.schema import AgentAnswer, BenchItem

JUDGE_SYSTEM = (
    "You are an impartial judge evaluating whether a personal agent correctly INFERRED the "
    "user's preference from memory. Be objective. Do not let answer length influence you. "
    "First reason briefly, then output STRICT JSON only."
)

JUDGE_USER_TMPL = (
    "User facts (memory):\n{context}\n\n"
    "Request to the agent:\n{query}\n\n"
    "Ground truth (the correct inferred preference/answer):\n{gold}\n\n"
    "Agent answer (response to grade):\n{answer}\n\n"
    "Constraints that the answer must satisfy (ordered):\n{constraints}\n\n"
    "Return JSON: {{\"score\": <0..5>, \"verdict\": \"yes|no\", "
    "\"constraint_satisfaction\": [<0|1 per constraint>], \"rationale\": \"...\"}}"
)


def _parse(raw: str) -> Dict:
    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    # last resort: pull a [[k]] style rating
    m = re.search(r"\[\[(\d+(?:\.\d+)?)\]\]", raw)
    score = float(m.group(1)) if m else 0.0
    return {"score": score, "verdict": "yes" if score >= 3 else "no",
            "constraint_satisfaction": [], "rationale": "parsed-fallback"}


def judge_answer(item: BenchItem, ans: AgentAnswer, llm: LLM, samples: int = 1) -> Dict:
    """Grade one open-ended answer. Returns {score01, verdict, constraint_satisfaction,...}."""
    user = JUDGE_USER_TMPL.format(
        context="\n".join(f"- {c}" for c in item.stored_context[:40]),
        query=item.query, gold=item.gold, answer=ans.answer,
        constraints="\n".join(f"{i+1}. {c}" for i, c in enumerate(item.constraints)) or "(none)",
    )
    msgs = [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]
    scores, verdicts, sats = [], [], []
    for _ in range(max(1, samples)):
        d = _parse(llm.chat(msgs, json_mode=True))
        scores.append(float(d.get("score", 0.0)))
        verdicts.append(str(d.get("verdict", "no")).lower())
        if d.get("constraint_satisfaction"):
            sats.append([float(v) for v in d["constraint_satisfaction"]])
    score01 = (sum(scores) / len(scores)) / 5.0
    verdict = max(set(verdicts), key=verdicts.count)
    csat = sats[0] if sats else ([1.0] * len(item.constraints) if verdict == "yes"
                                 else [0.0] * len(item.constraints))
    return {"score01": score01, "verdict": verdict,
            "constraint_satisfaction": csat, "raw_score": sum(scores) / len(scores)}


def judge_pairwise(item: BenchItem, ans_a: str, ans_b: str, llm: LLM) -> str:
    """Swap-and-require-agreement pairwise judge (returns 'A'|'B'|'tie')."""
    def one(x, y):
        u = (f"Request:\n{item.query}\nGround truth:\n{item.gold}\n"
             f"Answer A:\n{x}\nAnswer B:\n{y}\nWhich is better? JSON {{\"winner\":\"A|B|tie\"}}")
        d = _parse(llm.chat([{"role": "system", "content": JUDGE_SYSTEM},
                             {"role": "user", "content": u}], json_mode=True))
        return str(d.get("winner", "tie")).upper()[:1]
    g1, g2 = one(ans_a, ans_b), one(ans_b, ans_a)        # second call swaps order
    if g1 == "A" and g2 == "B":
        return "A"
    if g1 == "B" and g2 == "A":
        return "B"
    return "tie"                                          # inconsistent -> undecided

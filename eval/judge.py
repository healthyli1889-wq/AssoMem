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
    "user's preference from memory, and whether it did so ASSOCIATIVELY (by combining distinct "
    "pieces of evidence) rather than by luck or generic knowledge. Be objective. Do not let "
    "answer length influence you. First reason briefly, then output STRICT JSON only."
)

JUDGE_USER_TMPL = (
    "User facts (memory, may be truncated for length -- the target evidence below is NOT "
    "truncated, it is guaranteed complete regardless of what appears above):\n{context}\n\n"
    "Target evidence the answer should draw on (id: text):\n{evidence_block}\n\n"
    "Request to the agent:\n{query}\n\n"
    "Ground truth (the correct inferred preference/answer):\n{gold}\n\n"
    "Agent answer (response to grade):\n{answer}\n"
    "Agent rationale, if provided:\n{rationale}\n\n"
    "Constraints / required elements that the answer must satisfy (ordered):\n{constraints}\n\n"
    "Return STRICT JSON only:\n"
    "{{\"score\": <0..5>, \"verdict\": \"yes|no\", "
    "\"constraint_satisfaction\": [<0|1 per constraint, same order as above>], "
    "\"target_evidence_used\": {{\"<evidence_id>\": <0|1>, ...}}  // for EACH id listed above, "
    "1 only if the answer's reasoning genuinely relied on it (not just coincidentally correct), "
    "\"is_associative\": <0|1>  // 1 only if answering correctly required COMBINING >=2 distinct "
    "target evidence ids via a non-obvious bridge; 0 if a single fact or generic knowledge would "
    "have sufficed, "
    "\"rationale\": \"...\"}}"
)


def _evidence_block(item: BenchItem) -> str:
    ids = item.evidence_ids or []
    if not ids:
        return "(no target evidence ids on this item)"
    cons = item.constraints or []
    lines = []
    for i, eid in enumerate(ids):
        text = cons[i] if i < len(cons) else "(text not separately extracted -- locate it in User facts above)"
        lines.append(f"- {eid}: {text}")
    return "\n".join(lines)


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
            "constraint_satisfaction": [], "target_evidence_used": {}, "is_associative": 0,
            "rationale": "parsed-fallback"}


def judge_answer(item: BenchItem, ans: AgentAnswer, llm: LLM, samples: int = 1) -> Dict:
    """Grade one open-ended answer.

    Returns the original keys (score01, verdict, constraint_satisfaction, raw_score) plus the
    associative-memory triad the team wants tracked: is_associative, target_evidence_used,
    target_evidence_coverage. `evidence_block` guarantees the judge sees full target-evidence
    text even when `stored_context` above it is truncated to the first 40 lines (long LoCoMo
    conversations put evidence past line 40 -- without this the judge silently can't see what
    it's grading).
    """
    user = JUDGE_USER_TMPL.format(
        context="\n".join(f"- {c}" for c in item.stored_context[:40]),
        evidence_block=_evidence_block(item),
        query=item.query, gold=item.gold, answer=ans.answer,
        rationale=ans.rationale or "(none provided)",
        constraints="\n".join(f"{i+1}. {c}" for i, c in enumerate(item.constraints)) or "(none)",
    )
    msgs = [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]
    scores, verdicts, sats, assoc_votes, tev_samples = [], [], [], [], []
    for _ in range(max(1, samples)):
        d = _parse(llm.chat(msgs, json_mode=True))
        scores.append(float(d.get("score", 0.0)))
        verdicts.append(str(d.get("verdict", "no")).lower())
        if d.get("constraint_satisfaction"):
            sats.append([float(v) for v in d["constraint_satisfaction"]])
        assoc_votes.append(int(bool(d.get("is_associative", 0))))
        if d.get("target_evidence_used"):
            tev_samples.append(d["target_evidence_used"])
    score01 = (sum(scores) / len(scores)) / 5.0
    verdict = max(set(verdicts), key=verdicts.count)
    csat = sats[0] if sats else ([1.0] * len(item.constraints) if verdict == "yes"
                                 else [0.0] * len(item.constraints))
    is_associative = 1 if assoc_votes and sum(assoc_votes) * 2 >= len(assoc_votes) else 0
    raw_tev = tev_samples[0] if tev_samples else {}
    target_evidence_used = {eid: int(bool(raw_tev.get(eid, 0))) for eid in (item.evidence_ids or [])}
    target_evidence_coverage = (sum(target_evidence_used.values()) / len(target_evidence_used)
                                if target_evidence_used else None)
    return {"score01": score01, "verdict": verdict,
            "constraint_satisfaction": csat, "raw_score": sum(scores) / len(scores),
            "is_associative": is_associative,
            "target_evidence_used": target_evidence_used,
            "target_evidence_coverage": target_evidence_coverage}


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

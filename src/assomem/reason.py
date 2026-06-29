"""
REASON stage -- infer a NEW preference / pick the answer from associated memory.

Borrowed from: Generative Agents `run_reflect` / `generate_insights_and_evidence`
  github.com/joonspk-research/generative_agents/.../cognitive_modules/reflect.py
Key idea kept: the inferred insight is stored back WITH its evidence note-ids
(traceability), and reflection is importance-gated (only fire when enough salient
memory has accumulated) so it stays cheap.

For MC items we select the option whose embedding best matches the
retrieved + associated memory context (mock) or ask the LLM (openai backend).
"""
from __future__ import annotations

import json
import time
from typing import List, Optional, Tuple

from .llm import LLM, cosine
from .schema import AgentAnswer, BenchItem, MemoryNote

INFER_PROMPT = (
    "You are a personal agent with memory of the user. Using ONLY the user facts below, "
    "infer the most plausible answer to the request. Think about associations across facts "
    "(hobbies, work, personality, context). Return STRICT JSON: "
    "{\"answer\": \"...\", \"rationale\": \"...\", \"confidence\": 0.0-1.0}."
)


def _context_block(mem: List[MemoryNote]) -> str:
    return "\n".join(f"- ({m.category}) {m.content}" for m in mem)


def reflect_insight(mem: List[MemoryNote], llm: LLM) -> Optional[MemoryNote]:
    """Generate a higher-level preference insight from memory (stored back with evidence)."""
    if len(mem) < 2:
        return None
    facts = _context_block(mem)
    try:
        raw = llm.chat(
            [{"role": "system", "content": "Infer one higher-level user preference (insight)."},
             {"role": "user", "content": f"Facts:\n{facts}\nInfer one new preference."}],
            json_mode=True,
        )
        insight = json.loads(raw).get("insight")
    except Exception:
        insight = None
    if not insight:
        return None
    note = MemoryNote(content=insight, kind="insight",
                      evidence=[m.note_id for m in mem],
                      embedding=llm.embed(insight), poignancy=6.0,
                      valid_at=time.time())
    return note


def answer_item(item: BenchItem, mem: List[MemoryNote], llm: LLM) -> AgentAnswer:
    """Produce the agent's answer for one item from its (retrieved+associated) memory."""
    used = [m.note_id for m in mem]
    ctx = _context_block(mem)

    if item.is_mc:
        # rank options by similarity to the memory context (+ the query)
        cue = llm.embed(item.query + " " + ctx)
        opt_embs = llm.embed_batch(item.options)
        sims = [cosine(cue, e) for e in opt_embs]
        best = max(range(len(sims)), key=lambda i: sims[i]) if sims else 0
        # confidence = margin between top-1 and top-2 similarity (calibration signal)
        ordered = sorted(sims, reverse=True)
        margin = (ordered[0] - ordered[1]) if len(ordered) > 1 else ordered[0]
        conf = max(0.0, min(1.0, 0.5 + margin))
        return AgentAnswer(item_id=item.item_id, answer=item.options[best],
                           chosen_option_idx=best, used_evidence=used,
                           confidence=conf, rationale="selected by memory-context similarity",
                           action=item.options[best] if item.scenario == "memory_to_action" else None)

    # open-ended inference
    try:
        raw = llm.chat(
            [{"role": "system", "content": INFER_PROMPT},
             {"role": "user", "content": f"User facts:\n{ctx}\n\nRequest: {item.query}"}],
            json_mode=True,
        )
        d = json.loads(raw)
        ans = d.get("answer", "")
        conf = float(d.get("confidence", 0.5))
        rat = d.get("rationale", "")
    except Exception:
        ans, conf, rat = (mem[0].content if mem else ""), 0.3, "fallback: top memory"
    return AgentAnswer(item_id=item.item_id, answer=ans, used_evidence=used,
                       confidence=conf, rationale=rat,
                       action=ans if item.scenario == "memory_to_action" else None)

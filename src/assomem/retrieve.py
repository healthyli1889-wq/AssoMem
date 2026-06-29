"""
RETRIEVE + MATCH stage -- score stored notes for a query.

Borrowed from: Generative Agents `new_retrieve`
  github.com/joonspk-research/generative_agents/.../cognitive_modules/retrieve.py
Score = w_rec * recency + w_rel * relevance + w_imp * importance, each normalized to [0,1].
Accessing a note refreshes its recency (human-like reinforcement).

Relevance = cosine(query, note) (Mem0 vector search).  Recency = exp decay over note age.
Importance = note.poignancy (Generative Agents).
"""
from __future__ import annotations

import math
import time
from typing import Dict, List, Tuple

from .llm import LLM, cosine
from .schema import MemoryNote


def _normalize(d: Dict[str, float]) -> Dict[str, float]:
    if not d:
        return d
    lo, hi = min(d.values()), max(d.values())
    if hi - lo < 1e-9:
        return {k: 1.0 for k in d}
    return {k: (v - lo) / (hi - lo) for k, v in d.items()}


def retrieve(query: str, notes: List[MemoryNote], llm: LLM, top_k: int = 8,
             w_rec: float = 0.5, w_rel: float = 3.0, w_imp: float = 2.0,
             half_life_days: float = 30.0) -> List[Tuple[MemoryNote, float]]:
    """Return top_k (note, score) pairs and refresh their last_accessed."""
    if not notes:
        return []
    q = llm.embed(query)
    now = time.time()
    decay = math.log(2) / (half_life_days * 86400.0)

    relevance = {n.note_id: cosine(q, n.embedding or []) for n in notes}
    recency = {n.note_id: math.exp(-decay * (now - n.last_accessed)) for n in notes}
    importance = {n.note_id: n.poignancy for n in notes}

    relevance, recency, importance = _normalize(relevance), _normalize(recency), _normalize(importance)
    by_id = {n.note_id: n for n in notes}
    scored = {
        nid: w_rec * recency[nid] + w_rel * relevance[nid] + w_imp * importance[nid]
        for nid in by_id
    }
    ranked = sorted(scored.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    out = []
    for nid, sc in ranked:
        n = by_id[nid]
        n.last_accessed = now                       # access refreshes recency
        out.append((n, sc))
    return out

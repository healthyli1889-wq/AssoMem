"""
ASSOCIATE stage -- the heart of *associative* memory.

Two complementary mechanisms, both from verified SOTA:

1. Graph link building (A-MEM `process_memory` -> MemoryNote.links)
   github.com/agiresearch/A-mem/blob/main/agentic_memory/memory_system.py
   On insert, connect a note to its nearest neighbors (bidirectional) so memory is a graph.

2. Spreading activation via Personalized PageRank (HippoRAG `run_ppr`)
   github.com/OSU-NLP-Group/HippoRAG/blob/main/src/hipporag/HippoRAG.py
   Seed the graph with the query-activated notes, then random-walk so notes that are
   ASSOCIATED but not directly similar light up -> these are candidate *new* preferences.

We implement PPR with the power-iteration method (no igraph dependency) so the repo is
pip-light and runs anywhere.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from .llm import cosine
from .schema import MemoryNote, TemporalEdge


def build_links(notes: List[MemoryNote], sim_threshold: float = 0.25,
                max_links: int = 5) -> List[TemporalEdge]:
    """Connect each note to its most-similar neighbors (A-MEM 'strengthen')."""
    edges: List[TemporalEdge] = []
    for i, a in enumerate(notes):
        sims: List[Tuple[float, MemoryNote]] = []
        for j, b in enumerate(notes):
            if i == j:
                continue
            s = cosine(a.embedding or [], b.embedding or [])
            if s >= sim_threshold:
                sims.append((s, b))
        sims.sort(key=lambda x: x[0], reverse=True)
        for s, b in sims[:max_links]:
            if b.note_id not in a.links:
                a.links.append(b.note_id)
            rel = "co-occurs" if a.category == b.category else "cross-domain"
            edges.append(TemporalEdge(a.note_id, b.note_id, rel,
                                      fact=f"{a.content} ~ {b.content}", weight=float(s)))
    return edges


def _adjacency(notes: List[MemoryNote], edges: List[TemporalEdge]) -> Dict[str, Dict[str, float]]:
    adj: Dict[str, Dict[str, float]] = {n.note_id: {} for n in notes}
    for e in edges:
        if e.source_id in adj and e.target_id in adj:
            adj[e.source_id][e.target_id] = adj[e.source_id].get(e.target_id, 0.0) + e.weight
            adj[e.target_id][e.source_id] = adj[e.target_id].get(e.source_id, 0.0) + e.weight  # undirected
    return adj


def personalized_pagerank(seeds: Dict[str, float], notes: List[MemoryNote],
                          edges: List[TemporalEdge], damping: float = 0.5,
                          iters: int = 50, tol: float = 1e-6) -> Dict[str, float]:
    """Power-iteration PPR. `seeds` = query-activated reset vector (HippoRAG run_ppr).

    damping controls how far association spreads (higher -> wider spread).
    """
    ids = [n.note_id for n in notes]
    if not ids:
        return {}
    adj = _adjacency(notes, edges)
    # normalize reset vector
    ssum = sum(seeds.get(i, 0.0) for i in ids) or 1.0
    reset = {i: seeds.get(i, 0.0) / ssum for i in ids}
    rank = dict(reset)
    for _ in range(iters):
        nxt = {i: (1 - damping) * reset[i] for i in ids}
        for i in ids:
            out = adj[i]
            tot = sum(out.values())
            if tot <= 0:
                # dangling node: redistribute by reset
                for j in ids:
                    nxt[j] += damping * rank[i] * reset[j]
                continue
            for j, w in out.items():
                nxt[j] += damping * rank[i] * (w / tot)
        delta = sum(abs(nxt[i] - rank[i]) for i in ids)
        rank = nxt
        if delta < tol:
            break
    return rank


def associate(retrieved: List[MemoryNote], notes: List[MemoryNote],
              edges: List[TemporalEdge], damping: float = 0.5,
              top_k: int = 6) -> List[Tuple[MemoryNote, float]]:
    """Spread activation from `retrieved` seeds; return associated notes by PPR score.

    This surfaces facts that are *connected* to the query context but were not directly
    retrieved -- the substrate for inferring a NEW preference.
    """
    if not retrieved:
        return []
    seeds = {n.note_id: max(n.poignancy, 1.0) for n in retrieved}
    ranks = personalized_pagerank(seeds, notes, edges, damping=damping)
    by_id = {n.note_id: n for n in notes}
    seed_ids = set(seeds)
    ranked = sorted(((nid, r) for nid, r in ranks.items()), key=lambda kv: kv[1], reverse=True)
    out = []
    for nid, r in ranked:
        if nid in by_id:                       # include seeds + spread; caller can filter
            out.append((by_id[nid], r))
        if len(out) >= top_k + len(seed_ids):
            break
    return out

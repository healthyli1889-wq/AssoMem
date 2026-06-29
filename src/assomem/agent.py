"""
AssociativeMemoryAgent -- the full reference pipeline.

PATH (the "special map"):
    raw turns
       |  STORE      store.extract_facts -> store.make_notes        (Mem0)
       v
    MemoryNotes  --ASSOCIATE associate.build_links (graph)          (A-MEM)
       |
       |  (query arrives)
       v
    RETRIEVE  retrieve.retrieve  (recency x relevance x importance) (Generative Agents)
       |
       v
    ASSOCIATE associate.associate (Personalized PageRank spread)    (HippoRAG)
       |
       v
    REASON    reason.answer_item / reflect_insight                  (Gen. Agents reflection)
       |
       v
    ACT/UPDATE  consolidate (Ebbinghaus)  -> AgentAnswer            (MemoryBank)

Ablations are first-class (set flags off) so the benchmark can isolate which biological
component matters -- this is the experiment-setup control in the paper.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from . import associate as A
from . import consolidate as C
from . import reason as R
from . import retrieve as RT
from . import store as S
from .llm import LLM
from .schema import AgentAnswer, BenchItem, MemoryNote, TemporalEdge


@dataclass
class AgentConfig:
    use_association: bool = True       # HippoRAG PPR spread  (core associative ability)
    use_links: bool = True            # A-MEM graph edges
    use_reflection: bool = True       # Generative Agents insight generation
    use_forgetting: bool = True       # MemoryBank Ebbinghaus consolidation
    top_k_retrieve: int = 8
    top_k_associate: int = 6
    ppr_damping: float = 0.5

    @staticmethod
    def memory_only() -> "AgentConfig":
        """Ablation baseline: plain RAG, no association/reflection (the 'store-only' agent)."""
        return AgentConfig(use_association=False, use_links=False,
                           use_reflection=False, use_forgetting=False)


class AssociativeMemoryAgent:
    def __init__(self, llm: LLM, config: AgentConfig = None):
        self.llm = llm
        self.cfg = config or AgentConfig()
        self.notes: List[MemoryNote] = []
        self.edges: List[TemporalEdge] = []

    # ---- ingest a user's history into memory ----
    def ingest(self, turns: List[str]) -> None:
        facts = S.extract_facts(turns, self.llm)
        new_notes = S.make_notes(facts, self.llm)
        self.notes.extend(new_notes)
        if self.cfg.use_forgetting:
            self.notes = C.consolidate(self.notes)
        if self.cfg.use_links:
            self.edges = A.build_links(self.notes)
        if self.cfg.use_reflection:
            insight = R.reflect_insight(self.notes[-12:], self.llm)
            if insight is not None:
                self.notes.append(insight)

    def reset(self) -> None:
        self.notes, self.edges = [], []

    # ---- answer one benchmark item ----
    def answer(self, item: BenchItem) -> AgentAnswer:
        retrieved = RT.retrieve(item.query, self.notes, self.llm,
                                top_k=self.cfg.top_k_retrieve)
        seed_notes = [n for n, _ in retrieved]
        for n in seed_notes:
            C.reinforce(n)                                # recall reinforces (CLS)

        working = list(seed_notes)
        if self.cfg.use_association and self.edges:
            assoc = A.associate(seed_notes, self.notes, self.edges,
                                damping=self.cfg.ppr_damping,
                                top_k=self.cfg.top_k_associate)
            for n, _ in assoc:
                if n.note_id not in {w.note_id for w in working}:
                    working.append(n)

        return R.answer_item(item, working, self.llm)

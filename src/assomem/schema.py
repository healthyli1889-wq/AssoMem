"""
Core data structures for the associative-memory agent and benchmark.

Design rationale (evidence-based)
---------------------------------
Each structure below is borrowed/adapted from a verified SOTA codebase so that the
architecture is grounded, not invented:

* MemoryNote  ~ A-MEM `MemoryNote` (Zettelkasten note with `links`)
                github.com/agiresearch/A-mem/blob/main/agentic_memory/memory_system.py
                + Generative Agents `ConceptNode` (poignancy / last_accessed / evidence)
                github.com/joonspk-research/generative_agents/.../associative_memory/
* TemporalEdge ~ Zep/Graphiti `EntityEdge` bi-temporal fact (valid_at / invalid_at)
                github.com/getzep/graphiti/blob/main/graphiti_core/edges.py
* BenchItem   ~ PersonaMem item (stored context + query + options + gold) unified with
                LoCoMo evidence-IDs + PerLTQA memory-anchor + MemoryArena action target.

Everything is plain-dataclass + JSON-serializable so the repo runs anywhere
(Cursor, Jupyter, plain `python`), no DB required.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class MemoryNote:
    """A single stored unit of user information (atomic fact or derived insight).

    `links` makes the memory an associative GRAPH (A-MEM), `poignancy`/`last_accessed`
    drive recency x importance x relevance retrieval (Generative Agents), and
    `strength`/`last_recall` drive Ebbinghaus consolidation (MemoryBank).
    `evidence` holds the source note ids when this note is an *inferred* preference
    (Generative Agents reflection) -> full traceability/explainability.
    """
    content: str
    note_id: str = field(default_factory=_new_id)
    kind: str = "fact"                       # "fact" | "insight" (inferred preference)
    keywords: List[str] = field(default_factory=list)
    category: str = "general"                # e.g. hobby, food, work, personality
    links: List[str] = field(default_factory=list)        # ids of associated notes
    evidence: List[str] = field(default_factory=list)      # source ids for an insight
    embedding: Optional[List[float]] = None
    poignancy: float = 1.0                    # importance in [0..10]; LLM- or rule-scored
    strength: float = 1.0                     # memory strength S (MemoryBank)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    last_recall: float = field(default_factory=time.time)
    # bi-temporal validity (Graphiti) -- lets a preference be superseded, not deleted
    valid_at: Optional[float] = None
    invalid_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TemporalEdge:
    """Bi-temporal associative edge between two MemoryNotes (Graphiti EntityEdge)."""
    source_id: str
    target_id: str
    relation: str                            # e.g. "implies", "co-occurs", "updates"
    fact: str = ""
    weight: float = 1.0
    valid_at: Optional[float] = None
    invalid_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BenchItem:
    """One unified associative-inference test item.

    Maps the four base datasets onto one schema (see data/README.md):
      stored_context    : the user history / facts the agent may use
      query             : the trigger asking the agent to INFER something new
      options           : MC options (PersonaMem); empty -> open-ended
      gold              : ground-truth inferred preference / answer
      evidence_ids      : which stored facts support the gold
      constraints       : ordered list of accumulated conditions for long-horizon RS scoring
      action_gold       : downstream action the inferred preference should drive (MemoryArena)
      scenario          : "associative" | "long_horizon" | "memory_to_action" | "working_memory_control"
      question_type     : recall | suggest_new | recommend | generalize | track_update ...
      association_type  : A1_relational_binding | A2_cue_chain | A3_cross_domain |
                          A4_temporal_consistency | A5_absence_control
                          (from the annotation scheme; used to stratify evaluation results)
      counterfactual_probes : auto-detected probe types for A5 Counterfactual Necessity
                          (no_memory | remove_bridge | stale_memory | distractor_swap)
    """
    item_id: str
    source: str                              # personamem | locomo | perltqa | memoryarena | longmemeval
    scenario: str
    stored_context: List[str]
    query: str
    gold: str
    options: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    action_gold: Optional[str] = None
    question_type: str = "suggest_new"
    is_answerable: bool = True               # False -> abstention item (validity control)
    association_type: str = ""               # A1 / A2 / A3 / A4 / A5_absence_control
    counterfactual_probes: List[str] = field(default_factory=list)   # no_memory | remove_bridge | ...
    distractor_ids: List[str] = field(default_factory=list)   # session/turn ids of injected lures
    meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_mc(self) -> bool:
        return len(self.options) > 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BenchItem":
        known = BenchItem.__dataclass_fields__.keys()
        return BenchItem(**{k: v for k, v in d.items() if k in known})


@dataclass
class AgentAnswer:
    """What the agent returns for one item (the unit the judge scores)."""
    item_id: str
    answer: str                              # chosen option text or free-text inference
    chosen_option_idx: Optional[int] = None
    rationale: str = ""
    used_evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5                  # self-reported P(all constraints satisfied)
    action: Optional[str] = None             # proposed downstream action (memory_to_action)
    abstained: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

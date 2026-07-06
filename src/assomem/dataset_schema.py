"""Canonical dataset schema for associative-memory experiments.

This module defines the intermediate layer between messy source datasets
(LoCoMo, LongMemEval, LongBench, etc.) and the AssoMem benchmark.

The design is intentionally tailored to associative memory rather than generic
ETL:

* ``UnifiedData`` preserves source artifacts such as LongBench documents/code.
  Rationale: not every dataset is naturally conversational, and forcing every
  source into dialogue loses provenance.
* ``CanonicalConversation`` preserves session/turn structure.
  Rationale: LoCoMo and LongMemEval are evaluated through long-term interaction,
  so session and speaker boundaries must survive normalization.
* ``EvidenceSpan`` is the smallest grounding unit.
  Rationale: evidence recall and unsupported-path detection need tighter
  provenance than whole documents or turns.
* ``MemoryEvent`` is the atomic remembered content.
  Rationale: associative memory needs typed, temporal, polar, tagged memories,
  not just raw text chunks.
* ``RelationCandidate`` is first-class.
  Rationale: the research question depends on explicit association/path
  recovery, which ordinary retrieval QA does not test.
* ``BenchmarkCase`` binds query, candidates, answer, evidence, memories, and
  required paths into the downstream evaluation unit.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


SCHEMA_VERSION = "assomem-unified-v0.2"

OUTPUT_FILES = [
    "manifest.json",
    "unified_data.jsonl",
    "conversations.jsonl",
    "evidence_spans.jsonl",
    "memory_events.jsonl",
    "relation_candidates.jsonl",
    "benchmark_cases.jsonl",
]

DOWNSTREAM_FILES = [
    "memory_events.jsonl",
    "relation_candidates.jsonl",
    "benchmark_cases.jsonl",
]

MEMORY_TYPES = {
    "fact",
    "preference",
    "constraint",
    "goal",
    "habit",
    "event",
    "state",
    "temporal_update",
    "contradiction",
    "source_claim",
}

EVIDENCE_ROLES = {
    "memory_support",
    "answer_support",
    "relation_support",
    "temporal_update",
    "contradiction",
    "distractor",
    "query_context",
    "source_context",
}

RELATION_TYPES = {
    "tag_coactivation",
    "cross_domain_pattern",
    "latent_preference_completion",
    "constraint_binding",
    "temporal_update",
    "contradiction",
    "cause_effect",
    "goal_support",
    "source_answer_support",
    "abstention_boundary",
}

TASK_FAMILIES = {
    "single_memory_recall",
    "multi_session_reasoning",
    "temporal_update",
    "constraint_bound_association",
    "cross_domain_association",
    "source_grounded_qa",
    "contradiction_resolution",
    "abstention_when_under_evidenced",
}


def _clean_dict(value: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-friendly dict while keeping explicit False/0 values."""
    return {key: item for key, item in value.items() if item is not None}


@dataclass
class DatasetManifest:
    dataset_id: str
    adapter: str
    raw_access: Dict[str, Any]
    schema_version: str = SCHEMA_VERSION
    adapter_version: str = "0.1.0"
    created_at: str = ""
    counts: Dict[str, int] = field(default_factory=dict)
    file_hashes: Dict[str, str] = field(default_factory=dict)
    conversion_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class UnifiedData:
    data_id: str
    dataset_id: str
    source_record_id: str
    source_path: str
    data_type: str
    text: str
    title: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class Turn:
    turn_id: str
    role: str
    speaker_id: str
    text: str
    modality: str = "text"

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class Session:
    session_id: str
    turns: List[Turn]
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = _clean_dict(asdict(self))
        data["turns"] = [turn.to_dict() if hasattr(turn, "to_dict") else turn for turn in self.turns]
        return data


@dataclass
class CanonicalConversation:
    conversation_id: str
    dataset_id: str
    data_id: str
    source_record_id: str
    participant_ids: List[str]
    sessions: List[Session]
    conversion_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = _clean_dict(asdict(self))
        data["sessions"] = [
            session.to_dict() if hasattr(session, "to_dict") else session
            for session in self.sessions
        ]
        return data


@dataclass
class EvidenceSpan:
    span_id: str
    dataset_id: str
    conversation_id: str
    data_id: str
    session_id: str
    turn_id: str
    text: str
    evidence_role: str
    char_start: int = 0
    char_end: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class MemoryEvent:
    memory_id: str
    dataset_id: str
    conversation_id: str
    data_id: str
    subject_id: str
    memory_type: str
    content: str
    tags: List[str]
    evidence_span_ids: List[str]
    canonical_predicate: Dict[str, str] = field(default_factory=dict)
    polarity: int = 1
    salience: float = 0.7
    confidence: float = 0.7
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    temporal_status: str = "active"
    source_adapter: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class RelationCandidate:
    relation_id: str
    dataset_id: str
    conversation_id: str
    data_id: str
    source_memory_ids: List[str]
    source_tags: List[str]
    target_tag: str
    relation_type: str
    evidence_span_ids: List[str]
    target_memory_id: Optional[str] = None
    direction: str = "forward"
    weight: float = 0.5
    confidence: float = 0.5
    status: str = "auto_candidate"
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class CandidateAnswer:
    answer_id: str
    text: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _clean_dict(asdict(self))


@dataclass
class BenchmarkCase:
    case_id: str
    dataset_id: str
    conversation_id: str
    data_id: str
    query: str
    task_family: str
    candidates: List[CandidateAnswer]
    gold_answer_id: str
    retrieval_cues: List[str] = field(default_factory=list)
    acceptable_answer_ids: List[str] = field(default_factory=list)
    required_memory_ids: List[str] = field(default_factory=list)
    required_relation_ids: List[str] = field(default_factory=list)
    required_evidence_span_ids: List[str] = field(default_factory=list)
    required_path: List[str] = field(default_factory=list)
    distractor_memory_ids: List[str] = field(default_factory=list)
    allow_abstain: bool = False
    unsupported_if_no_path: bool = True
    source_task_type: str = "qa"
    question_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = _clean_dict(asdict(self))
        data["candidates"] = [
            candidate.to_dict() if hasattr(candidate, "to_dict") else candidate
            for candidate in self.candidates
        ]
        return data

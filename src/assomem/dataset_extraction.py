"""Evidence, memory, and relation extraction for normalized records."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .dataset_adapters import DatasetAdapter, as_text, normalize_role, stable_id
from .dataset_schema import (
    CanonicalConversation,
    EvidenceSpan,
    MemoryEvent,
    RelationCandidate,
    Session,
    Turn,
    UnifiedData,
)


SENTENCE_RE = re.compile(r"(?<=[.!?。！？])\s+")
NEGATIVE_RE = re.compile(
    r"\b(avoid|avoids|hate|hates|dislike|dislikes|allergic|sensitive|cannot|can't|never|no longer|not)\b",
    re.IGNORECASE,
)
PREFERENCE_RE = re.compile(
    r"\b(like|likes|love|loves|enjoy|enjoys|prefer|prefers|favorite|responds well)\b",
    re.IGNORECASE,
)
GOAL_RE = re.compile(r"\b(want|wants|goal|plan|plans|trying|hopes|needs)\b", re.IGNORECASE)
TEMPORAL_RE = re.compile(
    r"\b(now|recently|after|before|until|used to|no longer|changed|update|previously)\b",
    re.IGNORECASE,
)


def sentence_candidates(text: str, max_sentences: int = 8) -> List[str]:
    compact = " ".join(text.split())
    if not compact:
        return []
    pieces = SENTENCE_RE.split(compact)
    if len(pieces) == 1 and len(compact) > 320:
        pieces = [
            compact[index : index + 280]
            for index in range(0, min(len(compact), 2800), 280)
        ]
    result: List[str] = []
    for piece in pieces:
        cleaned = piece.strip()
        if 12 <= len(cleaned) <= 420:
            result.append(cleaned)
        if len(result) >= max_sentences:
            break
    return result


def infer_memory_type(text: str, role: str) -> Tuple[str, int, str]:
    if role == "source":
        return "source_claim", 1, "source_context"
    if NEGATIVE_RE.search(text):
        return "constraint", -1, "memory_support"
    if TEMPORAL_RE.search(text):
        return "temporal_update", 0, "temporal_update"
    if PREFERENCE_RE.search(text):
        return "preference", 1, "memory_support"
    if GOAL_RE.search(text):
        return "goal", 1, "memory_support"
    return "fact", 1, "memory_support"


def confidence_for(memory_type: str, text: str) -> float:
    if memory_type in {"preference", "constraint", "goal", "temporal_update"}:
        return 0.78
    return 0.65 if len(text) >= 40 else 0.55


def salience_for(memory_type: str, role: str) -> float:
    if memory_type in {"constraint", "temporal_update", "contradiction"}:
        return 0.92
    if memory_type in {"preference", "goal"}:
        return 0.86
    return 0.68 if role == "source" else 0.72


def extract_source_rows(
    adapter: DatasetAdapter,
    record: Dict[str, Any],
    source_path: Path,
    index: int,
) -> Tuple[UnifiedData, CanonicalConversation, List[EvidenceSpan], List[MemoryEvent], List[RelationCandidate]]:
    source_record_id = adapter.source_record_id(record, source_path, index)
    data_id = stable_id("data", adapter.dataset_id, source_path.as_posix(), source_record_id)
    conversation_id = stable_id("conv", adapter.dataset_id, source_record_id)
    context = adapter.context(record)
    question = adapter.question(record)

    unified_data = UnifiedData(
        data_id=data_id,
        dataset_id=adapter.dataset_id,
        source_record_id=source_record_id,
        source_path=source_path.as_posix(),
        data_type=adapter.data_type(record, context),
        title=as_text(adapter.source_record_id(record, source_path, index)),
        text=context or question or as_text(record),
        metadata={"original_fields": sorted(record.keys()), "adapter": adapter.dataset_id},
    )

    sessions, spans, memories = extract_conversation_memory(
        adapter=adapter,
        record=record,
        data_id=data_id,
        conversation_id=conversation_id,
    )
    conversation = CanonicalConversation(
        conversation_id=conversation_id,
        dataset_id=adapter.dataset_id,
        data_id=data_id,
        source_record_id=source_record_id,
        participant_ids=sorted({
            turn.speaker_id
            for session in sessions
            for turn in session.turns
            if turn.speaker_id
        }),
        sessions=sessions,
        conversion_notes=adapter.conversion_notes(),
    )
    relations = build_relation_candidates(adapter.dataset_id, conversation_id, data_id, memories)
    return unified_data, conversation, spans, memories, relations


def extract_conversation_memory(
    adapter: DatasetAdapter,
    record: Dict[str, Any],
    data_id: str,
    conversation_id: str,
) -> Tuple[List[Session], List[EvidenceSpan], List[MemoryEvent]]:
    sessions: List[Session] = []
    spans: List[EvidenceSpan] = []
    memories: List[MemoryEvent] = []
    fallback_timestamp = adapter.timestamp(record)

    for session_index, raw_turns in enumerate(adapter.sessions(record)):
        session_id = stable_id("session", conversation_id, session_index)
        timestamp = fallback_timestamp
        turns: List[Turn] = []
        for turn_index, raw_turn in enumerate(raw_turns):
            text = raw_turn["text"]
            role = normalize_role(raw_turn["role"])
            speaker_id = raw_turn.get("speaker_id") or role
            timestamp = raw_turn.get("timestamp") or timestamp
            turn_id = stable_id("turn", conversation_id, session_index, turn_index, text[:80])
            turns.append(Turn(turn_id=turn_id, role=role, speaker_id=speaker_id, text=text))

            max_sentences = 12 if role == "source" else 6
            for span_index, sentence in enumerate(sentence_candidates(text, max_sentences)):
                memory_type, polarity, evidence_role = infer_memory_type(sentence, role)
                if role == "assistant_reference":
                    evidence_role = "answer_support"
                if role == "assistant" and memory_type == "fact":
                    continue
                char_start = max(text.find(sentence), 0)
                span_id = stable_id("span", turn_id, span_index, sentence)
                spans.append(
                    EvidenceSpan(
                        span_id=span_id,
                        dataset_id=adapter.dataset_id,
                        conversation_id=conversation_id,
                        data_id=data_id,
                        session_id=session_id,
                        turn_id=turn_id,
                        char_start=char_start,
                        char_end=char_start + len(sentence),
                        text=sentence,
                        evidence_role=evidence_role,
                    )
                )
                if role == "assistant" and evidence_role != "answer_support":
                    continue
                tags = adapter.tags_for(sentence, record)
                memories.append(
                    MemoryEvent(
                        memory_id=stable_id("mem", conversation_id, span_id, memory_type),
                        dataset_id=adapter.dataset_id,
                        conversation_id=conversation_id,
                        data_id=data_id,
                        subject_id=speaker_id or "unknown_subject",
                        memory_type=memory_type,
                        content=sentence,
                        canonical_predicate={
                            "attribute": memory_type,
                            "value": "_".join(tags[:4]) if tags else "unlabeled",
                        },
                        tags=tags,
                        polarity=polarity,
                        salience=salience_for(memory_type, role),
                        confidence=confidence_for(memory_type, sentence),
                        valid_from=timestamp,
                        valid_to=None,
                        temporal_status="active",
                        evidence_span_ids=[span_id],
                        source_adapter=adapter.dataset_id,
                    )
                )
        sessions.append(Session(session_id=session_id, timestamp=timestamp, turns=turns))
    return sessions, spans, memories


def build_relation_candidates(
    dataset_id: str,
    conversation_id: str,
    data_id: str,
    memories: List[MemoryEvent],
) -> List[RelationCandidate]:
    relations: List[RelationCandidate] = []
    for left_index, left in enumerate(memories):
        for right in memories[left_index + 1 :]:
            common_tags = sorted(set(left.tags) & set(right.tags))
            relation_type = ""
            target_tag = ""
            confidence = 0.0
            if common_tags:
                relation_type = "tag_coactivation"
                target_tag = common_tags[0]
                confidence = 0.62
            elif "temporal_update" in {left.memory_type, right.memory_type}:
                relation_type = "temporal_update"
                target_tag = (left.tags or right.tags or ["temporal"])[0]
                confidence = 0.58
            elif "constraint" in {left.memory_type, right.memory_type}:
                relation_type = "constraint_binding"
                target_tag = (left.tags or right.tags or ["constraint"])[0]
                confidence = 0.57
            elif left.memory_type == right.memory_type == "preference":
                relation_type = "cross_domain_pattern"
                target_tag = "_".join((left.tags[:1] + right.tags[:1])[:2]) or "latent_preference"
                confidence = 0.54
            if not relation_type:
                continue
            relations.append(
                RelationCandidate(
                    relation_id=stable_id("rel", conversation_id, left.memory_id, right.memory_id, relation_type),
                    dataset_id=dataset_id,
                    conversation_id=conversation_id,
                    data_id=data_id,
                    source_memory_ids=[left.memory_id, right.memory_id],
                    source_tags=sorted(set(left.tags + right.tags))[:12],
                    target_tag=target_tag,
                    relation_type=relation_type,
                    evidence_span_ids=sorted(set(left.evidence_span_ids + right.evidence_span_ids)),
                    weight=round(confidence, 4),
                    confidence=round(confidence, 4),
                    rationale=f"Auto-derived {relation_type} from normalized memory events.",
                )
            )
            if len(relations) >= 64:
                return relations
    return relations

"""CLI orchestrator for dataset normalization and benchmark-case generation."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .dataset_adapters import (
    DatasetAdapter,
    adapter_for,
    as_text,
    first_field,
    load_records,
    tokenize,
)
from .dataset_extraction import extract_source_rows
from .dataset_schema import (
    SCHEMA_VERSION,
    BenchmarkCase,
    CandidateAnswer,
    DatasetManifest,
    MemoryEvent,
    RelationCandidate,
)


OUTPUT_JSONL = {
    "unified_data": "unified_data.jsonl",
    "conversations": "conversations.jsonl",
    "evidence_spans": "evidence_spans.jsonl",
    "memory_events": "memory_events.jsonl",
    "relation_candidates": "relation_candidates.jsonl",
    "benchmark_cases": "benchmark_cases.jsonl",
}

Bundle = Dict[str, List[Dict[str, Any]]]


def stable_case_id(dataset_id: str, *parts: object) -> str:
    raw = json.dumps(parts, ensure_ascii=True, sort_keys=True, default=str)
    return f"case_{hashlib.sha1((dataset_id + raw).encode('utf-8')).hexdigest()[:12]}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> List[Any]:
    rows: List[Any] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}") from exc
    return rows


def extract_choices(record: Dict[str, Any], answer: str) -> List[CandidateAnswer]:
    raw = first_field(record, ("candidates", "choices", "options", "all_classes"))
    values: List[str] = []
    if isinstance(raw, list):
        for item in raw:
            values.append(as_text(first_field(item, ("text", "answer", "label", "content")) if isinstance(item, dict) else item))
    if answer and answer not in values:
        values.insert(0, answer)
    if not values:
        values = [
            answer or "The answer is supported by the provided evidence.",
            "The context does not contain enough evidence to answer.",
            "A plausible distractor that is not supported by the evidence.",
        ]
    if len(values) == 1:
        values.extend([
            "The context does not contain enough evidence to answer.",
            "A plausible distractor that is not supported by the evidence.",
        ])
    return [
        CandidateAnswer(answer_id=chr(ord("A") + index), text=value, tags=tokenize(value, 6))
        for index, value in enumerate(values[:8])
    ]


def infer_gold_answer_id(candidates: List[CandidateAnswer], answer: str, allow_abstain: bool) -> str:
    if allow_abstain and not answer:
        return "INSUFFICIENT"
    answer_norm = answer.strip().lower()
    for candidate in candidates:
        text_norm = candidate.text.strip().lower()
        if answer_norm and (answer_norm == text_norm or answer_norm in text_norm):
            return candidate.answer_id
    return candidates[0].answer_id if candidates else "INSUFFICIENT"


def infer_task_family(
    dataset_id: str,
    memories: List[MemoryEvent],
    relations: List[RelationCandidate],
    allow_abstain: bool,
) -> str:
    if allow_abstain:
        return "abstention_when_under_evidenced"
    memory_types = {memory.memory_type for memory in memories}
    relation_types = {relation.relation_type for relation in relations}
    if "temporal_update" in memory_types or "temporal_update" in relation_types:
        return "temporal_update"
    if "constraint" in memory_types or "constraint_binding" in relation_types:
        return "constraint_bound_association"
    if "cross_domain_pattern" in relation_types:
        return "cross_domain_association"
    if dataset_id == "longbench":
        return "source_grounded_qa"
    return "single_memory_recall"


def build_benchmark_cases(
    adapter: DatasetAdapter,
    record: Dict[str, Any],
    source_record_id: str,
    data_id: str,
    conversation_id: str,
    memories: List[MemoryEvent],
    relations: List[RelationCandidate],
    answer_span_ids: List[str],
) -> List[BenchmarkCase]:
    question = adapter.question(record)
    answer = adapter.answer(record)
    if not question and not answer:
        return []
    allow_abstain = not bool(answer)
    candidates = extract_choices(record, answer)
    gold_answer_id = infer_gold_answer_id(candidates, answer, allow_abstain)
    query_tags = set(tokenize(question + " " + answer, 16))
    required_memories = [
        memory.memory_id
        for memory in memories
        if set(memory.tags) & query_tags or memory.memory_type in {"constraint", "temporal_update"}
    ][:8] or [memory.memory_id for memory in memories[:4]]
    required_memory_set = set(required_memories)
    required_relations = [
        relation.relation_id
        for relation in relations
        if required_memory_set & set(relation.source_memory_ids)
    ][:6]
    required_spans = sorted({
        span_id
        for memory in memories
        if memory.memory_id in required_memory_set
        for span_id in memory.evidence_span_ids
    } | set(answer_span_ids))
    return [
        BenchmarkCase(
            case_id=stable_case_id(adapter.dataset_id, source_record_id, question, answer),
            dataset_id=adapter.dataset_id,
            conversation_id=conversation_id,
            data_id=data_id,
            question_date=as_text(first_field(record, ("question_date", "date", "timestamp"))) or None,
            query=question,
            task_family=infer_task_family(adapter.dataset_id, memories, relations, allow_abstain),
            retrieval_cues=tokenize(question, 10),
            candidates=candidates,
            gold_answer_id=gold_answer_id,
            acceptable_answer_ids=[gold_answer_id] if gold_answer_id != "INSUFFICIENT" else [],
            required_memory_ids=required_memories,
            required_relation_ids=required_relations,
            required_evidence_span_ids=required_spans,
            required_path=required_memories[:2] + required_relations[:2],
            allow_abstain=allow_abstain,
            unsupported_if_no_path=bool(required_relations),
            source_task_type=as_text(first_field(record, ("task", "task_type", "category", "subset"))) or "qa",
        )
    ]


def normalize_record(adapter: DatasetAdapter, record: Dict[str, Any], path: Path, index: int) -> Bundle:
    data, conversation, spans, memories, relations = extract_source_rows(adapter, record, path, index)
    source_record_id = adapter.source_record_id(record, path, index)
    cases = build_benchmark_cases(
        adapter=adapter,
        record=record,
        source_record_id=source_record_id,
        data_id=data.data_id,
        conversation_id=conversation.conversation_id,
        memories=memories,
        relations=relations,
        answer_span_ids=[span.span_id for span in spans if span.evidence_role == "answer_support"],
    )
    return {
        "unified_data": [data.to_dict()],
        "conversations": [conversation.to_dict()],
        "evidence_spans": [span.to_dict() for span in spans],
        "memory_events": [memory.to_dict() for memory in memories],
        "relation_candidates": [relation.to_dict() for relation in relations],
        "benchmark_cases": [case.to_dict() for case in cases],
    }


def merge_outputs(chunks: Iterable[Bundle]) -> Bundle:
    merged: Bundle = {key: [] for key in OUTPUT_JSONL}
    key_by_kind = {
        "unified_data": "data_id",
        "conversations": "conversation_id",
        "evidence_spans": "span_id",
        "memory_events": "memory_id",
        "relation_candidates": "relation_id",
        "benchmark_cases": "case_id",
    }
    seen = {key: set() for key in OUTPUT_JSONL}
    for chunk in chunks:
        for kind, rows in chunk.items():
            id_key = key_by_kind[kind]
            for row in rows:
                row_id = row[id_key]
                if row_id in seen[kind]:
                    continue
                seen[kind].add(row_id)
                merged[kind].append(row)
    return merged


def validate_bundle(bundle: Bundle) -> List[str]:
    errors: List[str] = []
    data_ids = {row["data_id"] for row in bundle["unified_data"]}
    conversation_ids = {row["conversation_id"] for row in bundle["conversations"]}
    span_ids = {row["span_id"] for row in bundle["evidence_spans"]}
    memory_ids = {row["memory_id"] for row in bundle["memory_events"]}
    relation_ids = {row["relation_id"] for row in bundle["relation_candidates"]}
    for row in bundle["memory_events"]:
        missing = set(row["evidence_span_ids"]) - span_ids
        if missing:
            errors.append(f"memory {row['memory_id']} references missing spans {sorted(missing)}")
    for row in bundle["relation_candidates"]:
        missing_memories = set(row["source_memory_ids"]) - memory_ids
        missing_spans = set(row["evidence_span_ids"]) - span_ids
        if missing_memories:
            errors.append(f"relation {row['relation_id']} references missing memories {sorted(missing_memories)}")
        if missing_spans:
            errors.append(f"relation {row['relation_id']} references missing spans {sorted(missing_spans)}")
    for row in bundle["benchmark_cases"]:
        candidate_ids = {candidate["answer_id"] for candidate in row["candidates"]}
        if row["data_id"] not in data_ids:
            errors.append(f"case {row['case_id']} references missing data_id {row['data_id']}")
        if row["conversation_id"] not in conversation_ids:
            errors.append(f"case {row['case_id']} references missing conversation {row['conversation_id']}")
        if set(row["required_memory_ids"]) - memory_ids:
            errors.append(f"case {row['case_id']} references missing memories")
        if set(row["required_relation_ids"]) - relation_ids:
            errors.append(f"case {row['case_id']} references missing relations")
        if set(row["required_evidence_span_ids"]) - span_ids:
            errors.append(f"case {row['case_id']} references missing evidence spans")
        if row["gold_answer_id"] != "INSUFFICIENT" and row["gold_answer_id"] not in candidate_ids:
            errors.append(f"case {row['case_id']} gold answer not in candidates")
        if row["gold_answer_id"] == "INSUFFICIENT" and not row["allow_abstain"]:
            errors.append(f"case {row['case_id']} has abstain gold but allow_abstain=false")
    return errors


def write_bundle(
    out_dir: Path,
    dataset: str,
    input_path: Path,
    adapter: DatasetAdapter,
    bundle: Bundle,
) -> DatasetManifest:
    out_dir.mkdir(parents=True, exist_ok=True)
    for kind, filename in OUTPUT_JSONL.items():
        write_jsonl(out_dir / filename, bundle[kind])
    file_hashes = {filename: sha256_file(out_dir / filename) for filename in OUTPUT_JSONL.values()}
    manifest = DatasetManifest(
        dataset_id=adapter.dataset_id,
        adapter=adapter.dataset_id,
        raw_access={"type": "local_path", "path": input_path.as_posix(), "requested_dataset": dataset},
        created_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        counts={kind: len(rows) for kind, rows in bundle.items()},
        file_hashes=file_hashes,
        conversion_notes=[
            "Dataset-specific raw fields normalized into associative-memory canonical rows.",
            "Relation candidates are auto-derived and should be reviewed before final claims.",
        ],
    )
    write_json(out_dir / "manifest.json", manifest.to_dict())
    return manifest


def load_output_bundle(out_dir: Path) -> Bundle:
    return {kind: read_jsonl(out_dir / filename) for kind, filename in OUTPUT_JSONL.items()}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize datasets for AssoMem experiments")
    parser.add_argument("--dataset", choices=("locomo", "longmemeval", "longbench", "auto", "generic"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)

    if args.validate_only:
        bundle = load_output_bundle(args.out_dir)
        errors = validate_bundle(bundle)
        manifest_path = args.out_dir / "manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for filename, expected in manifest.get("file_hashes", {}).items():
                actual = sha256_file(args.out_dir / filename)
                if actual != expected:
                    errors.append(f"hash mismatch for {filename}: {actual} != {expected}")
        if errors:
            for error in errors:
                print(f"VALIDATION_ERROR={error}")
            return 2
        print("VALIDATION_STATUS=PASS")
        return 0

    records = load_records(args.input)
    if args.limit:
        records = records[: args.limit]
    adapter = adapter_for(args.dataset, records)
    bundle = merge_outputs(normalize_record(adapter, record, path, index) for record, path, index in records)
    errors = validate_bundle(bundle)
    if errors:
        for error in errors:
            print(f"VALIDATION_ERROR={error}")
        return 2
    manifest = write_bundle(args.out_dir, args.dataset, args.input, adapter, bundle)
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"dataset_id={manifest.dataset_id}")
    print(f"out_dir={args.out_dir}")
    print(f"counts={json.dumps(manifest.counts, sort_keys=True)}")
    print("VALIDATION_STATUS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

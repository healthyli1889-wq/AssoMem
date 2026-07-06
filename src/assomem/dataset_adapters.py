"""Dataset adapters for messy long-memory sources.

Adapters understand raw dataset shape. They do not decide final benchmark
labels; they expose source records as normalized source text, sessions, turns,
questions, answers, candidates, and provenance fields.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]{2,}")

STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "because",
    "but",
    "can",
    "does",
    "for",
    "from",
    "has",
    "have",
    "into",
    "not",
    "the",
    "their",
    "this",
    "that",
    "when",
    "with",
    "your",
}


def stable_id(prefix: str, *parts: object) -> str:
    raw = json.dumps(parts, ensure_ascii=True, sort_keys=True, default=str)
    return f"{prefix}_{hashlib.sha1(raw.encode('utf-8')).hexdigest()[:12]}"


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def first_field(record: Dict[str, Any], names: Tuple[str, ...]) -> Any:
    lowered = {key.lower(): key for key in record}
    for name in names:
        if name in record and record[name] not in (None, ""):
            return record[name]
        key = lowered.get(name.lower())
        if key and record[key] not in (None, ""):
            return record[key]
    return None


def tokenize(text: str, limit: int = 8) -> List[str]:
    tokens: List[str] = []
    for token in TOKEN_RE.findall(text.lower().replace("-", "_")):
        token = token.strip("_'")
        if len(token) < 3 or token in STOPWORDS:
            continue
        if token not in tokens:
            tokens.append(token)
        if len(tokens) >= limit:
            break
    return tokens


def normalize_role(value: Any) -> str:
    role = as_text(value).strip().lower()
    if role in {"assistant", "agent", "bot", "gpt", "ai"}:
        return "assistant"
    if role in {"source", "system", "document", "context"}:
        return "source"
    if role in {"reference", "assistant_reference"}:
        return "assistant_reference"
    return "user"


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


def expand_json_records(raw: Any) -> List[Any]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("data", "examples", "items", "records", "rows"):
            value = raw.get(key)
            if isinstance(value, list):
                return value
        return [raw]
    return [{"text": str(raw)}]


def load_records(input_path: Path) -> List[Tuple[Dict[str, Any], Path, int]]:
    files = (
        sorted(path for path in input_path.rglob("*") if path.suffix in {".json", ".jsonl"})
        if input_path.is_dir()
        else [input_path]
    )
    records: List[Tuple[Dict[str, Any], Path, int]] = []
    for path in files:
        rows = read_jsonl(path) if path.suffix == ".jsonl" else expand_json_records(json.loads(path.read_text()))
        for index, row in enumerate(rows):
            records.append((row if isinstance(row, dict) else {"text": str(row)}, path, index))
    return records


def turn_text(turn: Any) -> str:
    if isinstance(turn, str):
        return turn
    if isinstance(turn, dict):
        value = first_field(turn, ("text", "content", "message", "utterance", "value"))
        if value is not None:
            return as_text(value)
    return as_text(turn)


def turn_role(turn: Any, default: str) -> str:
    if isinstance(turn, dict):
        return normalize_role(first_field(turn, ("role", "speaker", "from", "author")) or default)
    return default


class DatasetAdapter:
    """Base adapter for LoCoMo, LongMemEval, LongBench, and similar JSON."""

    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id

    def source_record_id(self, record: Dict[str, Any], path: Path, index: int) -> str:
        value = first_field(record, ("id", "_id", "qid", "question_id", "sample_id", "conversation_id"))
        return as_text(value) if value is not None else f"{path.stem}_{index:06d}"

    def question(self, record: Dict[str, Any]) -> str:
        value = first_field(record, ("question", "query", "input", "prompt", "instruction"))
        if value is not None:
            return as_text(value)
        if self.dataset_id == "longbench":
            return "Answer the benchmark question from the provided long context."
        return ""

    def answer(self, record: Dict[str, Any]) -> str:
        value = first_field(record, ("answer", "answers", "output", "target", "label", "gold", "reference"))
        if isinstance(value, list):
            return as_text(value[0]) if value else ""
        return as_text(value)

    def context(self, record: Dict[str, Any]) -> str:
        value = first_field(
            record,
            ("context", "document", "documents", "article", "passage", "text", "content", "code"),
        )
        if isinstance(value, list):
            return "\n\n".join(as_text(item) for item in value)
        return as_text(value)

    def timestamp(self, record: Dict[str, Any]) -> str | None:
        value = first_field(record, ("timestamp", "date", "time", "created_at", "question_date"))
        return as_text(value) if value else None

    def data_type(self, record: Dict[str, Any], context: str) -> str:
        if self.dataset_id == "longbench":
            return "code" if "code" in record else "document"
        if first_field(record, ("sessions", "messages", "conversation", "history")) is not None:
            return "conversation"
        return "qa_record"

    def conversion_notes(self) -> List[str]:
        if self.dataset_id == "locomo":
            return ["Long-term conversation sessions preserved when present."]
        if self.dataset_id == "longmemeval":
            return ["Memory QA fields preserved; history converted to sessions."]
        if self.dataset_id == "longbench":
            return ["Long-context source wrapped as synthetic conversation turns."]
        return []

    def tags_for(self, text: str, record: Dict[str, Any]) -> List[str]:
        tags = tokenize(text, 8)
        for field in ("category", "task", "task_type", "subset"):
            value = first_field(record, (field,))
            if value:
                tag = re.sub(r"[^a-z0-9_]+", "_", as_text(value).lower()).strip("_")
                if tag and tag not in tags:
                    tags.append(tag)
        return tags[:10]

    def sessions(self, record: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
        session_value = first_field(record, ("sessions", "haystack_sessions", "chat_sessions"))
        if isinstance(session_value, list):
            sessions: List[List[Dict[str, Any]]] = []
            for session in session_value:
                turns = first_field(session, ("turns", "messages", "dialogue", "conversation", "history")) if isinstance(session, dict) else session
                raw_turns = turns if isinstance(turns, list) else []
                parsed = [
                    {
                        "role": turn_role(turn, "user" if index % 2 == 0 else "assistant"),
                        "speaker_id": as_text(first_field(turn, ("speaker_id", "speaker", "role")) if isinstance(turn, dict) else ""),
                        "text": turn_text(turn),
                        "timestamp": as_text(first_field(session, ("timestamp", "date", "time"))) if isinstance(session, dict) and first_field(session, ("timestamp", "date", "time")) else None,
                    }
                    for index, turn in enumerate(raw_turns)
                    if turn_text(turn).strip()
                ]
                if parsed:
                    sessions.append(parsed)
            if sessions:
                return sessions

        turns_value = first_field(record, ("turns", "messages", "dialogue", "conversation", "history", "chat_history"))
        if isinstance(turns_value, list):
            return [[
                {
                    "role": turn_role(turn, "user" if index % 2 == 0 else "assistant"),
                    "speaker_id": as_text(first_field(turn, ("speaker_id", "speaker", "role")) if isinstance(turn, dict) else ""),
                    "text": turn_text(turn),
                    "timestamp": self.timestamp(record),
                }
                for index, turn in enumerate(turns_value)
                if turn_text(turn).strip()
            ]]

        turns: List[Dict[str, Any]] = []
        context = self.context(record)
        question = self.question(record)
        answer = self.answer(record)
        if context:
            turns.append({"role": "source", "speaker_id": "source", "text": context, "timestamp": None})
        if question:
            turns.append({"role": "user", "speaker_id": "user", "text": question, "timestamp": None})
        if answer:
            turns.append({"role": "assistant_reference", "speaker_id": "reference", "text": answer, "timestamp": None})
        if not turns:
            turns.append({"role": "source", "speaker_id": "source", "text": as_text(record), "timestamp": None})
        return [turns]


def adapter_for(dataset: str, records: List[Tuple[Dict[str, Any], Path, int]]) -> DatasetAdapter:
    if dataset != "auto":
        return DatasetAdapter(dataset)
    haystack = " ".join(path.as_posix().lower() for _, path, _ in records[:5])
    if "locomo" in haystack:
        return DatasetAdapter("locomo")
    if "longmemeval" in haystack or "long_mem" in haystack:
        return DatasetAdapter("longmemeval")
    if "longbench" in haystack:
        return DatasetAdapter("longbench")
    return DatasetAdapter("generic")

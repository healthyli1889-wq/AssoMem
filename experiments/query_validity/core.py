"""Deterministic data preparation for the AssoMem query-validity experiment."""

from __future__ import annotations

import copy
import hashlib
import json
import random
import re
from pathlib import Path
from typing import Any

DOMAINS = ("work", "hobby", "health", "social", "finance")
ARMS = ("associative", "distractor", "absence")
CONDITION_NAMES = ("empty", "a_only", "b_only", "both", "distractor", "absence")
SAMPLE_RE = re.compile(r"AMB_[A-Z]+_u(?P<user>\d{2})_(?P<arm>\w+)_S(?P<scenario>\d+)\.json$")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sample_path(root: Path, domain: str, arm: str, user: int, scenario: int) -> Path:
    prefixes = {
        "work": "WL",
        "hobby": "HH",
        "health": "HD",
        "social": "SC",
        "finance": "FN",
    }
    return root / "src" / "data" / domain / arm / (
        f"AMB_{prefixes[domain]}_u{user:02d}_{arm}_S{scenario}.json"
    )


def load_balanced_selection(root: Path, seed: int = 17) -> list[dict[str, Any]]:
    """Select every domain/scenario exactly once and balance users 2x per domain."""
    rng = random.Random(seed)
    rows: list[dict[str, Any]] = []
    users = list(range(1, 11))
    for domain in DOMAINS:
        shuffled = users[:]
        rng.shuffle(shuffled)
        for scenario in range(1, 21):
            user = shuffled[(scenario - 1) % len(shuffled)]
            paths = {
                arm: _sample_path(root, domain, arm, user, scenario)
                for arm in ARMS
            }
            missing = [str(path) for path in paths.values() if not path.is_file()]
            if missing:
                raise FileNotFoundError("Missing paired arm files: " + ", ".join(missing))
            items = {arm: _json(path) for arm, path in paths.items()}
            _assert_pair_alignment(items, domain, user, scenario)
            rows.append({
                "selection_id": f"{domain}_u{user:02d}_S{scenario}",
                "domain": domain,
                "user_id": f"u{user:02d}",
                "scenario_id": f"S{scenario}",
                "user_index": user,
                "paths": {arm: str(path.relative_to(root)) for arm, path in paths.items()},
                "source_hashes": {
                    arm: hashlib.sha256(path.read_bytes()).hexdigest()
                    for arm, path in paths.items()
                },
            })
    return rows


def _assert_pair_alignment(items: dict[str, dict[str, Any]], domain: str, user: int, scenario: int) -> None:
    expected = f"S{scenario}"
    for arm, item in items.items():
        if item.get("pilot_arm") != arm:
            raise ValueError(f"{domain} u{user:02d} {expected}: wrong pilot_arm in {arm}")
        if item.get("provenance", {}).get("scenario_id") != expected:
            raise ValueError(f"{domain} u{user:02d} {expected}: scenario mismatch in {arm}")
    queries = {item.get("query") for item in items.values()}
    if len(queries) != 1:
        raise ValueError(f"{domain} u{user:02d} {expected}: paired arms have different queries")
    evidence_sets = {
        tuple(item.get("target_evidence_ids", []))
        for arm, item in items.items()
        if arm != "absence"
    }
    if evidence_sets != {("ev_A", "ev_B")}:
        raise ValueError(f"{domain} u{user:02d} {expected}: target evidence mismatch")


def _visible_context(item: dict[str, Any]) -> list[dict[str, Any]]:
    return copy.deepcopy(item["context"])


def _role_sessions(item: dict[str, Any], role: str) -> set[int]:
    return {
        int(sid) for sid, meta in item.get("annotation", {}).items()
        if meta.get("role_setup") == role
    }


def _replace_query(context: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    if not context:
        raise ValueError("Cannot replace query in an empty context")
    result = copy.deepcopy(context)
    result[-1]["dialogue"] = [{"role": "user", "content": query}]
    return result


def _without_sessions(context: list[dict[str, Any]], removed: set[int]) -> list[dict[str, Any]]:
    return [session for session in context if session["session_id"] not in removed]


def _condition_from_context(
    context: list[dict[str, Any]], query: str, condition: str
) -> dict[str, Any]:
    return {
        "condition": condition,
        "context": _replace_query(context, query),
        "query": query,
    }


def build_conditions(
    associative: dict[str, Any],
    distractor: dict[str, Any],
    absence: dict[str, Any],
    query: str,
) -> dict[str, dict[str, Any]]:
    """Build six evaluator-visible contexts without annotation or private metadata."""
    target_a = _role_sessions(associative, "target_evidence")
    if len(target_a) != 2:
        raise ValueError("Associative sample must expose exactly two target evidence sessions")
    ev_a_sid = next(
        int(sid) for sid, meta in associative["annotation"].items()
        if meta.get("evidence_id") == "ev_A"
    )
    ev_b_sid = next(
        int(sid) for sid, meta in associative["annotation"].items()
        if meta.get("evidence_id") == "ev_B"
    )
    pre_query = {session["session_id"] for session in associative["context"][:-1]}
    base = _visible_context(associative)
    distractor_context = _visible_context(distractor)
    absence_context = _visible_context(absence)
    contexts = {
        "empty": _without_sessions(base, pre_query),
        "a_only": _without_sessions(base, {ev_b_sid}),
        "b_only": _without_sessions(base, {ev_a_sid}),
        "both": base,
        "distractor": distractor_context,
        "absence": absence_context,
    }
    return {
        name: _condition_from_context(context, query, name)
        for name, context in contexts.items()
    }


def _strip_private(item: dict[str, Any]) -> dict[str, Any]:
    context = _visible_context(item)
    return {
        "user_id": item["persona"]["user_id"],
        "context": context,
    }


def redact_for_generator(item: dict[str, Any]) -> dict[str, Any]:
    """Keep original query as focus reference while hiding all gold annotations."""
    result = _strip_private(item)
    result["focus_reference"] = item["query"]
    result["instruction"] = (
        "Write a new natural English query with the same scenario focus. "
        "Do not repeat distinctive wording from the focus reference or evidence."
    )
    return result


def redact_for_validator(item: dict[str, Any], query: str, condition: str) -> dict[str, Any]:
    """Return only agent-visible fields for one condition."""
    result = _strip_private(item)
    result["query"] = query
    result["condition"] = condition
    return result


def validate_generated_payload(payload: dict[str, Any]) -> list[str]:
    required = ("query", "gold_answer", "required_elements")
    errors = [f"missing {key}" for key in required if not payload.get(key)]
    if not isinstance(payload.get("required_elements"), list):
        errors.append("required_elements must be a list")
    if payload.get("query") and len(payload["query"].split()) < 5:
        errors.append("query is too short")
    return errors

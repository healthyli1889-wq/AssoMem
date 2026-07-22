"""Materialize evaluator-only arms outside the immutable gold tree."""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import dataclass
from typing import Any

from dataset import PairedItem, solver_input
from profile import DatasetProfile


@dataclass(frozen=True)
class EvaluationArm:
    arm_id: str
    lineage: dict[str, Any]
    visible: dict[str, Any]
    ground_truth: dict[str, Any]


def _target_sessions(item: dict[str, Any], profile: DatasetProfile) -> list[int]:
    target_role = profile.evidence_roles["target"]
    return [
        int(session_id) for session_id, annotation in item[profile.annotation_field].items()
        if annotation.get("role_setup") == target_role
    ]


def _visible(item: dict[str, Any], query: str) -> dict[str, Any]:
    return solver_input(item, query)


def _evidence_contract(
    item: dict[str, Any], profile: DatasetProfile, sources: dict[str, str]
) -> dict[str, dict[str, str]]:
    contract: dict[str, dict[str, str]] = {}
    for annotation in item[profile.annotation_field].values():
        evidence_id = annotation.get("evidence_id")
        if evidence_id not in {"ev_A", "ev_B"}:
            continue
        contract[evidence_id] = {
            "fact": annotation.get("atomic_fact", ""),
            "source": sources.get(evidence_id, "missing"),
        }
    return contract


def _gold(
    item: dict[str, Any], expected_mode: str, evidence_contract: dict[str, dict[str, str]]
) -> dict[str, Any]:
    return {
        "gold_answer": item["gold_answer"],
        "required_elements": list(item["required_elements"]),
        "expected_mode": expected_mode,
        "evidence_contract": evidence_contract,
    }


def _remove_sessions(item: dict[str, Any], sessions: set[int]) -> dict[str, Any]:
    clone = copy.deepcopy(item)
    clone["context"] = [
        session for session in clone["context"] if session["session_id"] not in sessions
    ]
    return clone


def _session_text(session: dict[str, Any]) -> str:
    return " ".join(turn["content"] for turn in session["dialogue"])


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _no_target_audit(item: dict[str, Any], removed_sessions: set[int]) -> dict[str, Any]:
    removed = [
        _session_text(session) for session in item["context"]
        if session["session_id"] in removed_sessions
    ]
    visible = " ".join(
        _session_text(session) for session in item["context"]
        if session["session_id"] not in removed_sessions
    )
    normalized_visible = _normalized(visible)
    leaked = [
        text for text in removed
        if len(_normalized(text)) >= 40 and _normalized(text) in normalized_visible
    ]
    return {
        "removed_evidence_fingerprints": [
            hashlib.sha256(text.encode("utf-8")).hexdigest() for text in removed
        ],
        "exact_visible_leaks": len(leaked),
        "passed": not leaked,
    }


def _break_link(item: dict[str, Any], profile: DatasetProfile) -> dict[str, Any]:
    """Keep ev_B content but visibly make every turn a non-user source."""
    clone = copy.deepcopy(item)
    ev_b_session = next(
        int(session_id) for session_id, annotation in clone[profile.annotation_field].items()
        if annotation.get("evidence_id") == "ev_B"
    )
    for session in clone["context"]:
        if session["session_id"] != ev_b_session:
            continue
        for turn in session["dialogue"]:
            if turn["role"] == "user":
                turn["content"] = "Friend (not the user) said: " + turn["content"]
            else:
                turn["content"] = "Assistant replied to the friend: " + turn["content"]
    return clone


def materialize_arms(
    paired: PairedItem, profile: DatasetProfile, query: str
) -> dict[str, EvaluationArm]:
    base = paired.arms["associative"]
    target_sessions = set(_target_sessions(base, profile))
    no_target = _remove_sessions(base, target_sessions)
    broken = _break_link(base, profile)
    absence = paired.arms["absence"]
    distractor = paired.arms["distractor"]
    full_contract = _evidence_contract(base, profile, {"ev_A": "user", "ev_B": "user"})
    broken_contract = _evidence_contract(base, profile, {"ev_A": "user", "ev_B": "friend"})
    no_target_contract = _evidence_contract(base, profile, {"ev_A": "missing", "ev_B": "missing"})
    absence_contract = _evidence_contract(base, profile, {"ev_A": "user", "ev_B": "missing"})
    return {
        "full": EvaluationArm(
            "full", {"source": paired.filenames["associative"], "transform": "identity"},
            _visible(base, query), _gold(base, "answer", full_contract),
        ),
        "no_target": EvaluationArm(
            "no_target", {
                "source": paired.filenames["associative"],
                "removed_sessions": sorted(target_sessions),
                "leakage_audit": _no_target_audit(base, target_sessions),
            },
            _visible(no_target, query), _gold(base, "not_gold", no_target_contract),
        ),
        "broken_link": EvaluationArm(
            "broken_link", {"source": paired.filenames["associative"], "transform": "ev_B_to_friend"},
            _visible(broken, query), _gold(base, "not_gold", broken_contract),
        ),
        "distractor": EvaluationArm(
            "distractor", {"source": paired.filenames["distractor"], "transform": "shipped"},
            _visible(distractor, query), _gold(distractor, "answer", full_contract),
        ),
        "absence": EvaluationArm(
            "absence", {"source": paired.filenames["absence"], "transform": "shipped"},
            _visible(absence, query), _gold(absence, "abstain", absence_contract),
        ),
        "add_evidence": EvaluationArm(
            "add_evidence", {"source": paired.filenames["associative"], "transform": "restore_associative_twin"},
            _visible(base, query), _gold(base, "answer", full_contract),
        ),
    }

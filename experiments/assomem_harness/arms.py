"""Materialize evaluator-only arms outside the immutable gold tree."""

from __future__ import annotations

import copy
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


def _gold(item: dict[str, Any], expected_mode: str) -> dict[str, Any]:
    return {
        "gold_answer": item["gold_answer"],
        "required_elements": list(item["required_elements"]),
        "expected_mode": expected_mode,
    }


def _remove_sessions(item: dict[str, Any], sessions: set[int]) -> dict[str, Any]:
    clone = copy.deepcopy(item)
    clone["context"] = [
        session for session in clone["context"] if session["session_id"] not in sessions
    ]
    return clone


def _break_link(item: dict[str, Any], profile: DatasetProfile) -> dict[str, Any]:
    """Keep content but make ev_B explicitly attributable to a friend."""
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
                turn["content"] = "A friend told me: " + turn["content"]
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
    return {
        "full": EvaluationArm(
            "full", {"source": paired.filenames["associative"], "transform": "identity"},
            _visible(base, query), _gold(base, "answer"),
        ),
        "no_target": EvaluationArm(
            "no_target", {"source": paired.filenames["associative"], "removed_sessions": sorted(target_sessions)},
            _visible(no_target, query), _gold(base, "not_gold"),
        ),
        "broken_link": EvaluationArm(
            "broken_link", {"source": paired.filenames["associative"], "transform": "ev_B_to_friend"},
            _visible(broken, query), _gold(base, "not_gold"),
        ),
        "distractor": EvaluationArm(
            "distractor", {"source": paired.filenames["distractor"], "transform": "shipped"},
            _visible(distractor, query), _gold(distractor, "answer"),
        ),
        "absence": EvaluationArm(
            "absence", {"source": paired.filenames["absence"], "transform": "shipped"},
            _visible(absence, query), _gold(absence, "abstain"),
        ),
        "add_evidence": EvaluationArm(
            "add_evidence", {"source": paired.filenames["associative"], "transform": "restore_associative_twin"},
            _visible(base, query), _gold(base, "answer"),
        ),
    }

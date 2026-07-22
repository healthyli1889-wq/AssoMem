"""Run the query-only shortcut screen required before a vNext execution."""

from __future__ import annotations

from typing import Any

from protocol import solver_prompt
from profile import DatasetProfile


def run_zero_evidence_check(
    candidate: dict[str, Any],
    profile: DatasetProfile,
    solver: Any,
    call_model: Any,
    *,
    trials: int,
) -> dict[str, Any]:
    """Call the solver with no memories and reject target-positive guessing."""
    if trials < 1:
        raise ValueError("zero-evidence trials must be positive")
    visible = {"context": [], "query": candidate["query"]}
    attempts: list[dict[str, Any]] = []
    target_yes = 0
    valid = 0
    for index in range(trials):
        try:
            answer, usage = call_model(solver, solver_prompt(visible, profile))
        except (OSError, RuntimeError, ValueError) as exc:
            attempts.append({"trial": index + 1, "status": "solver_error", "error": str(exc)})
            continue
        decision = answer.get("decision")
        status = "valid" if decision in {"yes", "no"} else "invalid_response"
        if status == "valid":
            valid += 1
            target_yes += int(decision == "yes")
        attempts.append({
            "trial": index + 1,
            "status": status,
            "decision": decision,
            "response": answer,
            "solver_usage": usage,
        })
    false_positive_rate = target_yes / valid if valid else 1.0
    return {
        "check": "zero_evidence",
        "candidate_id": candidate["candidate_id"],
        "pair_id": candidate["pair_id"],
        "query_only": True,
        "context_session_count": 0,
        "trials_requested": trials,
        "valid_trials": valid,
        "target_yes_count": target_yes,
        "target_false_positive_rate": false_positive_rate,
        "pass": valid == trials and false_positive_rate == 0.0,
        "attempts": attempts,
    }

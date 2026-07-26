"""Run the query-only shortcut screen required before a vNext execution."""

from __future__ import annotations

from typing import Any

from protocol import score_prompt, solver_prompt
from profile import DatasetProfile
from workflow import validate_solver_answer, validate_validator_answer


def run_zero_evidence_check(
    candidate: dict[str, Any],
    profile: DatasetProfile,
    solver: Any,
    validator: Any,
    call_model: Any,
    *,
    trials: int,
) -> dict[str, Any]:
    """Call the solver with no memories and reject target-positive guessing."""
    if trials < 1:
        raise ValueError("zero-evidence trials must be positive")
    visible = {"context": [], "query": candidate["query"]}
    attempts: list[dict[str, Any]] = []
    target_positive = 0
    valid = 0
    ground_truth = {
        "target_proposition": candidate["answer_contract"]["target_proposition"],
        "allowed_decisions": candidate["answer_contract"]["allowed_decisions"],
        "decision_semantics": candidate["answer_contract"].get("decision_semantics", {}),
        "required_output_fields": candidate["answer_contract"]["required_output_fields"],
        "expected_mode": "withhold_C",
        "binary_decision": False,
        "required_elements": [],
        "rationale": "No memory evidence is visible.",
        "evidence_contract": {},
        "allowed_evidence_ids": [],
    }
    for index in range(trials):
        try:
            answer, usage = call_model(solver, solver_prompt(visible, profile))
        except (OSError, RuntimeError, ValueError) as exc:
            attempts.append({"trial": index + 1, "status": "solver_error", "error": str(exc)})
            break
        solver_error = validate_solver_answer(answer, profile)
        if solver_error:
            attempts.append({
                "trial": index + 1, "status": "invalid_response",
                "error": solver_error, "response": answer, "solver_usage": usage,
            })
            break
        try:
            judgment, validator_usage = call_model(
                validator,
                score_prompt(answer, ground_truth, profile, visible=visible),
            )
        except (OSError, RuntimeError, ValueError) as exc:
            attempts.append({
                "trial": index + 1, "status": "validator_error",
                "error": str(exc), "response": answer, "solver_usage": usage,
            })
            break
        validator_error = validate_validator_answer(judgment, profile)
        if validator_error:
            attempts.append({
                "trial": index + 1, "status": "invalid_validator_response",
                "error": validator_error, "response": answer, "validator": judgment,
                "solver_usage": usage, "validator_usage": validator_usage,
            })
            break
        valid += 1
        asserted = bool(judgment["target_asserted"])
        target_positive += int(asserted)
        attempts.append({
            "trial": index + 1,
            "status": "valid",
            "target_asserted": asserted,
            "response": answer,
            "solver_usage": usage,
            "validator": judgment,
            "validator_usage": validator_usage,
        })
    false_positive_rate = target_positive / valid if valid else 1.0
    return {
        "check": "zero_evidence",
        "candidate_id": candidate["candidate_id"],
        "pair_id": candidate["pair_id"],
        "query_only": True,
        "context_session_count": 0,
        "trials_requested": trials,
        "valid_trials": valid,
        "target_positive_count": target_positive,
        "target_false_positive_rate": false_positive_rate,
        "pass": valid == trials and false_positive_rate == 0.0,
        "attempts": attempts,
    }

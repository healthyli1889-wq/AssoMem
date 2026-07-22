"""Release-candidate validation for versioned Work vNext batches."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from behavior import controls_pass
from quality import CORE_CLAUSES, PASS_SCORE, deterministic_audit
from review import GATES, validate_human_gate
from schema import validate_candidate


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_release_candidate(candidate_path: Path) -> list[str]:
    """Reject any candidate that lacks every deterministic, model, and human gate."""
    candidate = _load(candidate_path)
    root = candidate_path.parents[1] / "artifacts" / candidate_path.stem
    errors = validate_candidate(candidate)
    if candidate.get("provenance", {}).get("release_eligible") is False:
        errors.append("candidate is quarantined and cannot enter the release pipeline")
    if not deterministic_audit(candidate)["pass"]:
        errors.append("deterministic audit does not pass")

    evaluator_path = root / "independent_evaluator.json"
    if not evaluator_path.exists():
        errors.append("independent evaluator artifact missing")
    else:
        evaluator = _load(evaluator_path)
        if not evaluator.get("pass"):
            errors.append("independent evaluator does not pass")
        scores = evaluator.get("verdict", {}).get("clause_scores", {})
        if any(scores.get(clause, 0) < PASS_SCORE for clause in CORE_CLAUSES):
            errors.append("one or more independent evaluator clauses below threshold")

    for gate in GATES:
        try:
            validate_human_gate(root / "review" / f"{gate}.csv", candidate["candidate_id"], gate)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    behavior_path = root / "behavioral_proof.json"
    if not behavior_path.exists():
        errors.append("behavioral proof artifact missing")
    else:
        if not controls_pass(_load(behavior_path)):
            errors.append("behavioral controls do not pass")
    return errors


def validate_batch(candidate_paths: list[Path]) -> dict[str, Any]:
    """Validate every candidate and enforce release-level taxonomy/polarity quotas."""
    candidates = [_load(path) for path in candidate_paths]
    errors = {path.name: validate_release_candidate(path) for path in candidate_paths}
    type_counts = Counter(candidate["query_type"] for candidate in candidates)
    polarity_counts = Counter(candidate["polarity"] for candidate in candidates)
    max_allowed = 0.4 * len(candidates)
    quota_errors = [
        f"query_type {name} exceeds 40% batch quota" for name, count in type_counts.items() if count > max_allowed
    ] + [
        f"polarity {name} exceeds 40% batch quota" for name, count in polarity_counts.items() if count > max_allowed
    ]
    return {
        "candidate_errors": errors,
        "query_type_counts": dict(type_counts),
        "polarity_counts": dict(polarity_counts),
        "quota_errors": quota_errors,
        "pass": not quota_errors and all(not error_list for error_list in errors.values()),
    }

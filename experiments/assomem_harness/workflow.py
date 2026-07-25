"""Pure deterministic post-processing for validator-produced answer scores."""

from __future__ import annotations

from scoring import rea_item
from profile import DatasetProfile


def validate_solver_answer(answer: dict, profile: DatasetProfile | None = None) -> str | None:
    if profile and profile.data_format in {"work-vnext-1", "assomem-vnext-1"}:
        decision = answer.get("decision")
        if decision not in {"yes", "no"}:
            return "response decision must be exactly yes or no"
        evidence_ids = answer.get("evidence_session_ids")
        if not isinstance(evidence_ids, list) or not all(isinstance(value, int) for value in evidence_ids):
            return "response evidence_session_ids must be a list of integers"
    value = answer.get("answer")
    if not isinstance(value, str):
        return "response must contain an answer string"
    if not value.strip():
        return "response answer is empty"
    return None


def score_solver_answer(
    verdict: dict,
    answer: dict | None = None,
    ground_truth: dict | None = None,
    profile: DatasetProfile | None = None,
) -> dict[str, int | bool]:
    element_records = verdict.get("required_elements", [])
    hits = (
        [bool(element.get("hit")) for element in element_records]
        if element_records
        else [bool(hit) for hit in verdict.get("element_hits", [])]
    )
    evidence_usage = verdict.get("evidence_usage", {})
    cited = int(evidence_usage.get("h_k", verdict.get("cited_evidence_count", 0)))
    abstention = verdict.get("abstention", {})
    abstains = bool(abstention.get("abstains", verdict.get("abstains")))
    absent_assertion = bool(
        abstention.get("asserts_absent_pattern", verdict.get("asserts_absent_pattern"))
    )
    source_misattribution = bool(
        evidence_usage.get("source_misattribution", verdict.get("source_misattribution"))
    )
    condition_correct = bool(verdict.get("condition_correct"))
    score = {
        "rea": rea_item(hits),
        "jer": int(cited >= 2),
        "h_k": max(0, min(2, cited)),
        "abstains": abstains,
        "asserts_absent_pattern": absent_assertion,
        "source_misattribution": source_misattribution,
        "condition_correct": condition_correct,
        "abc": int(abstains and not absent_assertion),
    }
    if profile and profile.data_format in {"work-vnext-1", "assomem-vnext-1"}:
        if answer is None or ground_truth is None:
            raise ValueError("vNext scoring requires solver answer and binary ground truth")
        expected = "yes" if ground_truth["binary_decision"] else "no"
        score["binary_correct"] = int(answer["decision"] == expected)
        score["binary_decision_correct"] = bool(verdict.get("binary_decision_correct"))
    return score

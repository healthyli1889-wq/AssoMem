"""Pure deterministic post-processing for validator-produced answer scores."""

from __future__ import annotations

from scoring import rea_item


def validate_solver_answer(answer: dict) -> str | None:
    value = answer.get("answer")
    if not isinstance(value, str):
        return "response must contain an answer string"
    if not value.strip():
        return "response answer is empty"
    return None


def score_solver_answer(verdict: dict) -> dict[str, int | bool]:
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
    return {
        "rea": rea_item(hits),
        "jer": int(cited >= 2),
        "h_k": max(0, min(2, cited)),
        "abstains": abstains,
        "asserts_absent_pattern": absent_assertion,
        "source_misattribution": source_misattribution,
        "condition_correct": condition_correct,
        "abc": int(abstains and not absent_assertion),
    }

"""Pure deterministic post-processing for validator-produced answer scores."""

from __future__ import annotations

from scoring import rea_item
from profile import DatasetProfile


def validate_solver_answer(answer: dict, profile: DatasetProfile | None = None) -> str | None:
    if profile and profile.data_format == "work-vnext-1":
        if set(answer) != {"mode", "answer", "evidence_session_ids"}:
            return "response must contain exactly mode, answer, and evidence_session_ids"
        mode = answer.get("mode")
        if mode not in {"answer", "withhold"}:
            return "response mode must be exactly answer or withhold"
        evidence_ids = answer.get("evidence_session_ids")
        if not isinstance(evidence_ids, list) or not all(isinstance(value, int) for value in evidence_ids):
            return "response evidence_session_ids must be a list of integers"
        if len(evidence_ids) != len(set(evidence_ids)):
            return "response evidence_session_ids must not contain duplicates"
    value = answer.get("answer")
    if not isinstance(value, str):
        return "response must contain an answer string"
    if not value.strip():
        return "response answer is empty"
    return None


def validate_validator_answer(verdict: dict, profile: DatasetProfile | None = None) -> str | None:
    if not profile or profile.data_format != "work-vnext-1":
        return None
    expected_keys = {
        "target_asserted", "target_evidence_grounded", "evidence_usage",
        "abstention", "condition_correct", "failure_tags", "reason",
    }
    if set(verdict) != expected_keys:
        return "validator response has missing or unexpected top-level fields"
    for key in ("target_asserted", "target_evidence_grounded", "condition_correct"):
        if type(verdict.get(key)) is not bool:
            return f"validator {key} must be boolean"
    evidence = verdict.get("evidence_usage")
    if not isinstance(evidence, dict) or set(evidence) != {
        "ev_A_used", "ev_B_used", "h_k", "source_misattribution"
    }:
        return "validator evidence_usage has invalid fields"
    for key in ("ev_A_used", "ev_B_used", "source_misattribution"):
        if type(evidence.get(key)) is not bool:
            return f"validator evidence_usage.{key} must be boolean"
    if type(evidence.get("h_k")) is not int or evidence["h_k"] not in {0, 1, 2}:
        return "validator evidence_usage.h_k must be 0, 1, or 2"
    abstention = verdict.get("abstention")
    if not isinstance(abstention, dict) or set(abstention) != {
        "abstains", "asserts_absent_pattern"
    }:
        return "validator abstention has invalid fields"
    if any(type(abstention.get(key)) is not bool for key in abstention):
        return "validator abstention fields must be boolean"
    if not isinstance(verdict.get("failure_tags"), list) or not all(
        isinstance(tag, str) for tag in verdict["failure_tags"]
    ):
        return "validator failure_tags must be a list of strings"
    if not isinstance(verdict.get("reason"), str) or not verdict["reason"].strip():
        return "validator reason must be a non-empty string"
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
    if profile and profile.data_format == "work-vnext-1":
        if answer is None or ground_truth is None:
            raise ValueError("vNext scoring requires solver answer and binary ground truth")
        allowed = set(ground_truth.get("allowed_evidence_ids", []))
        used = {
            evidence_id
            for evidence_id, key in (("ev_A", "ev_A_used"), ("ev_B", "ev_B_used"))
            if bool(evidence_usage.get(key))
        }
        evidence_allowed = used <= allowed
        target_asserted = bool(verdict["target_asserted"])
        target_grounded = bool(verdict["target_evidence_grounded"])
        if ground_truth["expected_mode"] == "infer_C":
            binary_correct = target_asserted and target_grounded and evidence_allowed
        elif ground_truth["expected_mode"] == "withhold_C":
            binary_correct = not target_asserted and evidence_allowed
        else:
            raise ValueError(f"unsupported vNext expected_mode: {ground_truth['expected_mode']}")
        score["binary_correct"] = int(binary_correct)
        score["binary_decision_correct"] = binary_correct
        score["condition_correct"] = binary_correct
        score["target_asserted"] = target_asserted
        score["target_evidence_grounded"] = target_grounded
        score["evidence_allowed"] = evidence_allowed
    return score

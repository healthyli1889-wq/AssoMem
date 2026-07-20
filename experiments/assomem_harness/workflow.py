"""Pure deterministic post-processing for validator-produced answer scores."""

from __future__ import annotations

from scoring import rea_item


def score_solver_answer(verdict: dict) -> dict[str, int | bool]:
    hits = [bool(hit) for hit in verdict.get("element_hits", [])]
    cited = int(verdict.get("cited_evidence_count", 0))
    abstains = bool(verdict.get("abstains"))
    absent_assertion = bool(verdict.get("asserts_absent_pattern"))
    return {
        "rea": rea_item(hits),
        "jer": int(cited >= 2),
        "h_k": max(0, min(2, cited)),
        "abstains": abstains,
        "asserts_absent_pattern": absent_assertion,
        "abc": int(abstains and not absent_assertion),
    }

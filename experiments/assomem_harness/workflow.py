"""Pure decision logic shared by query acceptance and answer scoring."""

from __future__ import annotations

from typing import Any

from scoring import rea_item


def accept_candidate(verdict: dict[str, Any]) -> bool:
    table = verdict.get("answer_table", {})
    return bool(
        verdict.get("accept")
        and not table.get("prior", True)
        and not table.get("ev_a_only", True)
        and not table.get("ev_b_only", True)
        and table.get("full", False)
        and verdict.get("gold_supported")
        and verdict.get("required_elements_supported")
        and all(verdict["required_elements_supported"])
    )


def score_solver_answer(verdict: dict[str, Any]) -> dict[str, int | bool]:
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

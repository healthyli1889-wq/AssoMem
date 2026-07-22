"""Human-gate packets and validators for Work vNext."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from quality import CORE_CLAUSES
from schema import CORE_ARMS, render_arms


GATES = ("gate_0", "gate_1", "gate_2", "gate_3", "gate_4", "gate_5")
GATE_CLAUSES = {
    "gate_0": (
        "construct_definition",
        "arm_semantics",
        "query_taxonomy",
        "scoring_rubric",
    ),
    "gate_1": (
        "ev_A",
        "ev_B",
        "coactivation_bridge",
        "latent_C",
        "query",
        "all_arm_gold",
    ),
    "gate_2": CORE_CLAUSES,
    "gate_3": (
        "full_rendered_text",
        "a_only_rendered_text",
        "b_only_rendered_text",
        "link_broken_rendered_text",
    ),
    "gate_4": (
        "full_behavior",
        "a_only_behavior",
        "b_only_behavior",
        "link_broken_behavior",
        "judge_reliability",
    ),
    "gate_5": (
        "schema_and_prompt_hashes",
        "model_and_rubric_hashes",
        "learning_record",
        "signed_exemplar_package",
    ),
}
SCENARIO_GATE_0_CLAUSES = (
    "behavioral_proxy_boundary",
    "episode_A_is_insufficient",
    "episode_B_is_insufficient",
    "visible_relational_connector",
    "calibrated_latent_C",
    "natural_retrieval_cue_Q",
    "full_arm_semantics",
    "a_only_arm_semantics",
    "b_only_arm_semantics",
    "link_broken_matched_connector_change",
    "no_generic_prior_shortcut",
    "no_source_or_format_confound",
)


def write_gate_template(candidate: dict[str, Any], gate: str, path: Path) -> None:
    if gate not in GATES:
        raise ValueError(f"unknown gate: {gate}")
    path.parent.mkdir(parents=True, exist_ok=True)
    clauses = list(GATE_CLAUSES[gate])
    if {"distractor", "absence"}.issubset(candidate.get("arm_gold", {})):
        if gate == "gate_3":
            clauses.extend(("distractor_rendered_text", "absence_rendered_text"))
        elif gate == "gate_4":
            clauses.extend(("distractor_behavior", "absence_behavior"))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("candidate_id", "gate", "clause", "human_pass", "reviewer", "notes"),
        )
        writer.writeheader()
        for clause in clauses:
            writer.writerow(
                {
                    "candidate_id": candidate["candidate_id"],
                    "gate": gate,
                    "clause": clause,
                    "human_pass": "",
                    "reviewer": "",
                    "notes": "",
                }
            )


def validate_human_gate(path: Path, candidate_id: str, gate: str) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = GATE_CLAUSES[gate]
    decisions = {
        row.get("clause", ""): row.get("human_pass", "").strip().lower()
        for row in rows
        if row.get("candidate_id") == candidate_id and row.get("gate") == gate
    }
    missing = [clause for clause in expected if decisions.get(clause) not in {"pass", "yes", "true"}]
    if missing:
        raise ValueError(f"{gate} is incomplete or failed: {', '.join(missing)}")


def validate_scenario_gate_0(path: Path, review_unit: str) -> None:
    """Require an approved construct before any candidate is authored or evaluated."""
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    decisions = {
        row.get("clause", ""): row.get("human_pass", "").strip().lower()
        for row in rows
        if row.get("review_unit") == review_unit and row.get("gate") == "gate_0"
    }
    missing = [
        clause
        for clause in SCENARIO_GATE_0_CLAUSES
        if decisions.get(clause) not in {"pass", "yes", "true"}
    ]
    if missing:
        raise ValueError(f"scenario Gate 0 is incomplete or failed: {', '.join(missing)}")


def write_review_packet(
    candidate: dict[str, Any],
    deterministic: dict[str, Any],
    output_path: Path,
) -> None:
    """Write a human-readable packet containing rendered solver-visible arms."""
    rendered = render_arms(candidate)
    evidence = candidate["evidence"]
    lines = [
        f"# Review packet — {candidate['candidate_id']}",
        "",
        "## Candidate",
        f"- User: `{candidate['user_id']}`",
        f"- Query type: `{candidate['query_type']}`",
        f"- Polarity: `{candidate['polarity']}`",
        f"- Query: {candidate['query']}",
        f"- Latent C: {candidate['latent_C']['inference']}",
        f"- Calibrated wording: {candidate['latent_C']['calibrated_language']}",
        "",
        "## Co-activation claim",
        f"- ev_A (session {evidence['ev_A']['session_id']}): {evidence['ev_A']['fact']}",
        f"- ev_B (session {evidence['ev_B']['session_id']}): {evidence['ev_B']['fact']}",
        f"- Bridge: {candidate['coactivation_bridge']}",
        "",
        "## Deterministic audit",
        "```json",
        json.dumps(deterministic, ensure_ascii=False, indent=2),
        "```",
    ]
    for arm in rendered:
        payload = rendered[arm]
        lines.extend(
            [
                "",
                f"## Arm: `{arm}`",
                f"- Expected mode: `{payload['expected_mode']}`",
                f"- Lineage: `{json.dumps(payload['lineage'], ensure_ascii=False)}`",
                "```json",
                json.dumps({"context": payload["context"], "query": payload["query"]}, ensure_ascii=False, indent=2),
                "```",
                f"- Why original C is or is not licensed: {candidate['arm_gold'][arm]['rationale']}",
            ]
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

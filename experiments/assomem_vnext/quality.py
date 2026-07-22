"""Strict deterministic and independent-model quality evaluation for vNext."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from schema import QUERY_TYPES, render_arms, validate_candidate

CLIENT_ROOT = Path(__file__).resolve().parents[1] / "query_validity"
sys.path.insert(0, str(CLIENT_ROOT))
from clients import ModelConfig, call_model_with_usage, config_from_env  # noqa: E402


CORE_CLAUSES = (
    "same_person_temporal_separation",
    "a_only_insufficiency",
    "b_only_insufficiency",
    "joint_support_for_C",
    "C_novelty_no_leakage",
    "query_natural_recall_trigger",
    "link_broken_validity",
    "gold_scoreability",
    "query_taxonomy_compliance",
)
PASS_SCORE = 96


def deterministic_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    """Audit falsifiable structure without claiming semantic construct validity."""
    failures = validate_candidate(candidate)
    scores: dict[str, int | None] = {
        "same_person_temporal_separation": 100,
        "a_only_insufficiency": None,
        "b_only_insufficiency": None,
        "joint_support_for_C": None,
        "C_novelty_no_leakage": 100,
        "query_natural_recall_trigger": None,
        "link_broken_validity": 100,
        "gold_scoreability": 100,
        "query_taxonomy_compliance": 100,
    }
    evidence = candidate.get("evidence", {})
    if failures:
        for failure in failures:
            if "owner" in failure or "temporally" in failure:
                scores["same_person_temporal_separation"] = 0
            if "leaked" in failure:
                scores["C_novelty_no_leakage"] = 0
            if "link_broken" in failure:
                scores["link_broken_validity"] = 0
            if "arm_gold" in failure or "expected_mode" in failure:
                scores["gold_scoreability"] = 0
            if "query_type" in failure:
                scores["query_taxonomy_compliance"] = 0
    if evidence.get("ev_A", {}).get("session_id") == evidence.get("ev_B", {}).get("session_id"):
        scores["a_only_insufficiency"] = 0
        scores["b_only_insufficiency"] = 0
        scores["joint_support_for_C"] = 0
    try:
        arms = render_arms(candidate)
        if len(arms["a_only"]["context"]) >= len(arms["full"]["context"]):
            scores["a_only_insufficiency"] = 0
        if len(arms["b_only"]["context"]) >= len(arms["full"]["context"]):
            scores["b_only_insufficiency"] = 0
        if not arms["link_broken"]["lineage"]["source_owner_preserved"]:
            scores["link_broken_validity"] = 0
    except ValueError:
        pass
    return {
        "kind": "deterministic",
        "scores": scores,
        "unscored_semantic_clauses": [
            clause for clause, score in scores.items() if score is None
        ],
        "failures": failures,
        "pass": not failures and all(
            score is None or score >= PASS_SCORE for score in scores.values()
        ),
    }


def evaluator_prompt(candidate: dict[str, Any], rendered: dict[str, Any]) -> str:
    clauses = "\n".join(f"- {name}" for name in CORE_CLAUSES)
    payload = {
        "candidate": candidate,
        "rendered_arms": rendered,
        "threshold": PASS_SCORE,
    }
    return f"""You are an independent, hostile quality auditor for a same-person
associative-memory benchmark. Do not reward polished prose or a plausible answer
unless the candidate actually meets every construct requirement.

Score EACH clause from 0 to 100 and cite exact session IDs/text spans:
{clauses}

Definitions:
- A-only and B-only must each be insufficient for latent C.
- Joint support means A+B jointly support a calibrated novel C.
- link_broken must preserve the same user and matched structure while invalidating
  the relation that licenses C. Source swap is optional and outside this four-arm run.
- Query naturalness means Q is a realistic reason to retrieve this person's memories,
  not a disguised request to restate C.

Return exactly one JSON object:
{{
  "clause_scores": {{{", ".join(f'"{name}": 0' for name in CORE_CLAUSES)}}},
  "evidence_spans": [{{"clause": str, "session_ids": [int], "quote": str}}],
  "failure_tags": [str],
  "revision_instructions": [str],
  "overall_verdict": "pass" | "fail"
}}

The overall verdict is pass ONLY when every clause score is at least {PASS_SCORE}.
Candidate and rendered solver-visible arms:
{json.dumps(payload, ensure_ascii=False, sort_keys=True)}
"""


def validate_evaluator_verdict(verdict: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    scores = verdict.get("clause_scores")
    if not isinstance(scores, dict):
        return ["clause_scores must be an object"]
    if set(scores) != set(CORE_CLAUSES):
        errors.append("clause_scores keys do not exactly match core clauses")
    for clause in CORE_CLAUSES:
        score = scores.get(clause)
        if not isinstance(score, int) or not 0 <= score <= 100:
            errors.append(f"{clause} must be an integer 0..100")
    if not isinstance(verdict.get("evidence_spans"), list):
        errors.append("evidence_spans must be a list")
    if verdict.get("overall_verdict") not in {"pass", "fail"}:
        errors.append("overall_verdict must be pass or fail")
    if not errors:
        expected = all(scores[clause] >= PASS_SCORE for clause in CORE_CLAUSES)
        if (verdict["overall_verdict"] == "pass") != expected:
            errors.append("overall_verdict conflicts with per-clause threshold")
    return errors


def load_quality_model() -> ModelConfig:
    return config_from_env("ASSOMEM_QUALITY")


def independent_audit(candidate: dict[str, Any], config: ModelConfig | None = None) -> dict[str, Any]:
    """Run a separately configured quality model; it is never the solver/judge."""
    deterministic = deterministic_audit(candidate)
    if not deterministic["pass"]:
        return {
            "kind": "independent_model",
            "status": "skipped_deterministic_failure",
            "deterministic": deterministic,
        }
    config = config or load_quality_model()
    solver = config_from_env("ASSOMEM_SOLVER")
    validator = config_from_env("ASSOMEM_VALIDATOR")
    forbidden = {solver.model.lower(), validator.model.lower()}
    if config.model.lower() in forbidden:
        raise ValueError(
            "ASSOMEM_QUALITY_MODEL must differ from both solver and validator models"
        )
    rendered = render_arms(candidate)
    verdict, usage = call_model_with_usage(config, evaluator_prompt(candidate, rendered))
    errors = validate_evaluator_verdict(verdict)
    scores = verdict.get("clause_scores", {})
    return {
        "kind": "independent_model",
        "status": "invalid_verdict" if errors else "completed",
        "model": config.model,
        "usage": usage,
        "verdict": verdict,
        "validation_errors": errors,
        "minimum_score": min(scores.values()) if scores else 0,
        "pass": not errors and all(scores[name] >= PASS_SCORE for name in CORE_CLAUSES),
    }

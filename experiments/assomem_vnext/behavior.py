"""Guarded single-item behavioral proof for the vNext core arms."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from review import validate_human_gate
from schema import CORE_ARMS, render_arms

CLIENT_ROOT = Path(__file__).resolve().parents[1] / "query_validity"
sys.path.insert(0, str(CLIENT_ROOT))
from clients import call_model_with_usage, config_from_env  # noqa: E402


def _solver_prompt(payload: dict[str, Any]) -> str:
    return f"""Answer a personalized work question from the provided memory only.
Use calibrated language. Never treat a memory owned by another person as evidence
about the user. Return JSON only: {{"answer": string, "evidence_session_ids": [int],
"withheld": boolean}}.

Memory and question:
{json.dumps({"context": payload["context"], "query": payload["query"]}, ensure_ascii=False)}
"""


def _judge_prompt(
    candidate: dict[str, Any], arm: str, answer: dict[str, Any], payload: dict[str, Any]
) -> str:
    gold = candidate["arm_gold"][arm]
    return f"""Judge an answer for a controlled associative-memory benchmark.
Return JSON only:
{{"condition_correct": boolean, "asserts_original_C": boolean,
"evidence_grounded": boolean, "calibrated": boolean, "source_misattribution": boolean,
"rationale": string}}.

Arm: {arm}
Expected mode: {gold["expected_mode"]}
Required elements: {gold["required_elements"]}
Why: {gold["rationale"]}
Visible input: {json.dumps(payload, ensure_ascii=False)}
Solver answer: {json.dumps(answer, ensure_ascii=False)}
"""


def _now() -> str:
    return datetime.now(UTC).isoformat()


def run_behavioral_proof(candidate: dict[str, Any], artifact_root: Path) -> list[dict[str, Any]]:
    """Run only after rendered-arm human approval; append one durable record per arm."""
    if candidate.get("provenance", {}).get("release_eligible") is False:
        raise ValueError("quarantined pre-Gate-0 illustration cannot enter behavioral proof")
    for gate in ("gate_1", "gate_2", "gate_3"):
        validate_human_gate(
            artifact_root / "review" / f"{gate}.csv", candidate["candidate_id"], gate
        )
    solver = config_from_env("ASSOMEM_SOLVER")
    validator = config_from_env("ASSOMEM_VALIDATOR")
    if solver.model.lower() == validator.model.lower():
        raise ValueError("solver and validator must be distinct")

    attempts = artifact_root / "attempts"
    records_dir = artifact_root / "records"
    attempts.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for arm, payload in render_arms(candidate).items():
        attempt_path = attempts / f"{arm}.json"
        record: dict[str, Any] = {
            "arm": arm,
            "expected_mode": payload["expected_mode"],
            "started_at": _now(),
            "status": "started",
        }
        try:
            answer, solver_usage = call_model_with_usage(solver, _solver_prompt(payload))
            verdict, validator_usage = call_model_with_usage(
                validator, _judge_prompt(candidate, arm, answer, payload)
            )
            required = {
                "condition_correct",
                "asserts_original_C",
                "evidence_grounded",
                "calibrated",
                "source_misattribution",
                "rationale",
            }
            if set(verdict) != required:
                raise ValueError("validator returned an invalid behavioral verdict schema")
            record.update(
                {
                    "status": "scored",
                    "solver_model": solver.model,
                    "validator_model": validator.model,
                    "solver_answer": answer,
                    "validator_verdict": verdict,
                    "solver_usage": solver_usage,
                    "validator_usage": validator_usage,
                }
            )
        except (RuntimeError, ValueError, OSError, TimeoutError) as exc:
            record.update({"status": "error", "error_type": type(exc).__name__, "error": str(exc)})
        record["finished_at"] = _now()
        attempt_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (records_dir / f"{arm}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        records.append(record)
    (artifact_root / "behavioral_proof.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return records


def controls_pass(records: list[dict[str, Any]]) -> bool:
    """Require every evaluated arm to match its expected target-C assertion mode."""
    arms = {record["arm"] for record in records}
    if not set(CORE_ARMS).issubset(arms) or len(arms) != len(records):
        return False
    for record in records:
        if record["status"] != "scored":
            return False
        verdict = record["validator_verdict"]
        if not verdict["condition_correct"]:
            return False
        should_assert = record.get("expected_mode") == "infer_C"
        if verdict["asserts_original_C"] != should_assert:
            return False
    return True

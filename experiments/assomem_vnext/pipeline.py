"""CLI for deterministic gates, independent evaluation, and review packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from behavior import run_behavioral_proof
from quality import deterministic_audit, independent_audit
from review import (
    GATES,
    validate_human_gate,
    validate_scenario_gate_0,
    write_gate_template,
    write_review_packet,
)
from schema import render_arms


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_root(candidate_path: Path) -> Path:
    return candidate_path.parents[1] / "artifacts" / candidate_path.stem


def ensure_release_eligible(candidate: dict) -> None:
    if candidate.get("provenance", {}).get("release_eligible") is False:
        raise ValueError("quarantined pre-Gate-0 illustration cannot advance")


def validate_prior_scenario_gate_0(candidate: dict, candidate_path: Path) -> None:
    provenance = candidate.get("provenance", {})
    review_path = provenance.get("gate_0_review_path")
    review_unit = provenance.get("gate_0_review_unit")
    if not review_path or not review_unit:
        raise ValueError("candidate provenance must cite an approved scenario Gate 0 review")
    validate_scenario_gate_0(candidate_path.parents[1] / review_path, review_unit)


def prepare(candidate_path: Path) -> int:
    candidate = load_json(candidate_path)
    root = artifact_root(candidate_path)
    audit = deterministic_audit(candidate)
    root.mkdir(parents=True, exist_ok=True)
    (root / "deterministic_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    try:
        rendered = render_arms(candidate)
    except ValueError:
        rendered = {}
    (root / "rendered_arms.json").write_text(
        json.dumps(rendered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if rendered:
        write_review_packet(candidate, audit, root / "review_packet.md")
    for gate in GATES:
        write_gate_template(candidate, gate, root / "review" / f"{gate}.csv")
    print(root)
    return 0 if audit["pass"] else 1


def evaluate(candidate_path: Path) -> int:
    candidate = load_json(candidate_path)
    ensure_release_eligible(candidate)
    validate_prior_scenario_gate_0(candidate, candidate_path)
    root = artifact_root(candidate_path)
    validate_human_gate(root / "review" / "gate_1.csv", candidate["candidate_id"], "gate_1")
    result = independent_audit(candidate)
    root.mkdir(parents=True, exist_ok=True)
    (root / "independent_evaluator.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(root / "independent_evaluator.json")
    return 0 if result.get("pass") else 1


def prove(candidate_path: Path) -> int:
    candidate = load_json(candidate_path)
    ensure_release_eligible(candidate)
    validate_prior_scenario_gate_0(candidate, candidate_path)
    records = run_behavioral_proof(candidate, artifact_root(candidate_path))
    return 0 if all(record["status"] == "scored" for record in records) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "evaluate", "prove"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    if args.command == "prepare":
        return prepare(args.candidate)
    if args.command == "evaluate":
        return evaluate(args.candidate)
    return prove(args.candidate)


if __name__ == "__main__":
    raise SystemExit(main())

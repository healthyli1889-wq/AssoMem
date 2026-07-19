"""CLI and orchestration for the 100-scenario query-validity experiment."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from clients import ModelConfig, call_model, config_from_env
from core import (
    CONDITION_NAMES,
    build_conditions,
    load_balanced_selection,
    redact_for_generator,
    validate_generated_payload,
)

EXPECTED = {
    "empty": {"not_gold", "abstain"},
    "a_only": {"not_gold", "abstain"},
    "b_only": {"not_gold", "abstain"},
    "both": {"gold"},
    "distractor": {"gold"},
    "absence": {"abstain"},
}


def _dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)


def make_generation_prompt(input_data: dict[str, Any], feedback: list[str] | None = None) -> str:
    feedback_text = "\nPrevious validation failures to correct:\n" + "\n".join(feedback or [])
    return f"""You are an independent benchmark query author.
Create one new natural English final-turn query with the same decision focus as
the focus_reference, but do not copy distinctive wording. The visible context
contains the user's prior conversations. The answer must require binding the
two relevant experiences and must not be directly stated in the context.
Return only JSON with:
query (string), gold_answer (string), required_elements (array of strings),
evidence_roles (array naming the two distinct necessary contributions),
association_type (string), and traps (array of strings).
Do not mention session IDs, hidden annotations, or benchmark mechanics.

Input:
{_dump(input_data)}
{feedback_text}
"""


def make_validation_prompt(condition: str, candidate: dict[str, Any]) -> str:
    return f"""You are a strict independent validator for a personal associative-memory item.
The candidate gold is valid in the BOTH-evidence condition only if it is warranted
by the visible context and requires two distinct earlier experiences. For this
single condition, classify whether the candidate gold is:
- gold: the answer is warranted and the candidate's required elements are supported;
- not_gold: the answer is not warranted under this condition;
- abstain: evidence is insufficient and a responsible agent should withhold the inference.
Do not infer missing evidence from general world knowledge. Return only JSON:
{{"verdict":"gold|not_gold|abstain","uses_evidence":["brief contribution 1", "brief contribution 2"],
"reason":"short explanation","required_elements_supported":[true,false]}}

Condition: {condition}
Candidate:
{_dump(candidate)}
"""


def condition_passes(condition: str, result: dict[str, Any]) -> bool:
    return result.get("verdict") in EXPECTED[condition]


def _load_item(root: Path, relative: str) -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_review_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "selection_id", "domain", "scenario_id", "user_id", "automatic_pass",
        "human_valid", "human_notes", "original_query", "generated_query",
        "gold_answer", "required_elements", "condition_summary",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "selection_id": row["selection_id"],
                "domain": row["domain"],
                "scenario_id": row["scenario_id"],
                "user_id": row["user_id"],
                "automatic_pass": row.get("automatic_pass", ""),
                "human_valid": "",
                "human_notes": "",
                "original_query": row.get("original_query", ""),
                "generated_query": row.get("candidate", {}).get("query", ""),
                "gold_answer": row.get("candidate", {}).get("gold_answer", ""),
                "required_elements": json.dumps(
                    row.get("candidate", {}).get("required_elements", []),
                    ensure_ascii=False,
                ),
                "condition_summary": json.dumps(row.get("conditions", {}), ensure_ascii=False),
            })


def _pending_record(selection: dict[str, Any], condition: str, prompt: str) -> dict[str, Any]:
    return {
        "selection_id": selection["selection_id"],
        "domain": selection["domain"],
        "scenario_id": selection["scenario_id"],
        "user_id": selection["user_id"],
        "condition": condition,
        "status": "pending_model_call",
        "prompt": prompt,
    }


def run_experiment(
    root: Path,
    output_dir: Path,
    *,
    generator: ModelConfig | None = None,
    validator: ModelConfig | None = None,
    seed: int = 17,
    limit: int | None = None,
    dry_run: bool = False,
    resume: bool = False,
    model_call: Callable[[ModelConfig, str], dict[str, Any]] = call_model,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    selection = load_balanced_selection(root, seed=seed)
    if limit is not None:
        selection = selection[:limit]
    (output_dir / "selection.json").write_text(_dump(selection) + "\n", encoding="utf-8")

    checkpoint_path = output_dir / "checkpoint.json"
    records: list[dict[str, Any]] = []
    if resume and checkpoint_path.is_file():
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        records = checkpoint.get("records", [])
        completed_ids = {row["selection_id"] for row in records}
        selection = [row for row in selection if row["selection_id"] not in completed_ids]
    pending: list[dict[str, Any]] = []
    for selected in selection:
        arms = {
            arm: _load_item(root, selected["paths"][arm])
            for arm in ("associative", "distractor", "absence")
        }
        generator_input = redact_for_generator(arms["associative"])
        generation_prompt = make_generation_prompt(generator_input)
        if dry_run:
            records.append({
                **selected,
                "status": "pending_model_call",
                "original_query": arms["associative"]["query"],
                "generation_prompt": generation_prompt,
            })
            checkpoint_path.write_text(
                _dump({"updated_at": _now(), "records": records}) + "\n",
                encoding="utf-8",
            )
            pending.extend(
                _pending_record(selected, condition, make_validation_prompt(
                    condition,
                    {"query": "<generated>", "gold_answer": "<generated>", "required_elements": []},
                ))
                for condition in CONDITION_NAMES
            )
            continue
        if generator is None or validator is None:
            raise ValueError("generator and validator configs are required unless dry_run")
        attempts: list[dict[str, Any]] = []
        candidate: dict[str, Any] | None = None
        condition_results: dict[str, Any] = {}
        feedback: list[str] = []
        for attempt in range(3):
            candidate = model_call(generator, make_generation_prompt(generator_input, feedback))
            errors = validate_generated_payload(candidate)
            if errors:
                feedback = errors
                attempts.append({"attempt": attempt, "candidate": candidate, "errors": errors})
                continue
            conditions = build_conditions(
                arms["associative"], arms["distractor"], arms["absence"], candidate["query"]
            )
            condition_results = {}
            failures = []
            for condition, prepared in conditions.items():
                validator_input = {
                    "context": prepared["context"],
                    "query": prepared["query"],
                    "candidate_gold": candidate["gold_answer"],
                    "required_elements": candidate["required_elements"],
                }
                result = model_call(validator, make_validation_prompt(condition, validator_input))
                condition_results[condition] = result
                if not condition_passes(condition, result):
                    failures.append(f"{condition}: {result.get('verdict')}")
            attempts.append({"attempt": attempt, "candidate": candidate, "failures": failures})
            if not failures:
                break
            feedback = failures
        records.append({
            **selected,
            "status": "completed",
            "original_query": arms["associative"]["query"],
            "candidate": candidate,
            "attempts": attempts,
            "conditions": condition_results,
            "automatic_pass": bool(condition_results) and all(
                condition_passes(name, result)
                for name, result in condition_results.items()
            ),
        })
        checkpoint_path.write_text(
            _dump({"updated_at": _now(), "records": records}) + "\n",
            encoding="utf-8",
        )
    _write_jsonl(output_dir / "records.jsonl", records)
    if pending:
        _write_jsonl(output_dir / "pending_model_calls.jsonl", pending)
    review_rows = records
    _write_review_csv(output_dir / "human_review.csv", review_rows)
    summary = summarize(records, dry_run=dry_run, seed=seed)
    (output_dir / "summary.json").write_text(_dump(summary) + "\n", encoding="utf-8")
    return summary


def summarize(records: list[dict[str, Any]], *, dry_run: bool, seed: int) -> dict[str, Any]:
    completed = [row for row in records if row.get("status") == "completed"]
    passed = sum(bool(row.get("automatic_pass")) for row in completed)
    failures = Counter()
    for row in completed:
        for condition, result in row.get("conditions", {}).items():
            if not condition_passes(condition, result):
                failures[f"{condition}:{result.get('verdict', 'missing')}"] += 1
    return {
        "generated_at": _now(),
        "seed": seed,
        "n_scenarios": len(records),
        "n_condition_checks_expected": len(records) * 6,
        "n_completed": len(completed),
        "n_pending": len(records) - len(completed),
        "automatic_pass_count": passed,
        "automatic_pass_rate": passed / len(completed) if completed else None,
        "failure_counts": dict(failures),
        "dry_run": dry_run,
        "human_review_required": True,
        "scope": "binary associative binding data validity; not agent performance",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path("experiments/query_validity/results/latest"))
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args(argv)
    try:
        generator = None if args.dry_run else config_from_env("ASSOMEM_GENERATOR")
        validator = None if args.dry_run else config_from_env("ASSOMEM_VALIDATOR")
        summary = run_experiment(
            args.root, args.output, generator=generator, validator=validator,
            seed=args.seed, limit=args.limit, dry_run=args.dry_run,
            resume=args.resume,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

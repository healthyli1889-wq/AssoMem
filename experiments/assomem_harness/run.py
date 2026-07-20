"""Prepare reproducible AssoMem runs without mutating gold data."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from arms import materialize_arms
from dataset import discover_items, solver_input
from models import load_roles, validate_solver_validator_independence
from profile import load_profile
from protocol import score_prompt, solver_prompt
from workflow import score_solver_answer

sys_path = Path(__file__).resolve().parents[1] / "query_validity"
import sys
sys.path.insert(0, str(sys_path))
from clients import call_model_with_usage  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def prepare_run(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, max_items: int | None = None,
) -> dict[str, Any]:
    """Create only experiment artifacts; all gold JSON stays read-only."""
    profile = load_profile(profile_path)
    items = discover_items(data_root, profile, domain)
    if max_items is not None:
        items = items[:max_items]
    run_root = log_root / domain / run_id
    log_dir = run_root / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    inventory: list[dict[str, Any]] = []
    for item in items:
        query = item.arms["associative"]["query"]
        arms = materialize_arms(item, profile, query)
        inventory.append({
            "item_id": item.item_id,
            "domain": domain,
            "query_focus": query,
            "filenames": item.filenames,
            "evaluation_arms": {
                name: {"lineage": arm.lineage, "prompt_hash": arm.visible["prompt_hash"]}
                for name, arm in arms.items()
            },
            "query_status": "needs_author_validator",
        })
    _write_jsonl(log_dir / "inventory.jsonl", inventory)
    with (run_root / "results.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["timestamp", "phase", "domain", "run_id", "status", "description"])
        writer.writerow([_now(), "A", domain, run_id, "keep", "inventory prepared; no model calls"])
    manifest = {
        "profile_id": profile.profile_id,
        "profile_path": str(profile_path),
        "data_root": str(data_root),
        "domain": domain,
        "run_id": run_id,
        "base_items": len(items),
        "shipped_conversations": len(items) * len(profile.arms),
        "generated_at": _now(),
        "mode": "dry-run",
    }
    (run_root / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def execute_run(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, max_items: int | None = None,
) -> dict[str, Any]:
    """Run one solver against frozen gold and score with an independent validator."""
    profile = load_profile(profile_path)
    roles = load_roles()
    validate_solver_validator_independence(roles)
    items = discover_items(data_root, profile, domain)
    if max_items is not None:
        items = items[:max_items]
    run_root = log_root / domain / run_id
    log_dir = run_root / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = run_root / "checkpoint.jsonl"
    completed = set()
    if checkpoint_path.is_file():
        completed = {
            json.loads(line)["checkpoint_id"]
            for line in checkpoint_path.read_text(encoding="utf-8").splitlines()
        }

    records: list[dict[str, Any]] = []
    for paired in items:
        frozen_query = paired.arms["associative"]["query"]
        for arm_name, arm in materialize_arms(paired, profile, frozen_query).items():
            checkpoint_id = f"{paired.item_id}:{arm_name}:solver"
            if checkpoint_id in completed:
                continue
            answer, solver_usage = call_model_with_usage(
                roles["solver"], solver_prompt(arm.visible)
            )
            judgment, validator_usage = call_model_with_usage(
                roles["validator"], score_prompt(answer, arm.ground_truth)
            )
            metric = score_solver_answer(judgment)
            record = {
                "checkpoint_id": checkpoint_id,
                "item_id": paired.item_id,
                "data_filename": arm.visible["data_filename"],
                "domain": domain,
                "arm": arm_name,
                "solver_model": roles["solver"].model,
                "validator_model": roles["validator"].model,
                "prompt_hash": arm.visible["prompt_hash"],
                "response": answer,
                "validator": judgment,
                "solver_usage": solver_usage,
                "validator_usage": validator_usage,
                **metric,
                "lineage": arm.lineage,
            }
            records.append(record)
            with checkpoint_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    _write_jsonl(log_dir / "results.jsonl", records)
    return {
        "run_id": run_id, "domain": domain, "answer_records": len(records),
        "run_root": str(run_root), "query_source": "frozen_gold_json",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=os.getenv("ASSOMEM_DATA_ROOT"))
    parser.add_argument("--profile", type=Path, default=os.getenv("ASSOMEM_PROFILE"))
    parser.add_argument("--domain", default=os.getenv("ASSOMEM_DOMAIN", "work"))
    parser.add_argument("--run-id", default=os.getenv("ASSOMEM_RUN_ID", "dry-run"))
    parser.add_argument("--log-root", type=Path, default=os.getenv("ASSOMEM_LOG_ROOT", "logs"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--max-items", type=int, help="Limit an inspection or real execution run.")
    args = parser.parse_args()
    if args.data_root is None or args.profile is None:
        parser.error("--data-root and --profile (or corresponding environment variables) are required")
    if args.execute:
        manifest = execute_run(
            args.data_root, args.profile, args.domain, args.run_id, args.log_root,
            max_items=args.max_items,
        )
    else:
        manifest = prepare_run(
            args.data_root, args.profile, args.domain, args.run_id, args.log_root,
            max_items=args.max_items,
        )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

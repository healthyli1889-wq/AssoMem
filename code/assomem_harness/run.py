"""Prepare reproducible AssoMem runs without mutating gold data."""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from arms import materialize_arms, materialize_vnext_arms
from dataset import discover_items, discover_vnext_items
from manifest import build_stratified_manifest, select_manifest_items
from models import load_roles, validate_solver_validator_independence
from profile import load_profile
from protocol import score_prompt, solver_prompt
from workflow import score_solver_answer, validate_solver_answer
from zero_evidence import run_zero_evidence_check

sys_path = Path(__file__).resolve().parents[1] / "model_client"
import sys
sys.path.insert(0, str(sys_path))
from clients import call_model_with_usage  # noqa: E402

EVALUATION_ARMS = ("full", "no_target", "broken_link", "distractor", "absence", "add_evidence")
VNEXT_EVALUATION_ARMS = ("full", "a_only", "b_only", "link_broken", "distractor", "absence")


def parse_arms(value: str) -> tuple[str, ...]:
    arms = tuple(part.strip() for part in value.split(",") if part.strip())
    unknown = set(arms) - set(EVALUATION_ARMS) - set(VNEXT_EVALUATION_ARMS)
    if not arms or unknown:
        raise ValueError(f"Unsupported evaluation arms: {', '.join(sorted(unknown)) or value}")
    return arms


def _evaluation_arms(profile: Any) -> tuple[str, ...]:
    return VNEXT_EVALUATION_ARMS if profile.is_vnext() else EVALUATION_ARMS


def _discover(data_root: Path, profile: Any, domain: str):
    return (
        discover_vnext_items(data_root, profile, domain)
        if profile.is_vnext()
        else discover_items(data_root, profile, domain)
    )


def _materialize(item: Any, profile: Any):
    return (
        materialize_vnext_arms(item, profile)
        if profile.is_vnext()
        else materialize_arms(item, profile, item.arms["associative"]["query"])
    )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_e1_template(path: Path, inventory: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "item_id", "arm", "source", "human_pass", "reviewer", "notes"
            ),
        )
        writer.writeheader()
        for row in inventory:
            for arm, evaluation in row["evaluation_arms"].items():
                writer.writerow({
                    "item_id": row["item_id"],
                    "arm": arm,
                    "source": evaluation["lineage"]["source"],
                    "human_pass": "",
                    "reviewer": "",
                    "notes": "",
                })


def _write_e2_template(path: Path, inventory: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "item_id", "arm", "human_rea", "human_h_k",
                "human_source_misattribution", "judge_agrees", "reviewer", "notes",
            ),
        )
        writer.writeheader()
        for row in inventory:
            for arm in row["evaluation_arms"]:
                writer.writerow({
                    "item_id": row["item_id"],
                    "arm": arm,
                    "human_rea": "",
                    "human_h_k": "",
                    "human_source_misattribution": "",
                    "judge_agrees": "",
                    "reviewer": "",
                    "notes": "",
                })


def validate_e1_gate(path: Path, item_ids: set[str], arms: tuple[str, ...]) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        reviewed = {
            (row["item_id"], row["arm"]): row.get("human_pass", "").strip().lower()
            for row in csv.DictReader(handle)
        }
    missing = [
        f"{item_id}:{arm}"
        for item_id in item_ids
        for arm in arms
        if reviewed.get((item_id, arm)) not in {"pass", "true", "yes"}
    ]
    if missing:
        raise ValueError(f"E1 review is incomplete or failed: {', '.join(sorted(missing))}")


def _append_registry(log_root: Path, manifest: dict[str, Any]) -> None:
    registry = log_root / "registry.jsonl"
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False) + "\n")


def _record_path(records_dir: Path, checkpoint_id: str) -> Path:
    digest = hashlib.sha256(checkpoint_id.encode("utf-8")).hexdigest()
    return records_dir / f"{digest}.json"


def _write_record(records_dir: Path, record: dict[str, Any]) -> None:
    records_dir.mkdir(parents=True, exist_ok=True)
    persisted = {**record, "attempt_id": str(uuid.uuid4()), "recorded_at": _now()}
    attempts_dir = records_dir.parent / "attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    attempt_destination = attempts_dir / f"{persisted['attempt_id']}.json"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=attempts_dir, suffix=".tmp", delete=False
    ) as temporary:
        temporary.write(json.dumps(persisted, ensure_ascii=False) + "\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, attempt_destination)

    destination = _record_path(records_dir, persisted["checkpoint_id"])
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=records_dir, suffix=".tmp", delete=False
    ) as temporary:
        temporary.write(json.dumps(persisted, ensure_ascii=False) + "\n")
        temporary_path = Path(temporary.name)
    os.replace(temporary_path, destination)


def completed_checkpoint_ids(records_dir: Path) -> set[str]:
    if not records_dir.is_dir():
        return set()
    return {
        record["checkpoint_id"]
        for path in records_dir.glob("*.json")
        for record in [json.loads(path.read_text(encoding="utf-8"))]
        if record.get("status") == "scored"
    }


@contextmanager
def acquire_run_lock(run_root: Path):
    run_root.mkdir(parents=True, exist_ok=True)
    lock_path = run_root / ".run.lock"
    with lock_path.open("w", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"run is already active: {run_root}") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def prepare_run(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, max_items: int | None = None,
) -> dict[str, Any]:
    """Create only experiment artifacts; all gold JSON stays read-only."""
    profile = load_profile(profile_path)
    all_items = _discover(data_root, profile, domain)
    selection_manifest = None
    if max_items is not None:
        if max_items > 20:
            raise ValueError("Pilot selection supports at most 20 items; provide a frozen manifest for larger runs")
        selection_manifest = build_stratified_manifest(
            all_items, profile, data_root, count=max_items, seed=20260722
        )
        items = select_manifest_items(all_items, selection_manifest, data_root)
    else:
        items = all_items
    run_root = log_root / domain / run_id
    log_dir = run_root / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    inventory: list[dict[str, Any]] = []
    for item in items:
        arms = _materialize(item, profile)
        query = item.arms["associative"]["query"]
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
    _write_e1_template(run_root / "review" / "e1_intervention.csv", inventory)
    _write_e2_template(run_root / "review" / "e2_judgment.csv", inventory)
    if selection_manifest:
        (run_root / "item_manifest.json").write_text(
            json.dumps(selection_manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
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
        "shipped_conversations": len(items) * (
            len(_evaluation_arms(profile))
            if profile.is_vnext()
            else len(profile.arms)
        ),
        "profile_sha256": _sha256_file(profile_path),
        "prompt_contract_version": 3,
        "evaluation_arms": list(_evaluation_arms(profile)),
        "generated_at": _now(),
        "mode": "dry-run",
    }
    (run_root / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    _append_registry(log_root, manifest)
    return manifest


def run_zero_evidence(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, item_manifest_path: Path, trials: int = 10,
) -> dict[str, Any]:
    """Execute the query-only shortcut screen and persist one artifact per item."""
    profile = load_profile(profile_path)
    if not profile.is_vnext():
        raise ValueError("zero-evidence is defined only for vNext profiles")
    roles = load_roles()
    manifest = json.loads(item_manifest_path.read_text(encoding="utf-8"))
    if manifest["profile_id"] != profile.profile_id or manifest["domain"] != domain:
        raise ValueError("Item manifest does not match the selected profile/domain")
    items = select_manifest_items(_discover(data_root, profile, domain), manifest, data_root)
    destination = log_root / domain / run_id / "zero_evidence"
    destination.mkdir(parents=True, exist_ok=True)
    results = []
    for item in items:
        result = run_zero_evidence_check(
            item.arms["associative"], profile, roles["solver"], call_model_with_usage, trials=trials
        )
        (destination / f"{item.item_id}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        results.append(result)
    return {
        "run_id": run_id,
        "domain": domain,
        "items": len(results),
        "passed": all(result["pass"] for result in results),
        "artifact_dir": str(destination),
    }


def _validate_zero_evidence_gate(run_root: Path, item_ids: set[str]) -> None:
    missing_or_failed = []
    for item_id in item_ids:
        path = run_root / "zero_evidence" / f"{item_id}.json"
        if not path.is_file():
            missing_or_failed.append(f"{item_id}:missing")
            continue
        result = json.loads(path.read_text(encoding="utf-8"))
        if not result.get("pass"):
            missing_or_failed.append(f"{item_id}:failed")
    if missing_or_failed:
        raise ValueError(
            "zero-evidence gate is incomplete or failed: " + ", ".join(sorted(missing_or_failed))
        )


def execute_run(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, max_items: int | None = None, arms: tuple[str, ...] | None = None,
    item_manifest_path: Path | None = None,
    e1_review_path: Path | None = None,
) -> dict[str, Any]:
    run_root = log_root / domain / run_id
    with acquire_run_lock(run_root):
        return _execute_run_unlocked(
            data_root, profile_path, domain, run_id, log_root,
            max_items=max_items, arms=arms, item_manifest_path=item_manifest_path,
            e1_review_path=e1_review_path,
        )


def _execute_run_unlocked(
    data_root: Path, profile_path: Path, domain: str, run_id: str, log_root: Path,
    *, max_items: int | None = None, arms: tuple[str, ...] | None = None,
    item_manifest_path: Path | None = None,
    e1_review_path: Path | None = None,
) -> dict[str, Any]:
    """Run one solver against frozen gold and score with an independent validator."""
    profile = load_profile(profile_path)
    selected_arms = arms or _evaluation_arms(profile)
    unsupported = set(selected_arms) - set(_evaluation_arms(profile))
    if unsupported:
        raise ValueError(f"Arms are unsupported by {profile.profile_id}: {', '.join(sorted(unsupported))}")
    roles = load_roles()
    validate_solver_validator_independence(roles)
    if item_manifest_path is None:
        raise ValueError("execute requires a frozen --item-manifest produced by dry-run")
    manifest = json.loads(item_manifest_path.read_text(encoding="utf-8"))
    if manifest["profile_id"] != profile.profile_id or manifest["domain"] != domain:
        raise ValueError("Item manifest does not match the selected profile/domain")
    items = select_manifest_items(_discover(data_root, profile, domain), manifest, data_root)
    if max_items is not None and max_items != len(items):
        raise ValueError("execute max-items must match the frozen item manifest")
    if e1_review_path is None:
        raise ValueError("execute requires an approved --e1-review CSV")
    validate_e1_gate(e1_review_path, {item.item_id for item in items}, selected_arms)
    run_root = log_root / domain / run_id
    if profile.is_vnext():
        _validate_zero_evidence_gate(run_root, {item.item_id for item in items})
    log_dir = run_root / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = run_root / "checkpoint.jsonl"
    records_dir = run_root / "records"
    completed = completed_checkpoint_ids(records_dir)
    if checkpoint_path.is_file() and not completed:
        completed = {
            json.loads(line)["checkpoint_id"]
            for line in checkpoint_path.read_text(encoding="utf-8").splitlines()
            if json.loads(line).get("status") == "scored"
        }

    records: list[dict[str, Any]] = []
    for paired in items:
        for arm_name, arm in _materialize(paired, profile).items():
            if arm_name not in selected_arms:
                continue
            checkpoint_id = f"{paired.item_id}:{arm_name}:solver"
            if checkpoint_id in completed:
                continue
            if arm_name == "no_target" and not arm.lineage["leakage_audit"]["passed"]:
                record = {
                    "checkpoint_id": checkpoint_id, "item_id": paired.item_id,
                    "arm": arm_name, "status": "invalid_arm",
                    "error": "no_target leakage audit failed", "lineage": arm.lineage,
                }
                _write_record(records_dir, record)
                records.append(record)
                continue
            try:
                answer, solver_usage = call_model_with_usage(
                    roles["solver"], solver_prompt(arm.visible, profile)
                )
            except (OSError, RuntimeError, ValueError) as exc:
                record = {
                    "checkpoint_id": checkpoint_id, "item_id": paired.item_id,
                    "arm": arm_name, "status": "solver_error",
                    "error": str(exc), "lineage": arm.lineage,
                }
                _write_record(records_dir, record)
                records.append(record)
                continue
            schema_error = validate_solver_answer(answer, profile)
            if schema_error:
                record = {
                    "checkpoint_id": checkpoint_id, "item_id": paired.item_id,
                    "arm": arm_name, "status": "invalid_response",
                    "error": schema_error, "response": answer,
                    "solver_usage": solver_usage, "lineage": arm.lineage,
                }
                _write_record(records_dir, record)
                records.append(record)
                continue
            try:
                judgment, validator_usage = call_model_with_usage(
                    roles["validator"], score_prompt(answer, arm.ground_truth, profile)
                )
            except (OSError, RuntimeError, ValueError) as exc:
                record = {
                    "checkpoint_id": checkpoint_id, "item_id": paired.item_id,
                    "arm": arm_name, "status": "validator_error",
                    "error": str(exc), "response": answer,
                    "solver_usage": solver_usage, "lineage": arm.lineage,
                }
                _write_record(records_dir, record)
                records.append(record)
                continue
            metric = score_solver_answer(judgment, answer, arm.ground_truth, profile)
            record = {
                "checkpoint_id": checkpoint_id,
                "item_id": paired.item_id,
                "data_filename": arm.lineage["source"],
                "domain": domain,
                "arm": arm_name,
                "solver_model": roles["solver"].model,
                "validator_model": roles["validator"].model,
                "prompt_hash": arm.visible["prompt_hash"],
                "response": answer,
                "validator": judgment,
                "solver_usage": solver_usage,
                "validator_usage": validator_usage,
                "status": "scored",
                **metric,
                "lineage": arm.lineage,
            }
            records.append(record)
            _write_record(records_dir, record)
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
    parser.add_argument("--zero-evidence", action="store_true")
    parser.add_argument("--zero-evidence-trials", type=int, default=10)
    parser.add_argument("--max-items", type=int, help="Limit an inspection or real execution run.")
    parser.add_argument("--arms", help="Comma-separated evaluation arms.")
    parser.add_argument("--item-manifest", type=Path, help="Frozen manifest generated by dry-run.")
    parser.add_argument("--e1-review", type=Path, help="Completed E1 intervention audit CSV.")
    args = parser.parse_args()
    if args.data_root is None or args.profile is None:
        parser.error("--data-root and --profile (or corresponding environment variables) are required")
    if args.execute and args.zero_evidence:
        parser.error("--execute and --zero-evidence are separate stages")
    parsed_arms = parse_arms(args.arms) if args.arms else None
    if args.zero_evidence:
        if args.item_manifest is None:
            parser.error("--zero-evidence requires --item-manifest")
        manifest = run_zero_evidence(
            args.data_root, args.profile, args.domain, args.run_id, args.log_root,
            item_manifest_path=args.item_manifest, trials=args.zero_evidence_trials,
        )
    elif args.execute:
        manifest = execute_run(
            args.data_root, args.profile, args.domain, args.run_id, args.log_root,
            max_items=args.max_items, arms=parsed_arms,
            item_manifest_path=args.item_manifest,
            e1_review_path=args.e1_review,
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

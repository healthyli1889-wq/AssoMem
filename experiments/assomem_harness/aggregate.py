"""Aggregate validator-scored solver logs into Table A and Table B."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from reporting import build_table_a, build_table_b, build_vnext_table_a, build_vnext_table_b


def audit_attempts(path: Path) -> dict[str, int]:
    """Audit legacy JSONL before any metric aggregation."""
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            records.append(json.loads(line))
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        if record.get("status") == "scored":
            key = (record.get("checkpoint_id", ""), record.get("prompt_hash", ""))
            groups[key].append(record)
    duplicated = [records for records in groups.values() if len(records) > 1]
    conflicts = sum(
        len({record.get("rea") for record in records if record.get("status") == "scored"}) > 1
        for records in duplicated
    )
    return {
        "records": len(records),
        "unique_keys": len(groups),
        "duplicate_keys": len(duplicated),
        "conflicting_scores": conflicts,
        "status_counts": dict(Counter(record.get("status", "unknown") for record in records)),
    }


def aggregate(results_path: Path, output_dir: Path, *, seed: int = 20260720) -> None:
    audit = audit_attempts(results_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "run_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    if audit["duplicate_keys"]:
        raise ValueError(
            "Refusing aggregation: duplicate attempts exist. "
            "Inspect the duplicate audit before choosing a resolution."
        )
    grouped: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    is_vnext = False
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("status") != "scored":
                continue
            solver = record["solver_model"]
            arm = record["arm"]
            is_vnext = is_vnext or arm in {"a_only", "b_only", "link_broken"}
            metric = "binary_correct" if "binary_correct" in record else "rea"
            grouped[solver][arm].append(int(record[metric]))
            if arm == "full":
                grouped[solver]["jer"].append(int(record["jer"]))
            if arm == "distractor":
                grouped[solver]["dir"].append(int(record["rea"]))
                grouped[solver]["fool_rate"].append(int(record["jer"] == 0))
            if arm == "absence":
                grouped[solver]["abc"].append(int(record["abc"]))
    rows = []
    control_rows = []
    for solver, values in sorted(grouped.items()):
        if is_vnext:
            ladder_required = ("full", "a_only", "b_only", "link_broken")
            if any(not values[key] for key in ladder_required):
                raise ValueError(
                    f"incomplete vNext ladder run for {solver}: "
                    f"{', '.join(key for key in ladder_required if not values[key])}"
                )
            row = {"solver": solver, **{key: values[key] for key in ladder_required}}
            rows.append(row)
            if values["distractor"] and values["absence"]:
                control_rows.append({
                    "solver": solver,
                    "distractor": values["distractor"],
                    "absence": values["absence"],
                })
            continue
        ladder_required = ("full", "no_target", "broken_link", "jer")
        if any(not values[key] for key in ladder_required):
            raise ValueError(
                f"incomplete ladder run for {solver}: "
                f"{', '.join(key for key in ladder_required if not values[key])}"
            )
        row = {"solver": solver, **{key: values[key] for key in ladder_required}}
        rows.append(row)
        control_required = ("dir", "fool_rate", "abc")
        if all(values[key] for key in control_required):
            control_rows.append({**row, **{key: values[key] for key in control_required}})
    table_a = build_vnext_table_a(rows, seed=seed) if is_vnext else build_table_a(rows, seed=seed)
    (output_dir / "table_a.md").write_text(table_a, encoding="utf-8")
    if control_rows:
        table_b = build_vnext_table_b(control_rows) if is_vnext else build_table_b(control_rows)
        (output_dir / "table_b.md").write_text(table_b, encoding="utf-8")
    (output_dir / "scores.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=20260720)
    args = parser.parse_args()
    aggregate(args.results, args.output, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Aggregate validator-scored solver logs into Table A and Table B."""

from __future__ import annotations

import argparse
import csv
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


def _validate_e2(path: Path, expected: set[tuple[str, str]]) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        reviewed = {
            (row["item_id"], row["arm"]): row.get("judge_agrees", "").strip().lower()
            for row in csv.DictReader(handle)
        }
    missing = sorted(
        f"{item_id}:{arm}"
        for item_id, arm in expected
        if reviewed.get((item_id, arm)) not in {"yes", "true", "pass"}
    )
    if missing:
        raise ValueError("E2 review is incomplete or disagrees: " + ", ".join(missing))


def _zero_evidence_summary(run_root: Path, item_ids: set[str]) -> tuple[bool, float]:
    rows = []
    for item_id in sorted(item_ids):
        path = run_root / "zero_evidence" / f"{item_id}.json"
        if not path.is_file():
            raise ValueError(f"missing zero-evidence artifact: {item_id}")
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    total_valid = sum(int(row["valid_trials"]) for row in rows)
    total_positive = sum(int(row.get("target_positive_count", 0)) for row in rows)
    return all(bool(row["pass"]) for row in rows), (
        total_positive / total_valid if total_valid else 1.0
    )


def aggregate(
    results_path: Path,
    output_dir: Path,
    *,
    seed: int = 20260720,
    e2_review_path: Path | None = None,
) -> None:
    audit = audit_attempts(results_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "run_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    if audit["duplicate_keys"]:
        raise ValueError(
            "Refusing aggregation: duplicate attempts exist. "
            "Inspect the duplicate audit before choosing a resolution."
        )
    records = []
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("status") != "scored":
                continue
            records.append(record)
    is_vnext = any(record.get("arm") in {"a_only", "b_only", "link_broken"} for record in records)
    if is_vnext:
        expected_pairs = {(record["item_id"], record["arm"]) for record in records}
        if e2_review_path is None:
            raise ValueError("vNext aggregation requires an approved E2 review CSV")
        _validate_e2(e2_review_path, expected_pairs)
        by_solver: dict[str, dict[str, dict[str, int]]] = defaultdict(
            lambda: defaultdict(dict)
        )
        for record in records:
            item_scores = by_solver[record["solver_model"]][record["item_id"]]
            if record["arm"] in item_scores:
                raise ValueError(
                    f"duplicate scored arm for {record['item_id']}:{record['arm']}"
                )
            item_scores[record["arm"]] = int(record["binary_correct"])
        required = {"full", "a_only", "b_only", "link_broken", "distractor", "absence"}
        rows = []
        control_rows = []
        per_item_rows = []
        scenario_rows: list[dict[str, str | float | int]] = []
        overall_rows = []
        for solver, item_map in sorted(by_solver.items()):
            incomplete = {
                item_id: sorted(required - set(scores))
                for item_id, scores in item_map.items()
                if set(scores) != required
            }
            if incomplete:
                raise ValueError(f"incomplete vNext item arms for {solver}: {incomplete}")
            ordered_ids = sorted(item_map)
            row = {
                "solver": solver,
                **{
                    arm: [item_map[item_id][arm] for item_id in ordered_ids]
                    for arm in ("full", "a_only", "b_only", "link_broken")
                },
            }
            rows.append(row)
            zero_pass, zero_fpr = _zero_evidence_summary(
                results_path.parent.parent, set(ordered_ids)
            )
            control_rows.append({
                "solver": solver,
                "distractor": [item_map[item_id]["distractor"] for item_id in ordered_ids],
                "absence": [item_map[item_id]["absence"] for item_id in ordered_ids],
                "zero_evidence_pass": zero_pass,
                "zero_evidence_fpr": zero_fpr,
            })
            for item_id in ordered_ids:
                scores = item_map[item_id]
                per_item_rows.append({
                    "solver": solver,
                    "item_id": item_id,
                    "scenario": item_id.split("_")[2],
                    **scores,
                    "joint_ladder_pass": int(all(scores[arm] for arm in (
                        "full", "a_only", "b_only", "link_broken"
                    ))),
                })
            scenarios = sorted({row["scenario"] for row in per_item_rows if row["solver"] == solver})
            for scenario in scenarios:
                selected = [
                    row for row in per_item_rows
                    if row["solver"] == solver and row["scenario"] == scenario
                ]
                scenario_rows.append({
                    "solver": solver,
                    "scenario": scenario,
                    "items": len(selected),
                    **{
                        arm: sum(int(item[arm]) for item in selected) / len(selected)
                        for arm in required
                    },
                })
            overall_rows.append({
                "solver": solver,
                "items": len(ordered_ids),
                **{
                    f"accuracy_{arm}": sum(item_map[item_id][arm] for item_id in ordered_ids)
                    / len(ordered_ids)
                    for arm in required
                },
                "delta_a_only": (
                    sum(row["full"]) - sum(row["a_only"])
                ) / len(ordered_ids),
                "delta_b_only": (
                    sum(row["full"]) - sum(row["b_only"])
                ) / len(ordered_ids),
                "delta_link_broken": (
                    sum(row["full"]) - sum(row["link_broken"])
                ) / len(ordered_ids),
                "zero_evidence_pass": zero_pass,
                "zero_evidence_fpr": zero_fpr,
            })
        (output_dir / "table_a.md").write_text(
            build_vnext_table_a(rows, seed=seed), encoding="utf-8"
        )
        (output_dir / "table_b.md").write_text(
            build_vnext_table_b(control_rows), encoding="utf-8"
        )
        (output_dir / "scores.json").write_text(
            json.dumps(rows, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "overall_scores.json").write_text(
            json.dumps(overall_rows, indent=2) + "\n", encoding="utf-8"
        )
        for filename, fieldnames, data in (
            (
                "per_item_scores.csv",
                ["solver", "item_id", "scenario", *sorted(required), "joint_ladder_pass"],
                per_item_rows,
            ),
            (
                "scenario_scores.csv",
                ["solver", "scenario", "items", *sorted(required)],
                scenario_rows,
            ),
        ):
            with (output_dir / filename).open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        return

    grouped: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for record in records:
            solver = record["solver_model"]
            arm = record["arm"]
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
    table_a = build_table_a(rows, seed=seed)
    (output_dir / "table_a.md").write_text(table_a, encoding="utf-8")
    if control_rows:
        table_b = build_table_b(control_rows)
        (output_dir / "table_b.md").write_text(table_b, encoding="utf-8")
    (output_dir / "scores.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=20260720)
    parser.add_argument("--e2-review", type=Path)
    args = parser.parse_args()
    aggregate(args.results, args.output, seed=args.seed, e2_review_path=args.e2_review)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

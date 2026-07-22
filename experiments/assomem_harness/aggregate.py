"""Aggregate validator-scored solver logs into Table A and Table B."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from reporting import build_table_a, build_table_b


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
    with results_path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("status") != "scored":
                continue
            solver = record["solver_model"]
            arm = record["arm"]
            grouped[solver][arm].append(int(record["rea"]))
            if arm == "full":
                grouped[solver]["jer"].append(int(record["jer"]))
            if arm == "distractor":
                grouped[solver]["dir"].append(int(record["rea"]))
                grouped[solver]["fool_rate"].append(int(record["jer"] == 0))
            if arm == "absence":
                grouped[solver]["abc"].append(int(record["abc"]))
    rows = []
    for solver, values in sorted(grouped.items()):
        required = ("full", "no_target", "broken_link", "jer", "dir", "fool_rate", "abc")
        if any(not values[key] for key in required):
            raise ValueError(f"incomplete scored run for {solver}: {', '.join(key for key in required if not values[key])}")
        rows.append({"solver": solver, **{key: values[key] for key in required}})
    (output_dir / "table_a.md").write_text(build_table_a(rows, seed=seed), encoding="utf-8")
    (output_dir / "table_b.md").write_text(build_table_b(rows), encoding="utf-8")
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

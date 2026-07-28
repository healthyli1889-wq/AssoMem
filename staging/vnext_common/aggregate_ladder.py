"""Turn a screen_vnext ladder run into the reportable table.

Target-positive rate per arm, plus the two derived deltas with paired bootstrap
confidence intervals. Δ is computed per item and then resampled over items, so the
interval reflects item-level variance rather than treating arms as independent.

    python3 aggregate_ladder.py review/ladder_full_100.json
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

ARMS = ("full", "a_only", "b_only", "link_broken", "distractor", "absence")
BOOTSTRAP = 10000
SEED = 20260727


def _yes(row: dict, arm: str) -> int | None:
    value = row.get(arm)
    return None if value not in {"yes", "no"} else int(value == "yes")


def _paired_delta(rows: list[dict], left: str, right: str) -> tuple[float, float, float]:
    pairs = [
        (_yes(row, left), _yes(row, right))
        for row in rows
        if _yes(row, left) is not None and _yes(row, right) is not None
    ]
    if not pairs:
        return float("nan"), float("nan"), float("nan")
    point = sum(a - b for a, b in pairs) / len(pairs)
    rng = random.Random(SEED)
    draws = []
    for _ in range(BOOTSTRAP):
        sample = [pairs[rng.randrange(len(pairs))] for _ in range(len(pairs))]
        draws.append(sum(a - b for a, b in sample) / len(sample))
    draws.sort()
    return point, draws[int(0.025 * BOOTSTRAP)], draws[int(0.975 * BOOTSTRAP) - 1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ladder", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.ladder.read_text(encoding="utf-8"))

    print(f"items: {len(rows)}\n")
    print(f"{'arm':14s} {'gold':>5s} {'target-positive rate':>21s} {'agrees with gold':>18s}")
    print("-" * 62)
    zero_yes = sum(1 for row in rows if row.get("zero_evidence") == "yes")
    print(f"{'zero_evidence':14s} {'no':>5s} {zero_yes / len(rows):>21.3f} "
          f"{f'{len(rows) - zero_yes}/{len(rows)}':>18s}")
    for arm in ARMS:
        values = [_yes(row, arm) for row in rows]
        values = [v for v in values if v is not None]
        gold = rows[0][f"{arm}_gold"]
        rate = sum(values) / len(values)
        agree = sum(1 for row in rows if row.get(arm) == row.get(f"{arm}_gold"))
        print(f"{arm:14s} {gold:>5s} {rate:>21.3f} {f'{agree}/{len(rows)}':>18s}")

    print("\nderived metrics (paired bootstrap, 95% CI over items):")
    for label, left, right in (
        ("Δ_mem   = full − absence     ", "full", "absence"),
        ("Δ_assoc = full − link_broken ", "full", "link_broken"),
        ("          full − a_only      ", "full", "a_only"),
        ("          full − b_only      ", "full", "b_only"),
    ):
        point, low, high = _paired_delta(rows, left, right)
        flag = "significant" if low > 0 else "CI includes 0"
        print(f"  {label} {point:+.3f}  [{low:+.3f}, {high:+.3f}]  {flag}")

    print("\nby polarity (target-positive rate):")
    header = f"  {'polarity':13s} {'n':>3s} " + " ".join(f"{a[:9]:>9s}" for a in ARMS)
    print(header)
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["polarity"]].append(row)
    for polarity in sorted(groups):
        subset = groups[polarity]
        cells = []
        for arm in ARMS:
            values = [_yes(row, arm) for row in subset]
            values = [v for v in values if v is not None]
            cells.append(f"{sum(values) / len(values):>9.2f}")
        print(f"  {polarity:13s} {len(subset):>3d} " + " ".join(cells))

    print("\nby scenario (Δ_mem):")
    scenarios: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        scenarios[row["scenario"]].append(row)

    def _order(name: str) -> tuple[int, str]:
        # S1..S20 sorts numerically; slug-named batches like health's
        # AMB_HV_<slug>_<nnn> fall back to alphabetical.
        if len(name) > 1 and name[0] == "S" and name[1:].isdigit():
            return (0, f"{int(name[1:]):04d}")
        return (1, name)

    if len(scenarios) > 30:
        print(f"  {len(scenarios)} distinct scenario slugs; per-scenario Δ needs a grid batch")
        return
    for scenario in sorted(scenarios, key=_order):
        subset = scenarios[scenario]
        point, low, high = _paired_delta(subset, "full", "absence")
        print(f"  {scenario:4s} n={len(subset):<3d} {point:+.3f}  [{low:+.3f}, {high:+.3f}]")


if __name__ == "__main__":
    main()

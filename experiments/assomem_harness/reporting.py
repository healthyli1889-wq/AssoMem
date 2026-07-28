"""Publishable aggregate tables from per-item validator scores."""

from __future__ import annotations

from typing import Any

from scoring import paired_delta_ci, wilson_interval


def _score(values: list[int]) -> tuple[float, float, float]:
    mean = sum(values) / len(values)
    low, high = wilson_interval(sum(values), len(values))
    return mean, low, high


def _cell(values: list[int]) -> str:
    mean, low, high = _score(values)
    return f"{mean:.2f} [{low:.2f}, {high:.2f}]"


def _delta(left: list[int], right: list[int], seed: int, draws: int) -> str:
    value, low, high = paired_delta_ci(left, right, seed=seed, draws=draws)
    marker = "✓" if low > 0 or high < 0 else "—"
    return f"{value:.2f} [{low:.2f}, {high:.2f}] {marker}"


def build_table_a(rows: list[dict[str, Any]], *, seed: int, draws: int = 10_000) -> str:
    lines = [
        "| Model | FULL REA [95% CI] | no-target REA [95% CI] | broken-link REA [95% CI] | Δ_mem | Δ_assoc |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows):
        lines.append(
            f"| {row['solver']} | {_cell(row['full'])} | {_cell(row['no_target'])} | "
            f"{_cell(row['broken_link'])} | "
            f"{_delta(row['full'], row['no_target'], seed + index, draws)} | "
            f"{_delta(row['full'], row['broken_link'], seed + index + 100, draws)} |"
        )
    return "\n".join(lines) + "\n"


def build_table_b(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Model | JER | DIR | FoolRate | AbC | SAA |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['solver']} | {_cell(row['jer'])} | {_cell(row['dir'])} | "
            f"{1 - sum(row['fool_rate']) / len(row['fool_rate']):.2f} | "
            f"{_cell(row['abc'])} | deferred (no source-swap/T6 profile capability) |"
        )
    return "\n".join(lines) + "\n"


# Whether an arm's gold is "assert the target". `binary_correct` is scored against
# each arm's own gold, so correctness means opposite things on the two halves.
VNEXT_ASSERT_GOLD = {
    "full": True,
    "distractor": True,
    "a_only": False,
    "b_only": False,
    "link_broken": False,
    "absence": False,
}


def target_assertion(arm: str, correctness: list[int]) -> list[int]:
    """Convert per-arm correctness into the target-assertion rate.

    A Δ has to subtract the *same quantity* measured on two arms. Subtracting
    accuracy(full) − accuracy(a_only) does not: on `full` a correct answer asserts
    the target, on `a_only` a correct answer withholds it. A solver that always
    asserts then scores accuracy 1.00 on full and 0.00 on every ablation, which
    reads as a perfect Δ of 1.00 despite the solver showing no discrimination at
    all. See `tests/test_reporting.py::test_constant_asserter_scores_zero_delta`.
    """
    if VNEXT_ASSERT_GOLD[arm]:
        return list(correctness)
    return [1 - value for value in correctness]


def build_vnext_table_a(rows: list[dict[str, Any]], *, seed: int, draws: int = 10_000) -> str:
    lines = [
        "| Model | FULL target-assertion [95% CI] | A-only | B-only | link-broken "
        "| Δ_A-only | Δ_B-only | Δ_assoc (link-broken) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows):
        assertion = {
            arm: target_assertion(arm, row[arm])
            for arm in ("full", "a_only", "b_only", "link_broken")
        }
        lines.append(
            f"| {row['solver']} | {_cell(assertion['full'])} | {_cell(assertion['a_only'])} | "
            f"{_cell(assertion['b_only'])} | {_cell(assertion['link_broken'])} | "
            f"{_delta(assertion['full'], assertion['a_only'], seed + index, draws)} | "
            f"{_delta(assertion['full'], assertion['b_only'], seed + index + 100, draws)} | "
            f"{_delta(assertion['full'], assertion['link_broken'], seed + index + 200, draws)} |"
        )
    return "\n".join(lines) + "\n"


def build_vnext_table_b(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Model | distractor binary accuracy [95% CI] | absence false-positive rate | zero-evidence gate |",
        "|---|---:|---:|---|",
    ]
    for row in rows:
        absence_fpr = 1 - sum(row["absence"]) / len(row["absence"])
        lines.append(
            f"| {row['solver']} | {_cell(row['distractor'])} | {absence_fpr:.2f} | "
            "required before execution |"
        )
    return "\n".join(lines) + "\n"

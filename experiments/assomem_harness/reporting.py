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


def build_vnext_table_a(rows: list[dict[str, Any]], *, seed: int, draws: int = 10_000) -> str:
    lines = [
        "| Model | FULL binary accuracy [95% CI] | A-only | B-only | link-broken | Δ_A-only | Δ_B-only | Δ_link-broken |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows):
        lines.append(
            f"| {row['solver']} | {_cell(row['full'])} | {_cell(row['a_only'])} | "
            f"{_cell(row['b_only'])} | {_cell(row['link_broken'])} | "
            f"{_delta(row['full'], row['a_only'], seed + index, draws)} | "
            f"{_delta(row['full'], row['b_only'], seed + index + 100, draws)} | "
            f"{_delta(row['full'], row['link_broken'], seed + index + 200, draws)} |"
        )
    return "\n".join(lines) + "\n"


def build_vnext_table_b(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Model | distractor binary accuracy [95% CI] | absence false-positive rate | zero-evidence gate |",
        "|---|---:|---:|---|",
    ]
    for row in rows:
        absence_fpr = 1 - sum(row["absence"]) / len(row["absence"])
        zero_fpr = float(row["zero_evidence_fpr"])
        zero_status = "pass" if bool(row["zero_evidence_pass"]) else "fail"
        lines.append(
            f"| {row['solver']} | {_cell(row['distractor'])} | {absence_fpr:.2f} | "
            f"{zero_status} (FPR {zero_fpr:.2f}) |"
        )
    return "\n".join(lines) + "\n"

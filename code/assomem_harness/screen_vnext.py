"""DATA CRITERIA Stage 6 + Stage 7 screens over a stratified sample.

Stage 6 (query-only): the solver sees Q with an empty context. Any target-positive
answer means the item is answerable without memory.

Stage 7 (single-evidence): the solver sees `a_only` and `b_only`. A target-positive
answer means one episode alone licenses C, which section 5.1 rejects outright.

Also runs `full`, `link_broken`, `distractor` and `absence` so one pass shows the
whole ladder. Reports agreement broken down by polarity and query type, because a
construct failure concentrated in one polarity is a design fault, not noise.

    source my_config.sh && python3 experiments/assomem_harness/screen_vnext.py --per-polarity 3
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "model_client"))

from arms import materialize_vnext_arms  # noqa: E402
from clients import call_model_with_usage  # noqa: E402
from dataset import discover_vnext_items  # noqa: E402
from models import load_roles  # noqa: E402
from profile import load_profile  # noqa: E402
from protocol import solver_prompt  # noqa: E402

LADDER = ("full", "a_only", "b_only", "link_broken", "distractor", "absence")


def _decide(solver: Any, profile: Any, visible: dict[str, Any]) -> tuple[str | None, dict]:
    try:
        answer, usage = call_model_with_usage(solver, solver_prompt(visible, profile))
    except (OSError, RuntimeError, ValueError) as exc:
        return None, {"error": str(exc)}
    return answer.get("decision"), {"answer": answer, "usage": usage}


def _stratify(items: list, per_polarity: int) -> list:
    """Take an even spread across polarity, then query type, then scenario."""
    buckets: dict[str, list] = defaultdict(list)
    for item in items:
        buckets[item.arms["associative"]["polarity"]].append(item)
    chosen = []
    for polarity in sorted(buckets):
        rows = sorted(
            buckets[polarity],
            key=lambda row: (row.arms["associative"]["query_type"], row.item_id),
        )
        step = max(1, len(rows) // per_polarity)
        chosen.extend(rows[::step][:per_polarity])
    return chosen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-polarity", type=int, default=3)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--out", type=Path, default=Path("/tmp/social_screen.json"))
    parser.add_argument(
        "--restart", action="store_true", help="ignore any existing progress sidecar"
    )
    args = parser.parse_args()

    profile = load_profile(Path(os.environ["ASSOMEM_PROFILE"]))
    data_root = Path(os.environ["ASSOMEM_DATA_ROOT"])
    solver = load_roles()["solver"]
    items = _stratify(
        discover_vnext_items(data_root, profile, os.environ["ASSOMEM_DOMAIN"]),
        args.per_polarity,
    )
    print(f"solver: {solver.model}\nsampled {len(items)} items\n")

    def screen(item) -> dict[str, Any]:
        associative = item.arms["associative"]
        rendered = materialize_vnext_arms(item, profile)
        row: dict[str, Any] = {
            "item_id": item.item_id,
            "polarity": associative["polarity"],
            "query_type": associative["query_type"],
            "scenario": associative["pair_id"].split("_")[2],
            "target": associative["answer_contract"]["target_proposition"],
        }
        zero, _ = _decide(solver, profile, {
            "context": [],
            "query": associative["query"],
            "target_proposition": associative["answer_contract"]["target_proposition"],
        })
        row["zero_evidence"] = zero
        for arm_name in LADDER:
            arm = rendered[arm_name]
            decision, _ = _decide(solver, profile, arm.visible)
            row[arm_name] = decision
            row[f"{arm_name}_gold"] = "yes" if arm.ground_truth["binary_decision"] else "no"
        return row

    # Progress is appended to a sidecar JSONL as each item finishes, so an
    # interrupted run neither loses work nor goes silent for ten minutes.
    progress_path = args.out.with_suffix(".progress.jsonl")
    done: dict[str, dict[str, Any]] = {}
    if progress_path.exists() and not args.restart:
        for line in progress_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done[row["item_id"]] = row
        print(f"resuming: {len(done)} items already in {progress_path.name}\n", flush=True)

    todo = [item for item in items if item.item_id not in done]
    total = len(items)
    lock = threading.Lock()
    started = time.monotonic()
    handle = progress_path.open("a", encoding="utf-8")

    def record(row: dict[str, Any]) -> None:
        with lock:
            done[row["item_id"]] = row
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            n = len(done)
            elapsed = time.monotonic() - started
            rate = (n - (total - len(todo))) / elapsed if elapsed > 0 else 0
            eta = (total - n) / rate if rate > 0 else float("nan")
            marks = "".join(
                "." if row[a] == row[f"{a}_gold"] else "X" for a in LADDER
            )
            print(
                f"[{n:>3d}/{total}] {row['item_id']:<18s} {row['polarity']:<12s} "
                f"zeroEv={str(row['zero_evidence']):<4s} arms={marks} "
                f"| {elapsed/60:.1f}m elapsed, ~{eta/60:.1f}m left",
                flush=True,
            )

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(screen, item): item for item in todo}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    record(future.result())
                except Exception as exc:  # noqa: BLE001 - keep the run going
                    print(f"[----] {item.item_id}: FAILED {exc}", flush=True)
    finally:
        handle.close()

    rows = [done[item.item_id] for item in items if item.item_id in done]
    print(f"\ncompleted {len(rows)}/{total} items in {(time.monotonic()-started)/60:.1f} min\n", flush=True)
    args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    header = f"{'item':18s} {'polarity':13s} {'zeroEv':7s} " + " ".join(f"{a[:9]:>9s}" for a in LADDER)
    print(header)
    print("-" * len(header))
    for row in sorted(rows, key=lambda r: (r["polarity"], r["item_id"])):
        cells = []
        for arm in LADDER:
            mark = "ok" if row[arm] == row[f"{arm}_gold"] else "XX"
            cells.append(f"{str(row[arm]):>6s}{mark:>3s}")
        zero_mark = "ok" if row["zero_evidence"] == "no" else "XX"
        print(f"{row['item_id']:18s} {row['polarity']:13s} {str(row['zero_evidence']):>4s}{zero_mark:>3s} " + " ".join(cells))

    print("\nagreement with gold, by arm:")
    for arm in LADDER:
        hits = sum(1 for row in rows if row[arm] == row[f"{arm}_gold"])
        print(f"  {arm:12s} {hits:2d}/{len(rows)}")
    zero_pass = sum(1 for row in rows if row["zero_evidence"] == "no")
    print(f"  {'zero_evidence':12s} {zero_pass:2d}/{len(rows)}  (Stage 6: must be 'no' every time)")

    print("\nStage 7 single-evidence leak, by polarity (a_only or b_only answering yes):")
    by_polarity: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        leaked = row["a_only"] == "yes" or row["b_only"] == "yes"
        by_polarity[row["polarity"]]["leak" if leaked else "clean"] += 1
    for polarity in sorted(by_polarity):
        counts = by_polarity[polarity]
        total = sum(counts.values())
        print(f"  {polarity:13s} {counts['leak']}/{total} leak")

    print("\nabsence answering yes, by polarity (should never happen):")
    for polarity in sorted({row["polarity"] for row in rows}):
        subset = [row for row in rows if row["polarity"] == polarity]
        bad = sum(1 for row in subset if row["absence"] == "yes")
        print(f"  {polarity:13s} {bad}/{len(subset)}")
    print(f"\nwritten to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

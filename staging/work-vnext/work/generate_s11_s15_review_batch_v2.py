#!/usr/bin/env python3
"""Generate the hand-authored S11-S15 review batch.

The five scenario modules contain the 50 authored specs.  This file only
materializes source arms, enforces cross-batch controls, and writes review files.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import generate_s1_s5_review_batch as base
import generate_s6_s10_review_batch as s6_s10
from s11_s15_specs_s11 import S11
from s11_s15_specs_s12 import S12
from s11_s15_specs_s13 import S13
from s11_s15_specs_s14 import S14
from s11_s15_specs_s15 import S15

HERE = Path(__file__).resolve().parent
OUT = HERE / "candidates-s11-s15-review-v2"
AUDIT_PATH = HERE / "review" / "s11_s15_generation_audit_v2.json"
sys.path.insert(0, str(HERE.parents[2] / "experiments" / "assomem_vnext"))
from schema import render_arms, validate_candidate  # noqa: E402

SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "S11": S11, "S12": S12, "S13": S13, "S14": S14, "S15": S15,
}
FAMILY = {
    "S11": "offsite response under recovery, health, calendar, and messaging constraints",
    "S12": "rehearsal load versus protected voice clarity",
    "S13": "APAC verbal ownership under incomplete records",
    "S14": "hot-desking versus protected compliance drafting",
    "S15": "night war-room leadership, dependency maps, and recovery debt",
}
FORBIDDEN_VISIBLE = (
    "case-note", "benchmark", "schema", "latent c", "target relation",
    "calibration constraint", "annotation", "criterion",
)


def build_context(sp: dict[str, Any], s_idx: int, u_idx: int, user_id: str) -> list[dict[str, Any]]:
    """Keep the established vNext slots with a timestamp window disjoint from all prior batches."""
    base_dt = datetime(2027, 1, 4, tzinfo=timezone.utc) + timedelta(days=s_idx * 60 + u_idx * 3)
    sessions = []
    for session_id in range(1, 21):
        if session_id in base.SLOT_BG:
            dialogue = base.fill(base.BG[base.SLOT_BG[session_id]], sp["props"])
        elif session_id == 3:
            dialogue = sp["cx1"]
        elif session_id == 6:
            dialogue = sp["a"]
        elif session_id == 7:
            dialogue = sp["cx2"]
        elif session_id == 9:
            dialogue = sp["e1"]
        elif session_id == 14:
            dialogue = sp["b"]
        elif session_id == 17:
            dialogue = sp["e2"]
        else:
            dialogue = [{"role": "user", "content": sp["query"]}]
        timestamp = base_dt + timedelta(days=session_id - 1, hours=base.HOURS[session_id % len(base.HOURS)])
        sessions.append({
            "session_id": session_id,
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:00Z"),
            "speaker_id": user_id,
            "speaker_label": "User",
            "dialogue": [dict(turn) for turn in dialogue],
        })
    return sessions


def _lines(sp: dict[str, Any]) -> set[str]:
    turns = [sp[key] for key in ("cx1", "cx2", "a", "e1", "b", "e2", "lure", "bprime")]
    return {
        dialogue[0]["content"].strip()
        for dialogue in turns
    } | {sp["query"].strip()}


def cross_batch_audit() -> list[str]:
    problems: list[str] = []
    earlier_lines: set[str] = set()
    for all_specs in (base.SCENARIOS, s6_s10.SCENARIOS):
        for specs in all_specs.values():
            for sp in specs:
                earlier_lines.update(_lines(sp))

    batch_lines: dict[str, str] = {}
    for sid, specs in SCENARIOS.items():
        for sp in specs:
            label = f"{sid}/{sp['uid']}"
            for line in _lines(sp):
                normalized = " ".join(line.lower().split())
                if normalized in batch_lines:
                    problems.append(f"{label} shares key dialogue with {batch_lines[normalized]}")
                elif line in earlier_lines:
                    problems.append(f"{label} reuses key dialogue from S1-S10")
                batch_lines[normalized] = label
                if any(term in normalized for term in FORBIDDEN_VISIBLE):
                    problems.append(f"{label} has forbidden visible term: {line}")
    return problems


def apply_s13_three_fact_contract(item: dict[str, Any], sp: dict[str, Any], arm: str) -> None:
    """S13 has A, B, E1 as decision facts; session 17 remains ordinary history."""
    item["supporting_constraints"] = {
        "E1": {"session_id": 9, "fact": sp["e1"][0]["content"]},
    }
    item["episode_annotations"]["17"] = {"role": "background_memory"}
    item["relational_connector"]["calibration_constraints"] = ["E1"]
    item["coactivation_bridge"] = (
        f"A and B form the intervention pair. {sp['relation']} "
        "The short APAC overlap is E1; session 17 is ordinary background, not decision evidence."
    )
    if arm == "absence":
        item["context"][16]["dialogue"] = [dict(turn) for turn in sp["e2"]]
        item["absence_note"] = {
            "replaced_session_ids": [6, 9, 14],
            "withheld_evidence_ids": ["ev_A", "ev_B", "E1"],
        }


def item_for(sid: str, s_idx: int, sp: dict[str, Any], u_idx: int, arm: str) -> dict[str, Any]:
    item = base.build_item(sid, s_idx, sp, u_idx, arm)
    if sid == "S13":
        apply_s13_three_fact_contract(item, sp, arm)
    return item


def write_readme() -> None:
    lines = [
        "# Work S11-S15 review batch v2",
        "",
        "50 explicitly authored sub-scenarios × 3 source arms = 150 JSON files.",
        "The rejected template batches are not part of this review set.",
        "",
        "| Scenario | User | Role | Query type | Polarity | A | B | E1/E2 | Calibrated target |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, specs in SCENARIOS.items():
        for sp in specs:
            e_facts = sp["e1"][0]["content"]
            if sid != "S13":
                e_facts += " / " + sp["e2"][0]["content"]
            else:
                e_facts += " (E2 is ordinary background)"
            row = [
                sid, sp["uid"], sp["role"], sp["query_type"], sp["polarity"],
                sp["a"][0]["content"], sp["b"][0]["content"], e_facts, sp["calibrated"],
            ]
            lines.append("| " + " | ".join(value.replace("|", "/") for value in row) + " |")
    lines.extend([
        "",
        "## Verification gates",
        "- [x] Explicit spec count: 50.",
        "- [x] Query-type quota: 8/8/8/8/9/9.",
        "- [x] Polarity quota: accept 15 / reject 20 / conditional 10 / non_decision 5.",
        "- [x] Source schema and four associative rendered arms.",
        "- [x] Key-dialogue and timestamp uniqueness against S1-S10.",
        "- [ ] Human spot-read: one full source per scenario.",
        "- [ ] Human arm review: full, a_only, b_only, link_broken, distractor, absence.",
    ])
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    problems = base.batch_audit(SCENARIOS) + cross_batch_audit()
    if problems:
        raise SystemExit("BATCH AUDIT FAILED:\n" + "\n".join(f"- {problem}" for problem in problems))
    base.FAMILY.update(FAMILY)
    original_context = base.build_context
    base.build_context = build_context
    records: list[dict[str, Any]] = []
    try:
        for arm in ("associative", "distractor", "absence"):
            (OUT / arm).mkdir(parents=True, exist_ok=True)
        for s_idx, (sid, specs) in enumerate(SCENARIOS.items()):
            for u_idx, sp in enumerate(specs):
                for arm in ("associative", "distractor", "absence"):
                    item = item_for(sid, s_idx, sp, u_idx, arm)
                    score, notes = base.score_item(item)
                    errors = validate_candidate(item)
                    record = {
                        "candidate_id": item["candidate_id"],
                        "scenario": sid,
                        "profile": sp["uid"],
                        "arm": arm,
                        "score": score,
                        "score_notes": notes,
                        "schema_errors": errors,
                    }
                    records.append(record)
                    if score < 95 or errors:
                        raise ValueError(f"{item['candidate_id']} rejected: {notes or errors}")
                    (OUT / arm / f"{item['candidate_id']}.json").write_text(
                        json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                    )
        rendered = 0
        for path in sorted((OUT / "associative").glob("*.json")):
            render_arms(json.loads(path.read_text(encoding="utf-8")))
            rendered += 1
        write_readme()
        AUDIT_PATH.write_text(json.dumps({
            "batch": "S11-S15 hand-authored v2",
            "records": records,
            "schema_valid": sum(not record["schema_errors"] for record in records),
            "rendered_associative": rendered,
            "cross_batch_problems": cross_batch_audit(),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS {len(records)}/150; rendered_associative={rendered}")
    finally:
        base.build_context = original_context
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

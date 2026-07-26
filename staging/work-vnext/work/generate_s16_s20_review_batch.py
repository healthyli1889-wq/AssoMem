#!/usr/bin/env python3
"""Generate the hand-authored S16-S20 review batch (v2 construct contract).

The five scenario modules contain the 50 authored specs. This file materializes
source arms, enforces cross-batch controls, emits six-arm review packets, and
writes versioned review files under candidates-s16-s20-review-v2/.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import generate_s1_s5_review_batch as base
import generate_s6_s10_review_batch as s6_s10
import generate_s11_s15_review_batch_v2 as s11_s15
from s16_s20_specs_s16 import S16
from s16_s20_specs_s17 import S17
from s16_s20_specs_s18 import S18
from s16_s20_specs_s19 import S19
from s16_s20_specs_s20 import S20

HERE = Path(__file__).resolve().parent
OUT = HERE / "candidates-s16-s20-review-v2"
AUDIT_PATH = HERE / "review" / "s16_s20_generation_audit_v2.json"
REVIEW_DIR = HERE / "review" / "s16-s20-v2"
CONSTRUCT_CSV = REVIEW_DIR / "construct_validity_review.csv"
PACKET_DIR = REVIEW_DIR / "arm_packets"
PACKET_INDEX = REVIEW_DIR / "arm_packet_index.csv"
sys.path.insert(0, str(HERE.parents[2] / "experiments" / "assomem_vnext"))
from schema import render_arms, validate_candidate  # noqa: E402

SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "S16": S16, "S17": S17, "S18": S18, "S19": S19, "S20": S20,
}
FAMILY = {
    "S16": "rapid live troubleshooting leadership versus careful asynchronous incident analysis",
    "S17": "negotiating scope commitments when project evidence is incomplete",
    "S18": "review and decision quality under interruption density versus protected focused work",
    "S19": "communicating uncertainty and risk escalation in cross-functional decisions",
    "S20": "choosing synchronous versus asynchronous collaboration for complex handoffs",
}
FORBIDDEN_VISIBLE = (
    "case-note", "benchmark", "schema", "latent c", "target relation",
    "calibration constraint", "annotation", "criterion",
)
# Diagnostic phrasing that must not appear in E1/E2 logistical constraints.
E_DIAGNOSTIC = (
    "i can ", "i should ", "i prefer", "my judgment", "my focus",
    "would let me", "would support", "ready to lead", "makes me",
    "i failed", "i succeeded", "premature", "too quickly", "overreached",
    "i recommend", "we recommend", "accept the", "reject the", "decline the",
)


def build_context(sp: dict[str, Any], s_idx: int, u_idx: int, user_id: str) -> list[dict[str, Any]]:
    """Keep the established vNext slots with a timestamp window disjoint from all prior batches."""
    base_dt = datetime(2028, 1, 8, tzinfo=timezone.utc) + timedelta(days=s_idx * 60 + u_idx * 3)
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
    for all_specs in (base.SCENARIOS, s6_s10.SCENARIOS, s11_s15.SCENARIOS):
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
                    problems.append(f"{label} reuses key dialogue from S1-S15")
                batch_lines[normalized] = label
                if any(term in normalized for term in FORBIDDEN_VISIBLE):
                    problems.append(f"{label} has forbidden visible term: {line}")
            for key in ("e1", "e2"):
                text = " ".join(turn["content"].lower() for turn in sp[key])
                if any(term in text for term in E_DIAGNOSTIC):
                    problems.append(f"{label} {key} contains diagnostic phrasing")
            for phrase in (sp["target"], sp["calibrated"]):
                needle = " ".join(phrase.lower().split())
                bprime = " ".join(turn["content"].lower() for turn in sp["bprime"])
                if len(needle) >= 18 and needle in bprime:
                    problems.append(f"{label} B-prime lexically contains target/calibrated wording")
    return problems


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def item_for(sid: str, s_idx: int, sp: dict[str, Any], u_idx: int, arm: str) -> dict[str, Any]:
    """Build a v2 item: mode contract; absence withholds only A/B and retains E1/E2."""
    item = base.build_item(sid, s_idx, sp, u_idx, arm)
    item["answer_contract"]["required_output_fields"] = [
        "mode", "answer", "evidence_session_ids",
    ]
    item["coactivation_bridge"] = (
        f"A and B form the only intervention pair. {sp['relation']} "
        "E1 and E2 are logistical calibration only and do not open a second route to C."
    )
    if arm == "absence":
        props = sp["props"]
        # Restore authored E1/E2; withhold only A (session 6) and B (session 14).
        item["context"][5]["dialogue"] = base.neutral(
            f"I did a standard pass over the {props[1]} records this morning.",
            "Any exceptions in there?", "None worth a note.")
        item["context"][8]["dialogue"] = [dict(turn) for turn in sp["e1"]]
        item["context"][13]["dialogue"] = base.neutral(
            f"I closed a routine {props[3]} cycle without surprises.",
            "Follow-up needed?", "A note for the next cycle, nothing more.")
        item["context"][16]["dialogue"] = [dict(turn) for turn in sp["e2"]]
        item["episode_annotations"]["9"] = {"role": "supporting_constraint", "fact_id": "E1"}
        item["episode_annotations"]["17"] = {"role": "supporting_constraint", "fact_id": "E2"}
        item["episode_annotations"]["6"] = {"role": "background_memory"}
        item["episode_annotations"]["14"] = {"role": "background_memory"}
        item["supporting_constraints"] = {
            "E1": {"session_id": 9, "fact": sp["e1"][0]["content"]},
            "E2": {"session_id": 17, "fact": sp["e2"][0]["content"]},
        }
        item["absence_note"] = {
            "replaced_session_ids": [6, 14],
            "withheld_evidence_ids": ["ev_A", "ev_B"],
        }
        item["target_evidence_ids"] = []
    return item


def _dialogue_map(context: list[dict[str, Any]]) -> dict[int, list[dict[str, str]]]:
    return {int(session["session_id"]): session["dialogue"] for session in context}


def _diff_sessions(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> list[int]:
    left_map = _dialogue_map(left)
    right_map = _dialogue_map(right)
    return sorted(
        session_id
        for session_id in left_map
        if left_map[session_id] != right_map.get(session_id)
    )


def deterministic_arm_audit(
    associative: dict[str, Any],
    distractor: dict[str, Any],
    absence: dict[str, Any],
) -> list[str]:
    problems: list[str] = []
    pair_id = associative["pair_id"]
    for label, item in (
        ("associative", associative),
        ("distractor", distractor),
        ("absence", absence),
    ):
        if len(item["context"]) != 20:
            problems.append(f"{pair_id}/{label}: expected 20 sessions")
        if item["answer_contract"]["required_output_fields"] != [
            "mode", "answer", "evidence_session_ids",
        ]:
            problems.append(f"{pair_id}/{label}: required_output_fields mismatch")

    rendered = render_arms(associative)
    for arm_name, arm in rendered.items():
        if len(arm["context"]) != 20:
            problems.append(f"{pair_id}/{arm_name}: rendered context length != 20")

    full = rendered["full"]["context"]
    if _diff_sessions(full, rendered["a_only"]["context"]) != [14]:
        problems.append(f"{pair_id}: a_only must differ only on session 14")
    if _diff_sessions(full, rendered["b_only"]["context"]) != [6]:
        problems.append(f"{pair_id}: b_only must differ only on session 6")
    if _diff_sessions(full, rendered["link_broken"]["context"]) != [14]:
        problems.append(f"{pair_id}: link_broken must differ only on session 14")

    distractor_diff = _diff_sessions(associative["context"], distractor["context"])
    if distractor_diff != [18]:
        problems.append(f"{pair_id}: distractor must differ only on session 18, got {distractor_diff}")
    absence_diff = _diff_sessions(associative["context"], absence["context"])
    if absence_diff != [6, 14]:
        problems.append(f"{pair_id}: absence must differ only on sessions 6 and 14, got {absence_diff}")

    e1 = associative["context"][8]["dialogue"]
    e2 = associative["context"][16]["dialogue"]
    for arm_name in ("full", "a_only", "b_only", "link_broken"):
        ctx = rendered[arm_name]["context"]
        if _dialogue_map(ctx)[9] != e1 or _dialogue_map(ctx)[17] != e2:
            problems.append(f"{pair_id}/{arm_name}: E1/E2 not retained verbatim")
    if _dialogue_map(absence["context"])[9] != e1 or _dialogue_map(absence["context"])[17] != e2:
        problems.append(f"{pair_id}/absence: E1/E2 not retained verbatim")

    target = _normalize(associative["latent_C"]["inference"])
    calibrated = _normalize(associative["latent_C"]["calibrated_language"])
    visible = _normalize(
        " ".join(
            turn["content"]
            for session in associative["context"]
            for turn in session["dialogue"]
        )
        + " "
        + associative["query"]
    )
    for phrase in (target, calibrated):
        if len(phrase) >= 18 and phrase in visible:
            problems.append(f"{pair_id}: target/calibrated leaked into context or query")
    return problems


def write_arm_packet(
    sid: str,
    sp: dict[str, Any],
    associative: dict[str, Any],
    distractor: dict[str, Any],
    absence: dict[str, Any],
) -> dict[str, Any]:
    rendered = render_arms(associative)
    packet = {
        "pair_id": associative["pair_id"],
        "scenario": sid,
        "uid": sp["uid"],
        "role": sp["role"],
        "query": sp["query"],
        "target": sp["target"],
        "calibrated": sp["calibrated"],
        "relation": sp["relation"],
        "A": sp["a"][0]["content"],
        "B": sp["b"][0]["content"],
        "E1": sp["e1"][0]["content"],
        "E2": sp["e2"][0]["content"],
        "B_prime": sp["bprime"][0]["content"],
        "lure": sp["lure"][0]["content"],
        "subset_gate": {
            "full_supports_C": "",
            "a_only_supports_C": "",
            "b_only_supports_C": "",
            "link_broken_supports_C": "",
            "absence_supports_C": "",
            "reviewer": "",
            "notes": "",
        },
        "arms": {},
    }
    for arm_name, arm in rendered.items():
        packet["arms"][arm_name] = {
            "expected_mode": arm["expected_mode"],
            "lineage": arm["lineage"],
            "changed_sessions": _diff_sessions(rendered["full"]["context"], arm["context"]),
            "context": arm["context"],
            "query": arm["query"],
        }
    packet["arms"]["distractor"] = {
        "expected_mode": "infer_C",
        "lineage": {"transform": "shipped", "changed_sessions": [18]},
        "changed_sessions": [18],
        "context": distractor["context"],
        "query": distractor["query"],
    }
    packet["arms"]["absence"] = {
        "expected_mode": "withhold_C",
        "lineage": {"transform": "replace_ev_A_and_ev_B_only", "changed_sessions": [6, 14]},
        "changed_sessions": [6, 14],
        "context": absence["context"],
        "query": absence["query"],
    }
    path = PACKET_DIR / f"{associative['pair_id']}.json"
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "pair_id": associative["pair_id"],
        "scenario": sid,
        "uid": sp["uid"],
        "packet": str(path.relative_to(HERE)),
    }


def write_construct_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "pair_id", "scenario", "uid", "role", "query", "target",
        "full_supports_C", "a_only_supports_C", "b_only_supports_C",
        "link_broken_supports_C", "absence_supports_C", "reviewer", "notes",
    ]
    with CONSTRUCT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_readme() -> None:
    lines = [
        "# Work S16-S20 review batch v2",
        "",
        "50 explicitly authored sub-scenarios × 3 source arms = 150 JSON files.",
        "Construct contract: A/B are the only target evidence; E1/E2 are logistical calibration.",
        "Absence withholds only A and B and retains E1/E2.",
        "",
        "| Scenario | User | Role | Query type | Polarity | A | B | E1/E2 | Calibrated target |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for sid, specs in SCENARIOS.items():
        for sp in specs:
            e_facts = sp["e1"][0]["content"] + " / " + sp["e2"][0]["content"]
            row = [
                sid, sp["uid"], sp["role"], sp["query_type"], sp["polarity"],
                sp["a"][0]["content"], sp["b"][0]["content"], e_facts, sp["calibrated"],
            ]
            lines.append("| " + " | ".join(value.replace("|", "/") for value in row) + " |")
    lines.extend([
        "",
        "## Verification gates",
        "- [x] Explicit spec count: 50.",
        "- [x] Query-type / polarity quotas.",
        "- [x] Source schema and four associative rendered arms.",
        "- [x] Absence retains E1/E2; withholds only A/B.",
        "- [x] Solver contract uses mode/answer/evidence_session_ids.",
        "- [x] Six-arm packets under review/s16-s20-v2/arm_packets/.",
        "- [ ] Human construct CSV: all subset columns filled; ablation arms must be no.",
        "- [ ] Human arm review for frozen pilot pairs.",
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
    arm_problems: list[str] = []
    construct_rows: list[dict[str, str]] = []
    packet_index: list[dict[str, str]] = []
    try:
        for arm in ("associative", "distractor", "absence"):
            (OUT / arm).mkdir(parents=True, exist_ok=True)
        PACKET_DIR.mkdir(parents=True, exist_ok=True)
        REVIEW_DIR.mkdir(parents=True, exist_ok=True)

        for s_idx, (sid, specs) in enumerate(SCENARIOS.items()):
            for u_idx, sp in enumerate(specs):
                built: dict[str, dict[str, Any]] = {}
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
                    built[arm] = item
                arm_problems.extend(
                    deterministic_arm_audit(built["associative"], built["distractor"], built["absence"])
                )
                packet_index.append(
                    write_arm_packet(sid, sp, built["associative"], built["distractor"], built["absence"])
                )
                construct_rows.append({
                    "pair_id": built["associative"]["pair_id"],
                    "scenario": sid,
                    "uid": sp["uid"],
                    "role": sp["role"],
                    "query": sp["query"],
                    "target": sp["target"],
                    "full_supports_C": "",
                    "a_only_supports_C": "",
                    "b_only_supports_C": "",
                    "link_broken_supports_C": "",
                    "absence_supports_C": "",
                    "reviewer": "",
                    "notes": "",
                })

        if arm_problems:
            raise SystemExit(
                "ARM AUDIT FAILED:\n" + "\n".join(f"- {problem}" for problem in arm_problems)
            )

        rendered = 0
        for path in sorted((OUT / "associative").glob("*.json")):
            render_arms(json.loads(path.read_text(encoding="utf-8")))
            rendered += 1
        write_readme()
        write_construct_csv(construct_rows)
        with PACKET_INDEX.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["pair_id", "scenario", "uid", "packet"])
            writer.writeheader()
            writer.writerows(packet_index)
        AUDIT_PATH.write_text(json.dumps({
            "batch": "S16-S20 hand-authored v2",
            "records": records,
            "schema_valid": sum(not record["schema_errors"] for record in records),
            "rendered_associative": rendered,
            "cross_batch_problems": cross_batch_audit(),
            "arm_audit_problems": arm_problems,
            "construct_csv": str(CONSTRUCT_CSV.relative_to(HERE)),
            "packet_dir": str(PACKET_DIR.relative_to(HERE)),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS {len(records)}/150; rendered_associative={rendered}")
    finally:
        base.build_context = original_context
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

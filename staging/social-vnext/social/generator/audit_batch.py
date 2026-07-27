"""Stage 5 deterministic audit for the social-vNext batch.

Runs the repository's own `assomem_vnext.schema.validate_candidate` on all 300
files, then adds the batch-level checks that per-file validation cannot see:
pair consistency, arm construction rules from DATA CRITERIA section 5, the
allocation quota, rendered-arm session counts, matched replacement lengths,
anonymisation, and surface-language hazards introduced by templating.

    python3 audit_batch.py [--candidates DIR] [--csv PATH]

Exit status is non-zero if any pair has an error, so this can gate the batch.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import allocation
from memoryquest_roster import ROSTER
from social_spec import SCENARIOS

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "experiments"))
from assomem_vnext.schema import render_arms, validate_candidate  # noqa: E402

ARMS = ("associative", "distractor", "absence")
SESSION_COUNT = 20

# Demographic, corpus and benchmark-metadata terms that must never reach a visible
# dialogue turn. Matched on word boundaries: a substring test flags "a personal
# best" for containing "persona".
FORBIDDEN_VISIBLE_WORDS = (
    "memoryquest", "persona", "personas", "corpus", "dynamicmem",
    "ev_a", "ev_b", "latent_c", "distractor", "gold", "annotation", "arm_gold",
    "non-binary", "retired", "unemployed", "bachelors", "canada", "ireland",
    "poland", "spain", "mexico",
)
FORBIDDEN_VISIBLE_PATTERNS = tuple(
    (re.compile(rf"\b{re.escape(word)}\b", re.I), word) for word in FORBIDDEN_VISIBLE_WORDS
) + (
    (re.compile(r"mq_user", re.I), "mq_user"),
    (re.compile(r"\buser\d+\b", re.I), "raw persona file id"),
    (re.compile(r"south africa", re.I), "south africa"),
)

# Surface hazards that templating produces and a human skim misses.
LANGUAGE_HAZARDS = (
    (re.compile(r"\ba the\b", re.I), "double article 'a the'"),
    (re.compile(r"\ban the\b", re.I), "double article 'an the'"),
    (re.compile(r"\bthe the\b", re.I), "repeated 'the the'"),
    (re.compile(r"\bto to\b", re.I), "repeated 'to to'"),
    (re.compile(r"\bof of\b", re.I), "repeated 'of of'"),
    (re.compile(r"\bin in\b", re.I), "repeated 'in in'"),
    (re.compile(r"\ba a\b", re.I), "repeated 'a a'"),
    (re.compile(r"\{|\}"), "unsubstituted template brace"),
    (re.compile(r"  +"), "double space"),
    (re.compile(r"\ba an\b", re.I), "article mismatch 'a an'"),
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _session_text(session: dict[str, Any]) -> str:
    return " ".join(turn["content"] for turn in session["dialogue"])


def _visible_text(candidate: dict[str, Any]) -> str:
    return " ".join(_session_text(session) for session in candidate["context"])


def _turn_count(session: dict[str, Any]) -> int:
    return len(session["dialogue"])


def _chars(session: dict[str, Any]) -> int:
    return len(_session_text(session))


def audit(candidates_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    stats: dict[str, Any] = {
        "query_types": Counter(),
        "polarities": Counter(),
        "bridge_types": Counter(),
        "personas": Counter(),
        "slot_signatures": set(),
        "queries": defaultdict(list),
        "c_inferences": defaultdict(list),
    }

    for scenario_index in range(1, 21):
        scenario = next(s for s in SCENARIOS if s["s"] == scenario_index)
        for user_index in range(1, 11):
            pair_id = f"AMB_SC_S{scenario_index}_U{user_index:02d}"
            errors: list[str] = []
            warnings: list[str] = []

            paths = {
                arm: candidates_root / arm / f"{pair_id}_{arm}.json" for arm in ARMS
            }
            missing = [arm for arm, path in paths.items() if not path.is_file()]
            if missing:
                rows.append({
                    "pair_id": pair_id, "errors": f"missing arms: {','.join(missing)}",
                    "warnings": "", "status": "error",
                })
                continue
            files = {arm: _load(path) for arm, path in paths.items()}
            associative = files["associative"]

            # ---- 1. repository schema validation on every arm
            for arm, candidate in files.items():
                for error in validate_candidate(candidate):
                    errors.append(f"{arm}: schema: {error}")

            # ---- 2. allocation agreement (Stage 0 freeze is authoritative)
            expected_type = allocation.query_type(scenario_index, user_index)
            expected_polarity = allocation.polarity(scenario_index, user_index)
            if associative["query_type"] != expected_type:
                errors.append(f"query_type {associative['query_type']} != frozen {expected_type}")
            if associative["polarity"] != expected_polarity:
                errors.append(f"polarity {associative['polarity']} != frozen {expected_polarity}")
            if associative["sub_scenario"]["bridge_type"] != allocation.BRIDGE_TYPES[scenario_index]:
                errors.append("bridge_type disagrees with the frozen allocation")

            # ---- 3. pair consistency (DATA CRITERIA section 6)
            for field in ("pair_id", "domain", "user_id", "query", "query_type", "polarity"):
                values = {json.dumps(candidate[field], sort_keys=True) for candidate in files.values()}
                if len(values) != 1:
                    errors.append(f"pair disagrees on {field}")
            for field in ("latent_C", "answer_contract"):
                values = {json.dumps(candidate[field], sort_keys=True) for candidate in files.values()}
                if len(values) != 1:
                    errors.append(f"pair disagrees on {field}")

            # ---- 4. session counts on every source and every rendered ablation
            for arm, candidate in files.items():
                if len(candidate["context"]) != SESSION_COUNT:
                    errors.append(f"{arm}: {len(candidate['context'])} sessions, expected {SESSION_COUNT}")
                ids = [session["session_id"] for session in candidate["context"]]
                if ids != list(range(1, SESSION_COUNT + 1)):
                    errors.append(f"{arm}: session ids are not 1..{SESSION_COUNT} in order")
            try:
                rendered = render_arms(associative)
            except Exception as exc:  # noqa: BLE001 - surfaced as an audit error
                rendered = {}
                errors.append(f"render_arms failed: {exc}")
            for arm_name, arm in rendered.items():
                if len(arm["context"]) != SESSION_COUNT:
                    errors.append(f"rendered {arm_name}: {len(arm['context'])} sessions")

            # ---- 5. matched replacements (section 3 length-control contract)
            a_sid = associative["evidence"]["ev_A"]["session_id"]
            b_sid = associative["evidence"]["ev_B"]["session_id"]
            by_id = {s["session_id"]: s for s in associative["context"]}
            replacements = {
                "a_only": (associative["single_evidence_replacements"]["a_only"], b_sid),
                "b_only": (associative["single_evidence_replacements"]["b_only"], a_sid),
                "link_broken": (associative["link_broken"], b_sid),
            }
            for name, (block, replaced_sid) in replacements.items():
                if block["replaced_session_id"] != replaced_sid:
                    errors.append(f"{name} replaces session {block['replaced_session_id']}, expected {replaced_sid}")
                dialogue = block["replacement_dialogue"]
                original = by_id[replaced_sid]
                if len(dialogue) != _turn_count(original):
                    errors.append(f"{name} replacement has {len(dialogue)} turns, original has {_turn_count(original)}")
                original_chars = _chars(original)
                new_chars = len(" ".join(turn["content"] for turn in dialogue))
                if original_chars and not 0.25 <= new_chars / original_chars <= 4.0:
                    warnings.append(f"{name} replacement length ratio {new_chars / original_chars:.2f}")

            # ---- 6. a_only / b_only must not paraphrase the removed target
            for name, (block, replaced_sid) in replacements.items():
                if name == "link_broken":
                    continue
                removed = _session_text(by_id[replaced_sid]).lower()
                new_text = " ".join(turn["content"] for turn in block["replacement_dialogue"]).lower()
                removed_words = {w for w in re.findall(r"[a-z']{5,}", removed)}
                new_words = {w for w in re.findall(r"[a-z']{5,}", new_text)}
                if removed_words and len(removed_words & new_words) / len(removed_words) > 0.3:
                    errors.append(f"{name} replacement paraphrases the removed target session")

            # ---- 7. link_broken must change only the connector
            lb_text = " ".join(
                turn["content"] for turn in associative["link_broken"]["replacement_dialogue"]
            ).lower()
            if "friend" in lb_text and "not the user" in lb_text:
                errors.append("link_broken reattributes the episode instead of breaking the relation")
            if len(associative["link_broken"]["replacement_dialogue"]) != _turn_count(by_id[b_sid]):
                errors.append("link_broken changes the turn count of ev_B")

            # ---- 8. distractor rules (section 5.2)
            distractor = files["distractor"]
            dist_sid = distractor["distractor_note"]["replaced_session_id"]
            if distractor["episode_annotations"][str(dist_sid)]["role"] != "distractor":
                errors.append("distractor session is not annotated as the distractor")
            for sid in (a_sid, b_sid):
                if _session_text(distractor["context"][sid - 1]) != _session_text(by_id[sid]):
                    errors.append(f"distractor arm altered target session {sid}")
            dist_text = _session_text(distractor["context"][dist_sid - 1]).lower()
            for evidence_id in ("ev_A", "ev_B"):
                fact_words = set(re.findall(r"[a-z']{5,}", associative["evidence"][evidence_id]["fact"].lower()))
                dist_words = set(re.findall(r"[a-z']{5,}", dist_text))
                if fact_words and len(fact_words & dist_words) / len(fact_words) > 0.4:
                    errors.append(f"distractor restates {evidence_id}")
            if set(distractor["arm_gold"]) != {"distractor"}:
                errors.append("distractor arm_gold is not exactly {distractor}")

            # ---- 9. absence rules (section 5.3)
            absence = files["absence"]
            if absence.get("target_evidence_ids") != []:
                errors.append("absence exposes target_evidence_ids")
            if absence["absence_note"]["replaced_session_ids"] != [a_sid, b_sid]:
                errors.append("absence_note does not record both target sessions")
            # The absence source legitimately keeps E1, E2 and the query, and those
            # name the same option and commitment the target episodes do. So the
            # leak test uses each episode's *distinctive* vocabulary - what is left
            # after removing everything the retained material already says - and
            # tests it per session, not against the concatenated context.
            retained = " ".join([
                associative["query"],
                associative["relation_specificity"]["nearby_relation"],
            ]).lower()
            retained_words = set(re.findall(r"[a-z']{5,}", retained))
            for evidence_id in ("ev_A", "ev_B"):
                fact_words = set(re.findall(
                    r"[a-z']{5,}", associative["evidence"][evidence_id]["fact"].lower()
                ))
                distinctive = fact_words - retained_words
                if len(distinctive) < 3:
                    warnings.append(
                        f"{evidence_id} shares almost all vocabulary with the retained constraints"
                    )
                    continue
                for session in absence["context"]:
                    words = set(re.findall(r"[a-z']{5,}", _session_text(session).lower()))
                    overlap = len(distinctive & words) / len(distinctive)
                    if overlap > 0.5:
                        errors.append(
                            f"absence session {session['session_id']} carries {evidence_id} "
                            f"content ({overlap:.0%} of its distinctive words)"
                        )
            for sid in (a_sid, b_sid):
                if _session_text(absence["context"][sid - 1]) == _session_text(by_id[sid]):
                    errors.append(f"absence session {sid} was not replaced")
            for sid in (a_sid, b_sid):
                if absence["episode_annotations"][str(sid)]["role"] != "background_memory":
                    errors.append(f"absence session {sid} is still annotated as a target")
            if absence["connector_spans"]:
                errors.append("absence retains connector spans")
            if "withheld" not in json.dumps(absence["evidence"]):
                errors.append("absence retains target evidence text")

            # ---- 10. the query must not leak the decision or name the episodes
            query = associative["query"].lower()
            calibrated = associative["latent_C"]["calibrated_language"].lower()
            for banned in ("poor fit", "good fit", "not enough basis", "a poor", "a good"):
                if banned in query:
                    errors.append(f"query leaks a verdict phrase: {banned!r}")
            if associative["latent_C"]["inference"].lower() in query:
                errors.append("query contains latent_C verbatim")
            if calibrated and calibrated in query:
                warnings.append("query contains the calibrated_language string")

            # ---- 11. anonymisation of every visible turn, on every arm
            for arm, candidate in files.items():
                visible = _visible_text(candidate)
                for pattern, label in FORBIDDEN_VISIBLE_PATTERNS:
                    if pattern.search(visible):
                        errors.append(f"{arm}: forbidden term in visible dialogue: {label!r}")

            # ---- 12. surface-language hazards in visible text and in the query
            for arm, candidate in files.items():
                visible = _visible_text(candidate)
                for pattern, label in LANGUAGE_HAZARDS:
                    if pattern.search(visible):
                        errors.append(f"{arm}: {label}")
            for pattern, label in LANGUAGE_HAZARDS:
                if pattern.search(associative["latent_C"]["inference"]):
                    errors.append(f"latent_C: {label}")

            # ---- 13. episode-role census must match the 20-session budget
            roles = Counter(a["role"] for a in associative["episode_annotations"].values())
            # Section 3's budget exactly: 2 targets + 2 counterexamples + 16 others
            # (15 background + the retrieval cue).
            expected_roles = {
                "background_memory": 15, "nearby_counterexample": 2,
                "ev_A": 1, "ev_B": 1, "retrieval_cue": 1,
            }
            if dict(roles) != expected_roles:
                errors.append(f"episode role census {dict(roles)} != {expected_roles}")

            # ---- 14. background must not be reused inside one item
            background_texts = [
                _session_text(session) for session in associative["context"]
                if associative["episode_annotations"][str(session["session_id"])]["role"] == "background_memory"
            ]
            if len(set(background_texts)) != len(background_texts):
                errors.append("a background session is duplicated inside the item")

            stats["query_types"][associative["query_type"]] += 1
            stats["polarities"][associative["polarity"]] += 1
            stats["bridge_types"][associative["sub_scenario"]["bridge_type"]] += 1
            stats["personas"][associative["provenance"]["persona_anchor"]] += 1
            stats["slot_signatures"].add((scenario_index, a_sid, b_sid))
            stats["queries"][associative["query"]].append(pair_id)
            stats["c_inferences"][associative["latent_C"]["inference"]].append(pair_id)

            rows.append({
                "pair_id": pair_id,
                "scenario": f"S{scenario_index}",
                "user": f"U{user_index:02d}",
                "query_type": associative["query_type"],
                "polarity": associative["polarity"],
                "bridge_type": associative["sub_scenario"]["bridge_type"],
                "ev_a_session": a_sid,
                "ev_b_session": b_sid,
                "errors": " | ".join(errors),
                "warnings": " | ".join(warnings),
                "status": "error" if errors else ("warn" if warnings else "pass"),
            })

    return rows, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[1] / "candidates-s1-s10-full"
    parser.add_argument("--candidates", type=Path, default=default_root)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "review" / "generation_audit.csv",
    )
    args = parser.parse_args()

    rows, stats = audit(args.candidates)

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "pair_id", "scenario", "user", "query_type", "polarity", "bridge_type",
        "ev_a_session", "ev_b_session", "status", "errors", "warnings",
    ]
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    failures = [row for row in rows if row["status"] == "error"]
    warned = [row for row in rows if row["status"] == "warn"]

    print(f"pairs audited      : {len(rows)}")
    print(f"errors             : {len(failures)}")
    print(f"warnings only      : {len(warned)}")
    print(f"query types        : {dict(sorted(stats['query_types'].items()))}")
    print(f"polarities         : {dict(sorted(stats['polarities'].items()))}")
    print(f"bridge types       : {dict(sorted(stats['bridge_types'].items()))}")
    print(f"persona anchors    : {len(stats['personas'])} distinct, {min(stats['personas'].values())}-{max(stats['personas'].values())} each")
    print(f"distinct (S,A,B)   : {len(stats['slot_signatures'])} (want 20 - one slot layout per scenario)")

    duplicate_queries = {q: ids for q, ids in stats["queries"].items() if len(ids) > 1}
    duplicate_c = {c: ids for c, ids in stats["c_inferences"].items() if len(ids) > 1}
    print(f"duplicate queries  : {len(duplicate_queries)}")
    print(f"duplicate latent_C : {len(duplicate_c)}")
    if duplicate_queries:
        for query, ids in list(duplicate_queries.items())[:5]:
            print(f"   {ids} -> {query[:110]}")
    if duplicate_c:
        for inference, ids in list(duplicate_c.items())[:5]:
            print(f"   {ids} -> {inference[:110]}")

    if failures:
        print("\nfirst failures:")
        for row in failures[:12]:
            print(f"  {row['pair_id']}: {row['errors'][:400]}")
    print(f"\naudit written to {args.csv}")

    if len(stats["personas"]) != len(ROSTER):
        print("persona coverage is incomplete")
        return 1
    return 1 if failures or duplicate_queries or duplicate_c else 0


if __name__ == "__main__":
    raise SystemExit(main())

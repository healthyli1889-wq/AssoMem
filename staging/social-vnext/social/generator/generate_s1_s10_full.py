"""Generate the social-vNext S1-S10 x U01-U10 x 3-arm candidate batch (300 JSON).

Deterministic: no model calls, no randomness, no clock. Re-running overwrites the
tree byte-for-byte, so the batch is reproducible from this file plus
`social_spec.py`, `memoryquest_roster.py` and `allocation.py`.

    python3 generate_s1_s10_full.py [--out <candidates dir>]

Stage 0 (allocation) is verified before anything is written; a quota breach
aborts the run rather than producing a batch that fails audit later.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import allocation
from memoryquest_roster import ANONYMIZATION_NOTE, profile_for
from social_spec import (
    C_TEMPLATES,
    FILLER,
    QUERY_TYPE_FRAMES,
    RELATIONS,
    REPLACEMENT_FILLER,
    scenario_for,
)

SCHEMA_VERSION = "social-vnext-1.0"
DOMAIN = "social"
PREFIX = "SC"
SESSION_COUNT = 20
CUE_SESSION = 20
TONE = "natural_chat_v1"

# Session clock cycle; the date advances one day per session so timestamps stay
# strictly monotonic regardless of the hour.
HOUR_CYCLE = (11, 14, 16, 18, 9)

# S1 opens here; each later scenario starts 45 days on, each later user 3 days on.
BATCH_EPOCH = datetime(2028, 1, 3, tzinfo=timezone.utc)
SCENARIO_STRIDE_DAYS = 45
USER_STRIDE_DAYS = 3

# `conditional` and `non_decision` items need the hedge visible in the cue, or the
# query does not actually ask what the polarity claims it asks.
POLARITY_TAIL = {
    "reject": "?",
    "accept": "?",
    "conditional": ", and if the answer depends on something, on what?",
    "non_decision": ", or is there not enough here to call it today?",
}

# A ranking question has to name both candidates or it is not a ranking question.
# An explanation question has to name the combination that goes wrong, so it uses
# the proposed option even when the supported answer endorses the alternative.
NEEDS_BOTH_OPTIONS = frozenset({"recommendation_ranking"})
ALWAYS_PROPOSED_OPTION = frozenset({"behavior_explanation"})


def _base_clause(scenario: dict, query_type: str, polarity: str, subs: dict[str, str]) -> str:
    proposed = scenario["query_option"].format(**subs)
    alternative = scenario["query_alt"].format(**subs)
    if query_type in NEEDS_BOTH_OPTIONS:
        return f"{proposed}, or {subs['protective']}"
    if query_type in ALWAYS_PROPOSED_OPTION:
        return proposed
    return alternative if polarity == "accept" else proposed


# --------------------------------------------------------------------------
# Small builders
# --------------------------------------------------------------------------


def _turns(triple: tuple[str, str, str], subs: dict[str, str]) -> list[dict[str, str]]:
    user_open, assistant, user_close = triple
    return [
        {"role": "user", "content": user_open.format(**subs)},
        {"role": "assistant", "content": assistant.format(**subs)},
        {"role": "user", "content": user_close.format(**subs)},
    ]


def _session(session_id: int, user_id: str, start: datetime, dialogue: list[dict[str, str]]) -> dict[str, Any]:
    stamp = start + timedelta(days=session_id - 1)
    stamp = stamp.replace(hour=HOUR_CYCLE[(session_id - 1) % len(HOUR_CYCLE)], minute=0, second=0)
    return {
        "session_id": session_id,
        "timestamp": stamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "speaker_id": user_id,
        "speaker_label": "User",
        "dialogue": dialogue,
    }


def _filler_indices(scenario_index: int, user_index: int, count: int) -> list[int]:
    """17 distinct filler sessions per item: 13 background + 4 replacements."""
    offset = (scenario_index * 13 + user_index * 7) % len(FILLER)
    return [(offset + step) % len(FILLER) for step in range(count)]


def _quote(text: str) -> str:
    """A connector span must be a literal visible substring of its session."""
    return text.rstrip(" .")


def _triple_chars(triple: tuple[str, str, str]) -> int:
    return len(" ".join(triple))


def _pick_replacement(
    target_chars: int, used: set[int], rotation: int
) -> tuple[int, tuple[str, str, str]]:
    """Closest-length unused neutral session, so the ablation matches `full`."""
    order = [
        (index + rotation) % len(REPLACEMENT_FILLER) for index in range(len(REPLACEMENT_FILLER))
    ]
    best = min(
        (index for index in order if index not in used),
        key=lambda index: (abs(_triple_chars(REPLACEMENT_FILLER[index]) - target_chars), order.index(index)),
    )
    used.add(best)
    return best, REPLACEMENT_FILLER[best]


# --------------------------------------------------------------------------
# One unit
# --------------------------------------------------------------------------


def build_unit(scenario_index: int, user_index: int) -> dict[str, dict[str, Any]]:
    scenario = scenario_for(scenario_index)
    profile = profile_for(user_index)
    slug = scenario["slug"]
    slots = scenario["slots"]
    a_sid, b_sid = slots["a"], slots["b"]
    e1_sid, e2_sid = slots["e1"], slots["e2"]
    cx_sids = list(slots["cx"])
    dist_sid = slots["dist"]

    reserved = {a_sid, b_sid, e1_sid, e2_sid, CUE_SESSION, *cx_sids}
    if len(reserved) != 7:
        raise ValueError(f"S{scenario_index}: slot collision in {slots}")
    if dist_sid in reserved:
        raise ValueError(f"S{scenario_index}: distractor slot {dist_sid} is not a background slot")

    pair_id = f"AMB_{PREFIX}_S{scenario_index}_U{user_index:02d}"
    user_id = f"social_s{scenario_index}_u{user_index:02d}"
    query_type = allocation.query_type(scenario_index, user_index)
    polarity = allocation.polarity(scenario_index, user_index)

    subs = {
        "a_obj": scenario["a_objs"][user_index - 1],
        "opt": scenario["opts"][user_index - 1],
        "commit": scenario["commits"][user_index - 1],
        "b_obj": scenario.get("b_objs", [""] * 10)[user_index - 1],
        "circle": profile.circle,
        "role": profile.role,
    }
    subs["protective"] = scenario["protective"].format(**subs)

    inference_tmpl, calibrated_tmpl = C_TEMPLATES[slug][polarity]
    inference = inference_tmpl.format(**subs)
    calibrated = calibrated_tmpl.format(**subs)

    base_clause = _base_clause(scenario, query_type, polarity, subs)
    query = QUERY_TYPE_FRAMES[query_type].format(base=base_clause)
    query = query[:-1] + POLARITY_TAIL[polarity]

    start = (
        BATCH_EPOCH
        + timedelta(days=SCENARIO_STRIDE_DAYS * (scenario_index - 1))
        + timedelta(days=USER_STRIDE_DAYS * (user_index - 1))
    )

    background_slots = [
        sid for sid in range(1, SESSION_COUNT + 1) if sid not in reserved
    ]
    background_fillers = _filler_indices(scenario_index, user_index, len(background_slots))

    a_turns = _turns(scenario["a"], subs)
    b_turns = _turns(scenario["b"], subs)
    a_chars = len(" ".join(turn["content"] for turn in a_turns))
    b_chars = len(" ".join(turn["content"] for turn in b_turns))

    # a_only stands in for ev_B, b_only for ev_A, absence for both; each pick is
    # length-matched to the session it replaces and unique within the item.
    used: set[int] = set()
    rotation = (scenario_index * 11 + user_index * 5) % len(REPLACEMENT_FILLER)
    _, repl_a_only = _pick_replacement(b_chars, used, rotation)
    _, repl_b_only = _pick_replacement(a_chars, used, rotation)
    _, repl_abs_a = _pick_replacement(a_chars, used, rotation)
    _, repl_abs_b = _pick_replacement(b_chars, used, rotation)

    context: list[dict[str, Any]] = []
    annotations: dict[str, Any] = {}
    for sid in range(1, SESSION_COUNT + 1):
        if sid == CUE_SESSION:
            dialogue = [{"role": "user", "content": query}]
            annotations[str(sid)] = {"role": "retrieval_cue"}
        elif sid == a_sid:
            dialogue = a_turns
            annotations[str(sid)] = {
                "role": "ev_A",
                "event_elements": {
                    "person": user_id,
                    **{key: value.format(**subs) for key, value in scenario["a_elements"].items()},
                },
            }
        elif sid == b_sid:
            dialogue = b_turns
            annotations[str(sid)] = {
                "role": "ev_B",
                "event_elements": {
                    "person": user_id,
                    **{key: value.format(**subs) for key, value in scenario["b_elements"].items()},
                },
            }
        elif sid == e1_sid:
            dialogue = _turns(scenario["e1"], subs)
            annotations[str(sid)] = {"role": "supporting_constraint", "fact_id": "E1"}
        elif sid == e2_sid:
            dialogue = _turns(scenario["e2"], subs)
            annotations[str(sid)] = {"role": "supporting_constraint", "fact_id": "E2"}
        elif sid in cx_sids:
            dialogue = _turns(scenario["cx"][cx_sids.index(sid)], subs)
            annotations[str(sid)] = {"role": "nearby_counterexample"}
        else:
            dialogue = _turns(FILLER[background_fillers[background_slots.index(sid)]], subs)
            annotations[str(sid)] = {"role": "background_memory"}
        context.append(_session(sid, user_id, start, dialogue))

    relation = RELATIONS[slug]
    nearby = scenario["nearby_relation"].format(**subs)

    shared = {
        "schema_version": SCHEMA_VERSION,
        "pair_id": pair_id,
        "domain": DOMAIN,
        "user_id": user_id,
        "sub_scenario": {
            "family": scenario["family"],
            "role": profile.role,
            "bridge_type": scenario["bridge_type"],
            "one_line": f"{profile.role}: {calibrated}",
        },
        "query_type": query_type,
        "polarity": polarity,
        "query": query,
        "supporting_constraints": {
            "E1": {"session_id": e1_sid, "fact": scenario["e1"][0].format(**subs)},
            "E2": {"session_id": e2_sid, "fact": scenario["e2"][0].format(**subs)},
        },
        "retrieval_cue": {
            "cue_type": query_type,
            "why_it_naturally_retrieves_R": scenario["cue_why"].format(**subs),
        },
        "relation_specificity": {
            "nearby_relation": nearby,
            "why_it_does_not_license_C": scenario["why_not_license"].format(**subs),
        },
        "latent_C": {"inference": inference, "calibrated_language": calibrated},
        "answer_contract": {
            "target_proposition": inference,
            "allowed_decisions": ["yes", "no"],
            "decision_semantics": {
                "yes": "The visible records support the target proposition.",
                "no": (
                    "The visible records do not support the target proposition; this does not "
                    "assert the opposite arrangement is good."
                ),
            },
            "required_output_fields": ["mode", "answer", "evidence_session_ids"],
        },
        "provenance": {
            "persona_anchor": profile.persona_anchor,
            "external_folder_tag": profile.persona_file,
            "external_source": "memoryquest",
            "status": "review_candidate_only",
            "tone": TONE,
            "voice": profile.voice,
            "anonymization": ANONYMIZATION_NOTE,
        },
    }

    evidence = {
        "ev_A": {"session_id": a_sid, "owner": user_id, "fact": a_turns[0]["content"]},
        "ev_B": {"session_id": b_sid, "owner": user_id, "fact": b_turns[0]["content"]},
    }
    connector_spans = [
        {"evidence_id": "ev_A", "session_id": a_sid, "quote": _quote(a_turns[0]["content"])},
        {"evidence_id": "ev_B", "session_id": b_sid, "quote": _quote(b_turns[0]["content"])},
    ]
    relational_connector = {
        "relation": relation,
        "requires_evidence": ["ev_A", "ev_B"],
        "calibration_constraints": ["E1", "E2"],
    }
    coactivation_bridge = (
        f"ev_A and ev_B are the only pair that licenses the target proposition. {relation} "
        f"E1 and E2 fix timing and identity only and do not open a second route to C. "
        f"The nearby relation ({nearby}) does not license it."
    )

    joint = f"connect the session {a_sid} pattern with the session {b_sid} episode"
    cite_both = f"cite both session {a_sid} and session {b_sid}"
    stay_calibrated = (
        f"stay inside the calibrated claim ({calibrated}) rather than a broader claim about the user"
    )
    refuse_opposite = "not claim instead that the proposed arrangement is good"

    associative = {
        **shared,
        "candidate_id": f"{pair_id}_associative",
        "data_arm": "associative",
        "context": context,
        "evidence": evidence,
        "episode_annotations": annotations,
        "relational_connector": relational_connector,
        "connector_spans": connector_spans,
        "coactivation_bridge": coactivation_bridge,
        "arm_gold": {
            "full": {
                "expected_mode": "infer_C",
                "binary_decision": True,
                "required_elements": ["answer yes", joint, cite_both, stay_calibrated],
                "rationale": "ev_A and ev_B jointly support the target proposition; neither does alone.",
            },
            "a_only": {
                "expected_mode": "withhold_C",
                "binary_decision": False,
                "required_elements": [
                    "answer no",
                    f"state that session {a_sid} alone does not establish the target proposition",
                    "not assert the target proposition",
                    refuse_opposite,
                ],
                "rationale": "ev_B is replaced by a matched neutral session, so the relation is unavailable.",
            },
            "b_only": {
                "expected_mode": "withhold_C",
                "binary_decision": False,
                "required_elements": [
                    "answer no",
                    f"state that session {b_sid} alone does not establish the target proposition",
                    "not assert the target proposition",
                    refuse_opposite,
                ],
                "rationale": "ev_A is replaced by a matched neutral session, so the relation is unavailable.",
            },
            "link_broken": {
                "expected_mode": "withhold_C",
                "binary_decision": False,
                "required_elements": [
                    "answer no",
                    f"state that the revised session {b_sid} no longer connects to session {a_sid}",
                    "not assert the original target proposition",
                    refuse_opposite,
                ],
                "rationale": (
                    "B-prime keeps the owner, date, session form and turn count while removing the "
                    "connector, so the original relation no longer holds."
                ),
            },
        },
        "single_evidence_replacements": {
            "a_only": {
                "replaced_session_id": b_sid,
                "replacement_dialogue": _turns(repl_a_only, subs),
            },
            "b_only": {
                "replaced_session_id": a_sid,
                "replacement_dialogue": _turns(repl_b_only, subs),
            },
        },
        "link_broken": {
            "replaced_session_id": b_sid,
            "replacement_dialogue": _turns(scenario["lb"], subs),
        },
    }

    # ---- distractor: one background session swapped for a tempting non-evidence one
    why_distractor = (
        f"It endorses {subs['opt']} in the user's own feed, so it competes for attention, but it "
        f"reports someone else's confidence rather than any episode of this user's, and it says "
        f"nothing about the relation between session {a_sid} and session {b_sid}."
    )
    distractor_context = [dict(session) for session in context]
    distractor_annotations = {key: dict(value) for key, value in annotations.items()}
    for index, session in enumerate(distractor_context):
        if session["session_id"] == dist_sid:
            replaced = dict(session)
            replaced["dialogue"] = _turns(scenario["dist"], subs)
            distractor_context[index] = replaced
    distractor_annotations[str(dist_sid)] = {
        "role": "distractor",
        "distractor_id": "dist_1",
        "why_distractor": why_distractor,
    }
    distractor = {
        **shared,
        "candidate_id": f"{pair_id}_distractor",
        "data_arm": "distractor",
        "context": distractor_context,
        "evidence": evidence,
        "episode_annotations": distractor_annotations,
        "relational_connector": relational_connector,
        "connector_spans": connector_spans,
        "coactivation_bridge": coactivation_bridge,
        "arm_gold": {
            "distractor": {
                "expected_mode": "infer_C",
                "binary_decision": True,
                "required_elements": [
                    "answer yes",
                    joint,
                    cite_both,
                    f"not cite session {dist_sid} as support",
                ],
                "rationale": (
                    "The swapped session is query-relevant but non-evidential; the ev_A/ev_B relation "
                    "is untouched, so the target proposition still holds."
                ),
            }
        },
        "distractor_note": {"replaced_session_id": dist_sid, "why_distractor": why_distractor},
    }

    # ---- absence: both target sessions swapped for matched neutral sessions.
    # Beyond the finance batch, the absence source also withholds the evidence
    # text, the connector spans and the bridge, per DATA CRITERIA section 5.3.
    absence_context = [dict(session) for session in context]
    absence_annotations = {key: dict(value) for key, value in annotations.items()}
    for index, session in enumerate(absence_context):
        if session["session_id"] == a_sid:
            replaced = dict(session)
            replaced["dialogue"] = _turns(repl_abs_a, subs)
            absence_context[index] = replaced
            absence_annotations[str(a_sid)] = {"role": "background_memory"}
        elif session["session_id"] == b_sid:
            replaced = dict(session)
            replaced["dialogue"] = _turns(repl_abs_b, subs)
            absence_context[index] = replaced
            absence_annotations[str(b_sid)] = {"role": "background_memory"}
    absence = {
        **shared,
        "candidate_id": f"{pair_id}_absence",
        "data_arm": "absence",
        "context": absence_context,
        "target_evidence_ids": [],
        "evidence": {
            "ev_A": {"session_id": a_sid, "owner": user_id, "withheld": True},
            "ev_B": {"session_id": b_sid, "owner": user_id, "withheld": True},
        },
        "episode_annotations": absence_annotations,
        "relational_connector": {
            "relation": "Withheld in the absence source.",
            "requires_evidence": ["ev_A", "ev_B"],
            "calibration_constraints": ["E1", "E2"],
        },
        "connector_spans": [],
        "coactivation_bridge": "Withheld in the absence source: neither target episode is visible.",
        "arm_gold": {
            "absence": {
                "expected_mode": "withhold_C",
                "binary_decision": False,
                "required_elements": [
                    "answer no",
                    "state that the visible history does not contain the episodes the question needs",
                    "not assert the target proposition",
                    refuse_opposite,
                ],
                "rationale": (
                    "Both target episodes are replaced by matched neutral sessions of the same owner, "
                    "date and turn count, so nothing licenses the target proposition."
                ),
            }
        },
        "absence_note": {
            "replaced_session_ids": [a_sid, b_sid],
            "withheld_evidence_ids": ["ev_A", "ev_B"],
        },
    }

    return {"associative": associative, "distractor": distractor, "absence": absence}


# --------------------------------------------------------------------------
# Batch
# --------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "candidates-s1-s10-full",
        help="candidate root; three arm subdirectories are created below it",
    )
    args = parser.parse_args()

    allocation.verify()

    written = 0
    for arm in ("associative", "distractor", "absence"):
        (args.out / arm).mkdir(parents=True, exist_ok=True)
    for scenario_index in range(1, 11):
        for user_index in range(1, 11):
            unit = build_unit(scenario_index, user_index)
            for arm, candidate in unit.items():
                path = args.out / arm / f"{candidate['candidate_id']}.json"
                path.write_text(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                written += 1
    print(f"Stage 0 verified. Wrote {written} JSON files to {args.out}")


if __name__ == "__main__":
    main()

"""Domain-independent generator for a vNext S1-S20 x U01-U10 x 3-arm batch.

Deterministic: no model calls, no randomness, no clock. Re-running overwrites the
tree byte-for-byte, so a batch is reproducible from this file plus its domain pack.

A domain pack supplies content only - scenarios, relations, roster, filler, the
proposition templates and the query frames. Everything structural lives here:
the 20-session budget, the arm construction rules from DATA CRITERIA section 5,
the length-matched neutral replacements, and the arm gold the harness needs.

Construct rules the packs are written against, each one adopted after a measured
failure rather than on principle (see the social batch README):

- Every target proposition is counter-conventional, so a solver with no memory of
  the person applies the convention and answers `no` - which is gold for every
  ablation arm. Only A+B together flip it to `yes`.
- ev_A gives trigger -> mediator state and fixes the scope of that state; ev_B
  gives mediator state -> outcome. Neither half alone completes the chain, and B
  never restates A's antecedent.
- Mediator states are described specifically but without valence. When A said
  whether the state was good or bad, ev_A alone carried the conclusion.
- `conditional` and `non_decision` bound on the scope condition from ev_A, not on
  the mediator, which ev_B alone establishes.
- Counterexamples are ordinary neutral episodes, never contrastive foils: a line
  like "so it isn't the hour, no" presupposes the target pattern and hands it over.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable

SESSION_COUNT = 20
CUE_SESSION = 20
TONE = "natural_chat_v1"

# Session clock cycle; the date advances one day per session so timestamps stay
# strictly monotonic regardless of the hour.
HOUR_CYCLE = (11, 14, 16, 18, 9)
SCENARIO_STRIDE_DAYS = 45
USER_STRIDE_DAYS = 3

# `conditional` and `non_decision` need the hedge visible in the cue, or the query
# does not actually ask what the polarity claims it asks.
POLARITY_TAIL = {
    "reject": "?",
    "accept": "?",
    "conditional": ", and if the answer depends on something, on what?",
    "non_decision": ", or is there not enough here to call it today?",
}

# A ranking question has to name both candidates or it is not a ranking question.
NEEDS_BOTH_OPTIONS = frozenset({"recommendation_ranking"})


@dataclass(frozen=True)
class DomainPack:
    domain: str
    prefix: str
    schema_version: str
    epoch: datetime
    scenarios: tuple[dict, ...]
    relations: dict[str, str]
    c_templates: dict[str, tuple[str, str]]
    query_type_frames: dict[str, str]
    filler: tuple[tuple[str, str, str], ...]
    replacement_filler: tuple[tuple[str, str, str], ...]
    profile_for: Callable[[int], Any]
    anonymization_note: str
    query_type_of: Callable[[int, int], str]
    polarity_of: Callable[[int, int], str]
    bridge_type_of: dict[int, str]

    def scenario_for(self, index: int) -> dict:
        for scenario in self.scenarios:
            if scenario["s"] == index:
                return scenario
        raise KeyError(f"{self.domain}: no scenario S{index}")


def _turns(triple: tuple[str, str, str], subs: dict[str, str]) -> list[dict[str, str]]:
    user_open, assistant, user_close = triple
    return [
        {"role": "user", "content": user_open.format(**subs)},
        {"role": "assistant", "content": assistant.format(**subs)},
        {"role": "user", "content": user_close.format(**subs)},
    ]


def _session(
    session_id: int, user_id: str, start: datetime, dialogue: list[dict[str, str]]
) -> dict[str, Any]:
    stamp = start + timedelta(days=session_id - 1)
    stamp = stamp.replace(hour=HOUR_CYCLE[(session_id - 1) % len(HOUR_CYCLE)], minute=0, second=0)
    return {
        "session_id": session_id,
        "timestamp": stamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "speaker_id": user_id,
        "speaker_label": "User",
        "dialogue": dialogue,
    }


def _filler_indices(pack: DomainPack, scenario_index: int, user_index: int, count: int) -> list[int]:
    offset = (scenario_index * 13 + user_index * 7) % len(pack.filler)
    return [(offset + step) % len(pack.filler) for step in range(count)]


def _quote(text: str) -> str:
    """A connector span must be a literal visible substring of its session."""
    return text.rstrip(" .")


def _triple_chars(triple: tuple[str, str, str]) -> int:
    return len(" ".join(triple))


def _pick_replacement(
    pack: DomainPack, target_chars: int, used: set[int], rotation: int
) -> tuple[str, str, str]:
    """Closest-length unused neutral session, so the ablation matches `full`."""
    pool = pack.replacement_filler
    order = [(index + rotation) % len(pool) for index in range(len(pool))]
    best = min(
        (index for index in order if index not in used),
        key=lambda index: (abs(_triple_chars(pool[index]) - target_chars), order.index(index)),
    )
    used.add(best)
    return pool[best]


def _base_clause(scenario: dict, query_type: str, polarity: str, subs: dict[str, str]) -> str:
    proposed = (
        scenario["query_conv"] if polarity == "reject" else scenario["query_unconv"]
    ).format(**subs)
    if query_type in NEEDS_BOTH_OPTIONS:
        other = subs["unconv"] if polarity == "reject" else subs["conv"]
        return f"{proposed}, or {other}"
    return proposed


def build_unit(pack: DomainPack, scenario_index: int, user_index: int) -> dict[str, dict[str, Any]]:
    scenario = pack.scenario_for(scenario_index)
    profile = pack.profile_for(user_index)
    slug = scenario["slug"]
    slots = scenario["slots"]
    a_sid, b_sid = slots["a"], slots["b"]
    cx_sids = list(slots["cx"])
    dist_sid = slots["dist"]

    reserved = {a_sid, b_sid, CUE_SESSION, *cx_sids}
    if len(reserved) != 5:
        raise ValueError(f"S{scenario_index}: slot collision in {slots}")
    if dist_sid in reserved:
        raise ValueError(f"S{scenario_index}: distractor slot {dist_sid} is not a background slot")

    pair_id = f"AMB_{pack.prefix}_S{scenario_index}_U{user_index:02d}"
    user_id = f"{pack.domain}_s{scenario_index}_u{user_index:02d}"
    query_type = pack.query_type_of(scenario_index, user_index)
    polarity = pack.polarity_of(scenario_index, user_index)

    subs = {
        "a_obj": scenario["a_objs"][user_index - 1],
        "commit": scenario["commits"][user_index - 1],
        "b_obj": scenario.get("b_objs", [""] * 10)[user_index - 1],
        "mediator": scenario["mediator"],
        "scope": scenario["scope"],
        "circle": profile.circle,
        "role": profile.role,
    }
    subs["unconv"] = scenario["unconv"][user_index - 1].format(**subs)
    subs["conv"] = scenario["conv"][user_index - 1].format(**subs)
    # `reject` items put the conventionally sensible option to the user; every
    # other polarity puts the conventionally reckless one.
    subs["opt"] = subs["conv"] if polarity == "reject" else subs["unconv"]

    inference_tmpl, calibrated_tmpl = pack.c_templates[polarity]
    inference = inference_tmpl.format(**subs)
    calibrated = calibrated_tmpl.format(**subs)

    base_clause = _base_clause(scenario, query_type, polarity, subs)
    query = pack.query_type_frames[query_type].format(base=base_clause)
    query = query[:-1] + POLARITY_TAIL[polarity]

    start = (
        pack.epoch
        + timedelta(days=SCENARIO_STRIDE_DAYS * (scenario_index - 1))
        + timedelta(days=USER_STRIDE_DAYS * (user_index - 1))
    )

    background_slots = [sid for sid in range(1, SESSION_COUNT + 1) if sid not in reserved]
    background_fillers = _filler_indices(pack, scenario_index, user_index, len(background_slots))

    a_turns = _turns(scenario["a"], subs)
    b_turns = _turns(scenario["b"], subs)
    a_chars = len(" ".join(turn["content"] for turn in a_turns))
    b_chars = len(" ".join(turn["content"] for turn in b_turns))

    # a_only stands in for ev_B, b_only for ev_A, absence for both; each pick is
    # length-matched to the session it replaces and unique within the item.
    used: set[int] = set()
    rotation = (scenario_index * 11 + user_index * 5) % len(pack.replacement_filler)
    repl_a_only = _pick_replacement(pack, b_chars, used, rotation)
    repl_b_only = _pick_replacement(pack, a_chars, used, rotation)
    repl_abs_a = _pick_replacement(pack, a_chars, used, rotation)
    repl_abs_b = _pick_replacement(pack, b_chars, used, rotation)

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
        elif sid in cx_sids:
            dialogue = _turns(scenario["cx"][cx_sids.index(sid)], subs)
            annotations[str(sid)] = {"role": "nearby_counterexample"}
        else:
            dialogue = _turns(pack.filler[background_fillers[background_slots.index(sid)]], subs)
            annotations[str(sid)] = {"role": "background_memory"}
        context.append(_session(sid, user_id, start, dialogue))

    relation = pack.relations[slug]
    nearby = scenario["nearby_relation"].format(**subs)

    shared = {
        "schema_version": pack.schema_version,
        "pair_id": pair_id,
        "domain": pack.domain,
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
        "convention_contradicted": scenario["convention"],
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
            "anonymization": pack.anonymization_note,
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
        "calibration_constraints": [],
    }
    coactivation_bridge = (
        f"ev_A and ev_B are the only pair that licenses the target proposition. {relation} "
        f"The proposition contradicts the convention a solver would otherwise apply "
        f"(\"{scenario['convention']}\"), so priors alone point the other way. "
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
        "It restates the conventional advice in the user's own feed, so it competes for attention "
        "and points at the answer a prior-driven solver already wants to give. It reports other "
        f"people's confidence rather than any episode of this user's, and says nothing about the "
        f"relation between session {a_sid} and session {b_sid}."
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

    # ---- absence: both target sessions swapped for matched neutral sessions. Also
    # withholds the evidence text, the connector spans and the bridge, per section 5.3.
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
            "calibration_constraints": [],
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


def generate(pack: DomainPack, out: Path, verify: Callable[[], Any]) -> int:
    """Write the whole batch. Stage 0 is verified before anything is written."""
    verify()
    for arm in ("associative", "distractor", "absence"):
        (out / arm).mkdir(parents=True, exist_ok=True)
    written = 0
    for scenario_index in range(1, len(pack.scenarios) + 1):
        for user_index in range(1, 11):
            for arm, candidate in build_unit(pack, scenario_index, user_index).items():
                path = out / arm / f"{candidate['candidate_id']}.json"
                path.write_text(
                    json.dumps(candidate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
                )
                written += 1
    return written

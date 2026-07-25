"""Directly author the social vNext 102-record pilot without external APIs."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SOCIAL_SCENARIOS = (
    {
        "slug": "hosting_before_mediation",
        "a": "After facilitating a lively group gathering, I need a quiet morning before I can listen carefully to someone else's conflict.",
        "b": "I have a Sunday mediation check-in already booked; it needs patient one-to-one listening.",
        "proposal": "A neighborhood group asks me to host a bigger Saturday evening welcome gathering.",
        "query": "A neighborhood group asked me to host a bigger Saturday welcome gathering. Would taking it on be a risk for me?",
        "c": "The bigger Saturday hosting role should be flagged as a fit risk because it would remove quiet recovery before the user's Sunday mediation check-in.",
        "broken": "I have a Sunday coffee with a friend that can be moved easily; it does not require focused listening.",
    },
    {
        "slug": "group_chat_before_support",
        "a": "When I keep an always-on group chat active late into the evening, I am less patient in a next-day support conversation.",
        "b": "I lead a weekly Sunday support call where a friend expects my full attention.",
        "proposal": "A reunion group asks me to keep a busy message thread running through Saturday night.",
        "query": "The reunion group wants me to keep its message thread active through Saturday night. Would taking that on be a risk for me?",
        "c": "The always-on reunion role should be flagged as a fit risk because it would impair the user's attention for the Sunday support call.",
        "broken": "I have a Sunday call to confirm restaurant reservations; it is routine and can be rescheduled.",
    },
    {
        "slug": "networking_before_repair",
        "a": "A long networking block leaves me socially flat and I struggle to notice nuance in the next difficult conversation.",
        "b": "I have a scheduled private repair conversation on Sunday that needs careful listening.",
        "proposal": "A colleague invites me to spend Saturday afternoon at an extended networking mixer.",
        "query": "A colleague invited me to spend Saturday afternoon at an extended networking mixer. Would that be a risk for me?",
        "c": "The extended networking mixer should be flagged as a fit risk because it would reduce the user's capacity for the scheduled repair conversation.",
        "broken": "I have a Sunday call to share travel photos; it is light and does not require careful listening.",
    },
    {
        "slug": "public_recognition_before_feedback",
        "a": "After I have to respond to public praise without preparation, I replay it for hours and find it hard to write thoughtful feedback.",
        "b": "I have promised to send detailed feedback on a friend's application by Sunday morning.",
        "proposal": "A dinner organizer asks me to take part in a live recognition round on Saturday night.",
        "query": "A dinner organizer asked me to join a live recognition round on Saturday night. Would agreeing to it be a risk for me?",
        "c": "The live recognition round should be flagged as a fit risk because it would interfere with the user's promised detailed feedback.",
        "broken": "I have a Sunday reminder to rate a café online; it needs no thoughtful writing.",
    },
    {
        "slug": "overnight_guest_before_mentoring",
        "a": "When overnight guests keep me talking late, I wake up socially depleted rather than ready to guide someone else.",
        "b": "I mentor a new volunteer on Sunday morning and need to be present for their first shift.",
        "proposal": "A friend asks to stay overnight after a Saturday event at my place.",
        "query": "A friend asked to stay over after Saturday's event. Would saying yes be a risk for me?",
        "c": "Accepting the overnight guest should be flagged as a fit risk because it would leave the user depleted for Sunday mentoring.",
        "broken": "I have a Sunday morning grocery pickup that is self-service and can be delayed.",
    },
    {
        "slug": "late_dinner_before_commitment",
        "a": "After a long late dinner, I need a slow morning before I can reliably coordinate other people.",
        "b": "I am responsible for opening a Sunday volunteer shift where others depend on me to coordinate arrivals.",
        "proposal": "Friends invite me to a Saturday dinner that will likely continue past midnight.",
        "query": "Friends invited me to a Saturday dinner that may run past midnight. Would going be a risk for me?",
        "c": "The late Saturday dinner should be flagged as a fit risk because it would compromise the user's Sunday coordination responsibility.",
        "broken": "I have a Sunday morning walk planned alone; no one depends on me and it can start later.",
    },
    {
        "slug": "drop_in_before_letter",
        "a": "Unexpected evening drop-ins make it hard for me to settle into reflective writing the next day.",
        "b": "I have committed to writing a careful recommendation letter on Sunday afternoon.",
        "proposal": "A friend asks whether their group can stop by my apartment spontaneously on Saturday night.",
        "query": "A friend asked whether their group can stop by spontaneously on Saturday night. Would saying yes be a risk for me?",
        "c": "The spontaneous Saturday drop-in should be flagged as a fit risk because it would disrupt the user's planned recommendation letter writing.",
        "broken": "I have a Sunday afternoon plan to sort old photos; it is optional and can be postponed.",
    },
    {
        "slug": "video_hang_before_reunion",
        "a": "Several back-to-back video hangouts make my voice thin and my attention scattered the following day.",
        "b": "I have an in-person reunion lunch on Sunday where I need energy to reconnect with a close friend.",
        "proposal": "A group invites me to join a long sequence of video hangouts on Saturday.",
        "query": "A group invited me to a long sequence of video hangouts on Saturday. Would joining be a risk for me?",
        "c": "The stacked video hangouts should be flagged as a fit risk because they would impair the user's energy for the reunion lunch.",
        "broken": "I have a Sunday lunch alone at a flexible time; it does not require social energy.",
    },
    {
        "slug": "late_party_before_airport_help",
        "a": "After a midnight party, I am not alert enough to navigate logistics for someone else the next morning.",
        "b": "I have promised to meet a visiting relative at the airport early Sunday and help them reach the city.",
        "proposal": "Friends invite me to a Saturday midnight send-off party.",
        "query": "Friends invited me to a midnight send-off party on Saturday. Would going be a risk for me?",
        "c": "The midnight send-off party should be flagged as a fit risk because it would undermine the user's airport-help commitment.",
        "broken": "I have a Sunday morning reminder to water plants; it does not require alert logistical support.",
    },
    {
        "slug": "open_house_before_planning",
        "a": "Hosting an open-house style event consumes the focused attention I need for careful relationship planning afterward.",
        "b": "I have a Sunday planning call with my sibling about a sensitive family visit.",
        "proposal": "A neighbor asks me to host an open-house event on Saturday evening.",
        "query": "A neighbor asked me to host an open-house event on Saturday evening. Would taking that on be a risk for me?",
        "c": "The Saturday open-house event should be flagged as a fit risk because it would reduce the user's capacity for the sensitive family planning call.",
        "broken": "I have a Sunday call to pick a movie with my sibling; it is low stakes and can be moved.",
    },
)

PERSONAS = (
    "keep a small paper calendar",
    "prefer one-to-one conversations to group chatter",
    "take evening walks to reset",
    "write short notes after busy weekends",
    "like hosting small dinners",
    "plan commitments a week ahead",
    "value dependable follow-through",
    "use quiet mornings for reflection",
    "check in with close friends regularly",
    "avoid making rushed social promises",
)


def _session(session_id: int, timestamp: datetime, user_id: str, text: str, reply: str) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "speaker_id": user_id,
        "speaker_label": "User",
        "dialogue": [
            {"role": "user", "content": text},
            {"role": "assistant", "content": reply},
        ],
    }


def _background_text(user_id: str, persona: str, session_id: int) -> tuple[str, str]:
    topics = (
        ("I updated my paper calendar before the week began.", "Keeping a visible plan helps you notice commitments."),
        ("I sent a short check-in to a friend after work.", "A brief check-in can still be meaningful."),
        ("I took a quiet walk after dinner.", "A small reset can make an evening feel less crowded."),
        ("I sorted a few photos from a recent trip.", "Low-pressure tasks can be restorative."),
        ("I made tea before reading for a while.", "You made room for a calm transition."),
        ("I wrote down a reminder for next week.", "External reminders protect follow-through."),
        ("I had a small lunch with a colleague.", "Smaller formats can leave room for the rest of the day."),
        ("I cleared a few messages before bed.", "Closing small loops can make tomorrow easier."),
        ("I chose a quiet route home.", "You protected a little decompression time."),
        ("I checked my weekend plan once more.", "Seeing the plan makes trade-offs easier to notice."),
        ("I put a library book by the door.", "You prepared for a simple errand."),
        ("I watered the plants before breakfast.", "A small routine can anchor the morning."),
        ("I organized a drawer that had been bothering me.", "A contained task gave you a reset."),
        ("I listened to a short podcast while cooking.", "You kept the evening low-pressure."),
        ("I replied to an invitation with a clear boundary.", "Clear expectations reduce social friction."),
        ("I made a note to call a relative next month.", "You planned the connection without rushing it."),
        ("I booked a routine appointment.", "You handled a practical detail early."),
    )
    text, reply = topics[(session_id + int(user_id[-2:])) % len(topics)]
    if session_id == 1:
        return f"I {persona}. {text}", reply
    return text, reply


def _annotations(context: list[dict[str, Any]], user_id: str, a_text: str, b_text: str) -> dict[str, Any]:
    annotations: dict[str, Any] = {}
    for session in context:
        sid = str(session["session_id"])
        annotations[sid] = {"role": "background_memory", "summary": "Non-target social memory."}
    annotations["5"] = {
        "role": "ev_A",
        "event_elements": {
            "person": user_id,
            "context": "A demanding social exposure",
            "goal_or_prediction": "Remain attentive the following day",
            "action": a_text,
            "outcome_or_affect": "Needs recovery before a demanding interpersonal task",
        },
    }
    annotations["12"] = {
        "role": "ev_B",
        "event_elements": {
            "person": user_id,
            "context": "A scheduled next-day social responsibility",
            "goal_or_prediction": "Show up attentively for another person",
            "action": b_text,
            "outcome_or_affect": "Creates the situational condition needed for latent C",
        },
    }
    annotations["20"] = {"role": "retrieval_cue", "summary": "Later fit question."}
    return annotations


def _core_gold(scenario: dict[str, str]) -> dict[str, dict[str, Any]]:
    return {
        "full": {
            "expected_mode": "infer_C",
            "binary_decision": True,
            "required_elements": [
                "answer yes",
                "connect the social-exposure recovery pattern with the scheduled next-day responsibility",
                "cite both session 5 and session 12",
                "state the calibrated fit-risk conclusion",
            ],
            "rationale": "A and B jointly support the target proposition.",
        },
        "a_only": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": [
                "answer no",
                "state that no specific next-day responsibility is available",
                "withhold the target proposition",
            ],
            "rationale": "A alone does not establish that the proposed event conflicts with a concrete responsibility.",
        },
        "b_only": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": [
                "answer no",
                "state that no exposure-recovery pattern is available",
                "withhold the target proposition",
            ],
            "rationale": "B alone does not establish that the proposed event would impair the responsibility.",
        },
        "link_broken": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": [
                "answer no",
                "identify that the replacement responsibility is low stakes or movable",
                "withhold the target proposition",
            ],
            "rationale": "B-prime removes the responsibility connector while retaining same-user conversational form.",
        },
    }


def _candidate(pair_number: int, source_arm: str) -> dict[str, Any]:
    scenario_index = (pair_number - 1) % len(SOCIAL_SCENARIOS)
    cycle = (pair_number - 1) // len(SOCIAL_SCENARIOS)
    scenario = SOCIAL_SCENARIOS[scenario_index]
    # Rotate persona assignment on every scenario cycle. This preserves scenario
    # coverage while preventing the duplicated scenario×persona combinations caused
    # by using the same modulus for both dimensions.
    user_number = ((scenario_index + cycle) % len(PERSONAS)) + 1
    user_id = f"anon_social_user_{user_number:02d}"
    pair_id = f"AMB_SV_{scenario['slug']}_{pair_number:03d}"
    persona = PERSONAS[user_number - 1]
    start = datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc)
    context = []
    for session_id in range(1, 21):
        timestamp = start + timedelta(days=session_id * 3)
        text, reply = _background_text(user_id, persona, session_id)
        context.append(_session(session_id, timestamp, user_id, text, reply))
    context[4] = _session(5, start + timedelta(days=15), user_id, scenario["a"], "That sounds like a repeatable recovery pattern.")
    context[11] = _session(12, start + timedelta(days=36), user_id, scenario["b"], "That responsibility has a specific interpersonal demand.")
    context[19] = _session(20, start + timedelta(days=60), user_id, scenario["proposal"], "It is worth checking the fit against the commitments you already described.")
    annotations = _annotations(context, user_id, scenario["a"], scenario["b"])
    core_gold = _core_gold(scenario)
    candidate = {
        "schema_version": "assomem-vnext-1.2",
        "candidate_id": f"{pair_id}_{source_arm}",
        "pair_id": pair_id,
        "domain": "social",
        "user_id": user_id,
        "query_type": "situational_fit",
        "polarity": "reject",
        "context": context,
        "query": scenario["query"],
        "evidence": {
            "ev_A": {"session_id": 5, "owner": user_id, "fact": scenario["a"]},
            "ev_B": {"session_id": 12, "owner": user_id, "fact": scenario["b"]},
        },
        "episode_annotations": annotations,
        "relational_connector": {
            "relation": "A social-exposure recovery pattern creates a fit risk only when paired with B's specific next-day interpersonal responsibility.",
            "requires_evidence": ["ev_A", "ev_B"],
            "excludes": ["all social events are unsuitable", "all next-day plans are incompatible"],
            "link_broken_change": "The next-day activity is replaced with a low-stakes, movable activity.",
        },
        "connector_spans": [
            {"evidence_id": "ev_A", "session_id": 5, "quote": scenario["a"].split(".")[0]},
            {"evidence_id": "ev_B", "session_id": 12, "quote": scenario["b"].split(".")[0]},
        ],
        "retrieval_cue": {
            "cue_type": "situational_fit",
            "why_it_naturally_retrieves_R": "The new invitation asks about fit without naming either prior episode.",
        },
        "relation_specificity": {
            "nearby_relation": "The user can enjoy small, low-demand social contact.",
            "why_it_does_not_license_C": "That fact does not establish a recovery-to-responsibility conflict.",
        },
        "coactivation_bridge": f"ev_A describes why the proposed exposure needs recovery; ev_B establishes the specific responsibility that would be impaired. Together they support C: {scenario['c']}",
        "latent_C": {"inference": scenario["c"], "calibrated_language": "flagged as a fit risk"},
        "answer_contract": {
            "target_proposition": scenario["c"],
            "allowed_decisions": ["yes", "no"],
            "decision_semantics": {
                "yes": "Visible evidence supports the target proposition.",
                "no": "Visible evidence does not support the target proposition.",
            },
            "required_output_fields": ["decision", "answer", "evidence_session_ids"],
        },
        "link_broken": {
            "replacement_dialogue": [
                {"role": "user", "content": scenario["broken"]},
                {"role": "assistant", "content": "That Sunday activity is low stakes and can be moved without affecting another person."},
            ],
            "connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed interpersonal responsibility.",
            "rationale": "A plus B-prime no longer supports the original C.",
        },
        "provenance": {
            "authoring_method": "directly authored social vNext pilot",
            "created_at": "2026-07-24",
            "anonymous_submission": True,
            "source_person_name": None,
            "source_corpus": None,
            "gate_0_review_path": "../review/gate_0.csv",
            "gate_0_review_unit": "social_v1_relational",
            "release_eligible": False,
            "materialized_from": pair_id,
            "source_data_arm": source_arm,
        },
        "data_arm": source_arm,
        "available_evaluation_conditions": ["full", "a_only", "b_only", "link_broken"],
    }
    if source_arm == "associative":
        candidate["arm_gold"] = core_gold
        if pair_number <= 7:
            friend_name = ("Alex", "Maya", "Jordan", "Priya", "Sam", "Nora", "Leo")[pair_number - 1]
            candidate["source_swap"] = {
                "speaker_id": f"friend_{pair_number:03d}",
                "speaker_label": friend_name,
                "replacement_dialogue": [
                    {"role": "user", "content": f"My friend {friend_name} told me: “{scenario['b']}”"},
                    {"role": "assistant", "content": f"That sounds like {friend_name}'s commitment, not yours."},
                ],
            }
            candidate["arm_gold"]["source_swap"] = {
                "expected_mode": "source_withhold",
                "binary_decision": False,
                "required_elements": ["answer no", "do not attribute the other person's fact to the user"],
                "rationale": "Other-person evidence cannot support a target-user conclusion.",
            }
    elif source_arm == "distractor":
        candidate["arm_gold"] = {
            "distractor": {
                **core_gold["full"],
                "expected_mode": "infer_C",
            }
        }
        candidate["distractor"] = {
            "added_session": _session(
                18,
                start + timedelta(days=54),
                user_id,
                "A friend says the invitation would be great for meeting more neighbors.",
                "That is a tempting social benefit, but it does not establish the user's recovery pattern.",
            )
        }
        candidate["context"][17] = candidate["distractor"]["added_session"]
        candidate["episode_annotations"]["18"] = {"role": "distractor", "summary": "Query-relevant social upside without target evidence."}
    else:
        candidate["arm_gold"] = {
            "absence": {
                "expected_mode": "withhold_C",
                "binary_decision": False,
                "required_elements": ["answer no", "state that the visible evidence does not support the target proposition"],
                "rationale": "Both necessary target episodes are unavailable.",
            }
        }
        candidate["target_evidence_ids"] = []
        candidate["context"][4] = _session(5, start + timedelta(days=15), user_id, "I organized a bookshelf after dinner.", "A quiet household task was straightforward.")
        candidate["context"][11] = _session(12, start + timedelta(days=36), user_id, "I scheduled a routine grocery pickup.", "The errand can be completed at a flexible time.")
        candidate["episode_annotations"]["5"] = {"role": "background_memory", "summary": "Neutral replacement for removed evidence."}
        candidate["episode_annotations"]["12"] = {"role": "background_memory", "summary": "Neutral replacement for removed evidence."}
    return candidate


def build_social_pilot(destination: Path, count: int = 34) -> dict[str, int]:
    if count != 34:
        raise ValueError("The authorized social pilot must contain exactly 34 source triads")
    shutil.rmtree(destination / "artifacts", ignore_errors=True)
    for source_arm in ("associative", "distractor", "absence"):
        shutil.rmtree(destination / source_arm, ignore_errors=True)
        (destination / source_arm).mkdir(parents=True, exist_ok=True)
    for pair_number in range(1, count + 1):
        for source_arm in ("associative", "distractor", "absence"):
            candidate = _candidate(pair_number, source_arm)
            path = destination / source_arm / f"{candidate['candidate_id']}.json"
            path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"base_candidates": count, "source_records": count * 3}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(json.dumps(build_social_pilot(args.destination), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

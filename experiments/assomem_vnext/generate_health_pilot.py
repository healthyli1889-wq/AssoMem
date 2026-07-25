"""Directly author the health vNext pilot without external APIs.

Mirrors generate_social_pilot.py's structure and schema (assomem-vnext-1.2)
exactly, swapping in health-topic scenario content. Unlike the social pilot,
pair count is capped at len(HEALTH_SCENARIOS) so every pair gets a unique
scenario AND a unique persona/user_id -- the social generator cycled 34 pairs
over 10 scenarios x 10 personas with the same modulus for both, which made
every 10th pair (7/17/27) collide on both axes and come out byte-identical.
No source_swap arm is authored here; VNEXT_EVALUATION_ARMS in run.py does not
evaluate it and the health-vnext-1 profile marks that capability false.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


HEALTH_SCENARIOS = (
    {
        "slug": "late_screen_before_migraine_checkin",
        "a": "Late-night screen time before bed leaves me with a lingering headache that makes it hard to concentrate the next morning.",
        "b": "I have a Sunday morning migraine-tracking check-in with my neurologist's care coordinator where I need to give clear, detailed symptom notes.",
        "proposal": "A friend invites me to a Saturday night movie marathon with a bright screen the whole time.",
        "query": "Based only on these records, should the Saturday night movie marathon be flagged as a fit risk for this user?",
        "c": "The Saturday night movie marathon should be flagged as a fit risk because it would leave a lingering headache right when Sunday's migraine check-in needs clear symptom reporting.",
        "broken": "I have a Sunday reminder to reorder a prescription online; it takes two minutes and needs no symptom reporting.",
    },
    {
        "slug": "heavy_meal_before_fasting_bloodwork",
        "a": "A heavy meal late at night leaves my stomach upset and my sleep broken, and I feel foggy through the next morning.",
        "b": "I have a Sunday morning fasting bloodwork appointment where I need to arrive alert and follow the phlebotomist's instructions carefully.",
        "proposal": "Coworkers invite me to a Saturday night all-you-can-eat dinner that runs late.",
        "query": "Based only on these records, should the Saturday night all-you-can-eat dinner be flagged as a fit risk for this user?",
        "c": "The Saturday night all-you-can-eat dinner should be flagged as a fit risk because it would leave me foggy exactly when Sunday's fasting bloodwork needs alertness.",
        "broken": "I have a Sunday reminder to renew a gym membership online; it needs no alertness or fasting.",
    },
    {
        "slug": "loud_concert_before_hearing_test",
        "a": "After a loud concert my ears ring and I have trouble picking out quiet sounds accurately for about a day.",
        "b": "I have a Sunday morning hearing test scheduled where I need to reliably detect faint tones.",
        "proposal": "A friend invites me to a loud Saturday night concert with front-row seats.",
        "query": "Based only on these records, should the loud Saturday night concert be flagged as a fit risk for this user?",
        "c": "The loud Saturday night concert should be flagged as a fit risk because it would impair sound processing exactly when Sunday's hearing test needs accurate faint-tone detection.",
        "broken": "I have a Sunday reminder to pick up a refill at the pharmacy; it needs no auditory precision.",
    },
    {
        "slug": "late_drinking_before_medication_review",
        "a": "Drinking late into the evening makes me groggy and less careful about details the next morning.",
        "b": "I have a Sunday morning medication review with my pharmacist where I need to accurately report every dose and timing change.",
        "proposal": "Friends invite me to a Saturday night bar crawl that goes past midnight.",
        "query": "Based only on these records, should the Saturday night bar crawl be flagged as a fit risk for this user?",
        "c": "The Saturday night bar crawl should be flagged as a fit risk because grogginess would compromise the careful dose reporting Sunday's medication review needs.",
        "broken": "I have a Sunday reminder to water the office plants; it needs no careful reporting.",
    },
    {
        "slug": "hot_yoga_before_bp_check",
        "a": "An intense hot yoga session leaves me dehydrated with my heart rate staying elevated for hours afterward.",
        "b": "I have a Sunday morning blood pressure check where I need a calm, rested baseline reading.",
        "proposal": "A studio invites me to an extended Saturday evening hot yoga workshop.",
        "query": "Based only on these records, should the extended Saturday hot yoga workshop be flagged as a fit risk for this user?",
        "c": "The extended Saturday hot yoga workshop should be flagged as a fit risk because elevated heart rate and dehydration would distort Sunday's resting blood pressure baseline.",
        "broken": "I have a Sunday reminder to schedule a dentist cleaning online; it needs no physiological baseline.",
    },
    {
        "slug": "red_eye_before_therapy",
        "a": "Red-eye travel leaves me exhausted and emotionally flat for a full day afterward.",
        "b": "I have a Sunday morning therapy session where I need to be emotionally present to do meaningful work.",
        "proposal": "A friend invites me to a spontaneous Saturday night red-eye trip to visit them.",
        "query": "Based only on these records, should the spontaneous Saturday red-eye trip be flagged as a fit risk for this user?",
        "c": "The spontaneous Saturday red-eye trip should be flagged as a fit risk because post-flight exhaustion would blunt the emotional presence Sunday's therapy session needs.",
        "broken": "I have a Sunday reminder to renew a parking permit online; it needs no emotional presence.",
    },
    {
        "slug": "spicy_dinner_before_endoscopy_prep",
        "a": "A spicy late dinner triggers heartburn that disrupts my sleep and leaves my stomach unsettled into the next day.",
        "b": "I have a Sunday morning procedure that requires following a strict clear-liquid prep the night before without deviation.",
        "proposal": "Friends invite me to a Saturday night spicy hot-pot dinner.",
        "query": "Based only on these records, should the Saturday night spicy hot-pot dinner be flagged as a fit risk for this user?",
        "c": "The Saturday night spicy hot-pot dinner should be flagged as a fit risk because heartburn and stomach upset would conflict with the strict prep Sunday's procedure requires.",
        "broken": "I have a Sunday reminder to update an insurance form online; it requires no dietary prep.",
    },
    {
        "slug": "cold_exposure_before_physical_therapy",
        "a": "Long cold-weather exposure leaves my joints stiff and slower to warm up the next day.",
        "b": "I have a Sunday morning physical therapy session where I need full joint mobility to perform the exercises correctly.",
        "proposal": "A friend invites me to a long Saturday evening outdoor ice-skating outing.",
        "query": "Based only on these records, should the long Saturday outdoor ice-skating outing be flagged as a fit risk for this user?",
        "c": "The long Saturday outdoor ice-skating outing should be flagged as a fit risk because next-day joint stiffness would limit the mobility Sunday's physical therapy session needs.",
        "broken": "I have a Sunday reminder to review a health-insurance statement online; it needs no joint mobility.",
    },
    {
        "slug": "adrenaline_shift_before_sleep_study",
        "a": "A long, high-adrenaline volunteer shift leaves me too wired to fall asleep at my normal time that night.",
        "b": "I have a Sunday overnight sleep study where I need to fall asleep close to my normal bedtime for the reading to be valid.",
        "proposal": "A shelter asks me to cover an extra-long, high-intensity Saturday evening volunteer shift.",
        "query": "Based only on these records, should the extra-long Saturday volunteer shift be flagged as a fit risk for this user?",
        "c": "The extra-long Saturday volunteer shift should be flagged as a fit risk because being too wired to sleep would invalidate Sunday's sleep-study timing.",
        "broken": "I have a Sunday reminder to file a receipt for reimbursement online; it needs no particular bedtime.",
    },
    {
        "slug": "strenuous_hike_before_physical_exam",
        "a": "A long, strenuous hike leaves my legs sore and my resting heart rate elevated well into the next day.",
        "b": "I have a Sunday morning physical exam where the doctor needs an accurate resting heart rate and normal gait.",
        "proposal": "A hiking group invites me to a long, strenuous Saturday trail push.",
        "query": "Based only on these records, should the long, strenuous Saturday trail push be flagged as a fit risk for this user?",
        "c": "The long, strenuous Saturday trail push should be flagged as a fit risk because next-day soreness and elevated heart rate would distort Sunday's physical exam readings.",
        "broken": "I have a Sunday reminder to schedule an annual eye exam online; it needs no resting heart rate or gait.",
    },
)

PERSONAS = (
    "tracks symptoms in a daily notes app",
    "prefers early bedtimes on weeknights",
    "keeps a paper medication log",
    "does a short stretch routine most mornings",
    "prepares meals ahead on Sundays",
    "checks in with a care coordinator monthly",
    "takes a short walk after most meals",
    "reviews upcoming appointments every Friday",
    "keeps a refill reminder on the fridge",
    "avoids scheduling two demanding things back to back",
)

# 20 distinct filler topics so no single item ever needs to repeat one across
# its ~17 background sessions, and different items can still land on
# different topics at the same session position.
BACKGROUND_TOPICS = (
    ("I updated my appointment calendar before the week began.", "Keeping a visible plan helps you notice conflicts early."),
    ("I sent a short check-in message to my care coordinator.", "A brief check-in can still be useful."),
    ("I took a quiet walk after dinner.", "A small reset can make an evening feel less crowded."),
    ("I sorted a few old prescription bottles for recycling.", "Clearing clutter can make the medicine cabinet easier to use."),
    ("I made tea before reading for a while.", "You made room for a calm transition."),
    ("I wrote down a reminder for next week's refill.", "External reminders protect follow-through."),
    ("I had a small lunch between errands.", "Smaller meals can leave room for the rest of the day."),
    ("I logged a routine symptom note before bed.", "Closing small loops can make tomorrow easier."),
    ("I chose a quiet route home instead of the busy one.", "You protected a little decompression time."),
    ("I checked my weekend appointment list once more.", "Seeing the plan makes trade-offs easier to notice."),
    ("I put a refill reminder note by the door.", "You prepared for a simple errand."),
    ("I watered the plants before breakfast.", "A small routine can anchor the morning."),
    ("I organized a drawer of old paperwork that had been bothering me.", "A contained task gave you a reset."),
    ("I listened to a short podcast while cooking.", "You kept the evening low-pressure."),
    ("I replied to a scheduling request with a clear boundary.", "Clear expectations reduce friction."),
    ("I made a note to call a relative next month.", "You planned the connection without rushing it."),
    ("I booked a routine follow-up appointment.", "You handled a practical detail early."),
    ("I tidied the kitchen after a quiet dinner.", "A contained task can be restorative."),
    ("I set out clothes for an early errand the next day.", "A little prep can smooth out the morning."),
    ("I reviewed a grocery list for the week.", "Planning ahead can reduce small decisions later."),
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


def _background_text(pair_number: int, persona: str, session_id: int) -> tuple[str, str]:
    # session_id in {1..19} minus {5,12}; distinct mod 20, offset per pair so
    # different items don't line up on the same topic at the same position.
    index = (session_id + pair_number * 7) % len(BACKGROUND_TOPICS)
    text, reply = BACKGROUND_TOPICS[index]
    return f"As someone who {persona}, {text[0].lower() + text[1:]}", reply


def _annotations(context: list[dict[str, Any]], user_id: str, a_text: str, b_text: str) -> dict[str, Any]:
    annotations: dict[str, Any] = {}
    for session in context:
        sid = str(session["session_id"])
        annotations[sid] = {"role": "background_memory", "summary": "Non-target health memory."}
    annotations["5"] = {
        "role": "ev_A",
        "event_elements": {
            "person": user_id,
            "context": "A demanding health-related exposure",
            "goal_or_prediction": "Remain functional the following day",
            "action": a_text,
            "outcome_or_affect": "Needs recovery before a demanding health responsibility",
        },
    }
    annotations["12"] = {
        "role": "ev_B",
        "event_elements": {
            "person": user_id,
            "context": "A scheduled next-day health responsibility",
            "goal_or_prediction": "Show up ready for a health appointment or procedure",
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
                "connect the health-exposure recovery pattern with the scheduled next-day responsibility",
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
    scenario = HEALTH_SCENARIOS[pair_number - 1]
    persona = PERSONAS[pair_number - 1]
    user_id = f"anon_health_user_{pair_number:02d}"
    pair_id = f"AMB_HV_{scenario['slug']}_{pair_number:03d}"
    start = datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc)
    context = []
    for session_id in range(1, 21):
        timestamp = start + timedelta(days=session_id * 3)
        text, reply = _background_text(pair_number, persona, session_id)
        context.append(_session(session_id, timestamp, user_id, text, reply))
    context[4] = _session(5, start + timedelta(days=15), user_id, scenario["a"], "That sounds like a repeatable recovery pattern.")
    context[11] = _session(12, start + timedelta(days=36), user_id, scenario["b"], "That responsibility has a specific health-related demand.")
    context[19] = _session(20, start + timedelta(days=60), user_id, scenario["proposal"], "It is worth checking the fit against the commitments you already described.")
    annotations = _annotations(context, user_id, scenario["a"], scenario["b"])
    core_gold = _core_gold(scenario)
    candidate = {
        "schema_version": "assomem-vnext-1.2",
        "candidate_id": f"{pair_id}_{source_arm}",
        "pair_id": pair_id,
        "domain": "health",
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
            "relation": "A health-exposure recovery pattern creates a fit risk only when paired with B's specific next-day health responsibility.",
            "requires_evidence": ["ev_A", "ev_B"],
            "excludes": ["all evening activities are unsuitable", "all next-day plans are incompatible"],
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
            "nearby_relation": scenario.get(
                "nearby_relation",
                "The user can generally tolerate a single late evening without any next-day appointment.",
            ),
            "why_it_does_not_license_C": "That fact does not by itself establish a recovery-to-responsibility conflict.",
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
                {"role": "assistant", "content": "That Sunday activity is low stakes and can be moved without affecting your care."},
            ],
            "connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed health responsibility.",
            "rationale": "A plus B-prime no longer supports the original C.",
        },
        "provenance": {
            "authoring_method": "directly authored health vNext pilot",
            "created_at": "2026-07-25",
            "anonymous_submission": True,
            "source_person_name": None,
            "source_corpus": None,
            "gate_0_review_path": "../review/gate_0.csv",
            "gate_0_review_unit": "health_v1_relational",
            "release_eligible": False,
            "materialized_from": pair_id,
            "source_data_arm": source_arm,
        },
        "data_arm": source_arm,
        "available_evaluation_conditions": ["full", "a_only", "b_only", "link_broken"],
    }
    if source_arm == "associative":
        candidate["arm_gold"] = core_gold
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
                "A friend says the invitation would be great for catching up with people I haven't seen in a while.",
                "That is a tempting social upside, but it does not establish the user's recovery pattern.",
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
        candidate["context"][4] = _session(5, start + timedelta(days=15), user_id, "I reorganized a shelf of vitamins after dinner.", "A quiet household task was straightforward.")
        candidate["context"][11] = _session(12, start + timedelta(days=36), user_id, "I scheduled a routine grocery pickup.", "The errand can be completed at a flexible time.")
        candidate["episode_annotations"]["5"] = {"role": "background_memory", "summary": "Neutral replacement for removed evidence."}
        candidate["episode_annotations"]["12"] = {"role": "background_memory", "summary": "Neutral replacement for removed evidence."}
    return candidate


def build_health_pilot(destination: Path, count: int = len(HEALTH_SCENARIOS)) -> dict[str, int]:
    if count < 1 or count > len(HEALTH_SCENARIOS):
        raise ValueError(
            f"count must be between 1 and {len(HEALTH_SCENARIOS)} (one authored scenario per pair; "
            "no cycling, to avoid the cross-item duplication seen in the social pilot)"
        )
    for source_arm in ("associative", "distractor", "absence"):
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
    parser.add_argument("--count", type=int, default=len(HEALTH_SCENARIOS))
    args = parser.parse_args()
    print(json.dumps(build_health_pilot(args.destination, args.count), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

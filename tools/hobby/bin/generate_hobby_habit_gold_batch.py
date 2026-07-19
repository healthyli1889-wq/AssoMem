#!/usr/bin/env python3
"""Generate hobby/habit gold batches (S1–S20).

Writes to src/data/{domain}/{arm}/AMB_*_u{NN}_{arm}_S{N}.json
Scenario batches are generated separately; neither overwrites the other by default.
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

PILOT_ROOT = Path(__file__).resolve().parents[3]
DOMAIN = Path(__file__).resolve().parents[1]
SHARED_BIN = PILOT_ROOT / "tools" / "shared"
sys.path.insert(0, str(SHARED_BIN))

from gold_lib import (  # noqa: E402
    GENERATED_AT,
    build_item,
    hard_gate_errors,
    model_input,
    output_path,
    score_item,
    session,
)

PERSONAS_PATH = DOMAIN / "personas" / "personas_hobby_habit.json"
COMPUTED_BY = "tools/hobby/bin/generate_hobby_habit_gold_batch.py"

HH_BATCH_CONFIG: dict[str, Any] = {
    "id_prefix": "HH",
    "pilot_domain": "hobby_habit",
    "domain_tags": ["hobby/leisure", "daily_habits"],
    "data_subdir": "hobby",
    "folder_prefix": "hobby",
    "batch_id": "HH_GOLD_S6_S10_2026-07-15_v2",
    "generator_name": "hobby_habit_gold_batch_v2",
    "reproduce_generator": "python3 tools/hobby/bin/generate_hobby_habit_gold_batch.py",
}

USER10_PERSONA: dict[str, Any] = {
    "user_index": 10,
    "user_id": "hh_u10",
    "folder_tag": "user10",
    "display_name": "desktop-Healthy_Li",
    "source_corpus": "desktop_user",
    "source_ref": "local:Healthy Li; migrated from pilot HH",
    "stable_traits": [
        "psychology + AI research student",
        "University of Michigan exchange",
        "King's College London BSc Psychology",
        "mundane hobby routines (running, film, cooking, clay, games)",
        "values low-drama sustainable habits",
    ],
    "voice": "curious, reflective, student-researcher",
}

# Shared cumulative hobby timeline (sessions 1–111): S1–S5, S6–S10, S11–S15, S16–S20
CANONICAL_TIMELINE = [
    # S1
    session(1, "2026-01-11T18:00:00Z", "Watered the balcony herbs. Basil is finally upright.", "Small wins count."),
    session(2, "2026-01-12T18:00:00Z", "Resoled my walking shoes. Feels less slapdash.", "Good maintenance habit."),
    session(
        3,
        "2026-01-18T18:00:00Z",
        "Weekday mornings I stick to a flat park loop. When I cut through steeper neighborhood streets, my right knee starts complaining.",
        "Flat comfort plus steeper-street discomfort points to incline load as the trigger.",
        "Yeah. Soft paths are fine; the hills are not.",
    ),
    session(4, "2026-01-26T18:00:00Z", "A quiet evening with a podcast. No drama.", "Low-key recovery counts."),
    session(
        5,
        "2026-02-03T18:00:00Z",
        "Clinic visit this week: keep elevation gentle for the next couple of months while things settle.",
        "Clear constraint. Gentle elevation for a couple of months while you keep moving on softer surfaces.",
        "I am treating that as non-negotiable.",
    ),
    session(6, "2026-02-10T18:00:00Z", "Coworker group chat is hyping a ridge trail team signup this month — everyone saying it is amazing.", "Signup FOMO around trail events is loud."),
    session(7, "2026-02-17T18:00:00Z", "Someone asked if joining the ridge trail team is worth it for networking.", "Networking and elevation load are different questions."),
    session(8, "2026-02-24T18:00:00Z", "Sky was grey. Stayed in with a book.", "Quiet evening material."),
    session(9, "2026-03-02T18:00:00Z", "Neighbor mentioned a spring craft fair. I saved the flyer without committing.", "Fairs are tempting calendar items."),
    # S2
    session(10, "2026-03-09T18:00:00Z", "Sorted old negatives into sleeves. Dusty but satisfying.", "Archive days feel good."),
    session(
        11,
        "2026-03-16T18:00:00Z",
        "I am developing rolls at home. Hobby spending is frozen until April, so no new equipment before then.",
        "A freeze until April is a hard budget boundary. Use what you already own.",
        "Exactly. No impulse gear until then.",
    ),
    session(12, "2026-03-23T18:00:00Z", "Tried a new tea while editing. Too floral.", "Back to the usual blend?"),
    session(
        13,
        "2026-03-30T18:00:00Z",
        "Weekday evenings I am indoors. My only outdoor shooting window is Saturday and Sunday mornings before winter light dies.",
        "Weekend mornings are your scarce outdoor resource.",
        "Midweek daylight is basically gone for me.",
    ),
    session(14, "2026-04-06T18:00:00Z", "Filed receipts from a small gear purchase.", "Budget hygiene helps."),
    session(15, "2026-04-13T18:00:00Z", "Someone floated a midweek shore outing with a borrowed premium body — friend said similar trips are amazing.", "Daylight plus gear FOMO often travel together."),
    session(16, "2026-04-20T18:00:00Z", "Group chat keeps asking whether that upgrade-style shore trip is worth it right now.", "Worth-it talk can drown out calendar and budget facts."),
    # S3
    session(17, "2026-04-27T18:00:00Z", "Wiped down the spice rack. Oddly calming.", "Kitchen resets help."),
    session(
        18,
        "2026-05-04T18:00:00Z",
        "My weekly meal-prep block is how I eat all week. Skip it and I am buying takeout by midweek.",
        "That block is load-bearing. Protect it from optional social cooking plans.",
        "It is not optional for me.",
    ),
    session(19, "2026-05-11T18:00:00Z", "Put a reminder to buy rice. Staples again.", "Boring and useful."),
    session(
        20,
        "2026-05-18T18:00:00Z",
        "For the next several weeks I will be on trains visiting family on my usual kitchen afternoon, so I will not be home.",
        "Anything that assumes you are home those afternoons needs another plan.",
        "Travel already ate that slot.",
    ),
    session(21, "2026-05-25T18:00:00Z", "Short flat ride after work. Easy on the body.", "Gentle movement days matter."),
    session(22, "2026-06-01T18:00:00Z", "Neighbor wants me to host a recurring Sunday supper for our building — friend said it would be amazing.", "Standing hosting invites are sticky."),
    session(23, "2026-06-08T18:00:00Z", "Building chat is full of Sunday supper hosting FOMO. Everyone asking who will say yes.", "Social pressure around hosting can outrun capacity."),
    session(24, "2026-06-15T18:00:00Z", "Printed the kitchen calendar. Afternoon blocks are marked in red.", "Paper copies help on busy weeks."),
    # S4
    session(
        25,
        "2026-06-22T18:00:00Z",
        "My weekday clay sessions on the wheel often run past eleven. I get home wired and it takes a while to settle.",
        "Nights that run past eleven can push bedtime later even when the making itself is enjoyable.",
        "The making is fun; the clock is not.",
    ),
    session(26, "2026-06-29T18:00:00Z", "Folded laundry while a podcast played.", "Parallel chores work."),
    session(
        27,
        "2026-07-02T18:00:00Z",
        "A few times a week I help shape loaves before sunrise at a friend's shop. I need solid sleep the night before or I am useless at the oven.",
        "Pre-dawn oven shifts make the prior night non-negotiable.",
        "Staying up late beforehand taxes that hard.",
    ),
    session(28, "2026-07-04T18:00:00Z", "The studio opened another late evening class signup — friends saying it is amazing.", "Extra late slots look fun until they collide with dawn shifts."),
    # S5
    session(
        29,
        "2026-07-06T18:00:00Z",
        "I like hosting small tabletop nights at home every couple of weeks. It is my main social hobby.",
        "Home hosting is a real social outlet. Keep the format compatible with whoever shares the space.",
        "Quiet games work well for me.",
    ),
    session(30, "2026-07-08T18:00:00Z", "Game cafe posted a Tuesday board-game night signup. Public venue again.", "Outings and apartment rules are different."),
    session(
        31,
        "2026-07-10T18:00:00Z",
        "My roommate is sensitive to noise after dinner and asked me to keep apartment evenings calmer, especially with groups.",
        "That is a hard household constraint. High-volume group nights at home will create conflict.",
        "I do not want to blow up the household over one night.",
    ),
    session(32, "2026-07-12T18:00:00Z", "Friends want me to host a loud party-game night signup at my place — they said it would be amazing.", "Hosting FOMO can outrun roommate constraints."),
    # S6 evidence block
    session(33, "2026-06-04T17:55:00Z", "Recovery days are finally visible on the hobby calendar again.", "Tradeoffs are easier to see."),
    session(
        34,
        "2026-06-07T20:30:00Z",
        "Long erg pulls on the indoor rower leave my wrist tendons cranky the next day. Casual flat cycling has been fine.",
        "Has the sustained grip load repeated?",
        "Twice this month. Short easy rides do not do it — it is the long erg grip.",
    ),
    session(35, "2026-06-09T13:20:00Z", "Walked back from the gym district. Nice reset.", "Small movement breaks add up."),
    session(
        36,
        "2026-06-11T07:10:00Z",
        "Physio this week: avoid repetitive wrist loading for about six weeks while things settle.",
        "Is that non-negotiable for now?",
        "Yes. I am treating it as a hard hobby boundary.",
    ),
    session(37, "2026-06-13T16:40:00Z", "Office chat is hyping an erg crew challenge this month — lots of signup pressure.", "Crew FOMO is loud."),
    session(38, "2026-06-14T18:05:00Z", "Someone asked whether joining any erg crew is worth it for networking.", "Networking and wrist load are different questions."),
    # S7
    session(39, "2026-06-16T19:15:00Z", "Rinsed drum practice pads again. Less smear on the table.", "Maintenance keeps the hobby pleasant."),
    session(
        40,
        "2026-06-18T21:50:00Z",
        "Hand-drum practice after dinner is my main evening hobby at home. I look forward to it most weekdays.",
        "Does it usually stay contained?",
        "Yes, but it is still an evening sound in the apartment.",
    ),
    session(41, "2026-06-20T12:05:00Z", "Short walk after lunch. Cleared the afternoon fog.", "Worth repeating."),
    session(
        42,
        "2026-06-22T08:35:00Z",
        "Building quiet hours start at eight in the evening. A prior noise note from management is still on file.",
        "Is that a hard household boundary?",
        "Yes. Group evenings after eight need another venue.",
    ),
    session(43, "2026-06-24T17:30:00Z", "Building social committee posted a late-evening noise event idea. I archived it.", "Hosting ideas need a capacity check."),
    session(44, "2026-06-25T14:20:00Z", "Someone asked whether any late-evening apartment gathering is a good idea before quiet hours.", "Worth-it talk often ignores building rules."),
    # S8
    session(
        45,
        "2026-06-27T09:00:00Z",
        "Saturday morning balcony plant care is non-negotiable in summer. If I skip it, the collection wilts by Monday.",
        "Is that timing fixed?",
        "Yes. It is a short but immovable block.",
    ),
    session(46, "2026-06-29T11:40:00Z", "Checked the watering schedule on the balcony pots.", "Summer plant care does not pause."),
    session(
        47,
        "2026-07-01T15:55:00Z",
        "Saturday morning is also my only reliable long local hike window for a mental reset. I protect it when I can.",
        "Has that been consistent?",
        "Yes. Midweek hikes do not substitute for me.",
    ),
    session(48, "2026-07-03T10:10:00Z", "Neighbor posted a long Saturday plant-market invite — lots of building hype.", "All-day Saturday invites are sticky."),
    session(49, "2026-07-04T13:45:00Z", "Building chat is full of Saturday market FOMO. Everyone asking who will host a table.", "Social pressure around Saturday blocks is loud."),
    # S9
    session(
        50,
        "2026-07-06T22:15:00Z",
        "A full-reel chemical bath in the spare nook leaves overnight fumes when I process thirty-six exposures.",
        "Does a shorter run behave differently?",
        "Full-reel runs are what linger. Short tests air out faster.",
    ),
    session(51, "2026-07-08T07:45:00Z", "Guest-room linens are washed. The spare nook still holds trays for now.", "Room use and hobbies overlap."),
    session(
        52,
        "2026-07-10T16:20:00Z",
        "Overnight guests arrive Sunday after lunch. The spare nook must be cleared and ventilated before then.",
        "Is that deadline firm?",
        "Yes. It is already on the calendar.",
    ),
    session(53, "2026-07-11T08:00:00Z", "Forum crowd insists long wet-bench runs Saturday night before guest weekends are normal apartment practice. I disagree.", "Online norms are not apartment facts."),
    session(54, "2026-07-12T19:30:00Z", "Someone forwarded hype about pushing a Saturday-night chemical marathon before hosting overnight guests. Not adopting that.", "Social pressure is not a schedule."),
    # S10
    session(
        55,
        "2026-07-14T18:10:00Z",
        "Dawn bike rides on two fixed weekdays need solid prior-night sleep and a tuned bike. I have slipped on both after late nights.",
        "Has that pattern repeated?",
        "Yes. Those commute mornings are unforgiving.",
    ),
    session(56, "2026-07-16T12:30:00Z", "Lubed the chain and checked tire pressure for commute week.", "Small bike prep prevents bigger hassles."),
    session(
        57,
        "2026-07-18T09:40:00Z",
        "Midweek downtown cards have run past one before. The next dawn ride was rough enough that I remember it clearly.",
        "Was that a one-off?",
        "No. Late midweek cards and the following dawn ride do not mix for me.",
    ),
    session(58, "2026-07-19T17:05:00Z", "Group chat keeps pushing a midweek cards signup. I am ignoring the hype for now.", "Late-game invites need a sleep check."),
    session(59, "2026-07-20T07:20:00Z", "Dawn ride is on the calendar two days after that late-week signup.", "Sleep math matters for bike mornings."),
    # S11 evidence block
    session(60, "2026-07-22T18:00:00Z", "Race-prep weeks are finally back on the hobby calendar.", "Tradeoffs are easier to see."),
    session(
        61,
        "2026-07-24T20:30:00Z",
        "Shared-studio raku firings on Saturdays leave me lightheaded the next morning — glaze-only days at home have been fine.",
        "Has that pattern repeated?",
        "Twice this month. It is the Saturday kiln load, not pottery in general.",
    ),
    session(62, "2026-07-26T13:20:00Z", "Walked back from the studio district. Nice reset.", "Small movement breaks add up."),
    session(
        63,
        "2026-07-28T07:10:00Z",
        "Sunday long-run training is non-negotiable during race prep. I protect that block even when social plans stack up.",
        "Is that timing firm?",
        "Yes. I am treating it as a hard hobby boundary.",
    ),
    session(64, "2026-07-30T16:40:00Z", "Studio newsletter landed. I only skimmed the open-hours section.", "Not every mailer needs a decision."),
    session(65, "2026-07-31T18:05:00Z", "Logged an easy shakeout jog after physio notes. Keeping Sunday legs fresh.", "Recovery notes are worth tracking."),
    # S12
    session(66, "2026-08-02T19:15:00Z", "Restocked meal-prep containers. Sunday rhythm still matters.", "Kitchen routines are not one-size."),
    session(
        67,
        "2026-08-04T21:50:00Z",
        "Saturday-night tabletop campaigns that run past midnight wreck my Sunday batch-cook rhythm — shorter games are fine.",
        "Has the late-night pattern repeated?",
        "Yes. Three marathon sessions did it; two-hour games did not.",
    ),
    session(68, "2026-08-06T12:30:00Z", "Short lunch away from the table. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        69,
        "2026-08-08T08:45:00Z",
        "Sunday afternoon batch-cook is fixed meal-prep for the work week and does not move easily.",
        "Is that slot movable?",
        "Not easily. The week depends on it.",
    ),
    session(70, "2026-08-10T14:10:00Z", "Game group chat is noisy about weekend campaigns. I muted the thread.", "Mute buttons save attention."),
    session(71, "2026-08-11T17:20:00Z", "Printed the August social calendar. Sunday kitchen blocks are locked.", "Paper copies help on busy weeks."),
    # S13
    session(
        72,
        "2026-08-13T10:05:00Z",
        "High-caffeine cupping tastings after two in the afternoon wreck my evening piano practice focus — morning tastings have been fine.",
        "Has the afternoon cupping pattern repeated?",
        "Yes. Three afternoon flights did it; morning flights did not.",
    ),
    session(73, "2026-08-14T15:40:00Z", "Metronome is set for this week's recital piece. Evening slots are scarce.", "Recital prep has a timeline."),
    session(
        74,
        "2026-08-16T19:30:00Z",
        "Piano recital piece needs calm evening practice this week — rushed evenings show up immediately in tempo control.",
        "Is that deadline firm?",
        "Yes. The piece is already on the calendar.",
    ),
    session(75, "2026-08-17T11:15:00Z", "Cafe posted a cupping-flight invite for the weekend. I filed it without replying.", "Invites can wait for a practice plan."),
    session(76, "2026-08-18T16:50:00Z", "Marked evening practice blocks on the recital checklist. Focus windows are the priority.", "Recital logistics are the priority."),
    # S14
    session(
        77,
        "2026-08-20T22:15:00Z",
        "Track tempo intervals aggravate shin splints for days — easy flat runs have been fine.",
        "Was that a one-off?",
        "No. Twice on track tempo; easy runs did not flare it.",
    ),
    session(78, "2026-08-22T07:45:00Z", "Running shoes are rotated. Thursday long-run is on the calendar.", "Long-run weeks need protected legs."),
    session(
        79,
        "2026-08-24T16:20:00Z",
        "Thursday long-run is on the training calendar this month and needs protected legs.",
        "Is that slot firm?",
        "Yes. It is already booked.",
    ),
    session(80, "2026-08-25T08:00:00Z", "Running-group forum is loud about pre-session rituals. I am not adopting forum norms.", "Forum norms are not injury facts."),
    session(81, "2026-08-26T19:30:00Z", "Packed electrolytes and a light snack for the long run. Legs still feel tight.", "Recovery timing matters on hard weeks."),
    # S15
    session(
        82,
        "2026-08-28T18:10:00Z",
        "Indoor resin pours without balcony venting overheat the apartment and stress the herb collection on the rail.",
        "Has that pattern repeated?",
        "Yes. Two enclosed pours did it; vented balcony pours did not.",
    ),
    session(83, "2026-08-30T12:30:00Z", "Heat-wave week is on the forecast. Daily balcony shade checks are on the list.", "Herb care context matters in heat."),
    session(
        84,
        "2026-09-01T09:40:00Z",
        "Heat-wave week requires daily balcony shade and watering for the herb collection.",
        "Is that timing firm?",
        "Yes. It is already on the calendar.",
    ),
    session(85, "2026-09-02T17:05:00Z", "Maker chat sent another indoor pour invite. I filed it without replying.", "Invites can wait for a ventilation plan."),
    session(86, "2026-09-03T07:20:00Z", "Set out the balcony shade checklist for heat-wave week. Herbs need daily checks.", "Heat weeks need a clean routine."),
    # S16
    session(87, "2026-09-05T18:00:00Z", "Autumn sketch calendar is printed. Solo pencil blocks are marked.", "Paper copies help on busy weeks."),
    session(
        88,
        "2026-09-07T20:45:00Z",
        "Open-window street noise wrecks my focused pencil sketching — closed-window sessions are fine.",
        "Has that pattern repeated?",
        "Yes. Twice on open-window evenings; closed-window sessions did not.",
    ),
    session(89, "2026-09-08T13:10:00Z", "Short walk to the art-supply district. Nice reset.", "Small movement breaks add up."),
    session(
        90,
        "2026-09-10T08:30:00Z",
        "Illustration sprint week needs protected morning solo sketch blocks Tuesday through Thursday — already on the calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(91, "2026-09-11T16:55:00Z", "Studio posted an open-air drawing circle blurb. I filed it without replying.", "Invites can wait for a sprint plan."),
    # S17
    session(92, "2026-09-13T19:20:00Z", "Restocked kiln shelves for the firing-prep sprint. Solo evenings still matter.", "Studio routines are not one-size."),
    session(
        93,
        "2026-09-15T21:10:00Z",
        "Full-day craft-fair volunteering leaves me too drained for studio work — short booth shifts are fine.",
        "Has the full-day volunteering pattern repeated?",
        "Yes. Three fair days did it; short booth shifts did not.",
    ),
    session(94, "2026-09-16T12:40:00Z", "Short lunch away from the booth. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        95,
        "2026-09-18T08:50:00Z",
        "Studio packet due Friday needs three solo evening studio blocks — already on the calendar.",
        "Is that slot movable?",
        "Not easily. The firing depends on it.",
    ),
    session(96, "2026-09-19T14:25:00Z", "Maker chat is noisy about market immersion weeks. I muted the thread.", "Mute buttons save attention."),
    # S18
    session(97, "2026-09-21T10:05:00Z", "Printed the autumn movement calendar. Solo prep blocks are marked.", "Prep weeks need a clean routine."),
    session(
        98,
        "2026-09-23T15:35:00Z",
        "Evening wine tastings wreck my next-morning yoga balance — afternoon tastings have been fine.",
        "Has the evening tasting pattern repeated?",
        "Yes. Three evening flights did it; afternoon flights did not.",
    ),
    session(99, "2026-09-24T11:20:00Z", "Cellar mailer landed. I filed it without replying.", "Invites can wait for a prep plan."),
    session(
        100,
        "2026-09-26T07:15:00Z",
        "Saturday flow intensive needs a sharp morning balance block — a late-slot social signup is already booked through the night before.",
        "Is that timing firm?",
        "Yes. The intensive is already scheduled.",
    ),
    session(101, "2026-09-27T16:50:00Z", "Packed reference notes for the flow lock. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S19
    session(102, "2026-09-29T18:15:00Z", "Corridor show outline is packed. Wednesday slot is on the calendar.", "Show weeks need protected prep blocks."),
    session(
        103,
        "2026-10-01T22:00:00Z",
        "I compose gallery layouts best on paper grid mockups — wall-only layout sessions produce weak results for me.",
        "Has the wall-only layout pattern repeated?",
        "Yes. Twice on wall-only prep; paper grid mockups did not.",
    ),
    session(104, "2026-10-02T08:00:00Z", "Gallery forum is loud about poster-board run-throughs. I am not adopting forum defaults.", "Forum norms are not prep facts."),
    session(
        105,
        "2026-10-04T16:30:00Z",
        "Prior wall-only gallery layout rehearsal went poorly before the corridor show — I lost the thread twice.",
        "Harsh memory. Was the material unfamiliar?",
        "No. The format fought my process.",
    ),
    session(106, "2026-10-05T19:40:00Z", "Printed the corridor show calendar. Solo grid-prep blocks are locked.", "Paper copies help on busy weeks."),
    # S20
    session(107, "2026-10-07T18:05:00Z", "Quiet-home stretch memo landed. I only skimmed the atmosphere section.", "Not every memo needs a decision."),
    session(
        108,
        "2026-10-09T07:50:00Z",
        "Long crowded transit legs to evening hobby venues drain my energy before home creative blocks — short bike trips are fine.",
        "Has the long crowded transit pattern repeated?",
        "Yes. Ninety-minute legs did it; short bike trips did not.",
    ),
    session(109, "2026-10-10T14:15:00Z", "Venue shuttle blurb posted. I filed it without replying.", "Invites can wait for a hosting plan."),
    session(
        110,
        "2026-10-12T09:25:00Z",
        "Quiet-home stretch requires calm atmosphere for restorative hobbies — already on the calendar.",
        "Is that timing firm?",
        "Yes. The hosting weekend is already booked.",
    ),
    session(111, "2026-10-13T17:30:00Z", "Packed a light bag for a possible evening outing. Corridor timing still feels heavy.", "Home stretches need an energy plan."),
]


def monotonic_timeline(timeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Re-stamp sessions so timestamps strictly increase with session_id."""
    from datetime import datetime, timedelta

    start = datetime(2026, 1, 5, 18, 0, 0)
    out: list[dict[str, Any]] = []
    for s in timeline:
        sid = s["session_id"]
        ts = start + timedelta(days=(sid - 1) * 2)
        out.append({**s, "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ")})
    return out


CANONICAL_TIMELINE = monotonic_timeline(CANONICAL_TIMELINE)


def persona_paint_config(persona: dict[str, Any]) -> dict[str, str]:
    idx = persona["user_index"]
    configs: dict[int, dict[str, str]] = {
        1: {"location": "Pittsburgh", "colleague_a": "Maya", "colleague_b": "Evan", "role_short": "consulting"},
        2: {"location": "Amsterdam", "colleague_a": "Sanne", "colleague_b": "Pieter", "role_short": "office"},
        3: {"location": "the city", "colleague_a": "Jules", "colleague_b": "Rina", "role_short": "maker"},
        4: {"location": "the suburbs", "colleague_a": "Nora", "colleague_b": "Ben", "role_short": "family"},
        5: {"location": "downtown", "colleague_a": "Luis", "colleague_b": "Carmen", "role_short": "busy-calendar"},
        6: {"location": "Berlin", "colleague_a": "Lena", "colleague_b": "Tobias", "role_short": "weekday"},
        7: {"location": "Austin", "colleague_a": "Chris", "colleague_b": "Sam", "role_short": "social"},
        8: {"location": "the hospital district", "colleague_a": "Priya", "colleague_b": "James", "role_short": "clinical"},
        9: {"location": "office campus", "colleague_a": "Helga", "colleague_b": "Karl", "role_short": "office"},
        10: {"location": "Ann Arbor", "colleague_a": "Mia", "colleague_b": "Leo", "role_short": "campus"},
    }
    base = configs.get(idx, configs[3])
    trait = persona.get("stable_traits", ["hobby routine keeper"])[0]
    base["trait0"] = trait
    base["voice"] = persona.get("voice", "measured").split(",")[0]
    return base


def paint_session(s: dict[str, Any], paint: dict[str, str]) -> dict[str, Any]:
    sid = s["session_id"]
    dlg = deepcopy(s["dialogue"])
    if sid == 2 and paint["user_index"] != 1:
        dlg[0]["content"] = f"Hobby mode felt very '{paint['trait0']}' today — small routines, no drama."
    if sid == 21 and paint["location"] != "Pittsburgh":
        dlg[0]["content"] = dlg[0]["content"].replace("hiking group", f"{paint['location']} walking group")
    return {"session_id": sid, "timestamp": s["timestamp"], "dialogue": dlg}


def build_timeline(persona: dict[str, Any]) -> list[dict[str, Any]]:
    paint = {**persona_paint_config(persona), "user_index": persona["user_index"]}
    if persona["user_index"] == 1:
        return deepcopy(CANONICAL_TIMELINE)
    return [paint_session(s, paint) for s in CANONICAL_TIMELINE]


def build_scenarios(persona: dict[str, Any]) -> dict[str, Any]:
    paint = persona_paint_config(persona)
    ca, cb = paint["colleague_a"], paint["colleague_b"]
    return {
        "S1": {
            "name": "knee_incline_x_mountain_race",
            "prefix_end": 9,
            "evidence": {
                "ev_A": {
                    "session_id": 3,
                    "fact": "User jogs weekday mornings on flat park paths and feels knee discomfort on steeper neighborhood streets.",
                },
                "ev_B": {
                    "session_id": 5,
                    "fact": "Clinic advised keeping elevation gentle for a couple of months.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-03-09T17:30:00Z",
            "query": "Worth joining the ridge trail team signup this month — based on what you know about me?",
            "gold": (
                "Decline the ridge trail team signup. Steeper neighborhood streets have caused knee discomfort on your flat-park "
                "routine, and the clinic advised keeping elevation gentle for a couple of months. The flat charity walk chatter "
                "is unrelated social noise."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Steeper routes have bothered your knee, but "
                "I cannot tell from the available memory whether the clinic restricted elevation load. Confirm any clinical "
                "elevation guidance before joining a ridge trail team."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the clinic advised keeping elevation "
                    "gentle for a couple of months, but the available memory does not establish that steeper streets cause knee "
                    "discomfort for you. I cannot reject the signup from clinical guidance alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Steeper routes have bothered your knee, but "
                    "I cannot tell from the available memory whether the clinic restricted elevation load. Confirm any clinical "
                    "elevation guidance before joining a ridge trail team."
                ),
            },
            "required": [
                "uses knee discomfort on steeper routes",
                "uses gentle-elevation clinic guidance",
                "recommends declining the ridge trail team signup",
            ],
            "absence_required": [
                "states that the clinical elevation guidance is missing",
                "does not infer harm from the signup invite alone",
                "asks about elevation guidance or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the knee-incline evidence is missing",
                    "does not infer elevation harm from the team invite alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the clinical elevation guidance is missing",
                    "does not infer harm from the signup invite alone",
                    "asks about elevation guidance or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "incline_knee_flare", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "elevation_load", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "poor_fit_steep_event", "hop": 2},
            ],
            "forbidden": ["contraindicated_elevation_events", "incline_flare_prone", "knee ban forever", "must never hike"],
            "distractor": {
                "timestamp": "2026-02-20T11:00:00Z",
                "user": f"My coworker is hyping a flat charity walk team signup for their fundraising crew. They keep saying the walk is amazing and asking if joining is worth it for networking.",
                "assistant": "A flat charity walk is a different event format.",
                "why": "Flat charity walk FOMO shares signup surface but is not evidence about this user's incline knee pattern or clinical elevation limit.",
            },
            "evolving": {"event_readiness": "contraindicated_elevation_events", "knee_pattern": "incline_flare_prone"},
        },
        "S2": {
            "name": "budget_freeze_x_weekday_coastal_shoot",
            "prefix_end": 16,
            "evidence": {
                "ev_A": {
                    "session_id": 11,
                    "fact": "Hobby spending frozen until April; developing at home; no new equipment.",
                },
                "ev_B": {
                    "session_id": 13,
                    "fact": "Only outdoor shooting window is Saturday and Sunday mornings; weekday evenings indoors.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-04-10T17:05:00Z",
            "query": "Worth taking a midweek shore shoot with a borrowed premium body — based on what you know about me?",
            "gold": (
                "No. Hobby spending is frozen until April and your only outdoor shooting window is Saturday and Sunday mornings, "
                "so a midweek shore outing conflicts on budget and daylight. The gift-shop compact upgrade chatter is unrelated "
                "impulse talk."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. A spending freeze may apply, but I cannot tell "
                "from the available memory whether your outdoor shooting window is weekend mornings only. Confirm budget and "
                "daylight availability before advising on a midweek shore shoot."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your outdoor shooting window is "
                    "weekend mornings only, but the available memory does not establish a hobby spending freeze until April. "
                    "I cannot reject the outing from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. A spending freeze may apply, but I cannot tell "
                    "from the available memory whether your outdoor shooting window is weekend mornings only. Confirm budget and "
                    "daylight availability before advising on a midweek shore shoot."
                ),
            },
            "required": [
                "uses spending freeze until April",
                "uses weekend-morning outdoor shooting window",
                "recommends declining midweek shore shoot",
            ],
            "absence_required": [
                "states that the outdoor-window evidence is missing",
                "does not infer harm from the outing invite alone",
                "asks about daylight window or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the spending-freeze evidence is missing",
                    "does not infer budget harm from the outing alone",
                    "explicitly abstains from rejecting the shoot",
                ],
                "ev_B": [
                    "states that the outdoor-window evidence is missing",
                    "does not infer harm from the outing invite alone",
                    "asks about daylight window or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "gear_outlay", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "weekday_daylight", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "poor_fit_wednesday_coastal", "hop": 2},
            ],
            "forbidden": ["frozen_until_april", "weekend_mornings_only", "gear ban forever", "must skip all shoots"],
            "distractor": {
                "timestamp": "2026-04-07T09:30:00Z",
                "user": f"A friend said a midweek shore outing with a borrowed premium body is amazing and asked if that upgrade-style trip is worth it right now.",
                "assistant": "Shore-outing hype and calendar facts are different ledgers.",
                "why": "Midweek shore outing hype shares query surface but is not evidence about this user's spending freeze or weekend-only outdoor window.",
            },
            "evolving": {"gear_budget": "frozen_until_april", "daylight_window": "weekend_mornings_only"},
        },
        "S3": {
            "name": "batch_cook_x_standing_sunday_host",
            "prefix_end": 24,
            "evidence": {
                "ev_A": {
                    "session_id": 18,
                    "fact": "Sunday batch cooking feeds the user for the work week.",
                },
                "ev_B": {
                    "session_id": 20,
                    "fact": "Next several Sundays spent on trains visiting family; not home for kitchen block.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-12T18:45:00Z",
            "query": "Neighbor wants a recurring Sunday supper hosted here — worth saying yes?",
            "gold": (
                "Say no or negotiate a very short appearance. Your weekly meal-prep block is load-bearing and upcoming family "
                "travel already removes your kitchen afternoons, so a recurring Sunday supper is a poor fit. The restaurant "
                "prix-fixe signup talk is a different one-off decision."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a recurring Sunday supper fits. Meal-prep blocks matter to you, "
                "but I cannot tell from the available memory whether family travel will keep you away on kitchen afternoons. "
                "Confirm upcoming Sunday travel before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know family travel will remove your kitchen "
                    "afternoons for several weeks, but the available memory does not establish that your weekly meal-prep block is "
                    "load-bearing. I cannot reject hosting from travel alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a recurring Sunday supper fits. Meal-prep blocks matter to you, "
                    "but I cannot tell from the available memory whether family travel will keep you away on kitchen afternoons. "
                    "Confirm upcoming Sunday travel before committing."
                ),
            },
            "required": [
                "uses weekly meal-prep block as load-bearing",
                "uses family travel removing kitchen afternoons",
                "recommends declining recurring Sunday supper hosting",
            ],
            "absence_required": [
                "states that the family-travel kitchen evidence is missing",
                "does not infer hosting harm from the neighbor invite alone",
                "asks about Sunday travel or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the meal-prep block evidence is missing",
                    "does not infer capacity harm from the supper invite alone",
                    "explicitly abstains from rejecting hosting",
                ],
                "ev_B": [
                    "states that the family-travel kitchen evidence is missing",
                    "does not infer hosting harm from the neighbor invite alone",
                    "asks about Sunday travel or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "meal_prep_load_bearing", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "home_kitchen_afternoons", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "cannot_host_standing_dinner", "hop": 2},
            ],
            "forbidden": ["travel_disrupts_batch_cook", "poor_for_standing_dinners", "cooking ban forever", "must never host"],
            "distractor": {
                "timestamp": "2026-05-10T14:00:00Z",
                "user": f"A friend said a prix-fixe Sunday dinner signup at a restaurant across town is amazing and asked if it is worth grabbing a seat for one night.",
                "assistant": "A one-night restaurant signup is just a reservation decision.",
                "why": "Restaurant prix-fixe hype shares Sunday supper surface but is not evidence about this user's meal-prep block or family travel removing kitchen afternoons.",
            },
            "evolving": {"sunday_capacity": "travel_disrupts_batch_cook", "hosting_fit": "poor_for_standing_dinners"},
        },
        "S4": {
            "name": "late_clay_x_predawn_bakery",
            "prefix_end": 28,
            "evidence": {
                "ev_A": {
                    "session_id": 25,
                    "fact": "User's weekday wheel sessions at the studio often run past eleven and leave them wired.",
                },
                "ev_B": {
                    "session_id": 27,
                    "fact": "User helps shape loaves before sunrise at a friend's shop and needs solid sleep the night before.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-23T17:20:00Z",
            "query": "Worth adding the studio's extra late slot before this week's dawn prep block — sensible?",
            "gold": (
                "Do not add it. Weekday wheel sessions already run past eleven and leave you wired, and pre-dawn oven shifts need "
                "solid sleep the night before. An extra late block on oven-shift mornings conflicts. The weekend glaze workshop "
                "ticket is a different one-off decision."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an extra late block fits oven-shift mornings. Late studio nights "
                "have left you wired, but I cannot tell from the available memory whether pre-dawn oven shifts need solid prior-night "
                "sleep. Confirm oven-shift timing before adding the block."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know pre-dawn oven shifts need solid "
                    "prior-night sleep, but the available memory does not establish that weekday wheel sessions run past eleven and "
                    "leave you wired. I cannot reject the block from oven timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an extra late block fits oven-shift mornings. Late studio nights "
                    "have left you wired, but I cannot tell from the available memory whether pre-dawn oven shifts need solid prior-night "
                    "sleep. Confirm oven-shift timing before adding the block."
                ),
            },
            "required": [
                "uses late weekday wheel sessions leaving user wired",
                "uses pre-dawn oven shift sleep requirement",
                "recommends against extra late block on oven-shift mornings",
            ],
            "absence_required": [
                "states that the oven-shift sleep evidence is missing",
                "does not infer schedule harm from the studio invite alone",
                "asks about oven-shift timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late wheel-session evidence is missing",
                    "does not infer sleep harm from the block alone",
                    "explicitly abstains from rejecting the block",
                ],
                "ev_B": [
                    "states that the oven-shift sleep evidence is missing",
                    "does not infer schedule harm from the studio invite alone",
                    "asks about oven-shift timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_wired_nights", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "prior_night_sleep", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "extra_late_class_conflicts", "hop": 2},
            ],
            "forbidden": ["pottery_vs_dawn_bakery", "pre_dawn_shift_protected", "clay ban forever", "must skip all studio"],
            "distractor": {
                "timestamp": "2026-05-10T14:30:00Z",
                "user": f"A friend said the studio's extra late-slot signup before dawn prep week is amazing hype and asked if it is worth adding once.",
                "assistant": "One-off signup hype and your sleep ledger are different questions.",
                "why": "Late-slot signup hype shares query surface but is not evidence about this user's late wheel sessions or pre-dawn oven sleep need.",
            },
            "evolving": {"schedule_conflict": "pottery_vs_dawn_bakery", "sleep_priority": "pre_dawn_shift_protected"},
        },
        "S5": {
            "name": "home_games_x_roommate_quiet",
            "prefix_end": 32,
            "evidence": {
                "ev_A": {
                    "session_id": 29,
                    "fact": "User regularly hosts small board game nights at home.",
                },
                "ev_B": {
                    "session_id": 31,
                    "fact": "Roommate is noise-sensitive in the evenings and asks for quieter nights at the apartment.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-02T19:30:00Z",
            "query": "Friends want a loud party-game night at the apartment — worth hosting?",
            "gold": (
                "Host somewhere else or pick a quiet game. You like home tabletop nights, but your roommate needs quieter evenings, "
                "so a loud party-game night at the apartment is a poor fit. The cafe game-night ticket discussion is a different outing."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Home tabletop hosting is your social hobby, but "
                "I cannot tell from the available memory whether your roommate restricts evening noise. Confirm household noise "
                "rules before hosting a loud party-game night."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your roommate needs quieter apartment "
                    "evenings, but the available memory does not establish that you regularly host tabletop nights at home. "
                    "I cannot reject hosting from roommate rules alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Home tabletop hosting is your social hobby, but "
                    "I cannot tell from the available memory whether your roommate restricts evening noise. Confirm household noise "
                    "rules before hosting a loud party-game night."
                ),
            },
            "required": [
                "uses home board game hosting habit",
                "uses roommate evening noise sensitivity",
                "recommends against loud party-game night at apartment or relocating",
            ],
            "absence_required": [
                "states that the roommate noise evidence is missing",
                "does not infer household harm from the friends invite alone",
                "asks about apartment noise rules or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the home tabletop hosting evidence is missing",
                    "does not infer noise conflict from the party invite alone",
                    "explicitly abstains from rejecting hosting",
                ],
                "ev_B": [
                    "states that the roommate noise evidence is missing",
                    "does not infer household harm from the friends invite alone",
                    "asks about apartment noise rules or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "home_tabletop_habit", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "apartment_noise", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "loud_party_poor_fit", "hop": 2},
            ],
            "forbidden": ["roommate_quiet_constraint", "needs_quiet_or_elsewhere", "game ban forever", "must never host"],
            "distractor": {
                "timestamp": "2026-05-28T09:30:00Z",
                "user": f"A friend said a board-game cafe game night signup is amazing and asked if that public event is worth it.",
                "assistant": "A cafe game night is just an outing ticket.",
                "why": "Cafe game-night signup hype shares party-game surface but is not evidence about this user's home tabletop habit or roommate evening noise constraint.",
            },
            "evolving": {"home_noise_budget": "roommate_quiet_constraint", "game_night_fit": "needs_quiet_or_elsewhere"},
        },
        "S6": {
            "name": "erg_grip_x_rowing_team_signup",
            "prefix_end": 38,
            "evidence": {
                "ev_A": {
                    "session_id": 34,
                    "fact": "Long erg pulls on the indoor rower leave the user's wrist tendons cranky the next day; casual flat cycling has been fine.",
                },
                "ev_B": {
                    "session_id": 36,
                    "fact": "Physio advised avoiding repetitive wrist loading for about six weeks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-15T17:10:00Z",
            "query": "A coworker says the indoor rowing marathon team signup this month is amazing and wants me on the crew. Should I join — is it worth it?",
            "gold": (
                "Decline the rowing marathon team for now. Long erg pulls have left your wrist tendons cranky the next day, "
                "and physio advised avoiding repetitive wrist loading for about six weeks. The flat charity walk signup "
                "chatter is unrelated social noise."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Long erg pulls have bothered your wrists, "
                "but I cannot tell from the available memory whether repetitive wrist loading is currently restricted. "
                "Confirm any physio guidance before joining an erg marathon crew."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know physio advised avoiding repetitive "
                    "wrist loading for about six weeks, but the available memory does not establish that long erg pulls bother "
                    "your wrists. I cannot reject the crew signup from clinical guidance alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Long erg pulls have bothered your wrists, "
                    "but I cannot tell from the available memory whether repetitive wrist loading is currently restricted. "
                    "Confirm any physio guidance before joining an erg marathon crew."
                ),
            },
            "required": [
                "links long erg pulls to next-day wrist tendon discomfort",
                "links physio guidance to avoid repetitive wrist loading",
                "recommends declining the rowing marathon team signup",
            ],
            "absence_required": [
                "states that the wrist-loading restriction is missing",
                "does not infer harm from the signup invite alone",
                "explicitly abstains or asks about physio guidance",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the erg wrist-response evidence is missing",
                    "does not infer wrist harm from the team invite alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the wrist-loading restriction is missing",
                    "does not infer harm from the signup invite alone",
                    "explicitly abstains or asks about physio guidance",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "erg_wrist_flare", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "repetitive_wrist_load", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "rowing_team_poor_fit", "hop": 2},
            ],
            "forbidden": ["wrist ban forever", "must never row", "skip all exercise"],
            "distractor": {
                "timestamp": "2026-06-12T09:15:00Z",
                "user": f"{ca} said a flat charity walk team signup is amazing and that joining is worth it for networking.",
                "assistant": "That describes a different event format.",
                "why": "A flat charity walk team signup is query-similar FOMO but not evidence about this user's erg wrist pattern or physio wrist-loading limit.",
            },
            "evolving": {"wrist_pattern": "erg_grip_flare", "physio_limit": "no_repetitive_wrist_load_6wk"},
        },
        "S7": {
            "name": "home_drums_x_quiet_hours_circle",
            "prefix_end": 44,
            "evidence": {
                "ev_A": {
                    "session_id": 40,
                    "fact": "Hand-drum practice after dinner is the user's main evening hobby at home on most weekdays.",
                },
                "ev_B": {
                    "session_id": 42,
                    "fact": "Building quiet hours start at eight in the evening with a prior noise note on file.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-26T18:20:00Z",
            "query": "A nine o'clock percussion-circle signup at my apartment is getting hype. Should I host it?",
            "gold": (
                "Do not host the percussion circle at home. Hand-drum practice is your main evening hobby, but building quiet hours "
                "start at eight and a prior noise note is on file. Host at a public workshop venue or pick a quieter format. "
                "The public drum workshop ticket talk is a different outing."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a nine o'clock drum circle fits at home. Hand-drum practice "
                "is your main evening hobby, but I cannot tell from the available memory whether building quiet-hour rules "
                "would block it. Confirm quiet-hour timing before hosting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know building quiet hours start at eight, "
                    "but the available memory does not establish that hand-drum practice is your main evening hobby at home. "
                    "I cannot reject hosting from quiet-hour rules alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a nine o'clock drum circle fits at home. Hand-drum practice "
                    "is your main evening hobby, but I cannot tell from the available memory whether building quiet-hour rules "
                    "would block it. Confirm quiet-hour timing before hosting."
                ),
            },
            "required": [
                "uses hand-drum practice as a home evening hobby",
                "uses eight o'clock quiet-hour building rule",
                "recommends against hosting the drum circle at home",
            ],
            "absence_required": [
                "states that quiet-hour evidence is missing",
                "does not infer building conflict from the invite alone",
                "asks about quiet-hour timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the home drum-hobby evidence is missing",
                    "does not infer noise conflict from the invite alone",
                    "explicitly abstains from rejecting hosting",
                ],
                "ev_B": [
                    "states that quiet-hour evidence is missing",
                    "does not infer building conflict from the invite alone",
                    "asks about quiet-hour timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "home_evening_drums", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "apartment_quiet_after_8pm", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "drum_circle_conflicts_quiet_hours", "hop": 2},
            ],
            "forbidden": ["drums banned", "must cancel all music", "never host friends"],
            "distractor": {
                "timestamp": "2026-06-23T11:00:00Z",
                "user": f"{cb} said a public percussion-circle workshop signup at nine is amazing hype and worth it as a one-off ticket night out.",
                "assistant": "A public workshop is a different venue decision.",
                "why": "Public percussion-circle workshop signup shares hype surface but is not evidence about this user's home drum habit or apartment quiet-hour constraint.",
            },
            "evolving": {"evening_hobby": "home_hand_drums", "quiet_hours": "building_after_8pm"},
        },
        "S8": {
            "name": "balcony_plants_x_saturday_hike_window",
            "prefix_end": 49,
            "evidence": {
                "ev_A": {
                    "session_id": 45,
                    "fact": "Saturday morning balcony plant care is non-negotiable in summer; skipping it wilts the collection by Monday.",
                },
                "ev_B": {
                    "session_id": 47,
                    "fact": "Saturday morning is the user's only reliable long local hike window for a mental reset.",
                },
            },
            "withheld_in_absence": "ev_A",
            "query_timestamp": "2026-07-05T16:30:00Z",
            "query": "My neighbor wants me at an all-day Saturday plant fair for the building. Friend said it would be amazing. Should I say yes — is it worth it?",
            "gold": (
                "Say no or negotiate a very short appearance. Saturday morning balcony plant care is non-negotiable in summer, "
                "and that same morning is your only reliable long local hike reset window. The restaurant prix-fixe Saturday "
                "signup is a different one-night decision."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the all-day plant fair fits. Saturday morning is your only "
                "reliable long hike reset window, but I cannot tell from the available memory whether balcony plant care also "
                "requires that block. Confirm your plant-care timing before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence to decide whether the all-day plant fair fits. Saturday morning is your only "
                    "reliable long hike reset window, but I cannot tell from the available memory whether balcony plant care also "
                    "requires that block. Confirm your plant-care timing before committing."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. I know Saturday balcony plant care is "
                    "non-negotiable in summer, but the available memory does not establish that Saturday morning is your only "
                    "hike reset window. I cannot reject the fair from plant care alone."
                ),
            },
            "required": [
                "uses non-negotiable Saturday balcony plant care",
                "uses Saturday morning as the only reliable long hike window",
                "recommends declining or sharply limiting the all-day plant fair",
            ],
            "absence_required": [
                "states that the plant-care requirement is missing",
                "does not infer schedule conflict from the invite alone",
                "asks about plant-care timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the plant-care requirement is missing",
                    "does not infer schedule conflict from the invite alone",
                    "asks about plant-care timing or explicitly abstains",
                ],
                "ev_B": [
                    "states that the hike-window evidence is missing",
                    "does not infer mental-reset cost from the fair alone",
                    "explicitly abstains from rejecting the fair",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "saturday_plant_care_block", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "saturday_hike_reset_window", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "plant_fair_collides_saturday_blocks", "hop": 2},
            ],
            "forbidden": ["never do plant care", "must skip all hikes", "decline all neighbor events"],
            "distractor": {
                "timestamp": "2026-07-02T14:30:00Z",
                "user": f"{ca} said a prix-fixe Saturday restaurant signup is amazing and worth it for one night out.",
                "assistant": "A one-night restaurant signup is a different decision.",
                "why": "Restaurant signup FOMO is query-similar but not evidence about this user's Saturday plant-care or hike-window constraints.",
            },
            "evolving": {"saturday_plant_care": "non_negotiable", "saturday_hike_window": "only_reliable_reset"},
        },
        "S9": {
            "name": "bulk_developing_x_weekend_guest_room",
            "prefix_end": 54,
            "evidence": {
                "ev_A": {
                    "session_id": 50,
                    "fact": "A full-reel chemical bath in the spare nook leaves overnight fumes when the user processes thirty-six exposures.",
                },
                "ev_B": {
                    "session_id": 52,
                    "fact": "Overnight guests arrive Sunday after lunch and the spare nook must be cleared and ventilated before then.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-12T20:45:00Z",
            "query": "Considering a long wet-bench run Saturday night while I'm hosting overnight guests — sensible timing?",
            "gold": (
                "Do not run a long wet-bench session Saturday night in the spare nook. Full-reel chemical baths there leave overnight "
                "fumes, and your overnight guests arrive Sunday after lunch needing that nook cleared and ventilated. Process earlier in the week "
                "or use a shorter run elsewhere. The weekend cinema signup is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether Saturday-night wet-bench work fits. Full-reel chemical baths have left "
                "overnight fumes in the spare nook, but I cannot tell from the available memory when your guests arrive or "
                "whether the nook must be cleared. Confirm guest timing and room prep before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know overnight guests arrive Sunday after lunch "
                    "needing the spare nook cleared, but the available memory does not establish that full-reel chemical baths leave "
                    "overnight fumes there. I cannot reject the session from guest timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether Saturday-night wet-bench work fits. Full-reel chemical baths have left "
                    "overnight fumes in the spare nook, but I cannot tell from the available memory when your guests arrive or "
                    "whether the nook must be cleared. Confirm guest timing and room prep before deciding."
                ),
            },
            "required": [
                "uses full-reel chemical-bath overnight fumes in the spare nook",
                "uses Sunday-after-lunch guest-room clearance requirement",
                "recommends against Saturday-night wet-bench work in that nook",
            ],
            "absence_required": [
                "states that the guest-nook timing requirement is missing",
                "does not infer fume conflict from the plan alone",
                "asks about guest timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the chemical-bath fume evidence is missing",
                    "does not infer nook conflict from guest weekend alone",
                    "explicitly abstains from rejecting the session",
                ],
                "ev_B": [
                    "states that the guest-nook timing requirement is missing",
                    "does not infer fume conflict from the plan alone",
                    "asks about guest timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "overnight_spare_nook_fumes", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "guest_nook_clear_by_sunday_lunch", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "saturday_wet_bench_conflicts_guests", "hop": 2},
            ],
            "forbidden": ["never develop film", "cancel the guest", "darkroom is always unsafe"],
            "distractor": {
                "timestamp": "2026-07-11T15:00:00Z",
                "user": f"{cb} said a Saturday-night cinema blockbuster signup is amazing hype and worth grabbing tickets before hosting overnight guests — everyone in the group chat is pushing it.",
                "assistant": "A cinema ticket is a separate leisure decision.",
                "why": "Cinema signup hype shares Saturday-night guest-weekend surface but is not evidence about this user's spare-nook fumes or guest clearance deadline.",
            },
            "evolving": {"wet_bench_bulk": "overnight_spare_nook_fumes", "guest_nook": "clear_by_sunday_after_lunch"},
        },
        "S10": {
            "name": "bike_commute_x_late_tuesday_poker",
            "prefix_end": 59,
            "evidence": {
                "ev_A": {
                    "session_id": 55,
                    "fact": "Dawn bike rides on two fixed weekdays need solid prior-night sleep and a tuned bike.",
                },
                "ev_B": {
                    "session_id": 57,
                    "fact": "Midweek downtown cards have run past one before and wrecked the next dawn ride.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-21T06:50:00Z",
            "query": "Tuesday night poker signup is getting hype in the group chat. Worth joining?",
            "gold": (
                "Skip the Tuesday poker signup. Dawn bike commutes need solid prior-night sleep and a tuned bike, and Tuesday "
                "poker downtown has already run past one and wrecked the next morning commute. The board-game cafe Tuesday "
                "ticket is a different public outing."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether Tuesday poker fits your week. Dawn bike commutes need solid "
                "prior-night sleep, but I cannot tell from the available memory whether Tuesday poker runs late enough to "
                "threaten Thursday morning. Confirm game timing before joining."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Tuesday poker has run past one "
                    "and wrecked the next dawn commute, but the available memory does not establish that dawn bike commutes "
                    "need solid prior-night sleep. I cannot reject poker from commute needs alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether Tuesday poker fits your week. Dawn bike commutes need solid "
                    "prior-night sleep, but I cannot tell from the available memory whether Tuesday poker runs late enough to "
                    "threaten Thursday morning. Confirm game timing before joining."
                ),
            },
            "required": [
                "uses dawn bike commute sleep and bike-prep needs",
                "uses late Tuesday poker harming the next dawn commute",
                "recommends skipping the Tuesday poker signup",
            ],
            "absence_required": [
                "states that the late-poker consequence evidence is missing",
                "does not infer commute harm from the signup alone",
                "asks about game end time or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the commute-sleep evidence is missing",
                    "does not infer sleep harm from the signup alone",
                    "explicitly abstains from rejecting poker",
                ],
                "ev_B": [
                    "states that the late-poker consequence evidence is missing",
                    "does not infer commute harm from the signup alone",
                    "asks about game end time or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "requires", "target": "dawn_commute_sleep_bike", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "late_poker_wrecks_commute", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "tuesday_poker_threatens_commute", "hop": 2},
            ],
            "forbidden": ["never play poker", "cancel the commute", "bike commuting is unsafe"],
            "distractor": {
                "timestamp": "2026-07-19T18:30:00Z",
                "user": f"{ca} said a board-game cafe Tuesday night signup is amazing hype and worth grabbing as a public outing ticket.",
                "assistant": "A cafe ticket outing uses a different venue.",
                "why": "Board-game cafe Tuesday signup shares hype surface but is not evidence about this user's dawn commute sleep needs or late Tuesday poker pattern.",
            },
            "evolving": {"dawn_commute": "needs_sleep_and_tuned_bike", "tuesday_poker": "runs_late_past_one"},
        },
        "S11": {
            "name": "raku_kiln_fumes_x_sunday_long_run",
            "prefix_end": 65,
            "evidence": {
                "ev_A": {
                    "session_id": 61,
                    "fact": "Shared-studio raku firings on Saturdays leave the user lightheaded the next morning; glaze-only days at home have been fine.",
                },
                "ev_B": {
                    "session_id": 63,
                    "fact": "Sunday long-run training is non-negotiable during race prep.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-01T10:30:00Z",
            "query": "Worth joining the weekend firing roster this month given my current race-prep rhythm?",
            "gold": (
                "Decline the weekend firing roster for now. Shared-studio raku firings have left you lightheaded the next morning, "
                "but Sunday long-run training is non-negotiable during race prep. The charity walk signup chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Saturday raku firings have left you lightheaded, "
                "but I cannot tell from the available memory whether Sunday long-run training is currently protected. "
                "Confirm your race-prep schedule before joining a kiln session."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Sunday long-run training is "
                    "non-negotiable during race prep, but the available memory does not establish that Saturday raku firings "
                    "leave you lightheaded. I cannot reject the signup from training alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Saturday raku firings have left you lightheaded, "
                    "but I cannot tell from the available memory whether Sunday long-run training is currently protected. "
                    "Confirm your race-prep schedule before joining a kiln session."
                ),
            },
            "required": [
                "links Saturday raku firings to next-morning lightheadedness",
                "links Sunday long-run training as non-negotiable during race prep",
                "recommends declining the weekend firing roster",
            ],
            "absence_required": [
                "states that the Sunday long-run protection evidence is missing",
                "does not infer harm from the kiln invite alone",
                "explicitly abstains or asks about race-prep schedule",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the raku lightheadedness evidence is missing",
                    "does not infer training harm from the invite alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the Sunday long-run protection evidence is missing",
                    "does not infer harm from the kiln invite alone",
                    "explicitly abstains or asks about race-prep schedule",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "raku_next_morning_lightheaded", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "sunday_long_run_block", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "raku_signup_poor_fit", "hop": 2},
            ],
            "forbidden": ["pottery ban forever", "must never train", "skip all studio work"],
            "distractor": {
                "timestamp": "2026-05-08T11:00:00Z",
                "user": f"{ca} said a weekend firing roster signup this month is amazing hype and worth joining for summer studio bonding.",
                "assistant": "A charity walk signup is a different format from kiln sessions.",
                "why": "Charity walk signup hype is query-similar FOMO but not evidence about this user's raku lightheadedness or Sunday long-run block.",
            },
            "evolving": {"raku_pattern": "saturday_kiln_lightheaded", "sunday_run": "non_negotiable_race_prep"},
        },
        "S12": {
            "name": "late_tabletop_x_sunday_batch_cook",
            "prefix_end": 71,
            "evidence": {
                "ev_A": {
                    "session_id": 67,
                    "fact": "Saturday-night tabletop campaigns past midnight wreck the user's Sunday batch-cook rhythm; shorter games are fine.",
                },
                "ev_B": {
                    "session_id": 69,
                    "fact": "Sunday afternoon batch-cook is fixed meal-prep for the work week and does not move easily.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-12T18:20:00Z",
            "query": "Thinking of joining the all-day campaign Saturday before next week's kitchen rhythm — good idea?",
            "gold": (
                "Do not join the all-day Saturday campaign before next week's kitchen rhythm. Saturday-night tabletop campaigns "
                "past midnight have wrecked your Sunday batch-cook rhythm, and Sunday afternoon batch-cook is fixed meal-prep "
                "for the work week. Pick a shorter game or wait until after meal-prep week. The game-group streak hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an all-day Saturday campaign fits next week. Late tabletop "
                "sessions have wrecked Sunday batch-cook, but I cannot tell from the available memory whether Sunday afternoon "
                "meal-prep is fixed. Confirm your kitchen schedule before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Sunday afternoon batch-cook is "
                    "fixed meal-prep for the work week, but the available memory does not establish that late Saturday campaigns "
                    "wreck your Sunday rhythm. I cannot reject the campaign from meal-prep alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an all-day Saturday campaign fits next week. Late tabletop "
                    "sessions have wrecked Sunday batch-cook, but I cannot tell from the available memory whether Sunday afternoon "
                    "meal-prep is fixed. Confirm your kitchen schedule before committing."
                ),
            },
            "required": [
                "uses late Saturday tabletop wrecking Sunday batch-cook",
                "uses fixed Sunday afternoon meal-prep block",
                "recommends against the all-day Saturday campaign",
            ],
            "absence_required": [
                "states that the Sunday meal-prep timing evidence is missing",
                "does not infer kitchen harm from the campaign invite alone",
                "asks about meal-prep timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-tabletop Sunday-wreck evidence is missing",
                    "does not infer kitchen harm from the campaign alone",
                    "explicitly abstains from rejecting the campaign",
                ],
                "ev_B": [
                    "states that the Sunday meal-prep timing evidence is missing",
                    "does not infer kitchen harm from the campaign invite alone",
                    "asks about meal-prep timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_tabletop_wrecks_sunday_cook", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "sunday_batch_cook_block", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "saturday_campaign_risky", "hop": 2},
            ],
            "forbidden": ["games always harmful", "must skip social hobbies", "meal prep always unsafe"],
            "distractor": {
                "timestamp": "2026-05-20T11:00:00Z",
                "user": f"{cb} said joining an all-day campaign Saturday before next week's kitchen rhythm is amazing hype and worth it for group bonding.",
                "assistant": "Campaign streak hype is loud.",
                "why": "All-day campaign hype shares weekend surface but is not evidence about this user's late-tabletop Sunday-wreck pattern or fixed meal-prep block.",
            },
            "evolving": {"tabletop_timing": "late_saturday_wrecks_sunday", "batch_cook": "sunday_afternoon_fixed"},
        },
        "S13": {
            "name": "cupping_jitters_x_piano_recital_prep",
            "prefix_end": 76,
            "evidence": {
                "ev_A": {
                    "session_id": 72,
                    "fact": "High-caffeine cupping tastings after two in the afternoon wreck the user's evening piano practice focus; morning tastings have been fine.",
                },
                "ev_B": {
                    "session_id": 74,
                    "fact": "Piano recital piece needs calm evening practice this week.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-19T09:15:00Z",
            "query": "Cafe wants me at an afternoon tasting flight before this week's recital prep — workable?",
            "gold": (
                "Skip the afternoon tasting flight before this week's recital prep. High-caffeine cupping tastings after two "
                "in the afternoon have wrecked your evening piano practice focus, and the recital piece needs calm evening "
                "practice this week. Choose a morning flight or defer until after recital week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an afternoon tasting flight fits recital prep. Afternoon cupping "
                "has wrecked evening piano focus, but I cannot tell from the available memory whether this week's recital piece "
                "needs calm evening practice. Confirm recital timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the recital piece needs calm "
                    "evening practice this week, but the available memory does not establish that afternoon cupping wrecks your "
                    "piano focus. I cannot reject the flight from recital prep alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an afternoon tasting flight fits recital prep. Afternoon cupping "
                    "has wrecked evening piano focus, but I cannot tell from the available memory whether this week's recital piece "
                    "needs calm evening practice. Confirm recital timing before deciding."
                ),
            },
            "required": [
                "uses afternoon cupping wrecking evening piano focus",
                "uses recital piece needing calm evening practice",
                "recommends against the afternoon tasting flight",
            ],
            "absence_required": [
                "states that the recital evening-practice requirement is missing",
                "does not infer focus harm from the tasting invite alone",
                "asks about recital timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the afternoon-cupping focus evidence is missing",
                    "does not infer practice harm from the flight alone",
                    "explicitly abstains from rejecting the flight",
                ],
                "ev_B": [
                    "states that the recital evening-practice requirement is missing",
                    "does not infer focus harm from the tasting invite alone",
                    "asks about recital timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "afternoon_cupping_wrecks_piano_focus", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "recital_calm_evening_practice", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "afternoon_flight_conflicts_recital", "hop": 2},
            ],
            "forbidden": ["coffee ban", "must cancel recital", "all tastings unsafe"],
            "distractor": {
                "timestamp": "2026-06-02T14:00:00Z",
                "user": f"{ca} said an afternoon tasting flight before this week's recital prep is amazing hype and worth it for cafe community bonding.",
                "assistant": "Community bonding and evening practice are different ledgers.",
                "why": "Afternoon tasting-flight hype shares recital-week surface but is not evidence about this user's cupping focus pattern or calm evening practice need.",
            },
            "evolving": {"cupping_timing": "afternoon_wrecks_piano", "recital_prep": "calm_evening_practice"},
        },
        "S14": {
            "name": "track_tempo_x_thursday_long_run",
            "prefix_end": 81,
            "evidence": {
                "ev_A": {
                    "session_id": 77,
                    "fact": "Track tempo intervals aggravate shin splints for days; easy flat runs have been fine.",
                },
                "ev_B": {
                    "session_id": 79,
                    "fact": "Thursday long-run is on the training calendar this month and needs protected legs.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-27T06:50:00Z",
            "query": "Running-group friends swear by a speed-rep block tomorrow before this week's endurance block — one-off worth testing?",
            "gold": (
                "Skip the speed-rep block tomorrow before this week's endurance block. Track tempo intervals have aggravated shin "
                "splints for days, and Thursday long-run is on your training calendar and needs protected legs. Keep tomorrow "
                "easy or wait until after the endurance block. The forum ritual hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a track-tempo block tomorrow fits this week's long run. Track "
                "tempo has aggravated shin splints, but I cannot tell from the available memory whether Thursday long-run needs "
                "protected legs. Confirm training timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Thursday long-run needs protected "
                    "legs, but the available memory does not establish that track tempo aggravates your shin splints. "
                    "I cannot reject the block from schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a track-tempo block tomorrow fits this week's long run. Track "
                    "tempo has aggravated shin splints, but I cannot tell from the available memory whether Thursday long-run needs "
                    "protected legs. Confirm training timing before deciding."
                ),
            },
            "required": [
                "uses track tempo aggravating shin splints",
                "uses Thursday long-run needing protected legs",
                "recommends skipping speed-rep block before endurance block",
            ],
            "absence_required": [
                "states that the Thursday long-run protection evidence is missing",
                "does not infer shin harm from the group push alone",
                "asks about training timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the track-tempo shin evidence is missing",
                    "does not infer shin harm from the block alone",
                    "explicitly abstains from rejecting the block",
                ],
                "ev_B": [
                    "states that the Thursday long-run protection evidence is missing",
                    "does not infer shin harm from the group push alone",
                    "asks about training timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "track_tempo_shin_flare", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "thursday_long_run_protected_legs", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "tempo_block_before_long_run_risky", "hop": 2},
            ],
            "forbidden": ["running ban", "must skip track club", "exercise always unsafe"],
            "distractor": {
                "timestamp": "2026-06-12T18:30:00Z",
                "user": f"{ca} said a speed-rep block tomorrow before this week's endurance block is worth testing and everyone in the running-group forum is pushing it.",
                "assistant": "Forum guarantees are not injury facts.",
                "why": "Track-tempo block hype shares long-run-week surface but is not evidence about this user's shin-splint flare pattern or Thursday long-run protection.",
            },
            "evolving": {"track_tempo": "shin_splint_flare", "thursday_long_run": "protected_legs"},
        },
        "S15": {
            "name": "resin_fumes_x_balcony_herb_heatwave",
            "prefix_end": 86,
            "evidence": {
                "ev_A": {
                    "session_id": 82,
                    "fact": "Indoor resin pours without balcony venting overheat the apartment and stress the herb collection on the rail.",
                },
                "ev_B": {
                    "session_id": 84,
                    "fact": "Heat-wave week requires daily balcony shade and watering for the herb collection.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-04T20:45:00Z",
            "query": "Guild wants me at an indoor casting session midweek during the heat spell — workable with my rail-side plant routine booked?",
            "gold": (
                "Skip the indoor casting session midweek during the heat spell. Indoor resin pours without balcony venting have "
                "overheated the apartment and stressed your herb collection, and heat-wave week requires daily balcony shade "
                "and watering. Vent on the balcony or wait until after the heat spell."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an enclosed pour fits the heat spell. Indoor resin pours have "
                "stressed balcony herbs, but I cannot tell from the available memory whether heat-wave week requires daily shade "
                "and watering. Confirm balcony plant duties before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know heat-wave week requires daily "
                    "balcony shade and watering, but the available memory does not establish that enclosed resin pours overheat "
                    "the apartment and stress herbs. I cannot reject the pour from plant duties alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an enclosed pour fits the heat spell. Indoor resin pours have "
                    "stressed balcony herbs, but I cannot tell from the available memory whether heat-wave week requires daily shade "
                    "and watering. Confirm balcony plant duties before deciding."
                ),
            },
            "required": [
                "uses enclosed resin pours overheating apartment and stressing herbs",
                "uses heat-wave week daily balcony shade and watering",
                "recommends skipping indoor casting session during heat spell",
            ],
            "absence_required": [
                "states that the heat-wave balcony-duty evidence is missing",
                "does not infer plant harm from the pour invite alone",
                "asks about balcony duties or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the resin-fume herb-stress evidence is missing",
                    "does not infer plant harm from the pour alone",
                    "explicitly abstains from rejecting the session",
                ],
                "ev_B": [
                    "states that the heat-wave balcony-duty evidence is missing",
                    "does not infer plant harm from the pour invite alone",
                    "asks about balcony duties or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "enclosed_resin_stresses_herbs", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "heatwave_balcony_duties", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "enclosed_pour_conflicts_heatwave", "hop": 2},
            ],
            "forbidden": ["resin ban forever", "must abandon herbs", "maker hobbies always unsafe"],
            "distractor": {
                "timestamp": "2026-06-22T15:00:00Z",
                "user": f"{cb} said an indoor casting session midweek during the heat spell is amazing hype and worth it for guild community bonding.",
                "assistant": "Community bonding and balcony plant duties are different decisions.",
                "why": "Enclosed pour hype shares heat-spell surface but is not evidence about this user's resin herb-stress pattern or heat-wave balcony duties.",
            },
            "evolving": {"resin_pour": "enclosed_overheats_herbs", "heatwave_herbs": "daily_shade_water"},
        },
        "S16": {
            "name": "street_noise_x_illustration_sprint",
            "prefix_end": 91,
            "evidence": {
                "ev_A": {
                    "session_id": 88,
                    "fact": "Open-window street noise wrecks the user's focused pencil sketching; closed-window sessions are fine.",
                },
                "ev_B": {
                    "session_id": 90,
                    "fact": "Illustration sprint week needs protected morning solo sketch blocks Tuesday through Thursday.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-10T10:15:00Z",
            "query": "Worth trying the open-air drawing circle before Thursday's illustration lock?",
            "gold": (
                "Skip the open-air drawing circle before Thursday's illustration lock. Open-window street noise has wrecked "
                "your focused pencil sketching, and illustration sprint week needs protected morning solo sketch blocks "
                "Tuesday through Thursday. Use closed-window blocks or defer the circle until after the lock. The studio "
                "signup blurb chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the open-air drawing circle fits before Thursday's illustration lock. "
                "Street noise has wrecked sketching focus, but I cannot tell from the available memory whether Tuesday through "
                "Thursday morning solo blocks are already protected. Confirm the illustration calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know illustration sprint week needs "
                    "protected morning solo sketch blocks Tuesday through Thursday, but the available memory does not establish "
                    "that open-window street noise wrecks your sketching focus. I cannot reject the circle from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the open-air drawing circle fits before Thursday's illustration lock. "
                    "Street noise has wrecked sketching focus, but I cannot tell from the available memory whether Tuesday through "
                    "Thursday morning solo blocks are already protected. Confirm the illustration calendar before deciding."
                ),
            },
            "required": [
                "uses street noise wrecking focused pencil sketching",
                "uses illustration sprint week needing protected morning solo blocks",
                "recommends skipping open-air drawing circle before illustration lock",
            ],
            "absence_required": [
                "states that the illustration-sprint solo-block evidence is missing",
                "does not infer focus harm from the drawing-circle invite alone",
                "asks about illustration calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the street-noise sketching evidence is missing",
                    "does not infer sketch harm from the circle alone",
                    "explicitly abstains from rejecting the circle",
                ],
                "ev_B": [
                    "states that the illustration-sprint solo-block evidence is missing",
                    "does not infer focus harm from the drawing-circle invite alone",
                    "asks about illustration calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "street_noise_wrecks_sketching", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "illustration_sprint_solo_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "drawing_circle_conflicts_sprint", "hop": 2},
            ],
            "forbidden": ["sketching ban forever", "must skip all studio events", "illustration always unsafe"],
            "distractor": {
                "timestamp": "2026-06-05T11:00:00Z",
                "user": f"{ca} said the open-air drawing circle before Thursday's illustration lock is amazing hype and worth joining for studio visibility.",
                "assistant": "Visibility circles and illustration lock focus are different ledgers.",
                "why": "Drawing-circle signup hype shares illustration-lock surface but is not evidence about this user's street-noise sketch pattern or protected morning solo blocks.",
            },
            "evolving": {"street_noise": "wrecks_open_window_sketching", "illustration_sprint": "tue_thu_morning_solo_blocks"},
        },
        "S17": {
            "name": "craft_fair_volunteer_x_kiln_prep_deadline",
            "prefix_end": 96,
            "evidence": {
                "ev_A": {
                    "session_id": 93,
                    "fact": "Full-day craft-fair volunteering leaves the user too drained for studio work; short booth shifts are fine.",
                },
                "ev_B": {
                    "session_id": 95,
                    "fact": "Studio packet due Friday needs three solo evening studio blocks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-18T17:30:00Z",
            "query": "Hall immersion week before Friday's packet filing cutoff — workable?",
            "gold": (
                "Do not add a hall immersion week before Friday's packet filing cutoff. Full-day craft-fair volunteering "
                "has left you too drained for studio work, and the studio packet due Friday needs three solo evening studio "
                "blocks. Keep short booth shifts only or wait until after the packet prep. The maker immersion streak hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a hall immersion week fits the packet filing push. "
                "Full-day volunteering has drained studio energy, but I cannot tell from the available memory whether Friday's "
                "filing cutoff needs three solo evening blocks. Confirm packet prep timing before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the studio packet due Friday "
                    "needs three solo evening studio blocks, but the available memory does not establish that full-day volunteering "
                    "drains your studio energy. I cannot reject immersion from deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a hall immersion week fits the packet filing push. "
                    "Full-day volunteering has drained studio energy, but I cannot tell from the available memory whether Friday's "
                    "filing cutoff needs three solo evening blocks. Confirm packet prep timing before committing."
                ),
            },
            "required": [
                "uses full-day craft-fair volunteering draining studio energy",
                "uses Friday studio packet needing solo evening blocks",
                "recommends against hall immersion week before packet filing cutoff",
            ],
            "absence_required": [
                "states that the kiln-prep solo-evening-block evidence is missing",
                "does not infer energy harm from the fair-shift invite alone",
                "asks about firing prep timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the volunteering energy-drain evidence is missing",
                    "does not infer kiln harm from the fair shifts alone",
                    "explicitly abstains from rejecting fair shifts",
                ],
                "ev_B": [
                    "states that the kiln-prep solo-evening-block evidence is missing",
                    "does not infer energy harm from the fair-shift invite alone",
                    "asks about firing prep timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "fair_volunteering_drains_studio", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "kiln_prep_solo_evening_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "fair_shift_conflicts_kiln_prep", "hop": 2},
            ],
            "forbidden": ["volunteering ban", "must skip all fairs", "kiln prep always unsafe"],
            "distractor": {
                "timestamp": "2026-06-08T14:00:00Z",
                "user": f"{cb} said a hall immersion week before Friday's packet filing cutoff is amazing hype and worth it for maker visibility.",
                "assistant": "Maker visibility and packet filing blocks are different ledgers.",
                "why": "Hall immersion week hype shares filing-cutoff surface but is not evidence about this user's volunteering energy drain or solo evening studio blocks.",
            },
            "evolving": {"craft_fair": "full_day_drains_studio", "studio_packet": "friday_solo_evening_blocks"},
        },
        "S18": {
            "name": "evening_wine_x_yoga_intensive",
            "prefix_end": 101,
            "evidence": {
                "ev_A": {
                    "session_id": 98,
                    "fact": "Evening wine tastings wreck the user's next-morning yoga balance; afternoon tastings have been fine.",
                },
                "ev_B": {
                    "session_id": 100,
                    "fact": "Saturday flow intensive needs sharp morning balance; a late-slot social signup is booked through the night before.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-28T11:40:00Z",
            "query": "Cellar crew added a dusk-to-dawn tasting signup — sensible with Saturday's flow lock ahead?",
            "gold": (
                "Skip the dusk-to-dawn tasting signup before Saturday's flow lock. Evening wine tastings have wrecked your "
                "next-morning yoga balance, and Saturday flow intensive needs a sharp morning balance block while a late-slot "
                "social signup is already booked through the night before. Protect sleep and morning balance or defer the signup "
                "until after the intensive."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a dusk-to-dawn tasting signup fits before Saturday's flow lock. "
                "Evening tastings have wrecked next-morning balance, but I cannot tell from the available memory whether Saturday "
                "flow intensive needs a sharp morning balance block. Confirm intensive timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Saturday flow intensive needs sharp "
                    "morning balance while a late-slot social signup is booked through the night before, but the available memory "
                    "does not establish that evening tastings wreck your next-morning balance. I cannot reject the signup from "
                    "intensive timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a dusk-to-dawn tasting signup fits before Saturday's flow lock. "
                    "Evening tastings have wrecked next-morning balance, but I cannot tell from the available memory whether Saturday "
                    "flow intensive needs a sharp morning balance block. Confirm intensive timing before deciding."
                ),
            },
            "required": [
                "uses evening wine tastings wrecking next-morning yoga balance",
                "uses Saturday flow intensive needing sharp morning balance",
                "recommends against dusk-to-dawn tasting signup before flow lock",
            ],
            "absence_required": [
                "states that the flow-intensive balance-block evidence is missing",
                "does not infer balance harm from the signup invite alone",
                "asks about intensive timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the evening-tasting balance evidence is missing",
                    "does not infer intensive harm from the signup alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the flow-intensive balance-block evidence is missing",
                    "does not infer balance harm from the signup invite alone",
                    "asks about intensive timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "evening_wine_wrecks_morning_balance", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "saturday_flow_sharp_morning", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "tasting_conflicts_flow_intensive", "hop": 2},
            ],
            "forbidden": ["wine ban forever", "must skip all cellar events", "yoga always unsafe"],
            "distractor": {
                "timestamp": "2026-06-15T16:30:00Z",
                "user": f"{ca} said the dusk-to-dawn tasting signup before Saturday's flow lock is amazing hype and worth it for cellar community bonding.",
                "assistant": "Community bonding and flow-lock balance are different ledgers.",
                "why": "Tasting signup hype shares flow-lock surface but is not evidence about this user's evening-wine balance pattern or Saturday morning balance block.",
            },
            "evolving": {"evening_wine": "wrecks_morning_balance", "flow_intensive": "saturday_sharp_morning_balance"},
        },
        "S19": {
            "name": "paper_grid_layout_x_gallery_wall_walkthrough",
            "prefix_end": 106,
            "evidence": {
                "ev_A": {
                    "session_id": 103,
                    "fact": "The user composes gallery layouts best on paper grid mockups; wall-only layout sessions produce weak results.",
                },
                "ev_B": {
                    "session_id": 105,
                    "fact": "A prior wall-only gallery layout rehearsal went poorly before the corridor show.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-07T16:20:00Z",
            "query": "Gallery wants me on the poster-board run-through for next week's corridor show — good fit?",
            "gold": (
                "Decline or renegotiate to a paper-grid prep role. You compose gallery layouts best on paper grid mockups and a "
                "prior wall-only gallery layout rehearsal went poorly before the corridor show. Offer a grid-based layout walkthrough "
                "or prepared mockup instead. The gallery forum hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a poster-board run-through fits next week's corridor show. "
                "Paper grid mockups have produced your strongest layouts, but I cannot tell from the available memory whether a "
                "prior wall-only rehearsal failed. Confirm your poster-board track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior wall-only gallery layout "
                    "rehearsal went poorly, but the available memory does not establish that paper grid mockups are your strongest "
                    "layout format. I cannot reject the walkthrough from one bad session alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a poster-board run-through fits next week's corridor show. "
                    "Paper grid mockups have produced your strongest layouts, but I cannot tell from the available memory whether a "
                    "prior wall-only rehearsal failed. Confirm your poster-board track record before volunteering."
                ),
            },
            "required": [
                "uses paper grid mockups as strongest layout format",
                "uses prior wall-only gallery layout rehearsal failure",
                "recommends declining or shifting away from poster-board run-through",
            ],
            "absence_required": [
                "states that the wall-only rehearsal failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about wall-only track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the paper-grid layout evidence is missing",
                    "does not infer corridor-show harm from the walkthrough alone",
                    "explicitly abstains from rejecting the walkthrough",
                ],
                "ev_B": [
                    "states that the wall-only rehearsal failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about wall-only track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "paper_grid_layout_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "wall_only_rehearsal_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "wall_walkthrough_poor_fit", "hop": 2},
            ],
            "forbidden": ["layout ban", "must skip corridor show", "gallery prep always unsafe"],
            "distractor": {
                "timestamp": "2026-06-20T18:00:00Z",
                "user": f"{ca} said the poster-board run-through for next week's corridor show is amazing hype and everyone in the gallery forum is pushing it.",
                "assistant": "Forum defaults are not prep facts.",
                "why": "Poster-board run-through hype shares corridor-show surface but is not evidence about this user's paper-grid layout strength or prior wall-only rehearsal failure.",
            },
            "evolving": {"layout_format": "paper_grid_strength", "corridor_show": "wall_only_rehearsal_failed"},
        },
        "S20": {
            "name": "crowded_transit_x_cousin_hosting_weekend",
            "prefix_end": 111,
            "evidence": {
                "ev_A": {
                    "session_id": 108,
                    "fact": "Long crowded transit legs to evening hobby venues drain the user's energy before home creative blocks; short bike trips are fine.",
                },
                "ev_B": {
                    "session_id": 110,
                    "fact": "Quiet-home stretch requires calm atmosphere for restorative hobbies.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-17T18:10:00Z",
            "query": "Worth accepting the heavier venue corridor block this week — based on what you know about me?",
            "gold": (
                "Lean no unless the block is shortened or moved earlier. Long crowded transit legs to evening hobby venues have "
                "drained your energy before home creative blocks, and quiet-home stretch requires calm atmosphere for restorative "
                "hobbies. Keep outings local or defer until after the stretch."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Long crowded transit has drained energy, "
                "but I cannot tell from the available memory whether quiet-home stretch requires calm atmosphere for restorative hobbies. "
                "Confirm stretch home needs before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know quiet-home stretch requires calm "
                    "atmosphere for restorative hobbies, but the available memory does not establish that long crowded transit drains "
                    "your energy before home creative blocks. I cannot reject the block from stretch timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Long crowded transit has drained energy, "
                    "but I cannot tell from the available memory whether quiet-home stretch requires calm atmosphere for restorative hobbies. "
                    "Confirm stretch home needs before deciding."
                ),
            },
            "required": [
                "uses long crowded transit draining energy before home creative blocks",
                "uses quiet-home stretch requiring calm atmosphere for restorative hobbies",
                "recommends declining or shortening late venue corridor block during quiet-home stretch",
            ],
            "absence_required": [
                "states that the quiet-home stretch atmosphere evidence is missing",
                "does not infer energy harm from the block invite alone",
                "asks about stretch home needs or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the crowded-transit energy-drain evidence is missing",
                    "does not infer home-harm from the outing alone",
                    "explicitly abstains from rejecting the outing",
                ],
                "ev_B": [
                    "states that the cousin-hosting quiet-home evidence is missing",
                    "does not infer energy harm from the outing invite alone",
                    "asks about hosting-week home needs or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "crowded_transit_drains_home_energy", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "cousin_hosting_quiet_home", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "late_outing_conflicts_hosting", "hop": 2},
            ],
            "forbidden": ["transit ban forever", "must cancel hosting", "hobbies always unsafe"],
            "distractor": {
                "timestamp": "2026-06-25T09:30:00Z",
                "user": f"{cb} said accepting the heavier venue corridor block this week is amazing hype and worth it for venue community bonding.",
                "assistant": "Venue bonding and quiet-home atmosphere are different ledgers.",
                "why": "Heavier venue corridor block hype is query-similar FOMO but is not evidence about this user's crowded-transit energy drain or calm-atmosphere need during quiet-home stretch.",
            },
            "evolving": {"crowded_transit": "drains_home_creative_energy", "quiet_home_stretch": "calm_atmosphere_required"},
        },
    }


def load_personas() -> list[dict[str, Any]]:
    data = json.loads(PERSONAS_PATH.read_text(encoding="utf-8"))
    personas = list(data["users"])
    personas.append(USER10_PERSONA)
    return personas


def parse_scenario_ids(raw: str) -> tuple[str, ...]:
    raw = raw.strip().upper()
    if raw in {"S1-S5", "1-5"}:
        return ("S1", "S2", "S3", "S4", "S5")
    if raw in {"S6-S10", "6-10", "NEW"}:
        return ("S6", "S7", "S8", "S9", "S10")
    if raw in {"S11-S15", "11-15"}:
        return ("S11", "S12", "S13", "S14", "S15")
    if raw in {"S16-S20", "16-20"}:
        return ("S16", "S17", "S18", "S19", "S20")
    if raw in {"S1-S20", "1-20"}:
        return tuple(f"S{i}" for i in range(1, 21))
    if raw in {"S6-S15", "6-15"}:
        return tuple(f"S{i}" for i in range(6, 16))
    if raw in {"S11-S20", "11-20"}:
        return tuple(f"S{i}" for i in range(11, 21))
    if raw in {"S6-S20", "6-20"}:
        return tuple(f"S{i}" for i in range(6, 21))
    if "," in raw:
        return tuple(part.strip() for part in raw.split(",") if part.strip())
    return (raw,)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate hobby/habit gold JSON items.")
    parser.add_argument(
        "--scenarios",
        default="S11-S15",
        help="Scenario scope: S1-S5, S6-S10, S11-S15, S16-S20, S1-S20, etc.",
    )
    args = parser.parse_args(argv)
    scenario_ids = parse_scenario_ids(args.scenarios)
    if scenario_ids == ("S1", "S2", "S3", "S4", "S5"):
        batch_config = {
            **HH_BATCH_CONFIG,
            "batch_id": "HH_GOLD_S1_S5_2026-07-16_v2",
            "generator_name": "hobby_habit_gold_s1_s5_v2",
        }
    elif scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        batch_config = {
            **HH_BATCH_CONFIG,
            "batch_id": "HH_GOLD_S16_S20_2026-07-16_v2",
            "generator_name": "hobby_habit_gold_s16_s20_v2",
        }
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **HH_BATCH_CONFIG,
            "batch_id": "HH_GOLD_S11_S15_2026-07-15_v2",
            "generator_name": "hobby_habit_gold_s11_s15_v2",
        }
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10"):
        batch_config = {
            **HH_BATCH_CONFIG,
            "batch_id": "HH_GOLD_S6_S10_2026-07-15_v2",
            "generator_name": "hobby_habit_gold_s6_s10_v2",
        }
    elif scenario_ids == tuple(f"S{i}" for i in range(1, 21)):
        batch_config = {
            **HH_BATCH_CONFIG,
            "batch_id": "HH_GOLD_S1_S20_2026-07-16_v2",
            "generator_name": "hobby_habit_gold_batch_v2",
        }
    else:
        batch_config = HH_BATCH_CONFIG
    arms = ("associative", "distractor", "absence")
    personas = load_personas()

    report_items: list[dict[str, Any]] = []
    failures = 0
    score_totals: list[float] = []

    for persona in personas:
        idx = persona["user_index"]
        timeline = build_timeline(persona)
        scenarios = build_scenarios(persona)
        for sid in scenario_ids:
            for arm in arms:
                item = build_item(
                    timeline,
                    scenarios,
                    persona,
                    idx,
                    sid,
                    arm,
                    computed_by=COMPUTED_BY,
                    batch_config=batch_config,
                )
                errors = hard_gate_errors(item, timeline, scenarios, computed_by=COMPUTED_BY)
                scores = score_item(item, errors)
                score_totals.append(scores["total"])
                path = output_path(PILOT_ROOT, persona, item, batch_config=batch_config)
                gate_pass = not errors
                if gate_pass:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                else:
                    failures += 1
                report_items.append(
                    {
                        "sample_id": item["sample_id"],
                        "path": str(path.relative_to(PILOT_ROOT)),
                        "user_index": idx,
                        "scenario_id": sid,
                        "arm": arm,
                        "hard_gate_pass": gate_pass,
                        "errors": errors,
                        "metrics": item["validity_metrics"],
                        "scores": scores,
                    }
                )
                status = "PASS" if gate_pass else "FAIL"
                print(f"{status}\t{item['sample_id']}\tscore={scores['total']}")
                for error in errors:
                    print(f"  - {error}")

    n = len(report_items)
    n_pass = sum(1 for r in report_items if r["hard_gate_pass"])
    report = {
        "generated_at": GENERATED_AT,
        "generator": batch_config["generator_name"],
        "scenario_scope": list(scenario_ids),
        "n": n,
        "n_pass": n_pass,
        "n_fail": failures,
        "score_distribution": {
            "min": min(score_totals) if score_totals else 0,
            "max": max(score_totals) if score_totals else 0,
            "mean": round(sum(score_totals) / len(score_totals), 2) if score_totals else 0,
            "at_95": sum(1 for s in score_totals if s >= 95),
        },
        "items": report_items,
    }
    manifest_dir = PILOT_ROOT / "manifests" / "hobby"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    report_path = manifest_dir / (
        "hobby_habit_gold_s1_s5_report.json"
        if scenario_ids == ("S1", "S2", "S3", "S4", "S5")
        else "hobby_habit_gold_s16_s20_report.json"
        if scenario_ids == ("S16", "S17", "S18", "S19", "S20")
        else "hobby_habit_gold_s11_s15_report.json"
        if scenario_ids == ("S11", "S12", "S13", "S14", "S15")
        else "hobby_habit_gold_s6_s10_report.json"
        if scenario_ids == ("S6", "S7", "S8", "S9", "S10")
        else "hobby_habit_gold_batch_v2_report.json"
    )
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nSUMMARY {n_pass}/{n} hard-gate PASS")
    print(f"SCORES min={report['score_distribution']['min']} max={report['score_distribution']['max']} mean={report['score_distribution']['mean']}")
    print(f"AT_95={report['score_distribution']['at_95']}")
    print(f"REPORT {report_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

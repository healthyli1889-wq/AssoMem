#!/usr/bin/env python3
"""Generate social/relationships gold batches (S1–S20).

Writes to src/data/{domain}/{arm}/AMB_*_u{NN}_{arm}_S{N}.json
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime, timedelta
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
    output_path,
    score_item,
    session,
)

PERSONAS_PATH = DOMAIN / "personas" / "personas_social.json"
COMPUTED_BY = "tools/social/bin/generate_social_gold_batch.py"

SC_BATCH_CONFIG: dict[str, Any] = {
    "id_prefix": "SC",
    "pilot_domain": "social_relation",
    "domain_tags": ["social/relationships", "everyday_social"],
    "data_subdir": "social",
    "folder_prefix": "social",
    "batch_id": "SC_GOLD_S1_S5_2026-07-17_v2",
    "generator_name": "social_gold_s1_s5_v2",
    "reproduce_generator": "python3 tools/social/bin/generate_social_gold_batch.py",
}

USER10_PERSONA: dict[str, Any] = {
    "user_index": 10,
    "user_id": "sc_u10",
    "folder_tag": "user10",
    "display_name": "desktop-Healthy_Li",
    "source_corpus": "desktop_user",
    "source_ref": "local:Healthy Li; migrated from pilot SC",
    "stable_traits": [
        "psychology + AI research student",
        "University of Michigan exchange",
        "King's College London BSc Psychology",
        "protects social energy budget",
        "prefers deep one-on-ones over large mixers",
    ],
    "voice": "curious, reflective, student-researcher",
}

# Shared cumulative social timeline (sessions 1–32 for S1–S5)
CANONICAL_TIMELINE = [
    # S1
    session(1, "2026-01-11T18:00:00Z", "Texted a friend back after a long day. Kept it short.", "Short replies are fine."),
    session(2, "2026-01-12T18:00:00Z", "Canceled a vague coffee invite. Felt lighter.", "Optional social plans can wait."),
    session(3, "2026-01-18T18:00:00Z", "Walked home after a small dinner. Conversation felt easy.", "Small formats suit you."),
    session(
        4,
        "2026-01-26T18:00:00Z",
        "Large noisy gatherings leave me drained and snappy the next day. Small dinners with three or four people are fine.",
        "Has that contrast repeated?",
        "Yes. Twice after packed house nights; small dinners did not.",
    ),
    session(5, "2026-02-03T18:00:00Z", "Muted a group chat for an afternoon. Quiet helped.", "Attention has a ledger."),
    session(
        6,
        "2026-02-10T18:00:00Z",
        "Roommate has early shifts this month and asked for quieter evenings at home — already on the household calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(7, "2026-02-17T18:00:00Z", "Friends chat is hyping a packed house mixer this weekend — everyone saying it is amazing for the group.", "Signup FOMO around hosting is loud."),
    session(8, "2026-02-24T18:00:00Z", "Someone asked whether hosting that packed house mixer is worth it for networking.", "Networking and capacity are different questions."),
    session(9, "2026-03-02T18:00:00Z", "Printed March social calendar. Quiet nights are marked.", "Paper copies help on busy weeks."),
    # S2
    session(10, "2026-03-09T18:00:00Z", "Archived old event photos from last year. Less phone clutter.", "Digital tidy helps."),
    session(
        11,
        "2026-03-16T18:00:00Z",
        "Rapid group-chat reply storms leave me anxious and snappy the next day. Slow one-to-one threads are fine.",
        "Has the reply-storm pattern repeated?",
        "Yes. Three storm days did it; slow threads did not.",
    ),
    session(12, "2026-03-23T18:00:00Z", "Short walk after lunch. Cleared the afternoon fog.", "Worth repeating."),
    session(
        13,
        "2026-03-30T18:00:00Z",
        "Close friend needs a slow one-on-one call this week — not group logistics. Already on the calendar.",
        "Is that slot movable?",
        "Not easily. The check-in depends on it.",
    ),
    session(14, "2026-04-06T18:00:00Z", "Someone hyped being the always-on message runner. Different beast from a real check-in.", "Signup FOMO comes in many shapes."),
    session(15, "2026-04-13T18:00:00Z", "Reunion planning chat is loud. I muted notifications overnight.", "Mute buttons save attention."),
    session(16, "2026-04-20T18:00:00Z", "Printed the check-in reminder. Slow call is marked in red.", "Paper copies help on busy weeks."),
    # S3
    session(17, "2026-04-27T18:00:00Z", "Declined a last-minute drinks invite. Energy was already spent.", "Boundaries are data."),
    session(
        18,
        "2026-05-04T18:00:00Z",
        "Stacking more than two social coffee hangs in one day leaves me hollow by evening. One or two are fine.",
        "Has that stacking pattern repeated?",
        "Yes. Three triple-coffee days did it; single hangs did not.",
    ),
    session(19, "2026-05-11T18:00:00Z", "Wrote a short note to a friend. No reply needed.", "Low-pressure contact counts."),
    session(
        20,
        "2026-05-18T18:00:00Z",
        "Thursday repair conversation with a friend needs my full presence — already booked as a protected block.",
        "Is that timing firm?",
        "Yes. Moving it would delay the repair.",
    ),
    session(21, "2026-05-25T18:00:00Z", "Calendar is filling with midweek catch-up invites. I filed two without replying.", "Invites can wait for an energy plan."),
    session(22, "2026-06-01T18:00:00Z", "Short reading block after lunch. Kept it under thirty minutes.", "Bounded breaks help."),
    session(23, "2026-06-08T18:00:00Z", "Friend chat is full of catch-up FOMO. Everyone asking who will say yes.", "Social pressure can outrun capacity."),
    session(24, "2026-06-15T18:00:00Z", "Printed the repair-talk calendar. Thursday block is marked.", "Paper copies help on busy weeks."),
    # S4
    session(
        25,
        "2026-06-22T18:00:00Z",
        "I freeze when put on the spot for public compliments in group settings. Private notes work better for me.",
        "Has the public-compliment freeze repeated?",
        "Yes. Twice at open tables; private notes did not.",
    ),
    session(26, "2026-06-29T18:00:00Z", "Wrote thank-you notes after a small dinner. Felt natural.", "Private formats fit."),
    session(
        27,
        "2026-07-02T18:00:00Z",
        "Prior live shoutout round at a group dinner went poorly — I blanked and felt awkward for hours.",
        "Harsh memory. Was the room unfamiliar?",
        "No. The format fought my process.",
    ),
    session(28, "2026-07-04T18:00:00Z", "Host chat is pushing a live recognition round. I filed it without replying.", "Format FOMO is loud."),
    # S5
    session(
        29,
        "2026-07-06T18:00:00Z",
        "Solo Saturday mornings are how I recover from a social week. Skipping them leaves me flat through Monday.",
        "Is that block fixed?",
        "Yes. It is a short but immovable recharge.",
    ),
    session(30, "2026-07-08T18:00:00Z", "Cafe posted a public daytime signup. Different venue, not home.", "Outings and recharge blocks are different."),
    session(
        31,
        "2026-07-10T18:00:00Z",
        "Family visit is already booked through Saturday afternoon — my morning alone time that day is gone.",
        "Is that deadline firm?",
        "Yes. It is already on the calendar.",
    ),
    session(32, "2026-07-12T18:00:00Z", "Neighbor floated another morning group invite. I archived it.", "Weekend mornings need a capacity check."),
    # S6
    session(33, "2026-06-04T17:55:00Z", "Social recovery evenings are finally visible on my calendar again.", "Tradeoffs are easier to see."),
    session(
        34,
        "2026-06-07T20:30:00Z",
        "Multi-hour group dinners past eleven leave me socially flat the next morning. Short two-hour dinners are fine.",
        "Has the late long-table pattern repeated?",
        "Twice this month. Short dinners do not do it — it is the late multi-hour tables.",
    ),
    session(35, "2026-06-09T13:20:00Z", "Walked back from a small coffee. Nice reset.", "Small resets add up."),
    session(
        36,
        "2026-06-11T07:10:00Z",
        "Promised a friend an early Saturday bike ride — I need solid prior-night energy or I am useless on the trail.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(37, "2026-06-13T16:40:00Z", "Friends chat keeps pushing a late multi-course group table signup. Lots of FOMO.", "Late-table FOMO is loud."),
    session(38, "2026-06-14T18:05:00Z", "Someone asked whether any late group table is worth it for staying socially warm.", "Warmth and next-morning energy are different questions."),
    # S7
    session(39, "2026-06-16T19:15:00Z", "Tidied the entryway after a planned visit. Felt calm.", "Planned visits land better."),
    session(
        40,
        "2026-06-18T21:50:00Z",
        "Unannounced drop-in visits wreck my evening wind-down for hours. Planned visits are fine.",
        "Has the drop-in pattern repeated?",
        "Yes. Once the evening fractures, I stay wired until late.",
    ),
    session(41, "2026-06-20T12:30:00Z", "Short lunch alone. Helped the afternoon.", "Breaks protect afternoon quality."),
    session(
        42,
        "2026-06-22T08:45:00Z",
        "Weekly Tuesday evening listening check-in with my sibling is already protected on the calendar.",
        "Is that slot movable?",
        "Not easily. We treat it as standing.",
    ),
    session(43, "2026-06-24T14:10:00Z", "Building chat is loud about spontaneous Tuesday evening pop-ins.", "Pop-in pressure is loud."),
    session(44, "2026-06-25T17:20:00Z", "Someone asked whether any Tuesday evening pop-in is worth the tradeoff.", "Spontaneity and protected check-ins are different questions."),
    # S8
    session(
        45,
        "2026-06-27T10:05:00Z",
        "I am best at private written thanks, not on-the-spot group gift speeches under lights.",
        "Has live gift-speech underperformed?",
        "Yes. Private notes land; live gift speeches do not.",
    ),
    session(46, "2026-06-28T15:40:00Z", "Wrote a short private thank-you after a farewell coffee.", "Private formats fit."),
    session(
        47,
        "2026-06-30T19:30:00Z",
        "Last live group gift toast went poorly — I blanked and follow-up felt awkward for days.",
        "Was that a one-off?",
        "No. Live gift speeches under pressure are a weak spot for me.",
    ),
    session(48, "2026-07-01T11:15:00Z", "Farewell chat is hyping a live gift-speech slot next week.", "Live format invites need a skill check."),
    session(49, "2026-07-02T16:50:00Z", "Someone forwarded hype about volunteering for any live gift toast for warmth.", "Warmth and live skill fit are different questions."),
    # S9
    session(
        50,
        "2026-07-06T22:15:00Z",
        "Overnight guests leave me cognitively and socially flat through the next full day — details slip on careful talks.",
        "Was it just one visit?",
        "Twice. The morning after overnight hosting is the problem.",
    ),
    session(51, "2026-07-08T07:45:00Z", "Guest towels are washed. Return timing for Sunday hosting still open.", "Hosting timing and Monday talks overlap."),
    session(
        52,
        "2026-07-10T16:20:00Z",
        "One-on-one mentoring coffee is locked Monday 10am right after the weekend.",
        "Is that deadline firm?",
        "Yes. It is already on the calendar.",
    ),
    session(53, "2026-07-11T08:00:00Z", "Forum crowd insists overnight guests Sunday before Monday mentoring is normal. I disagree.", "Online norms are not calendar facts."),
    session(54, "2026-07-12T19:30:00Z", "Someone forwarded hype about Sunday overnight hosting before Monday mentoring. Not my plan.", "Social pressure is not a schedule."),
    # S10
    session(
        55,
        "2026-07-14T18:10:00Z",
        "Constant status-update pings during evenings kill my presence for real conversations — sloppy replies follow.",
        "Has that pattern repeated?",
        "Yes. Always-on status evenings are costly.",
    ),
    session(56, "2026-07-16T12:30:00Z", "Muted non-urgent status channels before evening writing.", "Small guardrails help."),
    session(
        57,
        "2026-07-18T09:40:00Z",
        "A careful letter to a distant friend needs an uninterrupted evening without ping churn.",
        "Is that block protected?",
        "Yes. I already marked it.",
    ),
    session(58, "2026-07-19T17:05:00Z", "Group chat keeps pushing a five-day always-on status-update roster. I am ignoring the hype for now.", "Status invites need a presence check."),
    session(59, "2026-07-20T07:20:00Z", "Letter evening is on the calendar right after that proposed status-roster week.", "Presence math matters for letter weeks."),
    # S11
    session(60, "2026-07-22T18:00:00Z", "Social recovery blocks are finally visible on the calendar again.", "Tradeoffs are easier to see."),
    session(
        61,
        "2026-07-24T20:30:00Z",
        "Back-to-back video hangouts leave my voice and presence thin for next-day in-person talks — async notes do not.",
        "Has that pattern repeated?",
        "Twice this month. Async notes are fine — it is the stacked video hangs.",
    ),
    session(62, "2026-07-26T13:20:00Z", "Walked back from a short errand. Nice reset.", "Small movement breaks add up."),
    session(
        63,
        "2026-07-28T07:10:00Z",
        "In-person reunion lunch Thursday at noon is non-negotiable — I am treating it as a hard calendar boundary.",
        "Is that timing firm?",
        "Yes. It is already locked.",
    ),
    session(64, "2026-07-30T16:40:00Z", "Friends newsletter landed. I only skimmed the video-hang options section.", "Not every mailer needs a decision."),
    session(65, "2026-07-31T18:05:00Z", "Logged a short voice rest note. Keeping reunion day protected.", "Recovery notes are worth tracking."),
    # S12
    session(66, "2026-08-02T19:15:00Z", "Restocked tea for the conversation-prep sprint. Solo evenings still matter.", "Prep routines are not one-size."),
    session(
        67,
        "2026-08-04T21:50:00Z",
        "Afternoon networking mixers wreck my evening listening focus for hours — short hellos are fine.",
        "Has the afternoon mixer pattern repeated?",
        "Yes. Three long mixers did it; short hellos did not.",
    ),
    session(68, "2026-08-06T12:30:00Z", "Short lunch away from the phone. Helped the afternoon.", "Breaks protect afternoon quality."),
    session(
        69,
        "2026-08-08T08:45:00Z",
        "Evening repair call Friday needs protected listening blocks Wednesday and Thursday.",
        "Is that slot movable?",
        "Not easily. The repair depends on it.",
    ),
    session(70, "2026-08-10T14:10:00Z", "Alumni chat is noisy about afternoon mixers. I muted the thread.", "Mute buttons save attention."),
    session(71, "2026-08-11T17:20:00Z", "Printed the August social calendar. Solo listening blocks are locked.", "Paper copies help on busy weeks."),
    # S13
    session(
        72,
        "2026-08-13T10:05:00Z",
        "Late-night party nights wreck my alertness for next-morning favors — early evenings have been fine.",
        "Has the late-night party pattern repeated?",
        "Yes. Three midnight parties did it; early evenings did not.",
    ),
    session(73, "2026-08-14T15:40:00Z", "Airport pickup checklist is printed for next week. Dawn windows are scarce.", "Favor prep has a timeline."),
    session(
        74,
        "2026-08-16T19:30:00Z",
        "Dawn airport pickup for a friend starts Monday — I need reliable morning alertness.",
        "Is that deadline firm?",
        "Yes. The pickup is already scheduled.",
    ),
    session(75, "2026-08-17T11:15:00Z", "Party chat posted a late-night invite. I filed it without replying.", "Invites can wait for a pickup plan."),
    session(76, "2026-08-18T16:50:00Z", "Marked dawn pickup windows on the checklist. Focus windows are the priority.", "Favor logistics are the priority."),
    # S14
    session(
        77,
        "2026-08-20T22:15:00Z",
        "Open-house hosting days destroy focus for careful friendship writing — quiet home blocks are fine.",
        "Was that a one-off?",
        "No. Twice on open-house days; quiet home blocks did not.",
    ),
    session(78, "2026-08-22T07:45:00Z", "Friendship letter outline is packed. Wednesday deadline is on the calendar.", "Letter weeks need protected writing blocks."),
    session(
        79,
        "2026-08-24T16:20:00Z",
        "Quiet friendship letter is due Wednesday and needs a deep writing block without open-house churn.",
        "Is that slot firm?",
        "Yes. It is already booked.",
    ),
    session(80, "2026-08-25T08:00:00Z", "Building forum is loud about open-house norms. I am not adopting forum defaults.", "Forum norms are not writing facts."),
    session(81, "2026-08-26T19:30:00Z", "Packed reference notes for the letter. Timing still feels tight.", "Writing timing matters on deadline weeks."),
    # S15
    session(
        82,
        "2026-08-28T18:10:00Z",
        "Weekend social-inbox blitzes bleed into protected personal planning blocks — weekday triage has been fine.",
        "Has that pattern repeated?",
        "Yes. Two weekend blitzes did it; weekday triage did not.",
    ),
    session(83, "2026-08-30T12:30:00Z", "Sunday family call week is on the calendar. Monday half-day recovery blocks are marked.", "Family-call context matters for boundaries."),
    session(
        84,
        "2026-09-01T09:40:00Z",
        "Sunday family call requires protected post-call recovery — I need a clean Monday half-day afterward.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(85, "2026-09-02T17:05:00Z", "Group chat sent another weekend inbox-blitz invite. I filed it without replying.", "Invites can wait for a family-call window."),
    session(86, "2026-09-03T07:20:00Z", "Set out the family-call checklist for Sunday. Protected recovery needs a clean routine.", "Family-call weeks need a clean routine."),
    # S16
    session(87, "2026-09-05T18:00:00Z", "Autumn social calendar is printed. Solo friendship-planning blocks are marked.", "Paper copies help on busy weeks."),
    session(
        88,
        "2026-09-07T20:45:00Z",
        "Noisy multi-friend hangouts wreck my careful friendship planning — quiet one-on-one blocks are fine.",
        "Has that pattern repeated?",
        "Yes. Twice on noisy hangout days; quiet one-on-ones did not.",
    ),
    session(89, "2026-09-08T13:10:00Z", "Short walk between errands. Nice reset.", "Small movement breaks add up."),
    session(
        90,
        "2026-09-10T08:30:00Z",
        "Friendship check-in planning week needs protected morning solo blocks Tuesday through Thursday — already on the calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(91, "2026-09-11T16:55:00Z", "Friends posted a standing hang-loop signup blurb. I filed it without replying.", "Invites can wait for a planning window."),
    # S17
    session(92, "2026-09-13T19:20:00Z", "Restocked stationery for the recommendation-letter sprint. Solo evenings still matter.", "Focus routines are not one-size."),
    session(
        93,
        "2026-09-15T21:10:00Z",
        "Full-day friend immersion leaves me too drained to finish my own careful notes — short coffee hours are fine.",
        "Has the full-day immersion pattern repeated?",
        "Yes. Three immersion days did it; short coffee hours did not.",
    ),
    session(94, "2026-09-16T12:40:00Z", "Short lunch away from the phone. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        95,
        "2026-09-18T08:50:00Z",
        "Recommendation letter due Friday needs three solo evening writing blocks — already on the calendar.",
        "Is that slot movable?",
        "Not easily. The letter depends on it.",
    ),
    session(96, "2026-09-19T14:25:00Z", "Group chat is noisy about immersion weeks. I muted the thread.", "Mute buttons save attention."),
    # S18
    session(97, "2026-09-21T10:05:00Z", "Printed the autumn social calendar. Solo prep blocks are marked.", "Prep weeks need a clean routine."),
    session(
        98,
        "2026-09-23T15:35:00Z",
        "Late-night social drinks after two o'clock give me jittery nights and ruin next-morning clarity — early evening tea is fine.",
        "Has the late-drink pattern repeated?",
        "Yes. Three late drink nights did it; early evening tea did not.",
    ),
    session(99, "2026-09-24T11:20:00Z", "Crew mailer landed. I filed it without replying.", "Invites can wait for a prep plan."),
    session(
        100,
        "2026-09-26T07:15:00Z",
        "Midweek hard-talk readiness needs a sharp morning clarity block — a late-slot obligation is already booked through the night before.",
        "Is that timing firm?",
        "Yes. The hard talk is already scheduled.",
    ),
    session(101, "2026-09-27T16:50:00Z", "Packed reference notes for the hard-talk lock. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S19
    session(102, "2026-09-29T18:15:00Z", "Toast outline is packed. Wednesday slot is on the calendar.", "Toast weeks need protected prep blocks."),
    session(
        103,
        "2026-10-01T22:00:00Z",
        "I prep best with private written notes — flipchart-only group prep sessions produce weak outputs for me.",
        "Has the flipchart-only pattern repeated?",
        "Yes. Twice on flipchart-only prep; private notes did not.",
    ),
    session(104, "2026-10-02T08:00:00Z", "Friend forum is loud about flipchart run-throughs. I am not adopting forum defaults.", "Forum norms are not prep facts."),
    session(
        105,
        "2026-10-04T16:30:00Z",
        "Prior flipchart-only toast rehearsal went poorly before the farewell dinner — I lost the thread twice.",
        "Harsh memory. Was the material unfamiliar?",
        "No. The format fought my process.",
    ),
    session(106, "2026-10-05T19:40:00Z", "Printed the toast calendar. Solo note-prep blocks are locked.", "Paper copies help on busy weeks."),
    # S20
    session(107, "2026-10-07T18:05:00Z", "Friend-meetup cadence memo landed. I only skimmed the transit-time section.", "Not every memo needs a decision."),
    session(
        108,
        "2026-10-09T07:50:00Z",
        "Long rush-hour transit for social visits drains my energy before careful talks start — short bike rides are fine.",
        "Has the long transit pattern repeated?",
        "Yes. Ninety-minute legs did it; short bike rides did not.",
    ),
    session(109, "2026-10-10T14:15:00Z", "Transit board posted a shuttle blurb. I filed it without replying.", "Invites can wait for an energy plan."),
    session(
        110,
        "2026-10-12T09:25:00Z",
        "New distant friend-meetup rhythm requires ninety-minute each-way transit on hangout days — already on the calendar.",
        "Is that timing firm?",
        "Yes. The meetup rhythm is already booked.",
    ),
    session(111, "2026-10-13T17:30:00Z", "Packed a light bag for the first distant-meetup day. Transit timing still feels heavy.", "Cadence changes need an energy plan."),
]


def monotonic_timeline(timeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Re-stamp sessions so timestamps strictly increase with session_id."""
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
        1: {"location": "Pittsburgh", "colleague_a": "Maya", "colleague_b": "Evan"},
        2: {"location": "Amsterdam", "colleague_a": "Sanne", "colleague_b": "Pieter"},
        3: {"location": "the city", "colleague_a": "Jules", "colleague_b": "Rina"},
        4: {"location": "the suburbs", "colleague_a": "Nora", "colleague_b": "Ben"},
        5: {"location": "downtown", "colleague_a": "Luis", "colleague_b": "Carmen"},
        6: {"location": "Berlin", "colleague_a": "Lena", "colleague_b": "Tobias"},
        7: {"location": "Austin", "colleague_a": "Chris", "colleague_b": "Sam"},
        8: {"location": "the hospital district", "colleague_a": "Priya", "colleague_b": "James"},
        9: {"location": "office campus", "colleague_a": "Helga", "colleague_b": "Karl"},
        10: {"location": "Ann Arbor", "colleague_a": "Mia", "colleague_b": "Leo"},
    }
    base = configs.get(idx, configs[3])
    trait = persona.get("stable_traits", ["social energy keeper"])[0]
    base["trait0"] = trait
    base["voice"] = persona.get("voice", "measured").split(",")[0]
    return base


def paint_session(s: dict[str, Any], paint: dict[str, str]) -> dict[str, Any]:
    sid = s["session_id"]
    dlg = deepcopy(s["dialogue"])
    if sid == 2 and paint.get("user_index", 1) != 1:
        dlg[0]["content"] = f"Social mode felt very '{paint['trait0']}' today — short replies, no drama."
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
            "name": "large_gathering_drain_x_roommate_quiet",
            "prefix_end": 9,
            "evidence": {
                "ev_A": {
                    "session_id": 4,
                    "fact": "Large noisy gatherings leave the user drained and snappy the next day; small dinners are fine.",
                },
                "ev_B": {
                    "session_id": 6,
                    "fact": "Roommate has early shifts this month and asked for quieter evenings at home.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-03-09T17:30:00Z",
            "query": "Worth accepting the heavier weekend hosting block — based on what you know about me?",
            "gold": (
                "Decline or renegotiate to a small dinner. Large noisy gatherings have left you drained and snappy the next day, "
                "and your roommate already needs quieter evenings at home during early-shift weeks. A heavier weekend hosting "
                "block conflicts with both patterns. The packed house mixer chatter is unrelated social noise."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Large gatherings have drained you, but I cannot "
                "tell from the available memory whether quieter evenings at home are currently required. Confirm household quiet "
                "constraints before accepting a heavier weekend hosting block."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your roommate needs quieter evenings "
                    "at home during early-shift weeks, but the available memory does not establish that large noisy gatherings drain "
                    "you. I cannot reject the hosting block from household rules alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Large gatherings have drained you, but I cannot "
                    "tell from the available memory whether quieter evenings at home are currently required. Confirm household quiet "
                    "constraints before accepting a heavier weekend hosting block."
                ),
            },
            "required": [
                "uses large-gathering drain pattern",
                "uses roommate quieter-evening constraint",
                "recommends declining or shrinking the heavier weekend hosting block",
            ],
            "absence_required": [
                "states that the roommate quiet-evening evidence is missing",
                "does not infer household harm from the hosting invite alone",
                "asks about quiet constraints or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the large-gathering drain evidence is missing",
                    "does not infer drain harm from the hosting invite alone",
                    "explicitly abstains from rejecting the hosting block",
                ],
                "ev_B": [
                    "states that the roommate quiet-evening evidence is missing",
                    "does not infer household harm from the hosting invite alone",
                    "asks about quiet constraints or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "post_gathering_drain", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "home_quiet_evenings", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "weekend_hosting_poor_fit", "hop": 2},
            ],
            "forbidden": ["never host friends", "social ban forever", "roommate conflict diagnosis"],
            "distractor": {
                "timestamp": "2026-02-20T11:00:00Z",
                "user": f"{ca} said accepting the heavier weekend hosting block is amazing hype and worth it for networking.",
                "assistant": "Networking hype and household capacity are different ledgers.",
                "why": "Weekend hosting FOMO shares query surface but is not evidence about this user's post-gathering drain or roommate quiet-evening constraint.",
            },
            "evolving": {"gathering_load": "large_noisy_drain", "household": "roommate_early_shift_quiet"},
        },
        "S2": {
            "name": "reply_storm_x_slow_checkin",
            "prefix_end": 16,
            "evidence": {
                "ev_A": {
                    "session_id": 11,
                    "fact": "Rapid group-chat reply storms leave the user anxious and snappy the next day; slow one-to-one threads are fine.",
                },
                "ev_B": {
                    "session_id": 13,
                    "fact": "Close friend needs a slow one-on-one call this week; not group logistics.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-04-10T17:05:00Z",
            "query": "Group wants me as the always-on reunion chat lead — sensible?",
            "gold": (
                "Decline the always-on reunion chat lead. Rapid group-chat reply storms have left you anxious and snappy the next "
                "day, and a close friend already needs a slow one-on-one call this week. Protect the check-in and defer always-on "
                "chat coordination."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Reply storms have hurt your next-day mood, but "
                "I cannot tell from the available memory whether a slow one-on-one check-in is already booked this week. Confirm "
                "that calendar before accepting chat-lead duty."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a slow one-on-one check-in is booked "
                    "this week, but the available memory does not establish that rapid reply storms leave you anxious. I cannot "
                    "reject the chat-lead role from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Reply storms have hurt your next-day mood, but "
                    "I cannot tell from the available memory whether a slow one-on-one check-in is already booked this week. Confirm "
                    "that calendar before accepting chat-lead duty."
                ),
            },
            "required": [
                "uses rapid reply-storm anxiety pattern",
                "uses slow one-on-one check-in need",
                "recommends declining always-on reunion chat lead",
            ],
            "absence_required": [
                "states that the one-on-one check-in evidence is missing",
                "does not infer harm from the chat-lead invite alone",
                "asks about check-in timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the reply-storm evidence is missing",
                    "does not infer mood harm from the role alone",
                    "explicitly abstains from rejecting the role",
                ],
                "ev_B": [
                    "states that the one-on-one check-in evidence is missing",
                    "does not infer harm from the chat-lead invite alone",
                    "asks about check-in timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "reply_storm_anxiety", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "slow_checkin_window", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "chat_lead_poor_fit", "hop": 2},
            ],
            "forbidden": ["phone ban forever", "must leave all group chats", "anxiety diagnosis"],
            "distractor": {
                "timestamp": "2026-04-07T09:30:00Z",
                "user": f"{cb} said being the always-on reunion chat lead is amazing hype and worth it for staying visible.",
                "assistant": "Visibility hype and reply-load capacity are different ledgers.",
                "why": "Chat-lead FOMO shares query surface but is not evidence about this user's reply-storm pattern or slow check-in need.",
            },
            "evolving": {"messaging_load": "reply_storm_anxiety", "friend_need": "slow_one_on_one_checkin"},
        },
        "S3": {
            "name": "coffee_stack_x_repair_talk",
            "prefix_end": 24,
            "evidence": {
                "ev_A": {
                    "session_id": 18,
                    "fact": "Stacking more than two social coffee hangs in one day leaves the user hollow by evening.",
                },
                "ev_B": {
                    "session_id": 20,
                    "fact": "Thursday repair conversation with a friend needs the user's full presence.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-12T18:45:00Z",
            "query": "Calendar is filling with midweek catch-ups before Thursday's hard talk — worth stacking them?",
            "gold": (
                "Do not stack more than one or two midweek catch-ups. More than two social coffee hangs in a day have left you "
                "hollow by evening, and Thursday's repair conversation already needs your full presence. Protect that block; "
                "defer extra catch-ups."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether stacking midweek catch-ups fits. Coffee stacking has left you "
                "hollow, but I cannot tell from the available memory whether Thursday's hard talk needs protected presence. "
                "Confirm that block before packing the calendar."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Thursday's repair conversation needs "
                    "your full presence, but the available memory does not establish that stacking coffee hangs leaves you hollow. "
                    "I cannot reject the catch-ups from one meeting alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether stacking midweek catch-ups fits. Coffee stacking has left you "
                    "hollow, but I cannot tell from the available memory whether Thursday's hard talk needs protected presence. "
                    "Confirm that block before packing the calendar."
                ),
            },
            "required": [
                "uses coffee-hang stacking hollow pattern",
                "uses Thursday repair-talk presence need",
                "recommends against stacking midweek catch-ups before the hard talk",
            ],
            "absence_required": [
                "states that the repair-talk presence evidence is missing",
                "does not infer harm from the catch-up invites alone",
                "asks about Thursday timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the coffee-stacking evidence is missing",
                    "does not infer hollow harm from the invites alone",
                    "explicitly abstains from rejecting the catch-ups",
                ],
                "ev_B": [
                    "states that the repair-talk presence evidence is missing",
                    "does not infer harm from the catch-up invites alone",
                    "asks about Thursday timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "coffee_stack_hollow", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "repair_talk_presence", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "catchup_stack_poor_fit", "hop": 2},
            ],
            "forbidden": ["never meet friends", "coffee ban forever", "relationship diagnosis"],
            "distractor": {
                "timestamp": "2026-05-10T14:00:00Z",
                "user": f"{ca} said stacking midweek catch-ups before Thursday's hard talk is amazing for staying socially warm.",
                "assistant": "Warmth talk and presence capacity are different ledgers.",
                "why": "Catch-up stacking FOMO shares query surface but is not evidence about this user's hollow pattern or repair-talk presence need.",
            },
            "evolving": {"social_stacking": "coffee_hang_hollow", "repair_talk": "thursday_presence_protected"},
        },
        "S4": {
            "name": "public_shoutout_freeze_x_prior_fail",
            "prefix_end": 28,
            "evidence": {
                "ev_A": {
                    "session_id": 25,
                    "fact": "The user freezes when put on the spot for public compliments in group settings; private notes work better.",
                },
                "ev_B": {
                    "session_id": 27,
                    "fact": "A prior live shoutout round at a group dinner went poorly; the user blanked and felt awkward for hours.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-23T17:20:00Z",
            "query": "Host wants me to do a live recognition round at the dinner — good fit?",
            "gold": (
                "Decline the live recognition round or offer a private-note alternative. You freeze when put on the spot for "
                "public compliments, and a prior live shoutout round already went poorly. Private notes fit your process better."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a live recognition round fits. Public compliments have caused "
                "you to freeze, but I cannot tell from the available memory whether a prior live shoutout failed. Confirm that "
                "track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior live shoutout round went "
                    "poorly, but the available memory does not establish that you freeze on public compliments. I cannot reject "
                    "the round from one bad night alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a live recognition round fits. Public compliments have caused "
                    "you to freeze, but I cannot tell from the available memory whether a prior live shoutout failed. Confirm that "
                    "track record before volunteering."
                ),
            },
            "required": [
                "uses public-compliment freeze pattern",
                "uses prior live shoutout failure",
                "recommends declining live recognition round or shifting to private notes",
            ],
            "absence_required": [
                "states that the prior shoutout-failure evidence is missing",
                "does not infer format mismatch from the host invite alone",
                "asks about shoutout track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the public-compliment freeze evidence is missing",
                    "does not infer freeze harm from the invite alone",
                    "explicitly abstains from rejecting the round",
                ],
                "ev_B": [
                    "states that the prior shoutout-failure evidence is missing",
                    "does not infer format mismatch from the host invite alone",
                    "asks about shoutout track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "public_compliment_freeze", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "live_shoutout_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "live_recognition_poor_fit", "hop": 2},
            ],
            "forbidden": ["social anxiety diagnosis", "never speak in groups", "praise ban forever"],
            "distractor": {
                "timestamp": "2026-05-10T14:30:00Z",
                "user": f"A friend said a live recognition round at the dinner is amazing hype and everyone will love the warmth.",
                "assistant": "Warmth marketing and format fit are different questions.",
                "why": "Live recognition FOMO shares query surface but is not evidence about this user's public-compliment freeze or prior shoutout failure.",
            },
            "evolving": {"recognition_format": "private_notes_preferred", "live_shoutout": "prior_fail"},
        },
        "S5": {
            "name": "solo_saturday_x_family_visit",
            "prefix_end": 32,
            "evidence": {
                "ev_A": {
                    "session_id": 29,
                    "fact": "Solo Saturday mornings are how the user recovers from a social week; skipping them leaves them flat through Monday.",
                },
                "ev_B": {
                    "session_id": 31,
                    "fact": "Family visit is already booked through Saturday afternoon; morning alone time that day is gone.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-02T19:30:00Z",
            "query": "Worth accepting the heavier neighborhood morning block this weekend — based on what you know about me?",
            "gold": (
                "Decline the heavier neighborhood morning block this weekend. Solo Saturday mornings are your recovery block, and "
                "family visit is already booked through Saturday afternoon so that alone time is already gone. Protect whatever "
                "recharge remains; do not add another morning group plan."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Solo Saturday mornings matter for your recovery, "
                "but I cannot tell from the available memory whether a family visit already removes this Saturday morning. Confirm "
                "that calendar before accepting the neighborhood morning block."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a family visit already books through "
                    "Saturday afternoon, but the available memory does not establish that solo Saturday mornings are your recovery "
                    "block. I cannot reject the morning block from family logistics alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Solo Saturday mornings matter for your recovery, "
                    "but I cannot tell from the available memory whether a family visit already removes this Saturday morning. Confirm "
                    "that calendar before accepting the neighborhood morning block."
                ),
            },
            "required": [
                "uses solo Saturday morning recovery need",
                "uses family visit removing Saturday morning alone time",
                "recommends declining heavier neighborhood morning block this weekend",
            ],
            "absence_required": [
                "states that the family-visit Saturday evidence is missing",
                "does not infer calendar harm from the morning-block invite alone",
                "asks about Saturday logistics or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the solo-Saturday recovery evidence is missing",
                    "does not infer recovery harm from the invite alone",
                    "explicitly abstains from rejecting the morning block",
                ],
                "ev_B": [
                    "states that the family-visit Saturday evidence is missing",
                    "does not infer calendar harm from the morning-block invite alone",
                    "asks about Saturday logistics or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "solo_saturday_recharge", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "saturday_alone_time", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "morning_block_poor_fit", "hop": 2},
            ],
            "forbidden": ["never brunch", "family ban", "isolation prescription"],
            "distractor": {
                "timestamp": "2026-05-28T09:30:00Z",
                "user": f"{cb} said accepting the heavier neighborhood morning block this weekend is amazing hype and worth it for bonding.",
                "assistant": "Neighborhood bonding and recovery blocks are different ledgers.",
                "why": "Morning-block FOMO shares query surface but is not evidence about this user's solo Saturday recovery need or family-visit constraint.",
            },
            "evolving": {"saturday_recharge": "solo_morning_required", "family_visit": "saturday_afternoon_booked"},
        },
        "S6": {
            "name": "late_group_dinner_x_early_bike_ride",
            "prefix_end": 38,
            "evidence": {
                "ev_A": {
                    "session_id": 34,
                    "fact": "Multi-hour group dinners past eleven leave the user socially flat the next morning; short two-hour dinners are fine.",
                },
                "ev_B": {
                    "session_id": 36,
                    "fact": "Promised a friend an early Saturday bike ride; needs solid prior-night energy.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-15T17:10:00Z",
            "query": "Friends floated a seated supper that stretches past bedtime tonight — based on what you know about me?",
            "gold": (
                "Decline the seated supper that stretches past bedtime tonight. Multi-hour group dinners past eleven have left you socially "
                "flat the next morning, and you already promised an early Saturday bike ride that needs solid prior-night energy. "
                "Choose a short dinner or defer until after the ride."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Late long dinners have flattened your next morning, "
                "but I cannot tell from the available memory whether an early Saturday ride is already promised. Confirm that plan "
                "before accepting a late table."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know an early Saturday bike ride is promised, "
                    "but the available memory does not establish that late multi-hour dinners flatten your next morning. I cannot "
                    "reject the table from the ride alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Late long dinners have flattened your next morning, "
                    "but I cannot tell from the available memory whether an early Saturday ride is already promised. Confirm that plan "
                    "before accepting a late table."
                ),
            },
            "required": [
                "uses late multi-hour dinner next-morning flatness",
                "uses early Saturday bike-ride energy need",
                "recommends declining late multi-course group table",
            ],
            "absence_required": [
                "states that the early-ride evidence is missing",
                "does not infer harm from the table invite alone",
                "asks about Saturday plans or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-dinner flatness evidence is missing",
                    "does not infer energy harm from the invite alone",
                    "explicitly abstains from rejecting the table",
                ],
                "ev_B": [
                    "states that the early-ride evidence is missing",
                    "does not infer harm from the table invite alone",
                    "asks about Saturday plans or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_dinner_next_morning_flat", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "early_ride_energy", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "late_table_poor_fit", "hop": 2},
            ],
            "forbidden": ["never dine out", "friendship ban", "must cancel all rides"],
            "distractor": {
                "timestamp": "2026-06-12T09:15:00Z",
                "user": f"{ca} said a seated supper that stretches past bedtime tonight is amazing hype and worth it for staying socially warm.",
                "assistant": "Warmth hype and next-morning energy are different ledgers.",
                "why": "Late-supper FOMO shares query surface but is not evidence about this user's late-dinner flatness or early-ride energy need.",
            },
            "evolving": {"late_dinner": "next_morning_flat", "saturday_ride": "needs_prior_night_energy"},
        },
        "S7": {
            "name": "dropin_wreck_x_tuesday_sibling_checkin",
            "prefix_end": 44,
            "evidence": {
                "ev_A": {
                    "session_id": 40,
                    "fact": "Unannounced drop-in visits wreck the user's evening wind-down for hours; planned visits are fine.",
                },
                "ev_B": {
                    "session_id": 42,
                    "fact": "Weekly Tuesday evening listening check-in with sibling is already protected.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-26T18:20:00Z",
            "query": "Neighbor keeps floating spontaneous evening pop-ins on Tuesdays — keep saying yes?",
            "gold": (
                "Decline Tuesday spontaneous pop-ins. Unannounced drop-ins wreck your evening wind-down, and Tuesday evening "
                "listening check-in with your sibling is already protected. Keep planned visits; push back on surprise Tuesday pop-ins."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether Tuesday pop-ins fit. Drop-ins have wrecked your wind-down, but "
                "I cannot tell from the available memory whether a Tuesday sibling check-in is already protected. Confirm that "
                "calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a Tuesday sibling check-in is protected, "
                    "but the available memory does not establish that unannounced drop-ins wreck your wind-down. I cannot reject "
                    "pop-ins from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether Tuesday pop-ins fit. Drop-ins have wrecked your wind-down, but "
                    "I cannot tell from the available memory whether a Tuesday sibling check-in is already protected. Confirm that "
                    "calendar before deciding."
                ),
            },
            "required": [
                "uses unannounced drop-in wind-down wreck pattern",
                "uses protected Tuesday sibling check-in",
                "recommends declining Tuesday spontaneous pop-ins",
            ],
            "absence_required": [
                "states that the Tuesday check-in evidence is missing",
                "does not infer harm from the pop-in invite alone",
                "asks about Tuesday calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the drop-in wind-down evidence is missing",
                    "does not infer evening harm from the invite alone",
                    "explicitly abstains from rejecting pop-ins",
                ],
                "ev_B": [
                    "states that the Tuesday check-in evidence is missing",
                    "does not infer harm from the pop-in invite alone",
                    "asks about Tuesday calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "dropin_winddown_wreck", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "tuesday_sibling_checkin", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "tuesday_popin_poor_fit", "hop": 2},
            ],
            "forbidden": ["never host neighbors", "family ban", "must cancel all visits"],
            "distractor": {
                "timestamp": "2026-06-23T11:00:00Z",
                "user": f"{cb} said spontaneous Tuesday evening pop-ins are amazing hype and worth saying yes every time for neighbor warmth.",
                "assistant": "Neighbor warmth and protected check-ins are different ledgers.",
                "why": "Pop-in FOMO shares query surface but is not evidence about this user's drop-in wind-down pattern or Tuesday sibling check-in.",
            },
            "evolving": {"dropins": "wreck_evening_winddown", "tuesday_block": "sibling_listening_checkin"},
        },
        "S8": {
            "name": "private_thanks_x_live_gift_speech",
            "prefix_end": 49,
            "evidence": {
                "ev_A": {
                    "session_id": 45,
                    "fact": "The user is best at private written thanks, not on-the-spot group gift speeches.",
                },
                "ev_B": {
                    "session_id": 47,
                    "fact": "A prior live group gift toast went poorly; the user blanked and felt awkward for days.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-05T16:30:00Z",
            "query": "They want me to deliver the on-the-spot goodbye tribute — good fit?",
            "gold": (
                "Decline delivering the on-the-spot goodbye tribute or offer a private-note alternative. You are best at private written thanks, "
                "and a prior live group gift toast already went poorly. Private notes fit your process better."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether leading a live gift speech fits. Private written thanks work for you, "
                "but I cannot tell from the available memory whether a prior live toast failed. Confirm that track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior live gift toast went poorly, "
                    "but the available memory does not establish that private written thanks are your strongest format. I cannot "
                    "reject the speech from one bad night alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether leading a live gift speech fits. Private written thanks work for you, "
                    "but I cannot tell from the available memory whether a prior live toast failed. Confirm that track record before volunteering."
                ),
            },
            "required": [
                "uses private written-thanks preference",
                "uses prior live gift-toast failure",
                "recommends declining live gift speech or shifting to private notes",
            ],
            "absence_required": [
                "states that the prior live-toast failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about live-toast track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the private-thanks preference evidence is missing",
                    "does not infer format harm from the speech alone",
                    "explicitly abstains from rejecting the speech",
                ],
                "ev_B": [
                    "states that the prior live-toast failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about live-toast track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "private_thanks_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "live_gift_toast_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "live_gift_speech_poor_fit", "hop": 2},
            ],
            "forbidden": ["never speak in groups", "gift ban forever", "social anxiety diagnosis"],
            "distractor": {
                "timestamp": "2026-07-03T14:00:00Z",
                "user": f"{ca} said delivering the on-the-spot goodbye tribute is amazing hype and everyone will love the warmth.",
                "assistant": "Warmth marketing and format fit are different questions.",
                "why": "Goodbye-tribute FOMO shares query surface but is not evidence about this user's private-thanks preference or prior toast failure.",
            },
            "evolving": {"thanks_format": "private_written", "live_toast": "prior_fail"},
        },
        "S9": {
            "name": "overnight_host_fatigue_x_monday_mentoring",
            "prefix_end": 54,
            "evidence": {
                "ev_A": {
                    "session_id": 50,
                    "fact": "Overnight guests leave the user cognitively and socially flat through the next full day.",
                },
                "ev_B": {
                    "session_id": 52,
                    "fact": "One-on-one mentoring coffee is locked Monday 10am right after the weekend.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-12T20:45:00Z",
            "query": "Someone asked to stay the night before my Monday coaching slot — based on what you know about me?",
            "gold": (
                "Do not host an overnight stay the night before Monday's coaching slot. Overnight hosting has left you flat through the next "
                "full day, and Monday 10am mentoring coffee is already locked. Choose a daytime visit or move hosting after mentoring week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether Sunday overnight hosting fits. Overnight guests have flattened your "
                "next day, but I cannot tell from the available memory whether Monday mentoring is already locked. Confirm that "
                "calendar before hosting overnight."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Monday mentoring coffee is locked at 10am, "
                    "but the available memory does not establish that overnight guests flatten your next day. I cannot reject hosting "
                    "from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether Sunday overnight hosting fits. Overnight guests have flattened your "
                    "next day, but I cannot tell from the available memory whether Monday mentoring is already locked. Confirm that "
                    "calendar before hosting overnight."
                ),
            },
            "required": [
                "uses overnight-guest next-day flatness",
                "uses Monday mentoring coffee lock",
                "recommends against overnight stay before Monday coaching slot",
            ],
            "absence_required": [
                "states that the Monday mentoring evidence is missing",
                "does not infer harm from the hosting invite alone",
                "asks about Monday calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the overnight-guest flatness evidence is missing",
                    "does not infer next-day harm from hosting alone",
                    "explicitly abstains from rejecting overnight hosting",
                ],
                "ev_B": [
                    "states that the Monday mentoring evidence is missing",
                    "does not infer harm from the hosting invite alone",
                    "asks about Monday calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "overnight_host_next_day_flat", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_mentoring_presence", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "sunday_overnight_poor_fit", "hop": 2},
            ],
            "forbidden": ["never host overnight", "mentoring ban", "must cancel all guests"],
            "distractor": {
                "timestamp": "2026-07-09T11:00:00Z",
                "user": f"{cb} said staying the night before Monday's coaching slot is amazing hype and worth it for hospitality points.",
                "assistant": "Hospitality hype and Monday presence are different ledgers.",
                "why": "Overnight-stay FOMO shares query surface but is not evidence about this user's next-day flatness or Monday mentoring lock.",
            },
            "evolving": {"overnight_hosting": "next_day_flat", "monday_mentoring": "10am_locked"},
        },
        "S10": {
            "name": "status_ping_churn_x_friend_letter",
            "prefix_end": 59,
            "evidence": {
                "ev_A": {
                    "session_id": 55,
                    "fact": "Constant status-update pings during evenings kill the user's presence for real conversations.",
                },
                "ev_B": {
                    "session_id": 57,
                    "fact": "A careful letter to a distant friend needs an uninterrupted evening without ping churn.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-21T06:50:00Z",
            "query": "Thread wants me on a continuous presence roster all week — worth it?",
            "gold": (
                "Decline the continuous presence roster this week. Constant evening status pings kill your presence for real "
                "conversations, and a careful letter to a distant friend already needs an uninterrupted evening. Protect the letter "
                "block; defer always-on status duty."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Status pings have hurt your evening presence, but "
                "I cannot tell from the available memory whether a letter evening is already protected. Confirm that block before "
                "accepting always-on status duty."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a careful letter evening is protected, "
                    "but the available memory does not establish that status pings kill your presence. I cannot reject the roster "
                    "from the letter alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Status pings have hurt your evening presence, but "
                    "I cannot tell from the available memory whether a letter evening is already protected. Confirm that block before "
                    "accepting always-on status duty."
                ),
            },
            "required": [
                "uses evening status-ping presence damage",
                "uses protected letter evening need",
                "recommends declining always-on status-update roster",
            ],
            "absence_required": [
                "states that the letter-evening evidence is missing",
                "does not infer harm from the status roster alone",
                "asks about letter timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the status-ping presence evidence is missing",
                    "does not infer presence harm from the roster alone",
                    "explicitly abstains from rejecting the roster",
                ],
                "ev_B": [
                    "states that the letter-evening evidence is missing",
                    "does not infer harm from the status roster alone",
                    "asks about letter timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "status_ping_presence_loss", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "letter_evening_focus", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "status_roster_poor_fit", "hop": 2},
            ],
            "forbidden": ["phone ban forever", "must leave all chats", "never write letters"],
            "distractor": {
                "timestamp": "2026-07-18T09:30:00Z",
                "user": f"{ca} said a continuous presence roster all week is amazing hype and worth it for staying visible.",
                "assistant": "Visibility hype and letter presence are different ledgers.",
                "why": "Presence-roster FOMO shares query surface but is not evidence about this user's ping presence damage or letter-evening need.",
            },
            "evolving": {"status_pings": "kill_evening_presence", "friend_letter": "needs_uninterrupted_evening"},
        },
        "S11": {
            "name": "stacked_video_hangs_x_reunion_lunch",
            "prefix_end": 65,
            "evidence": {
                "ev_A": {
                    "session_id": 61,
                    "fact": "Back-to-back video hangouts leave the user's voice and presence thin for next-day in-person talks.",
                },
                "ev_B": {
                    "session_id": 63,
                    "fact": "In-person reunion lunch Thursday at noon is a hard calendar boundary.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-01T10:30:00Z",
            "query": "Worth stacking more lens-on hangouts before Thursday's in-person reunion?",
            "gold": (
                "Stop stacking more lens-on hangouts before Thursday. Back-to-back video hangouts leave your voice and presence thin "
                "for next-day in-person talks, and Thursday reunion lunch is already a hard boundary. Keep at most one short call; "
                "protect reunion presence."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether stacking video hangs fits. Video stacks have thinned your next-day "
                "presence, but I cannot tell from the available memory whether Thursday reunion lunch is already locked. Confirm "
                "that calendar before adding more hangs."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Thursday reunion lunch is locked, but "
                    "the available memory does not establish that stacked video hangs thin your next-day presence. I cannot reject "
                    "the hangs from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether stacking video hangs fits. Video stacks have thinned your next-day "
                    "presence, but I cannot tell from the available memory whether Thursday reunion lunch is already locked. Confirm "
                    "that calendar before adding more hangs."
                ),
            },
            "required": [
                "uses stacked video-hang next-day thin presence",
                "uses Thursday reunion lunch lock",
                "recommends against adding more video hangs before reunion",
            ],
            "absence_required": [
                "states that the reunion-lunch evidence is missing",
                "does not infer harm from the video-hang invites alone",
                "asks about Thursday timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the stacked-video presence evidence is missing",
                    "does not infer presence harm from the invites alone",
                    "explicitly abstains from rejecting the hangs",
                ],
                "ev_B": [
                    "states that the reunion-lunch evidence is missing",
                    "does not infer harm from the video-hang invites alone",
                    "asks about Thursday timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "stacked_video_thin_presence", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "thursday_reunion_presence", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pre_reunion_video_stack_poor_fit", "hop": 2},
            ],
            "forbidden": ["never video call", "reunion ban", "must cancel all hangs"],
            "distractor": {
                "timestamp": "2026-07-29T14:00:00Z",
                "user": f"{cb} said stacking more lens-on hangouts before Thursday's in-person reunion is amazing for staying warm with the group.",
                "assistant": "Warmth talk and reunion presence are different ledgers.",
                "why": "Lens-on stack FOMO shares query surface but is not evidence about this user's thin-presence pattern or Thursday reunion lock.",
            },
            "evolving": {"video_stacks": "thin_next_day_presence", "reunion_lunch": "thursday_locked"},
        },
        "S12": {
            "name": "afternoon_mixer_x_evening_repair",
            "prefix_end": 71,
            "evidence": {
                "ev_A": {
                    "session_id": 67,
                    "fact": "Afternoon networking mixers wreck the user's evening listening focus for hours; short hellos are fine.",
                },
                "ev_B": {
                    "session_id": 69,
                    "fact": "Evening repair call Friday needs protected listening blocks Wednesday and Thursday.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-12T18:20:00Z",
            "query": "Worth taking a long hallway networking block before Friday's hard talk?",
            "gold": (
                "Decline the long hallway networking block before Friday. Afternoon networking mixers wreck your evening listening focus, "
                "and Friday's repair call already needs protected Wednesday and Thursday listening blocks. Keep short hellos only."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a long afternoon mixer fits. Mixers have wrecked your evening "
                "listening, but I cannot tell from the available memory whether Friday's repair call needs protected blocks. Confirm "
                "that calendar before accepting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Friday's repair call needs protected "
                    "listening blocks, but the available memory does not establish that afternoon mixers wreck your evening focus. "
                    "I cannot reject the mixer from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a long afternoon mixer fits. Mixers have wrecked your evening "
                    "listening, but I cannot tell from the available memory whether Friday's repair call needs protected blocks. Confirm "
                    "that calendar before accepting."
                ),
            },
            "required": [
                "uses afternoon mixer evening-listening wreck pattern",
                "uses Friday repair-call protected listening need",
                "recommends declining long afternoon mixer before the hard talk",
            ],
            "absence_required": [
                "states that the repair-call evidence is missing",
                "does not infer harm from the mixer invite alone",
                "asks about Friday timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the afternoon-mixer listening evidence is missing",
                    "does not infer listening harm from the invite alone",
                    "explicitly abstains from rejecting the mixer",
                ],
                "ev_B": [
                    "states that the repair-call evidence is missing",
                    "does not infer harm from the mixer invite alone",
                    "asks about Friday timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "mixer_evening_listening_wreck", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "repair_call_listening_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pre_repair_mixer_poor_fit", "hop": 2},
            ],
            "forbidden": ["never network", "repair ban", "must skip all alumni events"],
            "distractor": {
                "timestamp": "2026-08-09T16:00:00Z",
                "user": f"{ca} said a long hallway networking block before Friday's hard talk is amazing for alumni warmth.",
                "assistant": "Alumni warmth and repair listening are different ledgers.",
                "why": "Hallway-networking FOMO shares query surface but is not evidence about this user's evening-listening wreck pattern or Friday repair-call need.",
            },
            "evolving": {"afternoon_mixers": "wreck_evening_listening", "repair_call": "friday_protected"},
        },
        "S13": {
            "name": "late_party_x_dawn_airport_pickup",
            "prefix_end": 76,
            "evidence": {
                "ev_A": {
                    "session_id": 72,
                    "fact": "Late-night party nights wreck the user's alertness for next-morning favors; early evenings have been fine.",
                },
                "ev_B": {
                    "session_id": 74,
                    "fact": "Dawn airport pickup for a friend starts Monday; needs reliable morning alertness.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-19T09:15:00Z",
            "query": "Crew added a midnight send-off before Monday's airport favor — sensible?",
            "gold": (
                "Skip the midnight send-off before Monday. Late-night party nights wreck your next-morning alertness, and a dawn "
                "airport pickup for a friend already needs reliable Monday morning energy. Choose an early evening or defer until "
                "after the pickup."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a midnight send-off fits. Late parties have wrecked your next-morning "
                "alertness, but I cannot tell from the available memory whether a dawn airport pickup is already scheduled. Confirm "
                "that favor before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a dawn airport pickup is scheduled Monday, "
                    "but the available memory does not establish that late-night parties wreck your next-morning alertness. I cannot "
                    "reject the send-off from the pickup alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a midnight send-off fits. Late parties have wrecked your next-morning "
                    "alertness, but I cannot tell from the available memory whether a dawn airport pickup is already scheduled. Confirm "
                    "that favor before deciding."
                ),
            },
            "required": [
                "uses late-party next-morning alertness wreck",
                "uses dawn airport-pickup Monday need",
                "recommends skipping midnight send-off before the pickup",
            ],
            "absence_required": [
                "states that the airport-pickup evidence is missing",
                "does not infer harm from the party invite alone",
                "asks about Monday pickup timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-party alertness evidence is missing",
                    "does not infer alertness harm from the invite alone",
                    "explicitly abstains from rejecting the send-off",
                ],
                "ev_B": [
                    "states that the airport-pickup evidence is missing",
                    "does not infer harm from the party invite alone",
                    "asks about Monday pickup timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_party_morning_alert_loss", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dawn_pickup_alertness", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "midnight_sendoff_poor_fit", "hop": 2},
            ],
            "forbidden": ["never party", "favor ban", "must cancel all nights out"],
            "distractor": {
                "timestamp": "2026-08-16T20:00:00Z",
                "user": f"{cb} said a midnight send-off before Monday's airport favor is amazing hype and worth it for crew loyalty.",
                "assistant": "Crew loyalty and dawn alertness are different ledgers.",
                "why": "Midnight send-off FOMO shares query surface but is not evidence about this user's late-party alertness pattern or dawn pickup need.",
            },
            "evolving": {"late_parties": "wreck_morning_alertness", "dawn_pickup": "monday_locked"},
        },
        "S14": {
            "name": "open_house_x_friendship_letter",
            "prefix_end": 81,
            "evidence": {
                "ev_A": {
                    "session_id": 77,
                    "fact": "Open-house hosting days destroy focus for careful friendship writing; quiet home blocks are fine.",
                },
                "ev_B": {
                    "session_id": 79,
                    "fact": "Quiet friendship letter is due Wednesday and needs a deep writing block without open-house churn.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-27T06:50:00Z",
            "query": "Building asked me to staff a walk-through hosting block midweek — workable with my writing week?",
            "gold": (
                "Decline the midweek walk-through hosting block. Open-house days destroy focus for careful friendship writing, and "
                "your quiet friendship letter is due Wednesday with a deep writing block already needed. Protect the letter week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether midweek open-house hosting fits. Open-house days have wrecked "
                "your writing focus, but I cannot tell from the available memory whether a friendship letter is due Wednesday. "
                "Confirm that deadline before accepting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a friendship letter is due Wednesday, "
                    "but the available memory does not establish that open-house hosting destroys writing focus. I cannot reject "
                    "the slot from the deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether midweek open-house hosting fits. Open-house days have wrecked "
                    "your writing focus, but I cannot tell from the available memory whether a friendship letter is due Wednesday. "
                    "Confirm that deadline before accepting."
                ),
            },
            "required": [
                "uses open-house hosting writing-focus wreck",
                "uses Wednesday friendship-letter deadline",
                "recommends declining midweek open-house hosting slot",
            ],
            "absence_required": [
                "states that the friendship-letter deadline evidence is missing",
                "does not infer harm from the hosting invite alone",
                "asks about letter timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the open-house writing-focus evidence is missing",
                    "does not infer writing harm from the slot alone",
                    "explicitly abstains from rejecting the hosting slot",
                ],
                "ev_B": [
                    "states that the friendship-letter deadline evidence is missing",
                    "does not infer harm from the hosting invite alone",
                    "asks about letter timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "open_house_writing_wreck", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "friendship_letter_deadline", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "midweek_open_house_poor_fit", "hop": 2},
            ],
            "forbidden": ["never host building events", "letter ban", "must skip all open houses"],
            "distractor": {
                "timestamp": "2026-08-24T12:00:00Z",
                "user": f"{ca} said a midweek walk-through hosting block during writing week is amazing for building goodwill.",
                "assistant": "Building goodwill and letter focus are different ledgers.",
                "why": "Walk-through hosting FOMO shares query surface but is not evidence about this user's writing-focus wreck pattern or Wednesday letter deadline.",
            },
            "evolving": {"open_house": "wrecks_writing_focus", "friendship_letter": "wednesday_deadline"},
        },
        "S15": {
            "name": "weekend_inbox_blitz_x_family_call",
            "prefix_end": 86,
            "evidence": {
                "ev_A": {
                    "session_id": 82,
                    "fact": "Weekend social-inbox blitzes bleed into protected personal planning blocks; weekday triage has been fine.",
                },
                "ev_B": {
                    "session_id": 84,
                    "fact": "Sunday family call requires protected post-call recovery with a clean Monday half-day afterward.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-04T20:45:00Z",
            "query": "Thread wants a Saturday message catch-up blitz before Sunday's family call — workable?",
            "gold": (
                "Decline the Saturday message catch-up blitz before Sunday's family call. Weekend inbox blitzes bleed into protected "
                "planning blocks, and Sunday family call already needs protected post-call recovery with a clean Monday half-day. "
                "Keep weekday triage only."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a weekend inbox blitz fits. Weekend blitzes have bled into your "
                "planning blocks, but I cannot tell from the available memory whether Sunday family call needs protected recovery. "
                "Confirm that calendar before accepting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Sunday family call needs protected "
                    "recovery, but the available memory does not establish that weekend inbox blitzes bleed into planning blocks. "
                    "I cannot reject the blitz from family-call timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a weekend inbox blitz fits. Weekend blitzes have bled into your "
                    "planning blocks, but I cannot tell from the available memory whether Sunday family call needs protected recovery. "
                    "Confirm that calendar before accepting."
                ),
            },
            "required": [
                "uses weekend inbox-blitz planning bleed pattern",
                "uses Sunday family-call recovery need",
                "recommends declining weekend social-inbox blitz before family call",
            ],
            "absence_required": [
                "states that the family-call recovery evidence is missing",
                "does not infer harm from the blitz invite alone",
                "asks about Sunday timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the weekend-blitz bleed evidence is missing",
                    "does not infer planning harm from the invite alone",
                    "explicitly abstains from rejecting the blitz",
                ],
                "ev_B": [
                    "states that the family-call recovery evidence is missing",
                    "does not infer harm from the blitz invite alone",
                    "asks about Sunday timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "weekend_blitz_planning_bleed", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "family_call_recovery", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pre_family_call_blitz_poor_fit", "hop": 2},
            ],
            "forbidden": ["never check messages", "family ban", "must cancel all weekends"],
            "distractor": {
                "timestamp": "2026-09-01T15:00:00Z",
                "user": f"{cb} said a Saturday message catch-up blitz before Sunday's family call is amazing for staying caught up with everyone.",
                "assistant": "Catch-up hype and family-call recovery are different ledgers.",
                "why": "Catch-up-blitz FOMO shares query surface but is not evidence about this user's weekend-bleed pattern or family-call recovery need.",
            },
            "evolving": {"weekend_blitz": "bleeds_planning_blocks", "family_call": "needs_monday_recovery"},
        },
        "S16": {
            "name": "noisy_hangout_x_friendship_planning",
            "prefix_end": 91,
            "evidence": {
                "ev_A": {
                    "session_id": 88,
                    "fact": "Noisy multi-friend hangouts wreck the user's careful friendship planning; quiet one-on-one blocks are fine.",
                },
                "ev_B": {
                    "session_id": 90,
                    "fact": "Friendship check-in planning week needs protected morning solo blocks Tuesday through Thursday.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-12T10:15:00Z",
            "query": "Worth trying the standing hang loop before Thursday's friendship check-in lock?",
            "gold": (
                "Skip the standing hang loop before Thursday's friendship check-in lock. Noisy multi-friend hangouts have "
                "wrecked your careful friendship planning, and planning week needs protected morning solo blocks Tuesday "
                "through Thursday. Use quiet one-on-ones or defer the hang loop until after the lock."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the standing hang loop fits before Thursday's check-in lock. "
                "Noisy hangouts have wrecked your planning focus, but I cannot tell from the available memory whether Tuesday "
                "through Thursday morning solo blocks are already protected. Confirm the check-in calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know friendship check-in planning week "
                    "needs protected morning solo blocks Tuesday through Thursday, but the available memory does not establish "
                    "that noisy hangouts wreck your planning focus. I cannot reject the hang loop from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the standing hang loop fits before Thursday's check-in lock. "
                    "Noisy hangouts have wrecked your planning focus, but I cannot tell from the available memory whether Tuesday "
                    "through Thursday morning solo blocks are already protected. Confirm the check-in calendar before deciding."
                ),
            },
            "required": [
                "uses noisy hangout wrecking friendship planning",
                "uses check-in planning week needing protected morning solo blocks",
                "recommends skipping standing hang loop before check-in lock",
            ],
            "absence_required": [
                "states that the check-in solo-block evidence is missing",
                "does not infer focus harm from the hang-loop invite alone",
                "asks about check-in calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the noisy-hangout planning evidence is missing",
                    "does not infer planning harm from the hang loop alone",
                    "explicitly abstains from rejecting the hang loop",
                ],
                "ev_B": [
                    "states that the check-in solo-block evidence is missing",
                    "does not infer focus harm from the hang-loop invite alone",
                    "asks about check-in calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "noisy_hangout_planning_wreck", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "checkin_solo_morning_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "hang_loop_before_checkin_poor_fit", "hop": 2},
            ],
            "forbidden": ["never hang out", "friendship ban", "must cancel all group plans"],
            "distractor": {
                "timestamp": "2026-09-09T11:00:00Z",
                "user": f"{ca} said a standing hang loop before Thursday's friendship check-in lock is amazing for staying warm with everyone.",
                "assistant": "Warmth hype and planning blocks are different ledgers.",
                "why": "Hang-loop FOMO shares query surface but is not evidence about this user's noisy-hangout planning wreck or check-in solo blocks.",
            },
            "evolving": {"noisy_hangouts": "wreck_friendship_planning", "checkin_week": "solo_mornings_protected"},
        },
        "S17": {
            "name": "full_day_immersion_x_recommendation_letter",
            "prefix_end": 96,
            "evidence": {
                "ev_A": {
                    "session_id": 93,
                    "fact": "Full-day friend immersion leaves the user too drained to finish careful notes; short coffee hours are fine.",
                },
                "ev_B": {
                    "session_id": 95,
                    "fact": "Recommendation letter due Friday needs three solo evening writing blocks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-20T18:20:00Z",
            "query": "Bench-adjacent hang marathon before Friday's packet filing cutoff — workable?",
            "gold": (
                "Decline the bench-adjacent hang marathon before Friday's packet filing cutoff. Full-day friend immersion leaves "
                "you too drained to finish careful notes, and the recommendation letter already needs three solo evening "
                "writing blocks. Keep short coffee hours only."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an immersion week fits before Friday's letter cutoff. "
                "Full-day immersions have drained your note-writing energy, but I cannot tell from the available memory "
                "whether Friday's letter already needs three solo evening blocks. Confirm that calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a recommendation letter due "
                    "Friday needs three solo evening writing blocks, but the available memory does not establish that "
                    "full-day immersions drain your note energy. I cannot reject immersion from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an immersion week fits before Friday's letter cutoff. "
                    "Full-day immersions have drained your note-writing energy, but I cannot tell from the available memory "
                    "whether Friday's letter already needs three solo evening blocks. Confirm that calendar before deciding."
                ),
            },
            "required": [
                "uses full-day immersion draining careful-note energy",
                "uses recommendation letter needing solo evening blocks",
                "recommends declining hang marathon before packet filing cutoff",
            ],
            "absence_required": [
                "states that the letter-block evidence is missing",
                "does not infer harm from the immersion invite alone",
                "asks about letter timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the immersion-drain evidence is missing",
                    "does not infer drain from the invite alone",
                    "explicitly abstains from rejecting immersion",
                ],
                "ev_B": [
                    "states that the letter-block evidence is missing",
                    "does not infer harm from the immersion invite alone",
                    "asks about letter timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "immersion_note_drain", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "letter_solo_evenings", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pre_letter_immersion_poor_fit", "hop": 2},
            ],
            "forbidden": ["never see friends", "letter ban", "must cancel all immersions forever"],
            "distractor": {
                "timestamp": "2026-09-17T16:00:00Z",
                "user": f"{cb} said a bench-adjacent hang marathon before Friday's packet filing cutoff is amazing for loyalty points.",
                "assistant": "Loyalty hype and letter evenings are different ledgers.",
                "why": "Hang-marathon FOMO shares query surface but is not evidence about this user's immersion drain or letter-evening need.",
            },
            "evolving": {"full_day_immersion": "drains_note_energy", "recommendation_letter": "friday_solo_evenings"},
        },
        "S18": {
            "name": "late_drinks_x_hard_talk_clarity",
            "prefix_end": 101,
            "evidence": {
                "ev_A": {
                    "session_id": 98,
                    "fact": "Late-night social drinks after two o'clock ruin the user's next-morning clarity; early evening tea is fine.",
                },
                "ev_B": {
                    "session_id": 100,
                    "fact": "Midweek hard-talk readiness needs a sharp morning clarity block with a late-slot obligation already booked.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-28T09:15:00Z",
            "query": "Crew added a dusk-to-dawn maker signup — sensible with Thursday's review lock ahead?",
            "gold": (
                "Skip the dusk-to-dawn maker signup before Thursday's review lock. Late-night social drinks ruin your "
                "next-morning clarity, and midweek hard-talk readiness already needs a sharp morning clarity block. Choose "
                "an early evening or defer until after the hard talk."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a dusk-to-dawn hang fits before Thursday's hard-talk lock. "
                "Late drinks have ruined your next-morning clarity, but I cannot tell from the available memory whether a "
                "midweek hard talk already needs a protected clarity block. Confirm that calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know midweek hard-talk readiness "
                    "needs a sharp morning clarity block, but the available memory does not establish that late-night drinks "
                    "ruin your next-morning clarity. I cannot reject the hang from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a dusk-to-dawn hang fits before Thursday's hard-talk lock. "
                    "Late drinks have ruined your next-morning clarity, but I cannot tell from the available memory whether a "
                    "midweek hard talk already needs a protected clarity block. Confirm that calendar before deciding."
                ),
            },
            "required": [
                "uses late-drink next-morning clarity wreck",
                "uses midweek hard-talk clarity-block need",
                "recommends skipping dusk-to-dawn maker signup before review lock",
            ],
            "absence_required": [
                "states that the hard-talk clarity evidence is missing",
                "does not infer harm from the hang invite alone",
                "asks about hard-talk timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-drink clarity evidence is missing",
                    "does not infer clarity harm from the invite alone",
                    "explicitly abstains from rejecting the hang",
                ],
                "ev_B": [
                    "states that the hard-talk clarity evidence is missing",
                    "does not infer harm from the hang invite alone",
                    "asks about hard-talk timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_drinks_clarity_loss", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "hard_talk_morning_clarity", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "dusk_to_dawn_before_hardtalk_poor_fit", "hop": 2},
            ],
            "forbidden": ["never drink", "hard-talk ban", "must cancel all nights out"],
            "distractor": {
                "timestamp": "2026-09-25T20:00:00Z",
                "user": f"{ca} said a dusk-to-dawn maker signup before Thursday's review lock is amazing for crew loyalty.",
                "assistant": "Crew loyalty and morning clarity are different ledgers.",
                "why": "Dusk-to-dawn FOMO shares query surface but is not evidence about this user's late-drink clarity pattern or hard-talk clarity need.",
            },
            "evolving": {"late_drinks": "ruin_morning_clarity", "hard_talk": "needs_morning_clarity"},
        },
        "S19": {
            "name": "private_notes_x_flipchart_toast",
            "prefix_end": 106,
            "evidence": {
                "ev_A": {
                    "session_id": 103,
                    "fact": "The user preps best with private written notes; flipchart-only group prep sessions produce weak outputs.",
                },
                "ev_B": {
                    "session_id": 105,
                    "fact": "A prior flipchart-only toast rehearsal went poorly before the farewell dinner.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-10-06T16:30:00Z",
            "query": "Circle wants me on the poster-board run-through for next week's farewell briefing — good fit?",
            "gold": (
                "Decline the poster-board run-through for next week's farewell briefing or shift to private-note prep. You prep best "
                "with private written notes, and a prior flipchart-only toast rehearsal already went poorly. Private notes "
                "fit your process better."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a flipchart-only run-through fits. Private written notes "
                "work for you, but I cannot tell from the available memory whether a prior flipchart toast rehearsal failed. "
                "Confirm that track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior flipchart-only toast "
                    "rehearsal went poorly, but the available memory does not establish that private written notes are your "
                    "strongest prep format. I cannot reject the run-through from one bad night alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a flipchart-only run-through fits. Private written notes "
                    "work for you, but I cannot tell from the available memory whether a prior flipchart toast rehearsal failed. "
                    "Confirm that track record before volunteering."
                ),
            },
            "required": [
                "uses private written-notes prep preference",
                "uses prior flipchart-only toast rehearsal failure",
                "recommends declining poster-board run-through or shifting to private notes",
            ],
            "absence_required": [
                "states that the prior flipchart-failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about flipchart track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the private-notes preference evidence is missing",
                    "does not infer format harm from the run-through alone",
                    "explicitly abstains from rejecting the run-through",
                ],
                "ev_B": [
                    "states that the prior flipchart-failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about flipchart track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "private_notes_prep_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "flipchart_toast_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "flipchart_runthrough_poor_fit", "hop": 2},
            ],
            "forbidden": ["never speak at toasts", "toast ban forever", "social anxiety diagnosis"],
            "distractor": {
                "timestamp": "2026-10-03T14:00:00Z",
                "user": f"{cb} said a poster-board run-through for next week's farewell briefing is amazing hype and everyone will love the energy.",
                "assistant": "Energy marketing and prep-format fit are different questions.",
                "why": "Poster-board FOMO shares query surface but is not evidence about this user's private-notes preference or prior flipchart failure.",
            },
            "evolving": {"toast_prep": "private_written_notes", "flipchart_rehearsal": "prior_fail"},
        },
        "S20": {
            "name": "long_transit_x_distant_meetup",
            "prefix_end": 111,
            "evidence": {
                "ev_A": {
                    "session_id": 108,
                    "fact": "Long rush-hour transit for social visits drains the user's energy before careful talks; short bike rides are fine.",
                },
                "ev_B": {
                    "session_id": 110,
                    "fact": "New distant friend-meetup rhythm requires ninety-minute each-way transit on hangout days.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-10-14T17:10:00Z",
            "query": "Worth accepting the heavier daily corridor time for the relocated meetup cadence — based on what you know about me?",
            "gold": (
                "Decline the heavier daily corridor time for the relocated meetup cadence. Long rush-hour transit for "
                "social visits drains your energy before careful talks, and the new distant meetup rhythm already requires "
                "ninety-minute each-way transit on hangout days. Prefer shorter meetups closer to home or async check-ins."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether heavier corridor time fits the relocated meetup cadence. "
                "Long transit has drained your energy before careful talks, but I cannot tell from the available memory "
                "whether a distant meetup rhythm with ninety-minute legs is already booked. Confirm that calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a distant meetup rhythm requires "
                    "ninety-minute each-way transit, but the available memory does not establish that long rush-hour transit "
                    "drains your energy before careful talks. I cannot reject the cadence from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether heavier corridor time fits the relocated meetup cadence. "
                    "Long transit has drained your energy before careful talks, but I cannot tell from the available memory "
                    "whether a distant meetup rhythm with ninety-minute legs is already booked. Confirm that calendar before deciding."
                ),
            },
            "required": [
                "uses long rush-hour transit energy drain before careful talks",
                "uses distant meetup rhythm with ninety-minute transit",
                "recommends declining heavier corridor time for relocated meetup cadence",
            ],
            "absence_required": [
                "states that the distant-meetup rhythm evidence is missing",
                "does not infer harm from the corridor-time invite alone",
                "asks about meetup cadence or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the long-transit drain evidence is missing",
                    "does not infer energy harm from corridor time alone",
                    "explicitly abstains from rejecting the cadence",
                ],
                "ev_B": [
                    "states that the distant-meetup rhythm evidence is missing",
                    "does not infer harm from the corridor-time invite alone",
                    "asks about meetup cadence or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "long_transit_talk_energy_drain", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "distant_meetup_transit_load", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "relocated_meetup_cadence_poor_fit", "hop": 2},
            ],
            "forbidden": ["never visit friends", "transit ban", "must cancel all distant meetups"],
            "distractor": {
                "timestamp": "2026-10-11T09:30:00Z",
                "user": f"{ca} said heavier daily corridor time for the relocated meetup cadence is amazing hype and worth it for staying close.",
                "assistant": "Closeness hype and transit energy are different ledgers.",
                "why": "Corridor-time FOMO shares query surface but is not evidence about this user's long-transit drain or distant-meetup rhythm.",
            },
            "evolving": {"long_transit": "drains_talk_energy", "distant_meetup": "ninety_minute_legs"},
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
    if raw in {"S6-S10", "6-10"}:
        return ("S6", "S7", "S8", "S9", "S10")
    if raw in {"S11-S15", "11-15"}:
        return ("S11", "S12", "S13", "S14", "S15")
    if raw in {"S16-S20", "16-20"}:
        return ("S16", "S17", "S18", "S19", "S20")
    if raw in {"S6-S15", "6-15"}:
        return tuple(f"S{i}" for i in range(6, 16))
    if raw in {"S1-S15", "1-15"}:
        return tuple(f"S{i}" for i in range(1, 16))
    if raw in {"S1-S20", "1-20"}:
        return tuple(f"S{i}" for i in range(1, 21))
    if "," in raw:
        return tuple(part.strip() for part in raw.split(",") if part.strip())
    return (raw,)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate social/relationships gold JSON items.")
    parser.add_argument(
        "--scenarios",
        default="S1-S5",
        help="Scenario scope: S1-S5, S6-S15, S16-S20, S1-S20, etc.",
    )
    args = parser.parse_args(argv)
    scenario_ids = parse_scenario_ids(args.scenarios)
    if scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        batch_config = {
            **SC_BATCH_CONFIG,
            "batch_id": "SC_GOLD_S16_S20_2026-07-17_v2",
            "generator_name": "social_gold_s16_s20_v2",
        }
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **SC_BATCH_CONFIG,
            "batch_id": "SC_GOLD_S6_S15_2026-07-17_v2",
            "generator_name": "social_gold_s6_s15_v2",
        }
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10"):
        batch_config = {
            **SC_BATCH_CONFIG,
            "batch_id": "SC_GOLD_S6_S10_2026-07-17_v2",
            "generator_name": "social_gold_s6_s10_v2",
        }
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **SC_BATCH_CONFIG,
            "batch_id": "SC_GOLD_S11_S15_2026-07-17_v2",
            "generator_name": "social_gold_s11_s15_v2",
        }
    else:
        batch_config = {
            **SC_BATCH_CONFIG,
            "batch_id": "SC_GOLD_S1_S5_2026-07-17_v2",
            "generator_name": "social_gold_s1_s5_v2",
        }
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
    manifest_dir = PILOT_ROOT / "manifests" / "social"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    if scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        report_name = "social_gold_s16_s20_report.json"
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15"):
        report_name = "social_gold_s6_s15_report.json"
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10"):
        report_name = "social_gold_s6_s10_report.json"
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        report_name = "social_gold_s11_s15_report.json"
    else:
        report_name = "social_gold_s1_s5_report.json"
    report_path = manifest_dir / report_name
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nSUMMARY {n_pass}/{n} hard-gate PASS")
    print(
        f"SCORES min={report['score_distribution']['min']} "
        f"max={report['score_distribution']['max']} mean={report['score_distribution']['mean']}"
    )
    print(f"AT_95={report['score_distribution']['at_95']}")
    print(f"REPORT {report_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

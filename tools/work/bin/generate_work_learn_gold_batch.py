#!/usr/bin/env python3
"""Generate work/learning gold batches (S1–S20).

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
    output_path,
    score_item,
    session,
)

PERSONAS_PATH = DOMAIN / "personas" / "personas_work_learn.json"
COMPUTED_BY = "tools/work/bin/generate_work_learn_gold_batch.py"

WL_BATCH_CONFIG: dict[str, Any] = {
    "id_prefix": "WL",
    "pilot_domain": "work_learning",
    "domain_tags": ["work/career", "education/learning"],
    "data_subdir": "work",
    "folder_prefix": "work",
    "batch_id": "WL_GOLD_S6_S10_2026-07-15_v2",
    "generator_name": "work_learn_gold_batch_v2",
    "reproduce_generator": "python3 tools/work/bin/generate_work_learn_gold_batch.py",
}

USER10_PERSONA: dict[str, Any] = {
    "user_index": 10,
    "user_id": "wl_u10",
    "folder_tag": "user10",
    "display_name": "desktop-Healthy_Li",
    "source_corpus": "desktop_user",
    "source_ref": "local:Healthy Li; migrated from pilot WL",
    "stable_traits": [
        "psychology + AI research student",
        "University of Michigan exchange",
        "King's College London BSc Psychology",
        "software/research work rhythms",
        "values deep work autonomy",
    ],
    "voice": "curious, reflective, student-researcher",
}

# Shared cumulative work timeline (sessions 1–111): S1–S5, S6–S10, S11–S15, S16–S20
CANONICAL_TIMELINE = [
    # S1
    session(1, "2026-01-11T18:00:00Z", "Cleared a long email thread. Brain feels flat.", "Worth a short walk."),
    session(2, "2026-01-12T18:00:00Z", "Repainted a shelf. Oddly satisfying.", "Small resets help."),
    session(3, "2026-01-18T18:00:00Z", "Filed expense receipts from last client trip.", "Budget hygiene helps."),
    session(
        4,
        "2026-01-26T18:00:00Z",
        "Keep getting dull headaches when I am up before six for those early calls.",
        "Do they fade later?",
        "By noon I am fine. The early stretch is the problem.",
    ),
    session(5, "2026-02-03T18:00:00Z", "Short walk after back-to-back calls.", "Movement between blocks matters."),
    session(
        6,
        "2026-02-10T18:00:00Z",
        "It is past midnight and I just finished a clean refactor. This window is when my brain actually locks in.",
        "Late focus can be powerful if you protect recovery somehow.",
        "I sleep in on weekends to compensate.",
    ),
    session(7, "2026-02-17T18:00:00Z", "Colleague mentioned a spring skills fair. Saved the flyer without committing.", "Fairs are tempting calendar items."),
    session(8, "2026-02-24T18:00:00Z", "Blocked Friday afternoon for deep review work.", "Protected blocks are scarce."),
    session(9, "2026-03-02T18:00:00Z", "Printed the March calendar. Dawn blocks are marked as protected.", "Paper copies help on busy weeks."),
    # S2
    session(10, "2026-03-09T18:00:00Z", "Archived old Slack channels from a closed project.", "Less notification noise."),
    session(
        11,
        "2026-03-16T18:00:00Z",
        "Python finally stuck after I rebuilt a tiny ETL script myself. Tutorials alone never lasted.",
        "Making something real is a strong teacher.",
        "If I am not typing the solution, it fades.",
    ),
    session(12, "2026-03-23T18:00:00Z", "Prepared a one-page brief before tomorrow's sync.", "Prep beats improvisation."),
    session(
        13,
        "2026-03-30T18:00:00Z",
        "Abandoned another course full of forty-minute talking-head recordings. I kept drifting and then felt lost.",
        "Passive video can be brutal. Did any format work better before?",
        "Short exercises with feedback. That is about it.",
    ),
    session(14, "2026-04-06T18:00:00Z", "Declined an optional evening networking mixer.", "Energy has a ledger."),
    session(15, "2026-04-13T18:00:00Z", "HR mailed two stipend options. I filed them without replying yet.", "Learning-budget choices often split theory vs build."),
    session(16, "2026-04-20T18:00:00Z", "Printed the stipend comparison sheet. Theory and build columns are side by side.", "Paper copies help on busy weeks."),
    # S3
    session(17, "2026-04-27T18:00:00Z", "Tested a new note template for client meetings.", "Templates reduce cognitive load."),
    session(
        18,
        "2026-05-04T18:00:00Z",
        "My coffee high dies after two o'clock. After that I am foggy and slow no matter what I drink.",
        "That afternoon dip is common. Does it hit focus hard?",
        "Yeah. Detailed reviews after that are a mess.",
    ),
    session(19, "2026-05-11T18:00:00Z", "Facilities posted updated ergonomic reminders in the lobby.", "Worth noting for long desk days."),
    session(
        20,
        "2026-05-18T18:00:00Z",
        "That 4pm account review last month was embarrassing. I lost the thread twice and someone else had to rescue the room.",
        "Harsh memory. Was the material unfamiliar?",
        "No, I knew it. I was just empty by then.",
    ),
    session(21, "2026-05-25T18:00:00Z", "Cleaned up stale calendar holds from last quarter.", "Calendar hygiene helps."),
    session(22, "2026-06-01T18:00:00Z", "Short reading block after lunch. Kept it under thirty minutes.", "Bounded breaks help."),
    session(23, "2026-06-08T18:00:00Z", "Visibility committee posted a late-block invite. I filed it without replying.", "Invites can wait for an energy plan."),
    session(24, "2026-06-15T18:00:00Z", "Printed the facilitation calendar. Late blocks are marked in red.", "Paper copies help on busy weeks."),
    # S4
    session(
        25,
        "2026-06-22T18:00:00Z",
        "Handwriting notes in my paper notebook is still how I remember anything. Typing feels like it slides off.",
        "Motor memory helps a lot of learners. Do you rewrite summaries too?",
        "Sometimes. The first pass on paper is the key.",
    ),
    session(26, "2026-06-29T18:00:00Z", "Labeled folders from a batch documentation pass.", "Order supports the week."),
    session(
        27,
        "2026-07-02T18:00:00Z",
        "That digital-slate highlighting experiment last fall was a disaster. I marked forever and still blanked on the quiz.",
        "Frustrating when the tool fights your process.",
        "I went back to paper the next week and scores jumped.",
    ),
    session(28, "2026-07-04T18:00:00Z", "Classmates are pushing a screen-only program signup. I filed it without replying.", "Digital-first program marketing is loud right now."),
    # S5
    session(
        29,
        "2026-07-06T18:00:00Z",
        "That two-week night-alert stretch last year wrecked me. I woke at every buzz and felt useless the next days.",
        "Sleep debt from alerts is brutal. Did recovery take long?",
        "Almost a month before I felt normal again.",
    ),
    session(30, "2026-07-08T18:00:00Z", "Café posted a one-day coworking signup. Public venue again.", "Coworking days and desk focus are different."),
    session(
        31,
        "2026-07-10T18:00:00Z",
        "If my night gets chopped up, the next day I ship sloppy mistakes. Unbroken sleep is non-negotiable for me.",
        "That is important self-knowledge. Protecting sleep is protecting work quality.",
        "Exactly. I schedule around it when I can.",
    ),
    session(32, "2026-07-12T18:00:00Z", "Ops team posted a rotation blurb. I filed it without replying yet.", "Invites can wait for a sleep plan."),
    # S6
    session(33, "2026-06-04T17:55:00Z", "Recovery blocks are finally visible on the work calendar again.", "Tradeoffs are easier to see."),
    session(
        34,
        "2026-06-07T20:30:00Z",
        "Extended standing-desk stretches without sit breaks leave my lower back tight the next morning. Walking one-on-ones do not.",
        "Has the sustained standing load repeated?",
        "Twice this month. Short walking chats do not do it — it is the long standing blocks.",
    ),
    session(35, "2026-06-09T13:20:00Z", "Walked back from the client district. Nice reset.", "Small movement breaks add up."),
    session(
        36,
        "2026-06-11T07:10:00Z",
        "Chiropractor this week: cap consecutive standing hours during flare weeks — treat it as a hard boundary.",
        "Is that non-negotiable for now?",
        "Yes. I am treating it as a hard work boundary.",
    ),
    session(37, "2026-06-13T16:40:00Z", "Office chat keeps pushing a full-day standing onsite workshop signup. Lots of facilities hype.", "Workshop FOMO is loud."),
    session(38, "2026-06-14T18:05:00Z", "Someone asked whether any standing workshop is worth it for career visibility.", "Visibility and back load are different questions."),
    # S7
    session(39, "2026-06-16T19:15:00Z", "Archived stale meeting notes from last sprint.", "Less clutter in the review queue."),
    session(
        40,
        "2026-06-18T21:50:00Z",
        "Dense spec review needs an uninterrupted 8-11am block; mid-morning pings wreck nested context.",
        "Has that pattern repeated?",
        "Yes. Once the block fractures, I lose the thread for hours.",
    ),
    session(41, "2026-06-20T12:30:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        42,
        "2026-06-22T08:45:00Z",
        "Manager scheduled a weekly leadership opener at the start of Tuesday blocks — already recurring.",
        "Is that slot movable?",
        "Not easily. Leadership treats it as standing.",
    ),
    session(43, "2026-06-24T14:10:00Z", "Leadership chat is loud about mandatory nine-o'clock Tuesday morning visibility slots.", "Visibility slot pressure is loud."),
    session(44, "2026-06-25T17:20:00Z", "Someone asked whether any Tuesday-morning visibility slot is worth the calendar tradeoff.", "Visibility and focus blocks are different questions."),
    # S8
    session(
        45,
        "2026-06-27T10:05:00Z",
        "Best client memos come from async written prep, not live improvisation under lights.",
        "Has live format underperformed?",
        "Yes. Written drafts land; live riffing does not.",
    ),
    session(46, "2026-06-28T15:40:00Z", "Polished a written brief for tomorrow's stakeholder note.", "Prep quality shows in output."),
    session(
        47,
        "2026-06-30T19:30:00Z",
        "Last live panel moderation went poorly — I lost the thread and client follow-up suffered.",
        "Was that a one-off?",
        "No. Live moderation under pressure is a weak spot for me.",
    ),
    session(48, "2026-07-01T11:15:00Z", "Client team chat is hyping a live panel moderation slot next week.", "Live format invites need a skill check."),
    session(49, "2026-07-02T16:50:00Z", "Someone forwarded hype about volunteering for any live client panel for visibility.", "Visibility and live skill fit are different questions."),
    # S9
    session(
        50,
        "2026-07-06T22:15:00Z",
        "Overnight return flights leave me cognitively flat through the next full workday — details slip on dense material.",
        "Was it just one trip?",
        "Twice. The morning after an overnight return is the problem.",
    ),
    session(51, "2026-07-08T07:45:00Z", "Travel bag is packed for the weekend client trip. Return timing still open.", "Return timing and Monday load overlap."),
    session(
        52,
        "2026-07-10T16:20:00Z",
        "Board rehearsal is locked Monday 10am right after the weekend trip.",
        "Is that deadline firm?",
        "Yes. It is already on the calendar.",
    ),
    session(53, "2026-07-11T08:00:00Z", "Forum crowd insists a late Sunday return before Monday board rehearsal is normal practice. I disagree.", "Online norms are not calendar facts."),
    session(54, "2026-07-12T19:30:00Z", "Someone forwarded hype about Sunday-night travel before Monday's board rehearsal. Not my plan.", "Social pressure is not a schedule."),
    # S10
    session(
        55,
        "2026-07-14T18:10:00Z",
        "Constant channel pings during focus blocks make me lose nested context — sloppy commits follow.",
        "Has that pattern repeated?",
        "Yes. Open channels during deep work are costly.",
    ),
    session(56, "2026-07-16T12:30:00Z", "Muted non-urgent channels before afternoon review work.", "Small guardrails help."),
    session(
        57,
        "2026-07-18T09:40:00Z",
        "Prior constant-interruption sprint week correlated with a measurable defect and rollback spike on my lane.",
        "Was that a one-off?",
        "No. Constant interruptions and desk-side churn do not mix for me.",
    ),
    session(58, "2026-07-19T17:05:00Z", "Platform chat keeps pushing a five-day desk-side collaboration sprint signup. I am ignoring the hype for now.", "Sprint invites need a focus check."),
    session(59, "2026-07-20T07:20:00Z", "Release review is on the calendar right after that proposed desk-side sprint week.", "Quality math matters for release weeks."),
    # S11 evidence block
    session(60, "2026-07-22T18:00:00Z", "Recovery blocks are finally visible on the work calendar again.", "Tradeoffs are easier to see."),
    session(
        61,
        "2026-07-24T20:30:00Z",
        "Back-to-back video-call days leave my voice strained for next-day presentations — async memo days do not.",
        "Has that pattern repeated?",
        "Twice this month. Async memo days are fine — it is the stacked video blocks.",
    ),
    session(62, "2026-07-26T13:20:00Z", "Walked back from the client district. Nice reset.", "Small movement breaks add up."),
    session(
        63,
        "2026-07-28T07:10:00Z",
        "Client keynote dry-run Thursday at nine is non-negotiable — I am treating it as a hard calendar boundary.",
        "Is that timing firm?",
        "Yes. It is already locked.",
    ),
    session(64, "2026-07-30T16:40:00Z", "Facilities newsletter landed. I only skimmed the seating-options section.", "Not every mailer needs a decision."),
    session(65, "2026-07-31T18:05:00Z", "Logged a short voice warm-up routine from the coach notes. Keeping presentation days protected.", "Recovery notes are worth tracking."),
    # S12
    session(66, "2026-08-02T19:15:00Z", "Restocked sticky notes for the design-doc sprint. Solo blocks still matter.", "Focus routines are not one-size."),
    session(
        67,
        "2026-08-04T21:50:00Z",
        "Afternoon pair-programming rotations wreck my solo architecture focus for hours — short syncs are fine.",
        "Has the afternoon pairing pattern repeated?",
        "Yes. Three long pairing blocks did it; short syncs did not.",
    ),
    session(68, "2026-08-06T12:30:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        69,
        "2026-08-08T08:45:00Z",
        "Architecture design-doc deadline Friday noon requires protected solo blocks Wednesday and Thursday.",
        "Is that slot movable?",
        "Not easily. The review depends on it.",
    ),
    session(70, "2026-08-10T14:10:00Z", "Platform chat is noisy about pairing rotations. I muted the thread.", "Mute buttons save attention."),
    session(71, "2026-08-11T17:20:00Z", "Printed the August delivery calendar. Solo design blocks are locked.", "Paper copies help on busy weeks."),
    # S13
    session(
        72,
        "2026-08-13T10:05:00Z",
        "Late-night certification cram sessions wreck my alert responsiveness the next morning — morning study blocks have been fine.",
        "Has the late-night cram pattern repeated?",
        "Yes. Three midnight sessions did it; morning blocks did not.",
    ),
    session(73, "2026-08-14T15:40:00Z", "Pager rotation checklist is printed for next week. Morning alert windows are scarce.", "On-call prep has a timeline."),
    session(
        74,
        "2026-08-16T19:30:00Z",
        "On-call rotation starts Monday with strict paging expectations — I need reliable morning alert response.",
        "Is that deadline firm?",
        "Yes. The rotation is already scheduled.",
    ),
    session(75, "2026-08-17T11:15:00Z", "Training portal posted a late cert-study invite. I filed it without replying.", "Invites can wait for a rotation plan."),
    session(76, "2026-08-18T16:50:00Z", "Marked morning alert windows on the on-call checklist. Focus windows are the priority.", "Rotation logistics are the priority."),
    # S14
    session(
        77,
        "2026-08-20T22:15:00Z",
        "Open-office hot-desk days destroy focus for dense policy drafting — quiet home blocks are fine.",
        "Was that a one-off?",
        "No. Twice on hot-desk days; quiet home blocks did not.",
    ),
    session(78, "2026-08-22T07:45:00Z", "Policy draft outline is packed. Wednesday deadline is on the calendar.", "Draft weeks need protected writing blocks."),
    session(
        79,
        "2026-08-24T16:20:00Z",
        "Quiet policy draft is due Wednesday and needs a deep writing block without open-office churn.",
        "Is that slot firm?",
        "Yes. It is already booked.",
    ),
    session(80, "2026-08-25T08:00:00Z", "Facilities forum is loud about hot-desk norms. I am not adopting forum defaults.", "Forum norms are not focus facts."),
    session(81, "2026-08-26T19:30:00Z", "Packed reference notes for the policy draft. Timing still feels tight.", "Writing timing matters on deadline weeks."),
    # S15
    session(
        82,
        "2026-08-28T18:10:00Z",
        "Weekend inbox catch-up blitzes bleed into protected personal planning blocks — weekday triage has been fine.",
        "Has that pattern repeated?",
        "Yes. Two weekend blitzes did it; weekday triage did not.",
    ),
    session(83, "2026-08-30T12:30:00Z", "Sabbatical planning week is on the calendar. Monday half-day blocks are marked.", "Planning context matters for boundaries."),
    session(
        84,
        "2026-09-01T09:40:00Z",
        "Sabbatical planning week requires protected Monday half-day blocks for structured planning work.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(85, "2026-09-02T17:05:00Z", "Ops chat sent another weekend catch-up invite. I filed it without replying.", "Invites can wait for a planning window."),
    session(86, "2026-09-03T07:20:00Z", "Set out the sabbatical planning checklist for Monday. Protected blocks need a clean routine.", "Planning weeks need a clean routine."),
    # S16
    session(87, "2026-09-05T18:00:00Z", "Autumn delivery calendar is printed. Solo blueprint blocks are marked.", "Paper copies help on busy weeks."),
    session(
        88,
        "2026-09-07T20:45:00Z",
        "Open-bullpen ambient chatter wrecks my architecture diagramming — quiet-room blocks are fine.",
        "Has that pattern repeated?",
        "Yes. Twice on bullpen days; quiet-room blocks did not.",
    ),
    session(89, "2026-09-08T13:10:00Z", "Short walk between buildings. Nice reset.", "Small movement breaks add up."),
    session(
        90,
        "2026-09-10T08:30:00Z",
        "Diagram sprint week needs protected morning solo blocks Tuesday through Thursday — already on the calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(91, "2026-09-11T16:55:00Z", "Facilities posted a huddle-loop signup blurb. I filed it without replying.", "Invites can wait for a push plan."),
    # S17
    session(92, "2026-09-13T19:20:00Z", "Restocked index tabs for the packet filing sprint. Solo evenings still matter.", "Focus routines are not one-size."),
    session(
        93,
        "2026-09-15T21:10:00Z",
        "Full-day mentor shadowing leaves me too drained to finish my own deliverables — short office hours are fine.",
        "Has the full-day shadowing pattern repeated?",
        "Yes. Three immersion days did it; short office hours did not.",
    ),
    session(94, "2026-09-16T12:40:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        95,
        "2026-09-18T08:50:00Z",
        "Advancement dossier due Friday needs three solo evening writing blocks — already on the calendar.",
        "Is that slot movable?",
        "Not easily. The review depends on it.",
    ),
    session(96, "2026-09-19T14:25:00Z", "HR chat is noisy about immersion weeks. I muted the thread.", "Mute buttons save attention."),
    # S18
    session(97, "2026-09-21T10:05:00Z", "Printed the autumn delivery calendar. Solo prep blocks are marked.", "Prep weeks need a clean routine."),
    session(
        98,
        "2026-09-23T15:35:00Z",
        "Extra espresso after two o'clock gives me jittery nights and ruins next-morning clarity — morning tea is fine.",
        "Has the afternoon espresso pattern repeated?",
        "Yes. Three late espressos did it; morning tea did not.",
    ),
    session(99, "2026-09-24T11:20:00Z", "Hall mailer landed. I filed it without replying.", "Invites can wait for a prep plan."),
    session(
        100,
        "2026-09-26T07:15:00Z",
        "Midweek readiness checkpoint needs a sharp morning clarity block — a late-slot obligation is already booked through the night before.",
        "Is that timing firm?",
        "Yes. The checkpoint is already scheduled.",
    ),
    session(101, "2026-09-27T16:50:00Z", "Packed reference notes for the review lock. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S19
    session(102, "2026-09-29T18:15:00Z", "Numbers session outline is packed. Wednesday slot is on the calendar.", "Session weeks need protected prep blocks."),
    session(
        103,
        "2026-10-01T22:00:00Z",
        "I think best in spreadsheet grid layouts — wall-chart-only prep sessions produce weak outputs for me.",
        "Has the wall-chart-only pattern repeated?",
        "Yes. Twice on wall-chart-only prep; spreadsheet grids did not.",
    ),
    session(104, "2026-10-02T08:00:00Z", "Leadership forum is loud about poster-board run-throughs. I am not adopting forum defaults.", "Forum norms are not prep facts."),
    session(
        105,
        "2026-10-04T16:30:00Z",
        "Prior wall-chart-only figures rehearsal went poorly before the exec briefing — I lost the thread twice.",
        "Harsh memory. Was the material unfamiliar?",
        "No. The format fought my process.",
    ),
    session(106, "2026-10-05T19:40:00Z", "Printed the numbers session calendar. Solo grid-prep blocks are locked.", "Paper copies help on busy weeks."),
    # S20
    session(107, "2026-10-07T18:05:00Z", "Account cadence change memo landed. I only skimmed the corridor-time section.", "Not every memo needs a decision."),
    session(
        108,
        "2026-10-09T07:50:00Z",
        "Long rush-hour commutes drain my cognitive energy before deep work starts — short bike rides are fine.",
        "Has the long commute pattern repeated?",
        "Yes. Ninety-minute legs did it; short bike rides did not.",
    ),
    session(109, "2026-10-10T14:15:00Z", "Facilities posted a campus-shuttle blurb. I filed it without replying.", "Invites can wait for an energy plan."),
    session(
        110,
        "2026-10-12T09:25:00Z",
        "New client site rhythm requires ninety-minute each-way transit on collaboration days — already on the calendar.",
        "Is that timing firm?",
        "Yes. The site rhythm is already booked.",
    ),
    session(111, "2026-10-13T17:30:00Z", "Packed a light bag for the first relocated-account day. Corridor timing still feels heavy.", "Cadence changes need an energy plan."),
]


def monotonic_timeline(timeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
        3: {"location": "the city", "colleague_a": "Jules", "colleague_b": "Rina", "role_short": "knowledge work"},
        4: {"location": "the suburbs", "colleague_a": "Nora", "colleague_b": "Ben", "role_short": "family-career"},
        5: {"location": "downtown", "colleague_a": "Luis", "colleague_b": "Carmen", "role_short": "busy-calendar"},
        6: {"location": "Berlin", "colleague_a": "Lena", "colleague_b": "Tobias", "role_short": "weekday"},
        7: {"location": "Austin", "colleague_a": "Chris", "colleague_b": "Sam", "role_short": "social workplace"},
        8: {"location": "the hospital district", "colleague_a": "Priya", "colleague_b": "James", "role_short": "clinical"},
        9: {"location": "office campus", "colleague_a": "Helga", "colleague_b": "Karl", "role_short": "office"},
        10: {"location": "Ann Arbor", "colleague_a": "Mia", "colleague_b": "Leo", "role_short": "campus"},
    }
    base = configs.get(idx, configs[3])
    trait = persona.get("stable_traits", ["work routine keeper"])[0]
    base["trait0"] = trait
    base["voice"] = persona.get("voice", "measured").split(",")[0]
    return base


def paint_session(s: dict[str, Any], paint: dict[str, str]) -> dict[str, Any]:
    sid = s["session_id"]
    dlg = deepcopy(s["dialogue"])
    if sid == 2 and paint["user_index"] != 1:
        dlg[0]["content"] = (
            f"Work mode today felt very '{paint['trait0']}' — long blocks, little slack."
        )
        if len(dlg) > 1:
            dlg[1]["content"] = "Given that practical pace, worth protecting recovery tonight."
    if sid == 21 and paint["location"] != "Pittsburgh":
        dlg[0]["content"] = dlg[0]["content"].replace(
            "conference agenda", f"{paint['location']} conference agenda"
        )
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
            "name": "early_headache_x_late_deepwork",
            "prefix_end": 9,
            "evidence": {
                "ev_A": {
                    "session_id": 4,
                    "fact": "Rising before 6am for early calls causes dull morning headaches that ease by noon.",
                },
                "ev_B": {
                    "session_id": 6,
                    "fact": "The user's peak deep-work window is roughly midnight to 3am.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-03-09T17:30:00Z",
            "query": "Manager offered a move onto the platform pod with a mandatory daily dawn check-in — would I thrive there based on what you know about me?",
            "gold": (
                "Probably not as-is. Rising before 6am for early calls already causes dull morning headaches, and your peak "
                "deep-work window is roughly midnight to 3am, so a mandatory daily dawn check-in conflicts with known patterns. "
                "Negotiate flexible hours or decline rather than accepting unchanged."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Early rising has caused morning headaches, "
                "but I cannot tell from the available memory whether your deep-work window is late at night. Confirm chronotype "
                "and morning tolerance before deciding on a dawn check-in team."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your peak deep-work window is "
                    "roughly midnight to 3am, but the available memory does not establish that early calls cause morning headaches. "
                    "I cannot reject the move from chronotype alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Early rising has caused morning headaches, "
                    "but I cannot tell from the available memory whether your deep-work window is late at night. Confirm chronotype "
                    "and morning tolerance before deciding on a dawn check-in team."
                ),
            },
            "required": [
                "uses early-rising headache pattern",
                "uses late-night peak deep-work window",
                "recommends declining or negotiating away mandatory dawn check-in",
            ],
            "absence_required": [
                "states that the late deep-work window evidence is missing",
                "does not infer schedule harm from the offer alone",
                "asks about chronotype or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the early-headache evidence is missing",
                    "does not infer morning harm from the offer alone",
                    "explicitly abstains from rejecting the move",
                ],
                "ev_B": [
                    "states that the late deep-work window evidence is missing",
                    "does not infer schedule harm from the offer alone",
                    "asks about chronotype or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "morning_impairment", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "evening_peak", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "dawn_checkin_poor_fit", "hop": 2},
            ],
            "forbidden": ["night_oriented_pattern", "must never work mornings", "decline all team moves"],
            "distractor": {
                "timestamp": "2026-02-20T11:00:00Z",
                "user": f"I really love my current team though. Honestly I would do almost anything to work more closely with {ca}'s crew — they are amazing.",
                "assistant": "People-fit is not the same as schedule-fit.",
                "why": "Team-bond FOMO is query-relevant but not evidence about this user's early-headache pattern or late-night deep-work window.",
            },
            "evolving": {"chronotype_pattern": "night_oriented_pattern", "early_calls": "morning_headaches"},
        },
        "S2": {
            "name": "project_learning_x_video_dropout",
            "prefix_end": 16,
            "evidence": {
                "ev_A": {"session_id": 11, "fact": "The user retains skills by building small projects, not by passive reading."},
                "ev_B": {"session_id": 13, "fact": "Long recorded lecture videos cause the user to zone out and quit courses."},
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-04-10T17:05:00Z",
            "query": "For the learning stipend, should I pick the theory-module track or the live build cohort? A friend says the theory track is amazing.",
            "gold": (
                "Choose the live build cohort despite the friend's theory-track praise. You retain skills by building small "
                "projects and abandon long talking-head recordings; certificate prestige is not evidence of retention fit."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Project-based learning has worked for you, "
                "but I cannot tell from the available memory whether long lecture videos cause dropout. Confirm learning-format "
                "history before picking a stipend track."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know long recorded lectures cause "
                    "dropout, but the available memory does not establish that you retain skills by building projects. "
                    "I cannot reject the theory track from video format alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Project-based learning has worked for you, "
                    "but I cannot tell from the available memory whether long lecture videos cause dropout. Confirm learning-format "
                    "history before picking a stipend track."
                ),
            },
            "required": [
                "uses project-based learning preference",
                "uses lecture-video abandonment pattern",
                "recommends live build cohort over theory-module track",
            ],
            "absence_required": [
                "states that the lecture-dropout evidence is missing",
                "does not infer format harm from the friend's praise alone",
                "asks about learning format or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the project-learning evidence is missing",
                    "does not infer retention fit from the theory track alone",
                    "explicitly abstains from recommending a track",
                ],
                "ev_B": [
                    "states that the lecture-dropout evidence is missing",
                    "does not infer format harm from the friend's praise alone",
                    "asks about learning format or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "build_based_retention", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "lecture_dropout", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "prefer_lab_track", "hop": 2},
            ],
            "forbidden": ["always choose beta", "learning style diagnosis", "must reject all theory"],
            "distractor": {
                "timestamp": "2026-04-07T09:30:00Z",
                "user": f"A friend said the theory-module stipend track is amazing — everyone at her company picks it because the certificate looks great.",
                "assistant": "Prestige signals can be tempting.",
                "why": "Another person's theory-track praise is query-similar but not evidence about this user's project-learning or lecture-dropout pattern.",
            },
            "evolving": {"learning_mode": "build_first", "passive_video": "dropout"},
        },
        "S3": {
            "name": "afternoon_crash_x_late_workshop",
            "prefix_end": 24,
            "evidence": {
                "ev_A": {"session_id": 18, "fact": "After a morning coffee peak, the user crashes hard after 2pm and cannot sustain detailed review work."},
                "ev_B": {"session_id": 20, "fact": "A prior late-afternoon account review went poorly because the user was already cognitively empty."},
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-12T18:45:00Z",
            "query": "Worth leading the recurring late facilitation block after mid-afternoon? A senior said those blocks are amazing for visibility.",
            "gold": (
                "Lean no or renegotiate to a morning slot. You crash hard after 2pm and already failed a late account review "
                "while cognitively empty; visibility talk does not override that pattern."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a late facilitation block fits. Post-2pm crashes have hurt "
                "focus, but I cannot tell from the available memory whether a prior late review failed while you were empty. "
                "Confirm afternoon energy before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a late account review failed while "
                    "you were cognitively empty, but the available memory does not establish that you crash after 2pm. "
                    "I cannot reject the block from one meeting alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a late facilitation block fits. Post-2pm crashes have hurt "
                    "focus, but I cannot tell from the available memory whether a prior late review failed while you were empty. "
                    "Confirm afternoon energy before committing."
                ),
            },
            "required": [
                "uses post-2pm crash pattern",
                "uses prior late-afternoon review failure",
                "recommends declining or shifting the late facilitation block",
            ],
            "absence_required": [
                "states that the late-review failure evidence is missing",
                "does not infer cognitive harm from visibility talk alone",
                "asks about afternoon energy or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the post-2pm crash evidence is missing",
                    "does not infer facilitation harm from the invite alone",
                    "explicitly abstains from rejecting the block",
                ],
                "ev_B": [
                    "states that the late-review failure evidence is missing",
                    "does not infer cognitive harm from visibility talk alone",
                    "asks about afternoon energy or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "post_2pm_crash", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "late_slot_failure", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "avoid_late_workshop_block", "hop": 2},
            ],
            "forbidden": ["ADHD diagnosis", "must decline all visibility", "never take late meetings"],
            "distractor": {
                "timestamp": "2026-05-10T14:00:00Z",
                "user": f"{cb} said late facilitation blocks are amazing for visibility — if you want to grow, you should say yes to every late invite for the career story.",
                "assistant": "Visibility advice is common.",
                "why": "Late-block visibility hype is query-similar but not evidence about this user's post-2pm crash or prior late-review failure.",
            },
            "evolving": {"post_lunch_dip": "severe_after_14h", "late_meeting_risk": "high"},
        },
        "S4": {
            "name": "handwriting_x_tablet_bootcamp",
            "prefix_end": 28,
            "evidence": {
                "ev_A": {"session_id": 25, "fact": "The user remembers material best when handwriting notes in a paper notebook."},
                "ev_B": {"session_id": 27, "fact": "A prior digital-slate study experiment failed; the user could not retain material."},
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-23T17:20:00Z",
            "query": "Worth enrolling in the vendor's screen-first skills cohort? Marketing says the digital refresh is amazing.",
            "gold": (
                "Do not choose the screen-only program as-is. Handwritten notebook notes are how you retain material, and a "
                "prior digital-slate experiment failed; marketing about an amazing upgrade is not retention evidence. Require "
                "a paper accommodation or pick another program."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a screen-only program fits. Handwriting has worked for retention, "
                "but I cannot tell from the available memory whether a prior digital-slate experiment failed. Confirm note-taking "
                "medium history before signing up."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a digital-slate experiment failed, "
                    "but the available memory does not establish that handwriting is your retention medium. I cannot reject the "
                    "program from one failed pilot alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a screen-only program fits. Handwriting has worked for retention, "
                    "but I cannot tell from the available memory whether a prior digital-slate experiment failed. Confirm note-taking "
                    "medium history before signing up."
                ),
            },
            "required": [
                "uses handwriting/notebook retention preference",
                "uses prior digital-slate failure",
                "recommends against screen-only program or requires paper accommodation",
            ],
            "absence_required": [
                "states that the digital-slate failure evidence is missing",
                "does not infer retention harm from marketing alone",
                "asks about note-taking medium or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the handwriting-retention evidence is missing",
                    "does not infer format mismatch from the program alone",
                    "explicitly abstains from rejecting the program",
                ],
                "ev_B": [
                    "states that the digital-slate failure evidence is missing",
                    "does not infer retention harm from marketing alone",
                    "asks about note-taking medium or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "paper_retention", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "digital_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "constrains", "target": "tablet_only_program", "hop": 2},
            ],
            "forbidden": ["dyslexia diagnosis", "never use tablets", "paper ban forever"],
            "distractor": {
                "timestamp": "2026-05-10T14:30:00Z",
                "user": f"A classmate said the vendor's screen-first cohort is amazing — sleek app, automatic sync, and everyone says the digital refresh is worth it.",
                "assistant": "Marketing around digital-first programs is loud.",
                "why": "Screen-only program hype is query-similar but not evidence about this user's handwriting retention or digital-slate failure.",
            },
            "evolving": {"note_medium": "paper_handwriting", "digital_slate": "failed_pilot"},
        },
        "S5": {
            "name": "night_alert_x_sre_rotation",
            "prefix_end": 32,
            "evidence": {
                "ev_A": {"session_id": 29, "fact": "A prior night-alert stretch caused multi-night sleep disruption and lingering daytime impairment."},
                "ev_B": {"session_id": 31, "fact": "The user needs unbroken night sleep to stay effective; fragmented nights cascade into sloppy mistakes."},
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-02T19:30:00Z",
            "query": "Six-week callback roster just landed. Friend keeps saying the crew is amazing — worth joining based on what you know about me?",
            "gold": (
                "Lean no unless overnight callbacks are protected. A prior night-alert stretch caused multi-week impairment, and unbroken "
                "night sleep is non-negotiable for your work quality; friend prestige talk does not override that."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an ops rotation with night paging fits. Night-alert stretches "
                "have caused impairment, but I cannot tell from the available memory whether unbroken sleep is non-negotiable "
                "for your work quality. Confirm sleep fragility before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know unbroken night sleep is "
                    "non-negotiable for your work quality, but the available memory does not establish that night-alert "
                    "stretches caused multi-week impairment. I cannot reject the rotation from sleep needs alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an ops rotation with night paging fits. Night-alert stretches "
                    "have caused impairment, but I cannot tell from the available memory whether unbroken sleep is non-negotiable "
                    "for your work quality. Confirm sleep fragility before deciding."
                ),
            },
            "required": [
                "uses prior night-alert sleep disruption",
                "uses unbroken-sleep requirement for work quality",
                "recommends declining or heavily conditioning the rotation",
            ],
            "absence_required": [
                "states that the unbroken-sleep requirement evidence is missing",
                "does not infer harm from friend praise alone",
                "asks about sleep fragility or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the night-alert impairment evidence is missing",
                    "does not infer rotation harm from the offer alone",
                    "explicitly abstains from rejecting the rotation",
                ],
                "ev_B": [
                    "states that the unbroken-sleep requirement evidence is missing",
                    "does not infer harm from friend praise alone",
                    "asks about sleep fragility or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "alert_sleep_debt", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "work_quality", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "ops_rotation_risky", "hop": 2},
            ],
            "forbidden": ["insomnia diagnosis", "never do on-call", "must reject all ops roles"],
            "distractor": {
                "timestamp": "2026-05-20T18:30:00Z",
                "user": f"A friend on the duty crew said the callback roster is amazing — fast promotion path, you should take it if you want career growth.",
                "assistant": "Prestige and growth stories are persuasive.",
                "why": "Ops rotation prestige hype is query-similar but not evidence about this user's night-alert impairment or unbroken-sleep requirement.",
            },
            "evolving": {"sleep_fragility": "alert_sensitive", "night_continuity": "non_negotiable"},
        },
        "S6": {
            "name": "standing_back_flare_x_full_day_workshop",
            "prefix_end": 38,
            "evidence": {
                "ev_A": {
                    "session_id": 34,
                    "fact": "Extended standing-desk stretches without sit breaks leave the user's lower back tight the next morning; walking one-on-ones are fine.",
                },
                "ev_B": {
                    "session_id": 36,
                    "fact": "Chiropractor advised capping consecutive standing hours during flare weeks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-15T17:10:00Z",
            "query": "Facilities is hyping a full-day standing onsite workshop next week. Worth signing up?",
            "gold": (
                "Decline the full-day standing onsite workshop for now. Extended standing-desk stretches without sit breaks "
                "have left your lower back tight the next morning, and your chiropractor advised capping consecutive standing "
                "hours during flare weeks. The seated virtual webinar signup chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Long standing blocks have bothered your "
                "lower back, but I cannot tell from the available memory whether consecutive standing hours are currently "
                "restricted. Confirm any chiropractor guidance before signing up."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your chiropractor advised "
                    "capping consecutive standing hours during flare weeks, but the available memory does not establish "
                    "that extended standing-desk stretches bother your lower back. I cannot reject the workshop from "
                    "clinical guidance alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Long standing blocks have bothered "
                    "your lower back, but I cannot tell from the available memory whether consecutive standing hours are "
                    "currently restricted. Confirm any chiropractor guidance before signing up."
                ),
            },
            "required": [
                "links extended standing-desk blocks to next-morning lower-back tightness",
                "links chiropractor guidance to cap consecutive standing hours",
                "recommends declining the full-day standing workshop signup",
            ],
            "absence_required": [
                "states that the standing-hour restriction is missing",
                "does not infer harm from the workshop invite alone",
                "explicitly abstains or asks about chiropractor guidance",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the standing-desk back-response evidence is missing",
                    "does not infer back harm from the workshop invite alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the standing-hour restriction is missing",
                    "does not infer harm from the workshop invite alone",
                    "explicitly abstains or asks about chiropractor guidance",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "standing_back_flare", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "consecutive_standing_cap", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "standing_workshop_poor_fit", "hop": 2},
            ],
            "forbidden": ["back ban forever", "must never stand", "skip all workshops"],
            "distractor": {
                "timestamp": "2026-06-12T09:15:00Z",
                "user": f"{ca} said a full-day standing onsite workshop signup next week is amazing hype and worth signing up for career visibility — everyone is pushing it.",
                "assistant": "A standing workshop signup is a different format from a seated webinar.",
                "why": "Standing workshop signup hype is query-similar FOMO but not evidence about this user's standing-desk back pattern or chiropractor standing-hour cap.",
            },
            "evolving": {"standing_pattern": "back_flare_after_long_blocks", "chiro_limit": "cap_consecutive_standing_hours"},
        },
        "S7": {
            "name": "morning_focus_block_x_tuesday_exec_sync",
            "prefix_end": 44,
            "evidence": {
                "ev_A": {
                    "session_id": 40,
                    "fact": "Dense spec review needs an uninterrupted 8-11am block; mid-morning pings wreck nested context.",
                },
                "ev_B": {
                    "session_id": 42,
                    "fact": "Manager scheduled a weekly leadership opener at the start of Tuesday blocks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-26T18:20:00Z",
            "query": "Leadership keeps adding a nine-o'clock Tuesday visibility opener to my calendar. Worth keeping it?",
            "gold": (
                "Push back or negotiate moving the nine-o'clock Tuesday visibility opener. Dense spec review needs an "
                "uninterrupted 8-11am block and mid-morning pings wreck nested context, but leadership already scheduled "
                "a weekly Tuesday opener at the start of the day. Protect the focus block or accept lower review quality. "
                "The Friday social coffee sync hype is a different outing."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the nine-o'clock Tuesday visibility opener fits. Dense morning "
                "review needs an uninterrupted block, but I cannot tell from the available memory whether a weekly Tuesday "
                "opener is already locked in. Confirm calendar placement before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a weekly Tuesday leadership opener "
                    "is on the calendar, but the available memory does not establish that dense morning review needs an "
                    "uninterrupted block. I cannot reject the opener from calendar facts alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the nine-o'clock Tuesday visibility opener fits. Dense morning "
                    "review needs an uninterrupted block, but I cannot tell from the available memory whether a weekly Tuesday "
                    "opener is already locked in. Confirm calendar placement before deciding."
                ),
            },
            "required": [
                "uses dense morning review needing an uninterrupted 8-11am block",
                "uses weekly Tuesday leadership opener on the calendar",
                "recommends pushing back or protecting the focus block",
            ],
            "absence_required": [
                "states that the recurring-sync evidence is missing",
                "does not infer focus harm from the invite alone",
                "asks about calendar placement or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the morning-focus-block evidence is missing",
                    "does not infer review harm from the sync invite alone",
                    "explicitly abstains from rejecting the sync",
                ],
                "ev_B": [
                    "states that the recurring-sync evidence is missing",
                    "does not infer focus harm from the invite alone",
                    "asks about calendar placement or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "requires", "target": "uninterrupted_morning_block", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "tuesday_9am_exec_sync", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "exec_sync_threatens_focus", "hop": 2},
            ],
            "forbidden": ["never attend meetings", "must quit leadership sync", "meetings always bad"],
            "distractor": {
                "timestamp": "2026-06-23T11:00:00Z",
                "user": f"{cb} said a Friday social coffee sync signup is amazing hype and worth keeping as optional visibility before a busy Tuesday week with leadership calendar adds.",
                "assistant": "A social coffee sync is a different calendar slot.",
                "why": "Friday coffee sync hype shares visibility surface but is not evidence about this user's morning focus block or Tuesday leadership opener.",
            },
            "evolving": {"morning_focus": "needs_8_11_block", "leadership_opener": "tuesday_nine_recurring"},
        },
        "S8": {
            "name": "async_writing_strength_x_live_panel_moderation",
            "prefix_end": 49,
            "evidence": {
                "ev_A": {
                    "session_id": 45,
                    "fact": "Best client memos come from async written prep, not live improvisation under lights.",
                },
                "ev_B": {
                    "session_id": 47,
                    "fact": "Last live panel moderation went poorly — the user lost the thread and client follow-up suffered.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-05T16:30:00Z",
            "query": "Client team wants me to moderate their live panel next Thursday. Worth volunteering?",
            "gold": (
                "Decline or renegotiate to an async written role. Your best client memos come from async written prep, not live "
                "improvisation, and your last live panel moderation went poorly with weak client follow-up. Offer a prepared "
                "brief or written commentary instead. The recorded async commentary signup is a different format."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether live panel moderation fits. Async written prep has produced "
                "your strongest client memos, but I cannot tell from the available memory whether live moderation has failed "
                "before. Confirm your live-format track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your last live panel moderation "
                    "went poorly, but the available memory does not establish that async written prep is your strongest format. "
                    "I cannot reject live moderation from one bad session alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether live panel moderation fits. Async written prep has produced "
                    "your strongest client memos, but I cannot tell from the available memory whether live moderation has failed "
                    "before. Confirm your live-format track record before volunteering."
                ),
            },
            "required": [
                "uses async written prep as strongest client output format",
                "uses prior live panel moderation failure and weak follow-up",
                "recommends declining or shifting to async written contribution",
            ],
            "absence_required": [
                "states that the live-moderation failure evidence is missing",
                "does not infer skill gap from the invite alone",
                "asks about live track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the async-writing strength evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "explicitly abstains from rejecting moderation",
                ],
                "ev_B": [
                    "states that the live-moderation failure evidence is missing",
                    "does not infer skill gap from the invite alone",
                    "asks about live track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "async_written_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "live_moderation_weakness", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "live_panel_poor_fit", "hop": 2},
            ],
            "forbidden": ["never speak in public", "must reject all clients", "live format always fails"],
            "distractor": {
                "timestamp": "2026-07-03T14:00:00Z",
                "user": f"{ca} said volunteering to moderate the client's live panel slot next Thursday is amazing hype and worth it for visibility — the team is pushing it hard.",
                "assistant": "Live panel volunteering is a different ask from recorded commentary.",
                "why": "Live panel volunteering hype shares client-visibility surface but is not evidence about this user's async writing strength or live moderation weakness.",
            },
            "evolving": {"client_output": "async_written_strength", "live_moderation": "prior_failure"},
        },
        "S9": {
            "name": "red_eye_jetlag_x_monday_board_dryrun",
            "prefix_end": 54,
            "evidence": {
                "ev_A": {
                    "session_id": 50,
                    "fact": "Overnight return flights leave the user cognitively flat through the next full workday.",
                },
                "ev_B": {
                    "session_id": 52,
                    "fact": "Board rehearsal is locked Monday 10am right after the weekend trip.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-12T20:45:00Z",
            "query": "Worth taking a late Sunday return flight to make Monday's board rehearsal?",
            "gold": (
                "Do not take the late Sunday return flight for Monday's board rehearsal. Overnight return flights leave you "
                "cognitively flat through the next full workday, and the board rehearsal is locked Monday 10am right after "
                "the weekend trip. Fly back earlier or shift the rehearsal. The Sunday afternoon keynote ticket is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a late Sunday return fits Monday's load. Overnight return "
                "flights have left you cognitively flat, but I cannot tell from the available memory when the board rehearsal "
                "is scheduled. Confirm Monday calendar timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the board rehearsal is locked "
                    "Monday 10am, but the available memory does not establish that overnight return flights leave you cognitively "
                    "flat. I cannot reject the flight from calendar timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a late Sunday return fits Monday's load. Overnight return "
                    "flights have left you cognitively flat, but I cannot tell from the available memory when the board rehearsal "
                    "is scheduled. Confirm Monday calendar timing before deciding."
                ),
            },
            "required": [
                "uses overnight return flight causing next-day cognitive flatness",
                "uses Monday 10am board rehearsal deadline",
                "recommends against the late Sunday return for Monday rehearsal",
            ],
            "absence_required": [
                "states that the board dry-run timing evidence is missing",
                "does not infer cognitive harm from the plan alone",
                "asks about Monday timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the red-eye cognitive-flat evidence is missing",
                    "does not infer Monday harm from the travel plan alone",
                    "explicitly abstains from rejecting the flight",
                ],
                "ev_B": [
                    "states that the board dry-run timing evidence is missing",
                    "does not infer cognitive harm from the plan alone",
                    "asks about Monday timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "next_day_cognitive_flat", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_board_dryrun", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "red_eye_conflicts_board_prep", "hop": 2},
            ],
            "forbidden": ["never travel", "cancel the board meeting", "flying is always unsafe"],
            "distractor": {
                "timestamp": "2026-07-11T15:00:00Z",
                "user": f"{cb} said a Sunday afternoon keynote ticket signup is amazing hype and worth grabbing before Monday's board week for visibility.",
                "assistant": "A keynote ticket is a separate leisure decision.",
                "why": "Sunday keynote signup shares weekend-before-Monday surface but is not evidence about this user's red-eye cognitive flatness or board dry-run deadline.",
            },
            "evolving": {"overnight_return": "next_day_cognitive_flat", "board_rehearsal": "monday_10am_locked"},
        },
        "S10": {
            "name": "channel_interrupts_x_desk_side_sprint",
            "prefix_end": 59,
            "evidence": {
                "ev_A": {
                    "session_id": 55,
                    "fact": "Constant channel pings during focus blocks make the user lose nested context and ship sloppy commits.",
                },
                "ev_B": {
                    "session_id": 57,
                    "fact": "Prior constant-interruption sprint week correlated with a measurable defect and rollback spike.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-21T06:50:00Z",
            "query": "Platform team is hyping a five-day desk-side collaboration sprint signup. Worth joining?",
            "gold": (
                "Skip the five-day desk-side collaboration sprint signup. Constant channel pings during focus blocks make you "
                "lose nested context and ship sloppy commits, and a prior constant-interruption sprint week already correlated "
                "with a defect and rollback spike on your lane. The café coworking day signup is a different public outing."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the desk-side sprint fits your week. Focus blocks are sensitive "
                "to channel interruptions, but I cannot tell from the available memory whether a prior constant-interruption sprint "
                "week hurt quality on your lane. Confirm sprint format before joining."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior constant-interruption sprint "
                    "week correlated with defects and rollbacks, but the available memory does not establish that channel pings during "
                    "focus blocks hurt your commit quality. I cannot reject the sprint from prior defects alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the desk-side sprint fits your week. Focus blocks are sensitive "
                    "to channel interruptions, but I cannot tell from the available memory whether a prior constant-interruption sprint "
                    "week hurt quality on your lane. Confirm sprint format before joining."
                ),
            },
            "required": [
                "uses channel pings during focus blocks harming nested context",
                "uses prior constant-interruption sprint week defect/rollback spike",
                "recommends skipping the five-day desk-side sprint signup",
            ],
            "absence_required": [
                "states that the prior war-room quality evidence is missing",
                "does not infer quality harm from the signup alone",
                "asks about war-room format or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the Slack-interrupt focus evidence is missing",
                    "does not infer quality harm from the signup alone",
                    "explicitly abstains from rejecting the war room",
                ],
                "ev_B": [
                    "states that the prior war-room quality evidence is missing",
                    "does not infer quality harm from the signup alone",
                    "asks about war-room format or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "slack_interrupt_context_loss", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "war_room_quality_spike", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "war_room_threatens_quality", "hop": 2},
            ],
            "forbidden": ["never use Slack", "cancel the sprint", "team collaboration is unsafe"],
            "distractor": {
                "timestamp": "2026-07-19T18:30:00Z",
                "user": f"{ca} said a five-day desk-side collaboration sprint signup is amazing hype and worth joining before the release review week — everyone on the platform team is pushing it.",
                "assistant": "A desk-side sprint signup is a different format from a café coworking day.",
                "why": "Desk-side sprint signup hype shares query surface but is not evidence about this user's channel interrupt sensitivity or prior sprint quality spike.",
            },
            "evolving": {"focus_blocks": "channel_interrupt_sensitive", "desk_side_sprint": "prior_defect_spike"},
        },
        "S11": {
            "name": "video_call_strain_x_client_keynote_dryrun",
            "prefix_end": 65,
            "evidence": {
                "ev_A": {
                    "session_id": 61,
                    "fact": "Back-to-back video-call days leave the user's voice strained for next-day presentations; async memo days are fine.",
                },
                "ev_B": {
                    "session_id": 63,
                    "fact": "Client keynote dry-run Thursday at nine is non-negotiable.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-01T10:30:00Z",
            "query": "Worth accepting consecutive lens-on blocks this week given Thursday's client presentation rehearsal?",
            "gold": (
                "Decline the consecutive lens-on blocks for now. Back-to-back video-call days have left your voice strained for "
                "next-day presentations, but client keynote dry-run Thursday at nine is non-negotiable. Protect voice recovery "
                "or shift lens-on blocks earlier in the week. The seated webinar signup chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Stacked video-call days have strained your "
                "voice, but I cannot tell from the available memory whether Thursday's client presentation rehearsal is "
                "currently protected. Confirm your presentation schedule before accepting camera blocks."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know client keynote dry-run Thursday "
                    "at nine is non-negotiable, but the available memory does not establish that stacked video-call days strain "
                    "your voice. I cannot reject camera blocks from calendar timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Stacked video-call days have strained your "
                    "voice, but I cannot tell from the available memory whether Thursday's client presentation rehearsal is "
                    "currently protected. Confirm your presentation schedule before accepting camera blocks."
                ),
            },
            "required": [
                "links stacked video-call days to next-day voice strain",
                "links Thursday client keynote dry-run as non-negotiable",
                "recommends declining consecutive lens-on blocks",
            ],
            "absence_required": [
                "states that the keynote dry-run protection evidence is missing",
                "does not infer voice harm from the calendar invite alone",
                "explicitly abstains or asks about presentation schedule",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the video-call voice-strain evidence is missing",
                    "does not infer presentation harm from the invite alone",
                    "explicitly abstains from rejecting camera blocks",
                ],
                "ev_B": [
                    "states that the keynote dry-run protection evidence is missing",
                    "does not infer voice harm from the calendar invite alone",
                    "explicitly abstains or asks about presentation schedule",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "video_call_voice_strain", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "thursday_keynote_dryrun", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "camera_blocks_poor_fit", "hop": 2},
            ],
            "forbidden": ["video ban forever", "must never present", "skip all client work"],
            "distractor": {
                "timestamp": "2026-05-08T11:00:00Z",
                "user": f"{ca} said consecutive lens-on blocks this week are amazing hype and worth accepting for team visibility before Thursday's client week.",
                "assistant": "Visibility blocks and voice recovery are different ledgers.",
                "why": "Camera-block signup hype is query-similar FOMO but not evidence about this user's video-call voice strain or Thursday keynote dry-run.",
            },
            "evolving": {"video_calls": "voice_strain_next_day", "keynote_dryrun": "thursday_nine_locked"},
        },
        "S12": {
            "name": "pair_programming_x_design_doc_deadline",
            "prefix_end": 71,
            "evidence": {
                "ev_A": {
                    "session_id": 67,
                    "fact": "Afternoon pair-programming rotations wreck the user's solo architecture focus for hours; short syncs are fine.",
                },
                "ev_B": {
                    "session_id": 69,
                    "fact": "Architecture design-doc deadline Friday noon requires protected solo blocks Wednesday and Thursday.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-12T18:20:00Z",
            "query": "Thinking of adding the afternoon shared-keyboard block before this week's architecture write-up push — good idea?",
            "gold": (
                "Do not add the afternoon shared-keyboard block before this week's architecture write-up push. Afternoon "
                "pair-programming rotations have wrecked your solo architecture focus for hours, and the design-doc deadline "
                "Friday noon requires protected solo blocks Wednesday and Thursday. Keep short syncs only or wait until after "
                "the review. The platform pairing streak hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether afternoon pairing fits the architecture write-up push. "
                "Pair-programming rotations have wrecked solo focus, but I cannot tell from the available memory whether "
                "Friday's design-doc deadline requires protected solo blocks. Confirm delivery timing before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the design-doc deadline Friday "
                    "noon requires protected solo blocks, but the available memory does not establish that afternoon pairing "
                    "wrecks your solo architecture focus. I cannot reject pairing from deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether afternoon pairing fits the architecture write-up push. "
                    "Pair-programming rotations have wrecked solo focus, but I cannot tell from the available memory whether "
                    "Friday's design-doc deadline requires protected solo blocks. Confirm delivery timing before committing."
                ),
            },
            "required": [
                "uses afternoon pairing wrecking solo architecture focus",
                "uses Friday design-doc deadline needing protected solo blocks",
                "recommends against afternoon shared-keyboard block before write-up push",
            ],
            "absence_required": [
                "states that the design-doc solo-block evidence is missing",
                "does not infer focus harm from the rotation invite alone",
                "asks about delivery timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the pairing solo-focus evidence is missing",
                    "does not infer architecture harm from the rotation alone",
                    "explicitly abstains from rejecting pairing",
                ],
                "ev_B": [
                    "states that the design-doc solo-block evidence is missing",
                    "does not infer focus harm from the rotation invite alone",
                    "asks about delivery timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "pairing_wrecks_solo_focus", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "design_doc_solo_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pairing_before_writeup_risky", "hop": 2},
            ],
            "forbidden": ["pairing always harmful", "must skip collaboration", "deadlines always unsafe"],
            "distractor": {
                "timestamp": "2026-05-20T11:00:00Z",
                "user": f"{cb} said adding an afternoon shared-keyboard block before this week's architecture write-up push is amazing hype and worth it for team bonding.",
                "assistant": "Pairing streak hype is loud.",
                "why": "Afternoon pairing rotation hype shares delivery-week surface but is not evidence about this user's solo-focus wreck pattern or design-doc solo blocks.",
            },
            "evolving": {"pair_programming": "afternoon_wrecks_solo_focus", "design_doc": "friday_noon_solo_blocks"},
        },
        "S13": {
            "name": "late_cert_cram_x_oncall_rotation",
            "prefix_end": 76,
            "evidence": {
                "ev_A": {
                    "session_id": 72,
                    "fact": "Late-night certification cram sessions wreck the user's alert responsiveness the next morning; morning study blocks are fine.",
                },
                "ev_B": {
                    "session_id": 74,
                    "fact": "On-call rotation starts Monday with strict paging expectations.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-19T09:15:00Z",
            "query": "Training group added midnight skill drills before next week's duty roster — one-off worth testing?",
            "gold": (
                "Skip the midnight skill drills before next week's duty roster. Late-night certification cram sessions "
                "have wrecked your alert responsiveness the next morning, and on-call rotation starts Monday with strict "
                "paging expectations. Use morning study blocks or wait until after rotation week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether late cert-study blocks fit next week's pager rotation. "
                "Late-night cram has wrecked morning alert response, but I cannot tell from the available memory when "
                "on-call rotation starts or how strict paging is. Confirm rotation timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know on-call rotation starts Monday "
                    "with strict paging expectations, but the available memory does not establish that late-night cram wrecks "
                    "your alert responsiveness. I cannot reject study blocks from rotation alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether late cert-study blocks fit next week's pager rotation. "
                    "Late-night cram has wrecked morning alert response, but I cannot tell from the available memory when "
                    "on-call rotation starts or how strict paging is. Confirm rotation timing before deciding."
                ),
            },
            "required": [
                "uses late-night cert cram wrecking morning alert response",
                "uses Monday on-call rotation with strict paging",
                "recommends against midnight skill drills before duty roster",
            ],
            "absence_required": [
                "states that the on-call rotation timing evidence is missing",
                "does not infer alert harm from the study invite alone",
                "asks about rotation timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-cram alert-response evidence is missing",
                    "does not infer paging harm from the study blocks alone",
                    "explicitly abstains from rejecting study blocks",
                ],
                "ev_B": [
                    "states that the on-call rotation timing evidence is missing",
                    "does not infer alert harm from the study invite alone",
                    "asks about rotation timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_cram_wrecks_alert_response", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_oncall_strict_paging", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "late_study_conflicts_oncall", "hop": 2},
            ],
            "forbidden": ["cert ban", "must skip on-call", "study always unsafe"],
            "distractor": {
                "timestamp": "2026-06-02T14:00:00Z",
                "user": f"{ca} said midnight skill drills before next week's duty roster are amazing hype and worth it for credential momentum.",
                "assistant": "Credential momentum and paging readiness are different ledgers.",
                "why": "Late cert-study hype shares rotation-week surface but is not evidence about this user's late-cram alert pattern or Monday on-call paging expectations.",
            },
            "evolving": {"cert_study": "late_cram_wrecks_alerts", "oncall_rotation": "monday_strict_paging"},
        },
        "S14": {
            "name": "hot_desk_noise_x_policy_draft_deadline",
            "prefix_end": 81,
            "evidence": {
                "ev_A": {
                    "session_id": 77,
                    "fact": "Open-office hot-desk days destroy focus for dense policy drafting; quiet home blocks are fine.",
                },
                "ev_B": {
                    "session_id": 79,
                    "fact": "Quiet policy draft is due Wednesday and needs a deep writing block without open-office churn.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-27T06:50:00Z",
            "query": "Worth trying floor-hopping days before this week's compliance memo deadline?",
            "gold": (
                "Skip the floor-hopping days before this week's compliance memo deadline. Open-office hot-desk days have "
                "destroyed focus for dense policy drafting, and the quiet policy draft due Wednesday needs a deep writing "
                "block without open-office churn. Work from a quiet block or home instead. The facilities forum hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether shared-desk days fit the policy write-up deadline. Hot-desk "
                "days have destroyed drafting focus, but I cannot tell from the available memory whether Wednesday's policy "
                "draft needs a quiet deep-writing block. Confirm draft timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the quiet policy draft due "
                    "Wednesday needs a deep writing block, but the available memory does not establish that hot-desk days "
                    "destroy your drafting focus. I cannot reject shared-desk days from deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether shared-desk days fit the policy write-up deadline. Hot-desk "
                    "days have destroyed drafting focus, but I cannot tell from the available memory whether Wednesday's policy "
                    "draft needs a quiet deep-writing block. Confirm draft timing before deciding."
                ),
            },
            "required": [
                "uses hot-desk days destroying policy drafting focus",
                "uses Wednesday policy draft needing quiet deep-writing block",
                "recommends skipping floor-hopping days before compliance memo deadline",
            ],
            "absence_required": [
                "states that the policy draft quiet-block evidence is missing",
                "does not infer focus harm from the desk invite alone",
                "asks about draft timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the hot-desk focus evidence is missing",
                    "does not infer drafting harm from the desk days alone",
                    "explicitly abstains from rejecting shared-desk days",
                ],
                "ev_B": [
                    "states that the policy draft quiet-block evidence is missing",
                    "does not infer focus harm from the desk invite alone",
                    "asks about draft timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "hot_desk_destroys_draft_focus", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "wednesday_quiet_policy_draft", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "shared_desk_before_deadline_risky", "hop": 2},
            ],
            "forbidden": ["office ban", "must skip all facilities events", "drafting always unsafe"],
            "distractor": {
                "timestamp": "2026-06-12T18:30:00Z",
                "user": f"{ca} said floor-hopping days before this week's compliance memo deadline are worth testing and everyone in the facilities forum is pushing them.",
                "assistant": "Forum defaults are not focus facts.",
                "why": "Shared-desk day hype shares policy-deadline surface but is not evidence about this user's hot-desk focus pattern or Wednesday quiet draft block.",
            },
            "evolving": {"hot_desk": "destroys_draft_focus", "policy_draft": "wednesday_quiet_block"},
        },
        "S15": {
            "name": "weekend_inbox_blitz_x_sabbatical_planning_week",
            "prefix_end": 86,
            "evidence": {
                "ev_A": {
                    "session_id": 82,
                    "fact": "Weekend inbox catch-up blitzes bleed into protected personal planning blocks; weekday triage is fine.",
                },
                "ev_B": {
                    "session_id": 84,
                    "fact": "Sabbatical planning week requires protected Monday half-day blocks for structured planning work.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-04T20:45:00Z",
            "query": "One-off Sunday admin session before next week's personal roadmap week — sensible?",
            "gold": (
                "Skip the Sunday admin session before next week's personal roadmap week. Weekend catch-up blitzes have "
                "bled into protected personal planning blocks, and sabbatical planning week requires protected Monday half-day "
                "blocks for structured planning work. Keep weekday triage or defer admin work until after roadmap week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a weekend inbox sweep fits next week's planning week. "
                "Weekend catch-up blitzes have bled into planning blocks, but I cannot tell from the available memory "
                "whether Monday half-day blocks are already protected. Confirm planning-week calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know sabbatical planning week "
                    "requires protected Monday half-day blocks, but the available memory does not establish that weekend "
                    "inbox blitzes bleed into planning blocks. I cannot reject the sweep from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a weekend inbox sweep fits next week's planning week. "
                    "Weekend catch-up blitzes have bled into planning blocks, but I cannot tell from the available memory "
                    "whether Monday half-day blocks are already protected. Confirm planning-week calendar before deciding."
                ),
            },
            "required": [
                "uses weekend inbox blitz bleeding into protected planning blocks",
                "uses sabbatical planning week requiring Monday half-day blocks",
                "recommends skipping Sunday admin session before roadmap week",
            ],
            "absence_required": [
                "states that the Monday planning-block evidence is missing",
                "does not infer planning harm from the sweep invite alone",
                "asks about planning-week calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the weekend-blitz planning-bleed evidence is missing",
                    "does not infer planning harm from the sweep alone",
                    "explicitly abstains from rejecting the sweep",
                ],
                "ev_B": [
                    "states that the Monday planning-block evidence is missing",
                    "does not infer planning harm from the sweep invite alone",
                    "asks about planning-week calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "weekend_blitz_bleeds_planning", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_halfday_planning_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "weekend_sweep_conflicts_planning", "hop": 2},
            ],
            "forbidden": ["inbox ban forever", "must cancel sabbatical", "weekend work always unsafe"],
            "distractor": {
                "timestamp": "2026-06-22T15:00:00Z",
                "user": f"{cb} said a Sunday admin session before next week's personal roadmap week is amazing hype and worth it for ops visibility.",
                "assistant": "Ops visibility and planning blocks are different decisions.",
                "why": "Weekend inbox sweep hype shares planning-week surface but is not evidence about this user's weekend-blitz planning bleed or Monday half-day blocks.",
            },
            "evolving": {"weekend_inbox": "bleeds_planning_blocks", "sabbatical_planning": "monday_halfday_protected"},
        },
        "S16": {
            "name": "bullpen_chatter_x_diagram_sprint",
            "prefix_end": 91,
            "evidence": {
                "ev_A": {
                    "session_id": 88,
                    "fact": "Open-bullpen ambient chatter wrecks the user's architecture diagramming; quiet-room blocks are fine.",
                },
                "ev_B": {
                    "session_id": 90,
                    "fact": "Diagram sprint week needs protected morning solo blocks Tuesday through Thursday.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-10T10:15:00Z",
            "query": "Worth trying the standing huddle loop before Thursday's blueprint lock?",
            "gold": (
                "Skip the standing huddle loop before Thursday's blueprint lock. Open-bullpen ambient chatter "
                "has wrecked your architecture diagramming, and diagram sprint week needs protected morning solo blocks "
                "Tuesday through Thursday. Use quiet-room blocks or defer the huddle loop until after the lock. The facilities "
                "signup blurb chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the standing huddle loop fits before Thursday's blueprint lock. Bullpen "
                "chatter has wrecked diagramming focus, but I cannot tell from the available memory whether Tuesday through "
                "Thursday morning solo blocks are already protected. Confirm the blueprint calendar before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know diagram sprint week needs "
                    "protected morning solo blocks Tuesday through Thursday, but the available memory does not establish "
                    "that bullpen chatter wrecks your diagramming focus. I cannot reject the huddle loop from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the standing huddle loop fits before Thursday's blueprint lock. Bullpen "
                    "chatter has wrecked diagramming focus, but I cannot tell from the available memory whether Tuesday through "
                    "Thursday morning solo blocks are already protected. Confirm the blueprint calendar before deciding."
                ),
            },
            "required": [
                "uses bullpen chatter wrecking architecture diagramming",
                "uses diagram sprint week needing protected morning solo blocks",
                "recommends skipping standing huddle loop before blueprint lock",
            ],
            "absence_required": [
                "states that the diagram-sprint solo-block evidence is missing",
                "does not infer focus harm from the huddle-loop invite alone",
                "asks about blueprint calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the bullpen-diagramming evidence is missing",
                    "does not infer diagram harm from the huddle loop alone",
                    "explicitly abstains from rejecting the huddle loop",
                ],
                "ev_B": [
                    "states that the diagram-sprint solo-block evidence is missing",
                    "does not infer focus harm from the huddle-loop invite alone",
                    "asks about blueprint calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "bullpen_wrecks_diagramming", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "diagram_sprint_solo_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "floor_circle_conflicts_sprint", "hop": 2},
            ],
            "forbidden": ["office ban forever", "must skip all facilities events", "diagramming always unsafe"],
            "distractor": {
                "timestamp": "2026-06-05T11:00:00Z",
                "user": f"{ca} said the standing huddle loop before Thursday's blueprint lock is amazing hype and worth joining for team visibility.",
                "assistant": "Visibility huddles and blueprint lock focus are different ledgers.",
                "why": "Huddle-loop signup hype shares blueprint-lock surface but is not evidence about this user's bullpen chatter pattern or protected morning solo blocks.",
            },
            "evolving": {"bullpen_chatter": "wrecks_diagramming", "diagram_sprint": "tue_thu_morning_solo_blocks"},
        },
        "S17": {
            "name": "full_day_shadowing_x_advancement_dossier",
            "prefix_end": 96,
            "evidence": {
                "ev_A": {
                    "session_id": 93,
                    "fact": "Full-day mentor shadowing leaves the user too drained to finish own deliverables; short office hours are fine.",
                },
                "ev_B": {
                    "session_id": 95,
                    "fact": "Advancement dossier due Friday needs three solo evening writing blocks.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-18T17:30:00Z",
            "query": "Bench-adjacent immersion week before Friday's packet filing cutoff — workable?",
            "gold": (
                "Do not add a bench-adjacent immersion week before Friday's packet filing cutoff. Full-day mentor shadowing "
                "has left you too drained to finish your own deliverables, and the advancement dossier due Friday needs three "
                "solo evening writing blocks. Keep short office hours only or wait until after the filing cutoff. The HR "
                "immersion streak hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a bench-adjacent immersion week fits the packet filing push. "
                "Full-day shadowing has drained deliverable energy, but I cannot tell from the available memory whether Friday's "
                "filing cutoff needs three solo evening blocks. Confirm filing timing before committing."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the advancement dossier due Friday "
                    "needs three solo evening writing blocks, but the available memory does not establish that full-day shadowing "
                    "drains your deliverable energy. I cannot reject immersion from deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a bench-adjacent immersion week fits the packet filing push. "
                    "Full-day shadowing has drained deliverable energy, but I cannot tell from the available memory whether Friday's "
                    "filing cutoff needs three solo evening blocks. Confirm filing timing before committing."
                ),
            },
            "required": [
                "uses full-day shadowing draining deliverable energy",
                "uses Friday advancement dossier needing solo evening blocks",
                "recommends against bench-adjacent immersion week before filing cutoff",
            ],
            "absence_required": [
                "states that the dossier solo-evening-block evidence is missing",
                "does not infer energy harm from the immersion invite alone",
                "asks about filing timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the shadowing energy-drain evidence is missing",
                    "does not infer filing harm from the immersion alone",
                    "explicitly abstains from rejecting immersion",
                ],
                "ev_B": [
                    "states that the dossier solo-evening-block evidence is missing",
                    "does not infer energy harm from the immersion invite alone",
                    "asks about filing timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "shadowing_drains_deliverables", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dossier_solo_evening_blocks", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "ridealong_conflicts_dossier", "hop": 2},
            ],
            "forbidden": ["mentorship ban", "must skip all shadowing", "deadlines always unsafe"],
            "distractor": {
                "timestamp": "2026-06-08T14:00:00Z",
                "user": f"{cb} said a bench-adjacent immersion week before Friday's packet filing cutoff is amazing hype and worth it for career visibility.",
                "assistant": "Career visibility and packet filing blocks are different ledgers.",
                "why": "Immersion week hype shares filing-cutoff surface but is not evidence about this user's shadowing energy drain or solo evening blocks.",
            },
            "evolving": {"mentor_shadowing": "full_day_drains_deliverables", "advancement_dossier": "friday_solo_evening_blocks"},
        },
        "S18": {
            "name": "afternoon_espresso_x_weekend_build_sprint",
            "prefix_end": 101,
            "evidence": {
                "ev_A": {
                    "session_id": 98,
                    "fact": "Extra espresso after 2pm causes jittery nights and ruins next-morning clarity; morning tea is fine.",
                },
                "ev_B": {
                    "session_id": 100,
                    "fact": "Midweek readiness checkpoint needs sharp morning clarity; a late-slot obligation is booked through the night before.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-28T11:40:00Z",
            "query": "Hall crew added a dusk-to-dawn maker signup — sensible with Thursday's review lock ahead?",
            "gold": (
                "Skip the dusk-to-dawn maker signup before Thursday's review lock. Extra espresso after 2pm has caused "
                "jittery nights and ruined next-morning clarity, and midweek readiness checkpoint needs a sharp morning clarity "
                "block while a late-slot obligation is already booked through the night before. Protect sleep and morning "
                "clarity or defer the signup until after the review lock."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a dusk-to-dawn maker signup fits before Thursday's review lock. "
                "Afternoon espresso has ruined next-morning clarity, but I cannot tell from the available memory whether "
                "midweek readiness checkpoint needs a sharp morning clarity block. Confirm checkpoint timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know midweek readiness checkpoint needs "
                    "sharp morning clarity while a late-slot obligation is booked through the night before, but the available "
                    "memory does not establish that afternoon espresso ruins next-morning clarity. I cannot reject the signup "
                    "from checkpoint timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a dusk-to-dawn maker signup fits before Thursday's review lock. "
                    "Afternoon espresso has ruined next-morning clarity, but I cannot tell from the available memory whether "
                    "midweek readiness checkpoint needs a sharp morning clarity block. Confirm checkpoint timing before deciding."
                ),
            },
            "required": [
                "uses afternoon espresso ruining next-morning clarity",
                "uses midweek readiness checkpoint needing sharp morning clarity",
                "recommends against dusk-to-dawn maker signup before review lock",
            ],
            "absence_required": [
                "states that the readiness-checkpoint clarity-block evidence is missing",
                "does not infer clarity harm from the signup invite alone",
                "asks about checkpoint timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the afternoon-espresso clarity evidence is missing",
                    "does not infer gate harm from the signup alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the readiness-gate clarity-block evidence is missing",
                    "does not infer clarity harm from the signup invite alone",
                    "asks about gate timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_espresso_wrecks_morning_clarity", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_review_sharp_morning", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "weekend_sprint_conflicts_review", "hop": 2},
            ],
            "forbidden": ["caffeine ban forever", "must skip all vendor events", "review always unsafe"],
            "distractor": {
                "timestamp": "2026-06-15T16:30:00Z",
                "user": f"{ca} said the dusk-to-dawn maker signup before Thursday's review lock is amazing hype and worth it for credential momentum.",
                "assistant": "Credential momentum and review-lock clarity are different ledgers.",
                "why": "Hall maker-signup hype shares review-lock surface but is not evidence about this user's afternoon-espresso clarity pattern or midweek checkpoint clarity block.",
            },
            "evolving": {"afternoon_espresso": "wrecks_morning_clarity", "readiness_checkpoint": "midweek_sharp_morning_clarity"},
        },
        "S19": {
            "name": "spreadsheet_grid_x_figures_briefing",
            "prefix_end": 106,
            "evidence": {
                "ev_A": {
                    "session_id": 103,
                    "fact": "The user thinks best in spreadsheet grid layouts; wall-chart-only prep sessions produce weak outputs.",
                },
                "ev_B": {
                    "session_id": 105,
                    "fact": "A prior wall-chart-only figures rehearsal went poorly before the exec briefing.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-07T16:20:00Z",
            "query": "Leadership wants me on the poster-board run-through for next week's numbers session — good fit?",
            "gold": (
                "Decline or renegotiate to a spreadsheet-grid prep role. You think best in spreadsheet grid layouts and a "
                "prior wall-chart-only figures rehearsal went poorly before the exec briefing. Offer a grid-based walkthrough "
                "or prepared memo instead. The leadership forum hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a poster-board run-through fits next week's numbers session. "
                "Spreadsheet grid prep has produced your strongest outputs, but I cannot tell from the available memory whether "
                "a prior wall-chart-only rehearsal failed. Confirm your poster-board track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior wall-chart-only figures "
                    "rehearsal went poorly, but the available memory does not establish that spreadsheet grid layouts are your "
                    "strongest prep format. I cannot reject the run-through from one bad session alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a poster-board run-through fits next week's numbers session. "
                    "Spreadsheet grid prep has produced your strongest outputs, but I cannot tell from the available memory "
                    "whether a prior wall-chart-only rehearsal failed. Confirm your poster-board track record before volunteering."
                ),
            },
            "required": [
                "uses spreadsheet grid layouts as strongest prep format",
                "uses prior wall-chart-only figures rehearsal failure",
                "recommends declining or shifting away from poster-board run-through",
            ],
            "absence_required": [
                "states that the wall-chart rehearsal failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about poster-board track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the spreadsheet-grid prep evidence is missing",
                    "does not infer briefing harm from the walkthrough alone",
                    "explicitly abstains from rejecting the walkthrough",
                ],
                "ev_B": [
                    "states that the wall-chart rehearsal failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about wall-chart track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "spreadsheet_grid_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "wall_chart_rehearsal_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "wall_chart_walkthrough_poor_fit", "hop": 2},
            ],
            "forbidden": ["spreadsheet ban", "must skip all briefings", "presentations always unsafe"],
            "distractor": {
                "timestamp": "2026-06-20T18:00:00Z",
                "user": f"{ca} said the poster-board run-through for next week's numbers session is amazing hype and everyone in the leadership forum is pushing it.",
                "assistant": "Forum defaults are not prep facts.",
                "why": "Poster-board run-through hype shares numbers-session surface but is not evidence about this user's spreadsheet-grid strength or prior wall-chart rehearsal failure.",
            },
            "evolving": {"prep_format": "spreadsheet_grid_strength", "figures_briefing": "wall_chart_rehearsal_failed"},
        },
        "S20": {
            "name": "rush_hour_commute_x_distant_client_site",
            "prefix_end": 111,
            "evidence": {
                "ev_A": {
                    "session_id": 108,
                    "fact": "Long rush-hour commutes drain the user's cognitive energy before deep work; short bike rides are fine.",
                },
                "ev_B": {
                    "session_id": 110,
                    "fact": "New client site rhythm requires ninety-minute each-way transit on collaboration days.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-17T18:10:00Z",
            "query": "Worth accepting the heavier daily corridor time for the relocated account cadence — based on what you know about me?",
            "gold": (
                "Lean no unless corridor time is shortened or collaboration days are reduced. Long rush-hour commutes have drained "
                "your cognitive energy before deep work, and the new client site rhythm requires ninety-minute each-way transit "
                "on collaboration days. Negotiate remote collaboration or a nearer cadence rather than accepting unchanged."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Long commutes have drained cognitive energy, "
                "but I cannot tell from the available memory whether the relocated account cadence requires ninety-minute each-way "
                "corridor time. Confirm daily corridor load before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the new client site rhythm "
                    "requires ninety-minute each-way transit on collaboration days, but the available memory does not establish "
                    "that long commutes drain your cognitive energy. I cannot reject the cadence from corridor facts alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Long commutes have drained cognitive energy, "
                    "but I cannot tell from the available memory whether the relocated account cadence requires ninety-minute each-way "
                    "corridor time. Confirm daily corridor load before deciding."
                ),
            },
            "required": [
                "uses long rush-hour commute draining cognitive energy",
                "uses new client site requiring ninety-minute each-way transit",
                "recommends declining or negotiating away heavier daily corridor time",
            ],
            "absence_required": [
                "states that the distant-site transit evidence is missing",
                "does not infer energy harm from the cadence memo alone",
                "asks about corridor load or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the commute energy-drain evidence is missing",
                    "does not infer deep-work harm from the site rhythm alone",
                    "explicitly abstains from rejecting the transit leg",
                ],
                "ev_B": [
                    "states that the distant-site transit evidence is missing",
                    "does not infer energy harm from the site memo alone",
                    "asks about transit load or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "commute_drains_cognitive_energy", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "ninety_min_each_way_transit", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "distant_site_poor_fit", "hop": 2},
            ],
            "forbidden": ["commute ban forever", "must reject all client sites", "remote only forever"],
            "distractor": {
                "timestamp": "2026-06-25T09:30:00Z",
                "user": f"{cb} said accepting the heavier daily corridor time for the relocated account cadence is amazing hype and worth it for career visibility on the account.",
                "assistant": "Account visibility and corridor energy are different ledgers.",
                "why": "Heavier corridor-time hype shares account-cadence surface but is not evidence about this user's commute energy drain or ninety-minute each-way transit requirement.",
            },
            "evolving": {"commute_load": "rush_hour_drains_energy", "client_site": "ninety_min_each_way"},
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
    if raw in {"S1-S15", "1-15"}:
        return tuple(f"S{i}" for i in range(1, 16))
    if raw in {"S1-S20", "1-20"}:
        return tuple(f"S{i}" for i in range(1, 21))
    if raw in {"S6-S15", "6-15"}:
        return tuple(f"S{i}" for i in range(6, 16))
    if raw in {"S11-S20", "11-20"}:
        return tuple(f"S{i}" for i in range(11, 21))
    if "," in raw:
        return tuple(part.strip() for part in raw.split(",") if part.strip())
    return (raw,)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate work/learning gold JSON items.")
    parser.add_argument(
        "--scenarios",
        default="S11-S15",
        help="Scenario scope: S1-S5, S6-S10, S11-S15, S16-S20, S1-S20, etc.",
    )
    args = parser.parse_args(argv)
    scenario_ids = parse_scenario_ids(args.scenarios)
    if scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        batch_config = {
            **WL_BATCH_CONFIG,
            "batch_id": "WL_GOLD_S16_S20_2026-07-16_v2",
            "generator_name": "work_learn_gold_s16_s20_v2",
        }
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **WL_BATCH_CONFIG,
            "batch_id": "WL_GOLD_S11_S15_2026-07-15_v2",
            "generator_name": "work_learn_gold_s11_s15_v2",
        }
    elif scenario_ids == ("S1", "S2", "S3", "S4", "S5"):
        batch_config = {
            **WL_BATCH_CONFIG,
            "batch_id": "WL_GOLD_S1_S5_2026-07-16_v2",
            "generator_name": "work_learn_gold_s1_s5_v2",
        }
    else:
        batch_config = WL_BATCH_CONFIG
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
    manifest_dir = PILOT_ROOT / "manifests" / "work"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    report_path = manifest_dir / (
        "work_learn_gold_s16_s20_report.json"
        if scenario_ids == ("S16", "S17", "S18", "S19", "S20")
        else "work_learn_gold_s11_s15_report.json"
        if scenario_ids == ("S11", "S12", "S13", "S14", "S15")
        else "work_learn_gold_s1_s5_report.json"
        if scenario_ids == ("S1", "S2", "S3", "S4", "S5")
        else "work_learn_gold_s6_s10_report.json"
    )
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nSUMMARY {n_pass}/{n} hard-gate PASS")
    print(
        f"SCORES min={report['score_distribution']['min']} "
        f"max={report['score_distribution']['max']} "
        f"mean={report['score_distribution']['mean']}"
    )
    print(f"AT_95={report['score_distribution']['at_95']}")
    print(f"REPORT {report_path}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

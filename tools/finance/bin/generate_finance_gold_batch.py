#!/usr/bin/env python3
"""Generate finance/personal gold batches (S1–S20; S6–S20 require v3_ultra score≥95).

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

PERSONAS_PATH = DOMAIN / "personas" / "personas_finance.json"
COMPUTED_BY = "tools/finance/bin/generate_finance_gold_batch.py"

FN_BATCH_CONFIG: dict[str, Any] = {
    "id_prefix": "FN",
    "pilot_domain": "finance_personal",
    "domain_tags": ["finance/personal", "everyday_money"],
    "data_subdir": "finance",
    "folder_prefix": "finance",
    "batch_id": "FN_GOLD_S1_S5_2026-07-18_v2",
    "generator_name": "finance_gold_s1_s5_v2",
    "reproduce_generator": "python3 tools/finance/bin/generate_finance_gold_batch.py",
}

USER10_PERSONA: dict[str, Any] = {
    "user_index": 10,
    "user_id": "fn_u10",
    "folder_tag": "user10",
    "display_name": "desktop-Healthy_Li",
    "source_corpus": "desktop_user",
    "source_ref": "local:Healthy Li; migrated from pilot FN",
    "stable_traits": [
        "psychology + AI research student",
        "University of Michigan exchange",
        "King's College London BSc Psychology",
        "tracks cashflow before speculative bets",
        "prioritizes high-interest debt clearance",
    ],
    "voice": "curious, reflective, student-researcher",
}

# Shared cumulative finance timeline (sessions 1–111 for S1–S20)
CANONICAL_TIMELINE = [
    # S1
    session(1, "2026-01-11T18:00:00Z", "Exported last month's ledger CSV. Categories look messy.", "Small tidy passes help."),
    session(2, "2026-01-12T18:00:00Z", "Skipped a flashy tip channel for now. Felt lighter.", "Optional money FOMO can wait."),
    session(3, "2026-01-18T18:00:00Z", "Paid a utility bill early. Boring and fine.", "Boring payments count."),
    session(
        4,
        "2026-01-26T18:00:00Z",
        "A revolving store card is still open at roughly twenty-four percent — minimum payments keep the balance sticky for months.",
        "Has that pattern repeated?",
        "Yes. Twice this year; paying more than the minimum is what actually shrinks it.",
    ),
    session(5, "2026-02-03T18:00:00Z", "Muted a tip-thread for an afternoon. Quiet helped.", "Attention has a ledger."),
    session(
        6,
        "2026-02-10T18:00:00Z",
        "Lease security deposit is due next month — already marked as a hard cash outflow on the calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(7, "2026-02-17T18:00:00Z", "Chat is hyping a speculative tip pool signup this month — everyone saying it is amazing.", "Signup FOMO around spare cash is loud."),
    session(8, "2026-02-24T18:00:00Z", "Someone asked whether parking spare cash in that tip pool is worth it for upside.", "Upside talk and cash obligations are different questions."),
    session(9, "2026-03-02T18:00:00Z", "Printed March money calendar. Deposit week is marked.", "Paper copies help on busy weeks."),
    # S2
    session(10, "2026-03-09T18:00:00Z", "Archived old brokerage statements. Less inbox clutter.", "Digital tidy helps."),
    session(
        11,
        "2026-03-16T18:00:00Z",
        "On sharp red days I have panic-sold broad holdings and then regretted it within a week. Holding through ordinary dips has been fine.",
        "Has the panic-sell pattern repeated?",
        "Yes. Three red-day sells did it; staying on the plan did not.",
    ),
    session(12, "2026-03-23T18:00:00Z", "Short walk after lunch. Cleared the afternoon fog.", "Worth repeating."),
    session(
        13,
        "2026-03-30T18:00:00Z",
        "Paycheck auto-transfers into a broad index fund on payday are the only investing habit that has stuck for me.",
        "Is that habit firm?",
        "Yes. It is already automated.",
    ),
    session(14, "2026-04-06T18:00:00Z", "Someone hyped a one-week day-trading bootcamp. Different beast from a quiet payday plan.", "Signup FOMO comes in many shapes."),
    session(15, "2026-04-13T18:00:00Z", "Trading-group chat is loud. I muted notifications overnight.", "Mute buttons save attention."),
    session(16, "2026-04-20T18:00:00Z", "Printed the payday transfer reminder. Auto-plan is marked in red.", "Paper copies help on busy weeks."),
    # S3
    session(17, "2026-04-27T18:00:00Z", "Declined a last-minute yield-chase invite. Buffer felt thin.", "Boundaries are data."),
    session(
        18,
        "2026-05-04T18:00:00Z",
        "My liquid reserve is under one month of expenses — a surprise bill would force a card swipe.",
        "Has that thin-reserve pattern repeated?",
        "Yes. Twice after surprise bills; a fuller reserve did not.",
    ),
    session(19, "2026-05-11T18:00:00Z", "Wrote a short note about skipping a tip pitch. No reply needed.", "Low-pressure contact counts."),
    session(
        20,
        "2026-05-18T18:00:00Z",
        "A dental procedure with a deductible reset is already on the books — I need money set aside before the appointment.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(21, "2026-05-25T18:00:00Z", "Forum crowd insists parking idle cash for extra return is normal. I disagree.", "Online norms are not cash facts."),
    session(22, "2026-06-01T18:00:00Z", "Someone forwarded hype about parking idle cash for extra return. Not my plan.", "Social pressure is not a schedule."),
    session(23, "2026-06-08T18:00:00Z", "Restocked basic pantry staples. Cash stayed local.", "Small local spends are fine."),
    session(24, "2026-06-15T18:00:00Z", "Printed the procedure-week checklist. Reserved cash is marked.", "Paper copies help on busy weeks."),
    # S4
    session(
        25,
        "2026-06-22T18:00:00Z",
        "Roth contribution room for 2026 is already used — no leftover annual space left to fill.",
        "Has that room been checked?",
        "Yes. The annual limit is already hit.",
    ),
    session(26, "2026-06-29T18:00:00Z", "Filed a short tax folder note. Boring and done.", "Admin tidying counts."),
    session(
        27,
        "2026-07-06T18:00:00Z",
        "A prior December dual-wrapper paperwork sprint left clutter and no useful new contribution room — I blanked on why I opened it.",
        "Was that a one-off?",
        "No. December dual-wrapper sprints have been a weak spot for me.",
    ),
    session(28, "2026-07-13T18:00:00Z", "Desk chat is hyping another December dual-wrapper paperwork sprint. I filed it without replying.", "Invites can wait for a room check."),
    # S5
    session(
        29,
        "2026-07-20T18:00:00Z",
        "Odd months with thinner freelance invoices leave cash gaps — fixed outflows still hit on time.",
        "Has that gap pattern repeated?",
        "Yes. Two thin invoice months did it; steadier months did not.",
    ),
    session(30, "2026-07-27T18:00:00Z", "Canceled one unused trial. Felt like oxygen.", "Small cuts help."),
    session(
        31,
        "2026-08-03T18:00:00Z",
        "Stacked auto-renew memberships are already hard to unwind mid-cycle — mid-cycle cancels rarely stick for me.",
        "Is that stack still active?",
        "Yes. It is already on the calendar of renewals.",
    ),
    session(32, "2026-08-10T18:00:00Z", "Someone hyped a bundled lifestyle membership. Different beast from trimming renewals.", "Signup FOMO comes in many shapes."),
    # S6
    session(33, "2026-08-12T18:00:00Z", "Printed the autumn money calendar. Match deadlines are marked.", "Paper copies help on busy weeks."),
    session(
        34,
        "2026-08-14T20:45:00Z",
        "Employer match on retirement contributions is still unused this pay cycle — only the paycheck remainder counts toward it.",
        "Has that unused-match pattern repeated?",
        "Yes. Twice this quarter; general savings do not earn the match.",
    ),
    session(35, "2026-08-15T13:10:00Z", "Short walk between errands. Nice reset.", "Small movement breaks add up."),
    session(
        36,
        "2026-08-17T08:30:00Z",
        "The paycheck remainder is already marked for the match window closing this Friday — it is not free discretionary money.",
        "Is that earmark firm?",
        "Yes. It is already on the calendar.",
    ),
    session(37, "2026-08-18T16:55:00Z", "Chat posted another speculative hallway invite. I filed it without replying.", "Invites can wait for a match plan."),
    session(38, "2026-08-19T19:20:00Z", "Restocked envelopes for bill sorting. Solo evenings still matter.", "Focus routines are not one-size."),
    # S7
    session(
        39,
        "2026-08-21T21:10:00Z",
        "Saturday and Sunday person-to-person remittances in foreign currency add steep FX fees for me — weekday bank wires have been cheaper.",
        "Has the weekend FX-fee pattern repeated?",
        "Yes. Three weekend P2P sends did it; weekday wires did not.",
    ),
    session(40, "2026-08-22T12:40:00Z", "Short lunch away from the phone. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        41,
        "2026-08-24T08:50:00Z",
        "The first-workday rent draft in euros is already locked — I need the weekday wire path, not a weekend remittance detour.",
        "Is that draft firm?",
        "Yes. It is already scheduled.",
    ),
    session(42, "2026-08-25T14:25:00Z", "Group chat is noisy about weekend investment-club transfers. I muted the thread.", "Mute buttons save attention."),
    # S8
    session(43, "2026-08-27T10:05:00Z", "Printed the estimated-tax checklist. Reserved cash is marked.", "Prep weeks need a clean routine."),
    session(
        44,
        "2026-08-29T15:35:00Z",
        "A prior buy-now-pay-later stack pushed me into overdraft — small card purchases have been fine.",
        "Has the BNPL overdraft pattern repeated?",
        "Yes. Two BNPL stacks did it; ordinary card purchases did not.",
    ),
    session(45, "2026-08-30T11:20:00Z", "Mailer landed. I filed it without replying.", "Invites can wait for a tax plan."),
    session(
        46,
        "2026-09-01T07:15:00Z",
        "Quarterly estimated tax reserve is already earmarked and due before month-end — not available for split payments.",
        "Is that reserve firm?",
        "Yes. The tax calendar is already booked.",
    ),
    session(47, "2026-09-02T16:50:00Z", "Packed notes for the tax filing week. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S9
    session(48, "2026-09-04T18:15:00Z", "HSA balance note is packed. Contribution room is on the calendar.", "Account weeks need protected checks."),
    session(
        49,
        "2026-09-06T22:00:00Z",
        "HSA contribution room for this year is still open — payroll deferrals into it have been the cleanest tax-advantaged use of leftover wages.",
        "Has that HSA-room pattern been checked?",
        "Yes. Room remains and payroll deferral works.",
    ),
    session(50, "2026-09-07T08:00:00Z", "Forum is loud about idle-cash tip channels. I am not adopting forum defaults.", "Forum norms are not tax facts."),
    session(
        51,
        "2026-09-09T16:30:00Z",
        "Elective dental work is already scheduled after deductible is met and counts as HSA-eligible care.",
        "Is that appointment firm?",
        "Yes. It is already booked.",
    ),
    session(52, "2026-09-10T19:40:00Z", "Printed the HSA and appointment calendar. Solo admin blocks are locked.", "Paper copies help on busy weeks."),
    # S10
    session(53, "2026-09-12T18:05:00Z", "Insurance packet landed. I only skimmed the deductible section.", "Not every packet needs a decision."),
    session(
        54,
        "2026-09-14T07:50:00Z",
        "Auto insurance deductible reset means the first repair hit this policy year comes from cash — I keep that rainy fund liquid.",
        "Has that deductible-cash pattern repeated?",
        "Yes. Last claim year taught it; parking that slice elsewhere hurt.",
    ),
    session(55, "2026-09-15T14:15:00Z", "Shop posted a shuttle blurb. I filed it without replying.", "Invites can wait for a repair plan."),
    session(
        56,
        "2026-09-17T09:25:00Z",
        "Inspection flagged a likely brake repair in the next few weeks — already on the garage calendar.",
        "Is that timing firm?",
        "Yes. The garage slot is already booked.",
    ),
    session(57, "2026-09-18T17:30:00Z", "Packed a light bag for the garage visit. Cash timing still feels tight.", "Repair weeks need an energy plan."),
    # S11
    session(58, "2026-09-20T18:00:00Z", "Loan autopay reminder printed. Draft dates are marked.", "Paper copies help on busy weeks."),
    session(
        59,
        "2026-09-22T20:45:00Z",
        "Student-loan autopay draft is locked on the 3rd — spending ahead of an incentive payout before that draft has bounced me before.",
        "Has that pre-bonus spend pattern repeated?",
        "Yes. Twice; waiting until after the draft cleared did not.",
    ),
    session(60, "2026-09-23T13:10:00Z", "Short walk between buildings. Nice reset.", "Small movement breaks add up."),
    session(
        61,
        "2026-09-25T08:30:00Z",
        "Incentive payout is dated after the loan draft — it is not cash I can pre-commit before the draft clears.",
        "Is that payout timing firm?",
        "Yes. Payroll already confirmed the date.",
    ),
    session(62, "2026-09-26T16:55:00Z", "Course vendor posted a hold-the-seat blurb. I filed it without replying.", "Invites can wait for a payout plan."),
    # S12
    session(63, "2026-09-28T19:20:00Z", "Restocked binder tabs for the joint-account sprint. Solo evenings still matter.", "Focus routines are not one-size."),
    session(
        64,
        "2026-09-30T21:10:00Z",
        "Joint household account requires dual approval above a set threshold — unilateral big transfers have been reversed before.",
        "Has the dual-approval pattern repeated?",
        "Yes. Two unilateral tries were reversed; dual-approved moves were fine.",
    ),
    session(65, "2026-10-01T12:40:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        66,
        "2026-10-03T08:50:00Z",
        "Partner already marked the current household window as dual-approval-only for any transfer above the threshold.",
        "Is that window firm?",
        "Yes. It is already on the household calendar.",
    ),
    session(67, "2026-10-04T14:25:00Z", "Friend chat is noisy about speculative side deals. I muted the thread.", "Mute buttons save attention."),
    # S13
    session(68, "2026-10-06T10:05:00Z", "Printed the risk-budget note. Boring index blocks are marked.", "Prep weeks need a clean routine."),
    session(
        69,
        "2026-10-08T15:35:00Z",
        "Buying coins off hype threads has left me with sharp losses before — slow index buys have been fine.",
        "Has the hype-thread loss pattern repeated?",
        "Yes. Three hype buys did it; scheduled index buys did not.",
    ),
    session(70, "2026-10-09T11:20:00Z", "Mailer landed. I filed it without replying.", "Invites can wait for a risk plan."),
    session(
        71,
        "2026-10-11T07:15:00Z",
        "Remaining risk budget this month is already allocated to the boring index schedule — nothing left for discretionary coin calls.",
        "Is that allocation firm?",
        "Yes. It is already booked.",
    ),
    session(72, "2026-10-12T16:50:00Z", "Packed notes for the index buy week. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S14
    session(73, "2026-10-14T18:15:00Z", "Escrow checklist is packed. Wire date is on the calendar.", "Housing weeks need protected checks."),
    session(
        74,
        "2026-10-16T22:00:00Z",
        "Apartment escrow wire already left the account — that cash is committed through move-in, not reusable.",
        "Has that escrow commitment been confirmed?",
        "Yes. The wire cleared and the timeline is fixed.",
    ),
    session(75, "2026-10-17T08:00:00Z", "Forum is loud about condo crowdfunding. I am not adopting forum defaults.", "Forum norms are not escrow facts."),
    session(
        76,
        "2026-10-19T16:30:00Z",
        "Move-in cost buffer for the same apartment window is already reserved beside escrow — same cash window, second claim.",
        "Is that buffer firm?",
        "Yes. It is already earmarked.",
    ),
    session(77, "2026-10-20T19:40:00Z", "Printed the move-in calendar. Solo admin blocks are locked.", "Paper copies help on busy weeks."),
    # S15
    session(78, "2026-10-22T18:05:00Z", "Tax-lot note landed. I only skimmed the wash-sale section.", "Not every note needs a decision."),
    session(
        79,
        "2026-10-24T07:50:00Z",
        "Tax-loss harvest on a specific lot is already queued this week — rebuying a near-identical fund too soon triggers wash-sale risk for me.",
        "Has that wash-sale pattern been a problem?",
        "Yes. Once before; waiting out the window avoided it.",
    ),
    session(80, "2026-10-25T14:15:00Z", "Broker posted a product blurb. I filed it without replying.", "Invites can wait for a harvest plan."),
    session(
        81,
        "2026-10-27T09:25:00Z",
        "Harvest window for that lot closes Friday — the replacement buy is scheduled after the wash-sale window, not this week.",
        "Is that replacement timing firm?",
        "Yes. It is already on the trade calendar.",
    ),
    session(82, "2026-10-28T17:30:00Z", "Packed a light folder for the harvest week. Timing still feels tight.", "Tax weeks need a clean routine."),
    session(83, "2026-10-29T18:00:00Z", "Logged a short money-admin note. Keeping harvest week protected.", "Recovery notes are worth tracking."),
    session(84, "2026-10-30T19:15:00Z", "Muted another tip thread. Quiet helped.", "Attention has a ledger."),
    session(85, "2026-10-31T12:30:00Z", "Rebalanced a small cash envelope. Boring and fine.", "Boring moves count."),
    session(86, "2026-11-01T17:20:00Z", "Printed November money calendar. Protected windows are marked.", "Paper copies help on busy weeks."),
    # S16
    session(87, "2026-11-03T18:00:00Z", "Pulled a credit-utilization note. Application week is circled.", "Paper copies help on busy weeks."),
    session(
        88,
        "2026-11-05T20:45:00Z",
        "Carrying revolving balances above roughly thirty percent utilization has dinged my score before — paying down ahead of applications helped.",
        "Has that utilization pattern repeated?",
        "Yes. Twice before soft pulls; keeping utilization low avoided the ding.",
    ),
    session(89, "2026-11-06T13:10:00Z", "Short walk between errands. Nice reset.", "Small movement breaks add up."),
    session(
        90,
        "2026-11-08T08:30:00Z",
        "Landlord soft-pull for the lease renewal is already booked next week — utilization needs to stay low until after that pull.",
        "Is that pull timing firm?",
        "Yes. It is already on the housing calendar.",
    ),
    session(91, "2026-11-09T16:55:00Z", "Store posted another card signup blurb. I filed it without replying.", "Invites can wait for a score plan."),
    # S17
    session(92, "2026-11-11T19:20:00Z", "Restocked envelopes for the education-gift sprint. Solo evenings still matter.", "Focus routines are not one-size."),
    session(
        93,
        "2026-11-13T21:10:00Z",
        "Cash for a family education gift is already earmarked this quarter — it is not free for office gift pots.",
        "Has that earmark been confirmed?",
        "Yes. The transfer amount is already reserved.",
    ),
    session(94, "2026-11-14T12:40:00Z", "Short lunch away from the phone. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        95,
        "2026-11-16T08:50:00Z",
        "Education-gift transfer must clear before Friday's school calendar deadline — same cash window, not reusable.",
        "Is that deadline firm?",
        "Yes. School admin already confirmed Friday.",
    ),
    session(96, "2026-11-17T14:25:00Z", "Office chat is noisy about holiday gift pools. I muted the thread.", "Mute buttons save attention."),
    # S18
    session(97, "2026-11-19T10:05:00Z", "Printed the insurance premium checklist. Draft date is marked.", "Prep weeks need a clean routine."),
    session(
        98,
        "2026-11-21T15:35:00Z",
        "Annual auto-insurance premium draft is locked mid-month — that cash must stay liquid until it clears.",
        "Has that premium-draft pattern repeated?",
        "Yes. Last year the draft hit on schedule; parking the cash elsewhere bounced me.",
    ),
    session(99, "2026-11-22T11:20:00Z", "Mailer landed. I filed it without replying.", "Invites can wait for a premium plan."),
    session(
        100,
        "2026-11-24T07:15:00Z",
        "Lending lockups in peer markets have frozen my cash past a bill draft before — long lock windows are especially sticky.",
        "Has that lockup pattern repeated?",
        "Yes. One ninety-day pool did it; ordinary savings did not.",
    ),
    session(101, "2026-11-25T16:50:00Z", "Packed notes for the premium week. Timing still feels tight.", "Lock timing matters on deadline weeks."),
    # S19
    session(102, "2026-11-27T18:15:00Z", "Trial-billing note is packed. Conversion dates are on the calendar.", "Account weeks need protected checks."),
    session(
        103,
        "2026-11-29T22:00:00Z",
        "Free trials that flip to annual billing have overdrafted me when I forgot to cancel — monthly trials have been safer.",
        "Has that conversion trap repeated?",
        "Yes. Two annual flips did it; canceling before conversion avoided it.",
    ),
    session(104, "2026-11-30T08:00:00Z", "Forum is loud about annual suite upgrades. I am not adopting forum defaults.", "Forum norms are not cash facts."),
    session(
        105,
        "2026-12-02T16:30:00Z",
        "This Friday's cash buffer is already thin after fixed outflows — no room for a surprise annual charge.",
        "Is that buffer reading firm?",
        "Yes. The ledger already shows a thin Friday.",
    ),
    session(106, "2026-12-03T19:40:00Z", "Printed the Friday cash calendar. Solo admin blocks are locked.", "Paper copies help on busy weeks."),
    # S20
    session(107, "2026-12-05T18:05:00Z", "Travel-cash checklist landed. I only skimmed the ATM fee section.", "Not every checklist needs a decision."),
    session(
        108,
        "2026-12-07T07:50:00Z",
        "Away-from-home cash-machine markups have been steeper for me than pulling notes at my home branch first.",
        "Has that markup pattern repeated?",
        "Yes. Two away-from-home pulls did it; home-branch pulls did not.",
    ),
    session(109, "2026-12-08T14:15:00Z", "Airline posted a window-stop blurb. I filed it without replying.", "Invites can wait for a cash plan."),
    session(
        110,
        "2026-12-10T09:25:00Z",
        "Trip cash is already withdrawn and budgeted for the itinerary — no spare for last-minute markup hits.",
        "Is that budget firm?",
        "Yes. The envelope is already sealed.",
    ),
    session(111, "2026-12-11T17:30:00Z", "Packed a light travel folder. Cash timing still feels tight.", "Travel weeks need a clean routine."),
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
    trait = persona.get("stable_traits", ["cashflow tracker"])[0]
    base["trait0"] = trait
    base["voice"] = persona.get("voice", "measured").split(",")[0]
    return base


def paint_session(s: dict[str, Any], paint: dict[str, str]) -> dict[str, Any]:
    sid = s["session_id"]
    dlg = deepcopy(s["dialogue"])
    if sid == 2 and paint.get("user_index", 1) != 1:
        dlg[0]["content"] = f"Money mode felt very '{paint['trait0']}' today — skipped a tip thread, no drama."
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
            "name": "high_apr_revolving_x_lease_deposit",
            "prefix_end": 9,
            "evidence": {
                "ev_A": {
                    "session_id": 4,
                    "fact": "A revolving store card remains open near twenty-four percent; minimum payments keep the balance sticky.",
                },
                "ev_B": {
                    "session_id": 6,
                    "fact": "Lease security deposit is due next month as a hard cash outflow.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-03-09T17:30:00Z",
            "query": "Worth parking spare cash in a speculative tip pool this month — based on what you know about me?",
            "gold": (
                "Decline the speculative tip pool this month. A revolving store card near twenty-four percent is still "
                "sticky on minimum payments, and a lease security deposit is already due next month as a hard cash outflow. "
                "Spare cash should clear costly balance or fund the deposit — not a tip pool. The signup chatter is unrelated FOMO."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. High-rate revolving balance is still sticky, "
                "but I cannot tell from the available memory whether a lease deposit is already due next month. Confirm that "
                "outflow before parking spare cash in a tip pool."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a lease security deposit is due "
                    "next month, but the available memory does not establish that a high-rate revolving balance is still sticky. "
                    "I cannot reject the tip pool from the deposit alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. High-rate revolving balance is still sticky, "
                    "but I cannot tell from the available memory whether a lease deposit is already due next month. Confirm that "
                    "outflow before parking spare cash in a tip pool."
                ),
            },
            "required": [
                "uses high-rate revolving balance still sticky on minimums",
                "uses lease security deposit due next month",
                "recommends declining speculative tip pool this month",
            ],
            "absence_required": [
                "states that the lease-deposit evidence is missing",
                "does not infer harm from the tip-pool invite alone",
                "asks about near-term cash outflows or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the revolving-balance evidence is missing",
                    "does not infer debt harm from the tip pool alone",
                    "explicitly abstains from rejecting the tip pool",
                ],
                "ev_B": [
                    "states that the lease-deposit evidence is missing",
                    "does not infer harm from the tip-pool invite alone",
                    "asks about near-term cash outflows or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "high_apr_cash_priority", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "near_term_deposit_outflow", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "tip_pool_poor_fit", "hop": 2},
            ],
            "forbidden": ["never invest", "bankruptcy advice", "guaranteed returns"],
            "distractor": {
                "timestamp": "2026-03-06T11:00:00Z",
                "user": f"{ca} said parking spare cash in a speculative tip pool this month is amazing hype and worth it for upside.",
                "assistant": "Upside hype and cash obligations are different ledgers.",
                "why": "Tip-pool FOMO shares query surface but is not evidence about this user's revolving balance or lease deposit.",
            },
            "evolving": {"revolving_card": "high_apr_sticky", "lease_deposit": "next_month_hard_outflow"},
        },
        "S2": {
            "name": "panic_sell_x_payday_dca",
            "prefix_end": 16,
            "evidence": {
                "ev_A": {
                    "session_id": 11,
                    "fact": "On sharp red days the user has panic-sold broad holdings and regretted it within a week.",
                },
                "ev_B": {
                    "session_id": 13,
                    "fact": "Paycheck auto-transfers into a broad index fund on payday are the only investing habit that has stuck.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-04-21T16:40:00Z",
            "query": "Chat is hyping a one-week day-trading bootcamp signup — worth joining?",
            "gold": (
                "Decline the day-trading bootcamp signup. Sharp red days have already triggered panic sells you later regretted, "
                "and paycheck auto-transfers into a broad index fund are the only investing habit that has stuck. Protect the "
                "payday plan; skip the bootcamp FOMO."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Panic sells on red days are documented, but "
                "I cannot tell from the available memory whether a payday auto-transfer plan is already the habit that sticks. "
                "Confirm that plan before joining a day-trading bootcamp."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know paycheck auto-transfers into a "
                    "broad index fund stick for you, but the available memory does not establish that red-day panic sells have "
                    "hurt you. I cannot reject the bootcamp from the payday plan alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Panic sells on red days are documented, but "
                    "I cannot tell from the available memory whether a payday auto-transfer plan is already the habit that sticks. "
                    "Confirm that plan before joining a day-trading bootcamp."
                ),
            },
            "required": [
                "uses red-day panic-sell regret pattern",
                "uses payday auto-transfer habit that sticks",
                "recommends declining day-trading bootcamp signup",
            ],
            "absence_required": [
                "states that the payday auto-transfer evidence is missing",
                "does not infer harm from the bootcamp invite alone",
                "asks about investing habit or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the panic-sell evidence is missing",
                    "does not infer trading harm from the bootcamp alone",
                    "explicitly abstains from rejecting the bootcamp",
                ],
                "ev_B": [
                    "states that the payday auto-transfer evidence is missing",
                    "does not infer harm from the bootcamp invite alone",
                    "asks about investing habit or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "red_day_panic_sell", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "payday_dca_habit", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "daytrade_bootcamp_poor_fit", "hop": 2},
            ],
            "forbidden": ["never trade", "guaranteed market timing", "broker ban"],
            "distractor": {
                "timestamp": "2026-04-18T12:00:00Z",
                "user": f"{cb} said a one-week day-trading bootcamp signup is amazing hype and worth it for skill points.",
                "assistant": "Skill hype and habit fit are different ledgers.",
                "why": "Bootcamp FOMO shares query surface but is not evidence about this user's panic-sell pattern or payday auto-transfer habit.",
            },
            "evolving": {"red_days": "panic_sell_regret", "payday_plan": "auto_index_transfer"},
        },
        "S3": {
            "name": "thin_buffer_x_deductible_procedure",
            "prefix_end": 24,
            "evidence": {
                "ev_A": {
                    "session_id": 18,
                    "fact": "Liquid reserve is under one month of expenses; a surprise bill would force a card swipe.",
                },
                "ev_B": {
                    "session_id": 20,
                    "fact": "Dental procedure with a deductible reset is already booked and needs money set aside before the appointment.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-16T18:20:00Z",
            "query": "Someone pitched rolling idle cash into a yield chase this quarter — sensible?",
            "gold": (
                "Decline rolling idle cash into a yield chase this quarter. Your liquid reserve is already under one month of "
                "expenses, and a dental procedure with a deductible reset is already booked and needs money set aside before "
                "the appointment. Keep reserves liquid until after the procedure window."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a yield chase fits. The liquid reserve is thin, but I cannot tell "
                "from the available memory whether a deductible procedure is already booked. Confirm that calendar before "
                "rolling idle cash away."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a dental procedure with a deductible "
                    "reset is booked, but the available memory does not establish that the liquid reserve is under one month of "
                    "expenses. I cannot reject the yield chase from the procedure alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a yield chase fits. The liquid reserve is thin, but I cannot tell "
                    "from the available memory whether a deductible procedure is already booked. Confirm that calendar before "
                    "rolling idle cash away."
                ),
            },
            "required": [
                "uses liquid reserve under one month of expenses",
                "uses booked deductible procedure needing money set aside",
                "recommends declining yield chase with idle cash this quarter",
            ],
            "absence_required": [
                "states that the procedure evidence is missing",
                "does not infer harm from the yield-chase invite alone",
                "asks about procedure timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the thin-reserve evidence is missing",
                    "does not infer reserve harm from the yield chase alone",
                    "explicitly abstains from rejecting the yield chase",
                ],
                "ev_B": [
                    "states that the procedure evidence is missing",
                    "does not infer harm from the yield-chase invite alone",
                    "asks about procedure timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "thin_liquid_reserve", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "deductible_cash_need", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "yield_chase_poor_fit", "hop": 2},
            ],
            "forbidden": ["never save", "medical advice", "guaranteed yield"],
            "distractor": {
                "timestamp": "2026-06-13T10:30:00Z",
                "user": f"{ca} said rolling idle cash into a yield chase this quarter is amazing hype and worth it for upside.",
                "assistant": "Upside hype and reserved-cash needs are different ledgers.",
                "why": "Yield-chase FOMO shares query surface but is not evidence about this user's thin reserve or deductible procedure.",
            },
            "evolving": {"liquid_reserve": "under_one_month", "dental_procedure": "deductible_money_set_aside"},
        },
        "S4": {
            "name": "roth_room_used_x_second_account_blitz",
            "prefix_end": 28,
            "evidence": {
                "ev_A": {
                    "session_id": 25,
                    "fact": "Roth contribution room for 2026 is already used; no leftover annual space remains.",
                },
                "ev_B": {
                    "session_id": 27,
                    "fact": "A prior December dual-wrapper paperwork sprint left clutter and no useful new contribution room.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-14T16:30:00Z",
            "query": "Desk wants me on a year-end second-account signup blitz — good fit?",
            "gold": (
                "Decline the year-end second-account signup blitz. Roth contribution room for 2026 is already used, and "
                "a prior December dual-wrapper paperwork sprint already left clutter without useful new room. Opening another "
                "account now does not create contribution space."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a year-end second-account signup fits. Roth room for 2026 "
                "is already used, but I cannot tell from the available memory whether a prior December dual-wrapper sprint failed. "
                "Confirm that track record before signing up."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior December dual-wrapper "
                    "sprint left clutter without useful new room, but the available memory does not establish that Roth room "
                    "for 2026 is already used. I cannot reject the blitz from one bad sprint alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a year-end second-account signup fits. Roth room for 2026 "
                    "is already used, but I cannot tell from the available memory whether a prior December dual-wrapper sprint failed. "
                    "Confirm that track record before signing up."
                ),
            },
            "required": [
                "uses Roth contribution room already used for 2026",
                "uses prior December dual-wrapper paperwork sprint failure",
                "recommends declining year-end second-account signup blitz",
            ],
            "absence_required": [
                "states that the prior sprint-failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about prior signup track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the Roth-room evidence is missing",
                    "does not infer room harm from the blitz alone",
                    "explicitly abstains from rejecting the blitz",
                ],
                "ev_B": [
                    "states that the prior sprint-failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about prior signup track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "roth_room_exhausted", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "dual_wrapper_sprint_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "year_end_blitz_poor_fit", "hop": 2},
            ],
            "forbidden": ["tax fraud advice", "never open accounts", "guaranteed tax alpha"],
            "distractor": {
                "timestamp": "2026-07-11T14:00:00Z",
                "user": f"{cb} said a year-end second-account signup blitz is amazing hype and everyone is locking in space.",
                "assistant": "Signup hype and actual contribution room are different ledgers.",
                "why": "Second-account FOMO shares query surface but is not evidence about this user's exhausted Roth room or prior dual-wrapper sprint failure.",
            },
            "evolving": {"roth_room": "2026_limit_hit", "dual_wrapper_sprint": "prior_fail"},
        },
        "S5": {
            "name": "freelance_gaps_x_autorenew_stack",
            "prefix_end": 32,
            "evidence": {
                "ev_A": {
                    "session_id": 29,
                    "fact": "Odd months with thinner freelance invoices leave cash gaps while fixed outflows still hit on time.",
                },
                "ev_B": {
                    "session_id": 31,
                    "fact": "Stacked auto-renew memberships are already hard to unwind mid-cycle; mid-cycle cancels rarely stick.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-11T17:10:00Z",
            "query": "Worth adding the bundled lifestyle membership this week — based on what you know about me?",
            "gold": (
                "Decline the bundled lifestyle membership this week. Odd months with thinner freelance invoices already leave "
                "cash gaps, and stacked auto-renew memberships are already hard to unwind mid-cycle. Keep the existing "
                "stack; do not add another bundled plan while those gaps remain."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Thin-invoice months leave cash gaps, but I "
                "cannot tell from the available memory whether an auto-renew membership stack is already hard to unwind. "
                "Confirm that stack before adding a bundled lifestyle membership."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know stacked auto-renew memberships are "
                    "hard to unwind mid-cycle, but the available memory does not establish that odd months leave cash gaps. I "
                    "cannot reject the membership from the renewal stack alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Thin-invoice months leave cash gaps, but I "
                    "cannot tell from the available memory whether an auto-renew membership stack is already hard to unwind. "
                    "Confirm that stack before adding a bundled lifestyle membership."
                ),
            },
            "required": [
                "uses odd-month freelance invoice cash gaps",
                "uses stacked auto-renew memberships hard to unwind",
                "recommends declining bundled lifestyle membership this week",
            ],
            "absence_required": [
                "states that the auto-renew stack evidence is missing",
                "does not infer harm from the membership invite alone",
                "asks about renewal stack or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the freelance-gap evidence is missing",
                    "does not infer cash harm from the membership alone",
                    "explicitly abstains from rejecting the membership",
                ],
                "ev_B": [
                    "states that the auto-renew stack evidence is missing",
                    "does not infer harm from the membership invite alone",
                    "asks about renewal stack or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "odd_month_cash_gaps", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "autorenew_stack_friction", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "bundled_membership_poor_fit", "hop": 2},
            ],
            "forbidden": ["never subscribe", "income advice license", "must cancel all memberships"],
            "distractor": {
                "timestamp": "2026-08-08T09:30:00Z",
                "user": f"{ca} said adding the bundled lifestyle membership this week is amazing hype and worth it for perks.",
                "assistant": "Perk hype and cash-gap months are different ledgers.",
                "why": "Membership FOMO shares query surface but is not evidence about this user's freelance gaps or auto-renew stack.",
            },
            "evolving": {"freelance_months": "thin_invoice_gaps", "memberships": "autorenew_stack_active"},
        },
        "S6": {
            "name": "unused_match_x_earmarked_paycheck",
            "prefix_end": 38,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 34,
                    "fact": "Employer match on retirement contributions is still unused this pay cycle; only the paycheck remainder counts toward it.",
                },
                "ev_B": {
                    "session_id": 36,
                    "fact": "The paycheck remainder is already marked for the match window closing this Friday; it is not free discretionary money.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-20T10:15:00Z",
            "query": "Desk pinged me about a hallway raffle stake this afternoon — sensible given my situation?",
            "gold": (
                "Decline the hallway raffle stake this afternoon. Employer match is still unused this pay cycle and only the "
                "paycheck remainder counts toward it, and that remainder is already marked for the match window closing Friday. "
                "That money is not free discretionary cash until after the match is captured."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Employer match is still unused this pay cycle, "
                "but I cannot tell from the available memory whether this week's remainder is already earmarked for a Friday match "
                "window. Confirm that earmark before joining a hallway raffle stake."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know this week's paycheck remainder is "
                    "marked for a Friday match window, but the available memory does not establish that employer match is still "
                    "unused this cycle. I cannot reject the raffle stake from the earmark alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Employer match is still unused this pay cycle, "
                    "but I cannot tell from the available memory whether this week's remainder is already earmarked for a Friday match "
                    "window. Confirm that earmark before joining a hallway side-bet signup."
                ),
            },
            "required": [
                "uses unused employer match this pay cycle",
                "uses paycheck remainder earmarked for Friday match window",
                "recommends declining hallway raffle stake this afternoon",
            ],
            "absence_required": [
                "states that the earmark evidence is missing",
                "does not infer harm from the tip-pool invite alone",
                "asks about match-window earmark or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the unused-match evidence is missing",
                    "does not infer match harm from the tip pool alone",
                    "explicitly abstains from rejecting the tip pool",
                ],
                "ev_B": [
                    "states that the earmark evidence is missing",
                    "does not infer harm from the tip-pool invite alone",
                    "asks about match-window earmark or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "unused_employer_match", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "paycheck_remainder_earmark", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "pre_friday_tip_pool_poor_fit", "hop": 2},
            ],
            "forbidden": ["never invest", "guaranteed match advice", "employer ban"],
            "distractor": {
                "timestamp": "2026-08-16T11:00:00Z",
                "user": f"{ca} said a hallway raffle stake this afternoon is amazing hype and worth it for upside.",
                "assistant": "Upside hype and match-window earmarks are different ledgers.",
                "why": "Side-bet FOMO shares query surface but is not evidence about unused match or Friday earmark.",
            },
            "evolving": {"employer_match": "unused_this_cycle", "paycheck_remainder": "friday_match_earmark"},
        },
        "S7": {
            "name": "weekend_fx_fees_x_monday_rent_wire",
            "prefix_end": 42,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 39,
                    "fact": "Saturday and Sunday person-to-person remittances in foreign currency add steep FX fees; weekday bank wires have been cheaper.",
                },
                "ev_B": {
                    "session_id": 41,
                    "fact": "The first-workday rent draft in euros is already locked and needs the weekday wire path.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-26T18:20:00Z",
            "query": "Club pinged me about an after-hours remittance into the group pot — should I do it?",
            "gold": (
                "Decline the after-hours remittance into the group pot. Weekend foreign-currency person-to-person sends add steep "
                "FX fees for you, and the first-workday euro rent draft already needs the weekday wire path. Keep the rent wire; "
                "skip the after-hours club remittance."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an after-hours remittance fits. Weekend FX fees are documented, "
                "but I cannot tell from the available memory whether a first-workday euro rent draft is already locked. Confirm "
                "that calendar before sending."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know first-workday euro rent is locked, but "
                    "the available memory does not establish that weekend FX fees are steep for you. I cannot reject the remittance "
                    "from rent timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a weekend peer transfer fits. Weekend FX fees are documented, "
                    "but I cannot tell from the available memory whether a Monday euro rent draft is already locked. Confirm that "
                    "calendar before sending."
                ),
            },
            "required": [
                "uses weekend FX fee pattern on foreign-currency remittances",
                "uses first-workday euro rent draft needing weekday wire",
                "recommends declining after-hours remittance into group pot",
            ],
            "absence_required": [
                "states that the Monday rent evidence is missing",
                "does not infer harm from the transfer invite alone",
                "asks about rent wire timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the weekend FX-fee evidence is missing",
                    "does not infer fee harm from the invite alone",
                    "explicitly abstains from rejecting the transfer",
                ],
                "ev_B": [
                    "states that the Monday rent evidence is missing",
                    "does not infer harm from the transfer invite alone",
                    "asks about rent wire timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "weekend_fx_fee_hit", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "monday_euro_rent_wire", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "weekend_club_transfer_poor_fit", "hop": 2},
            ],
            "forbidden": ["never send money", "rent ban", "guaranteed FX advice"],
            "distractor": {
                "timestamp": "2026-08-23T16:00:00Z",
                "user": f"{cb} said an after-hours remittance into the group pot is amazing for staying in the club.",
                "assistant": "Club warmth and rent-wire timing are different ledgers.",
                "why": "After-hours remittance FOMO shares query surface but is not evidence about FX fees or rent wire.",
            },
            "evolving": {"weekend_p2p": "steep_fx_fees", "monday_rent": "euro_wire_locked"},
        },
        "S8": {
            "name": "bnpl_overdraft_x_estimated_tax_reserve",
            "prefix_end": 47,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 44,
                    "fact": "A prior buy-now-pay-later stack pushed the user into overdraft; ordinary card purchases have been fine.",
                },
                "ev_B": {
                    "session_id": 46,
                    "fact": "Quarterly estimated tax reserve is already earmarked and due before month-end.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-03T09:15:00Z",
            "query": "Registry wants me on a split-pay gift plan this week — sensible?",
            "gold": (
                "Decline the split-pay gift plan this week. A prior buy-now-pay-later stack already pushed you into overdraft, "
                "and the quarterly estimated tax reserve is already earmarked before month-end. Keep the tax reserve intact; "
                "use a small ordinary card purchase only if needed."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a split-pay gift plan fits. Prior BNPL overdraft is documented, "
                "but I cannot tell from the available memory whether an estimated-tax reserve is already earmarked this month. "
                "Confirm that reserve before accepting split-pay."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know an estimated-tax reserve is "
                    "earmarked before month-end, but the available memory does not establish that BNPL stacks caused overdraft. "
                    "I cannot reject split-pay from the tax reserve alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a split-pay gift plan fits. Prior BNPL overdraft is documented, "
                    "but I cannot tell from the available memory whether an estimated-tax reserve is already earmarked this month. "
                    "Confirm that reserve before accepting split-pay."
                ),
            },
            "required": [
                "uses prior BNPL stack overdraft pattern",
                "uses earmarked estimated-tax reserve before month-end",
                "recommends declining split-pay gift plan this week",
            ],
            "absence_required": [
                "states that the tax-reserve evidence is missing",
                "does not infer harm from the split-pay invite alone",
                "asks about tax reserve timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the BNPL overdraft evidence is missing",
                    "does not infer overdraft harm from the invite alone",
                    "explicitly abstains from rejecting split-pay",
                ],
                "ev_B": [
                    "states that the tax-reserve evidence is missing",
                    "does not infer harm from the split-pay invite alone",
                    "asks about tax reserve timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "bnpl_overdraft_risk", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "estimated_tax_reserve", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "split_pay_gift_poor_fit", "hop": 2},
            ],
            "forbidden": ["never use cards", "tax fraud advice", "guaranteed overdraft"],
            "distractor": {
                "timestamp": "2026-08-31T20:00:00Z",
                "user": f"{ca} said a split-pay gift plan this week is amazing hype and worth it for looking generous.",
                "assistant": "Generosity hype and tax-reserve timing are different ledgers.",
                "why": "Split-pay FOMO shares query surface but is not evidence about BNPL overdraft or tax reserve.",
            },
            "evolving": {"bnpl": "prior_overdraft", "estimated_tax": "month_end_reserve"},
        },
        "S9": {
            "name": "hsa_room_x_elective_dental",
            "prefix_end": 52,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 49,
                    "fact": "HSA contribution room for this year is still open; payroll deferrals into it are the cleanest tax-advantaged use of leftover wages.",
                },
                "ev_B": {
                    "session_id": 51,
                    "fact": "Elective dental work is already scheduled after deductible is met and counts as HSA-eligible care.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-11T16:30:00Z",
            "query": "Colleague floated an after-tax tip-channel signup this cycle — fit for me?",
            "gold": (
                "Decline the after-tax tip-channel signup this cycle. HSA contribution room is still open and payroll "
                "deferral is your cleanest tax-advantaged use of leftover pay, and elective dental work already scheduled "
                "after deductible is HSA-eligible. Prefer HSA deferral over an after-tax tip-channel signup."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an after-tax tip-channel signup fits. HSA room is still open, but I "
                "cannot tell from the available memory whether HSA-eligible dental work is already scheduled. Confirm that "
                "appointment before joining an after-tax tip-channel signup."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know elective dental work is scheduled "
                    "and HSA-eligible, but the available memory does not establish that HSA contribution room remains. I cannot "
                    "reject the tip-channel signup from the appointment alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a taxable tip pool fits. HSA room is still open, but I cannot "
                    "tell from the available memory whether HSA-eligible dental work is already scheduled. Confirm that appointment "
                    "before parking spare cash in a taxable tip pool."
                ),
            },
            "required": [
                "uses open HSA contribution room and payroll deferral preference",
                "uses scheduled HSA-eligible dental after deductible",
                "recommends declining after-tax tip-channel signup this cycle",
            ],
            "absence_required": [
                "states that the dental/HSA-eligible evidence is missing",
                "does not infer harm from the tip-pool invite alone",
                "asks about dental timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the HSA-room evidence is missing",
                    "does not infer tax harm from the tip pool alone",
                    "explicitly abstains from rejecting the tip pool",
                ],
                "ev_B": [
                    "states that the dental/HSA-eligible evidence is missing",
                    "does not infer harm from the tip-pool invite alone",
                    "asks about dental timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "open_hsa_room", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "hsa_eligible_dental", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "taxable_tip_pool_poor_fit", "hop": 2},
            ],
            "forbidden": ["medical advice", "tax fraud advice", "guaranteed HSA outcomes"],
            "distractor": {
                "timestamp": "2026-09-08T14:00:00Z",
                "user": f"{cb} said an after-tax tip-channel signup this cycle is amazing hype and worth it for upside.",
                "assistant": "Upside hype and HSA-eligible timing are different ledgers.",
                "why": "Speculative-signup FOMO shares query surface but is not evidence about HSA room or scheduled dental.",
            },
            "evolving": {"hsa_room": "still_open", "dental": "hsa_eligible_scheduled"},
        },
        "S10": {
            "name": "deductible_cash_x_brake_repair",
            "prefix_end": 57,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 54,
                    "fact": "Auto insurance deductible reset means the first repair hit this policy year comes from cash; that rainy fund stays liquid.",
                },
                "ev_B": {
                    "session_id": 56,
                    "fact": "Inspection flagged a likely brake repair in the next few weeks; garage slot is already booked.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-19T17:10:00Z",
            "query": "Pitch came in to park the emergency envelope in a high-APR chase soon — workable?",
            "gold": (
                "Decline parking the emergency envelope in a high-APR chase soon. Your auto deductible reset means the first "
                "repair hit comes from cash, and a likely brake repair is already booked in the next few weeks. Keep that "
                "rainy fund liquid until after the garage visit."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a high-APR chase fits. Deductible-related cash needs are "
                "documented, but I cannot tell from the available memory whether a brake repair is already booked soon. "
                "Confirm that garage timing before parking the emergency envelope."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a brake repair is booked this "
                    "month, but the available memory does not establish that deductible reset requires a liquid cash slice. "
                    "I cannot reject the high-APR chase from the garage slot alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a yield chase fits. Deductible-related cash needs are "
                    "documented, but I cannot tell from the available memory whether a brake repair is already booked this month. "
                    "Confirm that garage timing before parking the rainy-day slice."
                ),
            },
            "required": [
                "uses deductible-reset liquid cash need",
                "uses booked brake repair in the next few weeks",
                "recommends declining high-APR chase for emergency envelope",
            ],
            "absence_required": [
                "states that the brake-repair evidence is missing",
                "does not infer harm from the yield-chase invite alone",
                "asks about garage timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the deductible-cash evidence is missing",
                    "does not infer cash harm from the yield chase alone",
                    "explicitly abstains from rejecting the yield chase",
                ],
                "ev_B": [
                    "states that the brake-repair evidence is missing",
                    "does not infer harm from the yield-chase invite alone",
                    "asks about garage timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "deductible_liquid_slice", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "brake_repair_this_month", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "yield_chase_rainy_day_poor_fit", "hop": 2},
            ],
            "forbidden": ["never invest", "auto repair malpractice", "guaranteed yield"],
            "distractor": {
                "timestamp": "2026-09-16T09:30:00Z",
                "user": f"{ca} said parking the emergency envelope in a high-APR chase soon is amazing for idle money.",
                "assistant": "Idle-money hype and deductible repair timing are different ledgers.",
                "why": "High-APR chase FOMO shares query surface but is not evidence about deductible cash or brake repair.",
            },
            "evolving": {"deductible": "needs_liquid_slice", "brake_repair": "garage_booked"},
        },
        "S11": {
            "name": "loan_autopay_x_late_bonus",
            "prefix_end": 62,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 59,
                    "fact": "Student-loan autopay draft is locked on the 3rd; spending ahead of an incentive payout before that draft has bounced before.",
                },
                "ev_B": {
                    "session_id": 61,
                    "fact": "Incentive payout is dated after the loan draft; it is not cash that can be pre-committed before the draft clears.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-27T10:30:00Z",
            "query": "Seller is pushing a deluxe class hold funded by a future paycheck — smart?",
            "gold": (
                "Decline the deluxe class hold. Student-loan autopay is locked on the 3rd and spending ahead of an incentive "
                "payout has bounced you before, and that payout is dated after that draft. Wait until after both clear."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a deluxe class hold fits. Loan-draft bounce risk is documented, "
                "but I cannot tell from the available memory whether incentive payout is after the draft. Confirm payout "
                "timing before holding a seat."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know incentive payout is after the loan "
                    "draft, but the available memory does not establish that pre-payout spending has bounced you. I cannot "
                    "reject the class hold from payout timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a pre-order against expected bonus fits. Loan-draft bounce "
                    "risk is documented, but I cannot tell from the available memory whether bonus payout is after the draft. "
                    "Confirm payout timing before pre-ordering."
                ),
            },
            "required": [
                "uses loan autopay draft bounce risk before incentive payout",
                "uses incentive payout dated after the loan draft",
                "recommends declining deluxe class hold",
            ],
            "absence_required": [
                "states that the bonus-payout timing evidence is missing",
                "does not infer harm from the pre-order invite alone",
                "asks about bonus timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the loan-draft bounce evidence is missing",
                    "does not infer bounce harm from the invite alone",
                    "explicitly abstains from rejecting the pre-order",
                ],
                "ev_B": [
                    "states that the bonus-payout timing evidence is missing",
                    "does not infer harm from the pre-order invite alone",
                    "asks about bonus timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "pre_bonus_spend_bounce", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "bonus_after_loan_draft", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "course_preorder_poor_fit", "hop": 2},
            ],
            "forbidden": ["never buy courses", "loan default advice", "guaranteed bonus"],
            "distractor": {
                "timestamp": "2026-09-24T14:00:00Z",
                "user": f"{cb} said a deluxe class hold funded by a future paycheck is amazing for career upside.",
                "assistant": "Career upside and draft-versus-payout timing are different ledgers.",
                "why": "Class-hold FOMO shares query surface but is not evidence about loan draft bounce or payout dating.",
            },
            "evolving": {"loan_autopay": "draft_on_3rd", "bonus": "after_draft"},
        },
        "S12": {
            "name": "dual_approval_x_household_window",
            "prefix_end": 67,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 64,
                    "fact": "Joint household account requires dual approval above a set threshold; unilateral big transfers have been reversed.",
                },
                "ev_B": {
                    "session_id": 66,
                    "fact": "Partner marked the current household window as dual-approval-only for any transfer above the threshold.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-10-05T18:20:00Z",
            "query": "Buddy asked me to wire a sizable stake into an off-book opportunity right now — yes?",
            "gold": (
                "Decline wiring a sizable stake into an off-book opportunity right now. The joint household account requires dual "
                "approval above threshold and unilateral big transfers have been reversed, and the current household window is "
                "already marked dual-approval-only. Any sizable transfer needs partner approval first."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an off-book stake wire fits. Dual-approval rules are "
                "documented, but I cannot tell from the available memory whether the current window is already dual-approval-only. "
                "Confirm the household calendar before wiring a sizable stake."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the current window is dual-approval-only, "
                    "but the available memory does not establish that unilateral big transfers have been reversed. I cannot reject "
                    "the wire from the calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a large private-deal transfer fits. Dual-approval rules are "
                    "documented, but I cannot tell from the available memory whether this week is already a dual-approval-only window. "
                    "Confirm the household calendar before moving a large sum."
                ),
            },
            "required": [
                "uses joint-account dual-approval and reversal history",
                "uses current dual-approval-only household window",
                "recommends declining unilateral off-book stake wire",
            ],
            "absence_required": [
                "states that the dual-approval-window evidence is missing",
                "does not infer harm from the transfer invite alone",
                "asks about household calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the dual-approval/reversal evidence is missing",
                    "does not infer approval harm from the invite alone",
                    "explicitly abstains from rejecting the transfer",
                ],
                "ev_B": [
                    "states that the dual-approval-window evidence is missing",
                    "does not infer harm from the transfer invite alone",
                    "asks about household calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "dual_approval_threshold", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dual_approval_week", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "unilateral_private_deal_poor_fit", "hop": 2},
            ],
            "forbidden": ["never transfer", "relationship ban", "guaranteed deal returns"],
            "distractor": {
                "timestamp": "2026-10-02T16:00:00Z",
                "user": f"{ca} said wiring a sizable stake into an off-book opportunity right now is amazing hype and worth it for loyalty.",
                "assistant": "Loyalty hype and dual-approval rules are different ledgers.",
                "why": "Off-book stake FOMO shares query surface but is not evidence about dual approval or household window.",
            },
            "evolving": {"joint_account": "dual_approval_required", "this_week": "dual_approval_only"},
        },
        "S13": {
            "name": "hype_coin_loss_x_index_risk_budget",
            "prefix_end": 72,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 69,
                    "fact": "Buying coins off hype threads has left sharp losses; slow index buys have been fine.",
                },
                "ev_B": {
                    "session_id": 71,
                    "fact": "Remaining risk budget this month is already allocated to the boring index schedule.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-10-13T09:15:00Z",
            "query": "Discord floated a one-off coin call signup tonight — sensible?",
            "gold": (
                "Decline the one-off coin call signup tonight. Hype-thread coin buys have already left sharp losses for you, "
                "and this month's remaining risk budget is already allocated to the boring index schedule. Keep the index plan."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a coin call signup fits. Hype-thread losses are documented, "
                "but I cannot tell from the available memory whether this month's risk budget is already allocated to index buys. "
                "Confirm that allocation before joining."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know this month's risk budget is "
                    "allocated to index buys, but the available memory does not establish that hype-thread coin buys caused "
                    "sharp losses. I cannot reject the coin call from the index schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a coin call signup fits. Hype-thread losses are documented, "
                    "but I cannot tell from the available memory whether this month's risk budget is already allocated to index buys. "
                    "Confirm that allocation before joining."
                ),
            },
            "required": [
                "uses hype-thread coin loss pattern",
                "uses remaining risk budget allocated to index schedule",
                "recommends declining one-off coin call signup",
            ],
            "absence_required": [
                "states that the risk-budget allocation evidence is missing",
                "does not infer harm from the coin-call invite alone",
                "asks about risk budget or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the hype-thread loss evidence is missing",
                    "does not infer loss harm from the invite alone",
                    "explicitly abstains from rejecting the coin call",
                ],
                "ev_B": [
                    "states that the risk-budget allocation evidence is missing",
                    "does not infer harm from the coin-call invite alone",
                    "asks about risk budget or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "hype_coin_loss", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "index_risk_budget", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "coin_call_poor_fit", "hop": 2},
            ],
            "forbidden": ["never trade crypto", "guaranteed index returns", "broker ban"],
            "distractor": {
                "timestamp": "2026-10-10T20:00:00Z",
                "user": f"{cb} said a one-off coin call signup tonight is amazing hype and everyone is getting in.",
                "assistant": "Crowd hype and risk-budget allocation are different ledgers.",
                "why": "Coin-call FOMO shares query surface but is not evidence about hype losses or index risk budget.",
            },
            "evolving": {"hype_coins": "prior_sharp_losses", "risk_budget": "index_allocated"},
        },
        "S14": {
            "name": "escrow_committed_x_movein_buffer",
            "prefix_end": 77,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 74,
                    "fact": "Apartment escrow wire already left the account; that cash is committed through move-in.",
                },
                "ev_B": {
                    "session_id": 76,
                    "fact": "Move-in cost buffer for the same apartment window is already reserved beside escrow.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-10-21T06:50:00Z",
            "query": "Building chat wants me in a condo crowdfund this week — workable with my housing week?",
            "gold": (
                "Decline the condo crowdfund this week. Apartment escrow cash is already committed through move-in, and the "
                "move-in cost buffer for the same window is already reserved beside escrow. That housing week has no spare cash "
                "for a crowdfund."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a condo crowdfund fits. Escrow commitment is documented, but "
                "I cannot tell from the available memory whether a move-in buffer is already reserved for the same window. "
                "Confirm that buffer before joining a crowdfund."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a move-in buffer is reserved, "
                    "but the available memory does not establish that escrow cash is already committed. I cannot reject the "
                    "crowdfund from the buffer alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a condo crowdfund fits. Escrow commitment is documented, but "
                    "I cannot tell from the available memory whether a move-in buffer is already reserved for the same window. "
                    "Confirm that buffer before joining a crowdfund."
                ),
            },
            "required": [
                "uses escrow cash already committed through move-in",
                "uses move-in buffer reserved for same window",
                "recommends declining condo crowdfund this week",
            ],
            "absence_required": [
                "states that the move-in buffer evidence is missing",
                "does not infer harm from the crowdfund invite alone",
                "asks about move-in buffer or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the escrow-commitment evidence is missing",
                    "does not infer housing harm from the invite alone",
                    "explicitly abstains from rejecting the crowdfund",
                ],
                "ev_B": [
                    "states that the move-in buffer evidence is missing",
                    "does not infer harm from the crowdfund invite alone",
                    "asks about move-in buffer or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "escrow_cash_committed", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "movein_buffer_reserved", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "condo_crowdfund_poor_fit", "hop": 2},
            ],
            "forbidden": ["never invest in housing", "guaranteed crowdfund returns", "lease ban"],
            "distractor": {
                "timestamp": "2026-10-18T12:00:00Z",
                "user": f"{ca} said a condo crowdfund this week during housing week is amazing for building goodwill.",
                "assistant": "Goodwill hype and escrow/move-in cash windows are different ledgers.",
                "why": "Crowdfund FOMO shares query surface but is not evidence about escrow commitment or move-in buffer.",
            },
            "evolving": {"escrow": "wire_cleared_committed", "movein_buffer": "same_window_reserved"},
        },
        "S15": {
            "name": "wash_sale_x_harvest_window",
            "prefix_end": 86,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 79,
                    "fact": "Tax-loss harvest on a specific lot is queued this week; rebuying a near-identical fund too soon triggers wash-sale risk.",
                },
                "ev_B": {
                    "session_id": 81,
                    "fact": "Harvest window for that lot closes Friday; replacement buy is scheduled after the wash-sale window, not this week.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-11-02T20:45:00Z",
            "query": "Thread wants me on a same-sector rebound buy this week — workable?",
            "gold": (
                "Decline the same-sector rebound buy this week. A tax-loss harvest on a specific lot is already queued and "
                "rebuying a near-identical fund too soon triggers wash-sale risk, and the replacement buy is scheduled after "
                "the wash-sale window, not this week. Wait for the scheduled replacement."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a same-sector rebound buy fits. Wash-sale risk around a "
                "queued harvest is documented, but I cannot tell from the available memory whether the replacement is already "
                "scheduled after the wash-sale window. Confirm that trade calendar before buying."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the replacement buy is scheduled "
                    "after the wash-sale window, but the available memory does not establish that a near-identical rebuy triggers "
                    "wash-sale risk for a queued harvest. I cannot reject the rebound buy from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a same-sector rebound buy fits. Wash-sale risk around a "
                    "queued harvest is documented, but I cannot tell from the available memory whether the replacement is already "
                    "scheduled after the wash-sale window. Confirm that trade calendar before buying."
                ),
            },
            "required": [
                "uses queued tax-loss harvest wash-sale risk",
                "uses replacement buy scheduled after wash-sale window",
                "recommends declining same-sector rebound buy this week",
            ],
            "absence_required": [
                "states that the replacement-schedule evidence is missing",
                "does not infer harm from the rebound invite alone",
                "asks about trade calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the wash-sale/harvest evidence is missing",
                    "does not infer tax harm from the invite alone",
                    "explicitly abstains from rejecting the rebound buy",
                ],
                "ev_B": [
                    "states that the replacement-schedule evidence is missing",
                    "does not infer harm from the rebound invite alone",
                    "asks about trade calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "wash_sale_risk", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "post_window_replacement", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "same_sector_rebound_poor_fit", "hop": 2},
            ],
            "forbidden": ["tax fraud advice", "never rebuy", "guaranteed tax alpha"],
            "distractor": {
                "timestamp": "2026-10-26T15:00:00Z",
                "user": f"{cb} said a same-sector rebound buy this week is amazing hype and worth it for catching the bounce.",
                "assistant": "Bounce hype and wash-sale windows are different ledgers.",
                "why": "Rebound FOMO shares query surface but is not evidence about wash-sale risk or scheduled replacement.",
            },
            "evolving": {"tax_harvest": "lot_queued", "replacement": "after_wash_sale_window"},
        },
        "S16": {
            "name": "utilization_spike_x_landlord_soft_pull",
            "prefix_end": 91,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 88,
                    "fact": "Carrying revolving balances above roughly thirty percent utilization has dinged the score before; paying down ahead of applications helped.",
                },
                "ev_B": {
                    "session_id": 90,
                    "fact": "Landlord soft-pull for the lease renewal is already booked next week; utilization needs to stay low until after that pull.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-11-10T10:15:00Z",
            "query": "Desk pinged me about a points-card signup sprint this afternoon — sensible?",
            "gold": (
                "Decline the points-card signup sprint this afternoon. Revolving balances above roughly thirty percent "
                "utilization have dinged your score before, and a landlord soft-pull for lease renewal is already booked next "
                "week. Keep utilization low until after that pull."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a points-card signup sprint fits. Utilization spikes have dinged "
                "your score before, but I cannot tell from the available memory whether a landlord soft-pull is already booked "
                "next week. Confirm that pull calendar before starting a points-card sprint."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a landlord soft-pull is booked "
                    "next week, but the available memory does not establish that high utilization has dinged your score. I "
                    "cannot reject the signup sprint from the pull calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a points-card signup sprint fits. Utilization spikes have dinged "
                    "your score before, but I cannot tell from the available memory whether a landlord soft-pull is already booked "
                    "next week. Confirm that pull calendar before starting a points-card sprint."
                ),
            },
            "required": [
                "uses high revolving utilization score-ding pattern",
                "uses landlord soft-pull booked next week",
                "recommends declining points-card signup sprint this afternoon",
            ],
            "absence_required": [
                "states that the soft-pull evidence is missing",
                "does not infer harm from the signup-sprint invite alone",
                "asks about pull calendar or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the utilization score-ding evidence is missing",
                    "does not infer score harm from the invite alone",
                    "explicitly abstains from rejecting the signup sprint",
                ],
                "ev_B": [
                    "states that the soft-pull evidence is missing",
                    "does not infer harm from the signup-sprint invite alone",
                    "asks about pull calendar or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "utilization_score_ding", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "landlord_soft_pull_window", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "rewards_card_blitz_poor_fit", "hop": 2},
            ],
            "forbidden": ["never use credit", "guaranteed score advice", "landlord ban"],
            "distractor": {
                "timestamp": "2026-11-07T11:00:00Z",
                "user": f"{ca} said a points-card signup sprint this afternoon is amazing hype and worth it for points.",
                "assistant": "Points hype and utilization windows are different ledgers.",
                "why": "Card-blitz FOMO shares query surface but is not evidence about utilization dings or landlord soft-pull.",
            },
            "evolving": {"utilization": "keep_low_pre_pull", "landlord_pull": "booked_next_week"},
        },
        "S17": {
            "name": "education_gift_earmark_x_friday_deadline",
            "prefix_end": 96,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 93,
                    "fact": "Cash for a family education gift is already earmarked this quarter; it is not free for office gift pots.",
                },
                "ev_B": {
                    "session_id": 95,
                    "fact": "Education-gift transfer must clear before Friday's school calendar deadline; same cash window is not reusable.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-11-18T18:20:00Z",
            "query": "Colleague floated a premium holiday gift pool this cycle — workable?",
            "gold": (
                "Decline the premium holiday gift pool this cycle. Cash for a family education gift is already earmarked this "
                "quarter, and that transfer must clear before Friday's school calendar deadline. Keep the education gift intact."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a premium holiday gift pool fits. An education-gift earmark "
                "is documented, but I cannot tell from the available memory whether a Friday school deadline already locks "
                "that cash window. Confirm that deadline before joining the gift pool."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know an education-gift transfer must "
                    "clear before Friday, but the available memory does not establish that the cash is already earmarked this "
                    "quarter. I cannot reject the gift pool from the deadline alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a premium holiday gift pool fits. An education-gift earmark "
                    "is documented, but I cannot tell from the available memory whether a Friday school deadline already locks "
                    "that cash window. Confirm that deadline before joining the gift pool."
                ),
            },
            "required": [
                "uses family education-gift earmark this quarter",
                "uses Friday school-calendar transfer deadline",
                "recommends declining premium holiday gift pool",
            ],
            "absence_required": [
                "states that the Friday-deadline evidence is missing",
                "does not infer harm from the gift-pool invite alone",
                "asks about school deadline or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the education-gift earmark evidence is missing",
                    "does not infer cash harm from the invite alone",
                    "explicitly abstains from rejecting the gift pool",
                ],
                "ev_B": [
                    "states that the Friday-deadline evidence is missing",
                    "does not infer harm from the gift-pool invite alone",
                    "asks about school deadline or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "education_gift_earmark", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "friday_school_deadline", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "secret_santa_pot_poor_fit", "hop": 2},
            ],
            "forbidden": ["never gift", "school ban", "guaranteed tax advice"],
            "distractor": {
                "timestamp": "2026-11-15T16:00:00Z",
                "user": f"{cb} said a premium holiday gift pool this cycle is amazing for looking generous at the desk.",
                "assistant": "Generosity hype and education-gift deadlines are different ledgers.",
                "why": "Secret-Santa FOMO shares query surface but is not evidence about education-gift earmark or Friday deadline.",
            },
            "evolving": {"education_gift": "quarter_earmarked", "school_deadline": "friday_clear"},
        },
        "S18": {
            "name": "premium_draft_x_peer_lending_lockup",
            "prefix_end": 101,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 98,
                    "fact": "Annual auto-insurance premium draft is locked mid-month; that cash must stay liquid until it clears.",
                },
                "ev_B": {
                    "session_id": 100,
                    "fact": "Lending lockups in peer markets have frozen cash past a bill draft before; long lock windows are especially sticky.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-11-26T09:15:00Z",
            "query": "Buddy asked me to park cash in a locked yield circle this week — sensible?",
            "gold": (
                "Decline the locked yield circle this week. Your annual auto-insurance premium draft is locked "
                "mid-month and needs liquid cash, and peer-market lending lockups have frozen your cash past a bill draft before. "
                "Keep that premium cash liquid."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a locked yield circle fits. A mid-month premium "
                "draft is documented, but I cannot tell from the available memory whether peer lending lockups have frozen "
                "your cash past drafts before. Confirm that lockup track record before parking cash there."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know peer lending lockups have frozen "
                    "cash past drafts before, but the available memory does not establish that an annual premium draft is "
                    "locked mid-month. I cannot reject the yield circle from lockup history alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a locked yield circle fits. A mid-month premium "
                    "draft is documented, but I cannot tell from the available memory whether peer lending lockups have frozen "
                    "your cash past drafts before. Confirm that lockup track record before parking cash there."
                ),
            },
            "required": [
                "uses mid-month auto-insurance premium draft needing liquid cash",
                "uses peer-lending lockup freezing cash past drafts",
                "recommends declining locked yield circle this week",
            ],
            "absence_required": [
                "states that the peer-lending lockup evidence is missing",
                "does not infer harm from the yield-circle invite alone",
                "asks about lockup track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the premium-draft evidence is missing",
                    "does not infer draft harm from the invite alone",
                    "explicitly abstains from rejecting the yield circle",
                ],
                "ev_B": [
                    "states that the peer-lending lockup evidence is missing",
                    "does not infer harm from the yield-circle invite alone",
                    "asks about lockup track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "constrains", "target": "premium_draft_liquidity", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "peer_lending_lockup", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "peer_lending_pool_poor_fit", "hop": 2},
            ],
            "forbidden": ["never lend", "insurance ban", "guaranteed peer returns"],
            "distractor": {
                "timestamp": "2026-11-23T20:00:00Z",
                "user": f"{ca} said parking cash in a locked yield circle this week is amazing hype and worth it for yield.",
                "assistant": "Yield hype and premium-draft liquidity are different ledgers.",
                "why": "Peer-lending FOMO shares query surface but is not evidence about premium draft or lockup history.",
            },
            "evolving": {"premium_draft": "mid_month_locked", "peer_lending": "prior_lockup"},
        },
        "S19": {
            "name": "annual_trial_trap_x_thin_friday_buffer",
            "prefix_end": 106,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 103,
                    "fact": "Free trials that flip to annual billing have overdrafted the user when cancel was missed; monthly trials have been safer.",
                },
                "ev_B": {
                    "session_id": 105,
                    "fact": "This Friday's cash buffer is already thin after fixed outflows; no room for a surprise annual charge.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-12-04T16:30:00Z",
            "query": "Colleague floated an annual productivity-suite trial convert this week — fit for me?",
            "gold": (
                "Decline the annual productivity-suite trial convert this week. Free trials that flip to annual billing "
                "have overdrafted you when cancel was missed, and this Friday's cash buffer is already thin after fixed "
                "outflows. Prefer a monthly trial or skip."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether an annual trial convert fits. Annual-flip overdrafts are "
                "documented, but I cannot tell from the available memory whether this Friday's cash buffer is already thin. "
                "Confirm that buffer before converting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know this Friday's cash buffer is "
                    "thin, but the available memory does not establish that annual trial flips have overdrafted you. I cannot "
                    "reject the convert from the buffer alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether an annual trial convert fits. Annual-flip overdrafts are "
                    "documented, but I cannot tell from the available memory whether this Friday's cash buffer is already thin. "
                    "Confirm that buffer before converting."
                ),
            },
            "required": [
                "uses annual trial-flip overdraft pattern",
                "uses thin Friday cash buffer after fixed outflows",
                "recommends declining annual productivity-suite trial convert",
            ],
            "absence_required": [
                "states that the thin-Friday-buffer evidence is missing",
                "does not infer harm from the trial-convert invite alone",
                "asks about Friday buffer or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the annual-flip overdraft evidence is missing",
                    "does not infer overdraft harm from the invite alone",
                    "explicitly abstains from rejecting the trial convert",
                ],
                "ev_B": [
                    "states that the thin-Friday-buffer evidence is missing",
                    "does not infer harm from the trial-convert invite alone",
                    "asks about Friday buffer or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "annual_trial_overdraft", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "thin_friday_buffer", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "annual_suite_convert_poor_fit", "hop": 2},
            ],
            "forbidden": ["never use software", "guaranteed overdraft", "must cancel all trials"],
            "distractor": {
                "timestamp": "2026-12-01T14:00:00Z",
                "user": f"{cb} said an annual productivity-suite trial convert this week is amazing hype and worth it for tools.",
                "assistant": "Tool hype and Friday cash buffers are different ledgers.",
                "why": "Trial-convert FOMO shares query surface but is not evidence about annual-flip overdrafts or Friday buffer.",
            },
            "evolving": {"trial_billing": "annual_flip_risk", "friday_buffer": "already_thin"},
        },
        "S20": {
            "name": "airport_fx_markup_x_trip_cash_budgeted",
            "prefix_end": 111,
            "gold_tier": "v3_ultra",
            "evidence": {
                "ev_A": {
                    "session_id": 108,
                    "fact": "Away-from-home cash-machine markups have been steeper than pulling notes at the home branch first.",
                },
                "ev_B": {
                    "session_id": 110,
                    "fact": "Trip cash is already withdrawn and budgeted for the itinerary; no spare for last-minute markup hits.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-12-12T17:10:00Z",
            "query": "Crew floated a last-minute FX window stop before boarding — workable?",
            "gold": (
                "Decline the last-minute FX window stop before boarding. Away-from-home cash-machine markups have been "
                "steeper for you than home-branch pulls, and trip cash is already withdrawn and budgeted with no spare for "
                "window markups. Stick to the sealed envelope."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a last-minute FX window stop fits. cash-machine markup history is "
                "documented, but I cannot tell from the available memory whether trip cash is already withdrawn and "
                "budgeted. Confirm that envelope before using a window stop."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know trip cash is already withdrawn "
                    "and budgeted, but the available memory does not establish that away-from-home cash-machine markups have been steep for "
                    "you. I cannot reject the window stop from the envelope alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a last-minute FX window stop fits. cash-machine markup history is "
                    "documented, but I cannot tell from the available memory whether trip cash is already withdrawn and "
                    "budgeted. Confirm that envelope before using a window stop."
                ),
            },
            "required": [
                "uses away-from-home cash-machine markup pattern",
                "uses trip cash already withdrawn and budgeted",
                "recommends declining last-minute FX window stop before boarding",
            ],
            "absence_required": [
                "states that the trip-cash budget evidence is missing",
                "does not infer harm from the FX-window invite alone",
                "asks about trip envelope or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the cash-machine markup evidence is missing",
                    "does not infer fee harm from the invite alone",
                    "explicitly abstains from rejecting the FX window stop",
                ],
                "ev_B": [
                    "states that the trip-cash budget evidence is missing",
                    "does not infer harm from the FX-window invite alone",
                    "asks about trip envelope or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "airport_fx_markup", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "trip_cash_budgeted", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "airport_booth_topup_poor_fit", "hop": 2},
            ],
            "forbidden": ["never travel", "guaranteed FX advice", "bank ban"],
            "distractor": {
                "timestamp": "2026-12-09T09:30:00Z",
                "user": f"{ca} said a last-minute FX window stop before boarding is amazing for convenience.",
                "assistant": "Convenience hype and FX markups are different ledgers.",
                "why": "FX-window FOMO shares query surface but is not evidence about markup history or trip-cash budget.",
            },
            "evolving": {"airport_fx": "steep_markups", "trip_cash": "envelope_sealed"},
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
    parser = argparse.ArgumentParser(description="Generate finance/personal gold JSON items.")
    parser.add_argument(
        "--scenarios",
        default="S1-S5",
        help="Scenario scope: S1-S5, S6-S15, S16-S20, etc.",
    )
    args = parser.parse_args(argv)
    scenario_ids = parse_scenario_ids(args.scenarios)
    if scenario_ids == ("S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **FN_BATCH_CONFIG,
            "batch_id": "FN_GOLD_S6_S15_2026-07-18_v3ultra",
            "generator_name": "finance_gold_s6_s15_v3ultra",
        }
        report_name = "finance_gold_s6_s15_report.json"
        require_score_95 = True
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10"):
        batch_config = {
            **FN_BATCH_CONFIG,
            "batch_id": "FN_GOLD_S6_S10_2026-07-18_v3ultra",
            "generator_name": "finance_gold_s6_s10_v3ultra",
        }
        report_name = "finance_gold_s6_s10_report.json"
        require_score_95 = True
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        batch_config = {
            **FN_BATCH_CONFIG,
            "batch_id": "FN_GOLD_S11_S15_2026-07-18_v3ultra",
            "generator_name": "finance_gold_s11_s15_v3ultra",
        }
        report_name = "finance_gold_s11_s15_report.json"
        require_score_95 = True
    elif scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        batch_config = {
            **FN_BATCH_CONFIG,
            "batch_id": "FN_GOLD_S16_S20_2026-07-18_v3ultra",
            "generator_name": "finance_gold_s16_s20_v3ultra",
        }
        report_name = "finance_gold_s16_s20_report.json"
        require_score_95 = True
    else:
        batch_config = {
            **FN_BATCH_CONFIG,
            "batch_id": "FN_GOLD_S1_S5_2026-07-18_v2",
            "generator_name": "finance_gold_s1_s5_v2",
        }
        report_name = "finance_gold_s1_s5_report.json"
        require_score_95 = False
    arms = ("associative", "distractor", "absence")
    personas = load_personas()

    report_items: list[dict[str, Any]] = []
    failures = 0
    score_totals: list[float] = []
    released = 0

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
                score_pass = scores["total"] >= 95
                release = gate_pass and (score_pass if require_score_95 else True)
                if release:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    released += 1
                else:
                    failures += 1
                    if path.exists() and require_score_95:
                        path.unlink()
                report_items.append(
                    {
                        "sample_id": item["sample_id"],
                        "path": str(path.relative_to(PILOT_ROOT)),
                        "user_index": idx,
                        "scenario_id": sid,
                        "arm": arm,
                        "hard_gate_pass": gate_pass,
                        "score_pass_95": score_pass,
                        "released": release,
                        "errors": errors,
                        "metrics": item["validity_metrics"],
                        "scores": scores,
                    }
                )
                status = "RELEASE" if release else ("FAIL_GATE" if not gate_pass else "FAIL_SCORE")
                print(f"{status}\t{item['sample_id']}\tscore={scores['total']}")
                for error in errors:
                    print(f"  - {error}")
                if gate_pass and require_score_95 and not score_pass:
                    print(f"  - score {scores['total']} < 95; notes={scores.get('notes')}")

    n = len(report_items)
    n_gate = sum(1 for r in report_items if r["hard_gate_pass"])
    n_95 = sum(1 for r in report_items if r["score_pass_95"])
    report = {
        "generated_at": GENERATED_AT,
        "generator": batch_config["generator_name"],
        "scenario_scope": list(scenario_ids),
        "require_score_95": require_score_95,
        "n": n,
        "n_gate_pass": n_gate,
        "n_score_ge_95": n_95,
        "n_released": released,
        "n_fail": failures,
        "score_distribution": {
            "min": min(score_totals) if score_totals else 0,
            "max": max(score_totals) if score_totals else 0,
            "mean": round(sum(score_totals) / len(score_totals), 2) if score_totals else 0,
            "at_95": n_95,
        },
        "items": report_items,
    }
    manifest_dir = PILOT_ROOT / "manifests" / "finance"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    report_path = manifest_dir / report_name
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nSUMMARY gate {n_gate}/{n} · score>=95 {n_95}/{n} · RELEASED {released}/{n}")
    print(
        f"SCORES min={report['score_distribution']['min']} "
        f"max={report['score_distribution']['max']} mean={report['score_distribution']['mean']}"
    )
    print(f"REPORT {report_path}")
    return 0 if released == n else 1

if __name__ == "__main__":
    raise SystemExit(main())

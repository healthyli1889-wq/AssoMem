#!/usr/bin/env python3
"""Generate all 150 health/diet golden samples (10 users × 5 scenarios × 3 arms).

Canonical generator for the v2 shared-timeline gold architecture.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

PILOT_ROOT = Path(__file__).resolve().parents[3]
DOMAIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_ROOT / "tools" / "shared"))

from gold_lib import (
    GENERATED_AT,
    build_item,
    hard_gate_errors,
    model_input,
    output_path,
    score_item,
    session,
)

ROOT = PILOT_ROOT
HD = DOMAIN
PERSONAS_PATH = DOMAIN / "personas" / "personas_health_diet.json"
COMPUTED_BY = "tools/health/bin/generate_health_diet_gold_batch.py"

# ── User1 canonical sessions 1-24 (must match existing gold) ─────────────────

USER1_TIMELINE_1_24 = [
    session(
        1,
        "2026-01-05T19:10:00Z",
        "The Oura trend is finally steady again. Three regular bedtimes made a bigger difference than I expected.",
        "A short consistent stretch can be informative.",
    ),
    session(
        2,
        "2026-01-11T18:30:00Z",
        "I batch-cooked lentils and rice for the consulting days this week. Lunch decisions are handled.",
        "That removes one variable from the workday.",
    ),
    session(
        3,
        "2026-01-18T17:50:00Z",
        "My lower back was stiff after a long report, but a twenty-minute walk loosened it up.",
        "Useful to notice what changes it.",
    ),
    session(
        4,
        "2026-01-26T20:05:00Z",
        "A normal cheese portion after dinner was fine again. It does not seem like dairy across the board.",
        "Timing and what else you ate may matter.",
    ),
    session(
        5,
        "2026-02-03T12:15:00Z",
        "On early offsite days I leave before I can face breakfast. I usually reach the venue with only water in me.",
        "Is food available when you arrive?",
        "Usually not until the first scheduled break.",
    ),
    session(
        6,
        "2026-02-12T09:40:00Z",
        "I tested the rich yogurt-and-cream bowl again while I was still empty. Within an hour I was bloated and mentally foggy.",
        "Did the same thing happen when you had it later in the day?",
        "No. After a proper lunch, a small serving has been uneventful.",
    ),
    session(
        7,
        "2026-02-17T18:20:00Z",
        "The soup portions I froze held up well. I have two emergency dinners left.",
        "Good buffer for a crowded week.",
    ),
    session(
        8,
        "2026-02-23T21:00:00Z",
        "The offsite working-group email finally listed the 8am room and the first-session agenda. I saved the map.",
        "Good to have the logistics settled.",
    ),
    session(
        9,
        "2026-03-02T16:45:00Z",
        "A catering newsletter compared tasting formats for corporate offsites. I saved it with the working-group material.",
        "That may be useful when the agenda is finalized.",
    ),
    session(
        10,
        "2026-03-13T14:10:00Z",
        "The weekend meal prep worked. I did not end up grazing through the afternoon calls.",
        "Worth keeping as a repeatable setup.",
    ),
    session(
        11,
        "2026-03-19T21:15:00Z",
        "The orange-label can I sometimes buy after work suppresses my appetite until late the next morning, although it has not affected my sleep.",
        "Does an ordinary morning coffee do that too?",
        "No. I have only noticed the long appetite drop with that can late in the day.",
    ),
    session(
        12,
        "2026-03-24T13:30:00Z",
        "A small coffee before lunch was fine today, and I stopped there.",
        "That is useful to record separately.",
    ),
    session(
        13,
        "2026-03-29T18:55:00Z",
        "I finished the methods appendix before dinner. Having a defined stopping point helped.",
        "Clear edges make long work easier to contain.",
    ),
    session(
        14,
        "2026-04-02T10:25:00Z",
        "If I lead an early briefing without a real breakfast, I lose my verbal thread and start misreading numbers halfway through.",
        "Has breakfast made a consistent difference?",
        "Yes. Three no-breakfast briefings went badly; the ones after a proper meal were steady.",
    ),
    session(
        15,
        "2026-04-05T17:40:00Z",
        "The template for presenting the research findings is loaded, and the eight o'clock video room is confirmed. The remaining work is slide order.",
        "The logistics sound settled.",
    ),
    session(
        16,
        "2026-04-08T19:20:00Z",
        "The vending machine now has the tonic in orange packaging beside the sparkling water.",
        "That is a noticeable restock.",
    ),
    session(
        17,
        "2026-04-14T18:35:00Z",
        "The low-salt bean stew was better after a day in the fridge. I froze the extra portion.",
        "That is a useful weekday fallback.",
    ),
    session(
        18,
        "2026-04-19T13:15:00Z",
        "A modest bowl of low-sodium ramen at lunch sat fine. Portion and broth concentration seem to matter.",
        "That is a more specific observation than treating all ramen alike.",
    ),
    session(
        19,
        "2026-04-23T08:50:00Z",
        "Concentrated restaurant broth is fine for me at lunch, but when I start a briny bowl after seven I wake up thirsty and dried out.",
        "Has the timing difference repeated?",
        "Three late bowls caused it; earlier servings and my lighter soup at home did not.",
    ),
    session(
        20,
        "2026-04-27T17:25:00Z",
        "I cleared the client revisions before the end of the workday. No late scramble this time.",
        "That is a better finish.",
    ),
    session(
        21,
        "2026-05-01T11:05:00Z",
        "On Pittsburgh client-review days the debrief runs until about 6:50, and the drive back means I cannot meet anyone for food before 7:40.",
        "Is that timing fairly fixed?",
        "Yes. The team books the same review block and traffic does the rest.",
    ),
    session(
        22,
        "2026-05-04T18:10:00Z",
        "I replaced the desk water bottle. The old cap kept leaking into my bag.",
        "A mundane but worthwhile fix.",
    ),
    session(
        23,
        "2026-05-07T12:40:00Z",
        "Friends attending next week's Pittsburgh review asked when I would be free afterward. I have not answered yet.",
        "You can reply once the schedule is settled.",
    ),
    session(
        24,
        "2026-05-10T19:05:00Z",
        "A new ramen place is advertising the chef's dense-stock bowl as its dinner special.",
        "That is a specific menu pitch.",
    ),
]

# Sessions 25-32 (S4/S5 evidence + filler)
USER1_TIMELINE_25_32 = [
    session(
        25,
        "2026-05-14T07:30:00Z",
        "I left with only coffee at dawn again and energy cratered before ten — focus just collapsed.",
        "Has that happened on other empty-start days?",
        "Yes. It is consistent when I skip a real first meal.",
    ),
    session(
        26,
        "2026-05-18T08:15:00Z",
        "Venue rider I countersigned: personal meal parcels are refused at the threshold; caterers alone supply edibles until staff declare the halfway refresh window.",
        "Is there any way to bring your own fuel?",
        "Not according to the signed rider. We are limited to what caterers place indoors.",
    ),
    session(
        27,
        "2026-05-20T17:00:00Z",
        "Planning note: the orientation block is 8 to 12 and the host email highlights viennoiserie at entry — just filing logistics.",
        "Worth thinking through fuel before a long indoor stretch.",
    ),
    session(
        28,
        "2026-05-22T12:30:00Z",
        "Orientation email highlights viennoiserie at entry as the featured catering choice for the 8-to-12 block.",
        "That is a common default for long indoor sessions.",
    ),
    session(
        29,
        "2026-05-25T21:45:00Z",
        "I tried the chili-heavy tasting plate within two hours of bedtime and woke up with reflux. Earlier spicy lunches have been fine.",
        "Does the timing window matter more than the heat level?",
        "For me, yes — close to bedtime is what triggers it.",
    ),
    session(
        30,
        "2026-05-28T08:20:00Z",
        "After those reflux nights my voice wavers on the morning video sessions I lead. I sound less steady than I want.",
        "Has that shown up on early calls after calm evenings?",
        "No. It tracks the reflux nights specifically.",
    ),
    session(
        31,
        "2026-05-30T16:10:00Z",
        "The debrief calendar shows a 7:30am video room tomorrow. I blocked prep time tonight.",
        "Early speaking days need a calm evening plate.",
    ),
    session(
        32,
        "2026-06-01T18:40:00Z",
        "A colleague forwarded the 9pm chili tasting invite for tonight. It overlaps with tomorrow's early debrief.",
        "That is a tight pairing on the calendar.",
    ),
]

# Sessions 33-59 (S6-S10 evidence + filler; appended after S1-S5 timeline)
USER1_TIMELINE_33_59 = [
    session(
        33,
        "2026-06-04T17:55:00Z",
        "The summer block schedule is loaded. I am trying to keep recovery days visible on the calendar.",
        "That makes tradeoffs easier to see.",
    ),
    session(
        34,
        "2026-06-07T20:30:00Z",
        "A strong roast after the workday ends left me waking twice overnight. Morning caffeine before midday has never done that.",
        "Has the late timing repeated?",
        "Twice now. It is specifically an after-work strong cup, not caffeine in general.",
    ),
    session(
        35,
        "2026-06-09T13:20:00Z",
        "I walked the long way back from the cafe district. Nice reset between calls.",
        "Small movement breaks add up.",
    ),
    session(
        36,
        "2026-06-11T07:10:00Z",
        "After those chopped-up nights I get lightheaded in the before-breakfast studio class — I stopped booking the dawn slot when sleep was bad.",
        "Does a full night change it?",
        "Yes. On rested nights the same class is fine.",
    ),
    session(
        37,
        "2026-06-13T16:40:00Z",
        "The studio sent a promo for dawn spin blocks. I saved it without replying.",
        "Early classes need a predictable recovery window.",
    ),
    session(
        38,
        "2026-06-14T18:05:00Z",
        "Office chat says a post-four strong cup is harmless before an early ride.",
        "Office folklore around caffeine timing is loud.",
    ),
    session(
        39,
        "2026-06-16T19:15:00Z",
        "Reorganized pantry labels. Minor win.",
        "Small order helps on busy weeks.",
    ),
    session(
        40,
        "2026-06-18T21:50:00Z",
        "A dense pulse-heavy plate near bedtime left me bloated all night. Midday portions of similar food were fine.",
        "Does the late timing matter for you?",
        "Clearly. Three late pulse-heavy dinners did it; earlier portions did not.",
    ),
    session(
        41,
        "2026-06-20T12:05:00Z",
        "Short walk after lunch cleared the afternoon fog.",
        "Worth repeating when the schedule allows.",
    ),
    session(
        42,
        "2026-06-22T08:35:00Z",
        "On uncomfortable mornings formal client pitches feel distracting — I am less present than I want.",
        "Has that tracked the heavy late dinners?",
        "Yes. Calm mornings after lighter evenings are fine in the same clothes.",
    ),
    session(
        43,
        "2026-06-24T17:30:00Z",
        "The nine o'clock structured-jacket pitch deck is almost final — still weighing whether tomorrow's late group meal matters.",
        "Early prep reduces morning scramble.",
    ),
    session(
        44,
        "2026-06-25T14:20:00Z",
        "Group meal invite mentions a late start and a plant-protein-heavy chef's table — filing the logistics only.",
        "Long evenings before speaking days need a plan.",
    ),
    session(
        45,
        "2026-06-27T09:00:00Z",
        "Periodic bloodwork requires nothing by mouth until the technician completes collection, usually early afternoon.",
        "Is that timing fairly fixed?",
        "Yes. The clinic books the same morning block.",
    ),
    session(
        46,
        "2026-06-29T11:40:00Z",
        "Picked up the lab requisition. No food until the draw, as usual.",
        "Worth blocking lunch plans around that.",
    ),
    session(
        47,
        "2026-07-01T15:55:00Z",
        "Deferring refueling until a late mid-day meal after collection makes the afternoon cognition window collapse — details slip on dense material.",
        "Has eating soon after collection helped?",
        "Always. Waiting until mid-afternoon or later costs me the whole afternoon.",
    ),
    session(
        48,
        "2026-07-03T10:10:00Z",
        "Dense post-lunch work blocks are stacked next week after the panel day — fuel timing may matter.",
        "Worth blocking hospitality meals around that.",
    ),
    session(
        49,
        "2026-07-04T13:45:00Z",
        "Calendar shows a hosted meal block right after the bloodwork appointment next week — exact timing still fuzzy.",
        "Worth confirming before the collection day.",
    ),
    session(
        50,
        "2026-07-06T22:15:00Z",
        "Even two drinks at an evening reception threw off my next-morning routine — I skipped steps I normally never miss.",
        "Was it just one night?",
        "Twice. Small amounts still disrupted the sequence.",
    ),
    session(
        51,
        "2026-07-08T07:45:00Z",
        "My morning supplement protocol needs food at a consistent time. When the routine slips, I feel off for hours.",
        "Is the timing as important as the dose?",
        "For me, yes — irregular mornings undo the benefit.",
    ),
    session(
        52,
        "2026-07-10T16:20:00Z",
        "Industry reception tonight lists complimentary cocktails on the invite.",
        "Evening events before dawn sequences are worth weighing.",
    ),
    session(
        53,
        "2026-07-11T08:00:00Z",
        "Blocked tomorrow morning for the supplement-and-breakfast sequence.",
        "Protecting that window is sensible.",
    ),
    session(
        54,
        "2026-07-12T19:30:00Z",
        "Someone said skipping the bar at mixers is antisocial and not worth it.",
        "Social pressure around drinks is common.",
    ),
    session(
        55,
        "2026-07-14T18:10:00Z",
        "Weekday staples hold desk blocks but I empty out when output is high.",
        "Portion size may need a mode switch.",
        "Desk portions are not enough when output is high.",
    ),
    session(
        56,
        "2026-07-16T12:30:00Z",
        "Short urban hike last month with the same containers left me shaky by hour four.",
        "Active days seem to need different fuel density.",
    ),
    session(
        57,
        "2026-07-18T09:40:00Z",
        "The mapped route tomorrow is endurance-length with zero purchase points.",
        "That is a different fueling problem than a desk week.",
    ),
    session(
        58,
        "2026-07-19T17:05:00Z",
        "Outing group chat says packing light means relying on sedentary-week staples you already have.",
        "Light packs and long circuits do not always align.",
    ),
    session(
        59,
        "2026-07-20T07:20:00Z",
        "Clear skies expected for the alpine circuit tomorrow. I have not finalized the pack list yet.",
        "Worth deciding fuel before you are on the route.",
    ),
]

# Sessions 60-89 (S11-S15 evidence + filler; gold v2 tier)
USER1_TIMELINE_60_89 = [
    session(60, "2026-07-22T18:00:00Z", "Recovery week is finally on the calendar again.", "Tradeoffs are easier to see."),
    session(
        61,
        "2026-07-24T20:30:00Z",
        "Cold plunge after hard training days speeds my recovery — warm-pool-only weeks feel sluggish the next morning.",
        "Has that contrast repeated?",
        "Twice this month. It is the cold plunge specifically, not swimming in general.",
    ),
    session(62, "2026-07-26T13:20:00Z", "Walked the long way back from the pool deck. Nice reset.", "Small movement breaks add up."),
    session(
        63,
        "2026-07-28T07:10:00Z",
        "Sports med this month: avoid overhead stroke loads for about four weeks while shoulder impingement settles.",
        "Is that non-negotiable for now?",
        "Yes. I am treating it as a hard training boundary.",
    ),
    session(64, "2026-07-30T16:40:00Z", "Pool newsletter arrived. I only skimmed the facility-hours section.", "Not every mailer needs a decision."),
    session(65, "2026-07-31T18:05:00Z", "Logged shoulder mobility drills from sports med. Keeping overhead moves light this month.", "Rehab notes are worth tracking."),
    # S12
    session(66, "2026-08-02T19:15:00Z", "Restocked the fridge probiotics. Timing still matters for me.", "Gut routines are not one-size."),
    session(
        67,
        "2026-08-04T21:50:00Z",
        "Refrigerated probiotic capsules on an empty stomach leave me bloated by afternoon — with food they are fine.",
        "Has empty-stomach timing repeated?",
        "Yes. Three fasted mornings did it; with-breakfast days were uneventful.",
    ),
    session(68, "2026-08-06T12:30:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        69,
        "2026-08-08T08:45:00Z",
        "Tuesday hospital rounds start at six-thirty with no food until mid-morning.",
        "Is that slot movable?",
        "Not easily. The service schedule is fixed.",
    ),
    session(70, "2026-08-10T14:10:00Z", "Residency group chat is noisy about supplement rituals. I muted the thread.", "Mute buttons save attention."),
    session(71, "2026-08-11T17:20:00Z", "Printed the August service calendar. Tuesday dawn blocks are locked.", "Paper copies help on busy weeks."),
    # S13
    session(
        72,
        "2026-08-13T10:05:00Z",
        "Natural low-sulfite pours trigger flushing and poor sleep for me — conventional wine in moderation has been fine.",
        "Has the natural-wine pattern repeated?",
        "Yes. Three natural pours did it; conventional glasses at lunch did not.",
    ),
    session(73, "2026-08-14T15:40:00Z", "Guest-room linens are washed for the weekend hosting block.", "Hosting prep has a timeline."),
    session(
        74,
        "2026-08-16T19:30:00Z",
        "Hosting in-laws Saturday through Sunday needs clear-headed mornings for meal prep.",
        "Is that deadline firm?",
        "Yes. Breakfast and lunch prep are already on the list.",
    ),
    session(75, "2026-08-17T11:15:00Z", "Partner ordered a mixed case for the guest weekend. I have not opened it yet.", "Cases can wait for a plan."),
    session(76, "2026-08-18T16:50:00Z", "Guest-room checklist is almost done. Saturday breakfast prep starts early.", "Hosting logistics are the priority."),
    # S14
    session(
        77,
        "2026-08-20T22:15:00Z",
        "Fiber supplement before vigorous exercise causes mid-session cramping — taking it with dinner later is fine.",
        "Was that a one-off?",
        "No. Twice on pre-workout timing; dinner timing was uneventful.",
    ),
    session(78, "2026-08-22T07:45:00Z", "Track bag is packed. Session timing changed this month.", "Dawn blocks need a different fuel plan."),
    session(
        79,
        "2026-08-24T16:20:00Z",
        "Track club moved my interval block to dawn Thursday this month.",
        "Is that slot firm?",
        "Yes. It is already on the calendar.",
    ),
    session(80, "2026-08-25T08:00:00Z", "Club forum is loud about pre-session rituals. I am not adopting forum norms.", "Forum norms are not stomach facts."),
    session(81, "2026-08-26T19:30:00Z", "Packed electrolytes and a light snack for the dawn block. Timing still feels tight.", "Fuel timing matters on short sleep."),
    # S15
    session(
        82,
        "2026-08-28T18:10:00Z",
        "Late refined-dessert evenings bump my dawn glucose reading above the personal target I track.",
        "Has that pattern repeated?",
        "Yes. Pastry-preview nights do it; lighter evenings do not.",
    ),
    session(83, "2026-08-30T12:30:00Z", "Glucose log is updated for the week. Thursday check-in is on the calendar.", "Fasting context matters for labs."),
    session(
        84,
        "2026-09-01T09:40:00Z",
        "Endocrinologist check-in Thursday at seven-thirty implies fasting labs.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(85, "2026-09-02T17:05:00Z", "Pastry club sent another social invite. I filed it without replying.", "Invites can wait for a lab window."),
    session(86, "2026-09-03T07:20:00Z", "Set out the fasting-lab checklist for Thursday morning. No food after the draw.", "Lab mornings need a clean routine."),
]

# Sessions 90-111 (S16-S20 evidence + filler; gold v2 tier)
USER1_TIMELINE_90_111 = [
    # S16
    session(87, "2026-09-05T18:00:00Z", "Autumn vitals calendar is printed. Afternoon walk blocks are marked.", "Paper copies help on busy weeks."),
    session(
        88,
        "2026-09-07T20:45:00Z",
        "Oil-kitchen lunches leave me sluggish with elevated post-walk glucose — grilled options have been fine.",
        "Has that pattern repeated?",
        "Yes. Twice on fryer-heavy lunches; grilled plates did not.",
    ),
    session(89, "2026-09-08T13:10:00Z", "Short walk after lunch. Nice reset.", "Small movement breaks add up."),
    session(
        90,
        "2026-09-10T08:30:00Z",
        "Wednesday corridor vitals block needs stable post-meal readings — already on the calendar.",
        "Is that timing firm?",
        "Yes. It is already booked.",
    ),
    session(91, "2026-09-11T16:55:00Z", "Cafeteria posted a grease-line signup blurb. I filed it without replying.", "Invites can wait for a calendar plan."),
    # S17
    session(92, "2026-09-13T19:20:00Z", "Restocked pantry supplies for the autumn sprint. Timing still matters.", "Clinic routines are not one-size."),
    session(
        93,
        "2026-09-15T21:10:00Z",
        "Fizz-heavy zero-cal drinks cause bloating on sensitive gut evenings — still water has been fine.",
        "Has the fizz-heavy pattern repeated?",
        "Yes. Three carbonated evenings did it; still-water days were uneventful.",
    ),
    session(94, "2026-09-16T12:40:00Z", "Short lunch away from the desk. Helped the afternoon block.", "Breaks protect afternoon quality."),
    session(
        95,
        "2026-09-18T08:50:00Z",
        "Friday scope prep window requires clear liquids with minimal bloating Wednesday night — already on the calendar.",
        "Is that slot movable?",
        "Not easily. The prep schedule is fixed.",
    ),
    session(96, "2026-09-19T14:25:00Z", "Clinic chat is noisy about fizz rituals. I muted the thread.", "Mute buttons save attention."),
    # S18
    session(97, "2026-09-21T10:05:00Z", "Printed the autumn lab calendar. Solo prep blocks are marked.", "Lab weeks need a clean routine."),
    session(
        98,
        "2026-09-23T15:35:00Z",
        "Large crunch-bowl evenings cause bloating before dawn blood draws — cooked veg portions have been fine.",
        "Has the crunch-bowl pattern repeated?",
        "Yes. Three raw-heavy evenings did it; cooked veg portions did not.",
    ),
    session(99, "2026-09-24T11:20:00Z", "Caterer mailer landed. I filed it without replying.", "Invites can wait for a draw plan."),
    session(
        100,
        "2026-09-26T07:15:00Z",
        "Thursday dawn panel draw needs a settled morning stomach — late-slot food signup is already booked through the night before.",
        "Is that timing firm?",
        "Yes. The draw is already scheduled.",
    ),
    session(101, "2026-09-27T16:50:00Z", "Packed reference notes for the dawn draw. Timing still feels tight.", "Draw timing matters on lab weeks."),
    # S19
    session(102, "2026-09-29T18:15:00Z", "Skills demo outline is packed. Wednesday slot is on the calendar.", "Demo weeks need protected prep blocks."),
    session(
        103,
        "2026-10-01T22:00:00Z",
        "I retain portioning skills best with whole-food prep — blender-only practice weakens demo performance for me.",
        "Has the blender-only pattern repeated?",
        "Yes. Twice on blender-only prep; whole-food practice did not.",
    ),
    session(104, "2026-10-02T08:00:00Z", "Culinary forum is loud about blender-only run-throughs. I am not adopting forum defaults.", "Forum norms are not prep facts."),
    session(
        105,
        "2026-10-04T16:30:00Z",
        "Prior blender-only rehearsal went poorly before skills demo night — I misjudged portions twice.",
        "Harsh memory. Was the material unfamiliar?",
        "No. The format fought my process.",
    ),
    session(106, "2026-10-05T19:40:00Z", "Printed the skills demo calendar. Solo whole-food prep blocks are locked.", "Paper copies help on busy weeks."),
    # S20
    session(107, "2026-10-07T18:05:00Z", "Stacked telehealth week memo landed. I only skimmed the corridor-transfer section.", "Not every memo needs a decision."),
    session(
        108,
        "2026-10-09T07:50:00Z",
        "Corridor transfers without snacks leave me shaky and foggy — light bar transfers have been fine.",
        "Has the no-snack transfer pattern repeated?",
        "Yes. Three empty-transfer blocks did it; light bar transfers did not.",
    ),
    session(109, "2026-10-10T14:15:00Z", "Clinic shuttle blurb posted. I filed it without replying.", "Invites can wait for a telehealth plan."),
    session(
        110,
        "2026-10-12T09:25:00Z",
        "Stacked telehealth week requires steady afternoon cognition with no scheduled meal gap — already on the calendar.",
        "Is that timing firm?",
        "Yes. The telehealth week is already booked.",
    ),
    session(111, "2026-10-13T17:30:00Z", "Packed a light bar for a possible corridor day. Transfer timing still feels tight.", "Telehealth weeks need an energy plan."),
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


CANONICAL_TIMELINE = monotonic_timeline(
    USER1_TIMELINE_1_24
    + USER1_TIMELINE_25_32
    + USER1_TIMELINE_33_59
    + USER1_TIMELINE_60_89
    + USER1_TIMELINE_90_111
)


def persona_paint_config(persona: dict[str, Any]) -> dict[str, str]:
    idx = persona["user_index"]
    traits = persona["stable_traits"]
    voice = persona.get("voice", "measured")

    configs: dict[int, dict[str, str]] = {
        1: {
            "tracker": "Oura Ring",
            "tracker_short": "Oura",
            "location": "Pittsburgh",
            "location_adj": "Pittsburgh suburbs",
            "role": "coatings industry consultant",
            "role_short": "consulting",
            "colleague_a": "Maya",
            "colleague_b": "Evan",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "Pittsburgh client-review",
            "workshop_type": "coatings workshop",
        },
        2: {
            "tracker": "Apple Watch",
            "tracker_short": "Apple Watch",
            "location": "Amsterdam",
            "location_adj": "Netherlands",
            "role": "Netherlands-based professional",
            "role_short": "office",
            "colleague_a": "Sanne",
            "colleague_b": "Pieter",
            "drink_brand": "Volt Leaf",
            "venue_type": "client site",
            "review_context": "Amsterdam client-review",
            "workshop_type": "compliance workshop",
        },
        3: {
            "tracker": "sleep tracker",
            "tracker_short": "tracker",
            "location": "the city",
            "location_adj": "urban",
            "role": "knowledge worker",
            "role_short": "desk",
            "colleague_a": "Jordan",
            "colleague_b": "Alex",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "quarterly review",
            "workshop_type": "morning workshop",
        },
        4: {
            "tracker": "health app",
            "tracker_short": "app",
            "location": "suburbs",
            "location_adj": "family suburb",
            "role": "family-oriented professional",
            "role_short": "weekday",
            "colleague_a": "Nina",
            "colleague_b": "Marcus",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "client review",
            "workshop_type": "training workshop",
        },
        5: {
            "tracker": "wearable",
            "tracker_short": "wearable",
            "location": "Chicago",
            "location_adj": "Chicago metro",
            "role": "busy professional",
            "role_short": "calendar-heavy",
            "colleague_a": "Rosa",
            "colleague_b": "Daniel",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "Chicago client-review",
            "workshop_type": "strategy workshop",
        },
        6: {
            "tracker": "sleep log",
            "tracker_short": "log",
            "location": "Berlin",
            "location_adj": "Berlin",
            "role": "structured weekday professional",
            "role_short": "weekday",
            "colleague_a": "Lena",
            "colleague_b": "Tobias",
            "drink_brand": "Volt Leaf",
            "venue_type": "client site",
            "review_context": "Berlin review",
            "workshop_type": "process workshop",
        },
        7: {
            "tracker": "fitness band",
            "tracker_short": "band",
            "location": "Austin",
            "location_adj": "Austin",
            "role": "social evening planner",
            "role_short": "evening-social",
            "colleague_a": "Chris",
            "colleague_b": "Sam",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "Austin review",
            "workshop_type": "team workshop",
        },
        8: {
            "tracker": "recovery tracker",
            "tracker_short": "tracker",
            "location": "the hospital district",
            "location_adj": "clinical schedule",
            "role": "early clinical professional",
            "role_short": "clinical",
            "colleague_a": "Priya",
            "colleague_b": "James",
            "drink_brand": "Volt Leaf",
            "venue_type": "conference block",
            "review_context": "morning rounds review",
            "workshop_type": "clinical workshop",
        },
        9: {
            "tracker": "step counter",
            "tracker_short": "counter",
            "location": "office campus",
            "location_adj": "steady office",
            "role": "office routine keeper",
            "role_short": "office",
            "colleague_a": "Helga",
            "colleague_b": "Karl",
            "drink_brand": "Volt Leaf",
            "venue_type": "offsite",
            "review_context": "quarterly review",
            "workshop_type": "operations workshop",
        },
        10: {
            "tracker": "sleep app",
            "tracker_short": "app",
            "location": "Ann Arbor",
            "location_adj": "campus",
            "role": "psychology + AI research student",
            "role_short": "research",
            "colleague_a": "Mia",
            "colleague_b": "Leo",
            "drink_brand": "Volt Leaf",
            "venue_type": "seminar block",
            "review_context": "lab review",
            "workshop_type": "morning seminar workshop",
        },
    }
    base = configs.get(idx, configs[3])
    base["trait0"] = traits[0] if traits else base["role"]
    base["voice"] = voice.split(",")[0]
    return base


def paint_session_u1(s: dict[str, Any], paint: dict[str, str]) -> dict[str, Any]:
    """Adapt user1 session text for other personas while preserving logical facts."""
    sid = s["session_id"]
    ts = s["timestamp"]
    dlg = deepcopy(s["dialogue"])

    def set_user(text: str) -> None:
        dlg[0]["content"] = text

    def set_asst(text: str) -> None:
        dlg[1]["content"] = text

    def set_followup(text: str) -> None:
        if len(dlg) > 2:
            dlg[2]["content"] = text

    if sid == 1:
        set_user(
            f"The {paint['tracker_short']} trend is finally steady again. Three regular bedtimes made a bigger difference than I expected."
        )
    elif sid == 2:
        set_user(
            f"I batch-cooked grains and protein for the {paint['role_short']} days this week. Lunch decisions are handled."
        )
    elif sid == 3:
        set_user(
            "My shoulders were tight after a long desk block, but a twenty-minute walk loosened them up."
        )
    elif sid == 5:
        set_user(
            "On early departure days I leave before I can face breakfast. I usually arrive with only water in me."
        )
    elif sid == 8:
        set_user(
            f"The {paint['venue_type']} email finally listed the 8am room and the first-session agenda. I saved the map."
        )
    elif sid == 11:
        set_user(
            f"The orange-label can I sometimes buy after work suppresses my appetite until late the next morning, although it has not affected my sleep."
        )
    elif sid == 14:
        set_user(
            "If I lead an early briefing without a real breakfast, I lose my verbal thread and start misreading numbers halfway through."
        )
    elif sid == 15:
        set_user(
            "The template for presenting the research findings is loaded, and the eight o'clock video room is confirmed. The remaining work is slide order."
        )
    elif sid == 21:
        set_user(
            f"On {paint['location']} client-review days the debrief runs until about 6:50, and the commute back means I cannot meet anyone for food before 7:40."
        )
    elif sid == 23:
        set_user(
            f"Friends attending next week's {paint['location']} review asked when I would be free afterward. I have not answered yet."
        )
    elif sid == 25:
        set_user(
            "I left with only coffee at dawn again and energy cratered before ten — focus just collapsed."
        )
    elif sid == 26:
        set_user(
            "Venue rider I countersigned: personal meal parcels are refused at the threshold; caterers alone supply edibles until staff declare the halfway refresh window."
        )
    elif sid == 27:
        set_user(
            "Planning note: the orientation block is 8 to 12 and the host email highlights viennoiserie at entry — just filing logistics."
        )
    elif sid == 28:
        set_user(
            "Orientation email highlights viennoiserie at entry as the featured catering choice for the 8-to-12 block."
        )
    elif sid == 29:
        set_user(
            "I tried the chili-heavy tasting plate within two hours of bedtime and woke up with reflux. Earlier spicy lunches have been fine."
        )
    elif sid == 30:
        set_user(
            "After those reflux nights my voice wavers on the morning video sessions I lead. I sound less steady than I want."
        )
    elif sid == 31:
        set_user(
            "The debrief calendar shows a 7:30am video room tomorrow. I blocked prep time tonight."
        )
    elif sid == 32:
        set_user(
            "A colleague forwarded the 9pm chili tasting invite for tonight. It overlaps with tomorrow's early debrief."
        )
    elif sid == 36:
        set_user(
            "After those chopped-up nights I get lightheaded in the before-breakfast studio class — I stopped booking the dawn slot when sleep was bad."
        )
    elif sid == 42:
        set_user(
            "On bloated mornings a fitted blazer feels distracting during client pitches — I am less present than I want."
        )
    elif sid == 45:
        set_user(
            "Periodic bloodwork requires nothing by mouth until the technician completes collection, usually early afternoon."
        )
    elif sid == 51:
        set_user(
            "My morning supplement protocol needs food at a consistent time. When the routine slips, I feel off for hours."
        )
    elif sid == 57:
        set_user(
            "The mapped route tomorrow is endurance-length with zero purchase points."
        )

    return {"session_id": sid, "timestamp": ts, "dialogue": dlg}


def build_timeline(persona: dict[str, Any]) -> list[dict[str, Any]]:
    base = deepcopy(CANONICAL_TIMELINE)
    if persona["user_index"] == 1:
        return base
    paint = persona_paint_config(persona)
    return [paint_session_u1(s, paint) for s in base]


def build_scenarios(persona: dict[str, Any]) -> dict[str, Any]:
    paint = persona_paint_config(persona)
    loc = paint["location"]
    ca, cb = paint["colleague_a"], paint["colleague_b"]
    brand = paint["drink_brand"]
    review = paint["review_context"]
    workshop = paint["workshop_type"]

    return {
        "S1": {
            "name": "fasted_offsite_x_cream_tasting",
            "prefix_end": 9,
            "evidence": {
                "ev_A": {
                    "session_id": 6,
                    "fact": "Cream-heavy food causes bloating and cognitive fog only when eaten on an empty stomach; a small serving after a proper meal has been tolerated.",
                },
                "ev_B": {
                    "session_id": 5,
                    "fact": "On early offsite mornings the user leaves without breakfast and usually has no food before the venue's first break.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-03-09T17:30:00Z",
            "query": "The gathering starts with an 8am cream-and-soft-cheese tasting before the first working session. Would that be a good way for me to join the group?",
            "gold": (
                "Skip the tasting portion this time. On early offsite mornings you normally arrive without "
                "having eaten, and cream-heavy food has caused bloating and fog specifically when you were empty. Join only "
                "after the tasting, unless you change the plan by arranging a substantial non-cream breakfast beforehand."
            ),
            "absence_gold": (
                "Cream-heavy food has caused problems when you were empty and has been tolerated after a proper meal, but I "
                "cannot tell whether you will have eaten before this event. I can give the conditional guidance to eat first "
                "or skip the tasting, but I cannot determine whether this specific plan fits your routine."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know early offsite mornings often "
                    "leave you without breakfast, but the available memory does not establish that cream-heavy food causes "
                    "you a problem in that state. I cannot reject this tasting based on the routine alone."
                ),
                "ev_B": (
                    "Cream-heavy food has caused problems when you were empty and has been tolerated after a proper meal, but "
                    "I cannot tell whether you will have eaten before this event. I can give the conditional guidance to eat "
                    "first or skip the tasting, but I cannot determine whether this specific plan fits your routine."
                ),
            },
            "required": [
                "uses the empty-stomach conditional rather than treating all dairy as harmful",
                "uses the early-offsite no-breakfast routine",
                "recommends eating substantial food first or skipping the tasting portion",
            ],
            "absence_required": [
                "states that meal/fasting status is missing",
                "does not infer that the user will arrive fasted",
                "asks whether substantial food can be eaten first or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the cream-response evidence is missing",
                    "does not infer a dairy or cream intolerance",
                    "explicitly abstains from rejecting the tasting",
                ],
                "ev_B": [
                    "states that meal/fasting status is missing",
                    "does not infer that the user will arrive fasted",
                    "asks whether substantial food can be eaten first or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "conditional_on", "target": "fasted_cream_reaction", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "arrives_fasted_at_early_offsite", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "cream_tasting_recreates_risk_condition",
                    "hop": 2,
                },
                {
                    "source": "cream_tasting_recreates_risk_condition",
                    "relation": "constrains",
                    "target": "answer_to_cue",
                    "hop": 3,
                },
            ],
            "forbidden": [
                "lactose intolerance diagnosis",
                "all dairy is unsafe",
                "the user definitely ate breakfast",
            ],
            "distractor": {
                "timestamp": "2026-03-05T20:20:00Z",
                "user": f"{ca} mentioned that her team used a cream-and-soft-cheese tasting as an icebreaker at last year's offsite, and she enjoyed meeting people there.",
                "assistant": "It sounds as though the social format worked well for her group.",
                "why": "A third party's similar offsite tasting is query-relevant but provides no evidence about this user's fasted morning response.",
            },
            "evolving": {
                "cream_response": "conditional_on_empty_stomach",
                "early_offsite_meal_state": "usually_fasted_until_first_break",
            },
        },
        "S2": {
            "name": "late_appetite_suppression_x_breakfast_dependent_briefing",
            "prefix_end": 16,
            "evidence": {
                "ev_A": {
                    "session_id": 11,
                    "fact": f"The orange-label can consumed after work suppresses the user's appetite until late the next morning.",
                },
                "ev_B": {
                    "session_id": 14,
                    "fact": "Leading an early briefing without a real breakfast makes the user lose their verbal thread and misread numbers.",
                },
            },
            "withheld_in_absence": "ev_A",
            "query_timestamp": "2026-04-10T17:05:00Z",
            "query": f"It is after five, and the vending machine's only option is the tonic in orange packaging. I need to present research findings at eight tomorrow; would taking one now fit?",
            "gold": (
                f"Skip the orange-label {brand} tonic unless you can commit to eating a real breakfast despite low appetite. "
                "That late can has suppressed your appetite into the next morning, and your no-breakfast early briefings have "
                "ended in lost verbal threads and misread numbers. A different drink is the safer fit for this task."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. The available memory says that skipping "
                "breakfast can disrupt your early briefings, but it does not establish that Volt Leaf changes your appetite. "
                "I cannot tell whether this drink makes a no-breakfast morning more likely without that missing history."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. The available memory says that skipping "
                    "breakfast can disrupt your early briefings, but it does not establish that Volt Leaf changes your appetite. "
                    "I cannot tell whether this drink makes a no-breakfast morning more likely without that missing history."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. The available memory says that a late "
                    "orange-label can suppresses your appetite into the morning, but it does not establish that a low-appetite "
                    "morning impairs your briefing. I cannot infer the task consequence without that missing history."
                ),
            },
            "required": [
                "links the late orange-label can to next-morning appetite suppression",
                "links missing breakfast to lost verbal thread and number-reading errors",
                "recommends avoiding Volt Leaf or explicitly securing a real breakfast",
            ],
            "absence_required": [
                "states that the drink-to-appetite link is missing",
                "does not infer that Volt Leaf will cause breakfast skipping",
                "explicitly abstains from the personalized recommendation",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the drink-to-appetite link is missing",
                    "does not infer that Volt Leaf will cause breakfast skipping",
                    "explicitly abstains from the personalized recommendation",
                ],
                "ev_B": [
                    "states that the appetite-to-briefing consequence is missing",
                    "does not infer briefing failure from appetite suppression",
                    "explicitly abstains from the personalized recommendation",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "next_morning_appetite_suppression", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "fasted_early_briefing_failure", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "late_volt_leaf_threatens_breakfast_dependent_briefing",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "energy drinks always suppress appetite",
                "Volt Leaf always ruins breakfast",
                "the briefing will definitely fail",
            ],
            "distractor": {
                "timestamp": "2026-04-07T09:30:00Z",
                "user": f"A colleague recommended the tonic in orange packaging from her vending machine; she took one after five before presenting findings at eight and felt fine.",
                "assistant": "That describes how it affected her during that deadline.",
                "why": "Another person's near-identical use of the same product is highly query-similar but is not evidence about this user's appetite or breakfast-dependent briefing performance.",
            },
            "evolving": {
                "late_volt_leaf_effect": "next_morning_appetite_suppression",
                "fasted_task_cost": "early_briefing_disruption",
            },
        },
        "S3": {
            "name": "late_briny_broth_x_client_review_timing",
            "prefix_end": 24,
            "evidence": {
                "ev_A": {
                    "session_id": 19,
                    "fact": "Concentrated briny broth is tolerated earlier but leaves the user thirsty and dry overnight when started after 7pm.",
                },
                "ev_B": {
                    "session_id": 21,
                    "fact": f"The user's recurring {loc} client-review schedule prevents dinner before about 7:40pm.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-12T18:45:00Z",
            "query": f"Friends invited me for the chef's dense-stock ramen after tomorrow's {loc} review. Does that dinner work for me?",
            "gold": (
                "The concentrated-broth special is a poor fit after that review. Your recurring client-review schedule puts "
                "dinner no earlier than about 7:40pm, and concentrated briny broth started after seven has left you thirsty and "
                "dry overnight. Join with a lighter-broth order or choose the special on an earlier day instead."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether this specific dinner recreates the late-broth problem. "
                "Concentrated briny broth has caused overnight thirst when started after seven, but I cannot tell from the "
                "available memory when you will be free after tomorrow's review. Confirm the dinner time before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the recurring review schedule "
                    "delays dinner until about 7:40pm, but the available memory does not establish that concentrated broth is "
                    "a problem for you at that hour. I cannot reject the dinner from timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether this specific dinner recreates the late-broth problem. "
                    "Concentrated briny broth has caused overnight thirst when started after seven, but I cannot tell from the "
                    "available memory when you will be free after tomorrow's review. Confirm the dinner time before deciding."
                ),
            },
            "required": [
                "uses the after-7pm condition on concentrated briny broth",
                "uses the recurring client-review schedule that delays dinner until about 7:40pm",
                "recommends a lighter broth or moving the special to an earlier day",
            ],
            "absence_required": [
                "states that the post-review dinner time is missing",
                "does not infer that dinner must occur after seven",
                "asks for the dinner time or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-broth response is missing",
                    "does not infer harm from a late dinner alone",
                    "explicitly abstains from rejecting the dinner",
                ],
                "ev_B": [
                    "states that the post-review dinner time is missing",
                    "does not infer that dinner must occur after seven",
                    "asks for the dinner time or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "conditional_on", "target": "late_broth_dryness", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "post_review_dinner_after_7", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "review_day_ramen_recreates_late_broth_condition",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "all briny food is unsafe",
                "all ramen is unsafe",
                "the client review always runs late",
            ],
            "distractor": {
                "timestamp": "2026-05-06T12:20:00Z",
                "user": f"{cb} said the chef's dense-stock ramen after his {loc} review was excellent last weekend.",
                "assistant": "It sounds as though he enjoyed the meal.",
                "why": "A third party's experience with the same menu item is query-relevant but does not establish this user's time-conditional broth response.",
            },
            "evolving": {
                "concentrated_broth_effect": "overnight_dryness_only_after_7pm",
                "client_review_meal_time": "not_before_19_40",
            },
        },
        "S4": {
            "name": "skip_breakfast_x_pastry_workshop",
            "prefix_end": 28,
            "evidence": {
                "ev_A": {
                    "session_id": 25,
                    "fact": "Skipping a real morning meal leads to a sharp mid-morning energy crash for the user.",
                },
                "ev_B": {
                    "session_id": 26,
                    "fact": "The long indoor block allows only contract caterer-supplied edibles until the halfway refresh window; personal meal parcels are refused at the threshold.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-05-23T17:20:00Z",
            "query": "The all-day orientation block runs 8 to 12 with only viennoiserie at entry until the noon gate. Should I depend on that?",
            "gold": (
                "Do not depend on entry viennoiserie alone. Skipping a real first meal has caused a sharp mid-morning crash, "
                "and the contract limits you to host-controlled entry catering until the noon gate with no outside parcels. "
                "Eat substantial fuel beforehand or arrange permitted backup if the addendum allows it."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether entry viennoiserie alone is enough. Skipping a real first "
                "meal has caused a sharp mid-morning crash, but I cannot tell from the available memory whether tomorrow's "
                "block restricts you to host-controlled entry catering until the noon gate. Confirm the facility addendum before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know the facility addendum limits "
                    "intake to host-controlled entry catering until the noon gate, but the available memory does not establish that skipping "
                    "a first meal causes you a mid-morning crash. I cannot reject entry viennoiserie from contract rules alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether entry viennoiserie alone is enough. Skipping a real first "
                    "meal has caused a sharp mid-morning crash, but I cannot tell from the available memory whether tomorrow's "
                    "block restricts you to host-controlled entry catering until the noon gate. Confirm the facility addendum before deciding."
                ),
            },
            "required": [
                "cites skip-breakfast mid-morning crash pattern",
                "cites host-controlled entry catering constraint until the noon gate",
                "recommends substantial fuel beyond entry viennoiserie or eating beforehand",
            ],
            "absence_required": [
                "states that facility catering constraints are missing",
                "does not infer host-only entry catering",
                "asks about the addendum or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the skip-breakfast crash evidence is missing",
                    "does not infer mid-morning crash from block length alone",
                    "explicitly abstains from rejecting entry viennoiserie",
                ],
                "ev_B": [
                    "states that facility catering constraints are missing",
                    "does not infer host-only entry catering",
                    "asks about the addendum or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "midmorning_crash", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "pastry_only_until_lunch", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "pastry_table_insufficient_fuel",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "hypoglycemia diagnosis",
                "must never skip breakfast",
                "pastry workshop forbidden",
            ],
            "distractor": {
                "timestamp": "2026-05-21T11:45:00Z",
                "user": f"The organizers said entry viennoiserie is amazing and that depending on it for the full 8-to-12 orientation block is totally fine.",
                "assistant": "Event catering spin is common. How do host-only entry spreads actually go for you?",
                "why": "Organizer praise for entry viennoiserie shares query vocabulary but provides no bodily evidence about this user's crash pattern.",
            },
            "evolving": {
                "morning_fuel": "protein_dependent",
                "sugar_only_crash": True,
            },
        },
        "S5": {
            "name": "late_chili_reflux_x_morning_video_debrief",
            "prefix_end": 32,
            "evidence": {
                "ev_A": {
                    "session_id": 29,
                    "fact": "Chili-heavy dinners within about two hours of bedtime trigger night reflux for the user; earlier spicy meals have been tolerated.",
                },
                "ev_B": {
                    "session_id": 30,
                    "fact": "After reflux nights the user's voice wavers on morning video sessions they lead.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-02T19:30:00Z",
            "query": "There is a 9pm chili tasting tonight and I lead a 7:30am video debrief tomorrow. Should I go to the tasting?",
            "gold": (
                "Skip the late chili tasting, or choose a mild early dinner instead. Chili-heavy meals close to bedtime have "
                "triggered night reflux, and reflux nights have made your morning video voice waver when you lead sessions. "
                "Protect the debrief with a calmer evening plate."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the chili tasting threatens tomorrow's debrief. Late spicy "
                "meals have triggered night reflux, but I cannot tell from the available memory whether reflux nights impair "
                "your morning video voice. Confirm how late meals affect your speaking days before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know you lead a 7:30am video debrief "
                    "tomorrow, but the available memory does not establish that late chili triggers reflux for you. I cannot "
                    "reject the tasting from schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the chili tasting threatens tomorrow's debrief. Late spicy "
                    "meals have triggered night reflux, but I cannot tell from the available memory whether reflux nights impair "
                    "your morning video voice. Confirm how late meals affect your speaking days before deciding."
                ),
            },
            "required": [
                "cites late chili within ~2h of bedtime reflux pattern",
                "cites morning video voice wavering after reflux nights",
                "recommends skipping late spicy tasting or choosing milder earlier dinner",
            ],
            "absence_required": [
                "states that morning voice consequence is missing",
                "does not infer debrief failure from reflux alone",
                "asks about speaking-day effects or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-chili reflux evidence is missing",
                    "does not infer reflux from tasting invite alone",
                    "explicitly abstains from rejecting the tasting",
                ],
                "ev_B": [
                    "states that morning voice consequence is missing",
                    "does not infer debrief failure from reflux alone",
                    "asks about speaking-day effects or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "night_reflux", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "morning_voice_impairment", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "late_chili_threatens_morning_debrief",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "GERD diagnosis",
                "spicy food ban",
                "must cancel the call",
            ],
            "distractor": {
                "timestamp": "2026-06-01T14:00:00Z",
                "user": f"{ca} said the 9pm chili tasting menu is amazing and that booking it before an early call is worth it for the experience.",
                "assistant": "Experience marketing is persuasive. How do late chili-heavy plates affect your next morning?",
                "why": "A third party's endorsement of the same tasting is query-relevant but provides no evidence about this user's reflux or morning voice pattern.",
            },
            "evolving": {
                "night_reflux_trigger": "spicy_late",
                "early_voice_quality": "fragile",
            },
        },
        "S6": {
            "name": "late_espresso_x_early_cycle_class",
            "prefix_end": 38,
            "evidence": {
                "ev_A": {
                    "session_id": 34,
                    "fact": "A strong roast after the workday ends leaves the user waking twice overnight; morning caffeine before midday has not caused this.",
                },
                "ev_B": {
                    "session_id": 36,
                    "fact": "After fragmented sleep the user gets lightheaded in the before-breakfast studio class and stopped booking the dawn slot when sleep was bad.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-15T17:10:00Z",
            "query": "The cafe across the street is pushing a post-four double espresso. I locked the dawn spin slot tomorrow — should I grab one now?",
            "gold": (
                "Skip the post-four double espresso. An after-work strong cup has left you waking twice overnight, and after "
                "fragmented sleep you get lightheaded in the before-breakfast studio class. Choose a non-caffeinated drink or move "
                "the spin slot to a day with protected sleep."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Late espresso has fragmented your "
                "sleep twice, but I cannot tell from the available memory whether tomorrow's cycle class is sensitive "
                "to that pattern. Confirm how you tolerate early classes after a chopped-up night before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know early cycle classes "
                    "have felt unsafe after bad sleep, but the available memory does not establish that post-four "
                    "espresso disrupts your nights. I cannot reject the drink from class timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Late espresso has fragmented "
                    "your sleep twice, but I cannot tell from the available memory whether tomorrow's cycle class is "
                    "sensitive to that pattern. Confirm how you tolerate early classes after a chopped-up night before deciding."
                ),
            },
            "required": [
                "links post-four espresso to fragmented overnight sleep",
                "links fragmented sleep to lightheadedness in the 6:30 cycle class",
                "recommends skipping the espresso or rescheduling the class",
            ],
            "absence_required": [
                "states that the class-after-bad-sleep consequence is missing",
                "does not infer lightheadedness from booking the class alone",
                "explicitly abstains or asks about early-class tolerance after poor sleep",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-espresso sleep evidence is missing",
                    "does not infer sleep harm from the invite alone",
                    "explicitly abstains from rejecting the espresso",
                ],
                "ev_B": [
                    "states that the class-after-bad-sleep consequence is missing",
                    "does not infer lightheadedness from booking the class alone",
                    "explicitly abstains or asks about early-class tolerance after poor sleep",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "fragmented_overnight_sleep", "hop": 1},
                {"source": "ev_B", "relation": "conditional_on", "target": "early_cycle_lightheadedness", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "late_espresso_threatens_early_cycle",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "all caffeine is unsafe",
                "must cancel the cycle class",
                "espresso always ruins sleep",
            ],
            "distractor": {
                "timestamp": "2026-06-12T09:15:00Z",
                "user": f"{ca} said a post-four double espresso before her dawn spin slot always feels fine and that I should grab one from the cafe across the street without overthinking it.",
                "assistant": "That describes her experience, not yours.",
                "why": "A third party's identical post-four espresso and dawn spin routine is query-similar but not evidence about this user's sleep fragmentation or studio-class lightheadedness pattern.",
            },
            "evolving": {
                "late_espresso_effect": "fragmented_sleep_after_4pm",
                "early_cycle_tolerance": "poor_after_bad_sleep",
            },
        },
        "S7": {
            "name": "late_fiber_dinner_x_fitted_pitch",
            "prefix_end": 44,
            "evidence": {
                "ev_A": {
                    "session_id": 40,
                    "fact": "Dense pulse-heavy plates near bedtime leave the user bloated overnight; midday portions of similar food have been fine.",
                },
                "ev_B": {
                    "session_id": 42,
                    "fact": "On uncomfortable mornings formal client pitches feel distracting and reduce the user's presence.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-06-26T18:20:00Z",
            "query": "Group meal tomorrow evening starts late with a bean-forward chef's table. I pitch to a client in structured jacket at nine — should I eat the full spread?",
            "gold": (
                "Do not treat the full bean-forward spread as a free pass. Late plant-protein dinners have left you bloated "
                "overnight, and bloated mornings make structured jacket pitches distracting. Join socially "
                "but choose a lighter plate or eat earlier if you can."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether tomorrow's menu fits you. Late bean-heavy dinners have "
                "caused overnight bloating, but I cannot tell from the available memory whether your nine o'clock pitch "
                "requires fitted attire that would be affected. Confirm clothing and comfort needs before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know fitted-blazer pitches feel "
                    "distracting on bloated mornings, but the available memory does not establish that late legume-heavy "
                    "dinners cause you overnight bloating. I cannot reject the menu from presentation needs alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether tomorrow's menu fits you. Late bean-heavy dinners "
                    "have caused overnight bloating, but I cannot tell from the available memory whether your nine "
                    "o'clock pitch requires fitted attire that would be affected. Confirm clothing and comfort needs before deciding."
                ),
            },
            "required": [
                "uses the after-8pm condition on legume-heavy dinners",
                "uses bloated-morning discomfort in fitted-blazer pitches",
                "recommends a lighter plate or earlier eating",
            ],
            "absence_required": [
                "states that the pitch-attire consequence is missing",
                "does not infer bloating from the invite alone",
                "asks about clothing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-fiber bloating evidence is missing",
                    "does not infer overnight bloating from the menu description alone",
                    "explicitly abstains from rejecting the dinner",
                ],
                "ev_B": [
                    "states that the pitch-attire consequence is missing",
                    "does not infer bloating from the invite alone",
                    "asks about clothing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "conditional_on", "target": "late_legume_bloating", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "pitch_presence_cost", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "late_dinner_threatens_morning_pitch",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "all legumes are unsafe",
                "must skip the dinner",
                "the pitch will definitely fail",
            ],
            "distractor": {
                "timestamp": "2026-06-23T11:00:00Z",
                "user": f"{cb} said the bean-forward group meal before her morning pitch in structured jacket was amazing and that eating the full chef's table spread is how you stay in the group.",
                "assistant": "Social pressure around set menus is real.",
                "why": "A third party's endorsement of the same late bean-forward dinner is query-relevant but not evidence about this user's late-fiber bloating or pitch comfort.",
            },
            "evolving": {
                "late_legume_effect": "overnight_bloating_after_8pm",
                "fitted_pitch_comfort": "reduced_when_bloated",
            },
        },
        "S8": {
            "name": "fasted_labs_x_post_draw_lunch",
            "prefix_end": 49,
            "evidence": {
                "ev_A": {
                    "session_id": 45,
                    "fact": "Periodic bloodwork requires nothing by mouth until collection completes, usually early afternoon.",
                },
                "ev_B": {
                    "session_id": 47,
                    "fact": "Deferring refueling until a late mid-day meal after collection collapses the afternoon cognition window and details slip.",
                },
            },
            "withheld_in_absence": "ev_A",
            "query_timestamp": "2026-07-05T16:30:00Z",
            "query": "Someone pinned a hospitality meal right after my panel appointment. Dense post-lunch work blocks follow — should I arrive unfed or hold off?",
            "gold": (
                "Do not stay unfed through the afternoon. Your panel requires no intake until collection finishes around midday, and waiting until "
                "a late mid-day meal has collapsed dense post-lunch work blocks before. Join promptly after collection and eat, "
                "or reschedule the hospitality meal earlier if clinic timing slips."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Waiting until a late lunch has "
                "collapsed your afternoon review blocks, but I cannot tell from the available memory whether tomorrow's "
                "draw requires fasting until noon. Confirm the lab fasting window before deciding whether 12:30 is safe."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. Waiting until a late lunch has "
                    "collapsed your afternoon review blocks, but I cannot tell from the available memory whether tomorrow's "
                    "draw requires fasting until noon. Confirm the lab fasting window before deciding whether 12:30 is safe."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. I know the draw requires fasting "
                    "until about noon, but the available memory does not establish that staying empty afterward impairs "
                    "your afternoon reviews. I cannot reject the lunch timing from fasting rules alone."
                ),
            },
            "required": [
                "uses the fasting-until-noon draw requirement",
                "uses the post-draw empty-until-late-lunch afternoon collapse",
                "recommends eating promptly after the draw at 12:30 or adjusting timing",
            ],
            "absence_required": [
                "states that the fasting requirement is missing",
                "does not infer fasting until noon from the lunch invite alone",
                "explicitly abstains or asks about the draw window",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the fasting requirement is missing",
                    "does not infer fasting until noon from the lunch invite alone",
                    "explicitly abstains or asks about the draw window",
                ],
                "ev_B": [
                    "states that the afternoon-collapse evidence is missing",
                    "does not infer review failure from fasting alone",
                    "explicitly abstains from the lunch recommendation",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "fasted_until_noon_draw", "hop": 1},
                {"source": "ev_B", "relation": "causes", "target": "afternoon_review_collapse", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "post_draw_lunch_timing_matters",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "must skip lunch entirely",
                "labs never require fasting",
                "afternoon reviews always fail",
            ],
            "distractor": {
                "timestamp": "2026-07-02T14:30:00Z",
                "user": f"{ca} always waits until mid-afternoon after her panel appointment and says dense post-lunch work blocks are fine when she arrives unfed.",
                "assistant": "Her post-collection timing may differ from yours.",
                "why": "Another person's post-panel meal timing before dense post-lunch work blocks is query-similar but not evidence about this user's intake requirement or afternoon collapse pattern.",
            },
            "evolving": {
                "lab_fasting_window": "until_noon_draw",
                "post_draw_fuel": "needed_before_afternoon_reviews",
            },
        },
        "S9": {
            "name": "evening_alcohol_x_morning_protocol",
            "prefix_end": 54,
            "evidence": {
                "ev_A": {
                    "session_id": 50,
                    "fact": "Even two drinks at an evening reception disrupt the user's next-morning routine adherence.",
                },
                "ev_B": {
                    "session_id": 51,
                    "fact": "The user's dawn supplement sequence needs food at a consistent time; irregular mornings undo the benefit.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-12T20:45:00Z",
            "query": "Tonight's industry reception lists complimentary cocktails. I need a stable dawn food-and-supplement sequence tomorrow — should I stay for rounds?",
            "gold": (
                "Treat the complimentary cocktails cautiously. Even two drinks at evening receptions have disrupted your next-morning "
                "routine, and your dawn supplement sequence needs food at a consistent time — irregular mornings undo the "
                "benefit. Stay for networking with non-alcoholic options or leave before rounds start."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether drinks tonight fit tomorrow's plan. Even small amounts "
                "at mixers have disrupted your morning routine, but I cannot tell from the available memory whether "
                "tomorrow's supplement protocol requires a consistent food window. Confirm protocol timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know your supplement protocol "
                    "needs food at a consistent time, but the available memory does not establish that evening drinks "
                    "disrupt your next-morning routine. I cannot reject the bar from protocol rules alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether drinks tonight fit tomorrow's plan. Even small amounts "
                    "at mixers have disrupted your morning routine, but I cannot tell from the available memory whether "
                    "tomorrow's supplement protocol requires a consistent food window. Confirm protocol timing before deciding."
                ),
            },
            "required": [
                "links evening drinks to disrupted next-morning routine",
                "links the supplement protocol to consistent morning food timing",
                "recommends limiting or skipping alcohol tonight",
            ],
            "absence_required": [
                "states that the protocol food-timing requirement is missing",
                "does not infer protocol harm from the mixer invite alone",
                "asks about protocol timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the drink-to-routine evidence is missing",
                    "does not infer routine disruption from the open bar alone",
                    "explicitly abstains from rejecting drinks",
                ],
                "ev_B": [
                    "states that the protocol food-timing requirement is missing",
                    "does not infer protocol harm from the mixer invite alone",
                    "asks about protocol timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "morning_routine_disruption", "hop": 1},
                {"source": "ev_B", "relation": "requires", "target": "consistent_morning_food_window", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "drinks_threaten_morning_protocol",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "alcohol ban",
                "must skip the mixer",
                "supplements never work",
            ],
            "distractor": {
                "timestamp": "2026-07-11T15:00:00Z",
                "user": f"{cb} said the complimentary cocktails at industry receptions are essential networking and that staying for rounds before a dawn supplement sequence is worth it for your career.",
                "assistant": "Career folklore around receptions is loud.",
                "why": "Social pressure to drink at receptions is query-relevant but not evidence about this user's routine disruption or supplement timing needs.",
            },
            "evolving": {
                "evening_drink_effect": "morning_routine_slip",
                "supplement_protocol": "needs_consistent_morning_food",
            },
        },
        "S10": {
            "name": "desk_prep_portions_x_long_trail",
            "prefix_end": 59,
            "evidence": {
                "ev_A": {
                    "session_id": 55,
                    "fact": "Weekday staples hold desk blocks but the user empties out when output is high.",
                },
                "ev_B": {
                    "session_id": 57,
                    "fact": "The mapped route tomorrow is endurance-length with zero purchase points.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-21T06:50:00Z",
            "query": "Clear skies for the alpine circuit tomorrow. Will my usual sedentary-week staples cover the entire circuit?",
            "gold": (
                "Do not rely on sedentary-week staples alone. Weekday staples hold desk blocks but "
                "you empty out when output is high, and tomorrow's alpine circuit is endurance-length with zero purchase points. "
                "Pack denser fuel or add circuit-specific calories beyond your usual staples."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether standard prep containers are enough. Desk-day portions "
                "have left you under-fueled on active days, but I cannot tell from the available memory whether tomorrow's "
                "route length or resupply options change the requirement. Confirm trail duration and stops before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know tomorrow's trail is six "
                    "hours without resupply stops, but the available memory does not establish that your usual prep "
                    "containers under-fuel you on active days. I cannot reject standard portions from route length alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether standard prep containers are enough. Desk-day portions "
                    "have left you under-fueled on active days, but I cannot tell from the available memory whether tomorrow's "
                    "route length or resupply options change the requirement. Confirm trail duration and stops before deciding."
                ),
            },
            "required": [
                "uses desk-day prep portions versus active-day under-fueling",
                "uses the six-hour no-resupply trail constraint",
                "recommends denser or additional trail fuel beyond standard prep",
            ],
            "absence_required": [
                "states that the trail duration/resupply constraint is missing",
                "does not infer under-fueling from the weather alone",
                "asks about route length or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the active-day portion evidence is missing",
                    "does not infer under-fueling from trail planning alone",
                    "explicitly abstains from rejecting standard prep",
                ],
                "ev_B": [
                    "states that the trail duration/resupply constraint is missing",
                    "does not infer under-fueling from the weather alone",
                    "asks about route length or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "desk_prep_insufficient_on_active_days", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "six_hour_no_resupply_trail", "hop": 1},
                {
                    "source": ["ev_A", "ev_B"],
                    "relation": "co_activate_to",
                    "target": "standard_prep_unsafe_for_trail",
                    "hop": 2,
                },
            ],
            "forbidden": [
                "meal prep is always enough",
                "must cancel the hike",
                "all trails need the same fuel",
            ],
            "distractor": {
                "timestamp": "2026-07-19T18:30:00Z",
                "user": f"{ca} said packing light on the alpine circuit means relying on sedentary-week staples and that extra food for an endurance-length circuit is dead weight.",
                "assistant": "Ultralight advice is not universal.",
                "why": "Third-party alpine-circuit packing folklore about sedentary-week staples is query-relevant but not evidence about this user's high-output fueling or tomorrow's zero-purchase route.",
            },
            "evolving": {
                "prep_portion_mode": "desk_sufficient_active_insufficient",
                "trail_fuel_need": "six_hour_no_resupply",
            },
        },
        "S11": {
            "name": "cold_plunge_recovery_x_open_water_mile",
            "prefix_end": 65,
            "evidence": {
                "ev_A": {
                    "session_id": 61,
                    "fact": "Cold plunge after hard training days speeds the user's recovery; warm-pool-only weeks feel sluggish the next morning.",
                },
                "ev_B": {
                    "session_id": 63,
                    "fact": "Sports med advised avoiding overhead stroke loads for about four weeks while shoulder impingement settles.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-01T10:30:00Z",
            "query": "A teammate keeps nudging me toward the bay swim challenge next weekend — sensible given my current recovery setup?",
            "gold": (
                "Decline the bay swim challenge for now. Cold plunge after hard training days speeds your recovery, but "
                "sports med advised avoiding overhead stroke loads for about four weeks while shoulder impingement settles. "
                "The pool-lap social chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. Cold plunge has helped your recovery, "
                "but I cannot tell from the available memory whether overhead stroke loads are currently restricted. "
                "Confirm any sports-med guidance before joining a mile swim."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know overhead stroke loads are "
                    "restricted for about four weeks, but the available memory does not establish that cold plunge affects "
                    "your recovery pattern. I cannot reject the signup from shoulder guidance alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. Cold plunge has helped your recovery, "
                    "but I cannot tell from the available memory whether overhead stroke loads are currently restricted. "
                    "Confirm any sports-med guidance before joining a mile swim."
                ),
            },
            "required": [
                "links cold plunge to faster recovery after hard training",
                "links sports-med limit on overhead stroke loads",
                "recommends declining the bay swim challenge",
            ],
            "absence_required": [
                "states that the shoulder-load restriction is missing",
                "does not infer harm from the signup alone",
                "explicitly abstains or asks about sports-med guidance",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the cold-plunge recovery evidence is missing",
                    "does not infer swim harm from the invite alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the shoulder-load restriction is missing",
                    "does not infer harm from the signup alone",
                    "explicitly abstains or asks about sports-med guidance",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "cold_plunge_recovery", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "no_overhead_stroke_load", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "open_water_mile_poor_fit", "hop": 2},
            ],
            "forbidden": ["swim ban forever", "must never train", "skip all cardio"],
            "distractor": {
                "timestamp": "2026-07-29T09:15:00Z",
                "user": f"{ca} said the bay swim challenge next weekend is amazing hype and worth joining for summer fitness before any pool-heavy month.",
                "assistant": "A bay challenge is a different format from lap socials.",
                "why": "Bay swim challenge hype is query-similar FOMO but not evidence about this user's cold-plunge recovery or shoulder stroke-load limit.",
            },
            "evolving": {"cold_plunge": "recovery_boost", "shoulder_limit": "no_overhead_stroke_4wk"},
        },
        "S12": {
            "name": "probiotic_fasted_x_dawn_rounds",
            "prefix_end": 71,
            "evidence": {
                "ev_A": {
                    "session_id": 67,
                    "fact": "Refrigerated probiotic capsules on an empty stomach leave the user bloated by afternoon; with food they are fine.",
                },
                "ev_B": {
                    "session_id": 69,
                    "fact": "Tuesday hospital rounds start at six-thirty with no food until mid-morning.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-12T18:20:00Z",
            "query": "Thinking of adding the refrigerated probiotic to my dawn routine before next week's service block — good idea?",
            "gold": (
                "Do not add the refrigerated probiotic to your dawn routine before next week's service block on an empty stomach. Fasted "
                "probiotic capsules have left you bloated by afternoon, and Tuesday rounds start at six-thirty with no food "
                "until mid-morning. Begin with breakfast pairing or wait until after rounds week. The residency streak hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a probiotic streak fits rounds week. Fasted probiotic "
                "capsules have caused afternoon bloating, but I cannot tell from the available memory when Tuesday rounds "
                "start or whether food is available. Confirm the rounds schedule before starting."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Tuesday rounds start at "
                    "six-thirty without food until mid-morning, but the available memory does not establish that fasted "
                    "probiotics cause afternoon bloating. I cannot reject the streak from schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a probiotic streak fits rounds week. Fasted probiotic "
                    "capsules have caused afternoon bloating, but I cannot tell from the available memory when Tuesday rounds "
                    "start or whether food is available. Confirm the rounds schedule before starting."
                ),
            },
            "required": [
                "uses fasted probiotic afternoon bloating pattern",
                "uses six-thirty rounds with delayed food",
                "recommends against starting the streak before rounds week without food",
            ],
            "absence_required": [
                "states that the rounds food-timing evidence is missing",
                "does not infer bloating from the streak invite alone",
                "asks about rounds timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the fasted-probiotic bloating evidence is missing",
                    "does not infer stomach harm from the streak alone",
                    "explicitly abstains from rejecting the streak",
                ],
                "ev_B": [
                    "states that the rounds food-timing evidence is missing",
                    "does not infer bloating from the streak invite alone",
                    "asks about rounds timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "fasted_probiotic_bloat", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dawn_rounds_no_food", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "streak_before_rounds_risky", "hop": 2},
            ],
            "forbidden": ["probiotics always harmful", "must skip gut health", "rounds always unsafe"],
            "distractor": {
                "timestamp": "2026-08-09T11:00:00Z",
                "user": f"{cb} said adding a refrigerated probiotic to a dawn routine before next week's service block is amazing hype and worth it for gut resilience during service.",
                "assistant": "Residency streak hype is loud.",
                "why": "Probiotic dawn-routine hype shares service-block surface but is not evidence about this user's fasted bloating or dawn rounds food window.",
            },
            "evolving": {"probiotic_timing": "fasted_bloat_with_food_ok", "rounds_window": "six_thirty_no_food"},
        },
        "S13": {
            "name": "natural_wine_x_weekend_inlaw_hosting",
            "prefix_end": 76,
            "evidence": {
                "ev_A": {
                    "session_id": 72,
                    "fact": "Natural low-sulfite pours trigger flushing and poor sleep for the user; conventional wine in moderation has been fine.",
                },
                "ev_B": {
                    "session_id": 74,
                    "fact": "Hosting in-laws Saturday through Sunday needs clear-headed mornings for meal prep.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-19T09:15:00Z",
            "query": "Partner picked something from the guest-weekend case for the first seated course — workable given how those nights usually affect my next morning?",
            "gold": (
                "Skip the guest-weekend case at the first seated course. Natural low-sulfite pours have triggered flushing "
                "and poor sleep for you, and hosting in-laws through Sunday needs clear-headed mornings for meal prep. "
                "Serve conventional wine in moderation or a non-alcohol welcome instead."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether natural wine fits the welcome dinner. Natural pours have "
                "triggered poor sleep, but I cannot tell from the available memory whether weekend hosting requires "
                "clear-headed mornings. Confirm hosting duties before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know weekend hosting needs "
                    "clear-headed mornings, but the available memory does not establish that natural wine triggers poor "
                    "sleep for you. I cannot reject the case from hosting alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether natural wine fits the welcome dinner. Natural pours have "
                    "triggered poor sleep, but I cannot tell from the available memory whether weekend hosting requires "
                    "clear-headed mornings. Confirm hosting duties before deciding."
                ),
            },
            "required": [
                "uses natural low-sulfite wine sleep/flushing pattern",
                "uses weekend hosting needing clear morning prep",
                "recommends against opening the guest-weekend case at the first seated course",
            ],
            "absence_required": [
                "states that the hosting morning-prep requirement is missing",
                "does not infer sleep harm from the dinner plan alone",
                "asks about hosting duties or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the natural-wine sleep evidence is missing",
                    "does not infer hosting conflict from dinner alone",
                    "explicitly abstains from rejecting the case",
                ],
                "ev_B": [
                    "states that the hosting morning-prep requirement is missing",
                    "does not infer sleep harm from the dinner plan alone",
                    "asks about hosting duties or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "natural_wine_poor_sleep", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "hosting_clear_mornings", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "natural_wine_conflicts_hosting", "hop": 2},
            ],
            "forbidden": ["alcohol ban", "must cancel guests", "all wine unsafe"],
            "distractor": {
                "timestamp": "2026-08-17T14:00:00Z",
                "user": f"{ca} said opening the guest-weekend case at the first seated course while guests are visiting is amazing hype and worth it for a memorable weekend.",
                "assistant": "Memorable weekends and morning prep are different ledgers.",
                "why": "Low-sulfite welcome-spread hype shares hosting surface but is not evidence about this user's natural-wine sleep response or morning prep needs.",
            },
            "evolving": {"natural_wine": "poor_sleep_trigger", "weekend_hosting": "clear_morning_prep"},
        },
        "S14": {
            "name": "fiber_preworkout_x_dawn_interval",
            "prefix_end": 81,
            "evidence": {
                "ev_A": {
                    "session_id": 77,
                    "fact": "Fiber supplement before vigorous exercise causes mid-session cramping for the user; dinner timing is fine.",
                },
                "ev_B": {
                    "session_id": 79,
                    "fact": "Track club moved the user's interval block to dawn Thursday this month.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-27T06:50:00Z",
            "query": "Running-group friends swear by a powder blend tonight before tomorrow's early reps — one-off worth testing?",
            "gold": (
                "Skip the powder blend tonight before early reps. Fiber supplement before vigorous exercise has caused "
                "mid-session cramping, and your interval block moved to dawn Thursday this month. Take fiber with dinner on "
                "non-interval nights only. The club guarantee hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a fiber drink tonight fits dawn intervals. Pre-workout "
                "fiber has caused cramping, but I cannot tell from the available memory whether your interval block is now "
                "at dawn. Confirm session timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know intervals moved to dawn "
                    "Thursday, but the available memory does not establish that pre-workout fiber causes cramping. "
                    "I cannot reject the drink from schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a fiber drink tonight fits dawn intervals. Pre-workout "
                    "fiber has caused cramping, but I cannot tell from the available memory whether your interval block is now "
                    "at dawn. Confirm session timing before deciding."
                ),
            },
            "required": [
                "uses pre-workout fiber mid-session cramping",
                "uses dawn Thursday interval block",
                "recommends skipping powder blend before early reps",
            ],
            "absence_required": [
                "states that the dawn interval timing evidence is missing",
                "does not infer cramping from the club push alone",
                "asks about session timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the pre-workout fiber cramping evidence is missing",
                    "does not infer cramping from the guarantee alone",
                    "explicitly abstains from rejecting the drink",
                ],
                "ev_B": [
                    "states that the dawn interval timing evidence is missing",
                    "does not infer cramping from the club push alone",
                    "asks about session timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "preworkout_fiber_cramp", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dawn_thursday_interval", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "fiber_drink_before_dawn_interval_risky", "hop": 2},
            ],
            "forbidden": ["fiber always bad", "must skip track club", "exercise unsafe"],
            "distractor": {
                "timestamp": "2026-08-25T18:30:00Z",
                "user": f"{ca} said a powder blend tonight before tomorrow's early reps is worth testing before Thursday track week — everyone in the running group is pushing it.",
                "assistant": "Club guarantees are not stomach facts.",
                "why": "Soluble-fiber mix hype shares dawn-rep surface but is not evidence about this user's pre-workout cramping or Thursday dawn block.",
            },
            "evolving": {"fiber_timing": "preworkout_cramp", "interval_block": "dawn_thursday"},
        },
        "S15": {
            "name": "late_dessert_x_fasting_endocrine_checkin",
            "prefix_end": 86,
            "evidence": {
                "ev_A": {
                    "session_id": 82,
                    "fact": "Late refined-dessert evenings bump the user's dawn glucose reading above their personal target.",
                },
                "ev_B": {
                    "session_id": 84,
                    "fact": "Endocrinologist check-in Thursday at seven-thirty implies fasting labs.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-09-04T20:45:00Z",
            "query": "Guild wants me at a late plated course midweek — okay with the morning panel already on my calendar?",
            "gold": (
                "Skip the late plated course midweek. Late refined-dessert evenings have bumped your dawn glucose "
                "above your personal target, and endocrinologist check-in Thursday at seven-thirty implies fasting labs. "
                "Choose a lighter evening or move social plans before the lab window."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the dessert preview fits Thursday's check-in. Late "
                "dessert evenings have raised dawn glucose, but I cannot tell from the available memory whether Thursday "
                "requires fasting labs. Confirm check-in timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Thursday check-in at "
                    "seven-thirty implies fasting labs, but the available memory does not establish that late dessert "
                    "raises your dawn glucose. I cannot reject the preview from lab timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the dessert preview fits Thursday's check-in. Late "
                    "dessert evenings have raised dawn glucose, but I cannot tell from the available memory whether Thursday "
                    "requires fasting labs. Confirm check-in timing before deciding."
                ),
            },
            "required": [
                "uses late refined dessert raising dawn glucose",
                "uses Thursday seven-thirty fasting check-in",
                "recommends skipping late plated course midweek",
            ],
            "absence_required": [
                "states that the fasting-lab timing evidence is missing",
                "does not infer glucose harm from the preview alone",
                "asks about check-in timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the late-dessert glucose evidence is missing",
                    "does not infer lab conflict from preview alone",
                    "explicitly abstains from rejecting the preview",
                ],
                "ev_B": [
                    "states that the fasting-lab timing evidence is missing",
                    "does not infer glucose harm from the preview alone",
                    "asks about check-in timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "late_dessert_dawn_glucose_spike", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "thursday_fasting_labs", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "preview_conflicts_fasting_checkin", "hop": 2},
            ],
            "forbidden": ["glucose ban forever", "must cancel check-in", "dessert always unsafe"],
            "distractor": {
                "timestamp": "2026-09-02T15:00:00Z",
                "user": f"{cb} said a late plated course midweek before the morning panel is amazing hype and worth it for the social experience.",
                "assistant": "Social experience and fasting labs are different decisions.",
                "why": "Chef's-table sweet-course hype shares Wednesday-before-Thursday surface but is not evidence about this user's dawn glucose response or fasting check-in.",
            },
            "evolving": {"late_dessert": "dawn_glucose_spike", "endocrine_checkin": "thursday_fasting_labs"},
        },
        "S16": {
            "name": "oil_kitchen_lunch_x_corridor_vitals_block",
            "prefix_end": 91,
            "evidence": {
                "ev_A": {
                    "session_id": 88,
                    "fact": "Oil-kitchen lunches leave the user sluggish with elevated post-walk glucose; grilled options have been fine.",
                },
                "ev_B": {
                    "session_id": 90,
                    "fact": "Wednesday corridor vitals block needs stable post-meal readings.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-10T10:15:00Z",
            "query": "Worth trying the cafeteria signup line before Wednesday's corridor check?",
            "gold": (
                "Skip the oil-kitchen lunch roster before Wednesday's corridor vitals block. Oil-kitchen lunches have left "
                "you sluggish with elevated post-walk glucose, and Wednesday corridor vitals block needs stable post-meal "
                "readings. Choose grilled options or defer fryer-heavy lunches until after the vitals block. The cafeteria "
                "signup blurb chatter is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether the oil-kitchen lunch roster fits before Wednesday's corridor "
                "vitals block. Fryer-heavy lunches have raised post-walk glucose, but I cannot tell from the available memory "
                "whether Wednesday vitals need stable post-meal readings. Confirm vitals timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Wednesday corridor vitals block "
                    "needs stable post-meal readings, but the available memory does not establish that oil-kitchen lunches raise "
                    "your post-walk glucose. I cannot reject the roster from calendar alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether the oil-kitchen lunch roster fits before Wednesday's corridor "
                    "vitals block. Fryer-heavy lunches have raised post-walk glucose, but I cannot tell from the available memory "
                    "whether Wednesday vitals need stable post-meal readings. Confirm vitals timing before deciding."
                ),
            },
            "required": [
                "uses oil-kitchen lunches raising post-walk glucose",
                "uses Wednesday corridor vitals needing stable post-meal readings",
                "recommends skipping oil-kitchen lunch roster before vitals block",
            ],
            "absence_required": [
                "states that the corridor-vitals timing evidence is missing",
                "does not infer glucose harm from the roster invite alone",
                "asks about vitals timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the oil-kitchen glucose evidence is missing",
                    "does not infer vitals harm from the roster alone",
                    "explicitly abstains from rejecting the roster",
                ],
                "ev_B": [
                    "states that the corridor-vitals timing evidence is missing",
                    "does not infer glucose harm from the roster invite alone",
                    "asks about vitals timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "oil_kitchen_glucose_spike", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "wednesday_vitals_stable_readings", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "fryer_lunch_conflicts_vitals", "hop": 2},
            ],
            "forbidden": ["fried food ban forever", "must skip all cafeteria meals", "vitals always unsafe"],
            "distractor": {
                "timestamp": "2026-06-05T11:00:00Z",
                "user": f"{ca} said the cafeteria signup line before Wednesday's corridor check is amazing hype and worth joining for cafeteria variety.",
                "assistant": "Variety hype and vitals readings are different ledgers.",
                "why": "Oil-kitchen roster hype shares vitals-block surface but is not evidence about this user's post-walk glucose pattern or stable post-meal reading need.",
            },
            "evolving": {"oil_kitchen": "post_walk_glucose_spike", "corridor_vitals": "wednesday_stable_readings"},
        },
        "S17": {
            "name": "fizz_zero_cal_x_scope_prep_window",
            "prefix_end": 96,
            "evidence": {
                "ev_A": {
                    "session_id": 93,
                    "fact": "Fizz-heavy zero-cal drinks cause bloating on sensitive gut evenings; still water has been fine.",
                },
                "ev_B": {
                    "session_id": 95,
                    "fact": "Friday scope prep window requires clear liquids with minimal bloating Wednesday night.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-18T17:30:00Z",
            "query": "Hall immersion week before Friday's packet filing cutoff — workable?",
            "gold": (
                "Skip the fizz-heavy zero-cal roster before Friday's scope prep window. Fizz-heavy zero-cal drinks have caused "
                "bloating on sensitive gut evenings, and Friday scope prep window requires clear liquids with minimal bloating "
                "Wednesday night. Use still water or defer carbonated options until after prep week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a fizz-heavy zero-cal roster fits Friday's scope prep window. "
                "Carbonated evenings have caused bloating, but I cannot tell from the available memory whether Wednesday night "
                "requires clear liquids with minimal bloating. Confirm prep timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Friday scope prep window requires "
                    "clear liquids with minimal bloating Wednesday night, but the available memory does not establish that fizz-heavy "
                    "zero-cal drinks cause bloating for you. I cannot reject the roster from prep timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a fizz-heavy zero-cal roster fits Friday's scope prep window. "
                    "Carbonated evenings have caused bloating, but I cannot tell from the available memory whether Wednesday night "
                    "requires clear liquids with minimal bloating. Confirm prep timing before deciding."
                ),
            },
            "required": [
                "uses fizz-heavy zero-cal drinks causing bloating",
                "uses Friday scope prep requiring clear liquids Wednesday night",
                "recommends against fizz-heavy zero-cal roster before scope prep",
            ],
            "absence_required": [
                "states that the scope-prep clear-liquid evidence is missing",
                "does not infer bloating harm from the roster invite alone",
                "asks about prep timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the fizz-bloating evidence is missing",
                    "does not infer prep harm from the roster alone",
                    "explicitly abstains from rejecting the roster",
                ],
                "ev_B": [
                    "states that the scope-prep clear-liquid evidence is missing",
                    "does not infer bloating harm from the roster invite alone",
                    "asks about prep timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "fizz_zero_cal_bloating", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "scope_prep_clear_liquids", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "fizz_roster_conflicts_scope_prep", "hop": 2},
            ],
            "forbidden": ["carbonation ban forever", "must skip all clinic prep", "scope prep always unsafe"],
            "distractor": {
                "timestamp": "2026-06-08T14:00:00Z",
                "user": f"{cb} said a hall immersion week before Friday's packet filing cutoff is amazing hype and worth it for clinic community bonding.",
                "assistant": "Community bonding and prep-window bloating are different ledgers.",
                "why": "Fizz roster hype shares scope-prep surface but is not evidence about this user's carbonated bloating pattern or clear-liquid prep requirement.",
            },
            "evolving": {"fizz_zero_cal": "evening_bloating", "scope_prep": "friday_clear_liquids_wed_night"},
        },
        "S18": {
            "name": "crunch_bowl_evening_x_dawn_panel_draw",
            "prefix_end": 101,
            "evidence": {
                "ev_A": {
                    "session_id": 98,
                    "fact": "Large crunch-bowl evenings cause bloating before dawn blood draws; cooked veg portions have been fine.",
                },
                "ev_B": {
                    "session_id": 100,
                    "fact": "Thursday dawn panel draw needs a settled morning stomach; late-slot food signup runs through the night before.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-07-28T11:40:00Z",
            "query": "Caterer added a dusk-to-morning signup before Thursday's lab lock — sensible?",
            "gold": (
                "Skip the crunch-bowl signup before Thursday's dawn panel draw. Large crunch-bowl evenings have caused bloating "
                "before dawn blood draws, and Thursday dawn panel draw needs a settled morning stomach while a late-slot food "
                "signup is already booked through the night before. Choose cooked veg portions or defer raw-heavy bowls until "
                "after draw week."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a crunch-bowl signup fits Thursday's dawn panel draw. "
                "Raw-heavy evenings have caused pre-draw bloating, but I cannot tell from the available memory whether Thursday "
                "dawn draw needs a settled morning stomach. Confirm draw timing before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know Thursday dawn panel draw needs a "
                    "settled morning stomach while a late-slot food signup runs through the night before, but the available memory "
                    "does not establish that crunch-bowl evenings cause pre-draw bloating. I cannot reject the signup from draw "
                    "timing alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a crunch-bowl signup fits Thursday's dawn panel draw. "
                    "Raw-heavy evenings have caused pre-draw bloating, but I cannot tell from the available memory whether Thursday "
                    "dawn draw needs a settled morning stomach. Confirm draw timing before deciding."
                ),
            },
            "required": [
                "uses crunch-bowl evenings causing pre-draw bloating",
                "uses Thursday dawn panel draw needing settled morning stomach",
                "recommends against crunch-bowl signup before dawn draw",
            ],
            "absence_required": [
                "states that the dawn-draw stomach-settling evidence is missing",
                "does not infer draw harm from the signup invite alone",
                "asks about draw timing or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the crunch-bowl bloating evidence is missing",
                    "does not infer draw harm from the signup alone",
                    "explicitly abstains from rejecting the signup",
                ],
                "ev_B": [
                    "states that the dawn-draw stomach-settling evidence is missing",
                    "does not infer draw harm from the signup invite alone",
                    "asks about draw timing or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "crunch_bowl_predraw_bloating", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "dawn_draw_settled_stomach", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "crunch_signup_conflicts_draw", "hop": 2},
            ],
            "forbidden": ["raw veg ban forever", "must skip all lab draws", "salad always unsafe"],
            "distractor": {
                "timestamp": "2026-06-15T16:30:00Z",
                "user": f"{ca} said a dusk-to-morning signup before Thursday's lab lock is amazing hype and worth it for caterer community bonding.",
                "assistant": "Community bonding and dawn-draw comfort are different ledgers.",
                "why": "Crunch-bowl signup hype shares dawn-draw surface but is not evidence about this user's pre-draw bloating pattern or settled-morning requirement.",
            },
            "evolving": {"crunch_bowl": "predraw_bloating", "dawn_panel_draw": "settled_morning_stomach"},
        },
        "S19": {
            "name": "whole_food_prep_x_blender_demo_night",
            "prefix_end": 106,
            "evidence": {
                "ev_A": {
                    "session_id": 103,
                    "fact": "The user retains portioning skills best with whole-food prep; blender-only practice weakens demo performance.",
                },
                "ev_B": {
                    "session_id": 105,
                    "fact": "A prior blender-only rehearsal went poorly before skills demo night.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-07T16:20:00Z",
            "query": "Culinary school wants me on the countertop-appliance run-through for next week's evaluation night — good fit?",
            "gold": (
                "Decline or renegotiate to a whole-food prep role. You retain portioning skills best with whole-food prep and a "
                "prior blender-only rehearsal went poorly before skills demo night. Offer a knife-and-plate practice session or "
                "prepared whole-food mockup instead. The culinary forum hype is unrelated."
            ),
            "absence_gold": (
                "There is insufficient evidence to decide whether a blender-only run-through fits next week's skills demo. "
                "Whole-food prep has produced your strongest portioning performance, but I cannot tell from the available memory "
                "whether a prior blender-only rehearsal failed. Confirm your blender-only track record before volunteering."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know a prior blender-only rehearsal went "
                    "poorly, but the available memory does not establish that whole-food prep is your strongest portioning format. "
                    "I cannot reject the run-through from one bad session alone."
                ),
                "ev_B": (
                    "There is insufficient evidence to decide whether a blender-only run-through fits next week's skills demo. "
                    "Whole-food prep has produced your strongest portioning performance, but I cannot tell from the available memory "
                    "whether a prior blender-only rehearsal failed. Confirm your blender-only track record before volunteering."
                ),
            },
            "required": [
                "uses whole-food prep as strongest portioning format",
                "uses prior blender-only rehearsal failure",
                "recommends declining or shifting away from blender-only run-through",
            ],
            "absence_required": [
                "states that the blender-only rehearsal failure evidence is missing",
                "does not infer format mismatch from the invite alone",
                "asks about blender-only track record or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the whole-food prep evidence is missing",
                    "does not infer demo harm from the run-through alone",
                    "explicitly abstains from rejecting the run-through",
                ],
                "ev_B": [
                    "states that the blender-only rehearsal failure evidence is missing",
                    "does not infer format mismatch from the invite alone",
                    "asks about blender-only track record or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "indicates", "target": "whole_food_portioning_strength", "hop": 1},
                {"source": "ev_B", "relation": "indicates", "target": "blender_only_rehearsal_fail", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "blender_runthrough_poor_fit", "hop": 2},
            ],
            "forbidden": ["blender ban", "must skip skills demo", "culinary prep always unsafe"],
            "distractor": {
                "timestamp": "2026-06-20T18:00:00Z",
                "user": f"{ca} said the countertop-appliance run-through for next week's evaluation night is amazing hype and everyone in the culinary forum is pushing it.",
                "assistant": "Forum defaults are not prep facts.",
                "why": "Blender-only run-through hype shares skills-demo surface but is not evidence about this user's whole-food portioning strength or prior blender-only rehearsal failure.",
            },
            "evolving": {"prep_format": "whole_food_portioning_strength", "skills_demo": "blender_only_rehearsal_failed"},
        },
        "S20": {
            "name": "no_snack_transfer_x_stacked_telehealth_week",
            "prefix_end": 111,
            "evidence": {
                "ev_A": {
                    "session_id": 108,
                    "fact": "Corridor transfers without snacks leave the user shaky and foggy; light bar transfers have been fine.",
                },
                "ev_B": {
                    "session_id": 110,
                    "fact": "Stacked telehealth week requires steady afternoon cognition with no scheduled meal gap.",
                },
            },
            "withheld_in_absence": "ev_B",
            "query_timestamp": "2026-08-17T18:10:00Z",
            "query": "Worth accepting the heavier no-fuel corridor block this week — based on what you know about me?",
            "gold": (
                "Lean no unless snacks are built into transfers. Corridor transfers without snacks have left you shaky and "
                "foggy, and stacked telehealth week requires steady afternoon cognition with no scheduled meal gap. Carry a "
                "light bar or defer no-fuel blocks until after telehealth week."
            ),
            "absence_gold": (
                "There is insufficient evidence for a personalized recommendation. No-snack transfers have caused shakiness, "
                "but I cannot tell from the available memory whether stacked telehealth week requires steady afternoon cognition "
                "with no meal gap. Confirm telehealth-week schedule before deciding."
            ),
            "absence_gold_by_missing": {
                "ev_A": (
                    "There is insufficient evidence for a personalized recommendation. I know stacked telehealth week requires "
                    "steady afternoon cognition with no scheduled meal gap, but the available memory does not establish that "
                    "corridor transfers without snacks leave you shaky and foggy. I cannot reject the block from schedule alone."
                ),
                "ev_B": (
                    "There is insufficient evidence for a personalized recommendation. No-snack transfers have caused shakiness, "
                    "but I cannot tell from the available memory whether stacked telehealth week requires steady afternoon cognition "
                    "with no meal gap. Confirm telehealth-week schedule before deciding."
                ),
            },
            "required": [
                "uses no-snack corridor transfers causing shakiness and fog",
                "uses stacked telehealth week requiring steady afternoon cognition",
                "recommends declining or adding snacks to no-fuel corridor block",
            ],
            "absence_required": [
                "states that the telehealth-week cognition-gap evidence is missing",
                "does not infer focus harm from the block invite alone",
                "asks about telehealth-week schedule or explicitly abstains",
            ],
            "absence_required_by_missing": {
                "ev_A": [
                    "states that the no-snack transfer shakiness evidence is missing",
                    "does not infer cognition harm from the block alone",
                    "explicitly abstains from rejecting the block",
                ],
                "ev_B": [
                    "states that the telehealth-week cognition-gap evidence is missing",
                    "does not infer focus harm from the block invite alone",
                    "asks about telehealth-week schedule or explicitly abstains",
                ],
            },
            "links": [
                {"source": "ev_A", "relation": "causes", "target": "no_snack_transfer_shakiness", "hop": 1},
                {"source": "ev_B", "relation": "constrains", "target": "telehealth_steady_afternoon_cognition", "hop": 1},
                {"source": ["ev_A", "ev_B"], "relation": "co_activate_to", "target": "no_fuel_block_conflicts_telehealth", "hop": 2},
            ],
            "forbidden": ["snacking ban forever", "must cancel telehealth", "transfers always unsafe"],
            "distractor": {
                "timestamp": "2026-06-25T09:30:00Z",
                "user": f"{cb} said accepting the heavier no-fuel corridor block this week is amazing hype and worth it for clinic efficiency.",
                "assistant": "Efficiency hype and afternoon cognition are different ledgers.",
                "why": "No-fuel corridor block hype is query-similar FOMO but is not evidence about this user's no-snack shakiness pattern or telehealth-week cognition requirement.",
            },
            "evolving": {"no_snack_transfer": "shaky_and_foggy", "telehealth_week": "steady_afternoon_cognition"},
        },
    }


def parse_scenario_ids(raw: str) -> tuple[str, ...]:
    raw = raw.strip().upper()
    if raw in {"ALL", "S1-S10", "1-10"}:
        return tuple(f"S{i}" for i in range(1, 11))
    if raw in {"S1-S5", "1-5", "LEGACY"}:
        return ("S1", "S2", "S3", "S4", "S5")
    if raw in {"S6-S10", "6-10", "NEW"}:
        return ("S6", "S7", "S8", "S9", "S10")
    if raw in {"S11-S15", "11-15", "ULTRA"}:
        return ("S11", "S12", "S13", "S14", "S15")
    if raw in {"S16-S20", "16-20"}:
        return ("S16", "S17", "S18", "S19", "S20")
    if raw in {"S1-S15", "1-15"}:
        return tuple(f"S{i}" for i in range(1, 16))
    if raw in {"S11-S20", "11-20"}:
        return tuple(f"S{i}" for i in range(11, 21))
    if raw in {"S1-S20", "1-20"}:
        return tuple(f"S{i}" for i in range(1, 21))
    if "," in raw:
        return tuple(part.strip() for part in raw.split(",") if part.strip())
    return (raw,)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Generate health/diet gold batch JSON items.")
    parser.add_argument(
        "--scenarios",
        default="S11-S15",
        help="Which scenarios to write: S16-S20, S11-S15, S1-S5, S6-S10, S1-S20, ALL",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="Optional minimum automated score to write files (default 0 = hard-gate only, v2 standard)",
    )
    args = parser.parse_args(argv)
    scenario_ids = parse_scenario_ids(args.scenarios)
    min_score = args.min_score

    personas_data = json.loads(PERSONAS_PATH.read_text(encoding="utf-8"))
    personas = personas_data["users"]
    arms = ("associative", "distractor", "absence")

    timelines: dict[int, list[dict[str, Any]]] = {}
    scenarios_by_user: dict[int, dict[str, Any]] = {}
    for persona in personas:
        idx = persona["user_index"]
        timelines[idx] = build_timeline(persona)
        scenarios_by_user[idx] = build_scenarios(persona)

    items: list[dict[str, Any]] = []
    report_items: list[dict[str, Any]] = []
    failures = 0
    score_totals: list[int] = []

    for persona in personas:
        idx = persona["user_index"]
        timeline = timelines[idx]
        scenarios = scenarios_by_user[idx]
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
                )
                errors = hard_gate_errors(
                    item, timeline, scenarios, computed_by=COMPUTED_BY
                )
                scores = score_item(item, errors)
                score_totals.append(scores["total"])
                path = output_path(ROOT, persona, item)
                gate_pass = not errors
                score_pass = scores["total"] >= min_score
                write_pass = gate_pass and (min_score <= 0 or score_pass)

                if write_pass:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(
                        json.dumps(item, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                else:
                    failures += 1

                items.append(item)
                report_items.append(
                    {
                        "sample_id": item["sample_id"],
                        "path": str(path.relative_to(ROOT)),
                        "user_index": idx,
                        "scenario_id": sid,
                        "arm": arm,
                        "hard_gate_pass": gate_pass,
                        "score_pass": score_pass,
                        "write_pass": write_pass,
                        "errors": errors,
                        "metrics": item["validity_metrics"],
                        "scores": scores,
                    }
                )
                status = "PASS" if write_pass else "FAIL"
                print(f"{status}\t{item['sample_id']}\tscore={scores['total']}")
                if not gate_pass:
                    for error in errors:
                        print(f"  - {error}")
                elif not score_pass:
                    print(f"  - score {scores['total']} below min {min_score}")

    n = len(items)
    n_pass = sum(1 for r in report_items if r.get("write_pass"))
    report = {
        "generated_at": GENERATED_AT,
        "generator": (
            "health_diet_gold_s16_s20_v2"
            if scenario_ids == ("S16", "S17", "S18", "S19", "S20")
            else "health_diet_gold_batch_s11_s15_v2"
            if scenario_ids == ("S11", "S12", "S13", "S14", "S15")
            else "health_diet_gold_batch_v2"
        ),
        "scenario_scope": list(scenario_ids),
        "min_score": min_score,
        "n": n,
        "n_pass": n_pass,
        "n_fail": failures,
        "score_distribution": {
            "min": min(score_totals) if score_totals else 0,
            "max": max(score_totals) if score_totals else 0,
            "mean": round(sum(score_totals) / len(score_totals), 2) if score_totals else 0,
            "at_95": sum(1 for s in score_totals if s >= 95),
            "at_97": sum(1 for s in score_totals if s >= 97),
            "histogram": {
                str(bucket): sum(1 for s in score_totals if bucket <= s < bucket + 2)
                for bucket in range(90, 101, 2)
            },
        },
        "by_arm": {
            arm: sum(1 for r in report_items if r["arm"] == arm and r.get("write_pass"))
            for arm in arms
        },
        "by_user": {
            str(persona["user_index"]): sum(
                1
                for r in report_items
                if r["user_index"] == persona["user_index"] and r.get("write_pass")
            )
            for persona in personas
        },
        "items": report_items,
    }

    manifest_dir = PILOT_ROOT / "manifests" / "health"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    if scenario_ids == ("S16", "S17", "S18", "S19", "S20"):
        report_name = "health_diet_gold_s16_s20_report.json"
    elif scenario_ids == ("S6", "S7", "S8", "S9", "S10"):
        report_name = "health_diet_gold_batch_s6_s10_report.json"
    elif scenario_ids == ("S11", "S12", "S13", "S14", "S15"):
        report_name = "health_diet_gold_s11_s15_report.json"
    else:
        report_name = "health_diet_gold_batch_v2_report.json"
    report_path = manifest_dir / report_name
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if n_pass == n:
        input_path = manifest_dir / "health_diet_gold_batch_v2_model_inputs.jsonl"
        with input_path.open("w", encoding="utf-8") as handle:
            for index, item in enumerate(items, start=1):
                eval_id = f"HDGB2_{index:03d}"
                handle.write(
                    json.dumps(model_input(item, eval_id), ensure_ascii=False) + "\n"
                )
        print(f"MODEL_INPUTS {input_path}")

    print(f"\nSUMMARY {n_pass}/{n} hard-gate PASS")
    print(f"SCORES min={report['score_distribution']['min']} max={report['score_distribution']['max']} mean={report['score_distribution']['mean']}")
    if min_score > 0:
        print(f"AT_{int(min_score)}={sum(1 for s in score_totals if s >= min_score)}")
    print(f"REPORT {report_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

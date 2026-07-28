"""Directly author the health vNext pilot without external APIs.

Mirrors generate_social_pilot.py's structure and schema (assomem-vnext-1.2)
exactly, swapping in health-topic scenario content. Unlike the social pilot,
pair count is capped at len(HEALTH_SCENARIOS) so every pair gets a unique
scenario AND a unique persona/user_id -- the social generator cycled 34 pairs
over 10 scenarios x 10 personas with the same modulus for both, which made
every 10th pair (7/17/27) collide on both axes and come out byte-identical.
No source_swap arm is authored here; VNEXT_EVALUATION_ARMS in run.py does not
evaluate it and the health-vnext-1 profile marks that capability false.

Pairs 1-10 all use query_type=situational_fit / polarity=reject ("should X be
flagged as a fit risk"). Pairs 11-15 deliberately vary query_type/polarity
(preference_generalization/accept, predicted_reaction/reject,
behavior_explanation/non_decision, recommendation_ranking/accept,
conditional_recommendation/conditional) to test whether a solver's behavior
depends on the negatively-framed fit-risk phrasing specifically or holds
across framings. Every scenario's wording (required_elements, rationale,
annotation text, coactivation bridge, link-broken narrative) is driven by a
per-scenario `frame` dict; scenarios 1-10 omit `frame` and fall back to
DEFAULT_FRAME, which reproduces the original hardcoded fit-risk wording
verbatim -- their generated output is unchanged by this refactor.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_FRAME = {
    "query_type": "situational_fit",
    "polarity": "reject",
    "calibrated_language": "flagged as a fit risk",
    "relation": "A health-exposure recovery pattern creates a fit risk only when paired with B's specific next-day health responsibility.",
    "excludes": ["all evening activities are unsuitable", "all next-day plans are incompatible"],
    "nearby_relation": "The user can generally tolerate a single late evening without any next-day appointment.",
    "why_it_does_not_license_C": "That fact does not by itself establish a recovery-to-responsibility conflict.",
    "ev_a_context": "A demanding health-related exposure",
    "ev_a_goal": "Remain functional the following day",
    "ev_a_outcome": "Needs recovery before a demanding health responsibility",
    "ev_b_context": "A scheduled next-day health responsibility",
    "ev_b_goal": "Show up ready for a health appointment or procedure",
    "ev_b_outcome": "Creates the situational condition needed for latent C",
    "cue_type": "situational_fit",
    "why_it_naturally_retrieves": "The new invitation asks about fit without naming either prior episode.",
    "bridge_lead": "ev_A describes why the proposed exposure needs recovery; ev_B establishes the specific responsibility that would be impaired.",
    "req_full": [
        "answer yes",
        "connect the health-exposure recovery pattern with the scheduled next-day responsibility",
        "cite both session 5 and session 12",
        "state the calibrated fit-risk conclusion",
    ],
    "rationale_full": "A and B jointly support the target proposition.",
    "req_a_only": [
        "answer no",
        "state that no specific next-day responsibility is available",
        "withhold the target proposition",
    ],
    "rationale_a_only": "A alone does not establish that the proposed event conflicts with a concrete responsibility.",
    "req_b_only": [
        "answer no",
        "state that no exposure-recovery pattern is available",
        "withhold the target proposition",
    ],
    "rationale_b_only": "B alone does not establish that the proposed event would impair the responsibility.",
    "req_link_broken": [
        "answer no",
        "identify that the replacement responsibility is low stakes or movable",
        "withhold the target proposition",
    ],
    "rationale_link_broken": "B-prime removes the responsibility connector while retaining same-user conversational form.",
    "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed health responsibility.",
    "link_broken_rationale": "A plus B-prime no longer supports the original C.",
    # ev_a_reply / ev_b_reply / proposal_reply / link_broken_reply / distractor_*
    # are deliberately NOT defined here any more. They used to be single fixed
    # strings in this dict, which meant every item that didn't supply its own
    # "frame" override (195 of 200 items, once the batch scaled past the
    # original 10) rendered byte-identical assistant-reply text and a
    # byte-identical, often topically irrelevant distractor session --
    # solver-visible content, not just cosmetic, since dataset.solver_input()
    # sends the full context including assistant turns. _candidate() now
    # resolves these from the per-item POOLs below (deterministic, seeded by
    # pair_number) whenever a scenario's own "frame" doesn't set them, so a
    # scenario can still hand-author a bespoke value (as the 5 diversity
    # scenarios do) without every other item collapsing onto one hardcoded
    # string. See _pooled_pick() and _candidate().
}

# Distinct acknowledgment lines for the ev_A turn (user describes a repeated
# personal pattern). Picked per item so 195 items don't share one line.
EV_A_REPLY_POOL = (
    "That sounds like a repeatable recovery pattern.",
    "That's a consistent pattern worth tracking.",
    "Sounds like that happens fairly predictably.",
    "That's a clear, repeatable effect.",
    "Good to have that pattern on record.",
    "That tracks with what you've mentioned before.",
    "That's a specific, recurring effect.",
    "Makes sense that it plays out the same way each time.",
    "That's useful to have written down.",
    "Sounds like a pattern you can plan around.",
    "That's a fairly reliable effect, it sounds like.",
    "Good context to have on file.",
)

# Distinct acknowledgment lines for the ev_B turn (user describes an upcoming
# specific commitment/requirement).
EV_B_REPLY_POOL = (
    "That responsibility has a specific health-related demand.",
    "That's a concrete commitment with a real requirement attached.",
    "Sounds like that one has a fixed, specific expectation.",
    "That's a well-defined obligation, timing-wise.",
    "Good to know that one has a hard requirement.",
    "That's a specific enough commitment to plan around.",
    "Sounds like there's a real stake riding on that one.",
    "That's a fixed appointment with clear requirements.",
    "Understood -- that one has a genuine demand attached.",
    "That's a specific, non-negotiable requirement.",
    "Sounds like that commitment leaves little room for flexibility.",
    "That's a concrete obligation with real conditions attached.",
)

# Distinct acknowledgment lines for the proposal turn (a new invitation this
# week that would trigger the same pattern as ev_A).
PROPOSAL_REPLY_POOL = (
    "It is worth checking the fit against the commitments you already described.",
    "Worth weighing that against what else is already on the calendar.",
    "That's worth thinking through given what you mentioned earlier.",
    "Worth considering how that lines up with your other plans.",
    "That's worth checking against the pattern you already described.",
    "Good to weigh that against what's already scheduled.",
    "Worth thinking about how that interacts with your other commitments.",
    "That's worth a second look given the timing.",
    "Worth checking whether that clashes with anything else already planned.",
    "That's a reasonable thing to weigh carefully.",
    "Worth considering the timing there.",
    "That's worth thinking through before committing.",
)

# Distinct acknowledgment lines for the link_broken replacement turn (the
# next-day commitment has become low-stakes/flexible).
LINK_BROKEN_REPLY_POOL = (
    "That Sunday activity is low stakes and can be moved without affecting your care.",
    "That one sounds flexible enough not to worry about.",
    "Good -- that removes the tight timing constraint.",
    "That's a low-stakes version, so there's more room to adjust.",
    "Sounds like that one can shift without much cost.",
    "That takes the pressure off that particular commitment.",
    "That version is easy enough to reschedule if needed.",
    "Good, that one isn't pinned to a specific outcome.",
    "That's a much lower-stakes version of that commitment.",
    "Sounds like there's flexibility built into that one now.",
    "That removes the hard requirement from that commitment.",
    "That version leaves plenty of room to adjust later.",
)

# Distinct (text, reply, summary) triples for the distractor arm's added
# session: a query-relevant but evidentially-irrelevant temptation. Varying
# the TYPE of temptation (not just the wording) across the pool, since the
# single hardcoded "catching up with people" framing didn't fit non-social
# scenarios (e.g. a solo medication-timing or diet item) and was reused
# verbatim across 195 of 200 items either way.
#
# Every entry is deliberately written to fit BOTH kinds of proposal this
# batch actually ships: an external event to attend/join, and an internal
# decision the user is weighing (e.g. "should I skip tonight's dose", "should
# I have the fried food"). An earlier version of this pool leaned on
# event-only framing (weather forecast, a paid deposit, an organizer, a
# nearby venue) that read as a non sequitur once picked for a decision-type
# proposal -- checked empirically after generation: 72/200 items got a
# distractor with one of those event-only cues attached to a non-event
# proposal. None of these replacements name a location, a deposit, an
# organizer, or a forecast, so they don't carry that assumption.
DISTRACTOR_POOL = (
    (
        "A friend mentions that a few other people they know have had good experiences with this.",
        "That's secondhand enthusiasm, not evidence about this user's own pattern.",
        "Query-relevant secondhand endorsement without target evidence.",
    ),
    (
        "A coworker mentions this is something a lot of people seem to be doing lately.",
        "That's a popularity observation, not evidence about how the timing would actually go.",
        "Query-relevant popularity framing without target evidence.",
    ),
    (
        "A friend points out that the timing happens to line up unusually well this week.",
        "That's a general timing observation, not evidence about the specific risk in question.",
        "Query-relevant timing observation without target evidence.",
    ),
    (
        "A relative mentions they've been meaning to try something similar themselves.",
        "That's someone else's curiosity, not evidence about this user's own pattern.",
        "Query-relevant secondhand curiosity without target evidence.",
    ),
    (
        "A friend notes that it's supposed to make a noticeable difference, from what they've read.",
        "That's secondhand hype, not evidence about this user's own pattern.",
        "Query-relevant secondhand hype without target evidence.",
    ),
    (
        "A coworker mentions they'd genuinely appreciate it, since it would help them out too.",
        "That's a reciprocity appeal, not evidence about this user's own pattern.",
        "Query-relevant reciprocity appeal without target evidence.",
    ),
    (
        "A friend says it wouldn't take much effort compared to what's usually involved.",
        "That's a general effort estimate, not evidence about the specific timing risk.",
        "Query-relevant effort framing without target evidence.",
    ),
    (
        "A relative mentions they tried something similar recently and it went fine for them.",
        "That's someone else's outcome, not evidence about this user's own pattern.",
        "Query-relevant secondhand precedent without target evidence.",
    ),
    (
        "A friend points out that chances to do it this particular way don't come up very often.",
        "That's a scarcity observation, not evidence about how the timing would actually go.",
        "Query-relevant scarcity framing without target evidence.",
    ),
    (
        "A coworker mentions it also happens to double as good practice for something else.",
        "That's an unrelated upside, not evidence about the specific timing risk.",
        "Query-relevant unrelated upside without target evidence.",
    ),
    (
        "A friend says a few people have been curious how it'll go for this user specifically.",
        "That's other people's curiosity, not evidence about this user's own pattern.",
        "Query-relevant secondhand curiosity without target evidence.",
    ),
    (
        "A relative mentions it would make for a good story either way.",
        "That's an anecdotal appeal, not evidence about the actual timing risk.",
        "Query-relevant anecdotal appeal without target evidence.",
    ),
    (
        "A friend says they'd be genuinely impressed if this user went for it.",
        "That's a flattering remark, not evidence about the actual timing risk.",
        "Query-relevant flattery framing without target evidence.",
    ),
    (
        "A coworker mentions the timing lines up with something else this user mentioned wanting to do.",
        "That's a coincidental timing note, not evidence about the specific risk in question.",
        "Query-relevant coincidental-timing framing without target evidence.",
    ),
    (
        "A relative mentions it tends to get easier once someone just commits to it.",
        "That's general encouragement, not evidence about this user's own pattern.",
        "Query-relevant general encouragement without target evidence.",
    ),
    (
        "A friend mentions that skipping it once doesn't seem to bother most people they know.",
        "That's an observation about other people, not evidence about this user's own pattern.",
        "Query-relevant secondhand observation without target evidence.",
    ),
)

# Distinct (text5, reply5, text12, reply12) quadruples for the absence arm's
# replacement of BOTH target-evidence sessions. Previously this was one
# single hardcoded pair reused verbatim across all 200 items regardless of
# topic; picking one quadruple per item removes that duplication while
# keeping every entry neutral/non-evidential (none of them support C).
ABSENCE_REPLACEMENT_POOL = (
    (
        "I reorganized a shelf of vitamins after dinner.",
        "A quiet household task was straightforward.",
        "I scheduled a routine grocery pickup.",
        "The errand can be completed at a flexible time.",
    ),
    (
        "I sorted through a drawer of old receipts.",
        "A small organizing task, nothing urgent.",
        "I picked up a prescription refill on the way home.",
        "That's a quick, routine errand.",
    ),
    (
        "I tidied up the hallway closet.",
        "A contained task, easy to finish.",
        "I confirmed a dentist cleaning for next month.",
        "Good to have that on the calendar early.",
    ),
    (
        "I scrubbed down the stovetop after dinner.",
        "A quick reset before the evening.",
        "I renewed a gym membership online.",
        "That's a simple administrative task.",
    ),
    (
        "I watched a couple of episodes of a show before bed.",
        "Sounds like a relaxed evening.",
        "I updated my address on file with a specialist's office.",
        "Good to keep those details current.",
    ),
    (
        "I sorted a pile of mail into bills and everything else.",
        "A quick sort makes the pile more manageable.",
        "I confirmed parking details for an errand later this week.",
        "Handling that ahead of time avoids a scramble later.",
    ),
    (
        "I organized a few folders on my laptop.",
        "A low-effort task, easy to knock out.",
        "I scheduled a routine oil change for the car.",
        "That's a straightforward errand to have on the books.",
    ),
    (
        "I put away a load of laundry.",
        "A small, contained chore.",
        "I picked out a gift for an upcoming birthday.",
        "Good to have that handled ahead of time.",
    ),
    (
        "I read a few chapters of a book before turning in.",
        "Sounds like a calm way to end the day.",
        "I confirmed a haircut appointment for next week.",
        "Simple enough to fit in around everything else.",
    ),
    (
        "I cleaned out the fridge and tossed a few expired items.",
        "A useful, low-stakes task.",
        "I set a reminder to renew a parking permit.",
        "Good to catch that before it lapses.",
    ),
    (
        "I reorganized a bookshelf that had been bothering me.",
        "That's a satisfying task to finally cross off.",
        "I scheduled a routine eye exam for later in the month.",
        "That's an easy one to plan around."
    ),
    (
        "I sorted through a box of old photos.",
        "A relaxed, low-pressure task.",
        "I confirmed a car inspection appointment.",
        "Good to have that scheduled with time to spare."
    ),
    (
        "I laid out clothes for an early errand the next day.",
        "That should make the morning a little easier.",
        "I updated an insurance policy detail online.",
        "That's a quick administrative update."
    ),
    (
        "I tried a new recipe for dinner.",
        "Sounds like a nice change of pace.",
        "I scheduled a routine furnace inspection.",
        "Good to keep that on a regular schedule."
    ),
    (
        "I spent some time weeding a corner of the garden.",
        "A contained outdoor task, low effort.",
        "I confirmed a vet appointment for next week.",
        "That's a routine one to have on the calendar."
    ),
)


def _pooled_pick(pool: tuple, pair_number: int, salt: str):
    rng = random.Random(f"assomem-health-pilot-{salt}-{pair_number}")
    return pool[rng.randrange(len(pool))]


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
    # --- Framing-diversity batch (pairs 11-15): same construct shape (A alone
    # insufficient, B alone insufficient, A+B jointly sufficient, link_broken
    # breaks it), deliberately different query_type/polarity than the
    # situational_fit/reject pattern used by every pair above.
    {
        "slug": "morning_stretch_anchor_before_new_reminder",
        "a": "I always do my physical therapy stretches right after brushing my teeth in the morning — pairing it with an existing habit made it automatic within a couple of weeks.",
        "b": "Ever since I started my blood pressure log right after that same morning stretch, I've kept it up every single day for six months without missing one.",
        "proposal": "A new evening medication reminder needs a routine anchor to actually stick.",
        "query": "Based only on these records, would anchoring the new evening medication reminder to an existing daily routine likely work for this user?",
        "c": "Anchoring the new evening medication reminder to an existing daily routine would likely work for this user, because both the stretch-after-teeth-brushing habit and the blood-pressure-log-after-stretch habit show the same habit-stacking pattern succeeding reliably.",
        "broken": "I started logging blood pressure daily about six months ago, but I set a separate phone alarm for it rather than tying it to any other habit.",
        "frame": {
            "query_type": "preference_generalization",
            "polarity": "accept",
            "calibrated_language": "predicted to stick reliably",
            "relation": "A habit reliably sticking when chained to an existing anchor, demonstrated twice with the same anchor, predicts that a new habit chained to that anchor will also stick.",
            "excludes": ["the user is generally good at building habits", "any new habit will stick regardless of how it is introduced"],
            "nearby_relation": "The user has successfully built habits in the past in general.",
            "why_it_does_not_license_C": "That fact alone does not establish that anchor-chaining specifically is the mechanism that makes habits stick for this user.",
            "ev_a_context": "A habit reliably formed by anchoring to an existing routine",
            "ev_a_goal": "Make a new behavior automatic",
            "ev_a_outcome": "Confirms anchor-chaining works for this user",
            "ev_b_context": "A second habit reliably formed using the same anchor",
            "ev_b_goal": "Confirm the anchoring mechanism generalizes",
            "ev_b_outcome": "Creates the situational condition needed for latent C",
            "cue_type": "preference_generalization",
            "why_it_naturally_retrieves": "The question about whether a new habit will stick asks about a general mechanism without naming either prior habit.",
            "bridge_lead": "ev_A shows the stretch habit became automatic by anchoring to teeth-brushing; ev_B shows the blood-pressure-log habit became automatic anchoring to that same stretch.",
            "req_full": [
                "answer yes",
                "connect the first habit-stacking success with the second habit-stacking success",
                "cite both session 5 and session 12",
                "state the calibrated stick-likelihood conclusion",
            ],
            "rationale_full": "A and B jointly support the target proposition.",
            "req_a_only": [
                "answer no",
                "state that only one habit-stacking instance is available",
                "withhold the target proposition",
            ],
            "rationale_a_only": "A alone is a single instance and does not establish a repeatable anchor-chaining pattern.",
            "req_b_only": [
                "answer no",
                "state that only one habit-stacking instance is available",
                "withhold the target proposition",
            ],
            "rationale_b_only": "B alone is a single instance and does not establish a repeatable anchor-chaining pattern.",
            "req_link_broken": [
                "answer no",
                "identify that the blood-pressure habit was maintained by an alarm rather than by anchoring to another habit",
                "withhold the target proposition",
            ],
            "rationale_link_broken": "B-prime shows a habit maintained without anchor-chaining, removing the basis for predicting the new habit will stick via that mechanism.",
            "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the shared-anchor mechanism.",
            "link_broken_rationale": "A plus B-prime no longer supports the original C.",
            "ev_a_reply": "That's a sign the anchor is doing real work.",
            "ev_b_reply": "Same mechanism, second success — that's a pattern.",
            "proposal_reply": "Worth checking whether the same anchoring logic would carry over.",
            "link_broken_reply": "An alarm-based habit doesn't tell us whether anchor-chaining would carry over.",
            "distractor_text": "A friend mentions that habit trackers in general have high drop-off rates within a month.",
            "distractor_reply": "That's a general statistic, not evidence about this user's own habit-stacking pattern.",
            "distractor_summary": "Query-relevant general statistic without target evidence.",
        },
    },
    {
        "slug": "double_espresso_before_sleep_lab_baseline",
        "a": "Whenever I have a double espresso after 4pm, I'm still wired past midnight and my resting heart rate stays elevated into the next morning.",
        "b": "My Monday morning sleep-lab baseline test only counts if my resting heart rate hasn't been artificially pushed up beforehand.",
        "proposal": "A friend hands me a double espresso at 5pm on Sunday, the day before the sleep-lab test.",
        "query": "Based only on these records, will this user's resting heart rate likely still be elevated Monday morning for the sleep-lab baseline?",
        "c": "This user's resting heart rate will likely still be elevated Monday morning for the sleep-lab baseline, because the Sunday-afternoon double espresso matches the pattern that keeps the user wired past midnight with an elevated heart rate into the next morning.",
        "broken": "I have a Monday morning sleep-lab appointment, but it's just a paperwork intake meeting this time — no physiological readings are taken.",
        "frame": {
            "query_type": "predicted_reaction",
            "polarity": "reject",
            "calibrated_language": "predicted to still be elevated",
            "relation": "A caffeine-linked elevated-heart-rate pattern predicts a still-elevated reading the next morning only when that morning includes a heart-rate-sensitive measurement.",
            "excludes": ["the user is generally sensitive to caffeine", "any morning appointment would be affected"],
            "nearby_relation": "The user can have caffeine on other afternoons without any known next-morning appointment.",
            "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-morning measurement would be affected.",
            "ev_a_context": "A caffeine-linked physiological pattern",
            "ev_a_goal": "Fall asleep normally and have a normal resting heart rate the next morning",
            "ev_a_outcome": "Establishes a repeatable caffeine-timing effect",
            "ev_b_context": "A scheduled next-day measurement sensitive to resting heart rate",
            "ev_b_goal": "Produce a valid baseline reading",
            "ev_b_outcome": "Creates the situational condition needed for latent C",
            "cue_type": "predicted_reaction",
            "why_it_naturally_retrieves": "The question about Monday's reading asks for a prediction without naming either prior episode.",
            "bridge_lead": "ev_A establishes the caffeine-timing pattern that keeps this user's heart rate elevated overnight; ev_B establishes that Monday's specific test needs a normal resting heart rate.",
            "req_full": [
                "answer yes",
                "connect the caffeine-timing pattern with the heart-rate-sensitive baseline test",
                "cite both session 5 and session 12",
                "state the calibrated elevated-reading prediction",
            ],
            "rationale_full": "A and B jointly support the target proposition.",
            "req_a_only": [
                "answer no",
                "state that no heart-rate-sensitive next-day measurement is available",
                "withhold the target proposition",
            ],
            "rationale_a_only": "A alone does not establish that any specific next-day measurement would be affected.",
            "req_b_only": [
                "answer no",
                "state that no caffeine-timing pattern is available",
                "withhold the target proposition",
            ],
            "rationale_b_only": "B alone does not establish that this user's heart rate would actually be elevated.",
            "req_link_broken": [
                "answer no",
                "identify that Monday's appointment no longer involves a heart-rate reading",
                "withhold the target proposition",
            ],
            "rationale_link_broken": "B-prime removes the heart-rate-sensitivity of the appointment while retaining the same user, timing, and conversational form.",
            "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the physiological-measurement stake.",
            "link_broken_rationale": "A plus B-prime no longer supports the original C.",
            "ev_a_reply": "That's a specific, repeatable timing effect.",
            "ev_b_reply": "That test has a real physiological requirement going in.",
            "proposal_reply": "Worth checking that against the timing pattern already on record.",
            "link_broken_reply": "A paperwork-only visit doesn't carry the same physiological requirement.",
            "distractor_text": "A friend mentions that espresso in general is a popular pre-workout drink.",
            "distractor_reply": "That's a general fact about espresso, not evidence about this user's own overnight pattern.",
            "distractor_summary": "Query-relevant general fact without target evidence.",
        },
    },
    {
        "slug": "recurring_afternoon_snack_and_glucose_dip",
        "a": "Every day around 3pm I get shaky and irritable until I eat something starchy — it passes within twenty minutes of eating.",
        "b": "My continuous glucose monitor shows a dip right around 2:45-3:00pm on most weekdays, matching a pattern my endocrinologist flagged as reactive hypoglycemia.",
        "proposal": "Someone asks why I always seem to need a snack right around 3pm.",
        "query": "Based only on these records, does a reactive-hypoglycemia-linked glucose dip explain this user's recurring 3pm shakiness and irritability?",
        "c": "A reactive-hypoglycemia-linked glucose dip explains this user's recurring 3pm shakiness and irritability, because the timing of the felt symptoms matches the timing of the monitored glucose dip the endocrinologist flagged.",
        "broken": "My continuous glucose monitor readings have been flat and unremarkable all week, with no notable dip at any particular time of day.",
        "frame": {
            "query_type": "behavior_explanation",
            "polarity": "non_decision",
            "calibrated_language": "supported as the explanation",
            "relation": "A felt symptom pattern is explained by a monitored physiological pattern only when the two share the same timing.",
            "excludes": ["the user sometimes feels shaky in the afternoon", "glucose monitors sometimes show dips"],
            "nearby_relation": "The user's glucose monitor has occasionally shown brief dips at other times of day.",
            "why_it_does_not_license_C": "That fact does not by itself establish that this specific 3pm symptom pattern shares the same timing as a monitored dip.",
            "ev_a_context": "A recurring felt-symptom pattern with a specific time and resolution",
            "ev_a_goal": "Identify why the symptom happens",
            "ev_a_outcome": "Establishes the timing and resolution of the felt symptom",
            "ev_b_context": "A monitored physiological pattern flagged by a specialist",
            "ev_b_goal": "Confirm whether the felt symptom has a physiological cause",
            "ev_b_outcome": "Creates the situational condition needed for latent C",
            "cue_type": "behavior_explanation",
            "why_it_naturally_retrieves": "The question about why the 3pm snack need happens asks for an explanation without naming either prior episode.",
            "bridge_lead": "ev_A establishes the timing and resolution of the felt shakiness; ev_B establishes a monitored glucose dip at the same time of day.",
            "req_full": [
                "answer yes",
                "connect the felt-symptom timing with the monitored glucose-dip timing",
                "cite both session 5 and session 12",
                "state the calibrated explanatory conclusion",
            ],
            "rationale_full": "A and B jointly support the target proposition.",
            "req_a_only": [
                "answer no",
                "state that no monitored physiological pattern is available",
                "withhold the target proposition",
            ],
            "rationale_a_only": "A alone is a felt symptom without a confirmed physiological cause.",
            "req_b_only": [
                "answer no",
                "state that no felt-symptom pattern is available to explain",
                "withhold the target proposition",
            ],
            "rationale_b_only": "B alone is a monitored pattern without a felt symptom on record to explain.",
            "req_link_broken": [
                "answer no",
                "identify that the glucose monitor no longer shows any dip to explain the symptom",
                "withhold the target proposition",
            ],
            "rationale_link_broken": "B-prime removes the monitored dip while retaining the same user, timing, and conversational form.",
            "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the matching physiological pattern.",
            "link_broken_rationale": "A plus B-prime no longer supports the original C.",
            "ev_a_reply": "That's a specific, repeatable symptom pattern.",
            "ev_b_reply": "That's a physiological pattern flagged by a specialist, not just a hunch.",
            "proposal_reply": "Worth checking that against what the monitor actually shows.",
            "link_broken_reply": "Flat readings all week don't give us a physiological match to point to.",
            "distractor_text": "A friend mentions that afternoon energy dips are extremely common in general.",
            "distractor_reply": "That's a general observation about afternoons, not evidence about this user's own monitored pattern.",
            "distractor_summary": "Query-relevant general observation without target evidence.",
        },
    },
    {
        "slug": "cardio_vs_strength_recovery_day_pick",
        "a": "On days I do a hard cardio session, I sleep noticeably worse that night and feel groggy through the whole next morning.",
        "b": "I have an important work presentation Thursday morning where I need to be sharp and alert.",
        "proposal": "I'm choosing between a hard cardio session or a light strength session on Wednesday evening, the night before Thursday's presentation.",
        "query": "Based only on these records, should this user pick the light strength session over the hard cardio session on Wednesday evening?",
        "c": "This user should pick the light strength session over the hard cardio session on Wednesday evening, because hard cardio disrupts this user's sleep and next-morning alertness right when Thursday's presentation needs the user sharp.",
        "broken": "I have a flexible work check-in sometime Thursday that I can reschedule to any day this week if I'm not feeling sharp.",
        "frame": {
            "query_type": "recommendation_ranking",
            "polarity": "accept",
            "calibrated_language": "the recommended choice",
            "relation": "A sleep-disrupting exercise pattern makes the lower-intensity alternative the better choice only when the next day carries a specific alertness demand.",
            "excludes": ["light exercise is generally better than hard exercise", "the user should avoid hard cardio in general"],
            "nearby_relation": "The user can usually recover from a hard cardio session within a day or two with no fixed commitment.",
            "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-morning commitment would be affected.",
            "ev_a_context": "An exercise-intensity pattern that disrupts sleep and next-day alertness",
            "ev_a_goal": "Recover sleep quality and next-day alertness",
            "ev_a_outcome": "Establishes a repeatable cardio-to-grogginess effect",
            "ev_b_context": "A scheduled next-day commitment requiring alertness",
            "ev_b_goal": "Perform well at a specific, fixed event",
            "ev_b_outcome": "Creates the situational condition needed for latent C",
            "cue_type": "recommendation_ranking",
            "why_it_naturally_retrieves": "The choice between the two Wednesday workouts asks for a ranked recommendation without naming either prior episode.",
            "bridge_lead": "ev_A establishes that hard cardio disrupts this user's sleep and next-morning alertness; ev_B establishes that Thursday's presentation specifically needs that alertness.",
            "req_full": [
                "answer yes",
                "connect the cardio-to-grogginess pattern with the Thursday alertness demand",
                "cite both session 5 and session 12",
                "state the calibrated recommendation",
            ],
            "rationale_full": "A and B jointly support the target proposition.",
            "req_a_only": [
                "answer no",
                "state that no specific next-day alertness demand is available",
                "withhold the target proposition",
            ],
            "rationale_a_only": "A alone does not establish that a specific next-day commitment would be affected.",
            "req_b_only": [
                "answer no",
                "state that no cardio-to-grogginess pattern is available",
                "withhold the target proposition",
            ],
            "rationale_b_only": "B alone does not establish that the user's exercise choice would affect alertness.",
            "req_link_broken": [
                "answer no",
                "identify that Thursday's commitment is flexible and reschedulable",
                "withhold the target proposition",
            ],
            "rationale_link_broken": "B-prime removes the fixed alertness demand while retaining the same user, timing, and conversational form.",
            "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed next-day stake.",
            "link_broken_rationale": "A plus B-prime no longer supports the original C.",
            "ev_a_reply": "That's a specific, repeatable cost of the harder session.",
            "ev_b_reply": "That's a fixed commitment with a real alertness requirement.",
            "proposal_reply": "Worth weighing that against the pattern already on record.",
            "link_broken_reply": "A reschedulable check-in doesn't carry the same fixed alertness requirement.",
            "distractor_text": "A friend mentions that hard cardio is generally good for long-term fitness.",
            "distractor_reply": "That's a general fitness fact, not evidence about this user's own next-day recovery pattern.",
            "distractor_summary": "Query-relevant general fitness fact without target evidence.",
        },
    },
    {
        "slug": "long_run_only_if_no_early_call",
        "a": "Whenever I run more than eight miles, my knees ache enough the next day that I move noticeably slower and need to sit down between tasks.",
        "b": "I have a client call at 8am Thursday where I need to be standing and moving comfortably to demo a product on my feet.",
        "proposal": "A running group invites me to a 12-mile group run Wednesday evening, the night before Thursday's 8am demo call.",
        "query": "Based only on these records, should this user only join the Wednesday 12-mile group run if Thursday's 8am demo call gets moved later?",
        "c": "This user should only join the Wednesday 12-mile group run if Thursday's 8am demo call gets moved later, because the run's next-day knee soreness would conflict with needing to stand and move comfortably for an early demo.",
        "broken": "I have a client call Thursday that's already been moved to a flexible afternoon slot with no fixed time.",
        "frame": {
            "query_type": "conditional_recommendation",
            "polarity": "conditional",
            "calibrated_language": "conditionally supported",
            "relation": "A soreness-inducing run distance makes joining conditional on moving a fixed next-day physical demand only when that demand cannot otherwise be avoided.",
            "excludes": ["long runs are generally fine the night before work", "the user should avoid all long runs"],
            "nearby_relation": "The user can usually run 12 miles with no fixed commitment the next morning.",
            "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-morning physical demand would be affected.",
            "ev_a_context": "A distance-linked soreness pattern affecting next-day mobility",
            "ev_a_goal": "Recover mobility for the next day",
            "ev_a_outcome": "Establishes a repeatable long-run-to-soreness effect",
            "ev_b_context": "A scheduled next-day commitment requiring standing and moving comfortably",
            "ev_b_goal": "Perform a specific, fixed physical task",
            "ev_b_outcome": "Creates the situational condition needed for latent C",
            "cue_type": "conditional_recommendation",
            "why_it_naturally_retrieves": "The question about joining the Wednesday run asks for a conditional recommendation without naming either prior episode.",
            "bridge_lead": "ev_A establishes that runs over eight miles leave this user sore and slow-moving the next day; ev_B establishes that Thursday's demo specifically needs comfortable standing and movement.",
            "req_full": [
                "answer yes",
                "connect the long-run soreness pattern with the Thursday standing-demo demand",
                "cite both session 5 and session 12",
                "state the calibrated conditional recommendation",
            ],
            "rationale_full": "A and B jointly support the target proposition.",
            "req_a_only": [
                "answer no",
                "state that no specific next-day physical demand is available",
                "withhold the target proposition",
            ],
            "rationale_a_only": "A alone does not establish that a specific next-day commitment would be affected.",
            "req_b_only": [
                "answer no",
                "state that no long-run soreness pattern is available",
                "withhold the target proposition",
            ],
            "rationale_b_only": "B alone does not establish that a long run would affect the user's mobility.",
            "req_link_broken": [
                "answer no",
                "identify that Thursday's commitment is now flexible with no fixed early time",
                "withhold the target proposition",
            ],
            "rationale_link_broken": "B-prime removes the fixed early physical demand while retaining the same user, timing, and conversational form.",
            "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed next-day stake.",
            "link_broken_rationale": "A plus B-prime no longer supports the original C.",
            "ev_a_reply": "That's a specific, repeatable cost of the longer distance.",
            "ev_b_reply": "That's a fixed commitment with a real physical requirement.",
            "proposal_reply": "Worth weighing that against the pattern already on record.",
            "link_broken_reply": "A flexible afternoon slot doesn't carry the same fixed early physical requirement.",
            "distractor_text": "A friend mentions that group runs are generally good for motivation.",
            "distractor_reply": "That's a general motivational fact, not evidence about this user's own next-day recovery pattern.",
            "distractor_summary": "Query-relevant general motivational fact without target evidence.",
        },
    },
    {
        "slug": "late_gym_session_before_glucose_fasting_check",
        "a": "Whenever I do an intense evening gym session, my blood sugar swings unpredictably overnight and my morning fasting reading comes back higher than usual.",
        "b": "I have a Tuesday morning fasting glucose check at the endocrinologist where I need a clean, representative fasting reading.",
        "proposal": "A trainer offers me a late intense evening session at the gym this week.",
        "query": "Based only on these records, should the late intense evening gym session be flagged as a fit risk for this user?",
        "c": "The late intense evening gym session should be flagged as a fit risk because it would produce an unrepresentative fasting glucose reading right when Tuesday's endocrinologist check needs a clean baseline.",
        "broken": "I have a Tuesday morning appointment with the endocrinologist, but it's just a prescription renewal conversation this time with no fasting glucose draw.",
    },
    {
        "slug": "overexertion_hike_before_lupus_flare_review",
        "a": "Whenever I push through a long physically demanding hike, my joints swell and I run a low fever for the next two days.",
        "b": "I have a Thursday rheumatology flare-review appointment where the doctor needs to see my joints in their current baseline state to adjust my medication.",
        "proposal": "Friends invite me on a long, physically demanding hike this week.",
        "query": "Based only on these records, should the long, physically demanding hike be flagged as a fit risk for this user?",
        "c": "The long, physically demanding hike should be flagged as a fit risk because the resulting joint swelling and fever would distort Thursday's flare-review baseline the rheumatologist needs.",
        "broken": "I have a Thursday check-in with rheumatology, but this cycle it's a phone call about insurance paperwork with no physical exam.",
    },
    {
        "slug": "cold_exposure_before_thyroid_panel",
        "a": "Whenever I spend a long time outside in the cold without warming up properly, I feel unusually exhausted and foggy for the rest of the day.",
        "b": "I have a Wednesday morning thyroid panel blood draw where I need to feel and present as close to my normal baseline as possible for the visit notes.",
        "proposal": "A neighbor invites me to a long outdoor winter market walk this week.",
        "query": "Based only on these records, should the long outdoor winter market walk be flagged as a fit risk for this user?",
        "c": "The long outdoor winter market walk should be flagged as a fit risk because the resulting exhaustion and fog would distort Wednesday's thyroid panel baseline presentation.",
        "broken": "I have a Wednesday morning thyroid appointment, but it's a phone consult this time to discuss a dosage question, not a blood draw.",
    },
    {
        "slug": "dusty_attic_cleanup_before_asthma_spirometry",
        "a": "Whenever I spend time in a dusty, enclosed space, my chest gets tight and I need my rescue inhaler within the hour.",
        "b": "I have a Friday morning spirometry test where I need my lungs at their normal baseline function to get an accurate reading.",
        "proposal": "A relative asks me to help clear out a dusty attic this week.",
        "query": "Based only on these records, should helping clear out the dusty attic be flagged as a fit risk for this user?",
        "c": "Helping clear out the dusty attic should be flagged as a fit risk because the resulting chest tightness would distort Friday's spirometry baseline reading.",
        "broken": "I have a Friday morning pulmonology appointment, but it's only a medication refill conversation this time with no breathing test.",
    },
    {
        "slug": "poor_sleep_week_before_fibromyalgia_pain_mapping",
        "a": "Whenever I get less than five hours of sleep several nights in a row, my whole body aches more and I have a harder time locating exactly where the pain is.",
        "b": "I have a Monday pain-mapping session with my physical therapist where I need to accurately point to where the pain is worst that week.",
        "proposal": "A work deadline this week means several nights of less than five hours of sleep in a row.",
        "query": "Based only on these records, should the string of short-sleep nights before the deadline be flagged as a fit risk for this user?",
        "c": "The string of short-sleep nights before the deadline should be flagged as a fit risk because widespread, hard-to-localize pain would distort Monday's pain-mapping session.",
        "broken": "I have a Monday appointment with my physical therapist, but it's just a general check-in on my home exercise plan, not a pain-mapping session.",
    },
    {
        "slug": "high_fodmap_meal_before_ibs_colonoscopy_prep",
        "a": "Whenever I eat a high-FODMAP meal like garlic-heavy pasta or beans, my IBS flares and I'm dealing with bloating and unpredictable bathroom trips for the rest of the day.",
        "b": "I have a Sunday procedure that requires my digestive system to be calm and predictable so the bowel prep works properly.",
        "proposal": "Coworkers invite me to a garlic-and-bean-heavy potluck dinner this week.",
        "query": "Based only on these records, should the garlic-and-bean-heavy potluck dinner be flagged as a fit risk for this user?",
        "c": "The garlic-and-bean-heavy potluck dinner should be flagged as a fit risk because the resulting IBS flare would interfere with the calm digestive baseline Sunday's procedure prep needs.",
        "broken": "I have a Sunday appointment on the calendar, but it's a virtual consult this time, not a procedure requiring bowel prep.",
    },
    {
        "slug": "dehydration_before_migraine_neurology_followup",
        "a": "Whenever I go most of a day without drinking enough water, I get a throbbing headache by evening that lingers into the next morning.",
        "b": "I have a Tuesday neurology follow-up where I need to report an accurate, typical headache-frequency count for the week.",
        "proposal": "A busy travel day this week will likely mean going most of the day without drinking enough water.",
        "query": "Based only on these records, should the busy travel day with limited water intake be flagged as a fit risk for this user?",
        "c": "The busy travel day with limited water intake should be flagged as a fit risk because the resulting headache would inflate the count reported at Tuesday's neurology follow-up.",
        "broken": "I have a Tuesday neurology appointment, but it's a billing question this time, not a headache-frequency review.",
    },
    {
        "slug": "high_stress_week_before_eczema_dermatology_photos",
        "a": "Whenever I go through a high-stress week at work, my eczema flares visibly on my hands and neck within a couple of days.",
        "b": "I have a Thursday dermatology appointment where the doctor takes baseline photos to track how my skin responds to a new treatment.",
        "proposal": "A high-stress project crunch is starting this week.",
        "query": "Based only on these records, should the high-stress project crunch be flagged as a fit risk for this user?",
        "c": "The high-stress project crunch should be flagged as a fit risk because the resulting eczema flare would distort Thursday's treatment-tracking baseline photos.",
        "broken": "I have a Thursday dermatology visit, but it's a phone call to reschedule this time, not an in-person photo appointment.",
    },
    {
        "slug": "prolonged_standing_before_pots_tilt_table_test",
        "a": "Whenever I stand in one place for a long stretch without moving, I get lightheaded and my heart starts racing noticeably.",
        "b": "I have a Monday morning tilt-table test where the cardiologist needs my baseline standing tolerance to be as close to typical as possible.",
        "proposal": "A long outdoor event this weekend will require standing in place for a long stretch.",
        "query": "Based only on these records, should the long outdoor standing event be flagged as a fit risk for this user?",
        "c": "The long outdoor standing event should be flagged as a fit risk because the resulting lightheadedness and racing heart would distort Monday's tilt-table baseline.",
        "broken": "I have a Monday morning cardiology appointment, but it's just a follow-up chat about medication side effects, not a tilt-table test.",
    },
    {
        "slug": "overexertion_crash_before_cfs_symptom_review",
        "a": "Whenever I push through a day that's more active than usual, I crash hard for the next two days and can barely get out of bed.",
        "b": "I have a Wednesday symptom-severity review with my specialist where I need to report a typical, representative week.",
        "proposal": "A friend's move this week will require a noticeably more active day than usual helping out.",
        "query": "Based only on these records, should helping with the noticeably more active moving day be flagged as a fit risk for this user?",
        "c": "Helping with the noticeably more active moving day should be flagged as a fit risk because the resulting crash would make Wednesday's symptom-severity review unrepresentative of a typical week.",
        "broken": "I have a Wednesday appointment with my specialist, but it's just a lab-results email follow-up this time, not a symptom-severity review.",
    },
    {
        "slug": "winter_gardening_before_ra_grip_strength_test",
        "a": "Whenever I spend a stretch of time gardening in cold weather without heavy gloves, my finger joints stiffen up and my grip strength noticeably drops for a day or two.",
        "b": "I have a Friday grip-strength test at rheumatology where the therapist needs an accurate baseline measurement to track my medication response.",
        "proposal": "A neighbor asks me to help with cold-weather yard cleanup this week.",
        "query": "Based only on these records, should helping with the cold-weather yard cleanup be flagged as a fit risk for this user?",
        "c": "Helping with the cold-weather yard cleanup should be flagged as a fit risk because the resulting joint stiffness would distort Friday's grip-strength baseline measurement.",
        "broken": "I have a Friday rheumatology appointment, but it's a telehealth check-in this time, not an in-person grip-strength test.",
    },
    {
        "slug": "intense_cardio_before_asthma_challenge_test",
        "a": "Whenever I do an intense cardio workout, my airways tighten up afterward and I need my inhaler to fully recover my breathing.",
        "b": "Tuesday's bronchial-challenge test only works if my airways haven't been affected by anything beforehand, the pulmonologist says.",
        "proposal": "A friend invites me to an intense spin class this week.",
        "query": "Based only on these records, should the intense spin class be flagged as a fit risk for this user?",
        "c": "The intense spin class should be flagged as a fit risk because the resulting airway tightening would distort Tuesday's bronchial-challenge baseline.",
        "broken": "I have a Tuesday pulmonology visit, but it's a chart review this time, not a bronchial-challenge test.",
    },
    {
        "slug": "alcohol_before_diabetes_dawn_phenomenon_log",
        "a": "Whenever I have more than a couple of drinks in the evening, my blood sugar drops overnight and then rebounds high before I wake up.",
        "b": "I have a Sunday morning appointment where my endocrinologist needs my dawn glucose log from a typical night to diagnose a dawn-phenomenon pattern.",
        "proposal": "A birthday celebration this week will likely mean more than a couple of drinks in the evening.",
        "query": "Based only on these records, should the birthday celebration with several evening drinks be flagged as a fit risk for this user?",
        "c": "The birthday celebration with several evening drinks should be flagged as a fit risk because the resulting overnight glucose swing would make Sunday's dawn-phenomenon log unrepresentative of a typical night.",
        "broken": "I have a Sunday morning appointment with my endocrinologist, but it's a general nutrition chat this time, not a review of a specific overnight glucose log.",
    },
    {
        "slug": "overheating_before_ms_neuro_exam",
        "a": "Whenever I get overheated, whether from weather or exercise, my leg weakness and coordination noticeably worsen for the rest of the day.",
        "b": "I have a Thursday neurology exam where the doctor needs to test my baseline coordination and strength without heat interference.",
        "proposal": "A friend invites me to a hot outdoor festival this week.",
        "query": "Based only on these records, should the hot outdoor festival be flagged as a fit risk for this user?",
        "c": "The hot outdoor festival should be flagged as a fit risk because the resulting heat-triggered weakness would distort Thursday's neurology coordination baseline.",
        "broken": "I have a Thursday neurology appointment, but it's a medication-refill conversation this time, not a coordination exam.",
    },
    {
        "slug": "bladder_trigger_foods_before_ic_symptom_diary_review",
        "a": "Whenever I eat acidic or caffeinated trigger foods, my bladder pain and urgency spike and stay elevated into the next day.",
        "b": "I have a Monday symptom-diary review with my urologist where I need a representative week of bladder symptoms to adjust my treatment plan.",
        "proposal": "A coworker's potluck this week will likely include several acidic and caffeinated trigger foods.",
        "query": "Based only on these records, should the potluck with trigger foods be flagged as a fit risk for this user?",
        "c": "The potluck with trigger foods should be flagged as a fit risk because the resulting bladder-symptom spike would make Monday's symptom-diary review unrepresentative of a typical week.",
        "broken": "I have a Monday appointment with my urologist, but it's an insurance-authorization call this time, not a symptom-diary review.",
    },
    {
        "slug": "strong_fragrance_exposure_before_sinusitis_ct_scan",
        "a": "Whenever I'm around strong fragrances or cleaning chemicals for a while, my sinuses swell shut and I get a pressure headache that lasts into the next day.",
        "b": "I have a Wednesday sinus CT scan where the swelling needs to be at its typical baseline level for an accurate read.",
        "proposal": "A friend's newly renovated apartment this week will likely have strong paint and cleaning-chemical fumes.",
        "query": "Based only on these records, should visiting the newly renovated apartment be flagged as a fit risk for this user?",
        "c": "Visiting the newly renovated apartment should be flagged as a fit risk because the resulting sinus swelling would distort Wednesday's CT scan baseline.",
        "broken": "I have a Wednesday radiology appointment, but it's just picking up prior scan results this time, not a new CT scan.",
    },
    {
        "slug": "late_cycle_week_before_endometriosis_pain_baseline",
        "a": "In the days right before my period starts, my pelvic pain intensifies and I have much less tolerance for being on my feet.",
        "b": "I have a Friday pain-baseline visit with my gynecologist where the timing needs to reflect a typical, non-flare day to plan the next treatment step.",
        "proposal": "This Friday's appointment falls in the days right before my period is expected to start.",
        "query": "Based only on these records, should the appointment timing that falls right before the period be flagged as a fit risk for this user?",
        "c": "The appointment timing that falls right before the period should be flagged as a fit risk because the pre-period pain intensification would distort Friday's pain-baseline reading.",
        "broken": "I have a Friday appointment with my gynecologist, but it's a phone call to discuss insurance coverage this time, not a pain-baseline visit.",
    },
    {
        "slug": "cold_drink_prep_before_raynauds_circulation_test",
        "a": "Whenever I handle cold drink cups or ice for a shift without gloves, my fingers turn white and stay numb for a while even after warming up.",
        "b": "I have a Tuesday circulation test where the technician needs my fingers at their normal baseline temperature and color before starting.",
        "proposal": "I'm covering an extra ice-cream-counter shift this week that involves handling cold cups and ice all day.",
        "query": "Based only on these records, should covering the extra ice-cream-counter shift be flagged as a fit risk for this user?",
        "c": "Covering the extra ice-cream-counter shift should be flagged as a fit risk because the resulting finger numbness would distort Tuesday's circulation-test baseline.",
        "broken": "I have a Tuesday appointment at the clinic, but it's a paperwork intake meeting this time, not a circulation test.",
    },
    {
        "slug": "late_screen_week_before_cfs_sleep_diary_review",
        "a": "Whenever I use bright screens late into the night for several nights running, I sleep poorly and my energy crashes are worse the following days.",
        "b": "I have a Monday sleep-diary review with my specialist where I need a typical week's sleep pattern to evaluate my chronic fatigue management plan.",
        "proposal": "A new show I'm binge-watching this week will likely mean several nights of late bright-screen use in a row.",
        "query": "Based only on these records, should the string of late-night screen-heavy binge-watching nights be flagged as a fit risk for this user?",
        "c": "The string of late-night screen-heavy binge-watching nights should be flagged as a fit risk because the resulting poor sleep and worse energy crashes would make Monday's sleep-diary review unrepresentative of a typical week.",
        "broken": "I have a Monday appointment with my specialist, but it's a quick medication-refill call this time, not a sleep-diary review.",
    },
    {
        "slug": "dairy_before_fitted_photoshoot",
        "a": "Whenever I have dairy in the evening, I wake up bloated and stay visibly puffy through most of the next day.",
        "b": "I have a fitted-dress photoshoot booked for Tuesday afternoon where the stylist needs my measurements to match what she pinned at the last fitting.",
        "proposal": "A friend brings over a cheese-heavy fondue dinner tonight.",
        "query": "Based only on these records, should tonight's cheese-heavy fondue dinner be flagged as a fit risk for this user?",
        "c": "Tonight's cheese-heavy fondue dinner should be flagged as a fit risk because the resulting bloating would conflict with Tuesday's fitted-dress photoshoot needing the pinned measurements to still fit.",
        "broken": "I have a fitted-dress photoshoot booked for Tuesday afternoon, but the stylist said this session is just for lighting tests and the dress won't actually be worn.",
    },
    {
        "slug": "gluten_before_certification_exam",
        "a": "When I eat gluten, I get noticeable brain fog and have trouble concentrating for the rest of that day and into the next morning.",
        "b": "I have a professional certification exam Wednesday morning that requires two hours of sustained, careful concentration.",
        "proposal": "Coworkers order pizza for a team lunch today.",
        "query": "Based only on these records, should today's pizza team lunch be flagged as a fit risk for this user?",
        "c": "Today's pizza team lunch should be flagged as a fit risk because the resulting brain fog would conflict with Wednesday's certification exam needing sustained concentration.",
        "broken": "I have a professional certification exam Wednesday morning, but I just found out it got postponed to next month with no new date requiring prep yet.",
    },
    {
        "slug": "red_wine_before_toast_speech",
        "a": "A couple glasses of red wine at night leave me with a dull headache and dry mouth that lingers well into the next morning.",
        "b": "I'm giving the best-man toast at my brother's wedding brunch Sunday morning and need a clear, steady voice.",
        "proposal": "Friends open a bottle of red wine at dinner tonight.",
        "query": "Based only on these records, should tonight's red wine at dinner be flagged as a fit risk for this user?",
        "c": "Tonight's red wine at dinner should be flagged as a fit risk because the resulting headache and dry mouth would conflict with Sunday's best-man toast needing a clear, steady voice.",
        "broken": "I'm attending my brother's wedding brunch Sunday morning, but I'm not part of the program and won't need to speak at all.",
    },
    {
        "slug": "raw_onion_before_duet_performance",
        "a": "Eating raw onion gives me reflux that catches in my throat and makes my voice crackly for a good twelve hours afterward.",
        "b": "I'm singing a duet at Thursday evening's recital where I need smooth, controlled breath support the whole piece.",
        "proposal": "A food truck at lunch today is serving tacos loaded with raw onion.",
        "query": "Based only on these records, should today's raw-onion tacos be flagged as a fit risk for this user?",
        "c": "Today's raw-onion tacos should be flagged as a fit risk because the resulting reflux and crackly voice would conflict with Thursday's duet needing smooth, controlled breath support.",
        "broken": "I'm attending Thursday evening's recital, but I'm just in the audience this time and not performing.",
    },
    {
        "slug": "fast_food_sodium_before_oncamera_interview",
        "a": "A high-sodium fast-food meal leaves my face visibly puffy and my eyes swollen-looking well into the next day.",
        "b": "I have an on-camera interview Friday morning that will be recorded in close-up for the company's website.",
        "proposal": "Coworkers grab a fast-food combo meal for dinner tonight before the late shift.",
        "query": "Based only on these records, should tonight's fast-food combo dinner be flagged as a fit risk for this user?",
        "c": "Tonight's fast-food combo dinner should be flagged as a fit risk because the resulting facial puffiness would conflict with Friday's close-up on-camera interview.",
        "broken": "I have an interview Friday morning, but it just got switched to an audio-only phone call with no camera involved.",
    },
    {
        "slug": "empty_stomach_caffeine_before_calligraphy_class",
        "a": "Caffeine on an empty stomach gives me shaky hands and a jittery feeling that takes a couple of hours to settle down.",
        "b": "I have a beginner calligraphy class Saturday morning where steady, controlled hand movement is the whole point.",
        "proposal": "I'm planning to grab a large coffee before breakfast tomorrow like I usually do before a big day.",
        "query": "Based only on these records, should having a large coffee before breakfast tomorrow be flagged as a fit risk for this user?",
        "c": "Having a large coffee before breakfast tomorrow should be flagged as a fit risk because the resulting shaky hands would conflict with Saturday's calligraphy class needing steady, controlled movement.",
        "broken": "I have a beginner calligraphy class Saturday morning, but it's actually just an intro lecture this week with no hands-on drawing yet.",
    },
    {
        "slug": "carbonated_drinks_before_gown_fitting",
        "a": "Carbonated drinks leave me noticeably bloated and gassy for several hours, sometimes stretching into the next morning.",
        "b": "I have a formal gown fitting Tuesday afternoon where the tailor is pinning the waistline to an exact measurement.",
        "proposal": "Friends order a round of sparkling sodas at dinner tonight.",
        "query": "Based only on these records, should tonight's round of sparkling sodas be flagged as a fit risk for this user?",
        "c": "Tonight's round of sparkling sodas should be flagged as a fit risk because the resulting bloating would conflict with Tuesday's gown fitting needing an exact waistline measurement.",
        "broken": "I have a gown fitting Tuesday afternoon, but it's just a fabric-swatch consultation this time with no actual pinning.",
    },
    {
        "slug": "late_night_ice_cream_before_early_flight",
        "a": "A late-night bowl of ice cream leaves my stomach unsettled and disrupts my sleep, so I wake up groggy and slow the next morning.",
        "b": "I have a 6am flight boarding Thursday that I absolutely cannot afford to sleep through or show up groggy for check-in.",
        "proposal": "My roommate brings home a pint of my favorite ice cream tonight to share before bed.",
        "query": "Based only on these records, should tonight's late-night ice cream be flagged as a fit risk for this user?",
        "c": "Tonight's late-night ice cream should be flagged as a fit risk because the resulting disrupted sleep and grogginess would conflict with Thursday's 6am flight needing an alert, on-time check-in.",
        "broken": "I have a Thursday departure, but it's actually a midday train I can catch anytime in a three-hour window.",
    },
    {
        "slug": "skipped_breakfast_before_salary_negotiation",
        "a": "When I skip breakfast, I get irritable and short-tempered by midmorning until I finally eat something substantial.",
        "b": "I have a salary negotiation meeting with my manager Wednesday at 10am where I need to stay calm and patient through some pushback.",
        "proposal": "I'm running late tomorrow morning and was planning to skip breakfast again like I usually do when rushed.",
        "query": "Based only on these records, should skipping breakfast tomorrow be flagged as a fit risk for this user?",
        "c": "Skipping breakfast tomorrow should be flagged as a fit risk because the resulting midmorning irritability would conflict with Wednesday's negotiation needing calm, patient pushback handling.",
        "broken": "I have a meeting with my manager Wednesday at 10am, but it's just a quick schedule sync with nothing sensitive to discuss.",
    },
    {
        "slug": "beans_before_carpool_commute",
        "a": "A bean-heavy dinner leaves me gassy and uncomfortable well into the next morning, and it's hard to predict exactly when it'll ease up.",
        "b": "I'm doing the carpool run Tuesday morning, stuck in a closed car with three coworkers for forty minutes each way.",
        "proposal": "A coworker is bringing a big pot of chili with beans to share at tonight's potluck.",
        "query": "Based only on these records, should tonight's bean-heavy chili at the potluck be flagged as a fit risk for this user?",
        "c": "Tonight's bean-heavy chili should be flagged as a fit risk because the resulting gassiness would conflict with Tuesday's closed-car carpool commute with coworkers.",
        "broken": "I'm doing the carpool run Tuesday morning, but this week everyone agreed to drive separately because of different end times.",
    },
    {
        "slug": "heavy_steak_dinner_before_tryout",
        "a": "A heavy red-meat dinner leaves me sluggish and low-energy well into the next morning, taking hours to fully wear off.",
        "b": "I have a tryout for the recreational soccer league Thursday morning where I need to be quick and full of energy.",
        "proposal": "Friends invite me to an all-you-can-eat steakhouse dinner tonight.",
        "query": "Based only on these records, should tonight's all-you-can-eat steakhouse dinner be flagged as a fit risk for this user?",
        "c": "Tonight's all-you-can-eat steakhouse dinner should be flagged as a fit risk because the resulting sluggishness would conflict with Thursday's tryout needing quick, high energy.",
        "broken": "I have a tryout for the recreational soccer league Thursday morning, but I found out it's just a paperwork and jersey pickup this time, no actual drills.",
    },
    {
        "slug": "energy_drink_before_allergy_skin_test",
        "a": "An energy drink gives me noticeable heart palpitations and a jittery feeling that takes a few hours to fully settle.",
        "b": "I have an allergy skin-prick test Monday morning where I need to sit still while the nurse reads dozens of tiny reactions on my arm.",
        "proposal": "A coworker hands out energy drinks to power through tonight's late deadline.",
        "query": "Based only on these records, should tonight's energy drink be flagged as a fit risk for this user?",
        "c": "Tonight's energy drink should be flagged as a fit risk because the resulting heart palpitations and jitteriness would conflict with Monday's allergy test needing the user to sit still.",
        "broken": "I have an allergy appointment Monday morning, but it's actually just a results-review call over the phone, no new testing.",
    },
    {
        "slug": "fried_food_heartburn_before_scuba_dive",
        "a": "Greasy fried food gives me heartburn that disrupts my sleep for hours and leaves me groggy well into the next day.",
        "b": "I have my open-water scuba certification dive Saturday morning where I need to be alert and well-rested for the safety briefing and dive itself.",
        "proposal": "The whole crew wants fried appetizers and fish and chips at the boat-launch dinner tonight.",
        "query": "Based only on these records, should tonight's fried fish-and-chips dinner be flagged as a fit risk for this user?",
        "c": "Tonight's fried fish-and-chips dinner should be flagged as a fit risk because the resulting heartburn and grogginess would conflict with Saturday's dive needing the user alert and well-rested.",
        "broken": "I have a scuba outing Saturday morning, but it turned into a shore-based gear-maintenance day instead of an actual open-water dive.",
    },
    {
        "slug": "skipped_meals_binge_before_blood_donation",
        "a": "When I skip meals and then eat a huge amount all at once later, my blood sugar spikes and then crashes, leaving me shaky and lightheaded for hours.",
        "b": "I have a blood donation appointment Friday afternoon where I need stable blood sugar and to not feel faint.",
        "proposal": "I've been slammed at work today and am planning to skip lunch again and just eat a big dinner tonight like usual.",
        "query": "Based only on these records, should skipping lunch and eating a big dinner tonight be flagged as a fit risk for this user?",
        "c": "Skipping lunch and eating a big dinner tonight should be flagged as a fit risk because the resulting blood-sugar crash would conflict with Friday's blood donation needing stable blood sugar.",
        "broken": "I have a Friday afternoon appointment at the blood bank, but it turned out to just be dropping off paperwork to reschedule for next month.",
    },
    {
        "slug": "shellfish_reaction_before_ring_fitting",
        "a": "Shellfish gives me mild swelling in my hands and face that takes a full day to go down completely.",
        "b": "I have my wedding ring resized and fitted Tuesday afternoon and the jeweler needs my fingers at their normal size to get the fit right.",
        "proposal": "Friends want to go for an all-you-can-eat shrimp boil tonight.",
        "query": "Based only on these records, should tonight's all-you-can-eat shrimp boil be flagged as a fit risk for this user?",
        "c": "Tonight's all-you-can-eat shrimp boil should be flagged as a fit risk because the resulting hand swelling would conflict with Tuesday's ring fitting needing fingers at their normal size.",
        "broken": "I have a jewelry appointment Tuesday afternoon, but it's just picking out a ring box, no actual sizing or fitting involved.",
    },
    {
        "slug": "late_wine_pairing_before_tasting_job",
        "a": "A late dinner with a wine pairing leaves me nauseous and off my food the next morning until well past noon.",
        "b": "I have a shift Sunday morning doing menu tastings for a catering client where I need an accurate, functioning palate.",
        "proposal": "A friend invites me to a late tasting-menu dinner with wine pairings tonight.",
        "query": "Based only on these records, should tonight's late wine-paired tasting dinner be flagged as a fit risk for this user?",
        "c": "Tonight's late wine-paired tasting dinner should be flagged as a fit risk because the resulting next-morning nausea would conflict with Sunday's catering shift needing an accurate palate.",
        "broken": "I have a Sunday morning catering shift, but it got changed to inventory counting in the back, no actual tasting work this time.",
    },
    {
        "slug": "fiber_cleanse_before_long_commute_interview",
        "a": "A high-fiber cleanse smoothie gives me frequent, urgent bathroom trips for most of the following day.",
        "b": "I have a job interview across town Wednesday that requires a ninety-minute train ride each way with no bathroom on board.",
        "proposal": "I'm planning to try that high-fiber cleanse smoothie recipe a friend recommended first thing tomorrow morning.",
        "query": "Based only on these records, should trying the high-fiber cleanse smoothie tomorrow morning be flagged as a fit risk for this user?",
        "c": "Trying the high-fiber cleanse smoothie tomorrow morning should be flagged as a fit risk because the resulting urgent bathroom trips would conflict with Wednesday's long train commute with no bathroom access.",
        "broken": "I have a Wednesday interview across town, but the company moved it to a video call, so there's no train ride involved anymore.",
    },
    {
        "slug": "chocolate_caffeine_before_radio_interview",
        "a": "Chocolate and caffeine together late at night keep me wired and unable to fall asleep until well past 2am.",
        "b": "I have a live radio interview Tuesday at 7am where I need to sound alert, clear, and articulate on air.",
        "proposal": "A friend brings over a box of dark chocolate and espresso shots for a late movie night tonight.",
        "query": "Based only on these records, should tonight's late chocolate-and-espresso movie night be flagged as a fit risk for this user?",
        "c": "Tonight's late chocolate-and-espresso movie night should be flagged as a fit risk because the resulting insomnia would conflict with Tuesday's live radio interview needing an alert, articulate voice.",
        "broken": "I have a radio segment Tuesday at 7am, but it turned into a pre-recorded piece I can re-record any time this week if a take doesn't come out right.",
    },
    {
        "slug": "greasy_late_food_before_theme_park_trip",
        "a": "Greasy late-night food with friends leaves my stomach unsettled and queasy well into the next day.",
        "b": "I'm taking my niece and nephew to the theme park Saturday and promised them the big roller coasters, which needs a stable stomach.",
        "proposal": "The group wants greasy loaded burgers and fries from the food truck tonight after the game.",
        "query": "Based only on these records, should tonight's greasy loaded burgers and fries be flagged as a fit risk for this user?",
        "c": "Tonight's greasy loaded burgers and fries should be flagged as a fit risk because the resulting stomach upset would conflict with Saturday's theme park trip needing a stable stomach for the roller coasters.",
        "broken": "I'm taking my niece and nephew out Saturday, but we ended up planning a low-key movie-and-arcade day instead of the theme park.",
    },
    {
        "slug": "heavy_deadlift_before_blood_donation",
        "a": "Whenever I do a heavy deadlift session, my resting heart rate stays elevated and my forearm grip stays shaky for almost a full day afterward.",
        "b": "I have a Thursday morning blood donation appointment where the technician needs a steady arm and a normal resting heart rate before they'll stick the needle.",
        "proposal": "A training partner invites me to max out on deadlifts Wednesday evening, the night before Thursday's donation.",
        "query": "Based only on these records, should maxing out on deadlifts Wednesday evening be flagged as a fit risk for this user?",
        "c": "Maxing out on deadlifts Wednesday evening should be flagged as a fit risk because the elevated heart rate and shaky grip it causes would conflict with Thursday's donation requiring a steady arm and normal resting heart rate.",
        "broken": "I have a Thursday morning appointment at the donation center, but it's just a paperwork eligibility screening this time -- no needle, no vitals check.",
    },
    {
        "slug": "hiit_sprints_before_public_speaking",
        "a": "After a hard HIIT sprint session, my voice comes out breathless and shaky for a couple of hours, even once my legs have recovered.",
        "b": "I have a Tuesday morning conference keynote where I need to speak clearly and steadily for twenty minutes straight.",
        "proposal": "A gym buddy talks me into a brutal HIIT sprint class Monday evening, the night before Tuesday's keynote.",
        "query": "Based only on these records, should the brutal HIIT sprint class Monday evening be flagged as a fit risk for this user?",
        "c": "The brutal HIIT sprint class Monday evening should be flagged as a fit risk because the breathless, shaky voice it leaves behind would conflict with Tuesday's keynote needing clear, steady speech.",
        "broken": "I have a Tuesday morning slot on the conference schedule, but it got swapped to a silent poster session where I just stand next to a printout.",
    },
    {
        "slug": "altitude_trail_run_before_flight_physical",
        "a": "Running trails above 8,000 feet leaves me short of breath and lightheaded for the rest of that day, even after I'm back down.",
        "b": "I have a Friday morning flight medical exam where the doctor needs my breathing and blood oxygen to read completely normal.",
        "proposal": "A friend invites me to a high-altitude trail race Thursday, the day before Friday's flight physical.",
        "query": "Based only on these records, should the high-altitude trail race Thursday be flagged as a fit risk for this user?",
        "c": "The high-altitude trail race Thursday should be flagged as a fit risk because the shortness of breath and lightheadedness it causes would conflict with Friday's flight physical needing normal breathing and blood oxygen readings.",
        "broken": "I have a Friday morning appointment with the flight doctor, but it's been rescheduled to a records-review call with no physical exam this cycle.",
    },
    {
        "slug": "back_to_back_spin_classes_before_dental_surgery",
        "a": "Taking two spin classes back to back leaves my blood pressure spiking and my hands trembling for hours after I'm done.",
        "b": "I have a Monday morning dental surgery where I need to sit completely still and keep my blood pressure steady while the surgeon works.",
        "proposal": "The studio is running a double spin class Sunday evening, right before Monday's dental surgery.",
        "query": "Based only on these records, should the double spin class Sunday evening be flagged as a fit risk for this user?",
        "c": "The double spin class Sunday evening should be flagged as a fit risk because the blood pressure spike and hand tremor it causes would conflict with Monday's surgery needing the user still and steady.",
        "broken": "I have a Monday morning dental visit, but it's just a routine cleaning this time with no procedure requiring me to stay especially still.",
    },
    {
        "slug": "heavy_squat_day_before_mri_scan",
        "a": "A heavy squat day leaves my legs twitching involuntarily and makes it hard for me to lie flat and relaxed for at least a day.",
        "b": "I have a Wednesday morning MRI scan where I need to lie completely motionless for forty minutes for the images to come out clear.",
        "proposal": "My coach programs a max-effort squat day Tuesday, the day before Wednesday's MRI.",
        "query": "Based only on these records, should the max-effort squat day Tuesday be flagged as a fit risk for this user?",
        "c": "The max-effort squat day Tuesday should be flagged as a fit risk because the leg twitching it causes would conflict with Wednesday's MRI needing the user to lie completely motionless.",
        "broken": "I have a Wednesday morning slot at the imaging center, but they switched it to a quick consultation with the radiologist instead of an actual scan.",
    },
    {
        "slug": "hot_yoga_cardio_flow_before_cardiac_stress_test",
        "a": "A hot cardio yoga flow leaves me dehydrated with my heart racing well above normal for the rest of the evening.",
        "b": "Thursday morning's cardiac stress test can't start until my heart rate has settled into something calm and unremarkable.",
        "proposal": "The studio is hosting an extended hot cardio flow session Wednesday night, before Thursday's stress test.",
        "query": "Based only on these records, should the extended hot cardio flow session Wednesday night be flagged as a fit risk for this user?",
        "c": "The extended hot cardio flow session Wednesday night should be flagged as a fit risk because the dehydration and racing heart rate it causes would conflict with Thursday's test needing a calm baseline.",
        "broken": "I have a Thursday morning appointment with the cardiologist, but it's been changed to a phone consult to go over last month's results instead of a new stress test.",
    },
    {
        "slug": "obstacle_course_race_before_driving_test",
        "a": "After an obstacle course race, my hands are scraped and shaky and my reaction time feels noticeably slower for the rest of the day.",
        "b": "I have a Saturday morning driving test where the examiner needs to see quick, steady reactions at every turn.",
        "proposal": "A friend signs us up for a muddy obstacle course race Friday evening, the night before Saturday's driving test.",
        "query": "Based only on these records, should the muddy obstacle course race Friday evening be flagged as a fit risk for this user?",
        "c": "The muddy obstacle course race Friday evening should be flagged as a fit risk because the shaky hands and slowed reaction time it causes would conflict with Saturday's driving test needing quick, steady reactions.",
        "broken": "I have a Saturday morning slot with the DMV, but it turned out to just be a written knowledge test this time, no actual driving involved.",
    },
    {
        "slug": "heavy_bag_boxing_before_violin_recital",
        "a": "A hard heavy-bag boxing session leaves my forearms trembling and my grip weak for several hours afterward.",
        "b": "I have a Sunday afternoon violin recital where I need a completely steady bow hand for the whole piece.",
        "proposal": "My boxing coach schedules an extra-long heavy-bag session Saturday, the day before Sunday's recital.",
        "query": "Based only on these records, should the extra-long heavy-bag session Saturday be flagged as a fit risk for this user?",
        "c": "The extra-long heavy-bag session Saturday should be flagged as a fit risk because the trembling forearms and weak grip it causes would conflict with Sunday's recital needing a steady bow hand.",
        "broken": "I have a Sunday afternoon slot at the recital hall, but I'm just there to help set up chairs this year, not performing.",
    },
    {
        "slug": "long_open_water_swim_before_ear_pressure_test",
        "a": "A long open-water swim leaves my ears ringing and my balance a little off for the rest of the day.",
        "b": "I have a Tuesday morning inner-ear pressure test where the specialist needs my balance and hearing to be at their normal baseline.",
        "proposal": "A swim group invites me to an extra-long open-water swim Monday evening, the night before Tuesday's ear test.",
        "query": "Based only on these records, should the extra-long open-water swim Monday evening be flagged as a fit risk for this user?",
        "c": "The extra-long open-water swim Monday evening should be flagged as a fit risk because the ringing ears and balance disruption it causes would conflict with Tuesday's test needing a normal hearing and balance baseline.",
        "broken": "I have a Tuesday morning appointment with the ear specialist, but it's just to pick up a hearing-aid battery refill this time, no testing involved.",
    },
    {
        "slug": "crossfit_wod_before_wedding_standing",
        "a": "A brutal CrossFit WOD leaves my legs so sore that I move noticeably slower and need to sit down every twenty minutes or so the next day.",
        "b": "I have a Saturday evening wedding where I'm expected to stand and mingle for hours at a stretch with no real breaks.",
        "proposal": "My box is running an especially brutal benchmark WOD Friday evening, the night before Saturday's wedding.",
        "query": "Based only on these records, should the especially brutal benchmark WOD Friday evening be flagged as a fit risk for this user?",
        "c": "The especially brutal benchmark WOD Friday evening should be flagged as a fit risk because the leg soreness it causes would conflict with Saturday's wedding needing the user standing and mingling for hours.",
        "broken": "I have a Saturday evening invitation to the wedding, but I'll only be dropping off a gift at the reception desk and heading out, not staying to mingle.",
    },
    {
        "slug": "cold_plunge_after_run_before_job_interview",
        "a": "Doing a cold plunge right after a hard run leaves me shivering with a shaky, uneven voice for a good while afterward, until my core temperature settles back down.",
        "b": "I have a Monday morning job interview where I need a steady, confident speaking voice through the whole conversation.",
        "proposal": "A friend talks me into a cold plunge right after Sunday's long run, the evening before Monday's interview.",
        "query": "Based only on these records, should the cold plunge right after Sunday's long run be flagged as a fit risk for this user?",
        "c": "The cold plunge right after Sunday's long run should be flagged as a fit risk because the shivering, shaky voice it causes would conflict with Monday's interview needing a steady, confident speaking voice.",
        "broken": "I have a Monday morning interview slot, but it's been switched to a written take-home assignment instead of a live conversation.",
    },
    {
        "slug": "stair_climb_challenge_before_childcare_shift",
        "a": "A stair-climb challenge leaves my legs wobbly and my balance off enough that I have to hold the railing going down stairs the rest of that day.",
        "b": "I have a Tuesday morning shift watching my toddler nephew where I need steady footing to keep up with him on the playground.",
        "proposal": "A charity event invites me to a 50-flight stair-climb challenge Monday evening, the night before Tuesday's childcare shift.",
        "query": "Based only on these records, should the 50-flight stair-climb challenge Monday evening be flagged as a fit risk for this user?",
        "c": "The 50-flight stair-climb challenge Monday evening should be flagged as a fit risk because the wobbly legs and balance trouble it causes would conflict with Tuesday's shift needing steady footing to keep up with a toddler.",
        "broken": "I have Tuesday morning blocked for my nephew, but his parents ended up keeping him home sick, so there's no playground time to keep up with.",
    },
    {
        "slug": "heavy_kettlebell_swings_before_blood_glucose_panel",
        "a": "A heavy kettlebell swing session leaves my blood sugar crashing and my hands shaky for an hour or two afterward until I eat something.",
        "b": "I have a Thursday morning glucose panel where I need to arrive in a normal, unstressed metabolic state, not right after a crash.",
        "proposal": "My trainer programs a high-volume kettlebell swing finisher Wednesday evening, the night before Thursday's glucose panel.",
        "query": "Based only on these records, should the high-volume kettlebell swing finisher Wednesday evening be flagged as a fit risk for this user?",
        "c": "The high-volume kettlebell swing finisher Wednesday evening should be flagged as a fit risk because the blood sugar crash it causes would conflict with Thursday's panel needing a normal, unstressed metabolic state.",
        "broken": "I have a Thursday morning lab visit, but they moved it to a simple prescription pickup instead of an actual blood panel this time.",
    },
    {
        "slug": "rowing_erg_test_before_piano_exam",
        "a": "A max-effort rowing erg test leaves my forearms and fingers cramping up for a good while after I'm done.",
        "b": "I have a Friday afternoon piano exam where I need full, uncramped finger control for a fast, technical piece.",
        "proposal": "My rowing coach schedules a max-effort 2k erg test Thursday, the day before Friday's piano exam.",
        "query": "Based only on these records, should the max-effort 2k erg test Thursday be flagged as a fit risk for this user?",
        "c": "The max-effort 2k erg test Thursday should be flagged as a fit risk because the finger and forearm cramping it causes would conflict with Friday's exam needing full, uncramped finger control.",
        "broken": "I have a Friday afternoon slot with my piano examiner, but it turned into a scheduling-only meeting to pick next semester's repertoire, no playing involved.",
    },
    {
        "slug": "mountain_bike_descent_before_photography_shoot",
        "a": "A rough mountain bike descent leaves my hands vibrating and unsteady for a couple of hours after I get off the bike.",
        "b": "I have a Saturday morning macro-photography shoot where I need dead-steady hands to hold focus on tiny details.",
        "proposal": "A riding group invites me to an extra-rough downhill trail Friday evening, the night before Saturday's photo shoot.",
        "query": "Based only on these records, should the extra-rough downhill trail Friday evening be flagged as a fit risk for this user?",
        "c": "The extra-rough downhill trail Friday evening should be flagged as a fit risk because the hand vibration and unsteadiness it causes would conflict with Saturday's shoot needing dead-steady hands for macro focus.",
        "broken": "I have a Saturday morning session booked with the photo client, but they asked to reschedule to editing existing photos instead of a new shoot.",
    },
    {
        "slug": "heat_chamber_training_before_courtroom_testimony",
        "a": "Training in the heat chamber leaves me flushed and light-headed with a racing pulse for hours after I step out.",
        "b": "I have a Tuesday morning courtroom testimony where I need to stay visibly calm and composed under cross-examination.",
        "proposal": "My coach schedules an extended heat chamber session Monday evening, the night before Tuesday's testimony.",
        "query": "Based only on these records, should the extended heat chamber session Monday evening be flagged as a fit risk for this user?",
        "c": "The extended heat chamber session Monday evening should be flagged as a fit risk because the flushed, light-headed, racing-pulse state it causes would conflict with Tuesday's testimony needing visible calm and composure.",
        "broken": "I have a Tuesday morning court date, but the hearing got postponed to next month, so there's no testimony to give this week.",
    },
    {
        "slug": "plyometric_box_jumps_before_ballet_audition",
        "a": "A heavy plyometric box-jump session leaves my calves so tight that my jumps look noticeably stiffer and less controlled the next day.",
        "b": "I have a Wednesday morning ballet audition where the choreographer is specifically watching for clean, controlled jump landings.",
        "proposal": "My trainer adds an extra plyometric box-jump block Tuesday evening, the night before Wednesday's audition.",
        "query": "Based only on these records, should the extra plyometric box-jump block Tuesday evening be flagged as a fit risk for this user?",
        "c": "The extra plyometric box-jump block Tuesday evening should be flagged as a fit risk because the calf tightness it causes would conflict with Wednesday's audition needing clean, controlled jump landings.",
        "broken": "I have a Wednesday morning slot at the studio, but the audition got restructured to barre work only this round, with no jumps evaluated.",
    },
    {
        "slug": "sauna_session_before_surgical_hygienist_exam",
        "a": "A long sauna session leaves my hands slightly swollen and less dexterous for an hour or two after I get out.",
        "b": "I have a Thursday morning dental hygienist licensing exam where I need full finger dexterity to handle fine instruments precisely.",
        "proposal": "The gym is hosting an extended sauna social Wednesday evening, the night before Thursday's licensing exam.",
        "query": "Based only on these records, should the extended sauna social Wednesday evening be flagged as a fit risk for this user?",
        "c": "The extended sauna social Wednesday evening should be flagged as a fit risk because the hand swelling and reduced dexterity it causes would conflict with Thursday's exam needing precise instrument handling.",
        "broken": "I have a Thursday morning exam slot reserved, but the licensing board pushed the practical portion back a week, leaving only a written test this week.",
    },
    {
        "slug": "missed_blood_thinner_dose_before_dental_extraction",
        "a": "Whenever I skip my evening blood-thinner dose, my gums bleed noticeably longer than usual if I so much as floss the next day.",
        "b": "I have a Tuesday morning dental extraction where the oral surgeon needs my clotting to be normal going in.",
        "proposal": "A back-to-back travel day this week means the user is considering skipping tonight's blood-thinner dose to avoid carrying liquids through security.",
        "query": "Based only on these records, should skipping tonight's blood-thinner dose be flagged as a fit risk for this user?",
        "c": "Skipping tonight's blood-thinner dose should be flagged as a fit risk because missed doses lead to longer bleeding, right when Tuesday's dental extraction needs normal clotting.",
        "broken": "I have a Tuesday morning dental cleaning that got downgraded to just a checkup with no procedure planned.",
    },
    {
        "slug": "grapefruit_juice_statin_before_liver_panel",
        "a": "Whenever I have grapefruit juice with my statin, I get unusual muscle soreness in my legs that lasts into the next day.",
        "b": "I have a Thursday morning liver-function panel where the lab wants my routine unchanged from the past week.",
        "proposal": "A brunch spot this week features fresh grapefruit juice alongside the usual morning dose.",
        "query": "Based only on these records, should having grapefruit juice with this week's dose be flagged as a fit risk for this user?",
        "c": "Having grapefruit juice with this week's dose should be flagged as a fit risk because it triggers muscle soreness right when Thursday's liver panel needs an unchanged routine.",
        "broken": "I have a Thursday morning liver panel that got rescheduled to next month while my dosage is being reviewed.",
    },
    {
        "slug": "insulin_site_rotation_lump_before_suit_fitting",
        "a": "When I forget to rotate my insulin injection sites, I get a tender lump that makes tight clothing uncomfortable against that spot for a couple of days.",
        "b": "I have a Friday afternoon suit fitting where the tailor needs to pin the fabric snugly against my torso.",
        "proposal": "A busy week has the user reaching for the same easy injection spot again instead of rotating.",
        "query": "Based only on these records, should reusing the same injection site again this week be flagged as a fit risk for this user?",
        "c": "Reusing the same injection site again this week should be flagged as a fit risk because it causes a tender lump right when Friday's suit fitting needs snug fabric against that spot.",
        "broken": "I have a Friday afternoon fitting that got moved to loose, unstructured clothing with no pinning needed.",
    },
    {
        "slug": "late_thyroid_refill_fatigue_before_early_flight",
        "a": "When my thyroid medication refill runs a few days late, I get noticeably more fatigued and slower to get moving in the mornings.",
        "b": "I have a Wednesday 6am flight where I need to be alert enough to navigate security and gate changes on my own.",
        "proposal": "This week's refill is running behind again with the pharmacy citing a supply delay.",
        "query": "Based only on these records, should this week's delayed thyroid refill be flagged as a fit risk for this user?",
        "c": "This week's delayed thyroid refill should be flagged as a fit risk because it brings on fatigue right when Wednesday's early flight needs the user alert enough to navigate alone.",
        "broken": "I have a Wednesday flight that got pushed to a relaxed 2pm departure with plenty of time to spare.",
    },
    {
        "slug": "dairy_with_antibiotic_before_repeat_culture",
        "a": "Whenever I take this antibiotic with milk or cheese, the infection symptoms seem to linger longer than they should by the next check.",
        "b": "I have a Monday morning repeat culture swab where the clinic needs to see real improvement from the current course.",
        "proposal": "A weekend of easy dairy-heavy meals this week has been landing right around dose times.",
        "query": "Based only on these records, should this week's dairy-heavy meals near dose times be flagged as a fit risk for this user?",
        "c": "This week's dairy-heavy meals near dose times should be flagged as a fit risk because they blunt the antibiotic's effect right when Monday's repeat culture needs to show real improvement.",
        "broken": "I have a Monday check-in that's just a phone call this time, with no swab or sample needed.",
    },
    {
        "slug": "nsaid_overuse_before_kidney_function_draw",
        "a": "When I lean on ibuprofen for more than a couple of days straight, my urine output noticeably drops and I feel puffier than usual.",
        "b": "I have a Tuesday morning blood draw where the doctor needs an accurate kidney-function reading.",
        "proposal": "A nagging headache has the user reaching for ibuprofen again for the third day in a row this week.",
        "query": "Based only on these records, should this third straight day of ibuprofen be flagged as a fit risk for this user?",
        "c": "This third straight day of ibuprofen should be flagged as a fit risk because it drops urine output and causes puffiness right when Tuesday's blood draw needs an accurate kidney-function reading.",
        "broken": "I have a Tuesday appointment that turned out to be just picking up paperwork, with no blood draw involved.",
    },
    {
        "slug": "steroid_taper_skip_before_portrait_session",
        "a": "If I skip a step of my steroid taper, my face and hands noticeably puff up with rebound inflammation for a day or two.",
        "b": "I have a Saturday afternoon portrait session where the photographer needs my face to look like it usually does.",
        "proposal": "A hectic schedule this week has the user considering skipping tomorrow's taper step to catch up on sleep instead.",
        "query": "Based only on these records, should skipping tomorrow's taper step be flagged as a fit risk for this user?",
        "c": "Skipping tomorrow's taper step should be flagged as a fit risk because it causes rebound facial puffing right when Saturday's portrait session needs the user's usual appearance.",
        "broken": "I have a Saturday session that got rescheduled to a phone consultation instead of an in-person portrait.",
    },
    {
        "slug": "antihistamine_drowsiness_before_evening_driving_test",
        "a": "The antihistamine I take for allergy flare-ups leaves me noticeably drowsy and slower to react for several hours after I take it.",
        "b": "The examiner grading Thursday evening's driving test is specifically watching how fast I react at each intersection.",
        "proposal": "Pollen counts this week have the user reaching for the same antihistamine right before Thursday evening.",
        "query": "Based only on these records, should taking the antihistamine right before Thursday evening be flagged as a fit risk for this user?",
        "c": "Taking the antihistamine right before Thursday evening should be flagged as a fit risk because it causes drowsy, slow reactions right when the driving test needs sharp reflexes.",
        "broken": "I have a Thursday evening test that turned into a written-only retake with no actual driving involved.",
    },
    {
        "slug": "sleep_aid_grogginess_before_early_client_call",
        "a": "Whenever I take my prescribed sleep aid, I wake up groggy and slow to form sentences for the first hour or two of the morning.",
        "b": "I have a Monday 7am client call where I need to speak clearly and think on my feet from the first minute.",
        "proposal": "A rough week of insomnia has the user planning to take the sleep aid again the night before Monday's call.",
        "query": "Based only on these records, should taking the sleep aid the night before Monday's call be flagged as a fit risk for this user?",
        "c": "Taking the sleep aid the night before Monday's call should be flagged as a fit risk because it leaves the user groggy right when the 7am client call needs clear, quick thinking.",
        "broken": "I have a Monday call that got moved to the afternoon with a teammate covering the opening minutes.",
    },
    {
        "slug": "beta_blocker_timing_before_fitness_assessment",
        "a": "When I take my beta-blocker close to a workout, my heart rate stays noticeably lower than expected and I feel unusually winded for the effort.",
        "b": "I have a Wednesday morning fitness assessment where the trainer needs my heart-rate response to reflect my real effort level.",
        "proposal": "This week's dosing schedule has the next dose landing just an hour before Wednesday's session.",
        "query": "Based only on these records, should this week's dose timing before Wednesday's session be flagged as a fit risk for this user?",
        "c": "This week's dose timing before Wednesday's session should be flagged as a fit risk because it blunts the heart-rate response right when the fitness assessment needs it to reflect real effort.",
        "broken": "I have a Wednesday session that got swapped for a flexibility-only class with no heart-rate tracking involved.",
    },
    {
        "slug": "glp1_injection_nausea_before_tasting_event",
        "a": "For about a day after my GLP-1 injection, I get intermittent nausea that makes it hard to enjoy or even want food.",
        "b": "I have a Sunday afternoon food-tasting event where I'm expected to sample and give feedback on a dozen dishes.",
        "proposal": "This week's injection is scheduled for Saturday, the day before Sunday's tasting.",
        "query": "Based only on these records, should this week's Saturday injection timing be flagged as a fit risk for Sunday's tasting event?",
        "c": "This week's Saturday injection timing should be flagged as a fit risk for Sunday's tasting event because the post-injection nausea would land right when the user needs to sample a dozen dishes.",
        "broken": "I have a Sunday afternoon that turned into a written recipe review from home, with no actual tasting required.",
    },
    {
        "slug": "antidepressant_dose_change_gi_upset_before_public_talk",
        "a": "Right after my antidepressant dose was adjusted, I get noticeable stomach upset and need to be near a bathroom for the first several days.",
        "b": "I have a Friday afternoon public talk where I need to stand at a podium for forty minutes without a break.",
        "proposal": "This week's dose adjustment just started, with the GI symptoms already showing up on schedule.",
        "query": "Based only on these records, should this week's fresh dose adjustment be flagged as a fit risk for this user?",
        "c": "This week's fresh dose adjustment should be flagged as a fit risk because it brings on stomach upset right when Friday's talk needs forty uninterrupted minutes at the podium.",
        "broken": "I have a Friday session that got turned into a pre-recorded video instead of a live podium talk.",
    },
    {
        "slug": "diuretic_timing_before_long_certification_exam",
        "a": "When I take my diuretic in the morning instead of the night before, I need the bathroom every hour or so for the first half of the day.",
        "b": "I have a Saturday morning certification exam that runs three hours with no bathroom breaks allowed once it starts.",
        "proposal": "A rushed morning this week has the user planning to take the diuretic right before heading out Saturday.",
        "query": "Based only on these records, should taking the diuretic right before Saturday's exam be flagged as a fit risk for this user?",
        "c": "Taking the diuretic right before Saturday's exam should be flagged as a fit risk because it causes frequent bathroom urges right when the three-hour exam allows no breaks.",
        "broken": "I have a Saturday exam that got moved to an open-book take-home format with no fixed sitting.",
    },
    {
        "slug": "missed_evening_bp_dose_headache_before_road_test",
        "a": "If I miss my evening blood-pressure dose, I wake up with a dull headache that makes it hard to focus on anything detailed for a couple of hours.",
        "b": "I have a Tuesday morning road test where the examiner needs me focused on details like mirror checks and signage the whole time.",
        "proposal": "A late night out this week has the user likely to miss tonight's evening dose.",
        "query": "Based only on these records, should missing tonight's evening dose be flagged as a fit risk for this user?",
        "c": "Missing tonight's evening dose should be flagged as a fit risk because it causes a focus-dulling headache right when Tuesday's road test needs sustained attention to detail.",
        "broken": "I have a Tuesday appointment that turned out to be just renewing my license by mail, with no actual test.",
    },
    {
        "slug": "immunosuppressant_fatigue_before_hosting_dinner",
        "a": "In the days right after my immunosuppressant infusion, I get a heavy fatigue that makes standing and cooking for long stretches genuinely hard.",
        "b": "I have a Saturday evening dinner I'm hosting for eight people, which means hours of standing, cooking, and cleaning up.",
        "proposal": "This week's infusion is scheduled for Thursday, two days before Saturday's dinner.",
        "query": "Based only on these records, should this week's Thursday infusion timing be flagged as a fit risk for hosting Saturday's dinner?",
        "c": "This week's Thursday infusion timing should be flagged as a fit risk for hosting Saturday's dinner because the post-infusion fatigue would land right when hours of standing and cooking are needed.",
        "broken": "I have a Saturday evening that turned into ordering takeout with guests bringing their own plates, no cooking involved.",
    },
    {
        "slug": "missed_seizure_med_dose_before_lake_swim",
        "a": "When I miss a dose of my anti-seizure medication, I get noticeably light-headed and unsteady on my feet for the following day.",
        "b": "I have a Sunday afternoon lake swim planned where I'd be in open water without a lifeguard nearby.",
        "proposal": "A hectic travel day this week has the user at real risk of missing this evening's dose.",
        "query": "Based only on these records, should missing this evening's dose be flagged as a fit risk for this user?",
        "c": "Missing this evening's dose should be flagged as a fit risk because it causes light-headedness and unsteadiness right when Sunday's open-water swim offers no lifeguard nearby.",
        "broken": "I have a Sunday afternoon that turned into a shallow, supervised pool session with a lifeguard right on deck.",
    },
    {
        "slug": "new_medication_dizziness_before_ladder_task",
        "a": "Since starting this new medication, I get a wave of dizziness for the first hour or two after each dose, especially when I stand up quickly.",
        "b": "I have a Wednesday afternoon task replacing gutter guards, which means being up on a ladder for a good chunk of the day.",
        "proposal": "This week's dose falls right before Wednesday afternoon's ladder work.",
        "query": "Based only on these records, should this week's dose timing before Wednesday's ladder task be flagged as a fit risk for this user?",
        "c": "This week's dose timing before Wednesday's ladder task should be flagged as a fit risk because the post-dose dizziness would hit right when the user needs to be steady up on a ladder.",
        "broken": "I have a Wednesday afternoon that turned into ground-level yard work with the ladder task pushed to a professional crew.",
    },
    {
        "slug": "gabapentin_gap_before_salary_negotiation",
        "a": "Whenever I run a few days short on my gabapentin refill, I get jittery and short-tempered, and it's hard to stay composed in conversations.",
        "b": "I have a Thursday afternoon salary negotiation where I need to stay calm and composed under pushback.",
        "proposal": "This week's refill is running three days behind with the pharmacy still processing the order.",
        "query": "Based only on these records, should this week's refill gap be flagged as a fit risk for this user?",
        "c": "This week's refill gap should be flagged as a fit risk because it brings on jitteriness and short temper right when Thursday's negotiation needs the user to stay calm under pushback.",
        "broken": "I have a Thursday afternoon that turned into a written offer exchanged by email, with no live negotiation conversation.",
    },
    {
        "slug": "loud_party_before_grief_support_group",
        "a": "After a loud, crowded party I feel emotionally raw and need a full day of quiet before I can be present with anyone else's feelings.",
        "b": "I facilitate a Sunday morning grief support group where I need to hold space calmly for other people's loss.",
        "proposal": "A neighbor invites me to a loud housewarming party Saturday night with a packed guest list.",
        "query": "Based only on these records, should the loud housewarming party be flagged as a fit risk for this user?",
        "c": "The loud housewarming party should be flagged as a fit risk because it would leave me too emotionally raw right when Sunday's grief support group needs me to hold calm space for others.",
        "broken": "I have a Sunday morning grief support group session, but a co-facilitator is covering it solo this week so I only need to observe.",
    },
    {
        "slug": "conflict_call_before_mediation_session",
        "a": "After a tense confrontational phone call, I stay keyed up and quick to snap for most of the next day.",
        "b": "I have a Sunday afternoon mediation session where I need to stay even-tempered while two other people argue in front of me.",
        "proposal": "My landlord wants to have a heated call Saturday evening about a disputed repair charge.",
        "query": "Based only on these records, should the heated landlord call be flagged as a fit risk for this user?",
        "c": "The heated landlord call should be flagged as a fit risk because it would leave me keyed up and quick to snap right when Sunday's mediation session needs an even temper.",
        "broken": "My landlord wants to send a written summary of the disputed repair charge Saturday evening instead of a call.",
    },
    {
        "slug": "overstimulating_expo_before_solo_parenting_day",
        "a": "After a long day at a crowded, loud expo, I get overstimulated and need total quiet to reset, otherwise I'm irritable with everyone around me.",
        "b": "I have full solo parenting duty Sunday, including a birthday party with a dozen loud kids at my house.",
        "proposal": "A colleague invites me to an all-day trade show Saturday with nonstop noise and crowds.",
        "query": "Based only on these records, should the all-day trade show be flagged as a fit risk for this user?",
        "c": "The all-day trade show should be flagged as a fit risk because the overstimulation it causes would leave me irritable right when Sunday's loud solo-parenting day needs patience.",
        "broken": "A colleague invites me to a quiet half-day trade show Saturday held in a small, low-traffic room.",
    },
    {
        "slug": "doomscrolling_before_public_speaking",
        "a": "Late-night doomscrolling spikes my anxiety and leaves my hands shaky and my thoughts scattered well into the next morning.",
        "b": "I'm giving a Sunday morning keynote where I need steady hands for slides and a clear head for audience questions.",
        "proposal": "A stressful news cycle Saturday night keeps pulling me into doomscrolling for hours.",
        "query": "Based only on these records, should Saturday night's doomscrolling spiral be flagged as a fit risk for this user?",
        "c": "Saturday night's doomscrolling spiral should be flagged as a fit risk because the anxiety spike leaves my hands shaky and thoughts scattered right when Sunday's keynote needs steady composure.",
        "broken": "A stressful news cycle Saturday night is happening, but I've already muted every news app and my phone is in another room.",
    },
    {
        "slug": "unresolved_argument_before_custody_exchange",
        "a": "When I go to bed after an unresolved argument with someone close to me, I ruminate all night and show up foggy and short-tempered the next day.",
        "b": "I have a Sunday morning custody exchange where I need to be calm and composed in front of my child.",
        "proposal": "My sibling wants to hash out an old unresolved family disagreement by phone Saturday night.",
        "query": "Based only on these records, should Saturday night's unresolved family call be flagged as a fit risk for this user?",
        "c": "Saturday night's unresolved family call should be flagged as a fit risk because the rumination it triggers would leave me foggy and short-tempered right when Sunday's custody exchange needs calm composure.",
        "broken": "My sibling wants to reschedule that old family disagreement conversation to sometime next month instead of this weekend.",
    },
    {
        "slug": "back_to_back_video_calls_before_eulogy",
        "a": "A day stacked with back-to-back video calls leaves my voice tired and my emotions oddly numb by evening, and it takes a full night's rest to feel anything clearly again.",
        "b": "I'm delivering a eulogy at a Sunday morning memorial service where I need to access real feeling, not a numbed-out read-through.",
        "proposal": "Work schedules a Saturday full of back-to-back video calls with no breaks between them.",
        "query": "Based only on these records, should Saturday's back-to-back video calls be flagged as a fit risk for this user?",
        "c": "Saturday's back-to-back video calls should be flagged as a fit risk because the emotional numbness they cause would undercut the real feeling Sunday's eulogy needs.",
        "broken": "Work schedules a light Saturday with just one short video call and the rest of the day open.",
    },
    {
        "slug": "crowded_reunion_before_therapy_intake",
        "a": "A crowded reunion with lots of small talk leaves me emotionally guarded and it takes a day before I can open up about anything real again.",
        "b": "I have a Sunday morning intake session with a new therapist where I need to be open about what's actually going on.",
        "proposal": "Former classmates invite me to a big, crowded reunion mixer Saturday night.",
        "query": "Based only on these records, should the crowded reunion mixer be flagged as a fit risk for this user?",
        "c": "The crowded reunion mixer should be flagged as a fit risk because the emotional guardedness it triggers would work against the openness Sunday's therapy intake needs.",
        "broken": "Former classmates invite me to a small dinner Saturday night with just three close friends from that era.",
    },
    {
        "slug": "roommate_conflict_before_panel_interview",
        "a": "After a loud conflict with a roommate, I stay anxious and second-guess every word I say for most of the next day.",
        "b": "I have a Sunday morning panel interview where I need to speak confidently and not second-guess myself in front of three interviewers.",
        "proposal": "A tense dispute over shared chores with my roommate is likely to boil over into a loud argument Saturday.",
        "query": "Based only on these records, should Saturday's loud roommate conflict be flagged as a fit risk for this user?",
        "c": "Saturday's loud roommate conflict should be flagged as a fit risk because the anxious self-doubt it triggers would undercut the confidence Sunday's panel interview needs.",
        "broken": "A tense dispute over shared chores with my roommate got resolved calmly over text earlier this week, so nothing is left to boil over Saturday.",
    },
    {
        "slug": "overnight_er_visit_before_crisis_line_shift",
        "a": "After a stressful overnight ER visit, I'm running on adrenaline and can't regulate my own emotions well for a full day afterward.",
        "b": "I'm scheduled for a Sunday evening crisis-line volunteer shift where I need steady emotional regulation to support callers in distress.",
        "proposal": "A friend needs me to accompany them to the ER Saturday night for a scary but non-life-threatening issue.",
        "query": "Based only on these records, should Saturday night's ER visit be flagged as a fit risk for this user?",
        "c": "Saturday night's ER visit should be flagged as a fit risk because the adrenaline crash afterward would undercut the emotional regulation Sunday's crisis-line shift needs.",
        "broken": "A friend needs a ride to a routine Saturday-afternoon check-up appointment, not an ER visit.",
    },
    {
        "slug": "social_media_pileon_before_wedding_toast",
        "a": "Getting piled on in a social media argument leaves me rattled and tearful on and off for the rest of the day.",
        "b": "I'm giving a toast at a Sunday afternoon wedding where I need to stay composed in front of the whole room.",
        "proposal": "A heated public thread I posted in is attracting a pile-on of replies Saturday.",
        "query": "Based only on these records, should Saturday's social-media pile-on be flagged as a fit risk for this user?",
        "c": "Saturday's social-media pile-on should be flagged as a fit risk because the rattled, tearful aftermath would undercut the composure Sunday's wedding toast needs.",
        "broken": "A heated public thread I posted in got quietly deleted by the platform Saturday before anyone could pile on.",
    },
    {
        "slug": "intense_therapy_session_before_negotiation",
        "a": "After an intense therapy session that surfaces old material, I feel emotionally raw and less able to hold firm boundaries for the rest of that day.",
        "b": "I have a Sunday morning salary negotiation where I need to hold firm boundaries and not cave under pressure.",
        "proposal": "My therapist suggests scheduling an extra, deeper session Saturday to work through some heavier material.",
        "query": "Based only on these records, should Saturday's deeper therapy session be flagged as a fit risk for this user?",
        "c": "Saturday's deeper therapy session should be flagged as a fit risk because the emotional rawness it leaves would undercut the firm boundaries Sunday's salary negotiation needs.",
        "broken": "My therapist suggests a light Saturday check-in focused only on scheduling logistics, no deeper material.",
    },
    {
        "slug": "family_estate_call_before_closing_pitch",
        "a": "Calls about our family estate leave me distracted and emotionally heavy, and I have trouble focusing on anything else until the next day passes.",
        "b": "I'm giving a Sunday morning closing pitch to a client where I need sharp, undistracted focus.",
        "proposal": "My siblings want to have a Saturday call to hash out details of our late parent's estate.",
        "query": "Based only on these records, should Saturday's family estate call be flagged as a fit risk for this user?",
        "c": "Saturday's family estate call should be flagged as a fit risk because the distracted, emotionally heavy aftermath would undercut the sharp focus Sunday's closing pitch needs.",
        "broken": "My siblings want to push the estate call to sometime after this month, once the paperwork is actually ready.",
    },
    {
        "slug": "public_criticism_before_recital",
        "a": "Getting publicly criticized in front of others leaves my confidence shaken and my hands unsteady for the rest of the day.",
        "b": "I have a Sunday afternoon piano recital where I need steady hands and confidence to perform in front of an audience.",
        "proposal": "My manager is planning to give me critical feedback in front of the whole team Saturday.",
        "query": "Based only on these records, should Saturday's public critical feedback be flagged as a fit risk for this user?",
        "c": "Saturday's public critical feedback should be flagged as a fit risk because the shaken confidence and unsteady hands it causes would undermine Sunday's recital performance.",
        "broken": "My manager is planning to give me written feedback privately by email Saturday instead of in front of the team.",
    },
    {
        "slug": "breakup_conversation_before_officiating_ceremony",
        "a": "After an emotionally heavy breakup conversation, I feel hollow and have trouble projecting warmth to others for about a day.",
        "b": "I'm officiating a Sunday morning naming ceremony where I need to project genuine warmth to the family.",
        "proposal": "My partner wants to have the breakup conversation Saturday evening, the one we've both been avoiding.",
        "query": "Based only on these records, should Saturday evening's breakup conversation be flagged as a fit risk for this user?",
        "c": "Saturday evening's breakup conversation should be flagged as a fit risk because the hollow aftermath would undercut the warmth Sunday's naming ceremony needs me to project.",
        "broken": "My partner wants to have a low-stakes conversation Saturday evening about picking a new couch, nothing emotionally heavy.",
    },
    {
        "slug": "sensory_overload_shift_before_exposure_session",
        "a": "A loud, chaotic retail shift leaves me sensorially overloaded and jumpy at sudden sounds for the rest of that evening and into the next morning.",
        "b": "I have a Sunday morning exposure-therapy session where I need to stay grounded through some deliberately uncomfortable moments.",
        "proposal": "My manager schedules me for a chaotic Saturday closing shift during a store-wide sale.",
        "query": "Based only on these records, should Saturday's chaotic closing shift be flagged as a fit risk for this user?",
        "c": "Saturday's chaotic closing shift should be flagged as a fit risk because the sensory overload and jumpiness it causes would undercut the groundedness Sunday's exposure session needs.",
        "broken": "My manager schedules me for a quiet Saturday morning shift restocking shelves before the store opens.",
    },
    {
        "slug": "friend_crisis_support_before_peer_group_facilitation",
        "a": "Spending hours supporting a friend through their own crisis leaves me emotionally drained with nothing left over for anyone else the next day.",
        "b": "I lead a Sunday morning peer-support meeting where I need emotional bandwidth left to actually listen to others.",
        "proposal": "A close friend is going through a crisis and wants me on the phone with them most of Saturday.",
        "query": "Based only on these records, should Saturday's hours of crisis support be flagged as a fit risk for this user?",
        "c": "Saturday's hours of crisis support should be flagged as a fit risk because the emotional drain it causes would leave nothing for Sunday's peer-support meeting to draw on when listening to others.",
        "broken": "A close friend just wants a quick Saturday check-in text, not hours of crisis support.",
    },
    {
        "slug": "performance_review_anxiety_before_first_date",
        "a": "In the hours after an anxiety-provoking performance review, my mind races and I struggle to be present in conversation for the rest of the day.",
        "b": "I have a first date Sunday evening where I need to be present and relaxed enough to actually connect with someone new.",
        "proposal": "My manager moves my performance review to Saturday, the same day I've been looking forward to.",
        "query": "Based only on these records, should Saturday's performance review be flagged as a fit risk for this user?",
        "c": "Saturday's performance review should be flagged as a fit risk because the racing-mind anxiety it triggers would undercut the presence Sunday's first date needs.",
        "broken": "My manager moves my performance review to a quick, informal Saturday check-in rated as no concerns, nothing to discuss.",
    },
    {
        "slug": "moving_day_exhaustion_before_open_house",
        "a": "A full day of moving boxes and logistics leaves me physically wiped and emotionally short-fused for the rest of that evening and into the next morning.",
        "b": "I'm hosting a Sunday evening open house for my small business where I need warm energy to greet everyone at the door.",
        "proposal": "Friends need my help with a full Saturday of moving apartments, boxes and all.",
        "query": "Based only on these records, should Saturday's full day of apartment-moving be flagged as a fit risk for this user?",
        "c": "Saturday's full day of apartment-moving should be flagged as a fit risk because the physical and emotional depletion it causes would undercut the warm energy Sunday's open house needs.",
        "broken": "Friends just need a quick Saturday hand carrying a couch up one flight of stairs, not a full day of moving.",
    },
    {
        "slug": "heavy_lifting_before_shoulder_impingement_test",
        "a": "Whenever I do heavy overhead lifting at the gym, my right shoulder catches and aches for about a day, especially raising my arm above head height.",
        "b": "I have a Tuesday morning shoulder impingement test where the therapist needs me to raise my arm through a full pain-free range of motion.",
        "proposal": "A friend asks me to help hoist heavy moving boxes onto a truck bed on Monday evening.",
        "query": "Based only on these records, should helping hoist heavy moving boxes onto a truck bed on Monday evening be flagged as a fit risk for this user?",
        "c": "Helping hoist heavy moving boxes onto a truck bed on Monday evening should be flagged as a fit risk because the overhead-lifting pattern that inflames this user's shoulder would conflict with Tuesday's full-range impingement test.",
        "broken": "I have a Tuesday morning shoulder appointment, but it's just a paperwork consent form this time \u2014 no range-of-motion testing is done.",
    },
    {
        "slug": "prolonged_kneeling_before_knee_brace_fitting",
        "a": "Any time I kneel on a hard floor for more than twenty minutes, my kneecap aches and swells slightly by evening.",
        "b": "I have a Wednesday morning knee brace fitting where the orthotist needs to measure my knee without any swelling present.",
        "proposal": "A neighbor asks me to help regrout bathroom tile, which means kneeling on the hard floor for a couple of hours on Tuesday.",
        "query": "Based only on these records, should helping regrout bathroom tile on Tuesday be flagged as a fit risk for this user?",
        "c": "Helping regrout bathroom tile on Tuesday should be flagged as a fit risk because the prolonged-kneeling pattern that swells this user's kneecap would conflict with Wednesday's swelling-free brace fitting.",
        "broken": "I have a Wednesday morning brace-shop visit, but it's just to pick up a spare strap this time \u2014 no measurement is taken.",
    },
    {
        "slug": "repetitive_typing_before_wrist_nerve_conduction",
        "a": "After a day of heavy typing without breaks, my wrist tingles and goes slightly numb along my thumb and first two fingers by nightfall.",
        "b": "I have a Thursday morning nerve conduction study on my wrist where the technician needs my nerves at their baseline, unaggravated state.",
        "proposal": "My manager asks me to finish a large data-entry backlog in one uninterrupted sitting on Wednesday.",
        "query": "Based only on these records, should finishing the large data-entry backlog in one sitting on Wednesday be flagged as a fit risk for this user?",
        "c": "Finishing the large data-entry backlog in one uninterrupted sitting on Wednesday should be flagged as a fit risk because the heavy-typing pattern that numbs this user's wrist would conflict with Thursday's baseline nerve conduction study.",
        "broken": "I have a Thursday morning wrist appointment, but it's just to reschedule a future study this time \u2014 no nerve testing happens.",
    },
    {
        "slug": "new_running_shoes_before_gait_analysis",
        "a": "Whenever I break in a new pair of running shoes, my stride gets uneven and my hips ache slightly until the shoes are broken in, usually a few runs.",
        "b": "I have a Friday morning gait analysis where the specialist needs to record my normal, uncompensated walking pattern.",
        "proposal": "A running store offers me a free trial run in a brand-new shoe model on Thursday evening.",
        "query": "Based only on these records, should the free trial run in the brand-new shoe model on Thursday evening be flagged as a fit risk for this user?",
        "c": "The free trial run in the brand-new shoe model on Thursday evening should be flagged as a fit risk because the new-shoe break-in pattern that unevens this user's stride would conflict with Friday's normal-gait analysis.",
        "broken": "I have a Friday morning shoe-store appointment, but it's just to browse colors this time \u2014 no gait recording happens.",
    },
    {
        "slug": "heavy_backpack_commute_before_posture_screening",
        "a": "On days I carry my heaviest backpack on the long commute, my upper back and neck feel hunched and sore by the time I get home.",
        "b": "I have a Monday morning posture screening at work where the ergonomics consultant needs to observe my natural, unstrained posture.",
        "proposal": "A friend asks me to carry an extra bag of borrowed textbooks on my usual Sunday evening commute.",
        "query": "Based only on these records, should carrying the extra bag of borrowed textbooks on Sunday evening's commute be flagged as a fit risk for this user?",
        "c": "Carrying the extra bag of borrowed textbooks on Sunday evening's commute should be flagged as a fit risk because the heavy-backpack pattern that hunches this user's posture would conflict with Monday's natural-posture screening.",
        "broken": "I have a Monday morning ergonomics meeting, but it's just a scheduling email this time \u2014 no posture observation happens.",
    },
    {
        "slug": "barefoot_trail_running_before_plantar_fasciitis_checkup",
        "a": "Whenever I go barefoot trail running, the arch of my foot aches sharply by the next morning and I limp for the first several steps of the day.",
        "b": "I have a Tuesday morning plantar fasciitis checkup where the podiatrist needs to see my foot's normal, unaggravated arch.",
        "proposal": "A trail-running group invites me to a barefoot group run on Monday evening.",
        "query": "Based only on these records, should the barefoot group run on Monday evening be flagged as a fit risk for this user?",
        "c": "The barefoot group run on Monday evening should be flagged as a fit risk because the barefoot-running pattern that aches this user's arch would conflict with Tuesday's unaggravated-arch checkup.",
        "broken": "I have a Tuesday morning podiatry appointment, but it's just to pick up custom insoles this time \u2014 no arch exam happens.",
    },
    {
        "slug": "overhead_painting_before_rotator_cuff_ultrasound",
        "a": "Whenever I paint a ceiling or high wall, my shoulder feels weak and clicks when I try to lift anything overhead for the rest of that day and into the next.",
        "b": "I have a Wednesday morning rotator cuff ultrasound where the technician needs me to lift my arm smoothly overhead on command.",
        "proposal": "A neighbor asks me to help paint their two-story stairwell ceiling on Tuesday afternoon.",
        "query": "Based only on these records, should helping paint the two-story stairwell ceiling on Tuesday afternoon be flagged as a fit risk for this user?",
        "c": "Helping paint the two-story stairwell ceiling on Tuesday afternoon should be flagged as a fit risk because the overhead-painting pattern that weakens this user's shoulder would conflict with Wednesday's smooth-overhead-lift ultrasound.",
        "broken": "I have a Wednesday morning ultrasound appointment, but it's for my ankle this time \u2014 no overhead shoulder movement is needed.",
    },
    {
        "slug": "long_car_ride_before_hip_flexibility_test",
        "a": "After sitting in a car for more than two hours straight, my hips feel locked and stiff, and it takes real effort to get a normal stride back for the rest of the day.",
        "b": "I have a Thursday morning hip flexibility test where the physiotherapist needs my hips at their loosest, most flexible baseline.",
        "proposal": "A cousin asks me to drive four hours to help with a family move on Wednesday.",
        "query": "Based only on these records, should driving four hours to help with the family move on Wednesday be flagged as a fit risk for this user?",
        "c": "Driving four hours to help with the family move on Wednesday should be flagged as a fit risk because the long-sitting pattern that locks this user's hips would conflict with Thursday's loosest-baseline flexibility test.",
        "broken": "I have a Thursday morning appointment with the physiotherapist, but it's just to reorder a heating pad this time \u2014 no flexibility testing happens.",
    },
    {
        "slug": "heavy_grocery_carry_before_grip_strength_test",
        "a": "Whenever I carry heavy grocery bags for several blocks, my forearm cramps and my grip feels weak for the rest of the day and into the next morning.",
        "b": "My hand therapist is measuring grip strength Friday morning, and the reading only means something if my forearm hasn't already been worn out.",
        "proposal": "A roommate asks me to help carry a case of bottled water up four flights of stairs on Thursday evening.",
        "query": "Based only on these records, should helping carry the case of bottled water up four flights of stairs on Thursday evening be flagged as a fit risk for this user?",
        "c": "Helping carry the case of bottled water up four flights of stairs on Thursday evening should be flagged as a fit risk because the heavy-carrying pattern that cramps this user's forearm would conflict with Friday's unfatigued grip strength test.",
        "broken": "I have a Friday morning hand-therapy appointment, but it's just an insurance form this time \u2014 no grip testing happens.",
    },
    {
        "slug": "high_heels_shift_before_ankle_stability_exam",
        "a": "After a full shift standing in heels, my ankle feels wobbly and slightly swollen, and I catch myself rolling it on uneven ground more easily the next day.",
        "b": "I have a Monday morning ankle stability exam where the doctor needs my ankle at its normal, unswollen baseline.",
        "proposal": "My manager asks me to cover an extra evening shift in dress shoes on Sunday.",
        "query": "Based only on these records, should covering the extra evening shift in dress shoes on Sunday be flagged as a fit risk for this user?",
        "c": "Covering the extra evening shift in dress shoes on Sunday should be flagged as a fit risk because the standing-in-heels pattern that swells this user's ankle would conflict with Monday's unswollen-baseline stability exam.",
        "broken": "I have a Monday morning ankle appointment, but it's just to pick up a compression sleeve this time \u2014 no stability exam happens.",
    },
    {
        "slug": "heavy_backpack_hiking_before_spine_xray",
        "a": "Whenever I hike with a fully loaded backpack, my lower back tightens into a dull ache that lingers into the next day and makes bending over uncomfortable.",
        "b": "I have a Tuesday morning spine X-ray where the technician needs me to stand fully upright without any guarding or favoring one side.",
        "proposal": "A hiking club invites me on a Monday overnight backpacking trip with a full-weight pack.",
        "query": "Based only on these records, should the Monday overnight backpacking trip with a full-weight pack be flagged as a fit risk for this user?",
        "c": "The Monday overnight backpacking trip with a full-weight pack should be flagged as a fit risk because the loaded-hiking pattern that tightens this user's lower back would conflict with Tuesday's fully-upright spine X-ray.",
        "broken": "I have a Tuesday morning spine appointment, but it's just to review old X-ray films this time \u2014 no new imaging is taken.",
    },
    {
        "slug": "cold_plunge_before_muscle_biopsy",
        "a": "Whenever I do a cold plunge, my calf muscles seize up and stay tight and sore for about a day afterward.",
        "b": "I have a Wednesday morning muscle biopsy on my calf where the surgeon needs the muscle relaxed and at its normal resting tone.",
        "proposal": "A friend invites me to try their new cold-plunge tub on Tuesday evening.",
        "query": "Based only on these records, should trying the friend's new cold-plunge tub on Tuesday evening be flagged as a fit risk for this user?",
        "c": "Trying the friend's new cold-plunge tub on Tuesday evening should be flagged as a fit risk because the cold-plunge pattern that seizes this user's calf would conflict with Wednesday's relaxed-muscle biopsy.",
        "broken": "I have a Wednesday morning appointment with the surgeon, but it's just a pre-op paperwork review this time \u2014 no biopsy is performed.",
    },
    {
        "slug": "heavy_squat_session_before_knee_replacement_followup",
        "a": "After a heavy squat session at the gym, my reconstructed knee swells and stiffens, and I need a cane to get around comfortably for a day or two.",
        "b": "I have a Thursday morning knee replacement follow-up where the surgeon needs to see my knee bend through its full range without swelling.",
        "proposal": "A gym buddy talks me into a heavy squat personal-record attempt on Wednesday evening.",
        "query": "Based only on these records, should the heavy squat personal-record attempt on Wednesday evening be flagged as a fit risk for this user?",
        "c": "The heavy squat personal-record attempt on Wednesday evening should be flagged as a fit risk because the heavy-squat pattern that swells this user's reconstructed knee would conflict with Thursday's full-range, swelling-free follow-up.",
        "broken": "I have a Thursday morning follow-up with the surgeon, but it's a phone call check-in this time \u2014 no in-person knee exam happens.",
    },
    {
        "slug": "long_violin_practice_before_hand_therapy_eval",
        "a": "After more than two hours of violin practice without a break, the tendons in my left hand ache and my fingers feel stiff and slow to respond for the rest of the day.",
        "b": "I have a Friday morning hand therapy evaluation where the therapist needs my fingers at their normal, unstrained dexterity.",
        "proposal": "My conductor asks me to squeeze in an extra three-hour rehearsal block on Thursday evening before the concert.",
        "query": "Based only on these records, should squeezing in the extra three-hour rehearsal block on Thursday evening be flagged as a fit risk for this user?",
        "c": "Squeezing in the extra three-hour rehearsal block on Thursday evening should be flagged as a fit risk because the long-practice pattern that stiffens this user's fingers would conflict with Friday's normal-dexterity hand therapy evaluation.",
        "broken": "I have a Friday morning hand therapy appointment, but it's just to reschedule for next month this time \u2014 no dexterity evaluation happens.",
    },
    {
        "slug": "yard_work_bending_before_disc_mri",
        "a": "A long session of yard work with a lot of bending and raking leaves my lower back in spasm, and I have to move carefully for the rest of the day.",
        "b": "I have a Tuesday morning lumbar disc MRI where the technician needs me to lie flat and still without any muscle spasm.",
        "proposal": "My neighbor asks me to help clear a large overgrown yard full of bending and raking work on Monday afternoon.",
        "query": "Based only on these records, should helping clear the large overgrown yard on Monday afternoon be flagged as a fit risk for this user?",
        "c": "Helping clear the large overgrown yard on Monday afternoon should be flagged as a fit risk because the bending-and-raking pattern that spasms this user's lower back would conflict with Tuesday's lie-flat-and-still disc MRI.",
        "broken": "I have a Tuesday morning MRI appointment, but it's for my shoulder this time \u2014 no lying flat for the back is required.",
    },
    {
        "slug": "rock_climbing_before_finger_pulley_ultrasound",
        "a": "After a hard rock climbing session, the tendons in my fingers throb and feel tight, and gripping small objects is uncomfortable for a day afterward.",
        "b": "I have a Wednesday morning finger pulley ultrasound where the technician needs my finger tendons relaxed and untender.",
        "proposal": "A climbing partner invites me to project a hard new route on Tuesday evening.",
        "query": "Based only on these records, should projecting the hard new climbing route on Tuesday evening be flagged as a fit risk for this user?",
        "c": "Projecting the hard new climbing route on Tuesday evening should be flagged as a fit risk because the hard-climbing pattern that tenders this user's finger tendons would conflict with Wednesday's relaxed-tendon ultrasound.",
        "broken": "I have a Wednesday morning ultrasound appointment, but it's for my elbow this time \u2014 no finger tendon scan happens.",
    },
    {
        "slug": "standing_desk_marathon_before_foot_pressure_mapping",
        "a": "Whenever I stand at my desk for a full eight-hour shift without sitting, the balls of my feet ache and stay tender well into the next morning.",
        "b": "I have a Thursday morning foot pressure mapping session where the specialist needs my feet at their normal, untender baseline.",
        "proposal": "My team asks me to cover a full standing-desk shift with no breaks on Wednesday to cover for a sick coworker.",
        "query": "Based only on these records, should covering the full standing-desk shift with no breaks on Wednesday be flagged as a fit risk for this user?",
        "c": "Covering the full standing-desk shift with no breaks on Wednesday should be flagged as a fit risk because the all-day-standing pattern that tenders this user's feet would conflict with Thursday's untender-baseline pressure mapping.",
        "broken": "I have a Thursday morning appointment with the specialist, but it's just to pick up new orthotic inserts this time \u2014 no pressure mapping happens.",
    },
    {
        "slug": "heavy_toddler_carrying_before_lumbar_strength_test",
        "a": "Whenever I carry my toddler on one hip for an extended errand, my lower back and hip flexor ache unevenly and stay sore into the next day.",
        "b": "I have a Friday morning lumbar strength test where the physical therapist needs my back muscles at their normal, unfatigued baseline.",
        "proposal": "My sister asks me to watch her toddler for a full day of errands on Thursday, carrying the child on my hip most of the time.",
        "query": "Based only on these records, should watching my sister's toddler for a full day of hip-carrying errands on Thursday be flagged as a fit risk for this user?",
        "c": "Watching my sister's toddler for a full day of hip-carrying errands on Thursday should be flagged as a fit risk because the one-hip-carrying pattern that aches this user's back and hip would conflict with Friday's unfatigued-baseline lumbar strength test.",
        "broken": "I have a Friday morning appointment with the physical therapist, but it's just a phone consultation this time \u2014 no strength testing happens.",
    },
    {
        "slug": "late_sugar_before_fasting_lipid_panel",
        "a": "A late-night sugary snack leaves me starving and lightheaded by mid-morning, and I end up eating something before I even think about it.",
        "b": "I have a Tuesday morning fasting lipid panel where I need to go twelve hours without eating or drinking anything but water.",
        "proposal": "A coworker brings a batch of leftover birthday cake to Monday night's team happy hour.",
        "query": "Based only on these records, should bringing leftover birthday cake to Monday night's team happy hour be flagged as a fit risk for this user?",
        "c": "Eating the leftover birthday cake at Monday night's team happy hour should be flagged as a fit risk because a late-night sugary snack leaves this user starving enough to break a fast before Tuesday's lipid panel window closes.",
        "broken": "I have a Tuesday morning check-in with HR that's just a quick paperwork signature, no fasting or dietary restriction involved.",
    },
    {
        "slug": "jaw_grinding_before_dental_xray",
        "a": "Nights when I grind my teeth from stress leave my jaw so sore the next morning that I can barely open my mouth wide without wincing.",
        "b": "I have a Wednesday morning dental appointment where I need to hold my jaw open wide and steady for X-ray sensor placement.",
        "proposal": "A high-pressure client deadline lands Tuesday night, the kind that's triggered jaw-grinding nights before.",
        "query": "Based only on these records, should working through Tuesday night's high-pressure client deadline be flagged as a fit risk for this user?",
        "c": "Working through Tuesday night's high-pressure client deadline should be flagged as a fit risk because stress-triggered jaw-grinding leaves this user too sore to hold their jaw open wide for Wednesday's X-ray sensor placement.",
        "broken": "I have a Wednesday morning dental appointment, but it's just a schedule-confirmation call with the front desk, no exam involved.",
    },
    {
        "slug": "evening_run_before_mri_stillness",
        "a": "An evening run after 7pm leaves my legs restless and twitchy well into the next day, and I can't sit still for long stretches.",
        "b": "Thursday morning's MRI scan won't come out clear unless I can hold completely still on the table for forty-five minutes straight.",
        "proposal": "A running club invites me to an evening trail run Wednesday night, the night before Thursday's MRI.",
        "query": "Based only on these records, should Wednesday night's evening trail run be flagged as a fit risk for this user?",
        "c": "Wednesday night's evening trail run should be flagged as a fit risk because next-day restless legs would make it hard to lie still for Thursday's forty-five-minute MRI.",
        "broken": "I have a Thursday morning appointment that's just picking up MRI results on paper at the front desk, no scanning involved.",
    },
    {
        "slug": "flu_shot_soreness_before_moving_help",
        "a": "My arm gets sore and stiff at the injection site for about a day whenever I get a shot, and I can barely lift anything overhead.",
        "b": "I have a Friday moving job helping a friend carry boxes up three flights of stairs.",
        "proposal": "The clinic calls to schedule my flu shot for Thursday afternoon, the day before Friday's move.",
        "query": "Based only on these records, should scheduling the flu shot for Thursday afternoon be flagged as a fit risk for this user?",
        "c": "Scheduling the flu shot for Thursday afternoon should be flagged as a fit risk because next-day arm soreness would make it hard to carry boxes for Friday's move.",
        "broken": "The clinic calls to schedule a flu-shot information session for Thursday afternoon, just handing out pamphlets, no actual injection given.",
    },
    {
        "slug": "salty_dinner_before_biometric_bp_screening",
        "a": "A salty takeout dinner leaves my ankles puffy and my blood pressure reading noticeably higher the next morning when I check it at home.",
        "b": "I have a Monday morning workplace biometric screening where my blood pressure reading needs to reflect my normal baseline.",
        "proposal": "Coworkers are ordering salty fried chicken for a Sunday night watch party.",
        "query": "Based only on these records, should Sunday night's salty fried chicken watch party be flagged as a fit risk for this user?",
        "c": "Sunday night's salty fried chicken watch party should be flagged as a fit risk because a salty dinner raises this user's blood pressure reading the next morning, right when Monday's biometric screening needs a normal baseline.",
        "broken": "I have a Monday morning meeting to review last year's screening results on paper, no new reading is taken.",
    },
    {
        "slug": "caffeine_withdrawal_before_colonoscopy_prep",
        "a": "When I go a full day without any caffeine, I get a pounding headache by early afternoon that makes it hard to focus on anything.",
        "b": "I have a colonoscopy prep day Thursday where the instructions say no caffeine at all starting at breakfast.",
        "proposal": "A coworker asks me to run point on a detailed budget review Thursday afternoon.",
        "query": "Based only on these records, should running point on Thursday afternoon's detailed budget review be flagged as a fit risk for this user?",
        "c": "Running point on Thursday afternoon's detailed budget review should be flagged as a fit risk because a caffeine-free day gives this user a pounding headache by early afternoon, right when the colonoscopy prep day requires no caffeine at all.",
        "broken": "I have a colonoscopy prep day Thursday, but the updated instructions say caffeine is fine as long as it isn't red or purple in color.",
    },
    {
        "slug": "shoulder_workout_before_mammogram",
        "a": "A heavy shoulder-day workout leaves my upper arms and chest muscles sore enough that raising my arms overhead is uncomfortable for a full day after.",
        "b": "I have a Tuesday morning mammogram appointment where I need to raise my arms overhead and hold different positions without flinching.",
        "proposal": "My gym is running a one-time heavy shoulder-press class Monday evening, the night before Tuesday's mammogram.",
        "query": "Based only on these records, should Monday evening's heavy shoulder-press class be flagged as a fit risk for this user?",
        "c": "Monday evening's heavy shoulder-press class should be flagged as a fit risk because next-day soreness would make it uncomfortable to hold the overhead positions Tuesday's mammogram needs.",
        "broken": "I have a Tuesday morning appointment to pick up a mammogram referral letter at the front desk, no positioning or exam involved.",
    },
    {
        "slug": "calcium_supplement_before_bone_density_scan",
        "a": "I take a calcium supplement with breakfast every single day out of habit, and I forget it's in my pillbox unless someone reminds me.",
        "b": "I have a Wednesday morning bone density scan where I'm told not to take any calcium supplements for 24 hours beforehand.",
        "proposal": "This week's pillbox is already filled through Wednesday with the usual calcium supplement still in it.",
        "query": "Based only on these records, should taking Wednesday's usual calcium supplement from the pre-filled pillbox be flagged as a fit risk for this user?",
        "c": "Taking Wednesday's usual calcium supplement from the pre-filled pillbox should be flagged as a fit risk because this user habitually takes it without noticing, right when the bone density scan requires no calcium for 24 hours beforehand.",
        "broken": "I have a Wednesday morning appointment to schedule the bone density scan for next month, no supplement restriction applies yet.",
    },
    {
        "slug": "unreliable_ride_before_dilation_exam",
        "a": "After my eyes get dilated, my vision stays blurry for hours and I genuinely cannot read street signs or judge distance safely.",
        "b": "I have a Friday afternoon eye exam with dilation, and my ride home is a friend whose schedule is unconfirmed and often falls through last minute.",
        "proposal": "The clinic asks if I want to add the dilation portion to Friday's exam or skip it this visit.",
        "query": "Based only on these records, should adding the dilation portion to Friday's exam be flagged as a fit risk for this user?",
        "c": "Adding the dilation portion to Friday's exam should be flagged as a fit risk because post-dilation blurry vision would leave this user stranded given the unconfirmed, often-unreliable ride home.",
        "broken": "I have a Friday afternoon eye exam with dilation, and my ride home is my partner, who has already blocked out the whole afternoon and confirmed twice.",
    },
    {
        "slug": "lotion_habit_before_skin_cancer_screening",
        "a": "I moisturize heavily right after every shower out of habit, layering on thick lotion without really thinking about it.",
        "b": "I have a Monday morning full-body skin cancer screening where the dermatologist needs bare, lotion-free skin to see moles clearly.",
        "proposal": "My usual Monday morning shower routine already has the thick lotion sitting right by the sink.",
        "query": "Based only on these records, should following the usual Monday morning shower routine with thick lotion be flagged as a fit risk for this user?",
        "c": "Following the usual Monday morning shower routine with thick lotion should be flagged as a fit risk because this user moisturizes heavily out of habit, right when the skin cancer screening needs bare, lotion-free skin.",
        "broken": "I have a Monday morning appointment to reschedule the skin cancer screening to next month, no exam happens this visit.",
    },
    {
        "slug": "screen_strain_before_dmv_vision_test",
        "a": "Staring at spreadsheets for hours without breaks leaves my eyes dry and my vision noticeably blurrier by early evening.",
        "b": "Tuesday afternoon's DMV vision screening comes down to whether I can clearly make out the smallest line on their chart.",
        "proposal": "My manager asks me to finish a big spreadsheet audit Tuesday morning, right before the afternoon DMV appointment.",
        "query": "Based only on these records, should finishing Tuesday morning's spreadsheet audit be flagged as a fit risk for this user?",
        "c": "Finishing Tuesday morning's spreadsheet audit should be flagged as a fit risk because hours of screen strain leaves this user's vision blurrier by early evening, right when the DMV vision screening needs sharp reading of the smallest line.",
        "broken": "I have a Tuesday afternoon appointment to pick up a replacement DMV card by mail, no vision screening happens this visit.",
    },
    {
        "slug": "bathroom_habit_before_prenatal_ultrasound",
        "a": "I always use the bathroom right before I leave the house, out of habit, even when I know I'm not supposed to.",
        "b": "I have a Thursday morning prenatal ultrasound where I'm told to arrive with a full bladder for a clear image.",
        "proposal": "My Thursday morning routine already has me stopping at the bathroom right before heading out the door, same as always.",
        "query": "Based only on these records, should following the usual bathroom-before-leaving routine Thursday morning be flagged as a fit risk for this user?",
        "c": "Following the usual bathroom-before-leaving routine Thursday morning should be flagged as a fit risk because this user does it out of habit even when told not to, right when the prenatal ultrasound needs a full bladder for a clear image.",
        "broken": "I have a Thursday morning prenatal appointment that's just a quick paperwork update, no ultrasound imaging this visit.",
    },
    {
        "slug": "afternoon_caffeine_before_cardiac_stress_test",
        "a": "An afternoon coffee, even a small one, keeps my heart rate elevated and jittery for hours afterward.",
        "b": "I have a Wednesday morning cardiac stress test where the technician needs my resting heart rate at its normal baseline before starting.",
        "proposal": "A coworker brings a thermos of strong coffee to share at Tuesday afternoon's team meeting, the day before Wednesday's test.",
        "query": "Based only on these records, should having coffee at Tuesday afternoon's team meeting be flagged as a fit risk for this user?",
        "c": "Having coffee at Tuesday afternoon's team meeting should be flagged as a fit risk because afternoon caffeine keeps this user's heart rate elevated for hours, right when Wednesday's cardiac stress test needs a normal resting baseline.",
        "broken": "I have a Wednesday morning cardiac follow-up that's just discussing last month's results, no new stress test this visit.",
    },
    {
        "slug": "houseguest_couch_before_sleep_apnea_test",
        "a": "Whenever I sleep on the couch instead of my bed, I end up on my back most of the night and wake up with a worse headache than usual.",
        "b": "I have a Sunday night home sleep apnea test where the equipment needs an accurate read of my normal sleep position and breathing.",
        "proposal": "A friend needs to crash on my couch for the weekend, which means I'd be sleeping on the couch too since I only have one bed.",
        "query": "Based only on these records, should sleeping on the couch during the friend's weekend visit be flagged as a fit risk for this user?",
        "c": "Sleeping on the couch during the friend's weekend visit should be flagged as a fit risk because couch-sleeping puts this user on their back most of the night, right when Sunday's home sleep apnea test needs an accurate read of normal sleep position.",
        "broken": "A friend needs to crash at my place for the weekend, but I have a guest room with its own bed, so my own sleep setup doesn't change.",
    },
    {
        "slug": "daily_allergy_pill_before_skin_test",
        "a": "I take my daily allergy pill every single morning without fail, it's the first thing I do after I wake up.",
        "b": "I have a Friday morning allergy skin test where I'm told to stop all antihistamines for five days beforehand or the results won't be accurate.",
        "proposal": "This week's pillbox is already filled with Friday's usual allergy pill sitting right on top.",
        "query": "Based only on these records, should taking Friday's usual allergy pill from the pre-filled pillbox be flagged as a fit risk for this user?",
        "c": "Taking Friday's usual allergy pill from the pre-filled pillbox should be flagged as a fit risk because this user takes it automatically every morning, right when the allergy skin test needs five antihistamine-free days for accurate results.",
        "broken": "I have a Friday morning appointment to reschedule the allergy skin test for next month, no antihistamine restriction applies yet.",
    },
    {
        "slug": "forgotten_followup_before_tb_test_reading",
        "a": "I regularly forget follow-up appointments that aren't the same day as the first visit, especially ones a few days out.",
        "b": "I have a TB skin test placed Monday that needs to be read by a nurse within 48 to 72 hours or the results are invalid.",
        "proposal": "My calendar this week has no reminder set for Wednesday's TB test reading, same as my usual habit of skipping reminders for follow-ups.",
        "query": "Based only on these records, should skipping a reminder for Wednesday's TB test reading be flagged as a fit risk for this user?",
        "c": "Skipping a reminder for Wednesday's TB test reading should be flagged as a fit risk because this user regularly forgets follow-up appointments a few days out, right when the reading needs to happen within the 48-to-72-hour window or the results are invalid.",
        "broken": "I have a TB skin test placed Monday, but this clinic reads results by photo upload any time within a week, no in-person return window.",
    },
    {
        "slug": "spontaneous_trip_before_pap_smear",
        "a": "A weekend trip usually means I skip my usual routines and let plans happen spontaneously without much forethought.",
        "b": "I have a Monday morning pap smear where I'm told to avoid certain products and activities for 48 hours beforehand for accurate results.",
        "proposal": "My partner is planning a spontaneous anniversary weekend getaway this Saturday and Sunday, right before Monday's appointment.",
        "query": "Based only on these records, should going along with the spontaneous anniversary weekend be flagged as a fit risk for this user?",
        "c": "Going along with the spontaneous anniversary weekend should be flagged as a fit risk because this user's spontaneous, routine-skipping weekend pattern could easily breach the 48-hour restriction Monday's pap smear needs for accurate results.",
        "broken": "I have a Monday morning appointment to pick up last month's pap smear results, no new sample collected this visit.",
    },
    {
        "slug": "long_ride_before_psa_screening",
        "a": "My weekend habit is a long bike ride on the road bike, usually two to three hours on the saddle without much of a break.",
        "b": "I have a Monday morning PSA blood test where I'm told to avoid cycling and certain activities for 48 hours beforehand or the reading can be artificially elevated.",
        "proposal": "My cycling group is doing the usual long Saturday ride, same route as every weekend, two days before Monday's test.",
        "query": "Based only on these records, should joining Saturday's usual long bike ride be flagged as a fit risk for this user?",
        "c": "Joining Saturday's usual long bike ride should be flagged as a fit risk because extended time on the saddle falls inside the 48-hour window Monday's PSA test needs to avoid, and could artificially elevate the reading.",
        "broken": "I have a Monday morning appointment to go over last quarter's PSA results, no new blood draw this visit.",
    },
    {
        "slug": "travel_eating_before_hepatitis_panel",
        "a": "Whenever my meal schedule gets thrown off by travel, I end up snacking constantly through the day just to keep from feeling awful.",
        "b": "I have a Thursday morning hepatitis panel that requires a 12-hour fast, arriving before I've eaten or had anything but water.",
        "proposal": "My manager wants me to fly out Wednesday afternoon for a same-day work trip that lands late Wednesday night, right before Thursday's fasting draw.",
        "query": "Based only on these records, should flying out Wednesday afternoon for the same-day work trip be flagged as a fit risk for this user?",
        "c": "Flying out Wednesday afternoon for the same-day work trip should be flagged as a fit risk because travel-disrupted meal schedules lead this user to snack constantly, right when Thursday's hepatitis panel needs a clean 12-hour fast.",
        "broken": "I have a Thursday morning appointment to drop off a paper referral form at the lab, no blood draw or fasting required this visit.",
    },
    {
        "slug": "high_pollen_lawn_mowing_before_allergy_test",
        "a": "Whenever I mow the lawn during high pollen days, my eyes swell and my nose stays stuffy well into the next morning.",
        "b": "I have a Sunday morning allergy skin-prick test where the clinician needs my skin free of swelling or histamine reaction to read the results accurately.",
        "proposal": "A neighbor asks me to mow their overgrown lawn this Saturday, which is forecast to be a high-pollen day.",
        "query": "Based only on these records, should mowing the neighbor's overgrown lawn on Saturday be flagged as a fit risk for this user?",
        "c": "Mowing the neighbor's overgrown lawn on Saturday should be flagged as a fit risk because high-pollen mowing triggers swelling and congestion that would interfere with Sunday's allergy skin-prick reading.",
        "broken": "I have a Sunday morning allergy consultation, but it's just a phone call to discuss past results, with no skin testing involved.",
    },
    {
        "slug": "wildfire_smoke_run_before_spirometry",
        "a": "Running outside when the wildfire smoke is heavy leaves me wheezing and short of breath for the rest of the day.",
        "b": "My spirometry appointment is Sunday morning, and the technician can only get a valid reading if my lungs haven't been irritated beforehand.",
        "proposal": "A running club invites me to an outdoor group run this Saturday, and the air quality index is forecast to be in the smoky range.",
        "query": "Based only on these records, should the outdoor group run on smoky Saturday be flagged as a fit risk for this user?",
        "c": "The outdoor group run on smoky Saturday should be flagged as a fit risk because smoke exposure triggers wheezing and reduced lung capacity right before Sunday's spirometry baseline.",
        "broken": "I have a Sunday morning appointment to pick up a spacer device from the pharmacy, which needs no lung function testing.",
    },
    {
        "slug": "cold_air_jog_before_peak_flow_check",
        "a": "Jogging in cold, dry air below freezing tightens my chest and sets off a cough that lingers through the next day.",
        "b": "I have a Sunday morning peak-flow check with my pulmonologist where I need to blow a reading close to my personal best.",
        "proposal": "A friend wants to do an early Saturday morning cold-weather jog together, with temperatures forecast well below freezing.",
        "query": "Based only on these records, should the early Saturday cold-weather jog be flagged as a fit risk for this user?",
        "c": "The early Saturday cold-weather jog should be flagged as a fit risk because cold, dry air tightens this user's chest and triggers a cough that would depress Sunday's peak-flow reading.",
        "broken": "I have a Sunday morning reminder to reorder inhaler refills online, which needs no peak-flow performance.",
    },
    {
        "slug": "damp_basement_cleanup_before_mold_panel",
        "a": "Spending more than an hour in a damp, musty basement leaves my sinuses inflamed and my breathing shallow into the next day.",
        "b": "I have a Sunday morning mold-sensitivity blood panel where the lab needs my sinuses in a non-inflamed baseline state.",
        "proposal": "A relative asks me to help clear out their damp, musty basement this Saturday afternoon.",
        "query": "Based only on these records, should helping clear the damp basement on Saturday be flagged as a fit risk for this user?",
        "c": "Helping clear the damp basement on Saturday should be flagged as a fit risk because damp, musty exposure inflames this user's sinuses right before Sunday's mold-sensitivity panel needs a non-inflamed baseline.",
        "broken": "I have a Sunday morning mold-panel results review, which is just a phone summary with no new sample needed.",
    },
    {
        "slug": "high_altitude_hike_before_oxygen_saturation_test",
        "a": "Hiking above 8,000 feet leaves me lightheaded with noticeably lower blood oxygen readings for a day or two afterward.",
        "b": "I have a Sunday morning oxygen-saturation test where the clinic needs my reading to reflect my normal sea-level baseline.",
        "proposal": "A hiking group invites me to a high-altitude trail above 8,000 feet this Saturday.",
        "query": "Based only on these records, should the high-altitude Saturday hike be flagged as a fit risk for this user?",
        "c": "The high-altitude Saturday hike should be flagged as a fit risk because elevation exposure lowers this user's blood oxygen for days afterward, right when Sunday's test needs a normal sea-level baseline.",
        "broken": "I have a Sunday morning check-in to update my primary care contact info, which needs no oxygen reading.",
    },
    {
        "slug": "fresh_paint_fumes_before_asthma_challenge_test",
        "a": "Being in a freshly painted room for more than twenty minutes triggers a tight chest and audible wheeze that takes hours to settle.",
        "b": "I have a Sunday morning bronchial challenge test where the technician needs my airways unirritated going in.",
        "proposal": "A friend asks me to help paint their spare room this Saturday afternoon.",
        "query": "Based only on these records, should helping paint the spare room on Saturday be flagged as a fit risk for this user?",
        "c": "Helping paint the spare room on Saturday should be flagged as a fit risk because fresh paint fumes trigger chest tightness and wheeze that would irritate the airways Sunday's bronchial challenge test needs unirritated.",
        "broken": "I have a Sunday morning reminder to renew my asthma action plan paperwork online, which needs no airway testing.",
    },
    {
        "slug": "campfire_smoke_evening_before_chest_xray",
        "a": "Sitting near a campfire for a couple of hours leaves my cough noticeably worse and my chest sore into the following morning.",
        "b": "I have a Sunday morning chest X-ray where the technician needs me to hold a full, steady breath without coughing.",
        "proposal": "Friends invite me to an evening campfire gathering this Saturday night.",
        "query": "Based only on these records, should the Saturday night campfire gathering be flagged as a fit risk for this user?",
        "c": "The Saturday night campfire gathering should be flagged as a fit risk because campfire smoke worsens this user's cough and chest soreness right before Sunday's X-ray needs a full steady breath without coughing.",
        "broken": "I have a Sunday morning appointment to sign a routine imaging consent form, which needs no breath-holding.",
    },
    {
        "slug": "perfume_heavy_event_before_fragrance_sensitivity_review",
        "a": "Spending an evening around heavy perfume or cologne gives me a pounding sinus headache that lasts until midday the next day.",
        "b": "I have a Sunday morning fragrance-sensitivity review with my allergist where I need to describe my symptoms without a headache clouding my recall.",
        "proposal": "A coworker invites me to a Saturday evening party where heavy perfume and cologne are common.",
        "query": "Based only on these records, should the Saturday evening perfume-heavy party be flagged as a fit risk for this user?",
        "c": "The Saturday evening perfume-heavy party should be flagged as a fit risk because fragrance exposure gives this user a lasting sinus headache right when Sunday's review needs clear, headache-free symptom recall.",
        "broken": "I have a Sunday morning fragrance-sensitivity review that was moved to a written questionnaire I can fill out anytime this week.",
    },
    {
        "slug": "dusty_attic_sort_before_pulmonary_function_test",
        "a": "Digging through a dusty attic for an afternoon leaves me sneezing in fits and coughing well into the next day.",
        "b": "I have a Sunday morning pulmonary function test where the technician needs three consistent, forceful exhales without a cough interrupting them.",
        "proposal": "A parent asks me to help sort through their dusty attic this Saturday afternoon.",
        "query": "Based only on these records, should helping sort the dusty attic on Saturday be flagged as a fit risk for this user?",
        "c": "Helping sort the dusty attic on Saturday should be flagged as a fit risk because attic dust triggers sneezing and coughing that would disrupt the forceful, uninterrupted exhales Sunday's pulmonary function test needs.",
        "broken": "I have a Sunday morning appointment to drop off a pulmonary function questionnaire at the front desk, which needs no breathing test.",
    },
    {
        "slug": "chlorine_heavy_pool_before_asthma_medication_titration",
        "a": "Swimming in a heavily chlorinated indoor pool leaves my throat raw and my breathing tight for the rest of the day.",
        "b": "I have a Sunday morning asthma medication titration appointment where the doctor needs to hear my current, unmedicated-for-the-moment breathing sounds clearly.",
        "proposal": "A friend invites me to an indoor pool party this Saturday at a heavily chlorinated facility.",
        "query": "Based only on these records, should the Saturday indoor chlorinated pool party be flagged as a fit risk for this user?",
        "c": "The Saturday indoor chlorinated pool party should be flagged as a fit risk because heavy chlorine exposure leaves this user's breathing tight right before Sunday's titration appointment needs clear breathing sounds.",
        "broken": "I have a Sunday morning asthma medication titration appointment that was switched to a phone check-in based on my logged symptom diary.",
    },
    {
        "slug": "new_carpet_voc_exposure_before_sleep_apnea_titration",
        "a": "Spending an evening in a room with newly installed carpet leaves my throat scratchy and my breathing noisier than usual overnight.",
        "b": "I have a Sunday overnight sleep apnea titration study where the technician needs my breathing sounds to reflect my normal baseline.",
        "proposal": "A friend just had new carpet installed and invites me over Saturday evening before it's had time to air out.",
        "query": "Based only on these records, should visiting the friend's newly carpeted home on Saturday evening be flagged as a fit risk for this user?",
        "c": "Visiting the friend's newly carpeted home on Saturday evening should be flagged as a fit risk because new-carpet fumes leave this user's breathing noisier right before Sunday's titration study needs a normal baseline.",
        "broken": "I have a Sunday overnight sleep apnea titration study that got rescheduled to use my existing at-home recording instead of a new one.",
    },
    {
        "slug": "high_humidity_yardwork_before_exercise_induced_asthma_test",
        "a": "Doing yard work in high humidity leaves me winded and coughing well beyond when the work itself is done.",
        "b": "I have a Sunday morning exercise-induced asthma test where the clinic needs to measure my breathing response to controlled exertion, not leftover strain.",
        "proposal": "A neighbor asks me to help clear brush in their yard this Saturday afternoon, forecast to be hot and humid.",
        "query": "Based only on these records, should helping clear brush in humid weather on Saturday be flagged as a fit risk for this user?",
        "c": "Helping clear brush in humid weather on Saturday should be flagged as a fit risk because high-humidity exertion leaves this user winded well beyond the activity, right before Sunday's test needs to measure a controlled, uncontaminated breathing response.",
        "broken": "I have a Sunday morning exercise-induced asthma test that was postponed to next month for equipment calibration.",
    },
    {
        "slug": "cat_dander_heavy_apartment_before_immunotherapy_dose",
        "a": "A few hours in an apartment with multiple cats leaves my eyes itchy and my chest tight until well into the next day.",
        "b": "I have a Sunday morning allergy immunotherapy dose where the nurse needs me free of an active reaction before injecting the next step-up dose.",
        "proposal": "A friend with several cats invites me over Saturday afternoon to watch a movie.",
        "query": "Based only on these records, should visiting the friend's multi-cat apartment on Saturday be flagged as a fit risk for this user?",
        "c": "Visiting the friend's multi-cat apartment on Saturday should be flagged as a fit risk because cat dander exposure leaves this user with itchy eyes and chest tightness right before Sunday's immunotherapy dose needs no active reaction present.",
        "broken": "I have a Sunday morning immunotherapy appointment that was changed to a dosing consultation with no injection this cycle.",
    },
    {
        "slug": "bonfire_beach_night_before_croup_followup",
        "a": "A smoky beach bonfire leaves my child's cough noticeably barking and their breathing raspier through the next morning.",
        "b": "I have a Sunday morning pediatric follow-up where the doctor needs to hear my child's breathing without recent smoke irritation clouding it.",
        "proposal": "Neighbors invite our family to a smoky beach bonfire this Saturday night.",
        "query": "Based only on these records, should attending the smoky beach bonfire on Saturday night be flagged as a fit risk for this child?",
        "c": "Attending the smoky beach bonfire on Saturday night should be flagged as a fit risk because smoke exposure worsens the child's cough and breathing right before Sunday's follow-up needs unclouded breathing sounds.",
        "broken": "I have a Sunday morning pediatric follow-up that was moved to a video call to review the home symptom log instead.",
    },
    {
        "slug": "incense_filled_temple_visit_before_rhinomanometry",
        "a": "An hour in a room thick with incense smoke leaves my nasal passages swollen and my breathing through my nose difficult until the next day.",
        "b": "I have a Sunday morning rhinomanometry test where the technician needs my nasal airflow to be at its normal, unswollen baseline.",
        "proposal": "Relatives invite me to a heavily incense-filled temple ceremony this Saturday.",
        "query": "Based only on these records, should attending the incense-filled temple ceremony on Saturday be flagged as a fit risk for this user?",
        "c": "Attending the incense-filled temple ceremony on Saturday should be flagged as a fit risk because incense smoke swells this user's nasal passages right before Sunday's rhinomanometry needs a normal, unswollen baseline.",
        "broken": "I have a Sunday morning rhinomanometry test that was rescheduled to next week while the clinic replaces its equipment.",
    },
    {
        "slug": "dry_cleaning_chemical_exposure_before_voc_sensitivity_panel",
        "a": "Picking up a large batch of dry cleaning and riding home with it in an unventilated car leaves my throat burning and my breathing shallow for hours.",
        "b": "I have a Sunday morning VOC-sensitivity panel where the lab needs my airway baseline free of recent chemical irritation.",
        "proposal": "I'm asked to pick up a large family order of dry cleaning this Saturday and drive it home in my car.",
        "query": "Based only on these records, should picking up the large dry-cleaning order on Saturday be flagged as a fit risk for this user?",
        "c": "Picking up the large dry-cleaning order on Saturday should be flagged as a fit risk because the chemical fumes burn this user's throat and shallow their breathing right before Sunday's VOC-sensitivity panel needs an unirritated baseline.",
        "broken": "I have a Sunday morning VOC-sensitivity panel that was changed to reviewing my symptom diary over the phone instead of a new sample.",
    },
    {
        "slug": "gym_ozone_air_purifier_room_before_methacholine_challenge",
        "a": "Working out in the gym's room with the industrial ozone-generating air purifier running leaves my chest burning and my cough triggered for the rest of the day.",
        "b": "I have a Sunday morning methacholine challenge test where the pulmonologist needs my airways at baseline sensitivity, not already irritated.",
        "proposal": "My usual gym class this Saturday is being held in the room with the ozone-generating purifier while the main room is renovated.",
        "query": "Based only on these records, should attending Saturday's gym class in the ozone-purifier room be flagged as a fit risk for this user?",
        "c": "Attending Saturday's gym class in the ozone-purifier room should be flagged as a fit risk because ozone exposure burns this user's chest and triggers coughing right before Sunday's methacholine challenge needs unirritated baseline airways.",
        "broken": "I have a Sunday morning methacholine challenge test that got pushed back a month because the clinic's equipment is being serviced.",
    },
    {
        "slug": "windy_construction_site_dust_before_nitric_oxide_test",
        "a": "Walking past a windy construction site with visible dust in the air leaves my breathing wheezy and my throat tight for the rest of the afternoon.",
        "b": "I have a Sunday morning fractional exhaled nitric oxide test where the clinic needs my airway inflammation at its normal resting level.",
        "proposal": "My usual walking route this Saturday goes right past a windy, dusty construction site that just started demolition.",
        "query": "Based only on these records, should taking the usual walking route past the dusty construction site on Saturday be flagged as a fit risk for this user?",
        "c": "Taking the usual walking route past the dusty construction site on Saturday should be flagged as a fit risk because construction dust triggers wheezing and throat tightness right before Sunday's nitric oxide test needs normal resting airway inflammation.",
        "broken": "I have a Sunday morning nitric oxide test that was rescheduled after the clinic's device failed calibration this week.",
    },
    {
        "slug": "vision_strain_close_beadwork_before_reading_exam",
        "a": "Hours of close-up beading work leave my eyes strained and my near vision blurry for the rest of the day.",
        "b": "I have a Sunday morning vision exam where I need to read the smallest line on the reading chart accurately.",
        "proposal": "A craft group invites me to an all-day Saturday beading marathon.",
        "query": "Based only on these records, should the all-day Saturday beading marathon be flagged as a fit risk for this user?",
        "c": "The all-day Saturday beading marathon should be flagged as a fit risk because hours of close-up beadwork strain near vision right when Sunday's exam needs the smallest line read accurately.",
        "broken": "I have a Sunday morning eye clinic visit, but it's only to update my insurance paperwork and doesn't involve any vision testing.",
    },
    {
        "slug": "glare_driving_afterimage_before_precision_hobby",
        "a": "Driving straight into bright afternoon glare leaves bright afterimages and halo rings in my vision for a couple of hours afterward.",
        "b": "I have a Sunday afternoon model-building session where I need sharp, accurate vision to align tiny parts.",
        "proposal": "Friends invite me to a Saturday afternoon road trip with several hours of driving into the western sun.",
        "query": "Based only on these records, should the Saturday afternoon glare-heavy road trip be flagged as a fit risk for this user?",
        "c": "The Saturday afternoon glare-heavy road trip should be flagged as a fit risk because the resulting afterimages would interfere with Sunday's model-building session that needs sharp, accurate vision.",
        "broken": "I have a Sunday afternoon plan to sort a box of old photos, which doesn't need sharp close-up vision.",
    },
    {
        "slug": "power_tool_tinnitus_before_soft_spoken_interview",
        "a": "Using power tools without earplugs leaves my ears ringing and makes it hard to pick out quiet voices for the rest of the day.",
        "b": "I have a Monday morning phone interview with a soft-spoken hiring manager where catching every word matters.",
        "proposal": "A neighbor asks for help running a table saw and drill for a Sunday afternoon woodworking project.",
        "query": "Based only on these records, should the Sunday afternoon power-tool woodworking help be flagged as a fit risk for this user?",
        "c": "The Sunday afternoon power-tool woodworking help should be flagged as a fit risk because the resulting ringing would make it hard to catch the soft-spoken hiring manager's words on Monday's interview.",
        "broken": "I have a Monday morning interview, but it just got switched to a written questionnaire instead of a phone call.",
    },
    {
        "slug": "loud_restaurant_auditory_fatigue_before_negotiation_call",
        "a": "Eating in loud, echoey restaurants leaves my ears fatigued, and I struggle to follow conversation nuance for the rest of that evening.",
        "b": "I have a Tuesday evening negotiation call where I need to catch subtle shifts in tone to know when to push back.",
        "proposal": "Coworkers want to celebrate a project wrap at a loud, crowded restaurant Tuesday at lunch.",
        "query": "Based only on these records, should the loud Tuesday lunch celebration be flagged as a fit risk for this user?",
        "c": "The loud Tuesday lunch celebration should be flagged as a fit risk because the resulting auditory fatigue would make it hard to catch tone shifts on Tuesday evening's negotiation call.",
        "broken": "I have a Tuesday evening call, but it's been rescheduled to an email exchange instead.",
    },
    {
        "slug": "spinning_ride_dizziness_before_ladder_task",
        "a": "Fast spinning amusement rides leave me dizzy and unsteady on my feet for several hours afterward.",
        "b": "I have a Sunday morning gutter-cleaning task that requires standing steadily on a ladder.",
        "proposal": "Cousins invite me to spend Saturday evening riding the fastest spinning rides at the fair.",
        "query": "Based only on these records, should the Saturday evening fast-spinning-ride outing be flagged as a fit risk for this user?",
        "c": "The Saturday evening fast-spinning-ride outing should be flagged as a fit risk because the resulting dizziness would undermine the steady footing Sunday's ladder task on the gutters needs.",
        "broken": "I have a Sunday morning task to clean gutters, but a neighbor said they'd handle the ladder part and I'd just hand up tools from the ground.",
    },
    {
        "slug": "sailing_sea_legs_before_calligraphy_class",
        "a": "A few hours of sailing leaves a swaying, off-balance feeling that lingers well into the next day.",
        "b": "I have a Sunday afternoon calligraphy class where I need a steady hand to keep the pen strokes even.",
        "proposal": "A friend invites me on a Saturday afternoon sailing trip out on the bay.",
        "query": "Based only on these records, should the Saturday afternoon sailing trip be flagged as a fit risk for this user?",
        "c": "The Saturday afternoon sailing trip should be flagged as a fit risk because the lingering sway would undermine the steady hand Sunday's calligraphy class needs.",
        "broken": "I have a Sunday afternoon calligraphy class, but this week's session is just watching a demonstration video, no pen work required.",
    },
    {
        "slug": "strobe_lights_photophobia_before_outdoor_shoot",
        "a": "Strobing club lights trigger a headache and make bright daylight uncomfortable to be in for most of the next day.",
        "b": "I have a Sunday morning outdoor photo shoot where I need to be comfortable working in full sunlight for a couple hours.",
        "proposal": "Friends invite me to a Saturday night party with a strobe-light dance floor.",
        "query": "Based only on these records, should the Saturday night strobe-light party be flagged as a fit risk for this user?",
        "c": "The Saturday night strobe-light party should be flagged as a fit risk because the resulting light sensitivity would conflict with Sunday's outdoor shoot that needs comfortable time in full sunlight.",
        "broken": "I have a Sunday morning photo shoot, but it moved indoors to a softly lit studio instead.",
    },
    {
        "slug": "late_screen_pupil_sensitivity_before_sunrise_hike",
        "a": "Staring at a bright phone screen right before bed leaves my eyes sensitive and squinty in daylight the next morning.",
        "b": "I have a Sunday sunrise hike where I need my eyes to adjust comfortably to the bright morning light on the trail.",
        "proposal": "A friend wants to binge-watch a show on a bright phone screen late Saturday night before bed.",
        "query": "Based only on these records, should the late Saturday night bright-screen binge be flagged as a fit risk for this user?",
        "c": "The late Saturday night bright-screen binge should be flagged as a fit risk because the resulting eye sensitivity would conflict with Sunday's sunrise hike needing comfortable adjustment to bright morning light.",
        "broken": "I have a Sunday hike, but the group decided to start at dusk instead of sunrise.",
    },
    {
        "slug": "scratchy_fabric_tactile_overload_before_massage_appointment",
        "a": "Wearing scratchy formal fabric for a few hours leaves my skin irritated and overly sensitive to touch for the rest of that day.",
        "b": "I have a Sunday afternoon massage therapy appointment where I need to be comfortable with firm touch and pressure.",
        "proposal": "A wedding this Saturday requires wearing a stiff, scratchy formal outfit for several hours.",
        "query": "Based only on these records, should wearing the stiff, scratchy outfit to Saturday's wedding be flagged as a fit risk for this user?",
        "c": "Wearing the stiff, scratchy outfit to Saturday's wedding should be flagged as a fit risk because the resulting skin irritation would conflict with Sunday's massage appointment needing comfort with firm touch.",
        "broken": "I have a Sunday appointment, but it's been changed to a consultation talk with no hands-on massage work.",
    },
    {
        "slug": "knitting_finger_numbness_before_medical_device_handling",
        "a": "Long stretches of tight-gauge knitting leave my fingertips numb and less sensitive to touch for the rest of the day.",
        "b": "I have a Sunday morning volunteer shift assembling first-aid kits where I need to feel small parts precisely by touch.",
        "proposal": "A craft fair invites me to run an all-day Saturday knitting demo table.",
        "query": "Based only on these records, should the all-day Saturday knitting demo table be flagged as a fit risk for this user?",
        "c": "The all-day Saturday knitting demo table should be flagged as a fit risk because the resulting finger numbness would undermine the precise touch Sunday's first-aid-kit assembly needs.",
        "broken": "I have a Sunday shift, but this week it's sorting kits by checking a printed list, not handling small parts by feel.",
    },
    {
        "slug": "loud_headphones_ear_fatigue_before_voice_memo_review",
        "a": "Long stretches with loud headphones leave my ears fatigued and I miss small audio details for the rest of the day.",
        "b": "I have a Sunday afternoon task reviewing detailed voice memos where I need to catch every quiet word.",
        "proposal": "A friend wants to marathon a podcast series Saturday at high volume through headphones for several hours.",
        "query": "Based only on these records, should the Saturday high-volume headphone podcast marathon be flagged as a fit risk for this user?",
        "c": "The Saturday high-volume headphone podcast marathon should be flagged as a fit risk because the resulting ear fatigue would make it hard to catch quiet details in Sunday's voice-memo review.",
        "broken": "I have a Sunday task, but the memos this week come with a written transcript, so listening carefully isn't required.",
    },
    {
        "slug": "carnival_teacups_vertigo_before_tightrope_class",
        "a": "Riding spinning teacup-style rides leaves me with lingering vertigo and a wobbly stance for several hours after.",
        "b": "I have a Sunday afternoon beginner slackline class where I need reliable balance to stay on the line.",
        "proposal": "Cousins invite me to ride the spinning teacups repeatedly at Saturday's carnival.",
        "query": "Based only on these records, should repeatedly riding the spinning teacups at Saturday's carnival be flagged as a fit risk for this user?",
        "c": "Repeatedly riding the spinning teacups at Saturday's carnival should be flagged as a fit risk because the resulting vertigo would undermine the balance Sunday's slackline class needs.",
        "broken": "I have a Sunday class, but this week's session is just watching instructors demonstrate technique from the ground.",
    },
    {
        "slug": "fluorescent_flicker_headache_before_art_gallery_review",
        "a": "Sitting under flickering fluorescent lighting gives me a headache and makes me want to avoid bright rooms for the rest of the day.",
        "b": "I have a Sunday afternoon gallery walkthrough where I need to comfortably view art under bright overhead lighting.",
        "proposal": "My office wants me to work a Saturday shift in the old wing that still has flickering fluorescent lights.",
        "query": "Based only on these records, should the Saturday shift under the flickering fluorescent lights be flagged as a fit risk for this user?",
        "c": "The Saturday shift under the flickering fluorescent lights should be flagged as a fit risk because the resulting headache would conflict with Sunday's gallery walkthrough needing comfort under bright lighting.",
        "broken": "I have a Sunday walkthrough, but the gallery's bright-light wing is closed this week, so viewing happens in a dim room instead.",
    },
    {
        "slug": "wool_sweater_skin_sensitivity_before_fabric_sample_review",
        "a": "A few hours in a wool sweater and my skin stays itchy and reactive to any fabric brushing against it well into the evening.",
        "b": "I have a Sunday afternoon job reviewing fabric samples where I need to compare textures carefully by hand.",
        "proposal": "Cold weather this Saturday means wearing a heavy wool sweater outdoors most of the day.",
        "query": "Based only on these records, should wearing the heavy wool sweater outdoors most of Saturday be flagged as a fit risk for this user?",
        "c": "Wearing the heavy wool sweater outdoors most of Saturday should be flagged as a fit risk because the resulting skin sensitivity would interfere with Sunday's careful hand comparison of fabric samples.",
        "broken": "I have a Sunday review, but this batch of samples just needs a visual inspection, not a hands-on texture comparison.",
    },
    {
        "slug": "underwater_pressure_ear_fullness_before_choir_rehearsal",
        "a": "Diving to the bottom of the deep end repeatedly leaves my ears feeling full and my pitch perception off for the rest of the day.",
        "b": "I have a Sunday afternoon choir rehearsal where I need accurate pitch to blend with the other singers.",
        "proposal": "Friends invite me to spend Saturday afternoon doing repeated deep dives at the pool.",
        "query": "Based only on these records, should the Saturday afternoon repeated deep-diving session be flagged as a fit risk for this user?",
        "c": "The Saturday afternoon repeated deep-diving session should be flagged as a fit risk because the resulting ear fullness would throw off the pitch accuracy Sunday's choir rehearsal needs.",
        "broken": "I have a Sunday rehearsal, but this week it's a seated music-theory session with no actual singing.",
    },
    {
        "slug": "long_scroll_eye_fatigue_before_proofreading_shift",
        "a": "Long stretches of scrolling through social media leave my eyes tired and my focus blurry for small text for the rest of the day.",
        "b": "I have a Sunday evening proofreading shift where I need sharp focus on small printed text for a couple hours.",
        "proposal": "A friend and I plan to spend Saturday evening scrolling through old photo albums online for hours.",
        "query": "Based only on these records, should the Saturday evening hours-long scrolling session be flagged as a fit risk for this user?",
        "c": "The Saturday evening hours-long scrolling session should be flagged as a fit risk because the resulting eye fatigue would undermine the sharp small-text focus Sunday's proofreading shift needs.",
        "broken": "I have a Sunday shift, but this week's assignment is checking large-print section headers only.",
    },
    {
        "slug": "perfume_scent_overload_before_wine_tasting_review",
        "a": "Being around strong perfume or cologne for a while leaves my sense of smell dulled and slow to recover for the rest of the day.",
        "b": "I have a Sunday afternoon wine-tasting review where I need my sense of smell sharp to describe the aromas accurately.",
        "proposal": "A department store wants me to work the fragrance counter Saturday, spraying samples most of the shift.",
        "query": "Based only on these records, should working Saturday's fragrance counter shift be flagged as a fit risk for this user?",
        "c": "Working Saturday's fragrance counter shift should be flagged as a fit risk because the resulting scent dulling would undermine the sharp sense of smell Sunday's wine-tasting review needs.",
        "broken": "I have a Sunday review, but this week it's rating wines purely by color and clarity, not by aroma.",
    },
    {
        "slug": "cold_water_plunge_numb_hands_before_pottery_class",
        "a": "A cold-water plunge leaves my hands numb and clumsy with fine movements for a couple hours afterward.",
        "b": "I have a Sunday afternoon pottery class where I need steady, sensitive fingers to shape the clay on the wheel.",
        "proposal": "A wellness group invites me to a Saturday morning cold-plunge session before pottery class the next day.",
        "query": "Based only on these records, should the Saturday morning cold-plunge session be flagged as a fit risk for this user?",
        "c": "The Saturday morning cold-plunge session should be flagged as a fit risk because the resulting hand numbness would undermine the sensitive fingers Sunday's pottery class needs.",
        "broken": "I have a Sunday class, but this week's session is just glazing pre-shaped pieces with a brush, no wheel work.",
    },
    {
        "slug": "bright_stage_lighting_glare_before_microscope_lab_shift",
        "a": "Standing under bright stage lighting leaves my eyes glare-sensitive and slow to refocus on close objects for hours after.",
        "b": "I have a Monday morning lab shift where I need to refocus quickly and clearly through a microscope eyepiece.",
        "proposal": "A community theater asks me to help run a lighting check under the bright stage lights Sunday evening.",
        "query": "Based only on these records, should helping with Sunday evening's bright stage-lighting check be flagged as a fit risk for this user?",
        "c": "Helping with Sunday evening's bright stage-lighting check should be flagged as a fit risk because the resulting glare sensitivity would undermine the quick microscope refocusing Monday's lab shift needs.",
        "broken": "I have a Monday lab shift, but this week's task is logging inventory from a printed sheet, no microscope work.",
    },
    {
        "slug": "eastward_flight_jetlag_before_safety_briefing",
        "a": "Whenever I fly eastward across several time zones, I'm wide awake at 3am my new local time and groggy and slow well past my usual wake-up hour for a couple of days.",
        "b": "I have an early morning flight-crew safety briefing on Tuesday where I need to demonstrate sharp reaction times on the emergency equipment checks.",
        "proposal": "A conference invites me to fly eastward across four time zones this weekend, landing Monday night.",
        "query": "Based only on these records, should flying eastward across four time zones this weekend be flagged as a fit risk for this user?",
        "c": "Flying eastward across four time zones this weekend should be flagged as a fit risk because the resulting jet lag would leave the user groggy and slow right when Tuesday's safety briefing needs sharp reaction times.",
        "broken": "I have an early morning flight-crew briefing on Tuesday, but it's been changed to a seated policy review with no equipment checks or reaction-time component.",
    },
    {
        "slug": "late_gaming_session_before_volunteer_hike_lead",
        "a": "Whenever I get into a late-night gaming session, I can't fall asleep before 2am even after I stop playing.",
        "b": "I'm leading a Saturday morning volunteer hike where I need to be alert enough to keep track of a dozen people on uneven trail.",
        "proposal": "Friends invite me to a new game's midnight launch event this Friday.",
        "query": "Based only on these records, should attending Friday's midnight game launch be flagged as a fit risk for this user?",
        "c": "Attending Friday's midnight game launch should be flagged as a fit risk because the resulting late sleep onset would leave the user under-rested right when Saturday's hike-leading role needs sustained alertness.",
        "broken": "I'm leading a Saturday morning info table at the trailhead this time, just handing out maps with no group to track on the trail.",
    },
    {
        "slug": "night_shift_switch_before_road_test",
        "a": "Whenever I switch from a night shift back to a day schedule, my reaction times stay noticeably slower for about two days while my body resets.",
        "b": "I have a driving-license renewal road test on Thursday morning where the examiner is grading my reaction time at intersections.",
        "proposal": "My manager wants me to cover one more night shift this week, ending Wednesday morning, right before switching back to days.",
        "query": "Based only on these records, should covering the extra night shift ending Wednesday be flagged as a fit risk for this user?",
        "c": "Covering the extra night shift ending Wednesday should be flagged as a fit risk because the shift-switch reaction-time slowdown would still be in effect right when Thursday's road test grades reaction time.",
        "broken": "I have a driving-license renewal appointment on Thursday morning, but it's just a vision and paperwork check this cycle, no road test.",
    },
    {
        "slug": "long_afternoon_nap_before_fasting_donation",
        "a": "Whenever I nap for more than ninety minutes in the afternoon, I'm still wide awake well past my normal bedtime that night.",
        "b": "I have an early morning blood donation appointment on Friday where I need to stay calm and fasted with steady vitals.",
        "proposal": "I've been catching up on sleep with long afternoon naps this week, including Thursday afternoon.",
        "query": "Based only on these records, should a long Thursday afternoon nap be flagged as a fit risk for this user?",
        "c": "A long Thursday afternoon nap should be flagged as a fit risk because the resulting delayed sleep onset would leave the user under-rested and less steady right when Friday's donation needs calm, steady vitals.",
        "broken": "I have a blood donation appointment on Friday, but it's just a screening interview this time with no draw and no vitals check.",
    },
    {
        "slug": "nightcap_before_trivia_finals",
        "a": "Whenever I have a nightcap drink before bed, my sleep is fragmented and I wake up several times through the night.",
        "b": "I'm competing in the trivia league finals on Tuesday evening where I need sharp, fast recall under time pressure.",
        "proposal": "Friends want to celebrate with a nightcap the night before Tuesday's finals.",
        "query": "Based only on these records, should having a nightcap the night before Tuesday's finals be flagged as a fit risk for this user?",
        "c": "Having a nightcap the night before Tuesday's finals should be flagged as a fit risk because the resulting fragmented sleep would blunt the sharp recall Tuesday's trivia finals need.",
        "broken": "I'm attending the trivia league's Tuesday evening social night this time, which is just casual hangout with no competition or scoring.",
    },
    {
        "slug": "storm_disrupted_sleep_before_certification_exam",
        "a": "Whenever a loud thunderstorm keeps waking me up overnight, I have noticeably poor concentration and make careless mistakes the next day.",
        "b": "I have a professional certification exam on Thursday morning that's timed and penalizes careless mistakes heavily.",
        "proposal": "The forecast shows thunderstorms rolling through Wednesday night, right before Thursday's exam.",
        "query": "Based only on these records, should Wednesday night's forecasted thunderstorms be flagged as a fit risk for this user?",
        "c": "Wednesday night's forecasted thunderstorms should be flagged as a fit risk because the sleep disruption they'd cause would produce the careless-mistake pattern right when Thursday's exam heavily penalizes exactly that.",
        "broken": "I have a certification exam on Thursday morning, but it's an open-book take-home format this cycle with no time pressure or penalty for small errors.",
    },
    {
        "slug": "late_heavy_lifting_before_meditation_retreat",
        "a": "Whenever I do a heavy weightlifting session after 8pm, I feel wired and it takes me much longer than usual to fall asleep.",
        "b": "I'm attending an early morning meditation retreat on Sunday where I need to sit calmly with a settled, unhurried mind.",
        "proposal": "My gym is offering a late evening heavy-lifting class Saturday night, right before Sunday's retreat.",
        "query": "Based only on these records, should Saturday night's late heavy-lifting class be flagged as a fit risk for this user?",
        "c": "Saturday night's late heavy-lifting class should be flagged as a fit risk because the resulting wired, delayed sleep onset would work against the settled, unhurried mind Sunday's meditation retreat needs.",
        "broken": "I'm attending an early morning coffee meetup on Sunday this time, just casual conversation with no meditation or sitting practice.",
    },
    {
        "slug": "late_heavy_dinner_before_swim_class",
        "a": "Whenever I eat a heavy dinner really late, indigestion keeps waking me up through the night.",
        "b": "I have an early morning swim class on Monday where I need to arrive on time and breathe steadily through the laps.",
        "proposal": "A late reservation opened up for a heavy tasting-menu dinner Sunday night, right before Monday's swim class.",
        "query": "Based only on these records, should Sunday night's late heavy tasting-menu dinner be flagged as a fit risk for this user?",
        "c": "Sunday night's late heavy tasting-menu dinner should be flagged as a fit risk because the indigestion-driven sleep disruption it causes would undercut the steady breathing Monday's swim class needs.",
        "broken": "I have a swim-class orientation on Monday morning this time, which is just a poolside talk with no laps or breathing component.",
    },
    {
        "slug": "clock_change_before_flight_connection",
        "a": "Whenever the clocks change for daylight saving, I feel noticeably groggy and slow to make decisions for a couple of days afterward.",
        "b": "I have a tight connecting flight on Monday where I need to make a fast gate-change decision at security.",
        "proposal": "This year's clock change falls on the Sunday right before Monday's tight connection.",
        "query": "Based only on these records, should this year's Sunday clock change be flagged as a fit risk for this user's Monday travel?",
        "c": "This year's Sunday clock change should be flagged as a fit risk for this user's Monday travel because the grogginess it causes would slow down the fast gate-change decision Monday's tight connection needs.",
        "broken": "I have a Monday flight this time, but it's a direct flight with no connection or gate-change decision required.",
    },
    {
        "slug": "restless_pet_wakeups_before_negotiation_call",
        "a": "Whenever my dog has a restless night, I get woken up repeatedly and feel foggy on details the next day.",
        "b": "I have a high-stakes negotiation call on Wednesday morning where I need to recall specific contract figures accurately.",
        "proposal": "My dog has been unsettled and restless the past two nights, including the night before Wednesday's call.",
        "query": "Based only on these records, should the dog's restless night before Wednesday's call be flagged as a fit risk for this user?",
        "c": "The dog's restless night before Wednesday's call should be flagged as a fit risk because the resulting foggy recall would undercut the accurate contract-figure recall Wednesday's negotiation needs.",
        "broken": "I have a call on Wednesday morning this time, but it's just a scheduling call to pick a future date, with no figures or details to recall.",
    },
    {
        "slug": "late_video_call_marathon_before_eye_exam",
        "a": "Whenever I do a marathon of back-to-back video calls into the evening, my eyes get dry and irritated and I sleep worse that night.",
        "b": "I have an eye exam on Friday morning where I need accurate visual acuity readings.",
        "proposal": "Work has scheduled a marathon of client video calls Thursday evening, right before Friday's exam.",
        "query": "Based only on these records, should Thursday evening's marathon of video calls be flagged as a fit risk for this user?",
        "c": "Thursday evening's marathon of video calls should be flagged as a fit risk because the eye strain and worse sleep it causes would undercut the accurate visual-acuity reading Friday's exam needs.",
        "broken": "I have an eye-clinic visit on Friday morning this time, but it's just picking up a repaired pair of glasses at the front desk, no vision testing.",
    },
    {
        "slug": "overseas_timezone_calls_before_equipment_inspection",
        "a": "Whenever I take a run of 1am calls for an overseas team, I build up a noticeable sleep debt over the following days.",
        "b": "I have a safety equipment inspection on Friday where I need to check every item carefully without missing a step.",
        "proposal": "The overseas team has scheduled a run of 1am calls this week, ending Thursday night, right before Friday's inspection.",
        "query": "Based only on these records, should this week's run of 1am overseas calls be flagged as a fit risk for this user?",
        "c": "This week's run of 1am overseas calls should be flagged as a fit risk because the sleep debt they build up would raise the risk of missing a step in Friday's careful equipment inspection.",
        "broken": "I have an equipment inspection on Friday this time, but it's a supplier's inspection with their own checklist and staff, so I'm just observing.",
    },
    {
        "slug": "late_carb_snacking_before_parent_teacher_conference",
        "a": "Whenever I snack heavily on carbs late at night, I get a blood sugar crash that wakes me up groggy and irritable in the morning.",
        "b": "I have a parent-teacher conference on Tuesday morning where I need to stay patient and communicate clearly.",
        "proposal": "I've been stress-snacking on carb-heavy food late at night this week, including Monday night before Tuesday's conference.",
        "query": "Based only on these records, should Monday night's late carb-heavy snacking be flagged as a fit risk for this user?",
        "c": "Monday night's late carb-heavy snacking should be flagged as a fit risk because the resulting blood-sugar-crash grogginess and irritability would undercut the patience Tuesday's conference needs.",
        "broken": "I have a parent-teacher conference on Tuesday morning this time, but it's been switched to a written email update with no meeting.",
    },
    {
        "slug": "skipped_wind_down_before_voiceover_session",
        "a": "Whenever I skip my wind-down routine and go straight from intense work into bed, my thoughts race and it takes a long time to fall asleep.",
        "b": "I have a voice-over recording session on Wednesday morning where I need a calm, steady voice for the whole session.",
        "proposal": "A late project deadline Tuesday night means skipping my wind-down routine again, right before Wednesday's session.",
        "query": "Based only on these records, should skipping Tuesday night's wind-down routine be flagged as a fit risk for this user?",
        "c": "Skipping Tuesday night's wind-down routine should be flagged as a fit risk because the racing thoughts and delayed sleep it causes would undercut the calm, steady voice Wednesday's recording session needs.",
        "broken": "I have a voice-over session on Wednesday morning this time, but it's just reviewing a finished recording with the engineer, no new takes to record.",
    },
    {
        "slug": "overnight_drive_before_woodworking_class",
        "a": "Whenever I drive through the night on a long haul, my reflexes stay noticeably slow for the rest of that day.",
        "b": "I have a woodworking class on Saturday afternoon where I need careful, precise control while operating the power tools.",
        "proposal": "A friend needs help with an overnight cross-country drive ending Saturday morning, right before Saturday afternoon's class.",
        "query": "Based only on these records, should helping with Saturday morning's overnight drive be flagged as a fit risk for this user?",
        "c": "Helping with Saturday morning's overnight drive should be flagged as a fit risk because the resulting slow reflexes would undercut the precise control Saturday afternoon's power-tool class needs.",
        "broken": "I have a woodworking class on Saturday afternoon this time, but it's a lecture-only session on wood types with no power tools involved.",
    },
    {
        "slug": "late_argument_before_mediation_session",
        "a": "Whenever I have an intense argument late in the evening, my heart races and I lie awake ruminating for hours before falling asleep.",
        "b": "I'm leading a mediation session on Thursday morning where I need to project a calm, settled demeanor.",
        "proposal": "A tense family disagreement is likely to come to a head Wednesday evening, right before Thursday's mediation session.",
        "query": "Based only on these records, should Wednesday evening's tense family disagreement be flagged as a fit risk for this user?",
        "c": "Wednesday evening's tense family disagreement should be flagged as a fit risk because the racing heart and rumination it causes would undercut the calm demeanor Thursday's mediation session needs.",
        "broken": "I'm attending Thursday morning's mediation training this time, which is just watching a recorded session with no live mediating.",
    },
    {
        "slug": "evening_nap_before_bp_screening_booth",
        "a": "Whenever I take a nap in the early evening, I can't fall asleep at my normal bedtime and end up shifting my whole night later.",
        "b": "I'm running an early morning blood-pressure screening booth on Saturday where I need to be punctual and keep a calm, steady affect with each visitor.",
        "proposal": "I've been so tired lately that I keep taking evening naps, including Friday evening before Saturday's booth shift.",
        "query": "Based only on these records, should Friday evening's nap be flagged as a fit risk for this user?",
        "c": "Friday evening's nap should be flagged as a fit risk because the resulting shifted, delayed sleep would work against the punctual, calm affect Saturday's screening booth shift needs.",
        "broken": "I'm helping set up Saturday morning's booth this time, which is just carrying tables and chairs before anyone else arrives, no visitor interaction.",
    },
    {
        "slug": "late_fluorescent_work_before_photography_session",
        "a": "Whenever I work late under bright fluorescent office lighting, I have a much harder time falling asleep once I finally get home.",
        "b": "I have a photography session on Thursday morning where I need a steady hand for close-up shots.",
        "proposal": "A project deadline means working under the office's fluorescent lights until midnight Wednesday, right before Thursday's session.",
        "query": "Based only on these records, should working under fluorescent lights until midnight Wednesday be flagged as a fit risk for this user?",
        "c": "Working under fluorescent lights until midnight Wednesday should be flagged as a fit risk because the resulting delayed sleep onset would undercut the steady hand Thursday's close-up photography session needs.",
        "broken": "I have a photography session on Thursday morning this time, but it's just reviewing printed proofs with the client, no camera work.",
    },
    {
        "slug": "fragmented_layover_sleep_before_interpreting_gig",
        "a": "Whenever I have a long overnight layover and try to sleep in the airport, my rest is badly fragmented and I feel foggy processing language the next day.",
        "b": "I have an interpreting gig on Monday morning where I need to process and translate fast-moving conversation accurately.",
        "proposal": "My connecting flight now has an overnight layover ending Monday morning, right before Monday's interpreting gig.",
        "query": "Based only on these records, should Monday morning's overnight-layover arrival be flagged as a fit risk for this user?",
        "c": "Monday morning's overnight-layover arrival should be flagged as a fit risk because the fragmented sleep it causes would undercut the fast, accurate language processing Monday's interpreting gig needs.",
        "broken": "I have an interpreting-related meeting on Monday morning this time, but it's just picking up my badge and schedule at the front desk, no live interpreting.",
    },
)

# ---------------------------------------------------------------------------
# Query-framing diversification (2026-07-28)
#
# Pairs 1-10 and 16-200 originally all used query_type=situational_fit
# ("should X be flagged as a fit risk"), leaving the batch at 195/200 (97.5%)
# on one query type -- far over this project's own DATA CRITERIA_new.md quota
# ("No query type exceeds 20% of the batch"). A framing-diversity smoke test
# (health-vnext-diversity-check-20260728b) compared this dominant phrasing
# against the 5 hand-authored alternate-framing items (pairs 11-15) and found
# the solver's "always say yes" pattern on the b_only/absence arms largely
# DISAPPEARED under alternate framings (b_only accuracy 0/5 -> 4/5, absence
# 3/5 -> 4/5), while a_only/link_broken failures replicated regardless of
# framing (0/5 -> 1/5 both) -- i.e. situational_fit's specific phrasing was
# priming affirmative answers on two of six arms, not just revealing a
# framing-independent memory failure.
#
# QUERY_FRAMING_OVERRIDES redistributes pairs 46-200 (155 items) across four
# alternate query_types, chosen because they map cleanly onto every item's
# existing A/B/proposal/broken shape (a repeated personal pattern colliding
# with a specific upcoming commitment) without altering the underlying facts
# -- only the query's phrasing and the calibrated target-conclusion (`c`)
# change. `a`/`b`/`proposal`/`broken` are untouched for every item.
#
# Resulting distribution across all 200 items: situational_fit 40 (20.0%),
# predicted_reaction 40 (20.0%), behavior_explanation 40 (20.0%),
# recommendation_ranking 40 (20.0%), conditional_recommendation 39 (19.5%),
# preference_generalization 1 (0.5%, pair 11 only -- its underlying shape,
# generalizing a mechanism from two same-type successes, doesn't map onto
# the single-exposure-vs-single-commitment shape the other 199 items share,
# so it was not forced onto ill-fitting content). Polarity: reject 80/200
# (40.0%, at but not over the 40% cap), accept 41/200 (20.5%), non_decision
# 40/200 (20.0%), conditional 39/200 (19.5%).
#
# The four frame templates below are deliberately generic/role-based (mirrors
# DEFAULT_FRAME's own style) rather than scenario-specific: every field they
# drive (relational_connector, retrieval_cue, relation_specificity,
# coactivation_bridge lead-in, arm_gold req_*/rationale_*) is validator/gold
# metadata, never sent to the solver (dataset.solver_input() only sends
# context+query -- confirmed earlier this session), so reusing one template
# per query_type across ~39 items each is not a duplication concern the way
# solver-visible text (dialogue, query wording) is. Only `query` and `c` are
# solver/validator-visible text and are authored per-item.
PREDICTED_REACTION_FRAME = {
    "query_type": "predicted_reaction",
    "polarity": "reject",
    "calibrated_language": "predicted to still apply",
    "relation": "A recovery-need pattern predicts a specific next-day impairment only when paired with a commitment that is sensitive to that impairment.",
    "excludes": ["the user is generally affected by this kind of exposure", "any next-day commitment would be affected"],
    "nearby_relation": "The user can have this kind of exposure on other occasions without any known sensitive next-day commitment.",
    "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-day commitment would be affected.",
    "ev_a_context": "A pattern that creates a recovery need affecting next-day functioning",
    "ev_a_goal": "Return to normal functioning by the next day",
    "ev_a_outcome": "Establishes a repeatable next-day impairment pattern",
    "ev_b_context": "A scheduled commitment sensitive to that specific impairment",
    "ev_b_goal": "Meet the commitment in an unimpaired state",
    "ev_b_outcome": "Creates the situational condition needed for latent C",
    "cue_type": "predicted_reaction",
    "why_it_naturally_retrieves": "The question asks for a prediction about the outcome without naming either prior episode.",
    "bridge_lead": "ev_A establishes the recovery-need pattern; ev_B establishes the specific commitment that pattern would affect.",
    "req_full": [
        "answer yes",
        "connect the recovery-need pattern with the specific next-day commitment",
        "cite both session 5 and session 12",
        "state the calibrated prediction",
    ],
    "rationale_full": "A and B jointly support the target proposition.",
    "req_a_only": [
        "answer no",
        "state that no specific next-day commitment is available",
        "withhold the target proposition",
    ],
    "rationale_a_only": "A alone does not establish that a specific next-day commitment would be affected.",
    "req_b_only": [
        "answer no",
        "state that no recovery-need pattern is available",
        "withhold the target proposition",
    ],
    "rationale_b_only": "B alone does not establish that the user would actually be impaired.",
    "req_link_broken": [
        "answer no",
        "identify that the replacement commitment no longer carries the same sensitivity",
        "withhold the target proposition",
    ],
    "rationale_link_broken": "B-prime removes the impairment-sensitivity of the commitment while retaining the same user, timing, and conversational form.",
    "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the specific sensitivity to the impairment.",
    "link_broken_rationale": "A plus B-prime no longer supports the original C.",
}

BEHAVIOR_EXPLANATION_FRAME = {
    "query_type": "behavior_explanation",
    "polarity": "non_decision",
    "calibrated_language": "supported as the explanation",
    "relation": "A recovery-need pattern explains a specific next-day shortfall only when paired with a commitment the shortfall would actually affect.",
    "excludes": ["the user sometimes feels off after this kind of exposure", "next-day commitments sometimes go poorly for unrelated reasons"],
    "nearby_relation": "The user can have this kind of exposure on other occasions without any known sensitive next-day commitment.",
    "why_it_does_not_license_C": "That fact does not by itself establish that this specific next-day shortfall shares a cause with a sensitive commitment.",
    "ev_a_context": "A pattern that creates a recovery need affecting next-day functioning",
    "ev_a_goal": "Identify why the shortfall happens",
    "ev_a_outcome": "Establishes a repeatable next-day impairment pattern",
    "ev_b_context": "A scheduled commitment sensitive to that specific impairment",
    "ev_b_goal": "Confirm whether the shortfall has a specific, identifiable cause",
    "ev_b_outcome": "Creates the situational condition needed for latent C",
    "cue_type": "behavior_explanation",
    "why_it_naturally_retrieves": "The question asks for an explanation without naming either prior episode.",
    "bridge_lead": "ev_A establishes the recovery-need pattern; ev_B establishes the specific commitment that pattern would affect.",
    "req_full": [
        "answer yes",
        "connect the recovery-need pattern with the specific next-day commitment",
        "cite both session 5 and session 12",
        "state the calibrated explanatory conclusion",
    ],
    "rationale_full": "A and B jointly support the target proposition.",
    "req_a_only": [
        "answer no",
        "state that no specific next-day commitment is available to explain",
        "withhold the target proposition",
    ],
    "rationale_a_only": "A alone is a recovery-need pattern without a specific commitment on record to explain.",
    "req_b_only": [
        "answer no",
        "state that no recovery-need pattern is available",
        "withhold the target proposition",
    ],
    "rationale_b_only": "B alone is a commitment without a confirmed recovery-need pattern to explain it.",
    "req_link_broken": [
        "answer no",
        "identify that the replacement commitment no longer carries the same sensitivity to explain",
        "withhold the target proposition",
    ],
    "rationale_link_broken": "B-prime removes the matching sensitivity while retaining the same user, timing, and conversational form.",
    "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the matching sensitivity.",
    "link_broken_rationale": "A plus B-prime no longer supports the original C.",
}

RECOMMENDATION_RANKING_FRAME = {
    "query_type": "recommendation_ranking",
    "polarity": "accept",
    "calibrated_language": "the recommended choice",
    "relation": "A recovery-need pattern makes declining or deferring the proposal the better choice only when the next day carries a specific commitment the pattern would affect.",
    "excludes": ["this kind of exposure is generally best avoided", "the user should avoid this kind of exposure in general"],
    "nearby_relation": "The user can usually recover from this kind of exposure within a day or two with no fixed commitment.",
    "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-day commitment would be affected.",
    "ev_a_context": "A pattern that creates a recovery need affecting next-day functioning",
    "ev_a_goal": "Recover functioning by the next day",
    "ev_a_outcome": "Establishes a repeatable next-day impairment pattern",
    "ev_b_context": "A scheduled commitment sensitive to that specific impairment",
    "ev_b_goal": "Perform well at a specific, fixed commitment",
    "ev_b_outcome": "Creates the situational condition needed for latent C",
    "cue_type": "recommendation_ranking",
    "why_it_naturally_retrieves": "The choice between proceeding with or declining the proposal asks for a ranked recommendation without naming either prior episode.",
    "bridge_lead": "ev_A establishes the recovery-need pattern; ev_B establishes the specific commitment that pattern would affect.",
    "req_full": [
        "answer yes",
        "connect the recovery-need pattern with the specific next-day commitment",
        "cite both session 5 and session 12",
        "state the calibrated recommendation",
    ],
    "rationale_full": "A and B jointly support the target proposition.",
    "req_a_only": [
        "answer no",
        "state that no specific next-day commitment is available",
        "withhold the target proposition",
    ],
    "rationale_a_only": "A alone does not establish that a specific next-day commitment would be affected.",
    "req_b_only": [
        "answer no",
        "state that no recovery-need pattern is available",
        "withhold the target proposition",
    ],
    "rationale_b_only": "B alone does not establish that the proposal would affect the commitment.",
    "req_link_broken": [
        "answer no",
        "identify that the replacement commitment is flexible and reschedulable",
        "withhold the target proposition",
    ],
    "rationale_link_broken": "B-prime removes the fixed sensitivity while retaining the same user, timing, and conversational form.",
    "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed next-day stake.",
    "link_broken_rationale": "A plus B-prime no longer supports the original C.",
}

CONDITIONAL_RECOMMENDATION_FRAME = {
    "query_type": "conditional_recommendation",
    "polarity": "conditional",
    "calibrated_language": "conditionally supported",
    "relation": "A recovery-need pattern makes proceeding with the proposal conditional on moving a fixed next-day commitment only when that commitment cannot otherwise be avoided.",
    "excludes": ["this kind of exposure is generally fine the night before a commitment", "the user should avoid this kind of exposure in general"],
    "nearby_relation": "The user can usually engage in this kind of exposure with no fixed commitment the next day.",
    "why_it_does_not_license_C": "That fact does not by itself establish that a specific next-day commitment would be affected.",
    "ev_a_context": "A pattern that creates a recovery need affecting next-day functioning",
    "ev_a_goal": "Recover functioning by the next day",
    "ev_a_outcome": "Establishes a repeatable next-day impairment pattern",
    "ev_b_context": "A scheduled commitment sensitive to that specific impairment",
    "ev_b_goal": "Perform a specific, fixed commitment",
    "ev_b_outcome": "Creates the situational condition needed for latent C",
    "cue_type": "conditional_recommendation",
    "why_it_naturally_retrieves": "The question about proceeding with the proposal asks for a conditional recommendation without naming either prior episode.",
    "bridge_lead": "ev_A establishes the recovery-need pattern; ev_B establishes the specific commitment that pattern would affect.",
    "req_full": [
        "answer yes",
        "connect the recovery-need pattern with the specific next-day commitment",
        "cite both session 5 and session 12",
        "state the calibrated conditional recommendation",
    ],
    "rationale_full": "A and B jointly support the target proposition.",
    "req_a_only": [
        "answer no",
        "state that no specific next-day commitment is available",
        "withhold the target proposition",
    ],
    "rationale_a_only": "A alone does not establish that a specific next-day commitment would be affected.",
    "req_b_only": [
        "answer no",
        "state that no recovery-need pattern is available",
        "withhold the target proposition",
    ],
    "rationale_b_only": "B alone does not establish that the proposal would affect the commitment.",
    "req_link_broken": [
        "answer no",
        "identify that the replacement commitment is now flexible with no fixed timing",
        "withhold the target proposition",
    ],
    "rationale_link_broken": "B-prime removes the fixed sensitivity while retaining the same user, timing, and conversational form.",
    "link_broken_connector_change": "B-prime preserves the same user, session position, and conversational style but removes the fixed next-day stake.",
    "link_broken_rationale": "A plus B-prime no longer supports the original C.",
}

# Populated by _load_query_framing_overrides() below from four JSON files
# (one per query_type, authored separately for each block of ~39 items).
# Maps slug -> {"query": ..., "c": ..., "frame": <one of the four templates
# above>}. Kept as a module-level dict built at import time so _candidate()
# can look it up the same way it looks up HEALTH_SCENARIOS.
QUERY_FRAMING_OVERRIDES: dict[str, dict[str, Any]] = {}


def _load_query_framing_overrides() -> dict[str, dict[str, Any]]:
    overrides: dict[str, dict[str, Any]] = {}
    block_dir = Path(__file__).parent / "health_query_framing"
    blocks = (
        ("framing_block_A.json", PREDICTED_REACTION_FRAME),
        ("framing_block_B.json", BEHAVIOR_EXPLANATION_FRAME),
        ("framing_block_C.json", RECOMMENDATION_RANKING_FRAME),
        ("framing_block_D.json", CONDITIONAL_RECOMMENDATION_FRAME),
    )
    for filename, frame_template in blocks:
        path = block_dir / filename
        if not path.is_file():
            continue
        entries = json.loads(path.read_text(encoding="utf-8"))
        for entry in entries:
            overrides[entry["slug"]] = {
                "query": entry["query"],
                "c": entry["c"],
                "frame": frame_template,
            }
    return overrides


QUERY_FRAMING_OVERRIDES = _load_query_framing_overrides()

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
    "keeps a running list of habits they're trying to build",
    "logs caffeine intake alongside sleep quality",
    "reviews continuous glucose monitor data most evenings",
    "blocks recovery time on the calendar after hard workouts",
    "checks the weather before committing to weekend plans",
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
    # --- Extension for the 200-item batch (pairs 16+ only). The original 20
    # entries above stay untouched at indices 0-19 so pairs 1-15 keep using
    # them exactly as before; pairs 16+ draw from the full extended pool via
    # a different selection formula (see _background_text). At ~185 new
    # items x ~17 filler slots each, a 20-entry pool would force heavy
    # cross-item filler repetition (pigeonhole: thousands of slots, 20
    # topics), so this extension exists specifically to keep that overlap
    # low, not to add narrative variety for its own sake.
    ("I skimmed a health newsletter over coffee.", "Passive reading can still plant useful ideas."),
    ("I reorganized my pillbox for the week.", "A visible system reduces the chance of missed doses."),
    ("I took a short break to stretch my wrists.", "Small breaks add up over a long day."),
    ("I charged my fitness tracker overnight.", "A charged device is one less friction point tomorrow."),
    ("I wiped down the kitchen counters after cooking.", "A quick reset can make the next meal easier."),
    ("I confirmed a ride for an appointment next week.", "Logistics handled early reduce day-of stress."),
    ("I read a few pages before turning off the light.", "A wind-down ritual can help mark the day's end."),
    ("I checked in on a friend who's been unwell.", "Checking in on others can be its own small reset."),
    ("I filed an old lab report into a folder.", "Keeping records organized pays off later."),
    ("I picked out clothes for a busy day ahead.", "A little prep can smooth out a rushed morning."),
    ("I skipped dessert and had fruit instead.", "Small substitutions can add up over time."),
    ("I answered a few emails before logging off.", "Closing loops early can protect the evening."),
    ("I took the stairs instead of the elevator.", "Small choices like that add up."),
    ("I labeled a few containers in the fridge.", "A little organization can prevent waste."),
    ("I reviewed my step count for the week.", "Tracking can highlight patterns you might otherwise miss."),
    ("I set a reminder to renew an insurance card.", "Catching it early avoids a last-minute scramble."),
    ("I swapped my usual coffee for decaf one afternoon.", "Small experiments can reveal useful patterns."),
    ("I tidied my desk before starting work.", "A clear space can make starting easier."),
    ("I looked up a recipe for a lighter dinner.", "Planning ahead can simplify the evening."),
    ("I jotted down a question for my next appointment.", "Writing questions down early avoids forgetting them."),
    ("I put fresh batteries in a home monitor device.", "Routine maintenance avoids surprises later."),
    ("I stretched my shoulders during a work break.", "Short resets can ease a long stretch at a desk."),
    ("I updated an emergency contact card in my wallet.", "A small update, but worth keeping current."),
    ("I skipped a second cup of coffee in the afternoon.", "Noticing the pattern is its own kind of data."),
    ("I packed a healthier lunch for the next day.", "A little prep the night before saves a decision later."),
    ("I reviewed a printed handout from a past visit.", "Revisiting notes can surface details you forgot."),
    ("I closed my laptop earlier than usual one night.", "An earlier stop can protect the rest of the evening."),
    ("I checked the expiration dates on a few supplements.", "A quick check avoids taking something past its date."),
    ("I took a short detour to avoid a noisy street.", "A quieter route can be its own small reset."),
    ("I wrote a one-line journal entry before bed.", "A short habit can still be a consistent one."),
    ("I rinsed out a water bottle to refill for tomorrow.", "A small habit that removes a morning decision."),
    ("I confirmed the time zone for a virtual appointment.", "Catching a mismatch early avoids missing the call."),
    ("I set aside a folder of receipts for reimbursement.", "A little sorting now saves a search later."),
    ("I looked over a shared calendar for scheduling conflicts.", "Seeing everything at once makes trade-offs clearer."),
    ("I did a few minutes of light tidying after work.", "A contained task can mark the end of the workday."),
    ("I tested a home blood pressure cuff for calibration.", "Confirming accuracy now avoids questioning a reading later."),
    ("I moved a plant to get more morning light.", "A small adjustment, low effort either way."),
    ("I reviewed a recipe's sodium content before cooking.", "A quick check can inform a small substitution."),
    ("I set a phone reminder for a follow-up call.", "External reminders protect intentions that are easy to forget."),
    ("I organized a folder of insurance paperwork.", "A little structure now avoids a scramble later."),
    ("I picked a lighter bag for a short errand.", "A small adjustment based on how the day is going."),
    ("I reviewed a discharge summary from an old visit.", "Old records can still be useful reference material."),
    ("I set out a reusable bag for tomorrow's errands.", "That's one less thing to remember in the morning."),
    ("I checked a weather forecast before planning the weekend.", "Planning around conditions can avoid a bad surprise."),
    ("I updated a contact number for a specialist's office.", "Keeping details current avoids a wasted call later."),
    ("I skimmed a wellness article shared by a coworker.", "Passive reading can still be useful context."),
    ("I sorted through a stack of old greeting cards.", "A low-effort task that gave a small sense of order."),
    ("I confirmed parking details for an upcoming appointment.", "Good to have that squared away ahead of time."),
    ("I tried a new stretch routine for five minutes.", "A short trial is a low-stakes way to test something new."),
    ("I reviewed a printed map for an unfamiliar clinic.", "Knowing the route ahead of time reduces last-minute stress."),
    ("I set my phone to do-not-disturb an hour early.", "A boundary like that can protect a wind-down routine."),
    ("I wrote down a list of current medications for reference.", "Having it written down helps in unexpected moments."),
    ("I reorganized a bathroom shelf of toiletries.", "A contained task gave a small sense of order."),
    ("I confirmed a co-pay amount before a scheduled visit.", "Knowing the cost ahead of time avoids a surprise."),
    ("I picked a quieter spot to eat lunch.", "A small environmental choice, low stakes either way."),
    ("I reviewed an old symptom log from a few months back.", "Old entries can reveal a pattern you forgot about."),
    ("I set a reminder to rotate an injection site.", "A small habit that protects against irritation over time."),
    ("I checked a pharmacy's hours before a planned pickup.", "A quick check avoids a wasted trip."),
    ("I looked over a benefits summary from open enrollment.", "Reviewing it now avoids confusion later in the year."),
    ("I tried a guided breathing exercise for a few minutes.", "A few minutes is enough to see if it helps."),
    ("I updated a fitness app with a new goal.", "Adjusting a target can keep it feeling realistic."),
    ("I sorted mail into bills and everything else.", "A quick sort makes the pile feel more manageable."),
    ("I reviewed an old x-ray report out of curiosity.", "Interesting to look back at, even without a specific reason."),
    ("I picked a earlier appointment slot than usual.", "A small scheduling choice, low stakes either way."),
    ("I confirmed a specialist referral was submitted.", "Following up early avoids a gap in scheduling."),
    ("I tidied a junk drawer that had been bothering me.", "Small, but satisfying to finally deal with."),
    ("I reviewed a printed exercise sheet from physical therapy.", "Revisiting instructions can surface a detail you forgot."),
    ("I set out vitamins for the week in a organizer.", "Sorting it out ahead of time saves a decision each morning."),
    ("I checked in with a sibling about a shared errand.", "Checking in on logistics is its own small task."),
    ("I looked over a printed nutrition label before buying.", "Worth a glance before it goes in the cart."),
    ("I confirmed an appointment reminder text went through.", "Catching a missed confirmation early avoids a no-show."),
    ("I reviewed a printed intake form before a visit.", "Filling it out ahead of time saves time at the desk."),
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


_FILLER_SESSION_IDS = tuple(range(1, 21))  # all 20, not just the ~17 real filler slots
# _candidate()'s initial context loop calls _background_text() once per
# session_id 1-20 unconditionally, before separately overwriting sessions
# 5, 12, and 20 (and 18 for the distractor arm) with real evidence/proposal/
# distractor content. Those overwritten calls' return values are discarded,
# but the call still happens, so this list has to cover the full domain the
# function is actually invoked with, not just the slots that survive.


def _background_text(pair_number: int, session_id: int) -> tuple[str, str]:
    # No longer applies a pair_number<=15 special case that preserved the
    # original linear-stride text verbatim: that text carried the same
    # "As someone who {persona}, ..." template defect this function used to
    # produce for every pair, so there is no reason to keep it just because
    # it was the first-tested batch. The persona-phrase wrapper this function
    # used to apply is gone entirely (see below) so no persona argument is
    # needed here any more; PERSONAS is unused for now and kept only as a
    # possible future hook (e.g. into provenance metadata), not decorative
    # dialogue text.
    #
    # A deterministic per-item random permutation (seeded by pair_number, so
    # still fully reproducible) avoids the periodic-collision problem a
    # linear stride formula had at 200-item scale (see prior version's
    # comment in git history for the measured 0.7 Jaccard collision).
    rng = random.Random(f"assomem-health-pilot-filler-{pair_number}")
    order = rng.sample(range(len(BACKGROUND_TOPICS)), k=len(_FILLER_SESSION_IDS))
    index = order[_FILLER_SESSION_IDS.index(session_id)]
    text, reply = BACKGROUND_TOPICS[index]
    # Previously this line prepended f"As someone who {persona}, " and
    # lowercased the topic's first letter to fit grammatically after that
    # clause. That wrapper was mechanical filler glued onto ~85% of every
    # item's sessions (17-18 of 20) with no relation between the persona
    # phrase and the sentence that followed it -- the opposite of the
    # organically-voiced background text finance's data uses. Returning the
    # topic text as-is (it is already a complete, natural first-person
    # sentence in BACKGROUND_TOPICS) removes the template without needing to
    # hand-rewrite the whole pool.
    return text, reply


def _annotations(context: list[dict[str, Any]], user_id: str, a_text: str, b_text: str, frame: dict[str, Any]) -> dict[str, Any]:
    annotations: dict[str, Any] = {}
    for session in context:
        sid = str(session["session_id"])
        annotations[sid] = {"role": "background_memory", "summary": "Non-target health memory."}
    annotations["5"] = {
        "role": "ev_A",
        "event_elements": {
            "person": user_id,
            "context": frame["ev_a_context"],
            "goal_or_prediction": frame["ev_a_goal"],
            "action": a_text,
            "outcome_or_affect": frame["ev_a_outcome"],
        },
    }
    annotations["12"] = {
        "role": "ev_B",
        "event_elements": {
            "person": user_id,
            "context": frame["ev_b_context"],
            "goal_or_prediction": frame["ev_b_goal"],
            "action": b_text,
            "outcome_or_affect": frame["ev_b_outcome"],
        },
    }
    annotations["20"] = {"role": "retrieval_cue", "summary": "Later fit question."}
    return annotations


def _core_gold(frame: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "full": {
            "expected_mode": "infer_C",
            "binary_decision": True,
            "required_elements": list(frame["req_full"]),
            "rationale": frame["rationale_full"],
        },
        "a_only": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": list(frame["req_a_only"]),
            "rationale": frame["rationale_a_only"],
        },
        "b_only": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": list(frame["req_b_only"]),
            "rationale": frame["rationale_b_only"],
        },
        "link_broken": {
            "expected_mode": "withhold_C",
            "binary_decision": False,
            "required_elements": list(frame["req_link_broken"]),
            "rationale": frame["rationale_link_broken"],
        },
    }


def _candidate(pair_number: int, source_arm: str) -> dict[str, Any]:
    scenario = HEALTH_SCENARIOS[pair_number - 1]
    framing_override = QUERY_FRAMING_OVERRIDES.get(scenario["slug"])
    if framing_override is not None:
        scenario = {**scenario, "query": framing_override["query"], "c": framing_override["c"]}
        scenario_frame = framing_override["frame"]
    else:
        scenario_frame = scenario.get("frame", {})
    frame = {**DEFAULT_FRAME, **scenario_frame}
    # These five are resolved from the scenario's own frame override when
    # present (the 5 diversity scenarios each hand-author their own), or a
    # per-item deterministic pool pick otherwise -- see the POOL definitions
    # and _pooled_pick() above for why. DEFAULT_FRAME intentionally no longer
    # carries these keys, so a plain dict-merge fallback isn't an option here.
    ev_a_reply = scenario_frame.get("ev_a_reply") or _pooled_pick(EV_A_REPLY_POOL, pair_number, "ev_a_reply")
    ev_b_reply = scenario_frame.get("ev_b_reply") or _pooled_pick(EV_B_REPLY_POOL, pair_number, "ev_b_reply")
    proposal_reply = scenario_frame.get("proposal_reply") or _pooled_pick(PROPOSAL_REPLY_POOL, pair_number, "proposal_reply")
    link_broken_reply = scenario_frame.get("link_broken_reply") or _pooled_pick(LINK_BROKEN_REPLY_POOL, pair_number, "link_broken_reply")
    user_id = f"anon_health_user_{pair_number:02d}"
    pair_id = f"AMB_HV_{scenario['slug']}_{pair_number:03d}"
    start = datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc)
    context = []
    for session_id in range(1, 21):
        timestamp = start + timedelta(days=session_id * 3)
        text, reply = _background_text(pair_number, session_id)
        context.append(_session(session_id, timestamp, user_id, text, reply))
    context[4] = _session(5, start + timedelta(days=15), user_id, scenario["a"], ev_a_reply)
    context[11] = _session(12, start + timedelta(days=36), user_id, scenario["b"], ev_b_reply)
    context[19] = _session(20, start + timedelta(days=60), user_id, scenario["proposal"], proposal_reply)
    annotations = _annotations(context, user_id, scenario["a"], scenario["b"], frame)
    core_gold = _core_gold(frame)
    candidate = {
        "schema_version": "assomem-vnext-1.2",
        "candidate_id": f"{pair_id}_{source_arm}",
        "pair_id": pair_id,
        "domain": "health",
        "user_id": user_id,
        "query_type": frame["query_type"],
        "polarity": frame["polarity"],
        "context": context,
        "query": scenario["query"],
        "evidence": {
            "ev_A": {"session_id": 5, "owner": user_id, "fact": scenario["a"]},
            "ev_B": {"session_id": 12, "owner": user_id, "fact": scenario["b"]},
        },
        "episode_annotations": annotations,
        "relational_connector": {
            "relation": frame["relation"],
            "requires_evidence": ["ev_A", "ev_B"],
            "excludes": list(frame["excludes"]),
            "link_broken_change": "The next-day activity is replaced with a low-stakes, movable activity.",
        },
        "connector_spans": [
            {"evidence_id": "ev_A", "session_id": 5, "quote": scenario["a"].split(".")[0]},
            {"evidence_id": "ev_B", "session_id": 12, "quote": scenario["b"].split(".")[0]},
        ],
        "retrieval_cue": {
            "cue_type": frame["cue_type"],
            "why_it_naturally_retrieves_R": frame["why_it_naturally_retrieves"],
        },
        "relation_specificity": {
            "nearby_relation": frame["nearby_relation"],
            "why_it_does_not_license_C": frame["why_it_does_not_license_C"],
        },
        "coactivation_bridge": f"{frame['bridge_lead']} Together they support C: {scenario['c']}",
        "latent_C": {"inference": scenario["c"], "calibrated_language": frame["calibrated_language"]},
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
                {"role": "assistant", "content": link_broken_reply},
            ],
            "connector_change": frame["link_broken_connector_change"],
            "rationale": frame["link_broken_rationale"],
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
        if "distractor_text" in scenario_frame:
            distractor_text = scenario_frame["distractor_text"]
            distractor_reply = scenario_frame["distractor_reply"]
            distractor_summary = scenario_frame["distractor_summary"]
        else:
            distractor_text, distractor_reply, distractor_summary = _pooled_pick(
                DISTRACTOR_POOL, pair_number, "distractor"
            )
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
                distractor_text,
                distractor_reply,
            )
        }
        candidate["context"][17] = candidate["distractor"]["added_session"]
        candidate["episode_annotations"]["18"] = {"role": "distractor", "summary": distractor_summary}
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
        abs_text5, abs_reply5, abs_text12, abs_reply12 = _pooled_pick(
            ABSENCE_REPLACEMENT_POOL, pair_number, "absence"
        )
        candidate["context"][4] = _session(5, start + timedelta(days=15), user_id, abs_text5, abs_reply5)
        candidate["context"][11] = _session(12, start + timedelta(days=36), user_id, abs_text12, abs_reply12)
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

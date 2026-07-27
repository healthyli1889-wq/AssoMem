"""Ten social-demand families, the U01-U10 object swaps, and the neutral filler pool.

Design principle, v2
--------------------

The v1 batch failed its own Stage 7 screen: with both target episodes removed the
solver still answered `yes` on 11 of 16 items, while answering `no` on all 16 with
an empty context. The background was not leaking the episodes - the *proposition*
was simply true by common sense. "Do not go to a big dinner the night before a
hard conversation" needs no memory of this person at all.

So every target proposition here is **counter-conventional**: A and B jointly
license the answer that generic social advice gets wrong.

    reject  items propose the conventionally sensible option, which this user's
            episodes show is a poor fit for them specifically
    accept  items propose the conventionally reckless option, which this user's
            episodes show actually works for them

A solver with no memory applies the convention and answers `no` on both, which is
gold for every ablation arm. Only A+B together flip it to `yes`. That is the gap
the ladder is supposed to measure.

Two structural rules follow from the same failure:

1. **B must not restate A's antecedent.** A supplies trigger -> mediator state;
   B supplies mediator state -> outcome. Neither half alone completes the chain.
   In v1, B said "the morning after one of those", which made B self-sufficient.
2. **Counterexamples must not be contrastive foils.** v1 used lines like "so it
   isn't the hour, no", which presuppose the target pattern and hand it to the
   solver. They are now ordinary neutral episodes.

The v1 `supporting_constraint` sessions (E1/E2) are gone. They were a finance-batch
invention, not a DATA CRITERIA requirement, and ablating them showed they leaked
(absence answered `yes` 9/10 with them, 7/10 without). The 20-session budget is now
exactly section 3's: 2 targets + 2 counterexamples + 15 background + 1 cue.

The five bridge types are each used by two scenarios:

    state_dependent_operation      S1, S6
    strategy_outcome_contingency   S2, S8
    threshold_context_interaction  S3, S7
    preference_constraint_fit      S4, S9
    prediction_calibration         S5, S10
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Neutral background filler: ordinary social admin. Enough to establish a person
# with a real social life, never enough to replace ev_A or ev_B, and carrying no
# hint of any scenario's target pattern.
# --------------------------------------------------------------------------

FILLER: tuple[tuple[str, str, str], ...] = (
    ("moved two things on the calendar and called that admin done.", "productive?", "generously described."),
    ("finally replied to the thread from last week.", "how late is late?", "nine days. a personal best."),
    ("someone sent a photo from years ago and derailed my afternoon.", "worth it?", "completely."),
    ("muted one group and un-muted another. net zero.", "any peace?", "about forty minutes of it."),
    ("walked the long way home and didn't check my phone.", "deliberate?", "half deliberate."),
    ("made a playlist for a thing that hasn't been planned yet.", "optimistic.", "aspirational, really."),
    ("booked the haircut I've been putting off since spring.", "which slot?", "an evening one, obviously."),
    ("left a voice note instead of typing. felt strange.", "faster?", "faster. stranger."),
    ("cleaned the kitchen instead of answering anything.", "avoidance?", "structured avoidance."),
    ("skimmed the invites and closed the tab.", "decide anything?", "no. classic."),
    ("someone changed the group name again.", "improvement?", "debatable."),
    ("ate standing up reading a thread I wasn't in.", "why?", "no defence."),
    ("found a birthday I'd forgotten and covered it with a message.", "did it land?", "seemed to."),
    ("said maybe to two things I already knew the answer to.", "which answer?", "you know which."),
    ("re-read something I sent and winced slightly.", "that bad?", "just the tone."),
    ("put my phone in a drawer for an hour.", "and?", "checked it twice from across the room."),
    ("agreed to be somewhere without checking the day.", "brave.", "reckless, more like."),
    ("sorted the photos from the last thing into a folder nobody will open.", "including you?", "including me."),
    ("had a coffee alone and it was the best part of the day.", "low bar?", "comfortable bar."),
    ("someone asked how I was and I answered honestly by accident.", "how did that go?", "surprisingly fine."),
    ("declined a thing politely and then felt weird about it for an hour.", "regret?", "not really. just weird."),
    ("wrote half a message and left it in the box.", "sending it?", "eventually. probably."),
    ("looked up how far away a place is instead of asking.", "and?", "further than the invite implied."),
    ("borrowed a charger and forgot to give it back. again.", "same person?", "same person, third time."),
    ("watched something everyone had already discussed.", "spoiled?", "thoroughly."),
    ("did the laundry and answered nothing for three hours.", "restorative?", "quietly, yes."),
    ("someone rescheduled and I was more relieved than I should admit.", "admitting it now.", "under duress."),
    ("stood outside a place for ten minutes before going in.", "nerves?", "just gathering."),
    ("made a list of people to check on. didn't check on them.", "the list helped?", "the list existed."),
    ("got the train instead of driving and read most of the way.", "better?", "much."),
    ("turned off read receipts and told nobody.", "strategic.", "purely defensive."),
    ("swapped a call for a message and everyone was fine with it.", "relief?", "enormous."),
    ("bought a card and didn't write in it yet.", "deadline?", "self-imposed and slipping."),
    ("sat in the same seat as last time out of habit.", "noticed?", "only by me."),
    ("someone summarised a two-hundred-message thread for me.", "accurate?", "kind, at least."),
    ("said I'd host something and immediately regretted the scale.", "downsizing?", "quietly, yes."),
    ("left a party early and nobody minded.", "expected worse?", "much worse."),
    ("put a recurring reminder on something I'll ignore.", "why bother?", "hope."),
    ("checked the weather for a plan that isn't confirmed.", "keen.", "or anxious."),
    ("tidied one shelf and stopped.", "momentum?", "a rumour of momentum."),
    ("answered the family thread first, as usual.", "priority?", "unspoken but real."),
    ("agreed on a date by elimination over four days.", "efficient.", "eventually."),
    ("printed something I could have shown on a phone.", "why?", "felt more like a real plan."),
    ("lost twenty minutes to a map of somewhere I'm not going.", "planning?", "wandering."),
)

# --------------------------------------------------------------------------
# Matched replacement sessions for a_only / b_only / absence. Kept separate from
# FILLER and spanning a wide length range so a replacement can be length-matched
# to the target session it stands in for: if the ablation is systematically
# shorter than `full`, a measured drop can be a reaction to context length rather
# than to the missing evidence.
# --------------------------------------------------------------------------

REPLACEMENT_FILLER: tuple[tuple[str, str, str], ...] = (
    ("filed a couple of things and moved on.", "anything odd?", "nothing worth typing."),
    ("did a nothing pass over the calendar this morning.", "exceptions?", "none."),
    ("closed a boring loop that had been open a while.", "follow-up?", "just a note for next time."),
    (
        "spent twenty minutes tidying the shared album from the last thing and gave up halfway.",
        "how far did you get?",
        "about a third. it can stay like that.",
    ),
    (
        "went through the unread pile properly for once and answered the easy ones, which was most of them.",
        "and the hard ones?",
        "still sitting there, obviously.",
    ),
    (
        "did a full pass over the whole calendar this afternoon, moved three things, cancelled one, and renamed a recurring entry that has had the wrong name since last year.",
        "productive, then?",
        "administratively, yes. otherwise nothing happened at all.",
    ),
    (
        "sat down and worked out who I actually owe a reply to, wrote the list out, then answered exactly none of them because it was late by the time the list existed.",
        "the list helped?",
        "the list existed. that's as far as it got.",
    ),
    (
        "spent most of the evening sorting old photos into folders by year, which turned into reading old threads instead, which turned into it being midnight.",
        "worth it?",
        "not by any measure I'd defend out loud.",
    ),
    (
        "did the weekly tidy: cleared the counter, put the recycling out, changed the sheets, and made a note about the tap that's been dripping since spring.",
        "the tap getting fixed?",
        "the note is the fix, for now.",
    ),
    (
        "walked the long way back and worked out that the reason my week feels full is that I've said yes to three things that are all admin rather than anything I'd have chosen.",
        "any of them droppable?",
        "one, maybe. I'll think about it and then not do anything.",
    ),
    (
        "went through the notifications backlog, muted four things, archived a couple of threads that finished months ago, and turned off two reminders I have never once acted on.",
        "any quieter?",
        "measurably quieter, yes. for about a day.",
    ),
    (
        "ended up rearranging the shelf instead of doing the thing I sat down to do, and then rearranged it back because the first version was better.",
        "net progress?",
        "net zero, with extra steps.",
    ),
    (
        "wrote out the month on paper to see it properly, realised two things clash, moved neither, and put the paper in a drawer where I will not look at it again.",
        "so the clash stands?",
        "the clash stands. it's a future problem now.",
    ),
    (
        "did the boring round of admin I've been putting off: two forms, one renewal, one address change, and a phone call that took nine minutes of hold music.",
        "all done?",
        "all done. no ceremony, which feels wrong somehow.",
    ),
    ("skimmed the invites and closed the tab without deciding.", "again?", "again."),
    (
        "cleared out the drafts folder, which was mostly half-written messages to people I have since spoken to about something else entirely.",
        "send any?",
        "deleted all of them. it was the right call.",
    ),
)

QUERY_TYPE_FRAMES: dict[str, str] = {
    "situational_fit": "{base} — does that actually fit how I work?",
    "preference_generalization": "{base} — is that generally true of me, or was that just the one time?",
    "recommendation_ranking": "{base} — of those two, which should I be putting first?",
    "predicted_reaction": "{base} — if I go ahead with it, how does it actually go for me?",
    "behavior_explanation": "{base} — why does this particular thing go the way it does for me?",
    "conditional_recommendation": "{base} — under what conditions should I be saying yes to this?",
}


SCENARIOS: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S1
    {
        "s": 1,
        "slug": "group_night_before_repair_talk",
        "family": "large-group warm-up versus a rested start before a repair conversation",
        "bridge_type": "state_dependent_operation",
        "convention": "Do not go out the night before a difficult conversation; arrive rested.",
        "mediator": "the warm, unguarded state",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 17},
        "a": (
            "the morning after {a_obj} I'm warm and loose — generous, unguarded, saying what I actually mean instead of managing it.",
            "how long does that last?",
            "till about two. it's the size of the thing that does it, not how late I get back.",
        ),
        "b": (
            "every clear-the-air conversation of mine that actually landed, I went into warm and unguarded. the ones I went into rested and sharp, I turned clipped and legalistic and made it worse.",
            "so being on form hurts?",
            "with those specific conversations, yes. every single time.",
        ),
        "lb": (
            "I've gone into those conversations both warm and sharp by now, and honestly it made no odds either way — they go how they go.",
            "no pattern?",
            "none I can find. the state just doesn't touch it.",
        ),
        "cx": [
            ("did a short lunch with one person midweek. pleasant, unremarkable.", "worth repeating?", "probably, yeah."),
            ("skipped a thing I'd said yes to and nobody noticed.", "guilt?", "briefly. then nothing."),
        ],
        "dist": (
            "{circle} are adamant that you never regret an early night before something that matters.",
            "adamant?",
            "loudly, and with total confidence.",
        ),
        "a_objs": [
            "the big Thursday table", "the res-hall block night", "the Sunday long table",
            "the full match-day group", "the after-concert supper", "the whole group chat turning up",
            "the book-group-plus-partners thing", "the neighbourhood street party",
            "the gallery afterparty", "the full workshop-circle dinner",
        ],
        "unconv": [
            "the twenty-person send-off dinner", "the all-night res party",
            "the long birthday table with everyone", "the full pre-match pub night",
            "the post-opera supper with the whole circle", "the house-warming that runs late",
            "the theatre night with drinks after for the whole group", "the comedy-night group thing",
            "the late gig plus afters", "the panel with drinks after for everyone",
        ],
        "conv": [
            "a quiet early night in on my own", "an early night alone in my room",
            "a quiet evening at home by myself", "an early night with no plans at all",
            "a quiet evening in with an early bed", "an early night alone before it",
            "a quiet evening at home on my own", "an early night in with the phone off",
            "a quiet night alone at the flat", "an early, deliberately quiet evening alone",
        ],
        "commits": [
            "the clear-the-air talk with my brother", "the honest conversation with my roommate",
            "the money talk with my cousin", "the apology I owe my old teammate",
            "the difficult conversation with my sister-in-law", "the talk about the lease with my flatmate",
            "the overdue conversation with my mother-in-law", "the hard talk with my landlord's daughter",
            "the conversation I've been dodging with my ex-flatmate", "the boundary conversation with my in-law",
        ],
        "nearby_relation": "This user enjoys large gatherings.",
        "why_not_license": (
            "An unremarkable midweek lunch and a skipped commitment say nothing about what a "
            "large-group night does to this user's state, and nothing about which state their "
            "difficult conversations actually go well in."
        ),
        "query_unconv": "{circle} want me at {unconv} the night before {commit}",
        "query_conv": "I was going to have {conv} the night before {commit}",
        "a_elements": {
            "context": "mornings after {a_obj}",
            "goal_or_prediction": "see what the next morning is like",
            "action": "went to the full-group version",
            "outcome_or_affect": "warm, unguarded and generous until early afternoon",
        },
        "b_elements": {
            "context": "clear-the-air conversations across several years",
            "goal_or_prediction": "resolve things properly",
            "action": "went into some warm and unguarded, others rested and sharp",
            "outcome_or_affect": "only the warm ones landed; rested ones turned clipped and made it worse",
        },
        "cue_why": (
            "A friend-group invitation lands against something already booked, which forces a "
            "personalised call without naming either episode or the link between them."
        ),
    },
    # ---------------------------------------------------------------- S2
    {
        "s": 2,
        "slug": "tidy_digest_over_rambling_note",
        "family": "efficient broadcast updates versus unedited one-to-one rambling",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Keeping people updated clearly and regularly is how you stay close.",
        "mediator": "the unedited rambling register",
        "slots": {"a": 5, "b": 13, "cx": [2, 9], "dist": 17},
        "a": (
            "when I'm keeping something tidy and regular I write in headlines — short, clean, decisive, every hedge taken out. it's the clearest I ever am.",
            "people like it?",
            "they say it's the easiest thing of mine to read, yeah.",
        ),
        "b": (
            "the friendships of mine that survived at any distance ran entirely on long unedited rambling. the ones I kept up with clean regular updates quietly died — nobody feels close to a status report.",
            "even good ones?",
            "especially the good ones. they read like a newsletter and got treated like one.",
        ),
        "lb": (
            "I've kept people up both ways since — tidy and rambling — and the friendships went exactly the same either way.",
            "no difference?",
            "none I can point at. the format just isn't the thing.",
        ),
        "cx": [
            ("sorted the group logistics thread into something usable. took ten minutes.", "appreciated?", "two thumbs-ups, which is the maximum available."),
            ("someone asked for my address and I sent it within the hour.", "efficient.", "one for the records."),
        ],
        "dist": (
            "{circle} keep saying a regular clear update is obviously the kindest way to keep people in your life.",
            "obviously?",
            "that's how they put it, yes.",
        ),
        "a_objs": [
            "the weekly round-up", "the tidy family update", "the Sunday summary",
            "the match-day recap", "the monthly note", "the course-group digest",
            "the book-group update", "the neighbourhood bulletin",
            "the gallery-night write-up", "the workshop recap",
        ],
        "unconv": [
            "one long unedited voice note a week", "a rambling unstructured message whenever",
            "a long meandering note with no point to it", "an unedited stream-of-thought message",
            "one long unpolished letter that goes nowhere", "a rambling late-night message",
            "a long unedited message with no structure", "an unpolished ramble whenever it occurs to me",
            "a long unedited voice memo", "one rambling uncomposed note a week",
        ],
        "conv": [
            "a tidy weekly digest to everyone", "a clean regular family update",
            "a neat Sunday summary to the group", "a tidy recap after each one",
            "a clear monthly note to everyone", "a well-organised group digest",
            "a tidy update to the whole book group", "a clean regular bulletin",
            "a neat write-up sent round", "a tidy regular summary",
        ],
        "commits": [
            "the friendship with my oldest flatmate", "the thread with my grandmother",
            "the friendship with my cousin abroad", "the weekly thing with my brother",
            "the correspondence with my old colleague", "the friendship with my school best friend",
            "the friendship with the one from the book group", "the friendship with my former neighbour",
            "the friendship with the person I shared a studio with", "the thread with my oldest friend",
        ],
        "nearby_relation": "This user is good at organised communication.",
        "why_not_license": (
            "Tidying a logistics thread and answering a request promptly both show competence at "
            "clear communication, but neither says what register this user's close friendships "
            "actually survive on."
        ),
        "query_unconv": "thinking of switching {commit} to {unconv}",
        "query_conv": "thinking of putting {commit} onto {conv} like everything else",
        "a_elements": {
            "context": "periods of keeping something tidy and regular",
            "goal_or_prediction": "be clear and easy to read",
            "action": "wrote in clean decisive headlines",
            "outcome_or_affect": "the clearest register this user has",
        },
        "b_elements": {
            "context": "distance friendships kept up over years in both registers",
            "goal_or_prediction": "keep the friendships alive",
            "action": "some got long unedited rambling, others clean regular updates",
            "outcome_or_affect": "only the rambling ones survived; the tidy ones quietly died",
        },
        "cue_why": (
            "A routine question about how to keep in touch reaches the register this user's "
            "closeness actually depends on, without naming it or the friendships it cost."
        ),
    },
    # ---------------------------------------------------------------- S3
    {
        "s": 3,
        "slug": "stacked_short_hangs_over_one_dinner",
        "family": "one planned proper sit-down versus several unpolished short catch-ups",
        "bridge_type": "threshold_context_interaction",
        "convention": "One proper unhurried dinner beats several rushed coffees.",
        "mediator": "the unpolished, stopped-performing state",
        "slots": {"a": 7, "b": 15, "cx": [3, 12], "dist": 18},
        "a": (
            "the first couple of {a_obj} in a week I'm still doing the polished version of myself. by the third or fourth I've run out of performance and just talk.",
            "run out?",
            "completely. no energy left to manage how I'm coming across.",
        ),
        "b": (
            "every time someone has actually told me something serious, it was never at a planned proper sit-down. it was always one of the unpolished ones, where I'd stopped trying.",
            "never at the planned ones?",
            "not once. those stay pleasant and say nothing.",
        ),
        "lb": (
            "people have told me serious things at the planned sit-downs and at the scrappy ones about equally, now I think about it.",
            "so it's not the setting?",
            "doesn't look like it. no pattern either way.",
        ),
        "cx": [
            ("had two catch-ups in one afternoon and enjoyed both.", "tiring?", "less than expected."),
            ("moved a coffee twice and it still happened.", "persistence.", "on their part, mostly."),
        ],
        "dist": (
            "{circle} keep telling me one proper unhurried dinner is worth five rushed coffees.",
            "worth five?",
            "their maths, not mine.",
        ),
        "a_objs": [
            "short coffee catch-ups", "quick campus coffees", "half-hour market coffees",
            "twenty-minute pre-match pints", "short gallery-cafe sits", "quick canteen catch-ups",
            "short interval drinks", "quick community-centre coffees",
            "short pre-gig catch-ups", "brief workshop-break coffees",
        ],
        "unconv": [
            "a third and fourth short coffee this week", "two more quick campus catch-ups before Friday",
            "another two rushed market coffees", "two more twenty-minute pints this week",
            "two extra short gallery-cafe sits", "another pair of quick canteen catch-ups",
            "two more short interval drinks", "two extra quick centre coffees",
            "another two short pre-gig catch-ups", "two more brief break coffees",
        ],
        "conv": [
            "one carefully planned proper dinner instead", "a proper unhurried sit-down instead",
            "one long planned lunch instead", "a proper booked dinner instead",
            "one carefully arranged long evening instead", "a proper planned meal instead",
            "one unhurried booked dinner instead", "a proper planned sit-down instead",
            "one long arranged evening instead", "a proper unhurried planned lunch instead",
        ],
        "commits": [
            "whatever my sister has been trying to tell me", "whatever my roommate keeps almost saying",
            "whatever my father hasn't said outright", "whatever my old teammate is going through",
            "whatever my neighbour has been hinting at", "whatever my coursemate isn't coping with",
            "whatever the one from the book group is carrying", "whatever the person two doors down is dealing with",
            "whatever my studio friend keeps deflecting", "whatever someone in the circle isn't saying",
        ],
        "nearby_relation": "This user can manage several social commitments in a week.",
        "why_not_license": (
            "Two catch-ups in an afternoon and a twice-moved coffee show only that the logistics "
            "are survivable; neither says what state this user has to be in before anyone tells "
            "them anything real."
        ),
        "query_unconv": "there's room for {unconv} on top of what's already in the week",
        "query_conv": "thinking of clearing the week and doing {conv}",
        "a_elements": {
            "context": "weeks containing different numbers of {a_obj}",
            "goal_or_prediction": "see how many is too many",
            "action": "kept going past the second one",
            "outcome_or_affect": "performance runs out; plain talking starts",
        },
        "b_elements": {
            "context": "occasions when people disclosed something serious",
            "goal_or_prediction": "be someone people can tell things to",
            "action": "attended both planned sit-downs and unpolished catch-ups",
            "outcome_or_affect": "disclosures only ever happened at the unpolished ones",
        },
        "cue_why": (
            "An ordinary scheduling question about how to spend the week runs straight at the "
            "state this user has to reach, without naming it or the disclosures it produced."
        ),
    },
    # ---------------------------------------------------------------- S4
    {
        "s": 4,
        "slug": "unprepared_toast_over_written_card",
        "family": "a carefully written card versus speaking unprepared",
        "bridge_type": "preference_constraint_fit",
        "convention": "If you are not a natural speaker, write it down; a written note is safer and more personal.",
        "mediator": "the unprepared, messy register",
        "slots": {"a": 4, "b": 12, "cx": [2, 8], "dist": 18},
        "a": (
            "anything I write for a person I over-edit. I keep sanding it down until it's correct and completely cold — what comes out reads like a reference letter.",
            "every time?",
            "every time I have the chance to revise it, yes.",
        ),
        "b": (
            "the two times anything I said actually landed with someone, I was speaking unprepared in front of people and it came out messy and true. nobody has ever once quoted back a thing I wrote them.",
            "not once?",
            "not once, and I've written a lot of them.",
        ),
        "lb": (
            "people have quoted back things I wrote and things I said about equally, thinking about it. no pattern in which stuck.",
            "so the format's neutral?",
            "seems to be. it doesn't decide anything.",
        ),
        "cx": [
            ("wrote the group a short logistics note and it did its job.", "clear?", "unambiguous, at least."),
            ("said a couple of words to three people in a kitchen. fine, unremarkable.", "nervous?", "not really, no."),
        ],
        "dist": (
            "{circle} are convinced a handwritten card is always the warmer, safer way to do this.",
            "always?",
            "they're very sure about it.",
        ),
        "a_objs": [
            "a written note", "a long handwritten card", "a proper letter",
            "a written message I've drafted", "a written note in an envelope", "a long written message",
            "a written note tucked into a book", "a handwritten card",
            "a written note left where they'll find it", "a written letter",
        ],
        "b_objs": [
            "the leaving drinks", "the res-hall farewell", "the family lunch",
            "the end-of-season do", "the anniversary dinner", "the course social",
            "the book-group anniversary", "the street-party thank-yous",
            "the gallery opening", "the workshop showcase",
        ],
        "unconv": [
            "standing up and saying it unprepared", "an unrehearsed speech in front of the hall",
            "saying it off the cuff at the lunch", "an unprepared thank-you in front of everyone",
            "standing up and speaking without notes", "an unrehearsed few words at the social",
            "saying it unprepared to the whole book group", "an off-the-cuff thank-you at the party",
            "speaking unprepared at the opening", "an unrehearsed tribute at the showcase",
        ],
        "conv": [
            "a carefully written card instead", "a properly drafted letter instead",
            "a carefully written note instead", "a well-drafted card instead",
            "a carefully composed letter instead", "a properly written note instead",
            "a carefully drafted card instead", "a properly composed note instead",
            "a carefully written letter instead", "a properly drafted note instead",
        ],
        "commits": [
            "the person being thanked", "my closest friend on the corridor",
            "my aunt", "the teammate who covered for me all season",
            "my husband", "the coursemate who got me through the year",
            "the friend who founded the book group", "the neighbour who organises everything",
            "the friend who lent me the studio", "the person who ran the workshop for free",
        ],
        "nearby_relation": "This user writes clearly and can speak in front of people.",
        "why_not_license": (
            "A functional group logistics note and a few words in a kitchen show basic competence "
            "in both formats; neither says which one this user's appreciation actually survives."
        ),
        "query_unconv": "{circle} want me to thank {commit} at {b_obj} — thinking of {unconv}",
        "query_conv": "thinking of thanking {commit} with {conv} rather than saying anything at {b_obj}",
        "a_elements": {
            "context": "years of writing things for people",
            "goal_or_prediction": "get the wording right",
            "action": "revised until it was correct",
            "outcome_or_affect": "reads formal and cold, like a reference letter",
        },
        "b_elements": {
            "context": "occasions when something this user expressed actually landed",
            "goal_or_prediction": "have the appreciation register",
            "action": "spoke unprepared in front of people on two of them",
            "outcome_or_affect": "only the unprepared ones were remembered; nothing written was ever quoted",
        },
        "cue_why": (
            "A group planning a thank-you asks a natural format question that runs at the user's "
            "fit constraint without naming it or the evidence behind it."
        ),
    },
    # ---------------------------------------------------------------- S5
    {
        "s": 5,
        "slug": "long_visit_over_protected_solo_time",
        "family": "protected solo recharge versus a house with people in it",
        "bridge_type": "prediction_calibration",
        "convention": "Protect your alone time; a long houseguest stay will drain you.",
        "mediator": "a house with people in it",
        "slots": {"a": 6, "b": 15, "cx": [4, 10], "dist": 13},
        "a": (
            "I was certain {a_obj} would recharge me. it doesn't — given a whole empty day I spiral, and I come out the other side worse than I went in.",
            "you predicted the opposite?",
            "confidently. I'd have argued the point.",
        ),
        "b": (
            "the stretches where there were people in the house constantly are the ones where I got most done and felt steadiest all year. I'd have bet money against that.",
            "steadier with people around?",
            "measurably. it's the thing I've been most wrong about.",
        ),
        "lb": (
            "I've had full houses and empty ones since and honestly they came out about the same — no clear winner either way.",
            "so it doesn't matter?",
            "doesn't look like it does, no.",
        ),
        "cx": [
            ("had someone over for one evening. nice, easy, no aftermath.", "repeat?", "happily."),
            ("spent a Saturday out and about instead of at home.", "restful?", "different, anyway."),
        ],
        "dist": (
            "{circle} keep warning me that a long stay will wreck me and I should protect my own time.",
            "confident about it?",
            "extremely. it's practically received wisdom.",
        ),
        "a_objs": [
            "my Saturday morning alone", "my one quiet evening a week", "my Sunday off the grid",
            "my Saturday-morning nobody-block", "my two quiet afternoons", "my one no-plans day",
            "my Friday evening alone", "my Sunday quiet morning",
            "my one screen-free evening", "my slow Sunday alone",
        ],
        "unconv": [
            "the ten-day stay", "a three-week houseguest run", "the full fortnight visit",
            "a nine-day stopover", "the month-long family stay", "the whole reading-week visit",
            "the twelve-day stay", "the three-week visit",
            "the two-week houseguest stretch", "the month of overlapping guests",
        ],
        "conv": [
            "keeping {a_obj} protected right through it", "ring-fencing {a_obj} regardless",
            "holding {a_obj} back for myself", "keeping {a_obj} untouched",
            "protecting {a_obj} the whole way through", "ring-fencing {a_obj} as usual",
            "keeping {a_obj} entirely to myself", "holding {a_obj} clear",
            "protecting {a_obj} throughout", "keeping {a_obj} ring-fenced",
        ],
        "commits": [
            "my cousin's visit", "my sister's stay", "my parents' trip over",
            "my brother's stopover", "my in-laws' visit", "my friend's reading-week stay",
            "my mother's fortnight here", "my old flatmate's stay",
            "my sibling's visit", "my friend's extended stay",
        ],
        "nearby_relation": "This user copes fine with short visits and busy weekends.",
        "why_not_license": (
            "One easy evening guest and a Saturday spent out both cost nothing, so neither "
            "calibrates a multi-week stay, and neither says which arrangement this user actually "
            "comes out of steadier."
        ),
        "query_unconv": "{circle} are asking about {unconv} for {commit}",
        "query_conv": "planning on {conv} during {commit}",
        "a_elements": {
            "context": "weeks built around {a_obj}",
            "goal_or_prediction": "predicted the protected time would recharge them",
            "action": "kept the block empty",
            "outcome_or_affect": "spiralled; came out worse than they went in",
        },
        "b_elements": {
            "context": "long stretches with people in the house continuously",
            "goal_or_prediction": "expected to be drained by it",
            "action": "lived through several such stretches",
            "outcome_or_affect": "most productive and steadiest periods of the year",
        },
        "cue_why": (
            "A family-visit request naturally raises the trade against this user's own time "
            "without naming the failed prediction or the stretch that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S6
    {
        "s": 6,
        "slug": "late_night_before_early_favour",
        "family": "an early night versus short sleep before an early commitment to someone",
        "bridge_type": "state_dependent_operation",
        "convention": "Get an early night before an early start you have promised someone.",
        "mediator": "the short-sleep, unhesitating state",
        "slots": {"a": 5, "b": 14, "cx": [3, 11], "dist": 18},
        "a": (
            "on about five hours I lose the part of me that hesitates. blunt, decisive, no rehearsing — I just do the thing and think about it later.",
            "reliably?",
            "reliably. it's the most useful I get, oddly.",
        ),
        "b": (
            "the early favours I've actually turned up for and done properly were the ones I hadn't slept on. fully rested I talk myself out of it somewhere on the way and cancel.",
            "you cancel when you're rested?",
            "every time. I find a reasonable-sounding excuse and take it.",
        ),
        "lb": (
            "I've turned up rested and I've turned up wrecked and the favours went about the same either way.",
            "no difference?",
            "not one I can point at. sleep just isn't the variable.",
        ),
        "cx": [
            ("had a late one with nothing on the next day. no harm done.", "worth it?", "at the time, definitely."),
            ("got a full night before an ordinary Tuesday. unremarkable.", "and?", "and nothing. it was Tuesday."),
        ],
        "dist": (
            "{circle} are adamant I should get a proper early night before something someone's relying on.",
            "adamant?",
            "unanimously so.",
        ),
        "a_objs": [
            "five hours", "a short night", "not much sleep",
            "four or five hours", "a short night's sleep", "very little sleep",
            "a short night", "five hours at most",
            "not much sleep at all", "a short night again",
        ],
        "unconv": [
            "the long late dinner the night before", "the party that runs past two the night before",
            "the late birthday dinner the night before", "the late awards do the night before",
            "the late anniversary supper the night before", "the end-of-term night out before it",
            "the late closing-night dinner before it", "the long fundraiser night before",
            "the late album launch the night before", "the long dinner after the last session",
        ],
        "conv": [
            "a proper early night before it", "an early night and a full eight hours before it",
            "getting a full night's sleep before it", "an early night before it",
            "a proper full night before it", "an early night and a decent sleep before it",
            "a full night's sleep before it", "an early night beforehand",
            "a proper early night the night before", "a full eight hours before it",
        ],
        "commits": [
            "the airport run for my friend", "the early train to my aunt's",
            "the market van I promised to load", "the early lift for my teammate",
            "the early appointment I said I'd go to", "the early move-out help I promised",
            "the early drive to my friend's ceremony", "the early shift at the food bank",
            "the early studio handover", "the early setup I said I'd cover",
        ],
        "nearby_relation": "This user's sleep varies and they cope either way.",
        "why_not_license": (
            "A late night with an empty next day and a full night before an ordinary Tuesday both "
            "cost nothing and reveal nothing about whether this user actually turns up for things "
            "they have promised."
        ),
        "query_unconv": "{circle} are planning {unconv} before {commit}",
        "query_conv": "planning on {conv} before {commit}",
        "a_elements": {
            "context": "days following {a_obj} of sleep",
            "goal_or_prediction": "see what short sleep does",
            "action": "operated on a short night repeatedly",
            "outcome_or_affect": "blunt, decisive, no hesitation",
        },
        "b_elements": {
            "context": "early commitments made to other people",
            "goal_or_prediction": "turn up for people who asked",
            "action": "approached some rested and some unrested",
            "outcome_or_affect": "only the unrested ones happened; rested attempts got talked out of",
        },
        "cue_why": (
            "An invitation lands the night before something promised to a person, forcing a "
            "personalised call without naming either episode."
        ),
    },
    # ---------------------------------------------------------------- S7
    {
        "s": 7,
        "slug": "drop_in_before_standing_call",
        "family": "a protected clear day versus a day whose plan has already broken",
        "bridge_type": "threshold_context_interaction",
        "convention": "Keep the day clear so you can give the call your full attention.",
        "mediator": "a day whose plan has already broken",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 13},
        "a": (
            "once one unplanned thing has wrecked the day's shape, I stop defending the schedule and finally do whatever I've been putting off for weeks. the plan being intact is exactly what keeps me stalling.",
            "the plan is the problem?",
            "the plan is absolutely the problem.",
        ),
        "b": (
            "the standing calls I've actually done properly were the days everything else had already fallen apart. on the tidy days I keep them to eight minutes and say nothing real.",
            "eight minutes?",
            "about that. pleasant, and completely empty.",
        ),
        "lb": (
            "I've had those calls on wrecked days and on clear days and they came out much the same.",
            "no pattern?",
            "none. the state of the day doesn't seem to do anything.",
        ),
        "cx": [
            ("someone came by for twenty minutes and then left. easy.", "disruptive?", "not remotely."),
            ("had a completely clear Thursday and enjoyed it.", "did much?", "not a thing, deliberately."),
        ],
        "dist": (
            "{circle} say the obvious thing is to keep the day clear so I can give it proper attention.",
            "the obvious thing.",
            "that's the framing, yes.",
        ),
        "a_objs": [
            "drop-in at the door", "knock on the res-room door", "someone turning up at the flat",
            "someone appearing at the door", "an unannounced caller", "someone turning up at my room",
            "someone arriving unannounced", "someone at the door with no warning",
            "someone turning up at the studio", "someone appearing unannounced",
        ],
        "unconv": [
            "letting someone drop in unannounced that day", "saying yes to a spontaneous room visit that day",
            "letting someone turn up with no warning that day", "taking an unplanned visit that day",
            "letting an unannounced caller in that day", "saying yes to a spur-of-the-moment visit that day",
            "letting someone arrive unannounced that day", "taking an unplanned drop-in that day",
            "letting someone turn up at the studio that day", "taking a no-notice visit that day",
        ],
        "conv": [
            "keeping the day completely clear for it", "protecting the whole day for it",
            "keeping the day free so I can focus on it", "clearing the day around it",
            "keeping the day entirely clear beforehand", "protecting the day so I'm properly there",
            "keeping the whole day clear for it", "clearing everything else off that day",
            "keeping the day protected for it", "holding the day clear for it",
        ],
        "commits": [
            "the standing Tuesday call with my sibling", "the Sunday call home",
            "the weekly call with my father", "the Wednesday call with my brother",
            "the standing call with my sister", "the Thursday call with my mum",
            "the standing call with my closest friend", "the weekly call with my nan",
            "the standing Monday call with my oldest friend", "the weekly call with my sibling",
        ],
        "nearby_relation": "This user is flexible about visitors and about free days.",
        "why_not_license": (
            "A brief easy visit and a pleasant empty Thursday both passed without consequence, so "
            "neither shows what a broken plan does for this user, nor which days their standing "
            "calls actually go anywhere."
        ),
        "query_unconv": "someone from {circle} wants to drop by on a day {commit} is due",
        "query_conv": "planning on {conv} on the day {commit} is due",
        "a_elements": {
            "context": "days containing one unplanned {a_obj}",
            "goal_or_prediction": "keep the day's plan",
            "action": "let the plan break",
            "outcome_or_affect": "stopped stalling and did the avoided thing",
        },
        "b_elements": {
            "context": "standing calls across many weeks",
            "goal_or_prediction": "keep the standing rhythm meaningful",
            "action": "held them on both tidy and collapsed days",
            "outcome_or_affect": "only the collapsed-day calls went anywhere; tidy ones stayed empty",
        },
        "cue_why": (
            "A friendly spontaneous visit is proposed on a day already carrying a standing "
            "commitment, without naming what either does for this user."
        ),
    },
    # ---------------------------------------------------------------- S8
    {
        "s": 8,
        "slug": "daily_reactions_over_long_letter",
        "family": "the composed monthly letter versus uncomposed daily reactions",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "A proper long letter shows real care; throwaway reactions are shallow.",
        "mediator": "the uncomposed daily register",
        "slots": {"a": 4, "b": 13, "cx": [2, 10], "dist": 18},
        "a": (
            "when I sit down to write {a_obj} I perform. it turns into an essay about my life with all the hard parts edited out and a neat ending stuck on.",
            "deliberately?",
            "not deliberately. it just happens once I'm composing something.",
        ),
        "b": (
            "the friendships at distance that stayed real are the ones where I was just reacting to their stuff daily with nothing composed. the ones I wrote proper letters to got a curated stranger and drifted.",
            "the letters made it worse?",
            "the letters made me a character. yeah.",
        ),
        "lb": (
            "I've done both with people abroad now and the friendships went the same either way.",
            "so composing doesn't matter?",
            "apparently not. no difference I can see.",
        ),
        "cx": [
            ("sent a long message about a trip and it was well received.", "detailed?", "exhaustively."),
            ("reacted to a few things on my phone in a queue.", "meaningful?", "not particularly."),
        ],
        "dist": (
            "{circle} reckon a proper written letter is obviously the version that shows you care.",
            "obviously?",
            "with total confidence, yes.",
        ),
        "a_objs": [
            "the long letter", "the long voice note", "the proper monthly email",
            "the long written update", "the letter-length message", "the long monthly note",
            "the long email", "the monthly written catch-up",
            "the long written letter", "the long monthly letter",
        ],
        "unconv": [
            "just reacting to their posts daily with nothing composed", "throwaway daily replies to their stories",
            "quick daily pings with no thought in them", "daily one-line reactions",
            "uncomposed daily replies to whatever they post", "daily throwaway check-ins",
            "quick uncomposed daily reacts", "daily one-word replies to their stuff",
            "uncomposed daily reactions to their posts", "daily throwaway reacts",
        ],
        "conv": [
            "keeping the long monthly letter going", "sticking with the proper composed letter",
            "keeping up the proper monthly email", "carrying on with the long written update",
            "keeping the letter-length message going", "sticking with the long monthly note",
            "keeping the long composed email going", "carrying on with the written catch-up",
            "keeping the long written letter going", "sticking with the monthly letter",
        ],
        "commits": [
            "the friend who moved abroad", "my cousin who emigrated",
            "the friend who moved to another continent", "my brother who moved overseas",
            "my friend who resettled overseas", "my school friend who moved away",
            "the friend from the book group who moved countries", "my former neighbour who emigrated",
            "the friend who moved to another city years ago", "my oldest friend who moved abroad",
        ],
        "nearby_relation": "This user can write at length and also keep up light daily contact.",
        "why_not_license": (
            "A well-received trip write-up and some idle reactions in a queue show both registers "
            "are available; neither says which one this user's distance friendships actually "
            "survive on."
        ),
        "query_unconv": "thinking of swapping to {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "sitting down to compose {a_obj}",
            "goal_or_prediction": "say something real",
            "action": "composed it properly",
            "outcome_or_affect": "an edited performance with the hard parts removed",
        },
        "b_elements": {
            "context": "distance friendships kept up in both registers",
            "goal_or_prediction": "stay genuinely close at distance",
            "action": "some got uncomposed daily reactions, others proper letters",
            "outcome_or_affect": "only the uncomposed ones stayed real; the letter ones drifted",
        },
        "cue_why": (
            "A plausible habit question reaches the register this user's distance friendships run "
            "on, without naming the register or the friendships it cost."
        ),
    },
    # ---------------------------------------------------------------- S9
    {
        "s": 9,
        "slug": "overnight_guest_before_mentoring",
        "family": "an empty house versus company the night before giving guidance",
        "bridge_type": "preference_constraint_fit",
        "convention": "Clear your evening and rest so you can give someone your best advice.",
        "mediator": "the concrete, example-led state",
        "slots": {"a": 7, "b": 14, "cx": [3, 12], "dist": 19},
        "a": (
            "with the place to myself the night before, I overthink everything into theory. I turn up with a framework nobody asked for and a diagram.",
            "every time?",
            "whenever I've had a quiet evening to build one, yes.",
        ),
        "b": (
            "the sessions where I actually helped anyone, I'd been talking to a real person the night before and I turned up with examples instead of a framework.",
            "examples work better?",
            "it's the only thing that's ever worked, honestly.",
        ),
        "lb": (
            "I've gone in off quiet nights and busy ones by now and the sessions came out about the same.",
            "so the night before is neutral?",
            "looks that way. nothing rides on it.",
        ),
        "cx": [
            ("had someone stay over on a week with nothing on. lovely, easy.", "any cost?", "none at all."),
            ("had a quiet evening in and read most of a book.", "restful?", "genuinely, yes."),
        ],
        "dist": (
            "{circle} think the obviously generous and sensible call is to keep the evening clear and rest up.",
            "sensible.",
            "hard to argue with out loud.",
        ),
        "a_objs": [
            "mentor someone", "tutor my coursemate", "talk someone through a decision",
            "coach the junior side", "advise on someone's application", "help a coursemate plan",
            "talk the newer members through it", "help someone with their CV",
            "give feedback on someone's portfolio", "run the one-to-one",
        ],
        "unconv": [
            "having someone stay over the night before", "putting up a visiting friend the night before",
            "hosting my cousin overnight beforehand", "putting up a teammate the night before",
            "hosting a guest overnight beforehand", "letting a coursemate crash the night before",
            "putting up a friend the night before", "hosting someone overnight beforehand",
            "letting a friend stay over the night before", "putting someone up the night before",
        ],
        "conv": [
            "keeping the place empty and resting the night before", "having a quiet evening alone beforehand",
            "keeping the evening completely clear beforehand", "resting alone the night before",
            "keeping the house to myself the night before", "having a quiet night in beforehand",
            "keeping the evening free and quiet beforehand", "having the place to myself the night before",
            "keeping the night before completely quiet", "resting up alone the night before",
        ],
        "commits": [
            "the mentoring session", "the tutoring session",
            "the decision talk with my cousin", "the coaching session with the junior side",
            "the application review", "the planning session with my coursemate",
            "the session with the new book-group members", "the CV session at the centre",
            "the portfolio feedback session", "the one-to-one session",
        ],
        "nearby_relation": "This user enjoys both hosting and quiet evenings.",
        "why_not_license": (
            "An easy overnight guest on an empty week and a restful evening with a book both went "
            "fine on their own terms; neither says which of the two produces guidance worth "
            "anything the next day."
        ),
        "query_unconv": "{circle} are asking about {unconv} {commit}",
        "query_conv": "planning on {conv} {commit}",
        "a_elements": {
            "context": "quiet nights before having to {a_obj}",
            "goal_or_prediction": "prepare properly",
            "action": "spent the evening alone thinking it through",
            "outcome_or_affect": "arrived with abstract frameworks nobody asked for",
        },
        "b_elements": {
            "context": "sessions that actually helped the other person",
            "goal_or_prediction": "say something useful",
            "action": "had been talking to a real person the night before",
            "outcome_or_affect": "arrived with concrete examples; the only thing that has worked",
        },
        "cue_why": (
            "A hosting request lands the night before something the user has committed to do well, "
            "without naming the fit constraint or the evidence for it."
        ),
    },
    # ---------------------------------------------------------------- S10
    {
        "s": 10,
        "slug": "stacked_video_hangs_before_reunion",
        "family": "arriving fresh versus arriving talked-out at an in-person reunion",
        "bridge_type": "prediction_calibration",
        "convention": "Clear your week so you arrive fresh and energetic for the reunion.",
        "mediator": "the talked-out, listening state",
        "slots": {"a": 5, "b": 15, "cx": [2, 9], "dist": 12},
        "a": (
            "I assumed stacking {a_obj} would leave me socially wrung out. what actually happens is I arrive talked-out — nothing left of my own to say, so I just listen.",
            "you expected the opposite?",
            "completely. I'd have argued it.",
        ),
        "b": (
            "the gatherings where people told me anything real were the ones where I said almost nothing. the ones I turned up fresh and full of my own news, I talked over everyone and came away knowing nothing.",
            "fresh is worse?",
            "for finding anything out, much worse.",
        ),
        "lb": (
            "I've turned up to those both talked-out and fresh and they came out about the same.",
            "no difference?",
            "none worth reporting. it doesn't seem to matter.",
        ),
        "cx": [
            ("had one call this week and it was fine.", "long?", "twenty minutes, no drama."),
            ("cleared a weekend and did very little with it.", "restful?", "adequately."),
        ],
        "dist": (
            "{circle} say the sensible thing is to keep the week clear so I turn up fresh for it.",
            "the sensible thing.",
            "that's the consensus, anyway.",
        ),
        "a_objs": [
            "video hangs", "video calls with the group", "long video calls",
            "group video calls", "video calls with the family", "video hangs with the course group",
            "video calls with the book group", "video calls with the regulars",
            "video hangs with the gallery friends", "video calls with the circle",
        ],
        "b_objs": [
            "the reunion lunch", "the res-hall reunion", "the family reunion",
            "the team reunion", "the anniversary lunch", "the course reunion",
            "the book-group reunion", "the neighbourhood reunion",
            "the studio reunion", "the workshop reunion",
        ],
        "unconv": [
            "five video hangs the week of it", "four group calls that same week",
            "six long calls the week before", "five group calls that week",
            "four family calls the same week", "five course calls that week",
            "four book-group calls the week before", "five calls with the regulars that week",
            "four gallery calls the same week", "five circle calls the week of it",
        ],
        "conv": [
            "keeping the week before it completely clear", "clearing the whole week beforehand",
            "keeping the week free so I turn up fresh", "clearing the calls out of that week",
            "keeping that week clear beforehand", "clearing the week so I arrive fresh",
            "keeping the week before it free", "clearing everything out of that week",
            "keeping the week ahead of it clear", "clearing the diary that week",
        ],
        "commits": [
            "the reunion lunch", "the res-hall reunion",
            "the family reunion", "the team reunion",
            "the anniversary lunch", "the course reunion",
            "the book-group reunion", "the neighbourhood reunion",
            "the studio reunion", "the workshop reunion",
        ],
        "nearby_relation": "This user is comfortable on video calls and with free weekends.",
        "why_not_license": (
            "A single ordinary call and a quiet cleared weekend both passed without consequence, "
            "so neither bounds the failed prediction, and neither says which state this user "
            "actually hears anything in."
        ),
        "query_unconv": "{circle} are scheduling {unconv} before {commit}",
        "query_conv": "planning on {conv} before {commit}",
        "a_elements": {
            "context": "a week of stacked {a_obj}",
            "goal_or_prediction": "predicted it would leave them socially wrung out",
            "action": "stacked the calls and went anyway",
            "outcome_or_affect": "arrived talked-out with nothing of their own to say, so listened",
        },
        "b_elements": {
            "context": "gatherings attended in both states",
            "goal_or_prediction": "come away actually knowing how people are",
            "action": "arrived at some with nothing to say and at others fresh and full of news",
            "outcome_or_affect": "only the quiet arrivals produced real disclosures",
        },
        "cue_why": (
            "Ordinary scheduling of catch-up calls lands in the week before something the user "
            "wants to get something out of, without naming the prediction or its correction."
        ),
    },
)


# --------------------------------------------------------------------------
# Target propositions. `full` gold is always yes, because the proposition is by
# construction what A+B support (DATA CRITERIA section 5.1). Polarity chooses
# which option is put to the user, and every proposition contradicts the
# convention recorded on the scenario.
# --------------------------------------------------------------------------

C_TEMPLATES: dict[str, tuple[str, str]] = {
    "accept": (
        "{unconv} before {commit} is a good fit for this user.",
        "go ahead with {unconv}",
    ),
    "reject": (
        "{conv} before {commit} is a poor fit for this user.",
        "do not rely on {conv}",
    ),
    "conditional": (
        "{unconv} is worth it before {commit} only in so far as it actually puts this user into "
        "{mediator}; without that it buys them nothing.",
        "worth it only in so far as it produces {mediator}",
    ),
    "non_decision": (
        "Whether {unconv} helps before {commit} turns on whether it puts this user into "
        "{mediator}, which the visible record does not settle for this occasion.",
        "turns on {mediator}, which the record does not settle here",
    ),
}


RELATIONS: dict[str, str] = {
    "group_night_before_repair_talk": (
        "Large-group nights leave this user warm and unguarded until early afternoon, and their "
        "clear-the-air conversations only ever landed when they went in warm — the rested, sharp "
        "ones turned clipped and made things worse. The conventional advice to arrive rested is "
        "backwards for this person."
    ),
    "tidy_digest_over_rambling_note": (
        "Keeping something tidy and regular puts this user into a clean headline register, and the "
        "friendships of theirs that survived distance ran entirely on unedited rambling while the "
        "cleanly-updated ones died. Their clearest register is the one that costs them closeness."
    ),
    "stacked_short_hangs_over_one_dinner": (
        "Past the second short catch-up in a week this user runs out of performance and simply "
        "talks, and every serious disclosure anyone has made to them came at one of those "
        "unpolished occasions rather than at a planned sit-down."
    ),
    "unprepared_toast_over_written_card": (
        "Given the chance to revise, this user sands anything written into something formal and "
        "cold, and the only times their appreciation ever registered were the unprepared spoken "
        "ones — nothing they wrote has ever been quoted back."
    ),
    "long_visit_over_protected_solo_time": (
        "This user confidently predicted protected solo time would recharge them and it does the "
        "opposite, while the stretches with people continuously in the house were their steadiest "
        "and most productive — the prediction was inverted, not merely miscalibrated."
    ),
    "late_night_before_early_favour": (
        "On a short night this user loses the part of them that hesitates, and the early favours "
        "they actually turned up for were the unrested ones; rested, they talk themselves out of "
        "it on the way and cancel."
    ),
    "drop_in_before_standing_call": (
        "Once an unplanned arrival has broken the day's shape this user stops defending the "
        "schedule and does what they have been avoiding, and their standing calls only went "
        "anywhere on those collapsed days — the tidy ones stayed eight empty minutes."
    ),
    "daily_reactions_over_long_letter": (
        "Composing a long letter turns this user into an edited performance of themselves, and "
        "the distance friendships that stayed real ran on uncomposed daily reactions while the "
        "properly-written ones drifted."
    ),
    "overnight_guest_before_mentoring": (
        "A quiet evening alone sends this user into abstraction and they arrive with a framework "
        "nobody asked for, while the sessions that actually helped followed a night spent talking "
        "to a real person and arrived carrying examples."
    ),
    "stacked_video_hangs_before_reunion": (
        "This user predicted stacked calls would leave them wrung out; instead they arrive "
        "talked-out and therefore listening, and the gatherings where anyone told them anything "
        "real were exactly the ones they turned up to with nothing of their own to say."
    ),
}


def scenario_for(index: int) -> dict:
    for scenario in SCENARIOS:
        if scenario["s"] == index:
            return scenario
    raise KeyError(f"no scenario S{index}")

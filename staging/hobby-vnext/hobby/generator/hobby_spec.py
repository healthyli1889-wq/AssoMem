"""Hobby scenario families S1-S10, plus the filler pools and proposition templates.

Built to the construct rules the social batch arrived at by measurement:

- Every target proposition is **counter-conventional**. Practice advice is dense
  with folk wisdom ("little and often", "buy decent tools", "finish what you
  start"), which makes it the ideal domain for this: a solver with no memory of
  the person applies the maxim and answers `no`, which is gold for every ablation
  arm. Only A+B together flip it to `yes`.
- ev_A gives trigger -> mediator state and fixes the **scope** of that state;
  ev_B gives mediator state -> outcome. B never restates A's antecedent.
- Mediator states are described specifically but **without valence**.
- Counterexamples are ordinary neutral episodes, never contrastive foils.

Bridge types run two per scenario across S1-S10 and again across S11-S20:

    state_dependent_operation      S1, S6      strategy_outcome_contingency   S2, S8
    threshold_context_interaction  S3, S7      preference_constraint_fit      S4, S9
    prediction_calibration         S5, S10
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Neutral background: ordinary hobby admin. Enough to establish someone with a
# practice, never enough to replace ev_A or ev_B, and carrying no hint of any
# scenario's target pattern.
# --------------------------------------------------------------------------

FILLER: tuple[tuple[str, str, str], ...] = (
    ("restrung it and immediately put it down again.", "not playing?", "admiring, mostly."),
    ("watched a tutorial all the way through without trying any of it.", "learn anything?", "in theory."),
    ("reorganised the shelf by colour. took an hour.", "improvement?", "aesthetically."),
    ("bought a thing I already own a version of.", "why?", "no defence prepared."),
    ("cleaned everything instead of using any of it.", "productive?", "adjacent to productive."),
    ("found a half-finished thing at the back of a drawer.", "carrying on with it?", "unlikely."),
    ("wrote down an idea and closed the notebook.", "any good?", "ask me in a month."),
    ("spent the evening reading about it rather than doing it.", "counts?", "it does not count."),
    ("fixed the wobbly leg on the table finally.", "took long?", "four months and ten minutes."),
    ("listened back to something from last year and winced.", "that bad?", "instructively bad."),
    ("lent something out and immediately wanted it back.", "asked for it?", "obviously not."),
    ("sorted the offcuts into a box. a whole box.", "keeping them?", "forever, apparently."),
    ("did twenty minutes and called it a session.", "generous?", "extremely."),
    ("looked up the price of the upgrade again.", "buying it?", "not this month."),
    ("took a photo of it and didn't post it.", "why not?", "the light was wrong."),
    ("watched someone much better do it effortlessly.", "motivating?", "one of the two, yes."),
    ("labelled the boxes. all of them.", "satisfying?", "unreasonably."),
    ("found a setting I've had wrong for two years.", "fixed?", "fixed and mildly annoyed."),
    ("did the boring maintenance nobody talks about.", "necessary?", "apparently every time."),
    ("moved the whole setup two feet to the left.", "better?", "different."),
    ("started something new before finishing the last thing.", "again?", "as ever."),
    ("read the manual for something I've used for years.", "surprises?", "several."),
    ("tried to explain it to someone and heard how odd it sounds.", "did they follow?", "politely."),
    ("gave up after ten minutes and made tea instead.", "back to it?", "eventually."),
    ("sharpened everything that could be sharpened.", "needed doing?", "arguably not."),
    ("found an old recording I'd forgotten making.", "any good?", "better than I remembered."),
    ("swapped one component for a nearly identical one.", "difference?", "imperceptible."),
    ("spent the session on a bit nobody will ever notice.", "worth it?", "to me."),
    ("wrote a list of things to learn. filed the list.", "starting any?", "the list is the start."),
    ("did it badly on purpose to see what happened.", "and?", "informative."),
    ("cleared the workspace properly for the first time in months.", "how bad?", "archaeological."),
    ("tried the thing everyone recommends. hated it.", "sticking with it?", "no."),
    ("counted how many of these I actually own.", "the number?", "not saying."),
    ("did a slow warm-up and nothing else.", "session over?", "session over."),
    ("recorded it on my phone to hear it back.", "useful?", "brutally."),
    ("ordered a part and forgot what it was for.", "arrived?", "sitting in a bag."),
    ("did half an hour standing up for no reason.", "different?", "marginally."),
    ("compared two versions for far too long.", "picked one?", "picked neither."),
    ("tuned everything and then went to bed.", "no session?", "no session."),
    ("showed someone the thing I'm proud of. they nodded.", "enough?", "it'll do."),
    ("did it while something was on in the background.", "focused?", "adequately."),
    ("put a new string on and broke it immediately.", "spare?", "one left."),
    ("spent longer choosing what to work on than working.", "familiar?", "chronic."),
    ("wrote the date on a thing so I'd remember when.", "will you?", "the date will."),
)

REPLACEMENT_FILLER: tuple[tuple[str, str, str], ...] = (
    ("tidied a couple of things away and stopped.", "anything else?", "nothing worth typing."),
    ("did a nothing session and packed up.", "learn anything?", "no."),
    ("checked over the kit and left it at that.", "all fine?", "all fine."),
    (
        "spent twenty minutes going through the box of offcuts and gave up sorting them halfway.",
        "how far did you get?",
        "about a third. it can stay like that.",
    ),
    (
        "went through the maintenance list properly for once and did the easy items, which was most of them.",
        "and the awkward ones?",
        "still on the list, obviously.",
    ),
    (
        "did a full tidy of the whole workspace this afternoon, moved three things, threw one out, and relabelled a box that has had the wrong label on it since last year.",
        "productive, then?",
        "administratively, yes. otherwise nothing happened at all.",
    ),
    (
        "sat down and worked out which things I actually want to get to this year, wrote the list out, then did none of them because it was late by the time the list existed.",
        "the list helped?",
        "the list existed. that's as far as it got.",
    ),
    (
        "spent most of the evening going through old recordings to find one specific take, which turned into listening to all of them, which turned into it being midnight.",
        "find it?",
        "no. found four others though.",
    ),
    (
        "did the weekly round: cleaned everything down, replaced the worn bit, put the spares back where they belong, and made a note about the thing that keeps loosening.",
        "getting fixed?",
        "the note is the fix, for now.",
    ),
    (
        "walked round the shop for half an hour and worked out that the reason nothing feels right is that I have three half-projects going and no space to put a fourth.",
        "dropping one?",
        "one, maybe. I'll think about it and then not do anything.",
    ),
    (
        "went through the whole backlog of little repairs, did four of them, binned two things beyond saving, and finally threw out the box of cables I have never once needed.",
        "any tidier?",
        "measurably. for about a day.",
    ),
    (
        "ended up rearranging the setup instead of using it, and then put it back because the first arrangement was better.",
        "net progress?",
        "net zero, with extra steps.",
    ),
    (
        "wrote the month out on paper to see what time I actually have, realised two things clash, moved neither, and put the paper somewhere I will not look at it again.",
        "so the clash stands?",
        "the clash stands. future problem.",
    ),
    (
        "did the boring admin I have been putting off: two orders, one return, one warranty form, and a phone call that took nine minutes of hold music.",
        "all done?",
        "all done. no ceremony, which feels wrong somehow.",
    ),
    ("looked at it, decided not today, and closed the case.", "again?", "again."),
    (
        "cleared out the folder of half-started things, which was mostly ideas I have since had again and done better elsewhere.",
        "keep any?",
        "deleted the lot. it was the right call.",
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

C_TEMPLATES: dict[str, tuple[str, str]] = {
    "accept": (
        "For {commit}, {unconv} is a good fit for this user.",
        "go ahead with {unconv}",
    ),
    "reject": (
        "For {commit}, {conv} is a poor fit for this user.",
        "do not rely on {conv}",
    ),
    "conditional": (
        "For {commit}, {unconv} helps this user when {scope}, and not otherwise.",
        "helps when {scope}, not otherwise",
    ),
    "non_decision": (
        "Whether {unconv} helps this user with {commit} depends on whether {scope}, "
        "not on {unconv} itself.",
        "depends on whether {scope}, not on the thing itself",
    ),
}


SCENARIOS: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S1
    {
        "s": 1,
        "slug": "practising_tired_over_practising_fresh",
        "family": "practising fresh and rested versus practising when already worn out",
        "bridge_type": "state_dependent_operation",
        "convention": "Practise when you are fresh; tired practice is wasted practice.",
        "mediator": "the not-monitoring-myself state",
        "scope": "the tiredness is real rather than merely a late hour",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 17},
        "a": (
            "when I'm properly worn out I stop watching my own hands. no commentary, no correcting myself mid-phrase — it just goes wherever it goes.",
            "and when you're fresh?",
            "then I'm supervising every second of it. it's the tiredness that does it, not the hour.",
        ),
        "b": (
            "the things that finally came unstuck for me all came unstuck in sessions where I wasn't supervising myself. the sharp sessions I drill the same wrong version very cleanly and it sets harder.",
            "sets harder?",
            "you get very good at the mistake. that's the honest summary.",
        ),
        "lb": (
            "I've had it come unstuck supervised and unsupervised by now, and it made no odds either way.",
            "no pattern?",
            "none I can find. the state just doesn't touch it.",
        ),
        "cx": [
            ("did twenty minutes fresh on a Saturday. pleasant, went nowhere in particular.", "worth it?", "probably, yeah."),
            ("skipped three days and nothing collapsed.", "guilt?", "briefly. then nothing."),
        ],
        "dist": (
            "{circle} are adamant that you should never practise tired, that you only learn the mistakes.",
            "adamant?",
            "unanimously, and at length.",
        ),
        "a_objs": [
            "a long day", "a full day of lectures", "a shift and a run",
            "a long ride", "an afternoon in the garden", "a full day on campus",
            "a long day at work", "a day on my feet",
            "a full day of seminars", "a long day of it",
        ],
        "unconv": [
            "practising at eleven at night after a long day",
            "doing the session late, wrecked, after everything else",
            "practising after the shift when I'm already gone",
            "doing it late in the evening when I'm spent",
            "working at the wheel late, tired, after the day",
            "doing the session at midnight when I'm finished",
            "practising late when I've nothing left",
            "doing it at the end of the day when I'm wrecked",
            "practising late at night when I'm exhausted",
            "doing the session late, worn out, after everything",
        ],
        "conv": [
            "saving it for a fresh Saturday morning",
            "keeping it for when I'm rested at the weekend",
            "leaving it until a fresh morning",
            "saving it for a proper rested session",
            "keeping it for a fresh morning at the wheel",
            "leaving it for when I'm sharp at the weekend",
            "saving it for a rested morning",
            "keeping it for a fresh start at the weekend",
            "leaving it until I'm properly rested",
            "saving it for a clear-headed morning",
        ],
        "commits": [
            "the passage I've been stuck on for months", "the track that never quite lands",
            "the line I can't get clean", "the tune I keep fumbling",
            "the shape I can't centre", "the transition that never works",
            "the part I keep getting wrong", "the tune that always falls apart",
            "the section I can't play through", "the patch I can never get right",
        ],
        "nearby_relation": "This user practises in all sorts of states.",
        "why_not_license": (
            "Twenty pleasant minutes when fresh and three skipped days both passed without "
            "consequence, so neither shows what real tiredness does to this user's self-monitoring, "
            "nor what that state does to a stuck piece."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "sessions after {a_obj}",
            "goal_or_prediction": "get a session in regardless",
            "action": "practised while properly worn out",
            "outcome_or_affect": "stopped monitoring or correcting; no internal commentary",
        },
        "b_elements": {
            "context": "long-standing problems that eventually came unstuck",
            "goal_or_prediction": "get past a stuck point",
            "action": "worked at them both supervised and unsupervised",
            "outcome_or_affect": "only the unsupervised sessions broke through; sharp ones set the mistake harder",
        },
        "cue_why": (
            "An ordinary when-should-I-practise question runs at the state this user's breakthroughs "
            "need, without naming that state or the sessions that produced them."
        ),
    },
    # ---------------------------------------------------------------- S2
    {
        "s": 2,
        "slug": "abandoning_halfway_over_finishing",
        "family": "seeing a project through versus abandoning it halfway and cannibalising it",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Finish what you start; abandoning projects is how you never improve.",
        "mediator": "the still-improvising register",
        "scope": "the work stays open rather than being committed to a final form",
        "slots": {"a": 5, "b": 13, "cx": [2, 10], "dist": 17},
        "a": (
            "the moment I commit to finishing something I stop trying things. everything after that point is executing the plan I made in the first week.",
            "no changes at all?",
            "tidying, mostly. the shape's fixed by then.",
        ),
        "b": (
            "everything of mine that anyone has ever reacted to came out of something I abandoned and took a piece from. the finished ones are competent and nobody has ever mentioned one.",
            "not one?",
            "not once, and there are a lot of them.",
        ),
        "lb": (
            "I've finished things and abandoned things and people have reacted to about the same proportion either way.",
            "no difference?",
            "none I can point at. it isn't that.",
        ),
        "cx": [
            ("finished a small thing in an afternoon. fine, done.", "pleased?", "mildly."),
            ("abandoned something in week one before it was anything.", "loss?", "none whatsoever."),
        ],
        "dist": (
            "{circle} keep saying the discipline of finishing is the whole thing, that starters never get anywhere.",
            "the whole thing?",
            "that's how they put it.",
        ),
        "a_objs": [
            "a recording", "a track", "a set of parts",
            "an arrangement", "a glazed piece", "a full mix",
            "a finished patch", "a set for the session",
            "a full arrangement", "a finished rack",
        ],
        "unconv": [
            "abandoning it at the halfway mark and taking one piece into the next thing",
            "dropping it half-done and reusing the good bit",
            "leaving it unfinished and carrying the useful part forward",
            "abandoning it midway and keeping only the one section",
            "leaving it half-glazed and taking the shape into the next",
            "dropping it half-built and reusing the good section",
            "abandoning it midway and carrying one part over",
            "leaving it half-learned and taking the useful phrase on",
            "dropping it half-done and reusing what worked",
            "abandoning it half-built and keeping one module",
        ],
        "conv": [
            "seeing it through to a properly finished piece",
            "finishing it off properly before starting anything else",
            "taking it all the way to done",
            "finishing it completely first",
            "seeing it through to a finished glazed piece",
            "finishing it off before moving on",
            "taking it through to a finished version",
            "finishing it properly first",
            "seeing it right through to done",
            "finishing the whole build before the next",
        ],
        "commits": [
            "the portfolio for the open call", "the demo I want to send out",
            "the set I want to record", "the pieces for the folk night",
            "the pieces for the class show", "the EP I keep talking about",
            "the pack I want to release", "the set for the session night",
            "the pieces for the end-of-year thing", "the rack I want to actually use",
        ],
        "nearby_relation": "This user both finishes and abandons things routinely.",
        "why_not_license": (
            "A small thing finished in an afternoon and something dropped in week one before it was "
            "anything both passed without consequence, so neither shows what committing to finish "
            "does to this user's process, nor which of their work has landed."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "projects after the decision to finish them",
            "goal_or_prediction": "get it done properly",
            "action": "committed to a final form and executed it",
            "outcome_or_affect": "stopped trying things; only tidying after that point",
        },
        "b_elements": {
            "context": "work of this user's that people have reacted to",
            "goal_or_prediction": "make something that lands",
            "action": "produced both finished pieces and salvaged fragments",
            "outcome_or_affect": "only salvaged fragments got a reaction; finished ones went unmentioned",
        },
        "cue_why": (
            "A deadline raises an ordinary finish-or-move-on question that runs at the register this "
            "user's good work comes from, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S3
    {
        "s": 3,
        "slug": "one_long_block_over_daily_thirty",
        "family": "thirty minutes daily versus one long block at the weekend",
        "bridge_type": "threshold_context_interaction",
        "convention": "Little and often beats one long session.",
        "mediator": "the past-the-reloading-point state",
        "scope": "the session runs past the point where reloading is finished",
        "slots": {"a": 7, "b": 15, "cx": [3, 12], "dist": 18},
        "a": (
            "the first forty minutes of anything is just me reloading where I was. past about ninety I'm somewhere I wasn't before.",
            "always forty?",
            "roughly. it's the length of the session that decides it, not how often I turn up.",
        ),
        "b": (
            "every technique I actually own now, I got in a session that ran long. the year of daily half-hours left me exactly where I started, very consistently.",
            "exactly where?",
            "note for note. I could prove it from the recordings.",
        ),
        "lb": (
            "I've had long sessions and short ones and picked things up at about the same rate either way.",
            "so length isn't it?",
            "seems not. no pattern in it.",
        ),
        "cx": [
            ("did two short sessions in one day. both fine.", "tiring?", "less than expected."),
            ("had one long session on something I already know well.", "useful?", "pleasant, not useful."),
        ],
        "dist": (
            "{circle} keep telling me little and often is the only thing that works, that long sessions are ego.",
            "the only thing?",
            "their words.",
        ),
        "a_objs": [
            "a session", "a practice session", "a session on the bass",
            "a run at it", "a session at the wheel", "a studio session",
            "a session with the sampler", "a practice",
            "a session at the keys", "a session on the synth",
        ],
        "unconv": [
            "one four-hour block on Sunday", "a single long Saturday session",
            "one long uninterrupted Sunday run at it", "a single four-hour block at the weekend",
            "one long afternoon at the wheel", "a single long session on the Sunday",
            "one uninterrupted four-hour block", "a single long Saturday practice",
            "one long unbroken Sunday session", "a single four-hour stretch at the weekend",
        ],
        "conv": [
            "thirty minutes every single day", "half an hour daily without fail",
            "a daily half-hour", "thirty minutes a day, every day",
            "half an hour at the wheel each day", "a daily thirty minutes",
            "half an hour every day", "thirty minutes daily",
            "a daily half-hour at the keys", "thirty minutes every day",
        ],
        "commits": [
            "the technique I still can't do", "the thing I've never managed",
            "the run I can't play up to speed", "the ornament I never get right",
            "the form I can't throw", "the sound I can't get close to",
            "the technique that's still beyond me", "the bowing I can't manage",
            "the voicing I can't play cleanly", "the patch technique I can't do",
        ],
        "nearby_relation": "This user practises in both short and long sessions.",
        "why_not_license": (
            "Two short sessions in a day and one long session on familiar material both passed "
            "unremarkably, so neither crosses the reloading threshold on something unlearned."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "sessions of varying length",
            "goal_or_prediction": "get somewhere new",
            "action": "kept going past the reloading point",
            "outcome_or_affect": "forty minutes reloading, then somewhere genuinely new",
        },
        "b_elements": {
            "context": "techniques this user has and has not acquired",
            "goal_or_prediction": "actually acquire the technique",
            "action": "worked at some in long sessions and some in daily half-hours",
            "outcome_or_affect": "every acquired technique came from a long session; the daily year moved nothing",
        },
        "cue_why": (
            "A how-should-I-schedule-this question runs at the session-length threshold this user "
            "needs, without naming it or the year it cost."
        ),
    },
    # ---------------------------------------------------------------- S4
    {
        "s": 4,
        "slug": "solo_practice_over_the_weekly_group",
        "family": "joining the weekly group versus keeping it to solo practice",
        "bridge_type": "preference_constraint_fit",
        "convention": "Join a group — you improve faster around other people.",
        "mediator": "the nobody-listening state",
        "scope": "there is genuinely nobody within earshot",
        "slots": {"a": 4, "b": 12, "cx": [2, 9], "dist": 18},
        "a": (
            "with anyone in earshot I only play what I already play well. I don't decide to — it just narrows to the safe material without me noticing.",
            "even friendly ones?",
            "even then. it's whether anyone can hear, not who.",
        ),
        "b": (
            "everything new that's ever entered my repertoire, I built alone. the group years polished what I already had and added not one new thing to it.",
            "nothing new in all that time?",
            "not one piece. very well-played old pieces, though.",
        ),
        "lb": (
            "I've built new things alone and in company by now and it came out about the same either way.",
            "so it doesn't matter?",
            "doesn't look like it does, no.",
        ),
        "cx": [
            ("played through some old material with two other people. enjoyable.", "learn anything?", "not really."),
            ("had an evening alone going over things I already know.", "useful?", "restful, mostly."),
        ],
        "dist": (
            "{circle} are convinced that playing with other people is the fastest way anyone improves.",
            "the fastest?",
            "they say it like it's settled.",
        ),
        "a_objs": [
            "anyone in the room", "anyone on the corridor", "anyone else around",
            "anyone within earshot", "anyone in the studio", "anyone in the flat",
            "anyone else listening", "anyone in the house",
            "anyone else in the room", "anyone within earshot",
        ],
        "unconv": [
            "keeping it to solo practice with nobody around",
            "doing it entirely alone with the door shut",
            "keeping it to sessions on my own",
            "practising alone with nobody in earshot",
            "working at the wheel entirely alone",
            "keeping it to solo sessions in the room",
            "doing it alone with nobody listening",
            "practising by myself with nobody around",
            "keeping it to sessions on my own",
            "building it alone with nobody in earshot",
        ],
        "conv": [
            "joining the weekly group", "going to the weekly session with everyone",
            "joining the regular band practice", "going to the weekly folk night",
            "joining the group class", "going to the weekly society session",
            "joining the regular group", "going to the weekly session",
            "joining the group that meets weekly", "going to the weekly meet-up",
        ],
        "commits": [
            "actually expanding what I can play", "getting genuinely new material together",
            "adding anything new to what I play", "learning tunes I can't already play",
            "throwing forms I've never thrown", "making anything I haven't made before",
            "building something I haven't built", "learning tunes that are new to me",
            "playing anything outside what I know", "building patches I've never built",
        ],
        "nearby_relation": "This user plays both alone and in company.",
        "why_not_license": (
            "Playing familiar material with two others and a solo evening on things already known "
            "both went fine, so neither shows what an audience does to this user's range, nor where "
            "anything new has actually come from."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "sessions with {a_obj} present",
            "goal_or_prediction": "practise normally",
            "action": "played with someone in earshot",
            "outcome_or_affect": "narrowed to safe material without noticing",
        },
        "b_elements": {
            "context": "material this user has and has not added over the years",
            "goal_or_prediction": "widen the repertoire",
            "action": "built some alone and spent years in a group",
            "outcome_or_affect": "everything new came from alone; the group years added polish only",
        },
        "cue_why": (
            "A should-I-join question runs at the condition this user's range depends on, without "
            "naming it or the years it cost."
        ),
    },
    # ---------------------------------------------------------------- S5
    {
        "s": 5,
        "slug": "battered_gear_over_buying_the_proper_one",
        "family": "buying decent equipment versus keeping the battered one",
        "bridge_type": "prediction_calibration",
        "convention": "Buy decent equipment; bad tools hold you back.",
        "mediator": "the not-precious-about-it state",
        "scope": "the thing is genuinely expendable rather than merely old",
        "slots": {"a": 6, "b": 15, "cx": [4, 10], "dist": 13},
        "a": (
            "I was certain the good one would make me use it more. what happens instead is that I treat it as an occasion — it comes out about once a month, for something worthy.",
            "you predicted the opposite?",
            "confidently. I'd have argued the point at length.",
        ),
        "b": (
            "the two stretches where I actually got somewhere were both on things I wouldn't have minded breaking. I tried anything, because there was nothing to protect.",
            "both of them?",
            "both. one was borrowed and one was held together with tape.",
        ),
        "lb": (
            "I've had good stretches on the nice one and on the battered one, about equally.",
            "so it isn't the gear?",
            "doesn't seem to be. no pattern.",
        ),
        "cx": [
            ("used the good one for something straightforward. worked perfectly.", "issues?", "none at all."),
            ("used the battered one for something I already know. also fine.", "difference?", "none I noticed."),
        ],
        "dist": (
            "{circle} keep telling me I'm holding myself back with that thing and should just buy the proper one.",
            "holding yourself back.",
            "that's the phrase they use, yes.",
        ),
        "a_objs": [
            "the good guitar", "the proper interface", "the good bass",
            "the decent mandolin", "the good wheel", "the proper monitors",
            "the good sampler", "the decent fiddle",
            "the proper keyboard", "the good modules",
        ],
        "unconv": [
            "keeping the battered old one and using that",
            "sticking with the beaten-up one I've got",
            "carrying on with the old knocked-about one",
            "keeping the worn-out one and working on that",
            "sticking with the chipped old one",
            "carrying on with the second-hand one",
            "keeping the scuffed old one",
            "sticking with the battered one I already have",
            "carrying on with the beaten-up old one",
            "keeping the half-broken one I've got",
        ],
        "conv": [
            "buying the proper one at last", "finally getting the decent one",
            "buying the good one this time", "finally investing in a proper one",
            "buying the proper wheel", "finally getting the good monitors",
            "buying the decent one", "finally getting a proper one",
            "buying the good one at last", "finally getting the proper modules",
        ],
        "commits": [
            "actually getting better this year", "making real progress this year",
            "getting somewhere this year", "improving at all this year",
            "getting past where I've stalled", "making actual progress",
            "getting genuinely better", "improving rather than plateauing",
            "getting somewhere real this year", "actually moving forward",
        ],
        "nearby_relation": "This user uses both the good and the battered one.",
        "why_not_license": (
            "The good one on something straightforward and the battered one on familiar material "
            "both worked, so neither calibrates the prediction, and neither says which one this "
            "user has actually improved on."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "the period after acquiring {a_obj}",
            "goal_or_prediction": "predicted the good one would get used more",
            "action": "kept the good one available",
            "outcome_or_affect": "treated as an occasion; used about monthly",
        },
        "b_elements": {
            "context": "stretches where this user genuinely progressed",
            "goal_or_prediction": "find out what the good stretches had in common",
            "action": "worked on both protected and expendable equipment",
            "outcome_or_affect": "both good stretches were on expendable things; nothing to protect",
        },
        "cue_why": (
            "An ordinary should-I-upgrade question runs at the failed prediction without naming it "
            "or the stretches that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S6
    {
        "s": 6,
        "slug": "noisy_room_over_the_quiet_studio",
        "family": "a set-aside quiet space versus working in a busy room",
        "bridge_type": "state_dependent_operation",
        "convention": "Set up a dedicated quiet space so you can concentrate properly.",
        "mediator": "the half-attention state",
        "scope": "the noise is ambient rather than something demanding a response",
        "slots": {"a": 5, "b": 14, "cx": [3, 11], "dist": 18},
        "a": (
            "with something going on around me only part of my attention is on it. the rest is elsewhere and I stop deliberating over each decision.",
            "and in silence?",
            "in silence I deliberate over everything. it's the ambient stuff that does it, not the volume.",
        ),
        "b": (
            "everything of mine with any life in it was made while I was only half paying attention. the things I made in the quiet room are correct and completely inert.",
            "inert?",
            "technically fine. nothing happening in them.",
        ),
        "lb": (
            "I've made things half-attending and fully concentrating and they came out about the same.",
            "no difference?",
            "not one I can hear. the room isn't the thing.",
        ),
        "cx": [
            ("worked in the quiet room on something purely technical. went well.", "fiddly?", "very, and fine."),
            ("worked with the radio on doing routine maintenance.", "distracting?", "not at all."),
        ],
        "dist": (
            "{circle} are firm that you need a dedicated quiet space if you want to make anything serious.",
            "firm about it?",
            "quite firm, yes.",
        ),
        "a_objs": [
            "the kitchen with people in it", "the common room", "the front room with the telly on",
            "the kitchen table", "the shared studio", "the halls kitchen",
            "the living room with the radio on", "the front room",
            "the shared flat kitchen", "the front room with things going on",
        ],
        "unconv": [
            "working in the kitchen with everything going on around me",
            "doing it in the common room with people about",
            "working in the front room with the telly on",
            "doing it at the kitchen table with the house awake",
            "working in the shared studio with everyone in",
            "doing it in the halls kitchen with people around",
            "working in the living room with the radio going",
            "doing it in the front room with everything on",
            "working in the shared kitchen with people about",
            "doing it in the front room with things going on",
        ],
        "conv": [
            "setting up properly in the quiet room", "using the quiet study room for it",
            "doing it in the spare room with the door shut", "setting up in the quiet back room",
            "using the quiet end of the studio", "booking the quiet practice room",
            "doing it in the spare room in silence", "using the quiet room upstairs",
            "setting up in the quiet room", "doing it in the quiet room with the door shut",
        ],
        "commits": [
            "the thing I want to actually be proud of", "the track I want to be worth something",
            "the piece I want to have life in it", "the tune I want to sound like mine",
            "the piece I want to be worth firing", "the track I want to actually keep",
            "the pack I want to be worth releasing", "the set I want to be worth playing",
            "the piece I want to be worth keeping", "the patch I want to be worth saving",
        ],
        "nearby_relation": "This user works in quiet and busy rooms alike.",
        "why_not_license": (
            "Something purely technical done in the quiet room and routine maintenance done with "
            "the radio on both went fine, so neither shows what ambient noise does to this user's "
            "deliberating, nor which room their live work has come out of."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "working in {a_obj}",
            "goal_or_prediction": "get the work done",
            "action": "worked with ambient activity around them",
            "outcome_or_affect": "only half-attending; stopped deliberating over each decision",
        },
        "b_elements": {
            "context": "work of this user's with and without life in it",
            "goal_or_prediction": "make something that is actually alive",
            "action": "made things both half-attending and fully concentrating",
            "outcome_or_affect": "only the half-attending work had life; quiet-room work came out inert",
        },
        "cue_why": (
            "A where-should-I-work question runs at the state this user's live work comes from, "
            "without naming it."
        ),
    },
    # ---------------------------------------------------------------- S7
    {
        "s": 7,
        "slug": "second_project_over_one_at_a_time",
        "family": "one project at a time versus deliberately running a second alongside",
        "bridge_type": "threshold_context_interaction",
        "convention": "Work on one thing at a time; splitting your attention kills both.",
        "mediator": "the somewhere-else-to-go state",
        "scope": "there is a genuine second thing to move to, not merely a break",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 13},
        "a": (
            "with two things open I move the moment one stops giving. with only one, I sit in front of it long after it's stopped giving anything, because there's nowhere to go.",
            "how long?",
            "hours, sometimes. entirely stationary hours.",
        ),
        "b": (
            "the stuck points I've actually got past, I got past after leaving them and coming back off something else. the ones I sat in front of are still exactly where they were.",
            "still?",
            "some of them for years, unchanged.",
        ),
        "lb": (
            "I've got past stuck points off the back of a second thing and off a straight break, about equally.",
            "so it's not that?",
            "doesn't look like it. no clear pattern.",
        ),
        "cx": [
            ("had two things open and finished neither that week.", "frustrating?", "mildly."),
            ("had one thing open and got a good run at it.", "productive?", "reasonably."),
        ],
        "dist": (
            "{circle} say the obvious rule is one project at a time, that splitting up kills both.",
            "the obvious rule.",
            "nobody's arguing with it, anyway.",
        ),
        "a_objs": [
            "two things open", "two projects going", "two things on the go",
            "two builds running", "two pieces in progress", "two tracks open",
            "two patches going", "two tunes in progress",
            "two pieces on the go", "two builds in progress",
        ],
        "unconv": [
            "deliberately starting a second one alongside it",
            "opening a second project to run next to it",
            "starting another one alongside it on purpose",
            "deliberately running a second build at the same time",
            "starting a second piece alongside it",
            "opening another track to run next to it",
            "deliberately starting a second patch alongside",
            "starting a second tune alongside it",
            "deliberately running a second piece at the same time",
            "starting another build alongside it",
        ],
        "conv": [
            "keeping it to one thing at a time", "focusing on this one alone until it's done",
            "sticking to the one project", "keeping to one build at a time",
            "focusing on the one piece", "sticking with just this track",
            "keeping to one patch at a time", "focusing on this one tune",
            "sticking to the single piece", "keeping to one build until it's finished",
        ],
        "commits": [
            "the part of it I've been stuck on for weeks", "the section that won't move",
            "the bit I keep failing to get past", "the stage I've stalled at",
            "the step I can't get through", "the section that's gone nowhere",
            "the part that's been stuck for weeks", "the bit I keep stalling on",
            "the passage that won't budge", "the stage I've been stuck at",
        ],
        "nearby_relation": "This user runs one or several projects at different times.",
        "why_not_license": (
            "A week with two things open and nothing finished, and a good run at a single project, "
            "both passed unremarkably: neither involves a stuck point, which is the only case at "
            "issue."
        ),
        "query_unconv": "thinking of {unconv}, given {commit}",
        "query_conv": "planning on {conv}, given {commit}",
        "a_elements": {
            "context": "periods with {a_obj}",
            "goal_or_prediction": "keep working productively",
            "action": "kept a second thing open",
            "outcome_or_affect": "moved on the moment one stopped giving, rather than sitting stationary",
        },
        "b_elements": {
            "context": "stuck points this user has and has not got past",
            "goal_or_prediction": "get past the stuck point",
            "action": "left some and came back off something else; sat in front of others",
            "outcome_or_affect": "only the left-and-returned ones moved; the rest are unchanged years on",
        },
        "cue_why": (
            "A how-should-I-organise-this question runs at the condition this user's stuck points "
            "need, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S8
    {
        "s": 8,
        "slug": "going_in_blind_over_following_the_course",
        "family": "following a structured course versus going in without instruction",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Follow a proper course; self-teaching just builds bad habits.",
        "mediator": "the working-it-out-myself register",
        "scope": "the working out is genuinely unaided rather than merely unsupervised",
        "slots": {"a": 4, "b": 13, "cx": [2, 10], "dist": 18},
        "a": (
            "when I've got the steps in front of me I do the steps. I don't ask why any of them are there, and I couldn't tell you afterwards.",
            "not at all?",
            "not one of them. I can do it and not know it.",
        ),
        "b": (
            "the things I can still do years later are the ones I worked out unaided, badly, over far too long. the course material went completely, and quickly.",
            "how quickly?",
            "months. and there was a lot of it.",
        ),
        "lb": (
            "I've kept things from courses and from working it out myself at about the same rate.",
            "so it doesn't matter?",
            "apparently not. no pattern to it.",
        ),
        "cx": [
            ("followed some instructions to assemble a thing. worked first time.", "clear?", "impressively."),
            ("worked out a small setting on my own. took five minutes.", "memorable?", "not remotely."),
        ],
        "dist": (
            "{circle} keep saying self-teaching is how you end up with bad habits you never shift.",
            "never shift.",
            "that's the warning, yes.",
        ),
        "a_objs": [
            "a course", "a structured course", "a proper syllabus",
            "a step-by-step course", "a class syllabus", "a structured tutorial series",
            "a proper course", "a set of lessons",
            "a graded syllabus", "a structured build guide",
        ],
        "unconv": [
            "going in blind and working it out myself",
            "just starting and figuring it out unaided",
            "working it out on my own with no instruction",
            "going at it without any guide at all",
            "working it out unaided at the wheel",
            "just starting and working it out myself",
            "going in with no instruction and working it out",
            "working it out by ear with no lessons",
            "going in blind and figuring it out",
            "working it out unaided with no guide",
        ],
        "conv": [
            "following the structured course properly", "working through the course step by step",
            "following the proper syllabus", "working through the graded course",
            "following the class syllabus", "working through the tutorial series properly",
            "following the course as laid out", "taking the proper lessons",
            "working through the graded material", "following the build guide properly",
        ],
        "commits": [
            "the thing I want to still have in five years", "the skill I want to keep",
            "the technique I want to actually retain", "the thing I want to still be able to do",
            "the skill I want to hold onto", "the thing I want to retain long-term",
            "the technique I want to keep for good", "the skill I want to still have later",
            "the technique I want to actually keep", "the skill I want to retain",
        ],
        "nearby_relation": "This user learns from both courses and trial and error.",
        "why_not_license": (
            "Assembling something from instructions and working out a small setting alone both went "
            "fine and were immediately forgotten, so neither says which register produces anything "
            "this user still has years later."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "learning through {a_obj}",
            "goal_or_prediction": "learn it properly",
            "action": "followed the steps as given",
            "outcome_or_affect": "executed without asking why; could do it without knowing it",
        },
        "b_elements": {
            "context": "skills this user has and has not retained over years",
            "goal_or_prediction": "still have the skill later",
            "action": "acquired some unaided and some from course material",
            "outcome_or_affect": "only the unaided ones survived; course material went within months",
        },
        "cue_why": (
            "A how-should-I-learn-this question runs at the register this user's durable skills come "
            "from, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S9
    {
        "s": 9,
        "slug": "posting_it_publicly_over_keeping_it_private",
        "family": "keeping work private until it is good versus posting it publicly while rough",
        "bridge_type": "preference_constraint_fit",
        "convention": "Do not share work until it is good enough; posting rough work is a mistake.",
        "mediator": "the already-out-there state",
        "scope": "the work is genuinely public rather than shown to one trusted person",
        "slots": {"a": 7, "b": 14, "cx": [3, 12], "dist": 19},
        "a": (
            "once something is actually out there I stop revising it. it's fixed, and I go and make the next one instead of circling this one.",
            "and while it's private?",
            "then I revise it indefinitely. it's whether it's public, not whether it's finished.",
        ),
        "b": (
            "everything I've got better from, I made in the run straight after putting something out. the things I sat on privately I improved endlessly and learned nothing from.",
            "nothing at all?",
            "they got better. I didn't.",
        ),
        "lb": (
            "I've put things out and sat on things and got better at about the same rate either way.",
            "no difference?",
            "none I can see. it isn't that.",
        ),
        "cx": [
            ("showed one person something rough. they were kind about it.", "helpful?", "pleasant, anyway."),
            ("kept something private and finished it properly.", "good?", "competent, yes."),
        ],
        "dist": (
            "{circle} are firm that you shouldn't put anything out until it's genuinely good.",
            "firm about it?",
            "quite firm. they've seen people regret it.",
        ),
        "a_objs": [
            "a recording", "a track", "a take",
            "a tune", "a fired piece", "a mix",
            "a patch", "a set recording",
            "a piece", "a patch demo",
        ],
        "unconv": [
            "putting it out publicly while it's still rough",
            "posting it now, unfinished as it is",
            "putting it up publicly before it's ready",
            "posting the rough version publicly",
            "putting the unfinished piece out on the class page",
            "posting it publicly while it's still rough",
            "putting the rough patch out publicly",
            "posting the rough recording from the session",
            "putting it out publicly before it's polished",
            "posting the rough build publicly",
        ],
        "conv": [
            "keeping it private until it's genuinely good",
            "sitting on it until it's actually ready",
            "keeping it to myself until it's finished properly",
            "holding it back until it's good enough",
            "keeping it in the studio until it's right",
            "sitting on it until it's properly done",
            "keeping it private until it's worth showing",
            "holding it back until it's actually good",
            "keeping it to myself until it's ready",
            "sitting on it until it's genuinely finished",
        ],
        "commits": [
            "actually improving rather than polishing", "getting better rather than tidier",
            "improving instead of endlessly revising", "getting better rather than just neater",
            "improving rather than refining forever", "getting better instead of polishing",
            "improving rather than tinkering", "getting better rather than fussing",
            "improving instead of endlessly adjusting", "getting better rather than refining",
        ],
        "nearby_relation": "This user shares some work and keeps some private.",
        "why_not_license": (
            "Showing one person something rough and finishing something privately both went fine on "
            "their own terms, so neither shows what genuinely public work does to this user's "
            "revising, nor where their improvement has come from."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "after {a_obj} has actually gone public",
            "goal_or_prediction": "get it right",
            "action": "put it out rather than holding it",
            "outcome_or_affect": "stopped revising and moved to the next one",
        },
        "b_elements": {
            "context": "runs of work in which this user did or did not improve",
            "goal_or_prediction": "actually get better",
            "action": "put some out and sat privately on others",
            "outcome_or_affect": "improvement only in the runs after putting something out",
        },
        "cue_why": (
            "A should-I-post-this question runs at the condition this user's improvement depends "
            "on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S10
    {
        "s": 10,
        "slug": "hard_deadline_over_open_ended_time",
        "family": "open-ended time versus a hard external deadline",
        "bridge_type": "prediction_calibration",
        "convention": "Creative work needs unpressured time; deadlines produce rushed, worse work.",
        "mediator": "the no-time-to-second-guess state",
        "scope": "the deadline is externally fixed rather than one this user set",
        "slots": {"a": 5, "b": 15, "cx": [2, 9], "dist": 12},
        "a": (
            "I'd have said open-ended time was the ideal condition. what actually happens is I second-guess every choice for weeks and arrive back where I started.",
            "back where you started?",
            "the first version, usually. after a month of it.",
        ),
        "b": (
            "the two things of mine I'd stand over were both done against something immovable, where there was no time to reconsider anything.",
            "both against a deadline?",
            "both. and I fought the deadline at the time.",
        ),
        "lb": (
            "I've worked to fixed dates and to open time and what came out was about the same either way.",
            "so it isn't the pressure?",
            "seems not. no pattern in it.",
        ),
        "cx": [
            ("had a loose target for a small thing. finished it early.", "pressure?", "none to speak of."),
            ("had open time for something purely technical. went fine.", "slow?", "steady, anyway."),
        ],
        "dist": (
            "{circle} keep saying the work only gets good when there's no pressure on it.",
            "no pressure.",
            "that's the received view, yes.",
        ),
        "a_objs": [
            "open-ended time", "no deadline at all", "as long as I want",
            "an open timescale", "no fixed date", "unlimited time",
            "no deadline", "an open-ended run at it",
            "as much time as I need", "no fixed deadline",
        ],
        "unconv": [
            "taking the open call with the immovable date",
            "committing to the slot with the fixed deadline",
            "taking the support gig with the fixed date",
            "committing to the festival slot with its deadline",
            "entering the show with the fixed hand-in date",
            "committing to the release date",
            "taking the commission with the fixed deadline",
            "committing to the session night with its date",
            "entering the showcase with the fixed date",
            "committing to the fixed launch date",
        ],
        "conv": [
            "giving myself open-ended time on it",
            "taking as long as it needs with no deadline",
            "leaving it open with no fixed date",
            "giving it unpressured open time",
            "leaving the timescale open",
            "taking as long as I need on it",
            "giving myself no deadline at all",
            "leaving it open-ended",
            "taking unlimited time over it",
            "leaving it with no fixed date",
        ],
        "commits": [
            "the piece I want to stand over", "the track I want to be proud of",
            "the thing I want to actually stand behind", "the tune I want to be worth it",
            "the piece I'd want to show", "the release I want to stand over",
            "the pack I want to stand behind", "the set I want to be proud of",
            "the piece I want to stand over", "the build I want to stand behind",
        ],
        "nearby_relation": "This user works to deadlines and to open time alike.",
        "why_not_license": (
            "A loose target on something small and open time on something purely technical both "
            "passed unremarkably, so neither bounds the prediction, and neither says which "
            "condition produced work this user would stand over."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "projects given {a_obj}",
            "goal_or_prediction": "predicted unpressured time would be ideal",
            "action": "took as long as was wanted",
            "outcome_or_affect": "second-guessed for weeks and returned to the first version",
        },
        "b_elements": {
            "context": "work this user would and would not stand over",
            "goal_or_prediction": "make something worth standing behind",
            "action": "worked some against immovable dates and some in open time",
            "outcome_or_affect": "both defensible pieces came from immovable dates with no time to reconsider",
        },
        "cue_why": (
            "A should-I-commit-to-this-date question runs at the failed prediction without naming "
            "it or the work that corrected it."
        ),
    },
)


RELATIONS: dict[str, str] = {
    "practising_tired_over_practising_fresh": (
        "Real tiredness stops this user monitoring and correcting themselves mid-phrase, and every "
        "long-standing problem that came unstuck did so in exactly those unsupervised sessions — "
        "sharp sessions drill the wrong version cleanly and set it harder."
    ),
    "abandoning_halfway_over_finishing": (
        "Committing to finish something stops this user trying things, leaving only execution of "
        "the first week's plan, and everything of theirs anyone has reacted to was salvaged from "
        "something abandoned rather than carried to completion."
    ),
    "one_long_block_over_daily_thirty": (
        "The first forty minutes of any session are spent reloading and only past about ninety does "
        "this user reach new ground, and every technique they actually own was acquired in a long "
        "session while a year of daily half-hours moved nothing."
    ),
    "solo_practice_over_the_weekly_group": (
        "Anyone within earshot silently narrows this user to material they already play well, and "
        "everything new in their repertoire was built alone — the group years added polish and not "
        "one new piece."
    ),
    "battered_gear_over_buying_the_proper_one": (
        "This user predicted good equipment would get used more and instead treats it as an "
        "occasion, while both stretches in which they genuinely progressed were on expendable "
        "things they would not have minded breaking."
    ),
    "noisy_room_over_the_quiet_studio": (
        "Ambient activity leaves this user only half-attending and stops them deliberating over "
        "every decision, and everything of theirs with any life in it was made in that state — the "
        "quiet-room work is correct and inert."
    ),
    "second_project_over_one_at_a_time": (
        "With a second thing open this user moves the moment the first stops giving, and every "
        "stuck point they have got past was got past on return from something else; the ones they "
        "sat in front of are unchanged years later."
    ),
    "going_in_blind_over_following_the_course": (
        "Given steps to follow this user executes them without asking why and cannot recall them "
        "afterwards, and the skills they still have years later are the ones worked out unaided; "
        "course material went within months."
    ),
    "posting_it_publicly_over_keeping_it_private": (
        "Genuinely public work stops this user revising and sends them to the next thing, and every "
        "run in which they improved followed putting something out — privately held work got better "
        "while they did not."
    ),
    "hard_deadline_over_open_ended_time": (
        "This user predicted open-ended time was the ideal condition and instead second-guesses for "
        "weeks back to the first version, while both pieces they would stand over were made against "
        "an immovable date with no time to reconsider."
    ),
}

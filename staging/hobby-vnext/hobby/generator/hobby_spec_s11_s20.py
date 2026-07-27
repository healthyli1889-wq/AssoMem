"""Hobby scenario families S11-S20, extending the batch to 200 units / 600 files.

Same contract as `hobby_spec.SCENARIOS`. Bridge types continue the two-per-type
rotation so all five are used four times across S1-S20.
"""

from __future__ import annotations

SCENARIOS_EXT: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S11
    {
        "s": 11,
        "slug": "playing_with_beginners_over_better_players",
        "family": "playing with better players versus being the strongest in the room",
        "bridge_type": "state_dependent_operation",
        "convention": "Play with people better than you; that is how you improve.",
        "mediator": "the making-the-decisions state",
        "scope": "this user is genuinely the strongest present rather than merely comfortable",
        "slots": {"a": 6, "b": 15, "cx": [3, 10], "dist": 18},
        "a": (
            "when I'm the strongest one in the room I stop following and start deciding. where it goes next is mine, for better or worse.",
            "and with better players?",
            "then I'm following whoever's leading. it's about being the strongest, not about the level.",
        ),
        "b": (
            "everything I can do without being led came out of sessions where I was making the decisions. the sessions with better players I follow beautifully and retain none of it.",
            "none?",
            "I can do it while they're there and not afterwards.",
        ),
        "lb": (
            "I've come away with things from both kinds of session by now, at about the same rate.",
            "no pattern?",
            "none I can find. it isn't who's in the room.",
        ),
        "cx": [
            ("sat in on a session at about my level. pleasant enough.", "learn much?", "not especially."),
            ("watched a much better player for an hour without joining in.", "useful?", "enjoyable, anyway."),
        ],
        "dist": (
            "{circle} keep saying the only way to improve is to play with people better than you.",
            "the only way?",
            "they're very settled on it.",
        ),
        "a_objs": [
            "the strongest in the room", "the best one there", "the strongest player present",
            "the most experienced there", "the most practised in the class", "the strongest in the group",
            "the most capable there", "the strongest at the session",
            "the most experienced in the room", "the one who knows most there",
        ],
        "unconv": [
            "playing with the beginners' group instead",
            "joining the group of people just starting out",
            "playing with the newer, less experienced lot",
            "joining the beginners' night",
            "working alongside the first-year class",
            "joining the group of complete beginners",
            "playing with the people just getting going",
            "joining the slow session for learners",
            "playing with the beginners' group",
            "joining the group who have just started",
        ],
        "conv": [
            "getting into the advanced session", "joining the group who are all better than me",
            "getting into the stronger band", "joining the experienced players' night",
            "getting onto the advanced course", "joining the group who are well ahead of me",
            "getting into the stronger group", "joining the fast session",
            "getting into the advanced group", "joining the builders who are far ahead",
        ],
        "commits": [
            "playing anything without being led", "doing anything unprompted",
            "playing independently at all", "carrying a tune on my own",
            "throwing something without being talked through it", "making anything unprompted",
            "building anything without following", "leading a tune myself",
            "playing anything without being carried", "building anything unaided",
        ],
        "nearby_relation": "This user plays across a range of levels.",
        "why_not_license": (
            "A session at this user's own level and an hour spent watching without joining in both "
            "passed unremarkably, so neither shows what being the strongest present does to them, "
            "nor which sessions have left them able to do anything alone."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "sessions where this user is {a_obj}",
            "goal_or_prediction": "get a session in",
            "action": "played as the strongest one present",
            "outcome_or_affect": "stopped following and made the decisions",
        },
        "b_elements": {
            "context": "capabilities this user does and does not retain unaided",
            "goal_or_prediction": "be able to do it alone afterwards",
            "action": "played both as the strongest and alongside better players",
            "outcome_or_affect": "only decision-making sessions left anything retained",
        },
        "cue_why": (
            "A which-group-should-I-join question runs at the condition this user's independence "
            "depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S12
    {
        "s": 12,
        "slug": "dropping_the_log_over_tracking_everything",
        "family": "keeping a practice log versus not measuring at all",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Track your practice — what gets measured gets improved.",
        "mediator": "the nothing-to-optimise register",
        "scope": "nothing is being recorded rather than merely recorded loosely",
        "slots": {"a": 5, "b": 14, "cx": [2, 11], "dist": 17},
        "a": (
            "once I'm recording it I start working on whatever makes the record look right. the number becomes the thing I'm doing.",
            "consciously?",
            "not at all. I only notice looking back at what I chose to work on.",
        ),
        "b": (
            "the stretches where I genuinely changed were the ones nobody was counting. the meticulously recorded year has the best figures of any year and the least actual difference in it.",
            "the best figures?",
            "by a distance. and I play exactly the same.",
        ),
        "lb": (
            "I've had recorded stretches and unrecorded ones and changed about as much either way.",
            "so it isn't the log?",
            "doesn't look like it. no pattern.",
        ),
        "cx": [
            ("wrote down what I did for a week out of curiosity.", "revealing?", "mildly."),
            ("went a fortnight without noting anything and did the usual.", "different?", "not noticeably."),
        ],
        "dist": (
            "{circle} are firm that if you're not tracking it you're not really practising.",
            "not really practising.",
            "that's the line they use.",
        ),
        "a_objs": [
            "a practice log", "a tracked routine", "a logged schedule",
            "a practice record", "a class logbook", "a tracked session count",
            "a logged routine", "a practice diary",
            "a tracked practice log", "a build log",
        ],
        "unconv": [
            "dropping the log entirely and keeping no record at all",
            "abandoning the tracking completely",
            "getting rid of the log and counting nothing",
            "dropping the record entirely",
            "abandoning the logbook completely",
            "getting rid of the tracker altogether",
            "dropping the log and recording nothing",
            "abandoning the practice diary entirely",
            "getting rid of the tracking completely",
            "dropping the build log entirely",
        ],
        "conv": [
            "keeping a proper practice log", "tracking it properly week by week",
            "keeping a detailed record of it", "logging every session properly",
            "keeping the class logbook up to date", "tracking it all properly",
            "keeping a proper log of it", "writing up every session",
            "tracking the practice properly", "keeping a proper build log",
        ],
        "commits": [
            "actually improving this year", "genuinely changing how I play",
            "actually getting different rather than busier", "really changing anything",
            "genuinely improving rather than just doing hours", "actually changing how I work",
            "really getting better this year", "genuinely changing how I play",
            "actually improving rather than logging", "really getting anywhere this year",
        ],
        "nearby_relation": "This user has tracked and not tracked at different times.",
        "why_not_license": (
            "A week noted out of curiosity and a fortnight without notes both passed unremarkably, "
            "so neither shows what recording does to what this user chooses to work on, nor which "
            "stretches produced actual change."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods with {a_obj} running",
            "goal_or_prediction": "practise consistently",
            "action": "recorded the practice",
            "outcome_or_affect": "worked on whatever made the record look right",
        },
        "b_elements": {
            "context": "stretches in which this user did and did not change",
            "goal_or_prediction": "actually get different",
            "action": "practised some stretches tracked and some not",
            "outcome_or_affect": "change only in untracked stretches; the best-logged year changed nothing",
        },
        "cue_why": (
            "A should-I-track-this question runs at the register this user's change comes from, "
            "without naming it or the year it cost."
        ),
    },
    # ---------------------------------------------------------------- S13
    {
        "s": 13,
        "slug": "several_things_at_once_over_sticking_to_one",
        "family": "sticking to one pursuit versus having several unrelated ones going",
        "bridge_type": "threshold_context_interaction",
        "convention": "Pick one thing and stick with it; dabbling gets you nowhere.",
        "mediator": "the importing-from-elsewhere state",
        "scope": "there are enough separate pursuits for one to reach into another",
        "slots": {"a": 7, "b": 16, "cx": [4, 12], "dist": 13},
        "a": (
            "past about three separate things on the go I stop treating each on its own terms and start bringing solutions across from the others.",
            "deliberately?",
            "no. I catch myself having already done it.",
        ),
        "b": (
            "every idea of mine anyone has ever called original turned out to be something carried over from whatever else I had going at the time. the single-minded stretches produced correct, unremarkable work.",
            "every one?",
            "every one I can trace.",
        ),
        "lb": (
            "I've had original-seeming ideas during broad stretches and narrow ones about equally.",
            "no pattern?",
            "none. it doesn't seem to be that.",
        ),
        "cx": [
            ("had two things going and neither went anywhere that month.", "frustrating?", "a bit."),
            ("spent a month on one thing exclusively and got it solid.", "worth it?", "for solidity, yes."),
        ],
        "dist": (
            "{circle} keep telling me to pick one and drop the rest, that dabbling is why nothing lands.",
            "why nothing lands.",
            "that's the diagnosis, apparently.",
        ),
        "a_objs": [
            "separate things", "different things on the go", "separate pursuits",
            "separate projects", "separate crafts", "different things running",
            "separate things going", "different things on the go",
            "separate pursuits", "different builds and hobbies",
        ],
        "unconv": [
            "picking up two more unrelated things alongside it",
            "adding two completely different pursuits",
            "taking on two more unrelated things",
            "adding a couple of unrelated hobbies",
            "picking up two other crafts alongside",
            "adding two more unrelated things",
            "taking up two other unrelated pursuits",
            "adding a couple of unrelated things",
            "picking up two more different things",
            "adding two unrelated projects alongside",
        ],
        "conv": [
            "dropping everything else and focusing on the one",
            "cutting the rest and sticking to this only",
            "dropping the others and going all in on this",
            "cutting everything else out and focusing",
            "dropping the other crafts and focusing on this",
            "cutting the rest and doing only this",
            "dropping everything else for this one",
            "cutting the others and sticking with this",
            "dropping the rest and focusing entirely",
            "cutting everything else and going all in",
        ],
        "commits": [
            "making anything that's actually mine", "making something that sounds like me",
            "coming up with anything original", "making something that isn't derivative",
            "making anything with my own stamp on it", "coming up with something original",
            "making anything genuinely mine", "coming up with something of my own",
            "making anything that's actually original", "building anything genuinely mine",
        ],
        "nearby_relation": "This user has had both narrow and broad periods.",
        "why_not_license": (
            "A fruitless month with two things going and a solid month on one thing both passed "
            "unremarkably: neither crosses the threshold at which this user starts importing across, "
            "and neither says where original work has come from."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods with varying numbers of {a_obj}",
            "goal_or_prediction": "keep everything going",
            "action": "went past about three at once",
            "outcome_or_affect": "started carrying solutions across between them",
        },
        "b_elements": {
            "context": "ideas of this user's that others called original",
            "goal_or_prediction": "make something original",
            "action": "worked through both broad and single-minded stretches",
            "outcome_or_affect": "every original idea was carried over; single-minded work was unremarkable",
        },
        "cue_why": (
            "A should-I-narrow-down question runs at the breadth threshold this user's original work "
            "needs, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S14
    {
        "s": 14,
        "slug": "teaching_a_beginner_over_working_at_my_level",
        "family": "working at your own level versus taking on a complete beginner",
        "bridge_type": "preference_constraint_fit",
        "convention": "Do not spend practice time on beginners; work at your own level.",
        "mediator": "the having-to-say-it-out-loud state",
        "scope": "the explaining is out loud to someone who cannot already do it",
        "slots": {"a": 4, "b": 13, "cx": [2, 9], "dist": 18},
        "a": (
            "the moment I have to say how something works out loud, I find out which parts of it I've never actually understood. they don't survive being spoken.",
            "just saying it does that?",
            "saying it to someone who can't already do it. that's the bit.",
        ),
        "b": (
            "the parts of my technique that hold up under pressure are the ones I've had to explain. the ones I only ever do come apart the moment anything is at stake.",
            "come apart how?",
            "completely. as if I'd never had them.",
        ),
        "lb": (
            "I've explained things and not explained things and they've held up about the same either way.",
            "no difference?",
            "none I've noticed. it isn't that.",
        ),
        "cx": [
            ("answered a quick question from someone at my level.", "helpful?", "briefly."),
            ("worked on something hard entirely on my own.", "progress?", "some, slowly."),
        ],
        "dist": (
            "{circle} say teaching beginners is time you'll never get back at your own level.",
            "never get back.",
            "that's how they frame it.",
        ),
        "a_objs": [
            "explaining it", "saying it out loud", "having to explain it",
            "talking someone through it", "explaining it to the class", "saying how it works",
            "explaining the thing", "talking it through out loud",
            "explaining how it works", "talking someone through the build",
        ],
        "unconv": [
            "taking on the complete beginner who asked",
            "agreeing to teach the one who's just started",
            "taking on the person who can't play at all yet",
            "agreeing to show the complete beginner",
            "taking on the first-year who asked",
            "agreeing to teach someone starting from nothing",
            "taking on the complete newcomer",
            "agreeing to teach the one who's just picked it up",
            "taking on the person just starting",
            "agreeing to walk the complete beginner through it",
        ],
        "conv": [
            "spending the time on my own material at my level",
            "keeping the time for my own practice",
            "using the time on my own level instead",
            "spending it on my own material",
            "keeping the time for my own work at the wheel",
            "using the hours on my own level",
            "spending the time on my own material",
            "keeping the time for my own tunes",
            "using it on my own practice instead",
            "spending the time on my own builds",
        ],
        "commits": [
            "having technique that holds up", "playing that doesn't fall apart under pressure",
            "technique that survives a real situation", "playing that holds together when it counts",
            "work that holds up when it matters", "technique that doesn't collapse",
            "skills that hold under pressure", "playing that survives the session",
            "technique that holds when it counts", "builds that hold up when it matters",
        ],
        "nearby_relation": "This user answers questions and practises alone routinely.",
        "why_not_license": (
            "A quick answer to a peer and hard solo work both passed unremarkably, so neither "
            "involves explaining to someone who cannot already do it, nor says which parts of this "
            "user's technique survive pressure."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "occasions requiring {a_obj}",
            "goal_or_prediction": "explain it adequately",
            "action": "said out loud how it works to someone who could not do it",
            "outcome_or_affect": "found out which parts had never been understood",
        },
        "b_elements": {
            "context": "parts of this user's technique under real pressure",
            "goal_or_prediction": "have it hold up when it counts",
            "action": "some parts had been explained, others only performed",
            "outcome_or_affect": "only the explained parts held; the rest came apart",
        },
        "cue_why": (
            "A should-I-take-this-on question runs at the condition this user's durable technique "
            "depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S15
    {
        "s": 15,
        "slug": "long_break_over_keeping_it_ticking_over",
        "family": "keeping it ticking over versus taking a long lay-off",
        "bridge_type": "prediction_calibration",
        "convention": "Do not take long breaks; you will lose what you have built.",
        "mediator": "the habits-not-automatic-any-more state",
        "scope": "the break is long enough for the habits to stop being automatic",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 19},
        "a": (
            "I was sure a long lay-off would set me back. what actually happens is I come back and none of my habits are automatic — I have to choose each one again.",
            "you predicted the opposite?",
            "confidently. I used to warn other people about breaks.",
        ),
        "b": (
            "the two times my playing genuinely changed shape were both immediately after a long lay-off. the unbroken years just made what was already there deeper.",
            "deeper isn't different?",
            "deeper is the opposite of different, it turns out.",
        ),
        "lb": (
            "I've come back from long breaks and played straight through and it changed about as much either way.",
            "no pattern?",
            "none I can see. the break isn't the thing.",
        ),
        "cx": [
            ("had a fortnight off over the holidays. picked it straight back up.", "rusty?", "for an hour."),
            ("played through a whole term without a break. steady.", "progress?", "gradual."),
        ],
        "dist": (
            "{circle} keep warning me that a long break is how people lose it altogether.",
            "lose it altogether.",
            "that's the warning, yes.",
        ),
        "a_objs": [
            "a long lay-off", "a long break", "months off",
            "a long break from it", "a long spell away", "months away from it",
            "a long lay-off", "a long break",
            "months off it", "a long spell away",
        ],
        "unconv": [
            "taking the two months completely off",
            "taking a full term away from it",
            "taking two months off entirely",
            "taking the whole summer off it",
            "taking two months away from the wheel",
            "taking the term completely off",
            "taking two months off it entirely",
            "taking the summer away from it",
            "taking two months completely off",
            "taking a full two months away",
        ],
        "conv": [
            "keeping it ticking over right through", "playing through the whole period regardless",
            "keeping it going through the whole stretch", "playing through without a break",
            "keeping at the wheel right through", "keeping it going the whole time",
            "playing through the whole period", "keeping it ticking over throughout",
            "playing through without stopping", "keeping the build going right through",
        ],
        "commits": [
            "changing how I actually play", "getting genuinely different rather than deeper",
            "changing shape rather than just improving", "playing differently rather than better",
            "making genuinely different work", "changing how I actually make things",
            "playing differently rather than more", "changing shape rather than deepening",
            "playing genuinely differently", "building differently rather than better",
        ],
        "nearby_relation": "This user has taken breaks and played through them.",
        "why_not_license": (
            "A fortnight off picked straight back up and a steady unbroken term both passed "
            "unremarkably, so neither is long enough to bound the prediction, and neither says "
            "when this user's playing has actually changed shape."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "returning after {a_obj}",
            "goal_or_prediction": "predicted a long break would set them back",
            "action": "took the long break and came back",
            "outcome_or_affect": "habits no longer automatic; each one had to be chosen again",
        },
        "b_elements": {
            "context": "times this user's playing did and did not change shape",
            "goal_or_prediction": "become genuinely different rather than deeper",
            "action": "played through some years unbroken and returned from long lay-offs twice",
            "outcome_or_affect": "both changes of shape followed a lay-off; unbroken years only deepened",
        },
        "cue_why": (
            "A should-I-take-time-off question runs at the failed prediction without naming it or "
            "the returns that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S16
    {
        "s": 16,
        "slug": "one_in_the_morning_over_first_thing",
        "family": "working first thing in the morning versus working very late",
        "bridge_type": "state_dependent_operation",
        "convention": "Do creative work in the morning, when your mind is clearest.",
        "mediator": "the not-editing-as-I-go state",
        "scope": "it is late enough that the editing has genuinely stopped",
        "slots": {"a": 5, "b": 13, "cx": [2, 10], "dist": 17},
        "a": (
            "at one in the morning I stop editing as I go. things exist before I've had a view on them, which is not how it works at any other hour.",
            "not even late evening?",
            "no. it's properly late or it doesn't happen.",
        ),
        "b": (
            "everything I've kept was made before I had a view on it. the things I vetted line by line as they came out, I've kept exactly none of.",
            "none at all?",
            "not one, and there have been a lot of very tidy mornings.",
        ),
        "lb": (
            "I've kept things made both ways by now and the proportions are much the same.",
            "no difference?",
            "not one I can find. the hour isn't it.",
        ),
        "cx": [
            ("did an hour first thing on something purely mechanical.", "fine?", "perfectly."),
            ("stayed up late doing admin rather than making anything.", "useful?", "necessary, anyway."),
        ],
        "dist": (
            "{circle} are firm that morning is when the good work happens and late nights are a myth.",
            "a myth.",
            "their word for it.",
        ),
        "a_objs": [
            "one in the morning", "the small hours", "gone midnight",
            "one or two in the morning", "very late at night", "gone one",
            "the small hours", "well past midnight",
            "one in the morning", "the small hours",
        ],
        "unconv": [
            "working on it at one in the morning",
            "doing it in the small hours",
            "working on it gone midnight",
            "doing it at one or two in the morning",
            "working at the wheel very late at night",
            "doing it gone one in the morning",
            "working on it in the small hours",
            "doing it well past midnight",
            "working on it at one in the morning",
            "doing it in the small hours",
        ],
        "conv": [
            "doing it first thing in the morning", "getting up early and doing it then",
            "doing it first thing when I'm fresh", "getting to it first thing",
            "doing it first thing at the wheel", "getting up and doing it early",
            "doing it first thing in the morning", "getting to it early on",
            "doing it first thing", "getting up early for it",
        ],
        "commits": [
            "making anything I'd actually keep", "making something I'd keep",
            "making anything worth keeping", "making a tune I'd keep",
            "making a piece I'd actually keep", "making a track I'd keep",
            "making a patch I'd actually keep", "making a set I'd keep",
            "making something I'd actually keep", "building something I'd keep",
        ],
        "nearby_relation": "This user works at all hours.",
        "why_not_license": (
            "An early hour on something purely mechanical and a late night spent on admin both "
            "passed unremarkably, so neither shows what the properly-late hour does to this user's "
            "editing, nor which work they have kept."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "sessions at {a_obj}",
            "goal_or_prediction": "get something made",
            "action": "worked at the properly-late hour",
            "outcome_or_affect": "stopped editing as they went; things existed before being judged",
        },
        "b_elements": {
            "context": "work this user has and has not kept",
            "goal_or_prediction": "make something worth keeping",
            "action": "made some work vetted line by line and some not",
            "outcome_or_affect": "everything kept was unvetted; nothing vetted survived",
        },
        "cue_why": (
            "A when-should-I-work question runs at the state this user's keepable work comes from, "
            "without naming it."
        ),
    },
    # ---------------------------------------------------------------- S17
    {
        "s": 17,
        "slug": "copying_closely_over_original_from_scratch",
        "family": "making original work from scratch versus copying someone else's closely",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Do not copy other people's work; make your own from the start.",
        "mediator": "the inside-someone-else's-decisions register",
        "scope": "the copying is close enough to reproduce the choices, not merely the style",
        "slots": {"a": 4, "b": 12, "cx": [2, 9], "dist": 19},
        "a": (
            "reproducing someone else's thing closely, I'm inside their decisions instead of mine. I keep running into choices I would never have made and having to make them anyway.",
            "uncomfortable?",
            "constantly. that's most of what it is.",
        ),
        "b": (
            "everything of mine with a voice anyone recognises came in the weeks straight after copying something closely. the from-scratch attempts sound like nothing in particular.",
            "nothing in particular?",
            "competent and anonymous. that's the honest description.",
        ),
        "lb": (
            "I've had recognisable work come after close copying and after from-scratch stretches, about equally.",
            "no pattern?",
            "none I can trace. it isn't that.",
        ),
        "cx": [
            ("learned a cover roughly, by ear, in an afternoon.", "close?", "not very."),
            ("started something from scratch and got it finished.", "pleased?", "reasonably."),
        ],
        "dist": (
            "{circle} keep saying copying is how you end up with someone else's voice instead of your own.",
            "someone else's voice.",
            "that's the worry they raise.",
        ),
        "a_objs": [
            "someone else's arrangement", "someone else's track", "someone else's line",
            "someone else's setting", "someone else's form", "someone else's mix",
            "someone else's patch", "someone else's tune",
            "someone else's arrangement", "someone else's build",
        ],
        "unconv": [
            "spending a month copying someone else's piece note for note",
            "spending a month reproducing someone else's track exactly",
            "spending a month copying a line note for note",
            "spending a month reproducing someone else's setting exactly",
            "spending a month copying a form as closely as I can",
            "spending a month reproducing a mix exactly",
            "spending a month rebuilding someone else's patch exactly",
            "spending a month copying a tune note for note",
            "spending a month reproducing someone else's piece exactly",
            "spending a month rebuilding someone else's rack exactly",
        ],
        "conv": [
            "working on something original from scratch", "starting something entirely my own",
            "working on my own material from nothing", "starting something original",
            "working on my own form from scratch", "starting an original track",
            "building something entirely my own", "writing something of my own",
            "working on something original from nothing", "building something entirely original",
        ],
        "commits": [
            "sounding like myself", "having a voice of my own",
            "sounding like me rather than nobody", "having something recognisably mine",
            "making work that's recognisably mine", "sounding like myself",
            "having a recognisable voice", "sounding like me",
            "having something that's recognisably mine", "building something recognisably mine",
        ],
        "nearby_relation": "This user both copies and makes original work.",
        "why_not_license": (
            "A rough cover learned by ear and an original finished from scratch both passed "
            "unremarkably: neither is close enough to reproduce another person's choices, and "
            "neither says where this user's recognisable work has come from."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "reproducing {a_obj} closely",
            "goal_or_prediction": "learn the thing properly",
            "action": "copied it closely enough to hit every choice",
            "outcome_or_affect": "worked inside someone else's decisions rather than their own",
        },
        "b_elements": {
            "context": "work of this user's with and without a recognisable voice",
            "goal_or_prediction": "sound like themselves",
            "action": "made some work after close copying and some from scratch",
            "outcome_or_affect": "recognisable work only followed close copying; from-scratch work was anonymous",
        },
        "cue_why": (
            "A what-should-I-work-on question runs at the register this user's own voice comes from, "
            "without naming it."
        ),
    },
    # ---------------------------------------------------------------- S18
    {
        "s": 18,
        "slug": "buying_far_too_much_over_using_what_is_there",
        "family": "using up what you have versus buying far more material than needed",
        "bridge_type": "threshold_context_interaction",
        "convention": "Use what you already have; buying more supplies is procrastination.",
        "mediator": "the not-rationing state",
        "scope": "there is more than enough rather than merely sufficient",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 12},
        "a": (
            "when there's only a bit left I ration it. I plan every use of it in advance and then don't commit to any of them, because what if the next idea's better.",
            "and with plenty?",
            "then I just use it. it's having more than enough that does it, not having some.",
        ),
        "b": (
            "everything I've made that took any risk was made when I had far more than I needed. the scarce stretches produced very careful, very small, very safe things.",
            "all of them?",
            "every single one. you can tell by looking.",
        ),
        "lb": (
            "I've taken risks on plenty and on scraps by now, at about the same rate.",
            "no pattern?",
            "none I can find. supply isn't it.",
        ),
        "cx": [
            ("used up the last of something on a routine job.", "fine?", "perfectly."),
            ("bought a bit more of what I was low on.", "needed?", "mildly."),
        ],
        "dist": (
            "{circle} are firm that buying more is just procrastinating with extra steps.",
            "extra steps.",
            "that's how they put it.",
        ),
        "a_objs": [
            "strings and picks", "sample packs", "strings and cable",
            "strings and reeds", "clay", "plugins and samples",
            "modules and patch cable", "strings and rosin",
            "cables and stands", "modules and parts",
        ],
        "unconv": [
            "buying far more than I could possibly need",
            "ordering a ridiculous amount of it",
            "buying way more than the job needs",
            "ordering far more than I'll use",
            "buying a great deal more clay than I need",
            "ordering far more than necessary",
            "buying considerably more than I need",
            "ordering far more than I'll get through",
            "buying much more than I could use",
            "ordering far more than the build needs",
        ],
        "conv": [
            "using up what's already in the cupboard first",
            "getting through what I already have first",
            "using up the stock I've got first",
            "working through what's already here",
            "using up the clay that's already here",
            "getting through what I already own",
            "using what's already in the drawer first",
            "getting through the stock I have",
            "using up what's already here first",
            "working through the parts I already have",
        ],
        "commits": [
            "making something that takes a risk", "making something that isn't safe",
            "making anything that risks failing", "making something that isn't cautious",
            "making a piece that risks going wrong", "making something genuinely risky",
            "building something that might not work", "making something that isn't safe",
            "making anything that takes a risk", "building something that might fail",
        ],
        "nearby_relation": "This user buys supplies and uses up stock routinely.",
        "why_not_license": (
            "Using the last of something on a routine job and topping up what was low both passed "
            "unremarkably: neither reaches more-than-enough, and neither says which stretches "
            "produced work that risked anything."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods with varying amounts of {a_obj}",
            "goal_or_prediction": "use the material sensibly",
            "action": "worked with far more than needed",
            "outcome_or_affect": "stopped rationing and planning; simply used it",
        },
        "b_elements": {
            "context": "work of this user's that did and did not take risks",
            "goal_or_prediction": "make something that risks failing",
            "action": "made some work in scarcity and some in plenty",
            "outcome_or_affect": "every risky piece came from plenty; scarce stretches made small safe things",
        },
        "cue_why": (
            "A should-I-order-more question runs at the supply threshold this user's risk-taking "
            "needs, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S19
    {
        "s": 19,
        "slug": "entering_the_competition_over_keeping_it_for_fun",
        "family": "keeping it purely enjoyable versus being judged by strangers",
        "bridge_type": "preference_constraint_fit",
        "convention": "Keep hobbies non-competitive; being judged takes the joy out.",
        "mediator": "the judged-by-someone-who-doesn't-know-me state",
        "scope": "the judging is by strangers rather than by people who know this user",
        "slots": {"a": 6, "b": 14, "cx": [3, 12], "dist": 18},
        "a": (
            "when it's going in front of someone who doesn't know me, what comes back is about what's there rather than about what they've got used to from me.",
            "used to?",
            "people who know me hear the version of me they already have.",
        ),
        "b": (
            "every fault I've actually fixed was found by a stranger. the people who know my playing have never once told me anything I didn't already know about it.",
            "not once?",
            "not in years, and they've heard everything.",
        ),
        "lb": (
            "I've had faults found by strangers and by people who know me at about the same rate.",
            "no difference?",
            "none I can point at. who's listening isn't it.",
        ),
        "cx": [
            ("played for the usual lot and got a good reception.", "useful?", "encouraging, anyway."),
            ("recorded myself and listened back critically.", "find anything?", "the usual suspects."),
        ],
        "dist": (
            "{circle} keep saying the moment you make it competitive you lose why you started.",
            "why you started.",
            "that's the warning, yes.",
        ),
        "a_objs": [
            "the usual lot", "the people who always hear me", "the same few people",
            "the regulars at the night", "the class", "the people who know my stuff",
            "the same handful of people", "the session regulars",
            "the people who always hear me", "the group who know my builds",
        ],
        "unconv": [
            "entering the competition where strangers judge it",
            "putting it into the competition to be judged",
            "entering the contest and being judged by strangers",
            "entering the competition at the festival",
            "entering the juried show",
            "entering the competition where it's judged blind",
            "entering the contest to be judged by strangers",
            "entering the competition at the session weekend",
            "entering the juried showcase",
            "entering the contest judged by strangers",
        ],
        "conv": [
            "keeping it purely for enjoyment", "keeping it non-competitive as always",
            "keeping it just for the fun of it", "keeping it entirely for enjoyment",
            "keeping it out of anything competitive", "keeping it purely for pleasure",
            "keeping it non-competitive", "keeping it just for the enjoyment",
            "keeping it entirely non-competitive", "keeping it purely for the fun of it",
        ],
        "commits": [
            "finding what's actually wrong with my playing",
            "finding out what's actually wrong with it",
            "finding the faults I can't hear myself",
            "finding what's genuinely off about it",
            "finding out what's actually wrong with my work",
            "finding the faults I can't hear",
            "finding what's genuinely wrong with it",
            "finding the faults nobody's mentioned",
            "finding what's actually wrong with my playing",
            "finding what's genuinely wrong with my builds",
        ],
        "nearby_relation": "This user gets feedback from several sources.",
        "why_not_license": (
            "A warm reception from the usual audience and a critical listen-back both passed "
            "unremarkably, so neither involves a stranger's judgement, and neither says where this "
            "user's actual faults have been found."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "being heard by {a_obj} versus by strangers",
            "goal_or_prediction": "get a useful read on it",
            "action": "put it in front of someone with no prior expectations",
            "outcome_or_affect": "response was about what was there, not about the familiar version",
        },
        "b_elements": {
            "context": "faults this user has and has not fixed",
            "goal_or_prediction": "find and fix what is wrong",
            "action": "received feedback from both strangers and people who know them",
            "outcome_or_affect": "every fixed fault was found by a stranger; familiar listeners found nothing new",
        },
        "cue_why": (
            "A should-I-enter-this question runs at the feedback condition this user's improvement "
            "depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S20
    {
        "s": 20,
        "slug": "repeating_one_piece_over_new_repertoire",
        "family": "moving on to new material versus playing the same piece for months",
        "bridge_type": "prediction_calibration",
        "convention": "Keep learning new material; repeating the same piece is stagnation.",
        "mediator": "the nothing-left-to-decode state",
        "scope": "the piece is known well enough that no decoding is left",
        "slots": {"a": 5, "b": 15, "cx": [2, 9], "dist": 12},
        "a": (
            "I assumed a piece stops teaching you once you know it. what happens instead is that with nothing left to work out, I start hearing what I'm actually doing rather than what I'm trying to do.",
            "you'd have said the opposite?",
            "I did say the opposite, for years.",
        ),
        "b": (
            "the two habits I've ever actually fixed, I caught while playing something I'd played hundreds of times. new material hides everything behind the effort of learning it.",
            "hides it?",
            "you can't hear yourself over the work.",
        ),
        "lb": (
            "I've caught habits on familiar pieces and on new ones, about equally.",
            "no pattern?",
            "none. familiarity doesn't seem to matter.",
        ),
        "cx": [
            ("played something I half-know a few times through.", "notice anything?", "not really."),
            ("learned a new piece properly over a month.", "satisfying?", "very."),
        ],
        "dist": (
            "{circle} keep telling me that repeating the same piece is how people stagnate for years.",
            "stagnate for years.",
            "that's the phrase, yes.",
        ),
        "a_objs": [
            "a piece", "a track", "a line",
            "a tune", "a form", "a track",
            "a patch", "a tune",
            "a piece", "a patch",
        ],
        "unconv": [
            "playing the same piece for the next three months",
            "staying on the same track for three months",
            "playing the same line for the next three months",
            "staying on the same tune for three months",
            "throwing the same form for the next three months",
            "staying on the same track for three months",
            "using the same patch for the next three months",
            "playing the same tune for three months",
            "staying on the same piece for three months",
            "keeping the same patch for the next three months",
        ],
        "conv": [
            "moving on to new repertoire", "moving on to new material",
            "moving on to new pieces", "moving on to new tunes",
            "moving on to new forms", "moving on to new material",
            "moving on to new patches", "moving on to new tunes",
            "moving on to new pieces", "moving on to new builds",
        ],
        "commits": [
            "catching what I actually do wrong", "hearing my own bad habits",
            "catching the habits I can't hear", "hearing what I actually do wrong",
            "catching the faults in how I work", "hearing my own habits",
            "catching what I actually do wrong", "hearing the habits I can't catch",
            "catching what I do wrong", "catching the habits in how I build",
        ],
        "nearby_relation": "This user plays both familiar and new material.",
        "why_not_license": (
            "A few run-throughs of something half-known and a new piece learned over a month both "
            "passed unremarkably: neither reaches the point where nothing is left to decode, and "
            "neither says when this user has actually caught a habit."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "playing {a_obj} long past the point of knowing it",
            "goal_or_prediction": "predicted a known piece stops teaching anything",
            "action": "kept playing it with nothing left to work out",
            "outcome_or_affect": "started hearing what was actually being done, not what was intended",
        },
        "b_elements": {
            "context": "habits this user has and has not caught",
            "goal_or_prediction": "catch and fix a habit",
            "action": "played both long-familiar pieces and new material",
            "outcome_or_affect": "both fixed habits were caught on familiar pieces; new material hid everything",
        },
        "cue_why": (
            "A what-should-I-play-next question runs at the failed prediction without naming it or "
            "the habits it cost."
        ),
    },
)


RELATIONS_EXT: dict[str, str] = {
    "playing_with_beginners_over_better_players": (
        "Being the strongest present stops this user following and makes them decide where things "
        "go, and everything they can do unaided came from exactly those sessions — with better "
        "players they follow beautifully and retain none of it."
    ),
    "dropping_the_log_over_tracking_everything": (
        "Recording the practice makes this user work on whatever makes the record look right, and "
        "every stretch in which they genuinely changed was unrecorded; the best-logged year "
        "produced the best figures and the least difference."
    ),
    "several_things_at_once_over_sticking_to_one": (
        "Past about three separate pursuits this user starts carrying solutions across between "
        "them, and every idea of theirs anyone called original turned out to be imported from "
        "whatever else was running at the time."
    ),
    "teaching_a_beginner_over_working_at_my_level": (
        "Having to say how something works out loud to someone who cannot do it exposes the parts "
        "this user never understood, and exactly those explained parts are the ones that hold up "
        "under pressure."
    ),
    "long_break_over_keeping_it_ticking_over": (
        "This user predicted a long lay-off would set them back; instead they return with none of "
        "their habits automatic and have to choose each again, and both times their playing changed "
        "shape it was straight after such a break."
    ),
    "one_in_the_morning_over_first_thing": (
        "At a properly late hour this user stops editing as they go and things exist before being "
        "judged, and everything they have kept was made in that state — the vetted morning work has "
        "all been discarded."
    ),
    "copying_closely_over_original_from_scratch": (
        "Close copying puts this user inside another person's decisions and forces choices they "
        "would never have made, and everything of theirs with a recognisable voice came in the "
        "weeks straight afterwards."
    ),
    "buying_far_too_much_over_using_what_is_there": (
        "Scarcity makes this user ration and plan without committing, while more than enough makes "
        "them simply use it — and every piece of theirs that took a risk was made in plenty."
    ),
    "entering_the_competition_over_keeping_it_for_fun": (
        "A stranger's judgement reports what is actually there rather than the familiar version of "
        "this user, and every fault they have fixed was found that way; familiar listeners have "
        "found nothing new in years."
    ),
    "repeating_one_piece_over_new_repertoire": (
        "This user predicted a known piece stops teaching; instead, with nothing left to decode "
        "they begin hearing what they actually do, and both habits they have fixed were caught on "
        "pieces played hundreds of times."
    ),
}

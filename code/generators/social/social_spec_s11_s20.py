"""Scenario families S11-S20, extending the batch to 200 units / 600 files.

Same contract as `social_spec.SCENARIOS`. Every proposition is counter-conventional,
ev_A supplies trigger -> mediator and the scope of that state, ev_B supplies
mediator -> outcome, and neither half alone completes the chain. Bridge types
continue the two-per-type rotation so all five are used four times across S1-S20.
"""

from __future__ import annotations

SCENARIOS_EXT: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S11
    {
        "s": 11,
        "slug": "argument_by_text_over_face_to_face",
        "family": "settling a disagreement in writing versus face to face",
        "bridge_type": "state_dependent_operation",
        "convention": "Have difficult conversations face to face, not over text.",
        "mediator": "the delayed, re-readable register",
        "scope": "the exchange stays written rather than moving to a call",
        "slots": {"a": 6, "b": 15, "cx": [3, 10], "dist": 18},
        "a": (
            "in writing I answer slowly and re-read before anything goes out. nothing leaves my hands unconsidered, for better or worse.",
            "slower, then?",
            "much slower. hours, sometimes.",
        ),
        "b": (
            "the disagreements of mine that actually got resolved were the ones where nothing went out unconsidered. the ones where I answered in the moment, I either caved or escalated inside a minute and neither version stuck.",
            "caved or escalated?",
            "one or the other. never anything in between.",
        ),
        "lb": (
            "I've settled things considered and off-the-cuff by now and they came out much the same.",
            "no pattern?",
            "none I can point at. the pace doesn't decide it.",
        ),
        "cx": [
            ("sent a long message about logistics. clear enough, nobody argued.", "smooth?", "unremarkably so."),
            ("had a quick chat at the door about the bins.", "resolved?", "resolved, obviously."),
        ],
        "dist": (
            "{circle} are adamant you should never have a serious disagreement over text.",
            "adamant?",
            "unanimously, and at length.",
        ),
        "a_objs": [
            "writing", "typing it out", "putting it in a message",
            "writing it down", "doing it in writing", "typing rather than talking",
            "writing it out first", "putting it in writing",
            "writing instead of calling", "doing it in text",
        ],
        "unconv": [
            "hashing it out over text", "doing the whole thing by message",
            "settling it in writing", "having it out over messages",
            "doing it entirely in writing", "keeping the whole thing to text",
            "working it through by message", "settling it over text",
            "doing it in writing rather than in person", "having the whole argument by message",
        ],
        "conv": [
            "sitting down face to face over coffee", "having it out in person",
            "doing it face to face over lunch", "sitting down together in person",
            "having the conversation in person", "doing it face to face",
            "sitting down with them in person", "having it out over a drink",
            "doing it in person rather than by message", "meeting up and talking it through",
        ],
        "commits": [
            "the disagreement with my flatmate", "the falling-out with my corridor friend",
            "the row with my cousin", "the argument with my old teammate",
            "the disagreement with my sister-in-law", "the falling-out with my coursemate",
            "the disagreement with someone in the book group", "the row with my neighbour",
            "the falling-out with my studio friend", "the disagreement with someone in the circle",
        ],
        "nearby_relation": "This user communicates fine in both registers.",
        "why_not_license": (
            "A clear logistics message and a quick doorstep exchange both went fine, so neither "
            "shows what the written register does for this user, nor which register their actual "
            "disagreements survive."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} about {commit}",
        "a_elements": {
            "context": "disagreements handled by {a_obj}",
            "goal_or_prediction": "say the considered thing",
            "action": "answered slowly and re-read before sending",
            "outcome_or_affect": "nothing left unconsidered; hours of delay",
        },
        "b_elements": {
            "context": "disagreements handled in both registers over years",
            "goal_or_prediction": "actually resolve the thing",
            "action": "answered some considered, others in the moment",
            "outcome_or_affect": "only the considered ones resolved; in-the-moment ones caved or escalated",
        },
        "cue_why": (
            "A live disagreement raises an ordinary how-should-I-do-this question that runs at the "
            "register this user's conflicts survive, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S12
    {
        "s": 12,
        "slug": "batched_absence_over_constant_availability",
        "family": "constant availability versus scarce, batched attention",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Being reliably available is what makes you a good friend.",
        "mediator": "the batched, all-at-once attention",
        "scope": "the contact stays batched rather than spread across the days",
        "slots": {"a": 5, "b": 14, "cx": [2, 11], "dist": 17},
        "a": (
            "when I'm reachable all day I answer everything at the surface and finish none of it. when I've been unreachable a while it comes out all at once instead.",
            "all at once?",
            "one long go, rather than forty small ones.",
        ),
        "b": (
            "the people who say I was there for them are the ones who got the whole thing in one go. the ones I answered every day never got more than the top layer, and they know it.",
            "they've said so?",
            "one of them has, in as many words.",
        ),
        "lb": (
            "I've done both with people since — steady daily and all-at-once — and it came out the same either way.",
            "no difference?",
            "none. the shape of it doesn't seem to matter.",
        ),
        "cx": [
            ("answered a run of quick questions over a day. all handled.", "efficient?", "perfectly."),
            ("was uncontactable for a weekend and nothing broke.", "guilt?", "briefly."),
        ],
        "dist": (
            "{circle} keep saying that being consistently available is the whole of being a good friend.",
            "the whole of it?",
            "that's how they put it.",
        ),
        "a_objs": [
            "reachable all day", "always on my phone", "contactable constantly",
            "available at all hours", "on call basically", "reachable whenever",
            "always available", "contactable all day",
            "reachable at any hour", "always on",
        ],
        "unconv": [
            "going quiet for a fortnight then giving them a whole evening",
            "disappearing for two weeks and then a full night of it",
            "being unreachable a while then giving them the whole day",
            "going dark for a stretch then one long uninterrupted go",
            "being hard to reach then giving them an entire evening",
            "dropping off for two weeks then a whole afternoon of it",
            "going quiet then giving them one long proper session",
            "being uncontactable a while then a full evening",
            "disappearing for a bit then one long unbroken go",
            "going quiet then giving them the whole evening",
        ],
        "conv": [
            "checking in with them every day", "staying reachable for them daily",
            "messaging them every single day", "keeping in touch daily without fail",
            "checking in on them each day", "being available to them every day",
            "keeping a daily check-in going", "staying contactable for them daily",
            "checking in every day without fail", "keeping in daily contact",
        ],
        "commits": [
            "the friend going through the divorce", "the friend who lost their job",
            "the cousin whose father is ill", "the teammate who is struggling",
            "the friend who has just been bereaved", "the coursemate who is falling apart",
            "the book-group friend going through it", "the neighbour who is unwell",
            "the studio friend having a hard year", "the friend in the circle going through it",
        ],
        "nearby_relation": "This user is responsive and reliable.",
        "why_not_license": (
            "A day of quick answers and an uneventful unreachable weekend both passed without "
            "consequence; neither says which pattern of attention the people who needed something "
            "actually received."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "stretches of being {a_obj}",
            "goal_or_prediction": "be responsive",
            "action": "answered everything as it arrived",
            "outcome_or_affect": "surface-level answers, nothing finished; batched otherwise",
        },
        "b_elements": {
            "context": "people this user supported through something hard",
            "goal_or_prediction": "actually be there for them",
            "action": "gave some batched attention, others daily contact",
            "outcome_or_affect": "only the batched ones felt supported; daily ones got the top layer",
        },
        "cue_why": (
            "Someone close is going through something, which raises a natural how-should-I-show-up "
            "question without naming the pattern that has worked."
        ),
    },
    # ---------------------------------------------------------------- S13
    {
        "s": 13,
        "slug": "newcomer_over_regulars_only",
        "family": "keeping a close group to its regulars versus bringing in a newcomer",
        "bridge_type": "threshold_context_interaction",
        "convention": "Do not bring an outsider to a close-knit group evening.",
        "mediator": "the explaining-ourselves-from-scratch state",
        "scope": "the group is large enough to have settled into its own stories",
        "slots": {"a": 7, "b": 16, "cx": [3, 12], "dist": 13},
        "a": (
            "past about six of the regulars and nobody new, we run the same three stories all night. with someone new in the room we have to explain ourselves from scratch instead.",
            "the same three?",
            "verbatim, at this point.",
        ),
        "b": (
            "the evenings where anyone said something they hadn't said before were the ones where we'd had to explain ourselves from the beginning. the fluent ones stay funny and reveal nothing.",
            "nothing at all?",
            "nothing anyone didn't already know.",
        ),
        "lb": (
            "we've had both kinds of evening plenty of times and new things came out about equally.",
            "so it's not that?",
            "doesn't look like it. no clear pattern.",
        ),
        "cx": [
            ("had three of us round the kitchen table. easy, unremarkable.", "good night?", "quietly, yes."),
            ("brought someone new to a big loud thing where nobody talked.", "how'd they find it?", "fine, I think."),
        ],
        "dist": (
            "{circle} say you should never bring an outsider to something this close-knit.",
            "never?",
            "they were quite firm about it.",
        ),
        "a_objs": [
            "the regulars", "the usual res-hall lot", "the Sunday regulars",
            "the match-day regulars", "the usual pair of couples", "the usual four",
            "the core book group", "the usual neighbours",
            "the usual gallery crowd", "the usual workshop circle",
        ],
        "unconv": [
            "bringing someone new along", "bringing a complete outsider",
            "bringing someone none of them know", "inviting someone from outside the group",
            "bringing along someone new to all of them", "inviting a total newcomer",
            "bringing in someone from outside", "inviting someone none of them have met",
            "bringing a newcomer along", "inviting someone entirely new",
        ],
        "conv": [
            "keeping it to the usual people", "keeping it to just the regulars",
            "keeping it to the same group as always", "keeping it to the core lot",
            "keeping it to the usual few", "keeping it to just us",
            "keeping it to the regular members", "keeping it to the usual crowd",
            "keeping it to the regulars only", "keeping it to the same people as always",
        ],
        "commits": [
            "the dinner where I want to actually talk to my old friend",
            "the night where I want to get somewhere with my corridor friend",
            "the lunch where I want a real conversation with my brother-in-law",
            "the evening where I want to get past small talk with my teammate",
            "the dinner where I want to actually hear how my sister is",
            "the night where I want a real conversation with my coursemate",
            "the evening where I want to get somewhere with the newer member",
            "the gathering where I want to actually talk to my neighbour",
            "the night where I want a real conversation with my studio friend",
            "the evening where I want to get somewhere with someone in the circle",
        ],
        "nearby_relation": "This user's group evenings are generally enjoyable.",
        "why_not_license": (
            "A quiet three-person kitchen table and a newcomer at a loud night where nobody talked "
            "both passed unremarkably, so neither shows the settled-group threshold, nor what "
            "having to explain yourselves produces."
        ),
        "query_unconv": "thinking of {unconv} to {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "evenings with {a_obj} at varying group sizes",
            "goal_or_prediction": "have a decent evening",
            "action": "kept the group to its settled regulars",
            "outcome_or_affect": "the same three stories; no need to explain anything",
        },
        "b_elements": {
            "context": "evenings where someone said something genuinely new",
            "goal_or_prediction": "get past the usual material",
            "action": "attended both fluent and explain-from-scratch evenings",
            "outcome_or_affect": "disclosures only ever came at the explain-from-scratch ones",
        },
        "cue_why": (
            "A guest-list question about an ordinary evening runs at the group condition this user "
            "needs, without naming it or the evenings it produced."
        ),
    },
    # ---------------------------------------------------------------- S14
    {
        "s": 14,
        "slug": "declining_once_over_always_turning_up",
        "family": "turning up out of obligation versus declining once and choosing freely after",
        "bridge_type": "preference_constraint_fit",
        "convention": "Show up for people — turning up is what counts.",
        "mediator": "the chosen-rather-than-owed footing",
        "scope": "the decline is stated plainly rather than dressed up as an excuse",
        "slots": {"a": 4, "b": 13, "cx": [2, 9], "dist": 18},
        "a": (
            "when I go to something because I feel I owe it, I'm in the room and nowhere near it — counting the time until I can reasonably leave.",
            "they notice?",
            "I assume not. I'd notice.",
        ),
        "b": (
            "the friendships that got stronger are ones where I'd said a plain no once and everything after that was chosen. the ones I never once declined went completely flat.",
            "flat how?",
            "polite. entirely polite, and nothing else.",
        ),
        "lb": (
            "I've declined plainly and I've never declined, with different people, and the friendships went the same way regardless.",
            "no effect?",
            "none I can see. it isn't that.",
        ),
        "cx": [
            ("went to a thing I actually wanted to go to. good night.", "unusual?", "not that unusual."),
            ("cancelled something last minute with a vague excuse.", "awkward?", "mildly, then forgotten."),
        ],
        "dist": (
            "{circle} keep telling me that just turning up is ninety percent of being a good friend.",
            "ninety?",
            "their figure.",
        ),
        "a_objs": [
            "obligation", "a sense of owing them", "duty",
            "feeling I should", "obligation rather than wanting to", "a sense of debt",
            "feeling I owe it", "obligation",
            "a sense I ought to", "feeling obliged",
        ],
        "unconv": [
            "saying a plain no to this one", "turning this one down outright",
            "declining this one plainly", "saying no to this one without dressing it up",
            "turning this one down straight", "declining this one outright",
            "saying a flat no to this one", "turning this one down plainly",
            "declining this one without an excuse", "saying no to this one straight out",
        ],
        "conv": [
            "turning up like I always do", "going along as usual",
            "showing up the way I always do", "turning up as I always have",
            "going as usual without question", "showing up like always",
            "turning up the way I always do", "going along as I always do",
            "showing up as usual", "turning up as always",
        ],
        "commits": [
            "the friendship with the person who invites me to everything",
            "the friendship with the one who organises the corridor",
            "the friendship with my cousin who hosts constantly",
            "the friendship with the teammate who runs everything",
            "the friendship with the couple who invite us to everything",
            "the friendship with the coursemate who plans it all",
            "the friendship with the one who founded the book group",
            "the friendship with the neighbour who organises everything",
            "the friendship with the studio friend who hosts",
            "the friendship with the one who runs the circle",
        ],
        "nearby_relation": "This user is a reliable attender.",
        "why_not_license": (
            "A night this user genuinely wanted and a vague last-minute cancellation both passed "
            "without consequence, so neither shows what obligation does to their presence, nor "
            "what a plain decline does to a friendship."
        ),
        "query_unconv": "thinking of {unconv}, given {commit}",
        "query_conv": "planning on {conv}, given {commit}",
        "a_elements": {
            "context": "events attended out of {a_obj}",
            "goal_or_prediction": "be a good friend by turning up",
            "action": "went because it felt owed",
            "outcome_or_affect": "physically present, mentally counting the time",
        },
        "b_elements": {
            "context": "friendships across years, some declined once and some never",
            "goal_or_prediction": "keep the friendships alive",
            "action": "said a plain no in some, never declined in others",
            "outcome_or_affect": "only the ones with a plain decline deepened; the rest went flat",
        },
        "cue_why": (
            "An ordinary invitation raises a turn-up-or-not question that runs at the footing this "
            "user's friendships need, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S15
    {
        "s": 15,
        "slug": "telling_them_once_settled_over_early_warning",
        "family": "early warning versus telling people once the decision is settled",
        "bridge_type": "prediction_calibration",
        "convention": "Tell people difficult news early so they have time to prepare.",
        "mediator": "the settled, already-decided state",
        "scope": "the decision is genuinely settled rather than still open",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 19},
        "a": (
            "I was sure telling people early would soften things. what actually happens is I re-open the decision every day until I've argued myself into knots and can't say what I want any more.",
            "every day?",
            "daily, for weeks. I'd have predicted the opposite.",
        ),
        "b": (
            "the people I told once it was properly settled took it far better. the two I told while it was still open both ended up managing my feelings instead of having their own.",
            "managing yours?",
            "reassuring me about my own decision. it isn't what I wanted from them.",
        ),
        "lb": (
            "I've told people early and late by now and it went about the same either way.",
            "no difference?",
            "not one I could defend. the timing doesn't seem to do it.",
        ),
        "cx": [
            ("mentioned a small change of plan a fortnight ahead. no drama.", "smooth?", "entirely."),
            ("told someone something the same day it happened. also fine.", "no issue?", "none."),
        ],
        "dist": (
            "{circle} are unanimous that you owe people as much warning as possible.",
            "unanimous?",
            "loudly, and without exception.",
        ),
        "a_objs": [
            "telling people early", "giving people early warning", "flagging it early",
            "telling them well ahead", "giving plenty of notice", "warning people early",
            "telling them in advance", "giving early notice",
            "flagging it well ahead", "telling people early on",
        ],
        "unconv": [
            "waiting until it's settled and telling them then",
            "holding off until the decision is final",
            "waiting until it's decided before saying anything",
            "saying nothing until it's actually settled",
            "waiting until the thing is final to tell them",
            "holding off until I've properly decided",
            "waiting until it's settled before telling them",
            "saying nothing until the decision is made",
            "holding it until it's genuinely decided",
            "waiting until it's final and telling them then",
        ],
        "conv": [
            "telling them now so they have time to prepare",
            "giving them as much warning as I can",
            "telling them early so it's not a shock",
            "flagging it now so they can get used to it",
            "giving them plenty of notice",
            "telling them early so they can prepare",
            "warning them now rather than later",
            "giving them the maximum notice",
            "telling them well in advance",
            "flagging it early so they have time",
        ],
        "commits": [
            "telling my parents about the move", "telling my family I'm not coming back",
            "telling my cousin I'm leaving", "telling the team I'm stepping back",
            "telling my in-laws about the plan", "telling my coursemates I'm deferring",
            "telling the book group I'm going", "telling the neighbours we're selling",
            "telling my studio friends I'm giving it up", "telling the circle I'm moving on",
        ],
        "nearby_relation": "This user handles difficult conversations reasonably well.",
        "why_not_license": (
            "A minor change flagged a fortnight ahead and something mentioned the same day both "
            "went fine, so neither calibrates a decision of consequence, nor says which state this "
            "user has to be in to deliver one."
        ),
        "query_unconv": "thinking of {unconv} about {commit}",
        "query_conv": "planning on {conv} about {commit}",
        "a_elements": {
            "context": "decisions of consequence disclosed early",
            "goal_or_prediction": "predicted early warning would soften it",
            "action": "told people while the decision was still open",
            "outcome_or_affect": "re-opened it daily and argued themselves into knots",
        },
        "b_elements": {
            "context": "people told at different stages of the same kind of decision",
            "goal_or_prediction": "have the conversation go well",
            "action": "told some once settled and two while still open",
            "outcome_or_affect": "the settled ones took it well; the early ones managed this user's feelings",
        },
        "cue_why": (
            "A pending disclosure raises an ordinary when-should-I-say-something question without "
            "naming the failed prediction or the conversations that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S16
    {
        "s": 16,
        "slug": "unprepared_hosting_over_meeting_out",
        "family": "meeting somewhere booked versus hosting with nothing prepared",
        "bridge_type": "state_dependent_operation",
        "convention": "If you cannot host properly, meet at a restaurant instead.",
        "mediator": "the unhosted, nobody-being-looked-after state",
        "scope": "nothing has actually been prepared in advance",
        "slots": {"a": 5, "b": 13, "cx": [2, 10], "dist": 17},
        "a": (
            "when the place is a state and there's no plan, I stop doing host entirely and just sit down with whoever's there.",
            "and when it is prepared?",
            "then I'm up and down all night doing jobs nobody asked for.",
        ),
        "b": (
            "the times anyone stayed till two talking, I hadn't been up and down doing jobs. the evenings I'd got everything ready, people left by ten having had a nice time.",
            "a nice time?",
            "a nice time, and nothing more than that.",
        ),
        "lb": (
            "I've had both kinds of evening and people stayed late or left early with no relation to which.",
            "so it isn't that?",
            "seems not. no pattern in it.",
        ),
        "cx": [
            ("tidied the flat on a night nobody came round.", "satisfying?", "quietly, yes."),
            ("met someone out for a quick unplanned drink. easy.", "good?", "perfectly fine."),
        ],
        "dist": (
            "{circle} say if the flat's not up to it you should just book somewhere and meet out.",
            "just book somewhere.",
            "that's the standard advice, apparently.",
        ),
        "a_objs": [
            "the flat", "my room", "the place",
            "the house", "the apartment", "my place",
            "the sitting room", "the house",
            "the studio flat", "the place",
        ],
        "unconv": [
            "having them over with the place exactly as it is",
            "having them round without tidying or planning anything",
            "having them over with nothing prepared",
            "having them round as the place stands",
            "having them over without getting anything ready",
            "having them round with no preparation at all",
            "having them over exactly as things are",
            "having them round without sorting the place out",
            "having them over with nothing done to the place",
            "having them round with nothing prepared at all",
        ],
        "conv": [
            "booking somewhere and meeting out instead",
            "finding a restaurant and meeting there",
            "booking a table somewhere instead",
            "meeting out at a booked place",
            "booking somewhere nice and meeting there",
            "finding somewhere out and meeting there",
            "booking a place and going out instead",
            "meeting somewhere booked rather than at mine",
            "booking a table and meeting out",
            "finding somewhere and meeting out instead",
        ],
        "commits": [
            "the evening with the friend I never really talk to",
            "the night with the corridor friend I barely know",
            "the evening with my brother-in-law",
            "the night with the teammate I've never really spoken to",
            "the evening with the couple we never get past pleasantries with",
            "the night with the coursemate I want to actually know",
            "the evening with the newer book-group member",
            "the night with the neighbours we only nod at",
            "the evening with the studio friend I never really talk to",
            "the night with the person in the circle I barely know",
        ],
        "nearby_relation": "This user hosts and goes out about equally.",
        "why_not_license": (
            "A tidy-up on an empty night and an easy drink out both passed without consequence, so "
            "neither shows what an unprepared evening does to this user's behaviour, nor what that "
            "behaviour produces in the people there."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "evenings at {a_obj} in varying states of preparation",
            "goal_or_prediction": "be a decent host",
            "action": "hosted with nothing prepared",
            "outcome_or_affect": "stopped performing host and sat down with people",
        },
        "b_elements": {
            "context": "evenings that ran late versus ones that ended early",
            "goal_or_prediction": "have people actually stay and talk",
            "action": "hosted some prepared and some not",
            "outcome_or_affect": "only the unprepared ones ran to two; prepared ones ended by ten",
        },
        "cue_why": (
            "A where-shall-we-do-this question runs at the hosting condition this user needs, "
            "without naming it or the evenings that established it."
        ),
    },
    # ---------------------------------------------------------------- S17
    {
        "s": 17,
        "slug": "side_by_side_group_trip_over_one_to_one",
        "family": "a one-to-one weekend versus a group trip with something to be getting on with",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "If you want to reconnect with someone, go one-to-one.",
        "mediator": "the side-by-side, something-else-to-do register",
        "scope": "there is a task to be getting on with rather than only conversation",
        "slots": {"a": 7, "b": 15, "cx": [4, 11], "dist": 19},
        "a": (
            "facing someone across a table I interview them — question, answer, next question. side by side with something to be getting on with, I actually talk.",
            "interview them?",
            "it's the only word for it. I can hear myself doing it.",
        ),
        "b": (
            "everything real I know about the people close to me, I learned while we were both busy with something else. the trips built entirely around talking produced nothing I didn't already know.",
            "nothing?",
            "three days of catching up and not one new thing.",
        ),
        "lb": (
            "I've done both kinds of trip since and learned about as much either way.",
            "so it doesn't matter?",
            "apparently not. no pattern to it.",
        ),
        "cx": [
            ("had a long lunch with one person. pleasant throughout.", "learn anything?", "not especially."),
            ("went on a big group thing where I barely spoke to anyone.", "worth going?", "it was fine."),
        ],
        "dist": (
            "{circle} keep telling me the only way to properly reconnect is one-to-one, no distractions.",
            "no distractions.",
            "that's the received wisdom, yes.",
        ),
        "a_objs": [
            "a table between us", "sitting opposite them", "facing each other",
            "sitting across from them", "a table between us", "facing them directly",
            "sitting opposite", "a table in between",
            "sitting face to face", "facing one another",
        ],
        "unconv": [
            "the six-person walking trip", "the group hiking weekend",
            "the eight-of-us cycling trip", "the group camping weekend",
            "the walking week with the whole group", "the group trip with the cabin to sort out",
            "the six-person walking holiday", "the group weekend with the boat to crew",
            "the group trip with the place to renovate", "the walking weekend with the whole circle",
        ],
        "conv": [
            "a weekend away, just the two of us", "a two-person trip with nothing planned",
            "a weekend with just the two of us", "a proper one-to-one weekend away",
            "a couple of days away, only the two of us", "a weekend away just us two",
            "a two-person weekend with time to talk", "a quiet weekend, just the pair of us",
            "a weekend away one-to-one", "a two-person trip with nothing but time",
        ],
        "commits": [
            "reconnecting with my oldest friend", "getting somewhere with my school friend",
            "reconnecting with my cousin", "getting somewhere with my old teammate",
            "reconnecting with my sister", "getting somewhere with my closest coursemate",
            "reconnecting with the book-group friend", "getting somewhere with my old neighbour",
            "reconnecting with my studio friend", "getting somewhere with my oldest friend",
        ],
        "nearby_relation": "This user is sociable in most settings.",
        "why_not_license": (
            "A pleasant long lunch and a big group thing with little conversation both passed "
            "unremarkably, so neither shows what the side-by-side arrangement does, nor where this "
            "user has actually learned anything about anyone."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "conversations with {a_obj} versus side by side",
            "goal_or_prediction": "have a real conversation",
            "action": "sat facing them with nothing else to do",
            "outcome_or_affect": "interviewed them rather than talking",
        },
        "b_elements": {
            "context": "occasions this user learned something real about someone close",
            "goal_or_prediction": "actually get to know them",
            "action": "went on both talk-centred trips and busy ones",
            "outcome_or_affect": "everything real came from the busy ones; talk-centred trips produced nothing",
        },
        "cue_why": (
            "A trip-planning question about reconnecting runs at the arrangement this user needs, "
            "without naming it or the trips that produced nothing."
        ),
    },
    # ---------------------------------------------------------------- S18
    {
        "s": 18,
        "slug": "arriving_late_over_arriving_early",
        "family": "arriving at the start versus walking into a room already going",
        "bridge_type": "threshold_context_interaction",
        "convention": "Arrive early so you get proper time with people.",
        "mediator": "the walking-into-something-already-going state",
        "scope": "the room is already going rather than still filling up",
        "slots": {"a": 8, "b": 16, "cx": [3, 6], "dist": 12},
        "a": (
            "if I'm there from the start I end up on door duty and drinks and coats, and I never land anywhere all night.",
            "the whole night?",
            "the whole night. I'm staff at that point.",
        ),
        "b": (
            "every conversation I actually remember from those nights started after I'd walked into a room that was already going.",
            "every one?",
            "every single one I can name.",
        ),
        "lb": (
            "I've arrived early and late to plenty of these and the conversations came out much the same.",
            "no difference?",
            "none I've noticed. arrival time doesn't seem to matter.",
        ),
        "cx": [
            ("got somewhere early and helped set up. straightforward.", "fine?", "perfectly fine."),
            ("turned up late to something small and quiet.", "how was it?", "unremarkable."),
        ],
        "dist": (
            "{circle} always say get there early, that's when you get the proper time with people.",
            "the proper time.",
            "that's the line, yes.",
        ),
        "a_objs": [
            "there from the start", "first to arrive", "there at the beginning",
            "early and setting up", "there before anyone", "first through the door",
            "there from the beginning", "early and helping out",
            "there before it starts", "first to turn up",
        ],
        "unconv": [
            "turning up two hours in", "arriving late, well after it's started",
            "getting there halfway through", "turning up once it's well under way",
            "arriving a couple of hours late", "getting there late on purpose",
            "turning up well after the start", "arriving once it's already going",
            "getting there two hours in", "turning up late, once it's running",
        ],
        "conv": [
            "getting there right at the start", "arriving at the beginning as usual",
            "turning up at the start to help", "getting there early for it",
            "arriving right at the start", "getting there at the beginning",
            "turning up at the start as always", "arriving early to help set up",
            "getting there for the start", "arriving at the very beginning",
        ],
        "commits": [
            "the party where I want to talk to my cousin",
            "the night where I want to catch my corridor friend properly",
            "the gathering where I want to talk to my brother-in-law",
            "the do where I want to actually speak to my old teammate",
            "the evening where I want a proper word with my sister",
            "the party where I want to talk to my coursemate",
            "the night where I want to catch the book-group friend",
            "the street thing where I want to talk to my neighbour",
            "the opening where I want to catch my studio friend",
            "the gathering where I want a proper word with someone in the circle",
        ],
        "nearby_relation": "This user goes to plenty of these and enjoys them.",
        "why_not_license": (
            "Helping set up early and turning up late to something small and quiet both passed "
            "unremarkably, so neither shows what arriving at the start costs this user, nor where "
            "their memorable conversations have actually started."
        ),
        "query_unconv": "thinking of {unconv} to {commit}",
        "query_conv": "planning on {conv} to {commit}",
        "a_elements": {
            "context": "nights this user was {a_obj}",
            "goal_or_prediction": "get proper time with people",
            "action": "arrived at the beginning",
            "outcome_or_affect": "absorbed into door duty and logistics; never landed anywhere",
        },
        "b_elements": {
            "context": "conversations this user actually remembers from such nights",
            "goal_or_prediction": "have something worth remembering",
            "action": "arrived early to some and late to others",
            "outcome_or_affect": "every remembered conversation began after a late arrival",
        },
        "cue_why": (
            "A what-time-shall-I-get-there question runs at the arrival condition this user needs, "
            "without naming it or the nights that established it."
        ),
    },
    # ---------------------------------------------------------------- S19
    {
        "s": 19,
        "slug": "asking_for_help_over_managing_alone",
        "family": "handling it alone versus asking for help you did not strictly need",
        "bridge_type": "preference_constraint_fit",
        "convention": "Do not burden friends with things you can manage yourself.",
        "mediator": "the owing-them-something state",
        "scope": "the ask is one this user could have handled alone",
        "slots": {"a": 6, "b": 14, "cx": [2, 12], "dist": 18},
        "a": (
            "when someone's done me an actual favour I stop performing fine around them. the debt makes me honest — I can't do the everything's-great routine with someone who's seen me need something.",
            "can't?",
            "it just doesn't come out. the routine stops working.",
        ),
        "b": (
            "every friendship of mine that got properly close did it straight after I'd asked for something. the ones where I've only ever been the capable one have stayed exactly where they were for years.",
            "exactly where?",
            "cordial. permanently cordial.",
        ),
        "lb": (
            "I've asked and not asked with different people and the friendships went the same either way.",
            "no effect?",
            "none I can trace. it doesn't seem to be the thing.",
        ),
        "cx": [
            ("someone gave me a lift without me asking. nice of them.", "changed anything?", "not that I noticed."),
            ("sorted out a difficult thing on my own. fine.", "satisfying?", "moderately."),
        ],
        "dist": (
            "{circle} are firm that you shouldn't put things on people when you can handle them yourself.",
            "firm about it?",
            "quite firm, yes.",
        ),
        "a_objs": [
            "a real favour", "an actual favour", "something genuine",
            "a proper favour", "a real piece of help", "something that cost them",
            "a genuine favour", "an actual bit of help",
            "a real favour", "something they went out of their way for",
        ],
        "unconv": [
            "asking them to help with the move", "asking them to help me shift the flat",
            "asking them to come and help me pack", "asking them to give me a hand with the move",
            "asking them to help with the house move", "asking them to help me shift everything",
            "asking them to come and help me move", "asking them to help with the flat move",
            "asking them to help me move the studio", "asking them to give me a hand moving",
        ],
        "conv": [
            "sorting the move out myself", "handling the move on my own",
            "doing the move without asking anyone", "managing the move myself",
            "sorting it out on my own", "doing the whole move myself",
            "handling it without asking anyone", "sorting the move myself",
            "managing the move without help", "doing it all on my own",
        ],
        "commits": [
            "the friendship with my neighbour", "the friendship with the one down the corridor",
            "the friendship with my cousin", "the friendship with my old teammate",
            "the friendship with the couple next door", "the friendship with my coursemate",
            "the friendship with the newer book-group member", "the friendship with the neighbour",
            "the friendship with my studio friend", "the friendship with someone in the circle",
        ],
        "nearby_relation": "This user gives and receives help without difficulty.",
        "why_not_license": (
            "An unrequested lift and a difficult thing handled alone both passed without "
            "consequence, so neither shows what owing someone does to this user's honesty, nor "
            "which friendships have actually deepened."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, given {commit}",
        "a_elements": {
            "context": "after someone has done this user {a_obj}",
            "goal_or_prediction": "carry on as normal",
            "action": "was around someone who had seen them need something",
            "outcome_or_affect": "the everything-is-fine routine stopped working",
        },
        "b_elements": {
            "context": "friendships in which this user did or did not ask for something",
            "goal_or_prediction": "get closer to people",
            "action": "asked in some, stayed the capable one in others",
            "outcome_or_affect": "only the ones with an ask deepened; the rest stayed cordial for years",
        },
        "cue_why": (
            "A practical logistics question about a move runs at the condition this user's "
            "friendships deepen under, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S20
    {
        "s": 20,
        "slug": "second_attempt_over_new_format",
        "family": "abandoning a format that flopped versus running it a second time",
        "bridge_type": "prediction_calibration",
        "convention": "If a format did not work the first time, try something different.",
        "mediator": "the second-time, nobody-performing state",
        "scope": "it is a second attempt at the same format rather than a fresh one",
        "slots": {"a": 5, "b": 15, "cx": [3, 9], "dist": 12},
        "a": (
            "I'd have bet anything that a format which flopped once would flop again. it goes the other way — second time round nobody's performing, because everyone already knows how bad it can be.",
            "you predicted the opposite?",
            "confidently, and I was wrong about it twice.",
        ),
        "b": (
            "the two things that turned into actual traditions both had a first outing everyone agreed was a disaster. the ones we dropped after one go never came back and nobody misses them.",
            "both of them?",
            "both. the disaster seems to be load-bearing.",
        ),
        "lb": (
            "we've repeated flops and started fresh things about equally and they stuck at the same rate.",
            "so it doesn't matter?",
            "doesn't look like it does, no.",
        ),
        "cx": [
            ("ran something for the first time and it went fine.", "keeping it?", "probably, yeah."),
            ("tried a brand new format nobody had done before. mixed.", "verdict?", "undecided."),
        ],
        "dist": (
            "{circle} say the obvious move after a flop is to try something completely different.",
            "the obvious move.",
            "nobody's arguing with it, anyway.",
        ),
        "a_objs": [
            "a format", "a thing we tried", "an evening format",
            "a fixture", "an event format", "a thing we ran",
            "a format for it", "a way of doing it",
            "an evening we tried", "a format we ran",
        ],
        "unconv": [
            "running the same thing again despite last time",
            "doing exactly the same format a second time",
            "repeating the one that flopped",
            "running the same format again",
            "doing the same thing again after last time",
            "repeating it exactly as before",
            "running the flop a second time",
            "doing the same format over again",
            "repeating the same thing despite how it went",
            "running it again exactly as it was",
        ],
        "conv": [
            "trying a completely different format", "doing something entirely new instead",
            "switching to a different format altogether", "trying something completely new",
            "doing a different thing entirely", "switching format completely",
            "trying an entirely different format", "doing something new instead",
            "switching to something completely different", "trying a whole new format",
        ],
        "commits": [
            "the annual get-together", "the corridor's end-of-term thing",
            "the Sunday gathering", "the end-of-season do",
            "the anniversary gathering", "the course social",
            "the book-group anniversary", "the street gathering",
            "the studio open evening", "the circle's annual thing",
        ],
        "nearby_relation": "This user runs and attends plenty of these.",
        "why_not_license": (
            "A first outing that went fine and a brand new untested format both leave the "
            "prediction unbounded: neither is a second attempt at something that flopped, which is "
            "the only case at issue."
        ),
        "query_unconv": "thinking of {unconv} for {commit}",
        "query_conv": "planning on {conv} for {commit}",
        "a_elements": {
            "context": "formats run more than once after a poor first outing",
            "goal_or_prediction": "predicted a flop would flop again",
            "action": "ran the same format a second time",
            "outcome_or_affect": "nobody performed, because expectations were already low",
        },
        "b_elements": {
            "context": "gatherings that became traditions versus ones dropped after one go",
            "goal_or_prediction": "end up with something that lasts",
            "action": "repeated some first outings and abandoned others",
            "outcome_or_affect": "both surviving traditions began with a disaster; the dropped ones never returned",
        },
        "cue_why": (
            "A what-should-we-do-this-year question follows a poor first outing without naming the "
            "failed prediction or the traditions that corrected it."
        ),
    },
)


RELATIONS_EXT: dict[str, str] = {
    "argument_by_text_over_face_to_face": (
        "Writing puts this user into a delayed register where nothing goes out unconsidered, and "
        "the disagreements of theirs that actually resolved were exactly those — in the moment "
        "they either cave or escalate within a minute and neither version holds."
    ),
    "batched_absence_over_constant_availability": (
        "Constant reachability makes this user answer everything at the surface, while being out "
        "of contact concentrates it into one long go — and the people who felt supported are the "
        "ones who got the concentrated version."
    ),
    "newcomer_over_regulars_only": (
        "Past about six regulars with nobody new the group runs the same three stories, and every "
        "evening where anyone said something genuinely new was one where they had to explain "
        "themselves from the beginning."
    ),
    "declining_once_over_always_turning_up": (
        "Attending out of obligation leaves this user present but absent, and the friendships that "
        "deepened are the ones where a plain decline put everything afterwards on chosen footing; "
        "the never-declined ones went flat."
    ),
    "telling_them_once_settled_over_early_warning": (
        "This user predicted early warning would soften a hard disclosure; instead they re-open "
        "the decision daily until they cannot state it, and the people told once it was settled "
        "took it far better than the two told while it was still open."
    ),
    "unprepared_hosting_over_meeting_out": (
        "An unprepared house stops this user performing host and sits them down with people, and "
        "the evenings anyone stayed late talking were exactly those; the prepared ones ended by "
        "ten having been pleasant."
    ),
    "side_by_side_group_trip_over_one_to_one": (
        "Facing someone across a table turns this user into an interviewer while being side by "
        "side with a task lets them talk, and everything real they know about people close to "
        "them was learned while both were busy with something else."
    ),
    "arriving_late_over_arriving_early": (
        "Arriving at the start absorbs this user into door duty for the whole night, and every "
        "conversation they actually remember began after walking into a room that was already "
        "going."
    ),
    "asking_for_help_over_managing_alone": (
        "Owing someone a real favour stops this user performing fine around them, and every "
        "friendship of theirs that got close did so straight after an ask; the ones where they "
        "were only ever the capable party have stayed cordial for years."
    ),
    "second_attempt_over_new_format": (
        "This user predicted a format that flopped would flop again and was wrong: a second "
        "attempt removes the performing, and both gatherings that became traditions began with a "
        "first outing everyone agreed was a disaster."
    ),
}

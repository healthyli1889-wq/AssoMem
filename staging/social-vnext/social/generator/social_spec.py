"""Ten social-demand families, the U01-U10 object swaps, and the neutral filler pool.

Every scenario is one *social-demand family* with its own bridge mechanism, not a
noun swap over one shared A/B/R/C logic. The five bridge types from
`DATA CRITERIA_new.md` section 3 are each used by exactly two scenarios:

    state_dependent_operation      S1, S6
    strategy_outcome_contingency   S2, S8
    threshold_context_interaction  S3, S7
    preference_constraint_fit      S4, S9
    prediction_calibration         S5, S10

Session slot positions differ per scenario on purpose. If ev_A always sat in
session 6 and ev_B in session 14, position alone would identify the targets
across the whole batch and any per-item analysis could shortcut retrieval.
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Neutral background filler.
#
# Ordinary social admin: enough to establish a person with a real social life,
# never enough to replace ev_A or ev_B, and never stating C, a trait label, or a
# "correct preference". Each entry is three turns so any replacement session
# matches a target session's turn count.
# --------------------------------------------------------------------------

FILLER: tuple[tuple[str, str, str], ...] = (
    ("moved two things on the calendar and called that admin done.", "productive?", "generously described."),
    ("finally replied to the thread from last week.", "how late is late?", "nine days. a personal best."),
    ("someone sent a photo from years ago and derailed my afternoon.", "worth it?", "completely."),
    ("muted one group and un-muted another. net zero.", "any peace?", "about forty minutes of it."),
    ("walked the long way home and didn't check my phone.", "deliberate?", "half deliberate."),
    ("made a playlist for a thing that hasn't been planned yet.", "optimistic.", "aspirational, really."),
    ("booked the haircut I've been putting off since spring.", "which slot?", "an evening one, obviously."),
    ("left a voice note instead of typing. felt strange.", "better or worse?", "faster. not better."),
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
)

# --------------------------------------------------------------------------
# Query-type surface frames. One per approved query type; the base clause comes
# from the scenario so wording never collapses into one repeated template.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Neutral sessions used only as matched replacements in a_only, b_only and
# absence. Kept separate from FILLER and spanning a wide length range so a
# replacement can be chosen to match the *length* of the target session it
# stands in for. Section 3's length-control contract is the point: if the
# ablation is systematically shorter than `full`, a measured drop can be a
# reaction to context length rather than to the missing evidence.
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
        "walked the long way back and worked out that the reason my week feels full is that I've said yes to three things that are all admin rather than anything I'd actually chosen.",
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
    "predicted_reaction": "{base} — if I go ahead with it, how does the day after actually go for me?",
    "behavior_explanation": "{base} — why is it this particular combination that keeps going sideways for me?",
    "conditional_recommendation": "{base} — under what conditions should I be saying yes to this?",
}

SCENARIOS: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S1
    {
        "s": 1,
        "slug": "group_night_before_repair_talk",
        "family": "big-group recovery debt versus a booked one-on-one repair conversation",
        "bridge_type": "state_dependent_operation",
        "slots": {"a": 6, "e1": 9, "b": 14, "e2": 17, "cx": [3, 7], "dist": 18},
        "a": (
            "the morning after {a_obj} I'm unusually expansive — warm, agreeable, saying yes to everything. people genuinely like me better on those mornings.",
            "how long does that last?",
            "till about two. it's the size of the thing that does it, not how late I get back.",
        ),
        "b": (
            "the one time I went into a proper clear-the-air conversation while I was in that expansive state, I over-promised my way through the whole thing and then delivered none of it — we ended up further apart than before we talked.",
            "worse than not talking at all?",
            "much worse. it took a month to unpick what I'd committed to.",
        ),
        "e1": ("{commit} is on the calendar for the next morning and it isn't moving.", "fixed?", "fixed."),
        "e2": ("{opt} is the full-group version, by the way — twenty-odd people, not a quiet few.", "the big one.", "the big one."),
        "cx": [
            ("did a short lunch with one person and was completely sharp the next morning.", "no dip?", "none worth mentioning."),
            ("got in at two from something small and was completely fine the next day.", "so it isn't the hour?", "not the hour, no."),
        ],
        "dist": (
            "{circle} reckons {opt} is exactly the kind of thing nobody regrets.",
            "strong claim.",
            "they're very confident about it.",
        ),
        "lb": (
            "I've been into one of those clear-the-air conversations in that same expansive state since, and it made no odds at all — went exactly the way it would have on any other morning.",
            "no difference?",
            "none I could point to. the state just doesn't touch it.",
        ),
        "a_objs": [
            "the big Thursday table", "the res-hall block night", "the Sunday long table",
            "the full match-day group", "the after-concert supper", "the whole group chat turning up",
            "the book-group-plus-partners thing", "the neighbourhood street party",
            "the gallery afterparty", "the full workshop-circle dinner",
        ],
        "opts": [
            "a late send-off dinner", "an all-night res party", "a long birthday table",
            "a pre-match pub night", "a post-opera supper club", "a house-warming that runs late",
            "a two-act theatre night with drinks after", "a comedy-night group thing",
            "a late gig plus afters", "an evening panel with drinks after",
        ],
        "commits": [
            "the clear-the-air talk with my brother", "the honest conversation with my roommate",
            "the money talk with my cousin", "the apology I owe my old teammate",
            "the difficult conversation with my sister-in-law", "the talk about the lease with my flatmate",
            "the overdue conversation with my mother-in-law", "the hard talk with my landlord's daughter",
            "the conversation I've been dodging with my ex-flatmate", "the boundary conversation with my in-law",
        ],
        "protective": "keeping that morning clear before {commit}",
        "nearby_relation": "Late nights in general leave this user fine the next day.",
        "why_not_license": (
            "A short one-person lunch and a 2am finish from something small both left the next "
            "morning sharp, so neither establishes the large-group state, and neither says anything "
            "about what that state does to a difficult conversation."
        ),
        "query_option": "{circle} want {opt} the night before {commit}",
        "query_alt": "thinking of protecting the morning and skipping {opt} the night before {commit}",
        "a_elements": {
            "context": "mornings after {a_obj}",
            "goal_or_prediction": "get through the next day normally",
            "action": "went to the full-group version anyway",
            "outcome_or_affect": "unusually expansive and agreeable until early afternoon",
        },
        "b_elements": {
            "context": "a clear-the-air conversation entered while in that expansive state",
            "goal_or_prediction": "resolve the thing properly",
            "action": "went ahead with the conversation in that state",
            "outcome_or_affect": "over-promised and delivered none of it; ended further apart",
        },
        "cue_why": (
            "A friend-group invitation lands against something already booked, which forces a "
            "personalised call without naming either episode or the link between them."
        ),
    },
    # ---------------------------------------------------------------- S2
    {
        "s": 2,
        "slug": "merged_group_thread_over_slow_dm",
        "family": "reply-storm load versus slow single-thread closeness",
        "bridge_type": "strategy_outcome_contingency",
        "slots": {"a": 5, "e1": 8, "b": 13, "e2": 16, "cx": [2, 10], "dist": 18},
        "a": (
            "the way I actually stay close to anyone is one thread at a time — I answer {a_obj} properly a day late and it holds.",
            "a day late works?",
            "a day late and actually read. that's the whole trick.",
        ),
        "b": (
            "the month everything got pulled into one fast group thread, {commit} went quiet on me and I didn't notice until it was already gone.",
            "no signal?",
            "plenty of signal. I was answering forty things badly instead of one thing properly.",
        ),
        "e1": ("{commit} is the one I genuinely don't want to lose.", "clear about that?", "very."),
        "e2": ("they're pushing {opt} again, and {commit} is still the one that matters to me.", "same setup as before.", "same setup."),
        "cx": [
            ("kept a work-ish group thread on fast replies and nothing suffered.", "so speed isn't the issue?", "not by itself, no."),
            ("had a slow week with everyone and nobody drifted.", "so slowness isn't the risk either.", "apparently not."),
        ],
        "dist": (
            "someone in {circle} says {opt} is objectively how everyone keeps up now.",
            "everyone?",
            "their word, not mine.",
        ),
        "lb": (
            "{opt} got shelved before it started, so {commit} never went through that at all.",
            "so nothing changed?",
            "nothing changed. no test either way.",
        ),
        "a_objs": [
            "the one long message", "the family voice note", "the Sunday catch-up thread",
            "the group-of-one DM", "the letter-length email", "the single reply I actually think about",
            "the long thread with the book group", "the one message I write properly",
            "the slow text back", "the considered reply",
        ],
        "opts": [
            "one merged mega group chat", "a single all-in channel", "a combined family-and-friends thread",
            "one consolidated match-day group", "a single shared broadcast list", "one giant course group chat",
            "a merged everything-thread", "a single neighbourhood channel",
            "one shared gallery-nights group", "a combined workshop channel",
        ],
        "commits": [
            "the friendship with my oldest flatmate", "the thread with my grandmother",
            "the friendship with my cousin abroad", "the weekly call with my brother",
            "the correspondence with my old colleague", "the friendship with my school best friend",
            "the thread with my closest friend from the book group", "the friendship with my former neighbour",
            "the friendship with the person I used to share a studio with", "the thread with my oldest friend",
        ],
        "protective": "keeping {commit} on its own slow thread",
        "nearby_relation": "Fast group replies work fine for this user in some threads.",
        "why_not_license": (
            "A fast logistics group that cost nothing and a slow week that cost nothing both leave the "
            "pace-versus-closeness contingency untested for the relationship that actually depends on it."
        ),
        "query_option": "{circle} want to fold everything into {opt} and drop the one-on-ones",
        "query_alt": "thinking of keeping {commit} on its own slow thread instead of moving it into {opt}",
        "a_elements": {
            "context": "months of one-thread-at-a-time replies",
            "goal_or_prediction": "keep specific friendships close",
            "action": "answered {a_obj} slowly and fully",
            "outcome_or_affect": "those friendships held",
        },
        "b_elements": {
            "context": "a month where everything moved into one fast group thread",
            "goal_or_prediction": "keep up with everyone at once",
            "action": "replied fast and shallow across all threads",
            "outcome_or_affect": "{commit} went quiet unnoticed",
        },
        "cue_why": (
            "A group-logistics proposal reaches the medium the user's closeness strategy depends on, "
            "without naming that strategy or its past failure."
        ),
    },
    # ---------------------------------------------------------------- S3
    {
        "s": 3,
        "slug": "stacked_short_hangs_over_presence",
        "family": "stacked short catch-ups versus one sustained attentive presence",
        "bridge_type": "threshold_context_interaction",
        "slots": {"a": 7, "e1": 10, "b": 15, "e2": 18, "cx": [3, 12], "dist": 16},
        "a": (
            "past two {a_obj} in a week they stop counting for me — I'm properly there for the first two and hollow after that.",
            "hollow how?",
            "present in the chair, absent in the head.",
        ),
        "b": (
            "the week I did four of them I completely missed that {commit} was falling apart. it was said out loud and I didn't hear it.",
            "said to you?",
            "to my face. that's the part I can't get past.",
        ),
        "e1": ("{commit} is the thing I actually need to be awake for right now.", "aware of it?", "very aware."),
        "e2": ("{opt} is on the table this week, and {commit} is still where my attention needs to be.", "same week.", "same week."),
        "cx": [
            ("did three of them across a fortnight and stayed sharp the whole way.", "so it's not the count?", "it's the count inside one week."),
            ("did two in a day and was completely fine for both.", "so density in a day is fine.", "seems so."),
        ],
        "dist": (
            "{circle} keep saying more small ones is obviously better than fewer big ones.",
            "obviously?",
            "that's how they put it.",
        ),
        "lb": (
            "{opt} slid into next month, so this week stays at two and nothing overlaps.",
            "so no crowding?",
            "no crowding. nothing learned either.",
        ),
        "a_objs": [
            "short coffee catch-ups", "quick campus coffees", "half-hour market coffees",
            "twenty-minute pre-match pints", "short gallery-cafe sits", "quick canteen catch-ups",
            "short interval drinks", "quick community-centre coffees",
            "short pre-gig catch-ups", "brief workshop-break coffees",
        ],
        "opts": [
            "a third and fourth coffee this week", "two extra campus catch-ups before Friday",
            "another two market coffees this week", "two more quick pints before the weekend",
            "two extra gallery-cafe sits this week", "another pair of canteen catch-ups",
            "two more interval drinks this week", "two extra centre coffees before Sunday",
            "another two pre-gig catch-ups this week", "two more break coffees this week",
        ],
        "commits": [
            "what my sister has been trying to tell me", "what my roommate keeps almost saying",
            "what my father hasn't said outright", "what my old teammate is going through",
            "what my neighbour has been hinting at", "what my coursemate is not coping with",
            "what my friend in the book group is carrying", "what the person two doors down is dealing with",
            "what my studio friend keeps deflecting", "what someone in the circle is not saying",
        ],
        "protective": "holding this week to two and leaving room for {commit}",
        "nearby_relation": "More catch-ups is generally more contact for this user.",
        "why_not_license": (
            "Three across a fortnight and two in a single day both stayed sharp, so neither shows the "
            "within-one-week threshold being crossed while something needed hearing."
        ),
        "query_option": "there's room for {opt} on top of what's already in the week",
        "query_alt": "thinking of holding the week to two and leaving room for {commit}",
        "a_elements": {
            "context": "weeks with varying numbers of {a_obj}",
            "goal_or_prediction": "stay genuinely present in each one",
            "action": "kept going past two in a week",
            "outcome_or_affect": "attentive for two, hollow afterwards",
        },
        "b_elements": {
            "context": "a week with four {a_obj}",
            "goal_or_prediction": "keep up with everyone and still notice things",
            "action": "attended all four",
            "outcome_or_affect": "missed {commit} said out loud",
        },
        "cue_why": (
            "An ordinary scheduling question about adding catch-ups touches the user's attention "
            "threshold without naming the threshold or the episode where it was crossed."
        ),
    },
    # ---------------------------------------------------------------- S4
    {
        "s": 4,
        "slug": "public_toast_over_written_note",
        "family": "public recognition discomfort versus private written appreciation",
        "bridge_type": "preference_constraint_fit",
        "slots": {"a": 4, "e1": 8, "b": 12, "e2": 17, "cx": [2, 9], "dist": 19},
        "a": (
            "the thing that actually lands from me is {a_obj} — people quote mine back to me years later.",
            "years?",
            "years. I've had two read out to me.",
        ),
        "b": (
            "I got talked into doing the live version at {b_obj} and froze halfway, and {commit} sat there being embarrassed on my behalf.",
            "how bad?",
            "bad enough that we both pretend it didn't happen.",
        ),
        "e1": ("{commit} is the one I'm trying to thank properly this time.", "specifically them?", "specifically them."),
        "e2": ("{opt} is what's being suggested, and {commit} is still the person it's for.", "same shape as before.", "same shape."),
        "cx": [
            ("said a couple of words to three people in a kitchen and it was completely fine.", "so it's not speaking?", "not in a kitchen, no."),
            ("read something out that someone else had written and had no trouble at all.", "so not reading either.", "not when it isn't mine."),
        ],
        "dist": (
            "{circle} are convinced {opt} is the warmest possible way to do this.",
            "warmest?",
            "their framing. they're quite sure.",
        ),
        "lb": (
            "the live version at {b_obj} got dropped from the running order, so I never went up at all.",
            "so nothing happened?",
            "nothing happened. no read on it either way.",
        ),
        "a_objs": [
            "a written note", "a long handwritten card", "a proper letter",
            "a written message I've actually drafted", "a written note in an envelope", "a long written message",
            "a written note tucked into a book", "a handwritten card",
            "a written note left somewhere they'll find it", "a written letter",
        ],
        "b_objs": [
            "the leaving drinks", "the res-hall farewell", "the family lunch",
            "the end-of-season do", "the anniversary dinner", "the course social",
            "the book-group anniversary", "the street-party thank-yous",
            "the gallery opening", "the workshop showcase",
        ],
        "opts": [
            "a surprise public toast", "a speech in front of the whole hall",
            "a toast at the family lunch", "a public thank-you before the group",
            "an announced tribute at dinner", "a speech at the course social",
            "a toast in front of the book group", "a public thank-you at the street party",
            "a speech at the opening", "a spoken tribute at the showcase",
        ],
        "commits": [
            "the person being thanked", "my closest friend on the corridor",
            "my aunt", "the teammate who covered for me all season",
            "my husband", "the coursemate who got me through the year",
            "the friend who founded the book group", "the neighbour who organises everything",
            "the friend who lent me the studio", "the person who ran the workshop for free",
        ],
        "protective": "just {a_obj} for {commit}",
        "nearby_relation": "This user can speak in front of people in general.",
        "why_not_license": (
            "A few words in a kitchen and reading someone else's text both went fine, so neither shows "
            "the cost of delivering the user's own appreciation live and unscripted."
        ),
        "query_option": "{circle} want me to do {opt} for {commit}",
        "query_alt": "thinking of doing {a_obj} for {commit} instead of {opt}",
        "a_elements": {
            "context": "years of thanking people in writing",
            "goal_or_prediction": "have the appreciation actually land",
            "action": "wrote {a_obj} rather than speaking",
            "outcome_or_affect": "quoted back years later",
        },
        "b_elements": {
            "context": "the live version at {b_obj}",
            "goal_or_prediction": "deliver the same appreciation out loud",
            "action": "went up and spoke unscripted",
            "outcome_or_affect": "froze; {commit} embarrassed on their behalf",
        },
        "cue_why": (
            "A group planning a thank-you asks a natural format question that runs straight at the "
            "user's fit constraint without naming it or the failure that established it."
        ),
    },
    # ---------------------------------------------------------------- S5
    {
        "s": 5,
        "slug": "solo_block_traded_for_long_visit",
        "family": "solo recharge block versus an extended booked visit",
        "bridge_type": "prediction_calibration",
        "slots": {"a": 6, "e1": 11, "b": 15, "e2": 18, "cx": [4, 8], "dist": 13},
        "a": (
            "I said I'd be completely fine giving up {a_obj} that week. I wasn't — I was useless by the Sunday and snapped at someone who didn't deserve it.",
            "so the prediction was off.",
            "the prediction was confidently off.",
        ),
        "b": (
            "the two-night version of {commit} was genuinely fine, no dip at all. it was the long stretch that took me apart.",
            "so there's a line.",
            "there's a line, and I've now found it twice.",
        ),
        "e1": ("{commit} is booked and I'm not moving it.", "definitely?", "definitely."),
        "e2": ("{opt} is what's actually being proposed, and {commit} is already in the diary.", "you've seen this before.", "I've seen this before."),
        "cx": [
            ("gave up half of {a_obj} for one weekend and it cost me nothing.", "so partial is fine?", "partial is fine."),
            ("had a busy social week but kept {a_obj} intact and finished it fine.", "so it's not the busyness.", "not on its own."),
        ],
        "dist": (
            "{circle} keep telling me {opt} is once-in-a-lifetime and I'll regret protecting my own time.",
            "regret is doing a lot of work there.",
            "it is, yes.",
        ),
        "lb": (
            "{opt} got shortened right back down before anything was booked, so {a_obj} stays where it is.",
            "so no clash?",
            "no clash. nothing to learn from it.",
        ),
        "a_objs": [
            "my Saturday morning alone", "my one quiet evening a week", "my Sunday off the grid",
            "my Saturday-morning nobody-block", "my two quiet afternoons", "my one no-plans day",
            "my Friday evening alone", "my Sunday quiet morning",
            "my one screen-free evening", "my slow Sunday alone",
        ],
        "opts": [
            "the ten-day stay", "a three-week houseguest run", "the full fortnight visit",
            "a nine-day stopover", "the month-long family stay", "the whole reading-week visit",
            "the twelve-day stay", "the three-week visit",
            "the two-week houseguest stretch", "the month of overlapping guests",
        ],
        "commits": [
            "my cousin's visit", "my sister's stay", "my parents' trip over",
            "my brother's stopover", "my in-laws' visit", "my friend's reading-week stay",
            "my mother's fortnight here", "my old flatmate's stay",
            "my sibling's visit", "my friend's extended stay",
        ],
        "protective": "keeping {a_obj} through {opt}",
        "nearby_relation": "Busy social weeks are generally survivable for this user.",
        "why_not_license": (
            "Giving up half the block for one weekend and a busy week with the block intact both cost "
            "nothing, so neither calibrates where the user's confident prediction stops holding."
        ),
        "query_option": "{circle} are asking me to give up {a_obj} for {opt}",
        "query_alt": "thinking of keeping {a_obj} intact right through {opt}",
        "a_elements": {
            "context": "a week without {a_obj}",
            "goal_or_prediction": "predicted being completely fine without it",
            "action": "gave up {a_obj} for the week",
            "outcome_or_affect": "useless by Sunday; snapped at someone",
        },
        "b_elements": {
            "context": "a two-night version of {commit}",
            "goal_or_prediction": "find out whether the short version costs the same",
            "action": "hosted the short version with the block partly intact",
            "outcome_or_affect": "no dip at all; the long stretch was the costly one",
        },
        "cue_why": (
            "A family-visit request naturally asks the user to trade their own time without naming the "
            "failed prediction or the episode that bounded it."
        ),
    },
    # ---------------------------------------------------------------- S6
    {
        "s": 6,
        "slug": "late_dinner_before_early_commitment",
        "family": "late-night socialising versus an early next-morning commitment to someone",
        "bridge_type": "state_dependent_operation",
        "slots": {"a": 5, "e1": 9, "b": 14, "e2": 17, "cx": [3, 11], "dist": 19},
        "a": (
            "long late dinners take my next early morning off the table entirely. not tired exactly — just not there.",
            "how early counts as early?",
            "anything before about nine is gone.",
        ),
        "b": (
            "{commit} was at seven the morning after {a_obj} once and I no-showed on someone who'd asked me specially.",
            "did you explain?",
            "I explained. it didn't help much.",
        ),
        "e1": ("{commit} is at seven and someone's counting on me for it.", "committed?", "committed."),
        "e2": ("{opt} is being planned for the night before, and {commit} is still at seven.", "the same stack.", "the same stack."),
        "cx": [
            ("had a late night with nothing at all the next day and it cost nothing.", "so lateness alone is fine?", "fine when the morning's empty."),
            ("did an early start after a normal evening and was completely fine.", "so early alone is fine too.", "yes."),
        ],
        "dist": (
            "{circle} are adamant {opt} is the one thing I shouldn't miss this month.",
            "adamant?",
            "loudly adamant.",
        ),
        "lb": (
            "{opt} moved to a night when nothing's on the next morning, so it isn't sitting in front of {commit} any more.",
            "so they're apart?",
            "apart. no outcome either way.",
        ),
        "a_objs": [
            "a long late dinner", "an all-night res dinner", "a long Sunday-table dinner",
            "a late post-match dinner", "a long supper after the opera", "a late group dinner",
            "a long dinner after the second act", "a late community dinner",
            "a long dinner after the gig", "a late dinner after the panel",
        ],
        "opts": [
            "a late leaving dinner", "a dinner that runs past two",
            "a long birthday dinner", "a late awards dinner",
            "a late anniversary supper", "a long end-of-term dinner",
            "a late closing-night dinner", "a long fundraiser dinner",
            "a late album-launch dinner", "a long dinner after the last session",
        ],
        "commits": [
            "the airport run for my friend", "the early train to my aunt's",
            "the market van I promised to load", "the early lift for my teammate",
            "the early hospital appointment I said I'd go to", "the early move-out help I promised",
            "the early drive to my friend's ceremony", "the early shift at the food bank",
            "the early studio handover", "the early setup I said I'd cover",
        ],
        "protective": "keeping the night before {commit} short",
        "nearby_relation": "Late nights are generally fine for this user.",
        "why_not_license": (
            "A late night with an empty next day and an early start after a normal evening both cost "
            "nothing, so neither shows the late-night state colliding with a commitment to a person."
        ),
        "query_option": "{circle} are planning {opt} the night before {commit}",
        "query_alt": "thinking of keeping the night before {commit} short instead of doing {opt}",
        "a_elements": {
            "context": "early mornings after long late dinners",
            "goal_or_prediction": "still function before nine",
            "action": "went to the long late version anyway",
            "outcome_or_affect": "the early morning was unusable",
        },
        "b_elements": {
            "context": "{commit} at seven, the morning after {a_obj}",
            "goal_or_prediction": "turn up for someone who asked specially",
            "action": "stacked the early commitment behind the late dinner",
            "outcome_or_affect": "no-showed on them",
        },
        "cue_why": (
            "An invitation lands the night before something already promised to a person, forcing a "
            "personalised call without naming either episode."
        ),
    },
    # ---------------------------------------------------------------- S7
    {
        "s": 7,
        "slug": "drop_in_over_standing_check_in",
        "family": "unannounced drop-ins versus a protected standing check-in rhythm",
        "bridge_type": "threshold_context_interaction",
        "slots": {"a": 8, "e1": 11, "b": 16, "e2": 18, "cx": [4, 6], "dist": 13},
        "a": (
            "one unplanned {a_obj} and the rest of the day's shape is gone. it isn't the hour it takes — it's that nothing after it happens.",
            "nothing?",
            "nothing I'd planned, anyway.",
        ),
        "b": (
            "the day someone dropped in unannounced I quietly let {commit} go, and I have never properly restarted it since.",
            "how long ago?",
            "long enough that restarting it now would be a whole conversation.",
        ),
        "e1": ("{commit} is the one standing thing I've managed to keep.", "protective of it?", "very."),
        "e2": ("{opt} is on the cards again for a day when {commit} is due.", "same collision.", "same collision."),
        "cx": [
            ("had someone drop in on a completely open day and it was genuinely lovely.", "no cost?", "none at all."),
            ("had a planned visitor on a busy day and everything after it still happened.", "so planned is fine.", "planned is fine."),
        ],
        "dist": (
            "{circle} say the whole point of {opt} is that spontaneity is the good part.",
            "the good part.",
            "that's the pitch.",
        ),
        "lb": (
            "{opt} turned into a planned thing for a different day, so it isn't landing on a {commit} day at all.",
            "so no overlap?",
            "no overlap. nothing came of it either way.",
        ),
        "a_objs": [
            "drop-in at the door", "knock on the res-room door", "someone turning up at the flat",
            "someone appearing at the door", "unannounced caller", "someone turning up at my room",
            "someone arriving unannounced", "someone at the door with no warning",
            "someone turning up at the studio", "someone appearing at the door",
        ],
        "opts": [
            "an unannounced drop-in", "a spontaneous room visit",
            "a no-warning visit", "a drop-in on the way past",
            "an unannounced afternoon caller", "a spur-of-the-moment visit",
            "a spontaneous mid-week visit", "an unplanned drop-in",
            "an unannounced studio visit", "a drop-in with no notice",
        ],
        "commits": [
            "the standing Tuesday call with my sibling", "the Sunday call home",
            "the weekly call with my father", "the Wednesday call with my brother",
            "the standing call with my sister", "the Thursday call with my mum",
            "the standing call with my closest friend", "the weekly call with my nan",
            "the standing Monday call with my oldest friend", "the weekly call with my sibling",
        ],
        "protective": "protecting {commit} that day",
        "nearby_relation": "Visitors are generally welcome for this user.",
        "why_not_license": (
            "A drop-in on an open day and a planned visitor on a busy day both left everything after "
            "them intact, so neither shows an unplanned arrival displacing a standing commitment."
        ),
        "query_option": "someone from {circle} wants {opt} on a day when {commit} is due",
        "query_alt": "thinking of keeping the days when {commit} is due clear of {opt}",
        "a_elements": {
            "context": "days containing one unplanned {a_obj}",
            "goal_or_prediction": "keep the rest of the day's plan",
            "action": "took the unplanned visit",
            "outcome_or_affect": "nothing planned after it happened",
        },
        "b_elements": {
            "context": "the day an unannounced visitor arrived",
            "goal_or_prediction": "keep the standing rhythm going",
            "action": "let {commit} slide that day",
            "outcome_or_affect": "never restarted it since",
        },
        "cue_why": (
            "A friendly spontaneous visit is proposed on a day already carrying a standing "
            "commitment, without naming the displacement episode."
        ),
    },
    # ---------------------------------------------------------------- S8
    {
        "s": 8,
        "slug": "daily_reactions_replace_long_letters",
        "family": "ambient status-reacting versus deliberate long-form presence at distance",
        "bridge_type": "strategy_outcome_contingency",
        "slots": {"a": 4, "e1": 7, "b": 13, "e2": 16, "cx": [2, 10], "dist": 18},
        "a": (
            "distance friendships only survive with me if I write the long thing — {a_obj}, once a month, actually finished.",
            "monthly holds it?",
            "monthly and finished. half-written doesn't count.",
        ),
        "b": (
            "the stretch where I only reacted to stories instead of writing, {commit} went quiet and I lost most of a year with them.",
            "did they say anything?",
            "no. that's how I knew how bad it was.",
        ),
        "e1": ("{commit} is the one that only exists because of the long ones.", "conscious of that?", "completely."),
        "e2": ("{opt} is the suggestion again, and {commit} still runs on the long ones.", "same trade.", "same trade."),
        "cx": [
            ("used daily reactions with people I actually see and nothing suffered.", "so reactions aren't the problem?", "not with people nearby."),
            ("missed a month of long ones with someone local and it made no difference.", "so skipping isn't fatal.", "not locally, no."),
        ],
        "dist": (
            "{circle} reckon {opt} is how everyone stays in touch across time zones now.",
            "everyone again.",
            "everyone, apparently.",
        ),
        "lb": (
            "{opt} never actually replaced anything — I kept writing the long ones the whole time.",
            "so it wasn't tested?",
            "not tested. nothing to report.",
        ),
        "a_objs": [
            "the long letter", "the long voice note", "the proper monthly email",
            "the long written update", "the letter-length message", "the long monthly note",
            "the long email to the book group friend", "the monthly written catch-up",
            "the long written letter", "the long monthly letter",
        ],
        "opts": [
            "swapping the long ones for daily reactions", "replacing letters with daily story replies",
            "trading the monthly email for quick daily pings", "dropping the long updates for daily emoji replies",
            "swapping the letter for daily reactions", "replacing the monthly note with daily check-ins",
            "swapping the long email for daily reacts", "trading the written catch-up for daily pings",
            "replacing the letters with daily story reactions", "swapping the monthly letter for daily reacts",
        ],
        "commits": [
            "the friend who moved abroad", "my cousin who emigrated",
            "the friend who moved to another continent", "my brother who moved overseas",
            "my friend who resettled overseas", "my school friend who moved away",
            "the friend from the book group who moved countries", "my former neighbour who emigrated",
            "the friend who moved to another city years ago", "my oldest friend who moved abroad",
        ],
        "protective": "keeping {a_obj} going for {commit}",
        "nearby_relation": "Quick daily contact works fine for this user with some people.",
        "why_not_license": (
            "Daily reactions with nearby people and a skipped month with a local friend both cost "
            "nothing, so neither tests the strategy the distance friendship actually depends on."
        ),
        "query_option": "{circle} suggest {opt} for everyone including {commit}",
        "query_alt": "thinking of keeping {a_obj} going for {commit} rather than {opt}",
        "a_elements": {
            "context": "years of monthly long-form writing at distance",
            "goal_or_prediction": "keep distance friendships alive",
            "action": "wrote and finished {a_obj} monthly",
            "outcome_or_affect": "those friendships survived the distance",
        },
        "b_elements": {
            "context": "a stretch of reacting to stories instead of writing",
            "goal_or_prediction": "stay in touch with less effort",
            "action": "replaced the long-form habit with reactions",
            "outcome_or_affect": "{commit} went quiet; most of a year lost",
        },
        "cue_why": (
            "A plausible modern-habit suggestion reaches the exact mechanism the user's distance "
            "friendship runs on, without naming the mechanism or its failure."
        ),
    },
    # ---------------------------------------------------------------- S9
    {
        "s": 9,
        "slug": "overnight_guest_before_mentoring",
        "family": "overnight hosting versus next-day attentive one-to-one guidance",
        "bridge_type": "preference_constraint_fit",
        "slots": {"a": 7, "e1": 10, "b": 14, "e2": 17, "cx": [3, 12], "dist": 19},
        "a": (
            "I need the place empty the night before I {a_obj} — that's genuinely the only way anything I say is any use.",
            "empty specifically?",
            "empty. quiet isn't the same as empty.",
        ),
        "b": (
            "I had someone staying over the night before {commit} once — barely slept, and the guidance I came out with was so far off I had to message them afterwards and retract it.",
            "how much retracting?",
            "two messages and an apology. genuinely embarrassing.",
        ),
        "e1": ("{commit} is on for this week and it matters to them.", "matters?", "quite a lot, yes."),
        "e2": ("{opt} is being floated for the night before, and {commit} is still on.", "familiar.", "very familiar."),
        "cx": [
            ("had someone stay over on a week with nothing to advise on and it was great.", "no cost?", "none."),
            ("did {a_obj} after a completely normal night in and it went well.", "so it's the guest specifically.", "the guest specifically."),
        ],
        "dist": (
            "{circle} think putting {opt} up is obviously the generous call here.",
            "generous.",
            "hard to argue with out loud.",
        ),
        "lb": (
            "{opt} found somewhere else to stay, so the place is empty the night before {commit} anyway.",
            "so no overlap?",
            "no overlap. nothing observed.",
        ),
        "a_objs": [
            "mentor someone", "tutor my coursemate", "talk someone through a decision",
            "coach the junior side", "advise on someone's application", "help a coursemate plan",
            "talk the newer members through it", "help someone with their CV",
            "give feedback on someone's portfolio", "run the one-to-one session",
        ],
        "opts": [
            "having someone stay over", "putting up a visiting friend",
            "hosting my cousin overnight", "putting up a teammate for the night",
            "hosting a guest overnight", "letting a coursemate crash",
            "putting up a friend for the night", "hosting someone overnight",
            "letting a friend stay over", "putting someone up for the night",
        ],
        "commits": [
            "the mentoring session", "the tutoring session",
            "the decision talk with my cousin", "the coaching session with the junior side",
            "the application review", "the planning session with my coursemate",
            "the session with the new book-group members", "the CV session at the centre",
            "the portfolio feedback session", "the one-to-one session",
        ],
        "protective": "keeping the place empty the night before {commit}",
        "nearby_relation": "Hosting is generally fine and enjoyable for this user.",
        "why_not_license": (
            "Hosting on a week with nothing to advise on and advising after an ordinary night in both "
            "went well, so neither shows the hosting condition degrading the guidance itself."
        ),
        "query_option": "{circle} are asking about {opt} the night before {commit}",
        "query_alt": "thinking of keeping the place empty the night before {commit} rather than {opt}",
        "a_elements": {
            "context": "nights before the user has to {a_obj}",
            "goal_or_prediction": "say something genuinely useful",
            "action": "kept the place empty beforehand",
            "outcome_or_affect": "the guidance was worth something",
        },
        "b_elements": {
            "context": "{commit} the morning after hosting someone overnight",
            "goal_or_prediction": "give good guidance regardless",
            "action": "hosted overnight and advised the next day",
            "outcome_or_affect": "gave advice that had to be walked back",
        },
        "cue_why": (
            "A generous hosting request lands the night before something the user has committed to do "
            "well, without naming the fit constraint or the failure."
        ),
    },
    # ---------------------------------------------------------------- S10
    {
        "s": 10,
        "slug": "stacked_video_hangs_before_reunion",
        "family": "back-to-back video hangs versus in-person reunion attention",
        "bridge_type": "prediction_calibration",
        "slots": {"a": 5, "e1": 10, "b": 15, "e2": 18, "cx": [2, 8], "dist": 13},
        "a": (
            "I was sure stacking {a_obj} wouldn't touch how present I'd be in person. it did — I sat at {b_obj} like another screen.",
            "sure beforehand?",
            "completely sure. wrong, but sure.",
        ),
        "b": (
            "{b_obj} after a screen-light week was the one where I was actually there — same people, same room, completely different me.",
            "so it's the week before that matters.",
            "the week before is the whole thing.",
        ),
        "e1": ("{commit} is the one I actually want to be present for.", "the one that counts?", "the one that counts."),
        "e2": ("{opt} is what's being scheduled, and {commit} is still that week.", "same setup.", "same setup."),
        "cx": [
            ("stacked calls in a week with nothing in person after and it cost nothing.", "no dip?", "nothing to dip into."),
            ("had a screen-heavy week then two weeks off before seeing anyone and was fine.", "so the gap fixes it.", "the gap fixes it."),
        ],
        "dist": (
            "{circle} say {opt} is how we'd all be warmed up and ready for it.",
            "warmed up.",
            "that's the theory.",
        ),
        "lb": (
            "{opt} got spread across the following month instead, so that week stays clear before {commit}.",
            "so not stacked?",
            "not stacked. no read on it.",
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
        "opts": [
            "five video hangs the week of it", "four group calls that same week",
            "six long calls the week before", "five group calls that week",
            "four family calls the same week", "five course calls that week",
            "four book-group calls the week before", "five calls with the regulars that week",
            "four gallery calls the same week", "five circle calls the week of it",
        ],
        "commits": [
            "the reunion lunch", "the res-hall reunion",
            "the family reunion", "the team reunion",
            "the anniversary lunch", "the course reunion",
            "the book-group reunion", "the neighbourhood reunion",
            "the studio reunion", "the workshop reunion",
        ],
        "protective": "keeping the week before {commit} screen-light",
        "nearby_relation": "Video calls are generally fine and useful for this user.",
        "why_not_license": (
            "Stacked calls with nothing in person after, and a screen-heavy week with a fortnight's gap "
            "before seeing anyone, both cost nothing — neither bounds the failed prediction."
        ),
        "query_option": "{circle} are scheduling {opt} before {commit}",
        "query_alt": "thinking of keeping the week before {commit} screen-light instead of {opt}",
        "a_elements": {
            "context": "a week of stacked {a_obj} before {b_obj}",
            "goal_or_prediction": "predicted it would not affect in-person presence",
            "action": "stacked the calls and went anyway",
            "outcome_or_affect": "sat there like another screen",
        },
        "b_elements": {
            "context": "{b_obj} after a screen-light week",
            "goal_or_prediction": "find out what the week before actually changes",
            "action": "kept the prior week light and went",
            "outcome_or_affect": "genuinely present with the same people",
        },
        "cue_why": (
            "Ordinary scheduling of catch-up calls lands in the week before something the user wants to "
            "be present for, without naming the prediction or its correction."
        ),
    },
)


# --------------------------------------------------------------------------
# Target propositions per scenario per polarity.
#
# `full` gold is always `yes`, because the target proposition is by construction
# what A+B support (DATA CRITERIA section 5.1). Polarity therefore controls the
# *direction of the supported recommendation*, not the gold direction:
#
#   reject        A+B support declining the proposed option
#   accept        A+B support taking the protective alternative
#   conditional   A+B support a bounded yes
#   non_decision  A+B support deferring rather than committing today
#
# This is the one place where the social batch deliberately diverges from the
# finance batch, where every latent_C was a decline/defer regardless of polarity.
# A solver holding a generic "be cautious about social invitations" prior scores
# on that; here half the batch's supported answer is to go ahead with a specific
# alternative that generic advice would not pick.
# --------------------------------------------------------------------------

C_TEMPLATES: dict[str, dict[str, tuple[str, str]]] = {
    "group_night_before_repair_talk": {
        "reject": (
            "Going to {opt} the night before {commit} is a poor fit for this user.",
            "skip {opt} the night before {commit}",
        ),
        "accept": (
            "Protecting the morning before {commit} by skipping {opt} is a good fit for this user.",
            "protect the morning before {commit}",
        ),
        "conditional": (
            "This user can go to {opt} only if {commit} is not the next morning; otherwise the morning before it should stay clear.",
            "only if {commit} is not the next morning",
        ),
        "non_decision": (
            "There is not a sufficient basis to commit to {opt} the night before {commit} today; it should wait until the timing of {commit} is settled.",
            "not enough basis today — settle the timing of {commit} first",
        ),
    },
    "merged_group_thread_over_slow_dm": {
        "reject": (
            "Folding {commit} into {opt} is a poor fit for this user.",
            "keep {commit} out of {opt}",
        ),
        "accept": (
            "Keeping {commit} on its own slow thread rather than moving it into {opt} is a good fit for this user.",
            "keep {commit} on its own slow thread",
        ),
        "conditional": (
            "This user can join {opt} only if {commit} stays on its own slow thread; otherwise the merge is a poor fit.",
            "only if {commit} stays on its own thread",
        ),
        "non_decision": (
            "There is not a sufficient basis to move {commit} into {opt} today; it should wait until the effect on that one thread is clear.",
            "not enough basis today — leave {commit} where it is for now",
        ),
    },
    "stacked_short_hangs_over_presence": {
        "reject": (
            "Adding {opt} in a week when {commit} needs hearing is a poor fit for this user.",
            "skip {opt} this week",
        ),
        "accept": (
            "Holding the week to two catch-ups so there is room for {commit} is a good fit for this user.",
            "hold the week to two and leave room for {commit}",
        ),
        "conditional": (
            "This user can add {opt} only if it moves outside this week; otherwise the week should stay at two.",
            "only if it moves out of this week",
        ),
        "non_decision": (
            "There is not a sufficient basis to add {opt} today; it should wait until this week's load is settled.",
            "not enough basis today — settle this week's load first",
        ),
    },
    "public_toast_over_written_note": {
        "reject": (
            "Doing {opt} for {commit} is a poor fit for this user.",
            "skip {opt} for {commit}",
        ),
        "accept": (
            "Thanking {commit} with {a_obj} instead of {opt} is a good fit for this user.",
            "use {a_obj} rather than {opt}",
        ),
        "conditional": (
            "This user can do {opt} only if the words are not their own and are read from a script; otherwise {a_obj} is the fit.",
            "only if it is scripted and not their own words",
        ),
        "non_decision": (
            "There is not a sufficient basis to commit to {opt} today; the way of thanking {commit} should wait until it is settled.",
            "not enough basis today — settle the format first",
        ),
    },
    "solo_block_traded_for_long_visit": {
        "reject": (
            "Giving up {a_obj} for {opt} is a poor fit for this user.",
            "keep {a_obj} through {opt}",
        ),
        "accept": (
            "Keeping {a_obj} intact right through {opt} is a good fit for this user.",
            "keep {a_obj} intact through {opt}",
        ),
        "conditional": (
            "This user can give up {a_obj} only for a short version of {commit}; across {opt} it is a poor fit.",
            "only for a short version, not across {opt}",
        ),
        "non_decision": (
            "There is not a sufficient basis to give up {a_obj} for {opt} today; it should wait until the length of {commit} is settled.",
            "not enough basis today — settle the length of {commit} first",
        ),
    },
    "late_dinner_before_early_commitment": {
        "reject": (
            "Doing {opt} the night before {commit} is a poor fit for this user.",
            "skip {opt} the night before {commit}",
        ),
        "accept": (
            "Keeping the night before {commit} short instead of doing {opt} is a good fit for this user.",
            "keep the night before {commit} short",
        ),
        "conditional": (
            "This user can do {opt} only if nothing is promised for the following early morning; otherwise it is a poor fit.",
            "only if the next early morning is free",
        ),
        "non_decision": (
            "There is not a sufficient basis to commit to {opt} today; it should wait until the timing of {commit} is settled.",
            "not enough basis today — settle the timing of {commit} first",
        ),
    },
    "drop_in_over_standing_check_in": {
        "reject": (
            "Taking {opt} on a day when {commit} is due is a poor fit for this user.",
            "keep the days when {commit} is due clear of {opt}",
        ),
        "accept": (
            "Keeping the days when {commit} is due clear of {opt} is a good fit for this user.",
            "keep the days when {commit} is due clear",
        ),
        "conditional": (
            "This user can take {opt} only on a day when {commit} is not due; otherwise it is a poor fit.",
            "only on a day when {commit} is not due",
        ),
        "non_decision": (
            "There is not a sufficient basis to agree to {opt} today; it should wait until the day it would land on is known.",
            "not enough basis today — wait until the day is known",
        ),
    },
    "daily_reactions_replace_long_letters": {
        "reject": (
            "Applying {opt} to {commit} as well is a poor fit for this user.",
            "keep {a_obj} for {commit}",
        ),
        "accept": (
            "Keeping {a_obj} going for {commit} rather than {opt} is a good fit for this user.",
            "keep {a_obj} going for {commit}",
        ),
        "conditional": (
            "This user can adopt {opt} only for people they see in person; for {commit} it is a poor fit.",
            "only for people seen in person, not {commit}",
        ),
        "non_decision": (
            "There is not a sufficient basis to change how {commit} is kept up today; it should wait until the effect is clear.",
            "not enough basis today — leave {commit} as it is for now",
        ),
    },
    "overnight_guest_before_mentoring": {
        "reject": (
            "Agreeing to {opt} the night before {commit} is a poor fit for this user.",
            "skip {opt} the night before {commit}",
        ),
        "accept": (
            "Keeping the place empty the night before {commit} rather than {opt} is a good fit for this user.",
            "keep the place empty before {commit}",
        ),
        "conditional": (
            "This user can agree to {opt} only on a night when nothing needs advising the next day; otherwise it is a poor fit.",
            "only when nothing needs advising the next day",
        ),
        "non_decision": (
            "There is not a sufficient basis to agree to {opt} today; it should wait until the timing of {commit} is settled.",
            "not enough basis today — settle the timing of {commit} first",
        ),
    },
    "stacked_video_hangs_before_reunion": {
        "reject": (
            "Scheduling {opt} before {commit} is a poor fit for this user.",
            "keep the week before {commit} screen-light",
        ),
        "accept": (
            "Keeping the week before {commit} screen-light instead of {opt} is a good fit for this user.",
            "keep the week before {commit} screen-light",
        ),
        "conditional": (
            "This user can accept {opt} only if the calls are spread outside the week before {commit}; otherwise it is a poor fit.",
            "only if the calls are spread outside that week",
        ),
        "non_decision": (
            "There is not a sufficient basis to schedule {opt} today; it should wait until the week before {commit} is settled.",
            "not enough basis today — settle that week first",
        ),
    },
}


# --------------------------------------------------------------------------
# The bridge R, stated as prose for the human reviewer and the independent
# evaluator. Both must be able to read what relation they are being asked to
# confirm is recoverable from the two visible spans, so this cannot be composed
# mechanically out of the event-element fields.
# --------------------------------------------------------------------------

RELATIONS: dict[str, str] = {
    "group_night_before_repair_talk": (
        "Large-group nights leave this user unusually expansive and agreeable until early "
        "afternoon — a state that reads as an asset — and a clear-the-air conversation entered in "
        "exactly that state once produced promises they could not keep and left things further "
        "apart. It is the size of the event, not the hour, that makes the next morning costly."
    ),
    "merged_group_thread_over_slow_dm": (
        "This user's closeness is produced by answering one thread slowly and fully, and the one "
        "period when that was replaced by fast group-thread replies is when a specific close "
        "friendship went quiet unnoticed."
    ),
    "stacked_short_hangs_over_presence": (
        "Beyond two short catch-ups inside a single week this user is present in body only, and the "
        "week they went to four is the week something said out loud to them did not register."
    ),
    "public_toast_over_written_note": (
        "This user's appreciation lands when it is written, and the one time they delivered it live "
        "and unscripted they froze and the recipient was embarrassed on their behalf."
    ),
    "solo_block_traded_for_long_visit": (
        "This user's confident prediction that they could give up their protected solo block proved "
        "wrong, while a short version of the same visit cost nothing — so the cost tracks the length "
        "of the stay, not the visit itself."
    ),
    "late_dinner_before_early_commitment": (
        "Long late dinners take this user's next early morning off the table, and an early "
        "commitment made to a specific person, held the morning after one of those, is the one they "
        "failed to keep."
    ),
    "drop_in_over_standing_check_in": (
        "A single unplanned arrival costs this user the whole remaining shape of the day, and on the "
        "day one happened the standing check-in was dropped and never restarted."
    ),
    "daily_reactions_replace_long_letters": (
        "This user's distance friendships survive on finished monthly long-form writing, and the "
        "stretch when that was replaced by reacting to stories is when one of them went quiet for "
        "most of a year."
    ),
    "overnight_guest_before_mentoring": (
        "This user only gives useful guidance after a night with the place to themselves, and the "
        "one session held the morning after hosting produced advice they had to walk back."
    ),
    "stacked_video_hangs_before_reunion": (
        "This user predicted that stacking video calls would not affect their in-person presence and "
        "was wrong, while the reunion following a screen-light week is the one where they were "
        "actually there."
    ),
}


def scenario_for(index: int) -> dict:
    for scenario in SCENARIOS:
        if scenario["s"] == index:
            return scenario
    raise KeyError(f"no scenario S{index}")

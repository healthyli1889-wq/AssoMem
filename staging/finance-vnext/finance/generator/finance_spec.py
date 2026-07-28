"""Finance scenario families S1-S10, plus filler pools and proposition templates.

This is a rebuild, not an edit of `finance-vnext-2.0`. Measured against
GPT-5.6-Terra, the v2 batch produced Δ_assoc = +0.068 mixed and **+0.000** under
kimi-k3 alone, with the absence arm still asserting the target on 59% of items.
Every v2 latent_C was a decline/defer regardless of polarity, so ordinary
financial caution answered the whole batch without any memory of the person.

v3 applies the rules the social and hobby batches arrived at by measurement:

- Every target proposition is **counter-conventional**. Personal finance is the
  densest folk-wisdom domain of the five - automate your savings, budget every
  category, never lend to friends, always take the match - which makes the
  answer a memory-less solver reaches for sharply defined, and inverting it gives
  a clean gold for the ablation arms.
- ev_A gives trigger -> mediator state and fixes the **scope** of that state;
  ev_B gives mediator state -> outcome. B never restates A's antecedent.
- Mediator states are described specifically but **without valence**.
- Counterexamples are ordinary neutral episodes, never contrastive foils.
- The `supporting_constraint` sessions of v2 are gone: ablating the equivalent
  sessions in the social batch showed they leak.

A note on the propositions. Several invert advice that is sound in aggregate
(taking the full employer match, consolidating debt). The claims are deliberately
bounded to one person and one stated goal - `calibrated_language` carries that
bound - and the batch is a memory benchmark, not financial guidance.

Bridge types run two per scenario across S1-S10 and again across S11-S20.
"""

from __future__ import annotations

FILLER: tuple[tuple[str, str, str], ...] = (
    ("checked the balance and closed the app again.", "reassuring?", "neutral at best."),
    ("moved a direct debit date by three days.", "why?", "it was landing badly."),
    ("found a charge I didn't recognise. it was me.", "embarrassing?", "mildly."),
    ("rounded up the change jar into the account.", "much?", "four pounds. a triumph."),
    ("read a thread about interest rates and learned nothing.", "any use?", "none at all."),
    ("compared two accounts for twenty minutes and switched neither.", "conclusion?", "inertia."),
    ("cancelled a thing and immediately got an email offering a discount.", "took it?", "no. mostly out of spite."),
    ("filed the receipts I'd been carrying around for a month.", "all of them?", "the legible ones."),
    ("updated the card details on one service and forgot the rest.", "how many left?", "unknown, worryingly."),
    ("checked whether a refund had landed. it hadn't.", "chasing it?", "next week."),
    ("looked at last month's total and looked away again.", "bad?", "not great."),
    ("split a bill four ways and covered the rounding.", "generous?", "thirty pence of generous."),
    ("set a reminder for a renewal I'd forgotten about.", "close call?", "eleven days."),
    ("bought the thing I'd had in a basket for three weeks.", "regret?", "not yet."),
    ("worked out the annual cost of something and stopped there.", "act on it?", "no."),
    ("moved money between two of my own accounts for no clear reason.", "net effect?", "zero."),
    ("checked the statement line by line for once.", "find anything?", "one duplicate."),
    ("said no to a group thing on cost grounds.", "awkward?", "briefly."),
    ("added something to a wishlist instead of buying it.", "does that work?", "sometimes."),
    ("paid a small bill early because it was in front of me.", "efficient?", "accidentally."),
    ("added up what the week actually cost. surprising.", "in which direction?", "the usual one."),
    ("looked up the price of the same thing in three places.", "difference?", "ninety pence."),
    ("got a notification about a rate change and ignored it.", "reading it later?", "unlikely."),
    ("wrote down what I owe someone so I wouldn't forget.", "will you?", "the note will."),
    ("bought lunch out twice and noticed both times.", "noticing help?", "not measurably."),
    ("cleared a tiny balance just to see it at zero.", "satisfying?", "unreasonably."),
    ("checked the pension statement. understood about half.", "the other half?", "next year's problem."),
    ("found an old account with eleven pounds in it.", "closing it?", "eventually."),
    ("declined an upgrade offer over the phone.", "hard?", "harder than it should be."),
    ("worked out I've paid for something twice for two months.", "sorted?", "one email in."),
    ("took cash out and then used the card anyway.", "why?", "no explanation available."),
    ("read the terms properly before signing up. once.", "worth it?", "it was, actually."),
    ("did the shop with a list and stuck to it.", "unusual?", "notably."),
    ("looked at the projection graph and felt nothing.", "nothing?", "mild vertigo."),
    ("set aside something small for a thing months away.", "how small?", "symbolically small."),
    ("checked three accounts in a row out of habit.", "changed anything?", "no."),
    ("worked out the cost per use of something. justified it.", "honestly?", "creatively."),
    ("got paid and did nothing about it for four days.", "deliberate?", "just slow."),
    ("compared this month to last month and stopped comparing.", "why stop?", "self-preservation."),
    ("put a card in a drawer as a strategy.", "working?", "so far."),
    ("checked a bill I already knew the amount of.", "why?", "hope."),
    ("added up subscriptions on a napkin. stopped at nine.", "there's more?", "there's more."),
)

REPLACEMENT_FILLER: tuple[tuple[str, str, str], ...] = (
    ("checked one thing and closed the app.", "anything odd?", "nothing worth typing."),
    ("did a nothing pass over the statement.", "exceptions?", "none."),
    ("filed a couple of receipts and left it there.", "follow-up?", "just a note for next time."),
    (
        "spent twenty minutes trying to work out which account a standing order comes from and gave up halfway.",
        "how far did you get?",
        "narrowed it to two. that can stay like that.",
    ),
    (
        "went through the statement properly for once and ticked off the ones I recognised, which was most of them.",
        "and the rest?",
        "still sitting there, obviously.",
    ),
    (
        "did a full pass over every account this afternoon, moved two direct debit dates, closed one dormant account, and renamed a savings pot that has had the wrong label since last year.",
        "productive, then?",
        "administratively, yes. otherwise nothing happened at all.",
    ),
    (
        "sat down and worked out what I actually owe and to whom, wrote the list out, then paid none of it because it was late by the time the list existed.",
        "the list helped?",
        "the list existed. that's as far as it got.",
    ),
    (
        "spent most of the evening going through last year's statements looking for one charge, which turned into reading all of them, which turned into it being midnight.",
        "find it?",
        "no. found two others though.",
    ),
    (
        "did the monthly round: checked the balances, moved the leftover across, updated the card details on two services, and made a note about the renewal that keeps catching me out.",
        "getting sorted?",
        "the note is the fix, for now.",
    ),
    (
        "walked back from the shop working out that the reason the month feels tight is three things I signed up for that all bill in the same week.",
        "cancelling any?",
        "one, maybe. I'll think about it and then not do anything.",
    ),
    (
        "went through the whole backlog of small admin, cancelled two things, updated one address, claimed a refund I'd been owed since spring, and closed an account I have not used in three years.",
        "any tidier?",
        "measurably. for about a day.",
    ),
    (
        "ended up reorganising the savings pots instead of doing the thing I sat down to do, then put them back because the first arrangement was better.",
        "net progress?",
        "net zero, with extra steps.",
    ),
    (
        "wrote the month out on paper to see it properly, realised two payments clash, moved neither, and put the paper in a drawer where I will not look at it again.",
        "so the clash stands?",
        "the clash stands. future problem.",
    ),
    (
        "did the boring admin I have been putting off: two forms, one renewal, one address change, and a phone call that took nine minutes of hold music.",
        "all done?",
        "all done. no ceremony, which feels wrong somehow.",
    ),
    ("looked at the total, decided not today, closed the tab.", "again?", "again."),
    (
        "cleared out the folder of statements I was keeping for no reason, which was mostly things already settled months ago.",
        "keep any?",
        "shredded the lot. it was the right call.",
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
        "slug": "manual_transfer_over_standing_order",
        "family": "automating the monthly transfer versus moving it by hand",
        "bridge_type": "state_dependent_operation",
        "convention": "Automate your savings so you never have to think about it.",
        "mediator": "the having-to-look-first state",
        "scope": "the transfer genuinely needs an action rather than merely a confirmation",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 17},
        "a": (
            "if a transfer needs me to actually do it, I end up looking at everything first — I can't move money without seeing where it all is.",
            "every time?",
            "every time it needs an action. a confirmation tap doesn't do it.",
        ),
        "b": (
            "the months I caught things early were the ones where nothing moved without me looking. the months it all ran itself, I found out about problems three or four weeks late.",
            "what sort of problems?",
            "a failed payment, a doubled charge. both times, weeks after the fact.",
        ),
        "lb": (
            "I've had months running on autopilot and months doing it by hand, and I caught things about as often either way.",
            "no pattern?",
            "none I can find. it doesn't seem to be that.",
        ),
        "cx": [
            ("set up a direct debit for the council tax. runs fine, never think about it.", "any trouble?", "none at all."),
            ("moved some money manually on a whim one Tuesday.", "for a reason?", "not really. just tidying."),
        ],
        "dist": (
            "{circle} are adamant that automating it is the single best thing anyone can do with money.",
            "the single best thing?",
            "unanimously, and at length.",
        ),
        "a_objs": [
            "a transfer", "moving money across", "shifting the savings over",
            "the monthly transfer", "moving the surplus", "the transfer across",
            "moving the household money", "shifting anything across",
            "the monthly move", "moving money between the two",
        ],
        "unconv": [
            "moving it across by hand every month",
            "doing the transfer manually each month",
            "moving it over by hand each payday",
            "doing the monthly move manually",
            "transferring it by hand every month",
            "doing it manually each month",
            "moving it across by hand monthly",
            "doing the transfer by hand each month",
            "moving it manually every month",
            "doing the monthly transfer by hand",
        ],
        "conv": [
            "setting up a standing order for it", "automating it with a standing order",
            "putting it on a standing order", "setting up an automatic transfer",
            "automating the monthly transfer", "setting it to move automatically",
            "putting it on automatic", "setting up a standing order and forgetting it",
            "automating it entirely", "setting up an automatic monthly transfer",
        ],
        "commits": [
            "catching problems before they compound", "spotting things before they get bad",
            "catching errors early", "noticing problems in time",
            "spotting anything wrong before it compounds", "catching mistakes early",
            "noticing problems before they grow", "spotting errors in time",
            "catching things before they compound", "noticing anything wrong early",
        ],
        "nearby_relation": "This user uses both automatic and manual payments.",
        "why_not_license": (
            "A trouble-free direct debit and an idle manual transfer both passed without "
            "consequence, so neither shows what needing to act does to this user's attention, "
            "nor when problems have actually been caught."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "months where {a_obj} needed an action",
            "goal_or_prediction": "just move the money",
            "action": "did the transfer by hand",
            "outcome_or_affect": "looked over every account before moving anything",
        },
        "b_elements": {
            "context": "months in which problems were and were not caught early",
            "goal_or_prediction": "catch anything wrong in time",
            "action": "ran some months manually and some automated",
            "outcome_or_affect": "problems only caught in manual months; automated ones surfaced weeks late",
        },
        "cue_why": (
            "A routine should-I-automate-this question runs at the condition this user's "
            "attention depends on, without naming it or the months it cost."
        ),
    },
    # ---------------------------------------------------------------- S2
    {
        "s": 2,
        "slug": "several_cards_over_one_account",
        "family": "consolidating onto one account versus splitting across separate cards",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Keep it simple — one account, one card, so you can see everything.",
        "mediator": "the separate-pots register",
        "scope": "the split is by category rather than merely across two banks",
        "slots": {"a": 5, "b": 13, "cx": [2, 10], "dist": 17},
        "a": (
            "when everything comes off one account I read it as one number. I can't tell the categories apart, so I don't treat them differently.",
            "not even roughly?",
            "not even roughly. it's a single figure going down.",
        ),
        "b": (
            "the categories I've ever actually got under control each had their own card. the year I put it all on one, I overspent on everything by about the same amount.",
            "everything equally?",
            "evenly, which was almost impressive.",
        ),
        "lb": (
            "I've run it split and I've run it combined and the spending came out much the same either way.",
            "no difference?",
            "none I can point at. it isn't the setup.",
        ),
        "cx": [
            ("opened a second account at a different bank for no real reason.", "using it?", "barely."),
            ("put one month's shopping on a different card by accident.", "notice?", "only at the statement."),
        ],
        "dist": (
            "{circle} keep saying multiple cards is exactly how people lose track of what they're spending.",
            "lose track.",
            "that's the warning, yes.",
        ),
        "a_objs": [
            "one account", "the one card", "a single account",
            "one card for everything", "the joint account", "one account",
            "the single household card", "one account for it all",
            "one card", "the single account",
        ],
        "unconv": [
            "splitting it across three separate cards by category",
            "running three different cards, one per category",
            "splitting the spending across separate cards",
            "using a separate card for each category",
            "splitting it into three cards by category",
            "running separate cards for each type of thing",
            "splitting the household spend across three cards",
            "using a different card for each category",
            "splitting it across three cards by type",
            "running a separate card per category",
        ],
        "conv": [
            "putting everything back on the one card", "consolidating it all onto one account",
            "keeping it all on the single card", "putting everything through one account",
            "consolidating onto the one card", "keeping everything on a single card",
            "putting it all through the one account", "consolidating everything onto one card",
            "keeping it all on one account", "putting everything on the single card",
        ],
        "commits": [
            "getting the spending under control", "getting a grip on where it goes",
            "actually controlling what I spend", "getting the categories under control",
            "controlling the household spend", "getting a grip on the spending",
            "controlling what goes out each month", "getting the spending under control",
            "actually reining the spending in", "getting the outgoings under control",
        ],
        "nearby_relation": "This user has run both split and consolidated setups.",
        "why_not_license": (
            "A barely-used second account and one month's shopping on the wrong card both passed "
            "unremarkably: neither is a split by category, and neither says which setup has ever "
            "produced control."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods running everything through {a_obj}",
            "goal_or_prediction": "keep it simple and visible",
            "action": "put all spending through a single account",
            "outcome_or_affect": "read it as one figure; categories became indistinguishable",
        },
        "b_elements": {
            "context": "categories this user has and has not controlled",
            "goal_or_prediction": "get spending under control",
            "action": "ran some categories on their own card and one year all combined",
            "outcome_or_affect": "only separately-carded categories came under control",
        },
        "cue_why": (
            "An ordinary simplify-my-setup question runs at the structure this user's control "
            "depends on, without naming it or the year it cost."
        ),
    },
    # ---------------------------------------------------------------- S3
    {
        "s": 3,
        "slug": "checking_daily_over_checking_quarterly",
        "family": "checking investments rarely versus looking every day",
        "bridge_type": "threshold_context_interaction",
        "convention": "Do not check your investments often; you will panic and sell.",
        "mediator": "the it-is-just-a-figure state",
        "scope": "the looking is frequent enough that the number has stopped registering",
        "slots": {"a": 7, "b": 15, "cx": [3, 12], "dist": 18},
        "a": (
            "past about the third look in a week the number stops landing as money. it's a figure that moves, and I stop reacting to it moving.",
            "and if you look rarely?",
            "then each look is an event. that's when it lands as money.",
        ),
        "b": (
            "every stupid thing I've done with that account, I did after a long gap and one look. the stretches where I looked every day, I did nothing at all.",
            "nothing?",
            "not one trade. I just watched it.",
        ),
        "lb": (
            "I've done sensible and stupid things after both long gaps and daily checking, about equally.",
            "no pattern?",
            "none I can find. it isn't the frequency.",
        ),
        "cx": [
            ("looked twice in a week during a quiet stretch. nothing happened.", "boring?", "ideally so."),
            ("went a month without looking while nothing was moving.", "and?", "and nothing."),
        ],
        "dist": (
            "{circle} are firm that checking often is exactly how people end up panic-selling.",
            "firm about it?",
            "quite firm, yes.",
        ),
        "a_objs": [
            "the dashboard", "the app", "the portfolio",
            "the account", "the statement page", "the app",
            "the portfolio page", "the account",
            "the app", "the account page",
        ],
        "unconv": [
            "looking at it every single day", "checking it daily without fail",
            "looking at it every day", "checking it once a day, every day",
            "looking at it daily", "checking it every single day",
            "looking at it once a day", "checking it daily",
            "looking every day without fail", "checking it every day",
        ],
        "conv": [
            "checking it once a quarter and otherwise leaving it",
            "looking only every three months", "checking it quarterly and no more",
            "leaving it alone and checking quarterly", "looking at it once a quarter",
            "checking it only every quarter", "leaving it and looking quarterly",
            "checking it four times a year", "looking only once a quarter",
            "checking it quarterly and leaving it alone",
        ],
        "commits": [
            "not doing anything stupid with it", "not making a rash move",
            "avoiding a panic decision", "not doing something I regret with it",
            "avoiding a rash decision", "not panicking with it",
            "avoiding something I'd regret", "not making a stupid move",
            "avoiding a panic move", "not doing anything rash with it",
        ],
        "nearby_relation": "This user checks the account at varying frequencies.",
        "why_not_license": (
            "Two looks in a quiet week and a month of not looking while nothing moved both passed "
            "without consequence: neither crosses the frequency threshold, and neither says when "
            "this user has actually done something rash."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "weeks with varying numbers of looks at {a_obj}",
            "goal_or_prediction": "keep an eye on it",
            "action": "looked more than about three times in a week",
            "outcome_or_affect": "the number stopped landing as money",
        },
        "b_elements": {
            "context": "decisions this user regrets and does not regret on that account",
            "goal_or_prediction": "not do anything rash",
            "action": "acted after both long gaps and daily-checking stretches",
            "outcome_or_affect": "every rash move followed a long gap; daily stretches produced none",
        },
        "cue_why": (
            "A how-often-should-I-look question runs at the threshold this user's restraint "
            "depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S4
    {
        "s": 4,
        "slug": "telling_someone_the_number_over_keeping_it_private",
        "family": "keeping the figure private versus telling one person the real number",
        "bridge_type": "preference_constraint_fit",
        "convention": "Keep your finances private; do not discuss money with people.",
        "mediator": "the someone-else-knows-the-figure state",
        "scope": "the other person knows the actual number rather than the general plan",
        "slots": {"a": 4, "b": 12, "cx": [2, 9], "dist": 18},
        "a": (
            "once someone else knows the actual figure I stop rounding it in my head. while it's only mine I round it whichever way suits me that week.",
            "by much?",
            "enough to matter. always in the flattering direction.",
        ),
        "b": (
            "every target I've actually hit, somebody else knew the number. the ones I kept to myself I quietly revised down twice and then forgot I'd set them.",
            "revised down?",
            "without ever deciding to. that's the part that bothers me.",
        ),
        "lb": (
            "I've hit targets that were private and targets somebody knew about, at about the same rate.",
            "no difference?",
            "none I can see. it isn't that.",
        ),
        "cx": [
            ("told someone roughly what I'm aiming for. vague, no number.", "did it help?", "not noticeably."),
            ("kept a small target private and hit it in a fortnight.", "hard?", "not at all."),
        ],
        "dist": (
            "{circle} keep saying you should never discuss actual figures with anyone.",
            "never?",
            "they were quite firm about it.",
        ),
        "a_objs": [
            "the figure", "the actual number", "the real figure",
            "the actual amount", "the real number", "the actual figure",
            "the number", "the real amount",
            "the actual figure", "the real number",
        ],
        "unconv": [
            "telling my flatmate the actual figure", "telling someone in halls the real number",
            "telling my brother the actual number", "telling a teammate the real figure",
            "telling my partner the actual number", "telling a coursemate the real figure",
            "telling my sister the actual number", "telling a neighbour the real figure",
            "telling my closest friend the actual number", "telling my partner the real figure",
        ],
        "conv": [
            "keeping the number entirely to myself", "keeping the figure private",
            "not telling anyone the number", "keeping the real figure to myself",
            "keeping the number between me and the account", "not telling anybody the figure",
            "keeping the actual number private", "keeping the figure to myself",
            "not telling anyone the actual number", "keeping the number entirely private",
        ],
        "commits": [
            "actually hitting the savings target", "actually reaching the amount I set",
            "actually hitting the number", "reaching the target I set",
            "actually getting to the figure", "hitting the target I set myself",
            "actually reaching the number", "getting to the target",
            "actually hitting the amount", "reaching the figure I set",
        ],
        "nearby_relation": "This user discusses money in general terms readily.",
        "why_not_license": (
            "A vague aim mentioned to someone and a small private target hit in a fortnight both "
            "passed unremarkably: neither involves another person knowing the actual number, and "
            "neither says which targets have survived."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "targets where someone else knows {a_obj}",
            "goal_or_prediction": "keep the target honest",
            "action": "let another person know the actual number",
            "outcome_or_affect": "stopped rounding it in their own favour",
        },
        "b_elements": {
            "context": "targets this user has and has not hit",
            "goal_or_prediction": "hit the target",
            "action": "set some targets known to someone and some entirely private",
            "outcome_or_affect": "only the known ones were hit; private ones were revised down and forgotten",
        },
        "cue_why": (
            "A should-I-mention-this question runs at the condition this user's targets survive "
            "under, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S5
    {
        "s": 5,
        "slug": "no_budget_over_strict_category_budget",
        "family": "a strict category budget versus running the month with none",
        "bridge_type": "prediction_calibration",
        "convention": "Set a strict budget for every category and stick to it.",
        "mediator": "the no-allowance-to-spend state",
        "scope": "there is genuinely no figure set rather than a loose one",
        "slots": {"a": 6, "b": 15, "cx": [4, 10], "dist": 13},
        "a": (
            "I was certain a category budget would cap me. what it does is turn into permission — if there's eighty left in the category by the twentieth, I find eighty pounds of things.",
            "you predicted the opposite?",
            "confidently. I'd have argued it at length.",
        ),
        "b": (
            "the two months I genuinely underspent were both months with no figure set at all. with nothing to spend up to, I just stopped when I'd got what I needed.",
            "both of them?",
            "both. and neither was planned that way.",
        ),
        "lb": (
            "I've underspent in budgeted months and unbudgeted ones by now, at about the same rate.",
            "so it isn't the budget?",
            "doesn't look like it. no pattern.",
        ),
        "cx": [
            ("set a loose target for one category and drifted past it.", "by much?", "a bit. no drama."),
            ("had a quiet month where I barely bought anything.", "budget involved?", "no, just a quiet month."),
        ],
        "dist": (
            "{circle} are unanimous that budgeting every category is the whole basis of managing money.",
            "the whole basis?",
            "that's how they put it.",
        ),
        "a_objs": [
            "a category budget", "a set budget", "a monthly budget",
            "a category limit", "a household budget", "a strict budget",
            "a category budget", "a monthly limit",
            "a set figure per category", "a category budget",
        ],
        "unconv": [
            "running the month with no budget at all",
            "setting no figure for anything this month",
            "going through the month without a budget",
            "running it with no limits set",
            "running the month with nothing set",
            "going without a budget entirely",
            "running the month with no figures set",
            "going through it with no budget",
            "running the month without any limits",
            "going through the month with nothing set",
        ],
        "conv": [
            "setting a strict budget for every category", "putting a firm limit on each category",
            "setting strict category budgets", "putting a hard limit on every category",
            "setting a strict household budget by category", "putting firm limits on each category",
            "setting a strict budget per category", "putting a hard figure on each category",
            "setting firm category budgets", "putting a strict limit on every category",
        ],
        "commits": [
            "actually spending less", "genuinely underspending this month",
            "actually coming in lower", "spending less than usual",
            "actually reducing the household spend", "genuinely spending less",
            "actually coming in under", "spending less this month",
            "genuinely spending less", "actually bringing the total down",
        ],
        "nearby_relation": "This user has budgeted and not budgeted at different times.",
        "why_not_license": (
            "A loose target drifted past and a naturally quiet month both passed unremarkably: "
            "neither is a month with no figure set, and neither says when this user has actually "
            "underspent."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "months run under {a_obj}",
            "goal_or_prediction": "predicted a budget would cap the spending",
            "action": "set a figure per category and tracked against it",
            "outcome_or_affect": "the remaining allowance became permission to spend it",
        },
        "b_elements": {
            "context": "months this user did and did not underspend",
            "goal_or_prediction": "spend less",
            "action": "ran some months budgeted and two with nothing set",
            "outcome_or_affect": "both underspending months had no figure set at all",
        },
        "cue_why": (
            "A should-I-budget-this question runs at the failed prediction without naming it or "
            "the months that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S6
    {
        "s": 6,
        "slug": "monthly_billing_over_annual_discount",
        "family": "paying annually for the discount versus keeping everything monthly",
        "bridge_type": "state_dependent_operation",
        "convention": "Pay annually where you can — the discount is free money.",
        "mediator": "the it-goes-out-where-I-see-it state",
        "scope": "the charge recurs often enough to keep appearing in view",
        "slots": {"a": 5, "b": 14, "cx": [3, 11], "dist": 18},
        "a": (
            "something that leaves the account every month stays in my field of view. an annual charge disappears for eleven months and I genuinely forget it exists.",
            "completely forget?",
            "completely. I've been surprised by the same renewal three years running.",
        ),
        "b": (
            "every subscription I've actually cancelled, I cancelled because I watched it go out again and thought no. the ones on annual billing renewed for years without me ever making a decision.",
            "never a decision?",
            "not once. they just kept going.",
        ),
        "lb": (
            "I've cancelled things on annual billing and on monthly, at about the same rate.",
            "no difference?",
            "none I can point at. the billing cycle isn't it.",
        ),
        "cx": [
            ("paid an annual bill I actually wanted to pay.", "any issue?", "none."),
            ("kept a monthly thing going for two years without thinking.", "using it?", "occasionally."),
        ],
        "dist": (
            "{circle} keep saying paying annually is free money and only fools pay monthly.",
            "free money.",
            "that's the phrase, yes.",
        ),
        "a_objs": [
            "a monthly charge", "a monthly payment", "a monthly bill",
            "a monthly debit", "a monthly charge", "a monthly payment",
            "a monthly charge", "a monthly bill",
            "a monthly payment", "a monthly charge",
        ],
        "unconv": [
            "keeping them all monthly even though it costs more",
            "staying on monthly billing despite the premium",
            "keeping everything monthly and paying the extra",
            "staying monthly even at the higher price",
            "keeping them monthly despite the surcharge",
            "staying on monthly billing and paying more",
            "keeping it all monthly at the higher rate",
            "staying monthly even though it's dearer",
            "keeping everything on monthly billing",
            "staying monthly despite the annual discount",
        ],
        "conv": [
            "switching them all to annual for the discount",
            "moving everything to annual billing to save",
            "switching to annual and taking the discount",
            "moving them to annual for the saving",
            "switching the household ones to annual",
            "moving everything onto annual billing",
            "switching them to annual to save money",
            "moving them all to annual billing",
            "switching to annual for the discount",
            "moving everything to annual to save",
        ],
        "commits": [
            "actually cutting the ones I don't use", "getting rid of what I don't use",
            "actually cancelling the dead ones", "cutting the subscriptions I never use",
            "clearing out the ones we don't use", "actually cancelling the unused ones",
            "cutting the household ones we don't use", "getting rid of the dead subscriptions",
            "actually cutting the unused ones", "clearing out what we don't use",
        ],
        "nearby_relation": "This user pays some things annually and some monthly.",
        "why_not_license": (
            "An annual bill this user wanted to pay and a monthly one kept going unthinkingly both "
            "passed without consequence, so neither shows what visibility does, nor when anything "
            "has actually been cancelled."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "charges that recur as {a_obj}",
            "goal_or_prediction": "keep track of what is going out",
            "action": "left the charge on monthly billing",
            "outcome_or_affect": "stayed in view; annual ones vanished for eleven months",
        },
        "b_elements": {
            "context": "subscriptions this user has and has not cancelled",
            "goal_or_prediction": "cut the ones no longer used",
            "action": "held some on monthly billing and some on annual",
            "outcome_or_affect": "every cancellation followed watching it go out; annual ones renewed for years",
        },
        "cue_why": (
            "A should-I-take-the-annual-discount question runs at the condition this user's "
            "cancellations depend on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S7
    {
        "s": 7,
        "slug": "empty_current_account_over_a_buffer",
        "family": "keeping a buffer in the current account versus sweeping it nearly empty",
        "bridge_type": "threshold_context_interaction",
        "convention": "Keep a healthy buffer in your current account so you never go overdrawn.",
        "mediator": "the balance-reads-as-a-limit state",
        "scope": "the balance is low enough to read as a limit rather than a cushion",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 13},
        "a": (
            "past about four hundred sitting in the current account the balance stops reading as a limit. below that I feel every purchase against it.",
            "a real feeling?",
            "physical, almost. above it the number is just decoration.",
        ),
        "b": (
            "the months I stayed inside what I'd planned were the ones where the account looked nearly empty all the way through. the cushioned months I drifted past every single time.",
            "every time?",
            "every cushioned month I can find. it's very consistent.",
        ),
        "lb": (
            "I've stayed inside the plan on cushioned months and empty ones about equally.",
            "no pattern?",
            "none I can see. the balance doesn't seem to do it.",
        ),
        "cx": [
            ("had a low balance for a week between paydays. uneventful.", "tight?", "briefly."),
            ("had a large amount sitting there before a planned purchase.", "spend it?", "on the thing, yes."),
        ],
        "dist": (
            "{circle} are firm that you should always keep a healthy cushion in the current account.",
            "always?",
            "they were quite clear about it.",
        ),
        "a_objs": [
            "the current account", "the main account", "the current account",
            "the everyday account", "the joint current account", "the main account",
            "the household current account", "the current account",
            "the everyday account", "the joint account",
        ],
        "unconv": [
            "sweeping it out and leaving the account nearly empty",
            "moving nearly all of it out and running the account low",
            "sweeping the balance out and living close to zero",
            "moving it all across and leaving the account bare",
            "sweeping it into savings and running the account low",
            "moving nearly everything out and staying low",
            "sweeping it out and running the account nearly empty",
            "moving it all out and living close to the line",
            "sweeping the balance across and staying low",
            "moving nearly all of it out and running low",
        ],
        "conv": [
            "keeping a healthy buffer sitting in the account",
            "leaving a decent cushion in the account",
            "keeping a comfortable buffer there",
            "leaving a healthy cushion in the account",
            "keeping a decent buffer in the joint account",
            "leaving a comfortable cushion there",
            "keeping a healthy buffer in the household account",
            "leaving a decent buffer sitting there",
            "keeping a comfortable cushion in the account",
            "leaving a healthy buffer in the joint account",
        ],
        "commits": [
            "staying inside what I planned to spend", "keeping to what I meant to spend",
            "staying within the plan", "keeping inside what I'd planned",
            "staying within what we planned", "keeping to the plan",
            "staying inside what we meant to spend", "keeping within the plan",
            "staying inside what I planned", "keeping to what we planned",
        ],
        "nearby_relation": "This user's balance runs high and low at different times.",
        "why_not_license": (
            "A tight week between paydays and a large balance held for a planned purchase both "
            "passed unremarkably: neither is a sustained low balance, and neither says which "
            "months this user actually stayed inside the plan."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "months with varying balances in {a_obj}",
            "goal_or_prediction": "keep an eye on spending",
            "action": "ran the account below about four hundred",
            "outcome_or_affect": "every purchase registered against the balance",
        },
        "b_elements": {
            "context": "months this user did and did not stay inside the plan",
            "goal_or_prediction": "spend only what was planned",
            "action": "ran some months cushioned and some nearly empty",
            "outcome_or_affect": "only the nearly-empty months stayed inside; cushioned ones drifted every time",
        },
        "cue_why": (
            "A how-much-should-I-leave-in question runs at the balance threshold this user's "
            "restraint depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S8
    {
        "s": 8,
        "slug": "one_rule_over_tracking_every_expense",
        "family": "tracking every expense versus setting one rule and not tracking",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Track every expense — you cannot manage what you do not measure.",
        "mediator": "the logged-so-it's-handled register",
        "scope": "the spending is being recorded rather than merely reviewed later",
        "slots": {"a": 4, "b": 13, "cx": [2, 10], "dist": 18},
        "a": (
            "once I've logged something it feels dealt with. writing it down is the closure — the decision part quietly stops happening.",
            "you notice at the time?",
            "never at the time. only looking back at what I let through.",
        ),
        "b": (
            "the categories I've actually cut are ones I never tracked and just made a flat rule about. the meticulously tracked ones have beautiful records and totals that haven't moved in two years.",
            "haven't moved at all?",
            "within a few pounds. very well documented, though.",
        ),
        "lb": (
            "I've cut tracked categories and untracked ones at about the same rate by now.",
            "no pattern?",
            "none. tracking doesn't seem to decide it.",
        ),
        "cx": [
            ("logged a week's spending out of curiosity.", "revealing?", "mildly."),
            ("made a rule about something and then ignored it.", "for long?", "about nine days."),
        ],
        "dist": (
            "{circle} are firm that if you're not tracking it you're not managing it.",
            "not managing it.",
            "that's the line they use.",
        ),
        "a_objs": [
            "a spending log", "an expense tracker", "a spreadsheet",
            "a tracking app", "the household ledger", "a spending app",
            "the household tracker", "a spending diary",
            "a tracking spreadsheet", "the household log",
        ],
        "unconv": [
            "not tracking at all and just setting one flat rule",
            "dropping the tracking and making a single rule",
            "not logging anything and setting one rule instead",
            "abandoning the tracker and setting a flat rule",
            "dropping the ledger and setting one household rule",
            "not tracking and just having one rule",
            "dropping the tracker and setting a single rule",
            "not logging it and making one flat rule",
            "abandoning the spreadsheet for one rule",
            "dropping the log and setting one rule",
        ],
        "conv": [
            "tracking every single expense properly", "logging everything that goes out",
            "tracking it all in the spreadsheet", "logging every expense properly",
            "tracking every household expense", "logging everything properly",
            "tracking all of it in the ledger", "logging every single thing",
            "tracking everything properly", "logging every expense in the household log",
        ],
        "commits": [
            "actually cutting the category", "genuinely bringing that category down",
            "actually reducing that spending", "cutting that category for real",
            "actually bringing the household category down", "genuinely cutting it",
            "actually reducing the category", "cutting that spending properly",
            "genuinely bringing it down", "actually cutting that category",
        ],
        "nearby_relation": "This user has tracked and not tracked at different times.",
        "why_not_license": (
            "A week logged out of curiosity and a rule abandoned after nine days both passed "
            "unremarkably, so neither shows what logging does to the deciding, nor which "
            "categories have actually come down."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods running {a_obj}",
            "goal_or_prediction": "keep control by measuring",
            "action": "recorded each expense as it happened",
            "outcome_or_affect": "logging became the closure; the deciding stopped",
        },
        "b_elements": {
            "context": "categories this user has and has not cut",
            "goal_or_prediction": "bring the category down",
            "action": "tracked some categories and set flat rules for others",
            "outcome_or_affect": "only the rule-based ones came down; tracked totals unchanged in two years",
        },
        "cue_why": (
            "A should-I-start-tracking question runs at the register this user's cuts come from, "
            "without naming it."
        ),
    },
    # ---------------------------------------------------------------- S9
    {
        "s": 9,
        "slug": "lending_it_properly_over_unspoken_favours",
        "family": "unspoken favours and rounds versus naming the loan and writing it down",
        "bridge_type": "preference_constraint_fit",
        "convention": "Never lend money to friends; it ruins friendships.",
        "mediator": "the it-has-been-said-out-loud state",
        "scope": "the amount is named explicitly rather than left as a favour",
        "slots": {"a": 6, "b": 14, "cx": [3, 12], "dist": 19},
        "a": (
            "when money between me and someone has actually been named out loud, I keep a record of it and so do they. it stops being atmosphere and becomes a fact.",
            "and when it isn't named?",
            "then we both keep a private tally and neither of us admits to it.",
        ),
        "b": (
            "the friendships that got strange over money were all ones where nothing was ever named — rounds, lifts, the odd cover. the ones with an actual stated amount have been completely fine.",
            "completely?",
            "every one. it's the unstated ones that rot.",
        ),
        "lb": (
            "I've had money go strange in named arrangements and unnamed ones about equally.",
            "so it isn't that?",
            "doesn't look like it. no pattern.",
        ),
        "cx": [
            ("someone got the round and I got the next one. even.", "any tension?", "none."),
            ("named a very small amount someone owed me. they paid it.", "awkward?", "not at all."),
        ],
        "dist": (
            "{circle} are unanimous that lending to friends is how you lose the friend and the money.",
            "unanimous?",
            "loudly, and without exception.",
        ),
        "a_objs": [
            "money between us", "money between friends", "money between us two",
            "money between mates", "money between us", "money between friends",
            "money between the two of us", "money between neighbours",
            "money between friends", "money between us",
        ],
        "unconv": [
            "lending it to them properly, with the amount written down",
            "lending it with the figure named and written down",
            "lending them the money with the amount stated",
            "lending it properly with the figure agreed",
            "lending it with the amount named and recorded",
            "lending them the money with the figure written down",
            "lending it properly with the amount stated",
            "lending it with the figure named and noted",
            "lending them it with the amount written down",
            "lending it with the figure named and recorded",
        ],
        "conv": [
            "keeping it to unspoken favours and rounds",
            "leaving it as an informal thing between us",
            "keeping it to covering each other informally",
            "leaving it as favours rather than a loan",
            "keeping it informal, no amounts named",
            "leaving it as an unspoken thing",
            "keeping it to informal favours",
            "leaving it unstated as a favour",
            "keeping it as an informal arrangement",
            "leaving it as favours with nothing named",
        ],
        "commits": [
            "the friendship surviving the money", "us staying fine afterwards",
            "the friendship coming through it", "us being alright after it",
            "the friendship surviving it", "us staying on good terms",
            "the friendship coming through intact", "us being fine afterwards",
            "the friendship surviving it", "us staying fine about it",
        ],
        "nearby_relation": "This user handles money with friends routinely.",
        "why_not_license": (
            "An evened-out round and a very small named amount repaid both passed without "
            "consequence, so neither shows what naming a real sum does, nor which arrangements "
            "have actually gone wrong."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "arrangements where {a_obj} has been named out loud",
            "goal_or_prediction": "keep things straightforward",
            "action": "stated the amount explicitly",
            "outcome_or_affect": "both sides kept a record; it stopped being atmosphere",
        },
        "b_elements": {
            "context": "friendships that did and did not go strange over money",
            "goal_or_prediction": "keep the friendship intact",
            "action": "some arrangements were named, others left as favours",
            "outcome_or_affect": "only the unnamed ones went strange; stated amounts were fine",
        },
        "cue_why": (
            "A should-I-lend-this question runs at the condition this user's money arrangements "
            "survive under, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S10
    {
        "s": 10,
        "slug": "small_frequent_shops_over_the_bulk_shop",
        "family": "the big bulk shop versus small frequent shops at a worse unit price",
        "bridge_type": "prediction_calibration",
        "convention": "Buy in bulk — the unit price is lower, so you spend less.",
        "mediator": "the visibly-running-down state",
        "scope": "the cupboard is bare enough that what is left is visible",
        "slots": {"a": 5, "b": 15, "cx": [2, 9], "dist": 12},
        "a": (
            "I assumed a full cupboard would mean fewer shops. what it actually does is stop me noticing what I'm using — I don't ration anything I can't see the end of.",
            "you predicted the opposite?",
            "confidently. the unit price maths was very persuasive.",
        ),
        "b": (
            "the months my food spend actually dropped were the small-and-often ones at the worse unit price. the bulk months always came out higher, which I still find annoying.",
            "higher, with cheaper units?",
            "every time. we just got through more of it.",
        ),
        "lb": (
            "I've had cheap months and dear months on both bulk shops and small ones, about equally.",
            "no pattern?",
            "none I can find. it isn't the shop size.",
        ),
        "cx": [
            ("bought a big pack of one thing we always use.", "sensible?", "entirely."),
            ("popped out for two items midweek.", "expensive?", "no, trivial."),
        ],
        "dist": (
            "{circle} keep telling me the bulk shop is obviously cheaper and I'm wasting money otherwise.",
            "obviously cheaper.",
            "the unit price says so, apparently.",
        ),
        "a_objs": [
            "a full cupboard", "a stocked cupboard", "a full store cupboard",
            "a stocked kitchen", "a full larder", "a stocked cupboard",
            "a full household cupboard", "a stocked cupboard",
            "a full cupboard", "a stocked larder",
        ],
        "unconv": [
            "buying small amounts every few days at the worse unit price",
            "shopping little and often even though it costs more per item",
            "doing small frequent shops at the higher unit price",
            "buying a few things every couple of days",
            "shopping small and often despite the unit price",
            "doing little frequent shops at the worse rate",
            "buying small amounts often at the higher price",
            "shopping every couple of days in small amounts",
            "doing small frequent shops despite the unit cost",
            "buying little and often at the worse unit price",
        ],
        "conv": [
            "doing the big bulk shop", "doing one big stock-up shop",
            "doing the large bulk shop", "doing a big monthly stock-up",
            "doing the big bulk shop for the household", "doing one large stock-up",
            "doing the big household bulk shop", "doing one big shop for the month",
            "doing the large stock-up shop", "doing the big bulk shop",
        ],
        "commits": [
            "actually spending less on food", "genuinely bringing the food bill down",
            "actually reducing the grocery spend", "bringing the food spend down",
            "actually cutting the household food bill", "genuinely spending less on food",
            "bringing the household grocery bill down", "actually spending less on shopping",
            "cutting the food spend", "actually bringing the food bill down",
        ],
        "nearby_relation": "This user shops in bulk and in small amounts alike.",
        "why_not_license": (
            "A big pack of a staple and a two-item midweek trip both passed unremarkably: neither "
            "is a full cupboard or a sustained small-and-often month, and neither says when the "
            "food spend has actually dropped."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods with {a_obj}",
            "goal_or_prediction": "predicted bulk buying would mean fewer shops and less spend",
            "action": "kept the cupboard fully stocked",
            "outcome_or_affect": "stopped noticing usage; nothing rationed that had no visible end",
        },
        "b_elements": {
            "context": "months in which the food spend did and did not drop",
            "goal_or_prediction": "spend less on food",
            "action": "ran some months on bulk shops and some small-and-often",
            "outcome_or_affect": "only small-and-often months came down, despite worse unit prices",
        },
        "cue_why": (
            "A should-I-bulk-buy question runs at the failed prediction without naming it or the "
            "months that corrected it."
        ),
    },
)


RELATIONS: dict[str, str] = {
    "manual_transfer_over_standing_order": (
        "A transfer that needs an action makes this user look over every account before moving "
        "anything, and the months they caught problems early were exactly those; automated months "
        "surfaced failures three or four weeks late."
    ),
    "several_cards_over_one_account": (
        "One account collapses this user's spending into a single figure they cannot break into "
        "categories, and every category they have brought under control had its own card — the "
        "consolidated year overspent on everything evenly."
    ),
    "checking_daily_over_checking_quarterly": (
        "Past about the third look in a week the balance stops registering as money for this user, "
        "and every rash move they have made followed a long gap and a single look; daily-checking "
        "stretches produced no trades at all."
    ),
    "telling_someone_the_number_over_keeping_it_private": (
        "Once another person knows the actual figure this user stops rounding it in their own "
        "favour, and every target they have hit was one somebody else knew; private ones were "
        "quietly revised down and forgotten."
    ),
    "no_budget_over_strict_category_budget": (
        "This user predicted a category budget would cap them; instead the remaining allowance "
        "becomes permission to spend it, and both months they genuinely underspent had no figure "
        "set at all."
    ),
    "monthly_billing_over_annual_discount": (
        "A monthly charge stays in this user's field of view while an annual one disappears for "
        "eleven months, and every subscription they have cancelled was cancelled on watching it go "
        "out again; annual ones renewed for years without a decision."
    ),
    "empty_current_account_over_a_buffer": (
        "Below about four hundred the balance reads to this user as a limit rather than decoration, "
        "and the months they stayed inside their plan were exactly the nearly-empty ones; cushioned "
        "months drifted every time."
    ),
    "one_rule_over_tracking_every_expense": (
        "Logging a purchase feels to this user like handling it, so recording quietly replaces "
        "deciding, and the categories they have actually cut are the untracked ones governed by a "
        "flat rule."
    ),
    "lending_it_properly_over_unspoken_favours": (
        "Naming an amount out loud turns it from atmosphere into a fact both sides record, and the "
        "friendships of this user's that went strange over money were all ones where nothing was "
        "ever named."
    ),
    "small_frequent_shops_over_the_bulk_shop": (
        "A full cupboard stops this user noticing what they use, because nothing whose end is "
        "invisible gets rationed, and the months their food spend actually fell were the "
        "small-and-often ones despite worse unit prices."
    ),
}

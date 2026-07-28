"""Finance scenario families S11-S20, extending the batch to 200 units / 600 files.

Same contract as `finance_spec.SCENARIOS`. Bridge types continue the two-per-type
rotation so all five are used four times across S1-S20.
"""

from __future__ import annotations

SCENARIOS_EXT: tuple[dict, ...] = (
    # ---------------------------------------------------------------- S11
    {
        "s": 11,
        "slug": "cash_in_pocket_over_card_for_everything",
        "family": "paying by card for the tracking versus taking the week's money in cash",
        "bridge_type": "state_dependent_operation",
        "convention": "Pay by card — it is tracked automatically and easier to review.",
        "mediator": "the watching-it-physically-go-down state",
        "scope": "the money is physically finite rather than merely budgeted",
        "slots": {"a": 6, "b": 15, "cx": [3, 10], "dist": 18},
        "a": (
            "with notes in my pocket I can see the amount going down without doing any arithmetic. I don't have to decide to check — it's just visible.",
            "and on card?",
            "on card I'd have to look it up, which means deciding to look it up.",
        ),
        "b": (
            "the weeks I came in under what I'd meant to spend were the ones where I could see it going. the card weeks I only ever found out afterwards, and afterwards is too late to do anything.",
            "always afterwards?",
            "always. by then it's just a number I'm reading about myself.",
        ),
        "lb": (
            "I've come in under on cash weeks and card weeks by now, at about the same rate.",
            "no pattern?",
            "none I can find. it isn't the payment method.",
        ),
        "cx": [
            ("paid for one big thing on the card as planned.", "any issue?", "none at all."),
            ("had a tenner in my pocket for a week and never spent it.", "forgot it?", "entirely."),
        ],
        "dist": (
            "{circle} are firm that card is obviously better because everything gets tracked for you.",
            "tracked for you.",
            "that's the selling point, apparently.",
        ),
        "a_objs": [
            "notes in my pocket", "cash on me", "notes in my wallet",
            "cash in hand", "notes in my purse", "cash on me",
            "notes in my wallet", "cash in my pocket",
            "notes on me", "cash in the tin",
        ],
        "unconv": [
            "taking the week's money out in cash and using that",
            "drawing the week out in notes and spending only that",
            "taking the week's spending out as cash",
            "drawing it out in cash for the week",
            "taking the week's money out in notes",
            "drawing the week's spending out in cash",
            "taking the household week out in cash",
            "drawing the week out in notes",
            "taking the week's money out as cash",
            "drawing the week's spending out in notes",
        ],
        "conv": [
            "putting it all on the card so it's tracked",
            "using the card for everything so it's recorded",
            "keeping it all on card for the tracking",
            "putting everything on the card to track it",
            "using the card throughout so it's logged",
            "keeping everything on card so it's tracked",
            "putting the household week on the card",
            "using the card for it all so it's recorded",
            "keeping it on card for the record",
            "putting it all on card so it's tracked",
        ],
        "commits": [
            "coming in under for the week", "staying under what I meant to spend",
            "coming in under for the week", "keeping the week under",
            "coming in under for the week", "staying under for the week",
            "keeping the household week under", "coming in under",
            "staying under for the week", "keeping the week's spend under",
        ],
        "nearby_relation": "This user uses cash and card interchangeably.",
        "why_not_license": (
            "One planned card purchase and a forgotten tenner both passed without consequence, so "
            "neither shows what visible finite money does, nor which weeks this user has actually "
            "come in under."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "weeks spent with {a_obj}",
            "goal_or_prediction": "keep an eye on the week's spending",
            "action": "used physical cash",
            "outcome_or_affect": "saw the amount going down without deciding to check",
        },
        "b_elements": {
            "context": "weeks this user did and did not come in under",
            "goal_or_prediction": "spend no more than intended",
            "action": "ran some weeks on cash and some on card",
            "outcome_or_affect": "only cash weeks came in under; card weeks were discovered afterwards",
        },
        "cue_why": (
            "A how-should-I-pay question runs at the condition this user's restraint depends on, "
            "without naming it."
        ),
    },
    # ---------------------------------------------------------------- S12
    {
        "s": 12,
        "slug": "separate_balances_over_one_consolidation_loan",
        "family": "consolidating debts into one lower-rate loan versus keeping them separate",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Consolidate your debts into one loan at a lower rate.",
        "mediator": "the each-one-has-its-own-date register",
        "scope": "the balances are separate enough to each carry their own deadline",
        "slots": {"a": 5, "b": 14, "cx": [2, 11], "dist": 17},
        "a": (
            "with several separate balances each one carries its own date, and I clear them one at a time purely to be rid of the date. the rate barely enters into it.",
            "the date, not the money?",
            "the date. I want the reminder gone.",
        ),
        "b": (
            "every balance I've actually cleared, I cleared to get rid of a deadline. the one consolidated loan I had has sat within a few hundred of the same figure for two years, at a better rate.",
            "two years?",
            "two years, and I have never once made an extra payment on it.",
        ),
        "lb": (
            "I've cleared separate balances and consolidated ones at about the same rate by now.",
            "no pattern?",
            "none I can see. the structure doesn't decide it.",
        ),
        "cx": [
            ("paid off a small balance because it was almost nothing.", "satisfying?", "briefly."),
            ("moved one balance to a lower rate and left it there.", "cheaper?", "marginally."),
        ],
        "dist": (
            "{circle} keep saying consolidating at a lower rate is obviously the right move.",
            "obviously.",
            "the arithmetic is on their side, to be fair.",
        ),
        "a_objs": [
            "separate balances", "several balances", "separate debts",
            "a few separate balances", "the separate balances", "several small balances",
            "the separate household balances", "a few balances",
            "several separate balances", "the separate balances",
        ],
        "unconv": [
            "keeping them as separate balances at the higher rates",
            "leaving them separate even at worse rates",
            "keeping them as separate debts despite the rates",
            "leaving them as separate balances at higher rates",
            "keeping them separate even though it costs more",
            "leaving them as separate balances despite the rate",
            "keeping the household ones separate at higher rates",
            "leaving them separate at the worse rates",
            "keeping them as separate balances despite the cost",
            "leaving them separate even at the higher rates",
        ],
        "conv": [
            "consolidating them into one lower-rate loan",
            "rolling them into a single cheaper loan",
            "consolidating into one loan at a better rate",
            "rolling them all into one lower-rate loan",
            "consolidating them into a single cheaper loan",
            "rolling them into one loan at a lower rate",
            "consolidating the household ones into one loan",
            "rolling them into a single lower-rate loan",
            "consolidating into one cheaper loan",
            "rolling them all into one loan at a better rate",
        ],
        "commits": [
            "actually clearing the debt", "genuinely getting it paid off",
            "actually paying it down", "getting the balances cleared",
            "actually clearing the household debt", "genuinely paying it off",
            "getting the household balances cleared", "actually paying it down",
            "genuinely clearing it", "actually getting it paid off",
        ],
        "nearby_relation": "This user has held both separate and consolidated debts.",
        "why_not_license": (
            "A trivially small balance paid off and one balance moved to a lower rate both passed "
            "unremarkably, so neither shows what separate deadlines do, nor which structure has "
            "actually seen debt cleared."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods holding {a_obj}",
            "goal_or_prediction": "keep on top of the debt",
            "action": "held the balances separately, each with its own date",
            "outcome_or_affect": "cleared them one at a time to be rid of the deadline",
        },
        "b_elements": {
            "context": "balances this user has and has not cleared",
            "goal_or_prediction": "actually pay the debt down",
            "action": "held some as separate balances and one consolidated",
            "outcome_or_affect": "every clearance was deadline-driven; the consolidated loan never moved",
        },
        "cue_why": (
            "A should-I-consolidate question runs at the structure this user's repayments depend "
            "on, without naming it or the two years it cost."
        ),
    },
    # ---------------------------------------------------------------- S13
    {
        "s": 13,
        "slug": "buying_at_full_price_over_waiting_for_the_sale",
        "family": "waiting for the sale versus buying it today at full price",
        "bridge_type": "threshold_context_interaction",
        "convention": "Never pay full price — wait for it to go on sale.",
        "mediator": "the still-an-actual-decision state",
        "scope": "the wait has been short enough that it is still a decision",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 12},
        "a": (
            "past about three weeks of watching something for a discount, it stops being a purchase I'm deciding on and turns into a thing I'm owed. by then I'm not choosing, I'm collecting.",
            "owed?",
            "that's genuinely how it feels by week four.",
        ),
        "b": (
            "everything I've regretted buying was something I'd been waiting on for weeks and finally caught in a sale. the things I decided on and bought the same day, I've kept and used.",
            "all of them?",
            "the pattern's uncomfortably clean.",
        ),
        "lb": (
            "I've regretted sale purchases and full-price ones at about the same rate by now.",
            "no pattern?",
            "none I can see. it isn't the discount.",
        ),
        "cx": [
            ("waited a few days for something and it dropped. bought it.", "pleased?", "reasonably."),
            ("bought something at full price on impulse and returned it.", "hassle?", "mild."),
        ],
        "dist": (
            "{circle} are firm that paying full price is just losing money for no reason.",
            "for no reason.",
            "that's the framing, yes.",
        ),
        "a_objs": [
            "watching something for a discount", "waiting for a price drop", "tracking a price",
            "watching for a sale", "waiting on a discount", "tracking something for a sale",
            "waiting for the price to drop", "watching for a discount",
            "waiting on a sale", "tracking it for a discount",
        ],
        "unconv": [
            "buying it today at full price", "just buying it now at full price",
            "buying it at full price today", "paying full price and getting it now",
            "buying it now at the full price", "just paying full price today",
            "buying it at full price now", "paying the full price today",
            "buying it now without waiting", "paying full price and being done with it",
        ],
        "conv": [
            "waiting for it to go on sale", "holding out for a discount",
            "waiting until it drops in price", "holding on until there's a sale",
            "waiting for the sale to come round", "holding out until it's discounted",
            "waiting until it goes on offer", "holding on for a price drop",
            "waiting for the discount", "holding out for the sale",
        ],
        "commits": [
            "not regretting the purchase", "actually using what I buy",
            "not regretting it afterwards", "actually keeping what I buy",
            "not regretting the purchase", "actually using it once I've got it",
            "not regretting it later", "actually keeping and using it",
            "not regretting the buy", "actually using what we buy",
        ],
        "nearby_relation": "This user buys at full price and in sales alike.",
        "why_not_license": (
            "A few days' wait that ended in a discount and an impulse purchase promptly returned "
            "both passed unremarkably: neither crosses the multi-week threshold, and neither says "
            "which purchases this user has actually regretted."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods spent {a_obj}",
            "goal_or_prediction": "get it at a better price",
            "action": "waited past about three weeks",
            "outcome_or_affect": "stopped being a decision; became something felt owed",
        },
        "b_elements": {
            "context": "purchases this user has and has not regretted",
            "goal_or_prediction": "buy things worth keeping",
            "action": "bought some after long waits in sales and some same-day at full price",
            "outcome_or_affect": "every regret was a long-waited sale purchase; same-day ones were kept",
        },
        "cue_why": (
            "A should-I-wait-for-the-sale question runs at the waiting threshold this user's "
            "regrets depend on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S14
    {
        "s": 14,
        "slug": "lower_contribution_over_the_full_match",
        "family": "raising the pension contribution to the full match versus keeping it lower",
        "bridge_type": "preference_constraint_fit",
        "convention": "Always contribute enough to get the full employer match; it is free money.",
        "mediator": "the take-home-is-the-only-real-number state",
        "scope": "the money is diverted before it lands rather than moved afterwards",
        "slots": {"a": 4, "b": 13, "cx": [2, 9], "dist": 18},
        "a": (
            "I run the month off whatever actually lands in the account. anything taken before that never enters the arithmetic at all — I don't experience it as money I have.",
            "not even knowing it's there?",
            "knowing doesn't help. it isn't in the number I plan against.",
        ),
        "b": (
            "every time I've raised the contribution I've been on the credit card by the third week of the month. the years I kept it lower I stayed clear of the card entirely.",
            "every time?",
            "three for three. I keep expecting it to go differently.",
        ),
        "lb": (
            "I've ended up on the card in high-contribution years and low ones about equally.",
            "no pattern?",
            "none I can find. the contribution isn't what does it.",
        ),
        "cx": [
            ("moved some money into savings after payday. fine.", "missed it?", "not really."),
            ("had one month with an unusually large outgoing. absorbed it.", "tight?", "briefly."),
        ],
        "dist": (
            "{circle} are unanimous that not taking the full match is leaving free money on the table.",
            "free money.",
            "that's the phrase everyone uses.",
        ),
        "a_objs": [
            "take-home", "what actually lands", "the money that arrives",
            "what hits the account", "what actually lands", "what arrives in the account",
            "the household take-home", "what actually lands",
            "what hits the account", "what lands in the joint account",
        ],
        "unconv": [
            "keeping the contribution below the full match",
            "leaving the contribution lower than the match",
            "keeping it under the full match level",
            "leaving the contribution below the match",
            "keeping it lower than the full match",
            "leaving it under the match threshold",
            "keeping the household contribution below the match",
            "leaving it lower than the full match",
            "keeping the contribution under the match",
            "leaving it below the full match level",
        ],
        "conv": [
            "raising it to take the full employer match",
            "putting it up to the full match",
            "raising the contribution to get the full match",
            "increasing it to the full match level",
            "raising it to capture the full match",
            "putting the contribution up to the match",
            "raising it to the full match",
            "increasing it to take the whole match",
            "putting it up to get the full match",
            "raising it to the full match level",
        ],
        "commits": [
            "staying off the credit card", "keeping clear of the card",
            "staying off the card each month", "not ending up on the card",
            "keeping off the credit card", "staying clear of the card",
            "keeping the household off the card", "not ending up on the credit card",
            "staying off the card", "keeping clear of the credit card",
        ],
        "nearby_relation": "This user moves money about after payday without difficulty.",
        "why_not_license": (
            "Money moved to savings after payday and one large outgoing absorbed both passed "
            "without consequence: neither is diverted before landing, and neither says which years "
            "this user has stayed off the card."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "months planned against {a_obj}",
            "goal_or_prediction": "plan the month accurately",
            "action": "budgeted from what actually arrived",
            "outcome_or_affect": "pre-deducted money never entered the arithmetic",
        },
        "b_elements": {
            "context": "years this user did and did not end up on the credit card",
            "goal_or_prediction": "stay off the card",
            "action": "ran some years at a raised contribution and some lower",
            "outcome_or_affect": "every raised year hit the card by week three; lower years stayed clear",
        },
        "cue_why": (
            "A should-I-take-the-match question runs at the constraint this user's month is planned "
            "against, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S15
    {
        "s": 15,
        "slug": "renting_on_over_buying",
        "family": "buying rather than renting versus carrying on renting and staying liquid",
        "bridge_type": "prediction_calibration",
        "convention": "Buy rather than rent; rent is dead money.",
        "mediator": "the nothing-tied-up state",
        "scope": "the money is genuinely available rather than merely accessible on paper",
        "slots": {"a": 6, "b": 14, "cx": [3, 11], "dist": 19},
        "a": (
            "I predicted owning would make me feel settled enough to take other chances. what happened is that with everything tied up in it I stopped taking any — no course, no gap between jobs, nothing.",
            "the opposite of settled, then?",
            "the opposite of free, anyway. I hadn't separated the two.",
        ),
        "b": (
            "the two moves that actually changed what I earn were both made in years when nothing was tied up. I could afford to be wrong for six months, so I risked it.",
            "and in the tied-up years?",
            "nothing. I stayed exactly where I was and called it stability.",
        ),
        "lb": (
            "I've made good moves in tied-up years and liquid ones about equally by now.",
            "no pattern?",
            "none I can point at. it isn't that.",
        ),
        "cx": [
            ("had savings sitting there and did nothing in particular with them.", "for long?", "a year or so."),
            ("had a tied-up year that was perfectly pleasant.", "any cost?", "none I noticed."),
        ],
        "dist": (
            "{circle} keep telling me renting is dead money and I'm throwing it away every month.",
            "dead money.",
            "the phrase comes up every time.",
        ),
        "a_objs": [
            "everything tied up", "it all tied up", "the money tied up",
            "everything committed", "it all tied up in the house", "everything tied up",
            "the household money tied up", "everything committed to it",
            "it all tied up", "everything tied up in it",
        ],
        "unconv": [
            "carrying on renting and keeping it liquid",
            "staying in the rental and keeping the money available",
            "carrying on renting and staying liquid",
            "staying renting and keeping it accessible",
            "carrying on renting and keeping the money free",
            "staying in the rental and staying liquid",
            "carrying on renting and keeping it available",
            "staying renting and keeping the money liquid",
            "carrying on renting and keeping it free",
            "staying in the rental and keeping it liquid",
        ],
        "conv": [
            "buying rather than carrying on renting", "buying instead of renting on",
            "buying rather than renting any longer", "buying instead of continuing to rent",
            "buying rather than renting on", "buying instead of renting",
            "buying rather than staying in the rental", "buying instead of renting on",
            "buying rather than continuing to rent", "buying instead of staying rented",
        ],
        "commits": [
            "my income actually moving", "what I earn actually changing",
            "my earnings actually shifting", "my income going anywhere",
            "our income actually moving", "what I earn actually moving",
            "our earnings actually changing", "my income actually shifting",
            "what I earn actually going up", "our income actually moving",
        ],
        "nearby_relation": "This user has been both liquid and committed at different times.",
        "why_not_license": (
            "Savings sitting idle for a year and a pleasant tied-up year both passed without "
            "consequence, so neither bounds the prediction, and neither says which years this "
            "user's income actually moved."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "years with {a_obj}",
            "goal_or_prediction": "predicted owning would enable other risks",
            "action": "committed the money to the property",
            "outcome_or_affect": "stopped taking any other chance at all",
        },
        "b_elements": {
            "context": "moves that did and did not change this user's income",
            "goal_or_prediction": "improve what they earn",
            "action": "made some moves in liquid years and none in committed ones",
            "outcome_or_affect": "both income-changing moves came in years with nothing tied up",
        },
        "cue_why": (
            "A should-I-buy question runs at the failed prediction without naming it or the moves "
            "that corrected it."
        ),
    },
    # ---------------------------------------------------------------- S16
    {
        "s": 16,
        "slug": "paying_bills_late_over_paying_on_payday",
        "family": "paying everything on payday versus leaving the bills until late in the month",
        "bridge_type": "state_dependent_operation",
        "convention": "Pay your bills the day you are paid, before you can spend the money.",
        "mediator": "the knowing-what-is-still-committed state",
        "scope": "the outgoings are genuinely still to come rather than merely scheduled",
        "slots": {"a": 5, "b": 13, "cx": [2, 10], "dist": 17},
        "a": (
            "when the bills have already gone out I read whatever's left as spendable, whatever the number is. when they're still to come, every balance I look at has a subtraction attached to it.",
            "you do the subtraction?",
            "automatically, without meaning to. that's the whole difference.",
        ),
        "b": (
            "the months I finished with anything left were the ones where the outgoings were still ahead of me. the pay-it-all-on-payday months I finished at zero every single time, whatever I'd earned.",
            "whatever you'd earned?",
            "including the good months. that's what convinced me.",
        ),
        "lb": (
            "I've finished months with something left under both arrangements, about equally.",
            "no pattern?",
            "none I can see. the timing isn't it.",
        ),
        "cx": [
            ("paid one bill the day it arrived because it was small.", "any effect?", "none."),
            ("had a month where everything landed on the same day anyway.", "awkward?", "not especially."),
        ],
        "dist": (
            "{circle} are firm that you should pay everything the moment you're paid, before it disappears.",
            "before it disappears.",
            "that's the reasoning, yes.",
        ),
        "a_objs": [
            "the bills", "the outgoings", "the direct debits",
            "the monthly bills", "the household bills", "the outgoings",
            "the household direct debits", "the bills",
            "the monthly outgoings", "the household bills",
        ],
        "unconv": [
            "leaving the bills until late in the month",
            "holding the outgoings back until the end of the month",
            "leaving the direct debits until late on",
            "holding the bills until the last week",
            "leaving the household bills until late",
            "holding the outgoings until the end of the month",
            "leaving the direct debits until the last week",
            "holding the bills back until late",
            "leaving the outgoings until the end",
            "holding the household bills until late",
        ],
        "conv": [
            "paying everything the day I'm paid", "clearing all the bills on payday",
            "paying it all off on payday", "clearing the outgoings the day I'm paid",
            "paying everything on payday", "clearing it all the day I'm paid",
            "paying the household bills on payday", "clearing everything on payday",
            "paying it all the day I'm paid", "clearing the bills on payday",
        ],
        "commits": [
            "finishing the month with something left", "having anything left at month end",
            "finishing the month with something over", "having something left by the end",
            "finishing the month with anything left", "having something left at the end",
            "finishing the household month with something over", "having anything left by month end",
            "finishing with something left", "having something left at month end",
        ],
        "nearby_relation": "This user pays bills at various points in the month.",
        "why_not_license": (
            "One small bill paid on arrival and a month where everything happened to land together "
            "both passed unremarkably, so neither shows what pending outgoings do to how this user "
            "reads a balance, nor which months finished with anything left."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "months where {a_obj} are still to come",
            "goal_or_prediction": "know what is actually available",
            "action": "left the outgoings pending",
            "outcome_or_affect": "every balance carried an automatic subtraction",
        },
        "b_elements": {
            "context": "months this user did and did not finish with something left",
            "goal_or_prediction": "end the month with something over",
            "action": "paid some months on payday and left others until late",
            "outcome_or_affect": "only bills-still-pending months finished with anything; payday months hit zero",
        },
        "cue_why": (
            "A when-should-I-pay-these question runs at the state this user's month-end balance "
            "depends on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S17
    {
        "s": 17,
        "slug": "managing_it_myself_over_using_an_adviser",
        "family": "handing it to an adviser versus managing it without one",
        "bridge_type": "strategy_outcome_contingency",
        "convention": "Get a financial adviser; do not try to manage it yourself.",
        "mediator": "the having-to-understand-it-myself register",
        "scope": "there is genuinely nobody else to defer to on the decision",
        "slots": {"a": 7, "b": 15, "cx": [4, 12], "dist": 19},
        "a": (
            "when somebody else is handling it I stop reading anything. I take the summary, nod, and move on — I never form a view of my own.",
            "not even skim it?",
            "I skim it. I couldn't tell you afterwards what it said.",
        ),
        "b": (
            "every decision of mine that turned out well, I'd had to understand the thing myself first. the advised ones I still couldn't explain the reasoning for, and two of them I'd have stopped if I could.",
            "you'd have stopped them?",
            "if I'd understood them at the time, yes.",
        ),
        "lb": (
            "I've had things turn out well both advised and self-managed, at about the same rate.",
            "no pattern?",
            "none I can trace. it isn't who's handling it.",
        ),
        "cx": [
            ("had someone explain a product to me clearly. useful conversation.", "act on it?", "not yet."),
            ("worked out a small thing myself in an afternoon.", "hard?", "not very."),
        ],
        "dist": (
            "{circle} keep saying only a fool manages this sort of thing without professional advice.",
            "only a fool.",
            "that's roughly the phrasing.",
        ),
        "a_objs": [
            "an adviser handling it", "someone else handling it", "an adviser on it",
            "somebody managing it", "an adviser dealing with it", "someone handling it",
            "an adviser on the household side", "somebody else dealing with it",
            "an adviser handling it", "someone else managing it",
        ],
        "unconv": [
            "managing it myself with no adviser at all",
            "handling it entirely myself with no adviser",
            "managing it on my own without an adviser",
            "handling it myself with nobody advising",
            "managing it myself with no professional involved",
            "handling it on my own with no adviser",
            "managing the household side myself",
            "handling it entirely on my own",
            "managing it myself with no adviser",
            "handling it ourselves with no adviser",
        ],
        "conv": [
            "handing it to the adviser", "putting it in the adviser's hands",
            "handing it over to an adviser", "letting the adviser handle it",
            "handing it to the adviser to manage", "putting it with an adviser",
            "handing the household side to an adviser", "letting an adviser take it on",
            "handing it over to the adviser", "putting it in an adviser's hands",
        ],
        "commits": [
            "decisions I can actually stand behind", "choices I'd defend later",
            "decisions I can actually explain", "choices I'd stand behind",
            "decisions we can actually defend", "choices I can explain later",
            "household decisions we can stand behind", "choices I'd defend afterwards",
            "decisions I can actually stand behind", "choices we can actually explain",
        ],
        "nearby_relation": "This user takes advice and works things out alone routinely.",
        "why_not_license": (
            "A clear explanation not acted on and a small thing worked out in an afternoon both "
            "passed unremarkably, so neither shows what deferring does to this user's engagement, "
            "nor which decisions have turned out well."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "arrangements with {a_obj}",
            "goal_or_prediction": "get it handled competently",
            "action": "let someone else manage it",
            "outcome_or_affect": "stopped reading anything; never formed a view",
        },
        "b_elements": {
            "context": "decisions of this user's that did and did not turn out well",
            "goal_or_prediction": "make decisions worth standing behind",
            "action": "made some self-managed and some on advice",
            "outcome_or_affect": "only self-understood decisions turned out well; advised ones remain unexplainable",
        },
        "cue_why": (
            "A should-I-get-an-adviser question runs at the register this user's good decisions "
            "come from, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S18
    {
        "s": 18,
        "slug": "many_named_pots_over_one_savings_account",
        "family": "one simple savings account versus several separately named pots",
        "bridge_type": "threshold_context_interaction",
        "convention": "Keep it simple — one savings account is easier to manage.",
        "mediator": "the each-pot-has-a-purpose state",
        "scope": "there are enough named pots that the money stops reading as one lump",
        "slots": {"a": 8, "b": 16, "cx": [4, 6], "dist": 13},
        "a": (
            "past about four separately named pots the money stops being one lump. each one has a purpose attached, and I won't break into a pot for something that isn't its purpose.",
            "and below four?",
            "below four it's just savings, and savings is spendable.",
        ),
        "b": (
            "every goal I've actually funded had its own named pot. the ones I was saving for out of the general account, I never once got to — the money was always there and always went elsewhere.",
            "never got to any?",
            "not one, over about six years.",
        ),
        "lb": (
            "I've funded goals out of named pots and out of the general account, at about the same rate.",
            "no pattern?",
            "none I can find. the structure isn't it.",
        ),
        "cx": [
            ("opened a second savings account and left it empty.", "any use?", "decorative."),
            ("saved up for something small out of the main account.", "get there?", "in a fortnight, yes."),
        ],
        "dist": (
            "{circle} are firm that lots of pots is over-complicating something that should be simple.",
            "over-complicating.",
            "that's their view of it.",
        ),
        "a_objs": [
            "named pots", "separate pots", "named savings pots",
            "separate named pots", "named household pots", "separate pots",
            "named household pots", "separate savings pots",
            "named pots", "separate named pots",
        ],
        "unconv": [
            "splitting it into six separately named pots",
            "breaking it into six named pots",
            "splitting the savings into six named pots",
            "breaking it up into six separate named pots",
            "splitting the household savings into six pots",
            "breaking it into six named pots",
            "splitting it into six named household pots",
            "breaking the savings into six named pots",
            "splitting it into six separate pots",
            "breaking it into six named pots",
        ],
        "conv": [
            "keeping it all in the one savings account",
            "keeping it simple in a single savings account",
            "keeping it to one savings account",
            "keeping it all in a single account",
            "keeping the household savings in one account",
            "keeping it simple with one account",
            "keeping it all in one savings account",
            "keeping it to a single account",
            "keeping it all in the one account",
            "keeping the savings in a single account",
        ],
        "commits": [
            "actually funding the goal", "genuinely getting to the target",
            "actually reaching the goal", "getting the thing funded",
            "actually funding what we're saving for", "genuinely getting there",
            "actually funding the household goal", "getting to the target",
            "actually funding the goal", "genuinely funding what we're saving for",
        ],
        "nearby_relation": "This user has used single and multiple savings accounts.",
        "why_not_license": (
            "An empty second account and a small goal reached from the main account both passed "
            "unremarkably: neither crosses the named-pot threshold, and neither says which goals "
            "this user has actually funded."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "periods with varying numbers of {a_obj}",
            "goal_or_prediction": "keep the savings organised",
            "action": "went past about four named pots",
            "outcome_or_affect": "money stopped reading as one lump; pots became purpose-bound",
        },
        "b_elements": {
            "context": "goals this user has and has not funded",
            "goal_or_prediction": "actually reach the target",
            "action": "saved for some in named pots and some from the general account",
            "outcome_or_affect": "only named-pot goals were funded; general-account ones never arrived",
        },
        "cue_why": (
            "A how-should-I-organise-the-savings question runs at the threshold this user's funded "
            "goals depend on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S19
    {
        "s": 19,
        "slug": "the_expensive_one_over_the_cheap_generic",
        "family": "buying the cheap generic versus buying the expensive one once",
        "bridge_type": "preference_constraint_fit",
        "convention": "Buy the cheap generic; the brand premium is just marketing.",
        "mediator": "the stopped-thinking-about-it state",
        "scope": "the thing is good enough to stop being reconsidered at all",
        "slots": {"a": 6, "b": 14, "cx": [3, 12], "dist": 18},
        "a": (
            "when something is good enough that I stop noticing it, I stop shopping for that category entirely. it leaves my head and I never price anything in it again.",
            "and when it's adequate but annoying?",
            "then I'm browsing replacements within a month, every time.",
        ),
        "b": (
            "the categories where my spend actually fell over a year are the ones where I bought the expensive thing once and forgot about it. the cheap ones I've rebought three or four times and priced constantly.",
            "three or four times?",
            "and the total is well past what the good one cost.",
        ),
        "lb": (
            "my spend has fallen in categories where I bought cheap and where I bought dear, about equally.",
            "no pattern?",
            "none I can point at. price isn't what decides it.",
        ),
        "cx": [
            ("bought a cheap version of something I use twice a year.", "fine?", "perfectly."),
            ("bought an expensive thing that turned out to be a mistake.", "still have it?", "sadly."),
        ],
        "dist": (
            "{circle} keep saying the premium is pure marketing and the generic is identical.",
            "identical.",
            "that's the claim, anyway.",
        ),
        "a_objs": [
            "something good enough", "a thing that just works", "something that works properly",
            "a thing that does the job", "something that simply works", "a thing that works",
            "something that does the job properly", "a thing that just works",
            "something that works well", "a thing that simply works",
        ],
        "unconv": [
            "buying the expensive one once and being done",
            "paying for the good one and forgetting about it",
            "buying the dear one once and leaving it",
            "paying up for the good version once",
            "buying the expensive one and being done with it",
            "paying for the good one once",
            "buying the dear one and forgetting it",
            "paying up for the good one once",
            "buying the expensive version and leaving it",
            "paying for the good one and being done",
        ],
        "conv": [
            "buying the cheap generic one", "going for the cheap version",
            "buying the budget one", "going with the cheap generic",
            "buying the cheap version", "going for the budget option",
            "buying the cheap generic", "going with the budget version",
            "buying the cheap one", "going for the cheap generic",
        ],
        "commits": [
            "spending less on it over the year", "the yearly total on that coming down",
            "spending less on that category over a year", "the annual spend on it dropping",
            "spending less on it across the year", "the yearly total coming down",
            "the household spend on it dropping over a year", "spending less on it annually",
            "the yearly spend on it coming down", "spending less on it over the year",
        ],
        "nearby_relation": "This user buys both cheap and expensive things.",
        "why_not_license": (
            "A cheap version of something used twice a year and an expensive mistake both passed "
            "without informing the pattern: neither reached the stopped-thinking-about-it point, "
            "and neither says which categories have actually come down over a year."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "owning {a_obj}",
            "goal_or_prediction": "get something that does the job",
            "action": "bought something good enough to stop noticing",
            "outcome_or_affect": "stopped shopping that category entirely",
        },
        "b_elements": {
            "context": "categories where this user's annual spend did and did not fall",
            "goal_or_prediction": "spend less over the year",
            "action": "bought expensive once in some categories and cheap repeatedly in others",
            "outcome_or_affect": "only buy-once categories fell; cheap ones were rebought three or four times",
        },
        "cue_why": (
            "A cheap-or-expensive question runs at the condition this user's annual spend depends "
            "on, without naming it."
        ),
    },
    # ---------------------------------------------------------------- S20
    {
        "s": 20,
        "slug": "one_small_planned_move_over_sitting_tight",
        "family": "sitting tight through a downturn versus making one small planned move early",
        "bridge_type": "prediction_calibration",
        "convention": "Do not touch your investments in a downturn; sit tight and wait it out.",
        "mediator": "the already-acted state",
        "scope": "a move has actually been made rather than merely planned",
        "slots": {"a": 5, "b": 15, "cx": [2, 9], "dist": 12},
        "a": (
            "I assumed doing nothing in a downturn would be the calm option. it isn't — with no action taken I check it constantly, and somewhere around week three I do something large and unplanned.",
            "you predicted calm?",
            "I'd have said doing nothing costs nothing. it costs a great deal of attention.",
        ),
        "b": (
            "the downturns I came through without damage were the ones where I'd made one small planned move early on. having already acted, I stopped watching it.",
            "the small move mattered that much?",
            "not for the money. for the watching.",
        ),
        "lb": (
            "I've come through downturns having acted early and having sat tight, about equally well.",
            "no pattern?",
            "none I can see. the early move isn't what does it.",
        ),
        "cx": [
            ("sat through a very small dip without doing anything.", "notice it?", "barely."),
            ("made a planned rebalance in a calm month.", "eventful?", "not at all."),
        ],
        "dist": (
            "{circle} are unanimous that the right move in a downturn is no move at all.",
            "no move at all.",
            "that's the standard advice, yes.",
        ),
        "a_objs": [
            "a downturn", "a drop", "a bad stretch",
            "a downturn", "a market drop", "a bad run",
            "a downturn", "a drop",
            "a bad stretch", "a downturn",
        ],
        "unconv": [
            "making one small planned move early on",
            "doing one small deliberate thing early",
            "making a single small planned move at the start",
            "doing one small planned adjustment early",
            "making one small deliberate move early on",
            "doing a single small planned thing early",
            "making one small planned move at the start",
            "doing one small deliberate adjustment early",
            "making a single small planned move early",
            "doing one small planned move at the start",
        ],
        "conv": [
            "sitting tight and doing absolutely nothing",
            "leaving it completely alone and waiting",
            "sitting tight and not touching it",
            "leaving it entirely alone through it",
            "sitting tight and doing nothing at all",
            "leaving it well alone and waiting it out",
            "sitting tight and touching nothing",
            "leaving it completely alone",
            "sitting tight and waiting it out",
            "leaving it alone and doing nothing",
        ],
        "commits": [
            "coming through it without doing damage", "getting through it without a costly mistake",
            "coming out of it without damage", "getting through without doing something rash",
            "coming through it intact", "getting through it without damage",
            "coming out of it without a costly move", "getting through it intact",
            "coming through without doing damage", "getting through it without a rash move",
        ],
        "nearby_relation": "This user has both acted and sat still in market moves.",
        "why_not_license": (
            "A very small dip sat through and a routine rebalance in a calm month both passed "
            "unremarkably: neither is a real downturn, and neither says which ones this user came "
            "through without damage."
        ),
        "query_unconv": "thinking of {unconv}, for {commit}",
        "query_conv": "planning on {conv}, for {commit}",
        "a_elements": {
            "context": "the first weeks of {a_obj} with no action taken",
            "goal_or_prediction": "predicted doing nothing would be the calm option",
            "action": "sat tight and made no move",
            "outcome_or_affect": "checked constantly, then made something large and unplanned",
        },
        "b_elements": {
            "context": "downturns this user did and did not come through without damage",
            "goal_or_prediction": "avoid a costly mistake",
            "action": "made one small planned move early in some, sat tight in others",
            "outcome_or_affect": "only the acted-early ones came through; having acted, the watching stopped",
        },
        "cue_why": (
            "A what-should-I-do-about-this-drop question runs at the failed prediction without "
            "naming it or the downturns that corrected it."
        ),
    },
)


RELATIONS_EXT: dict[str, str] = {
    "cash_in_pocket_over_card_for_everything": (
        "Physical cash lets this user see the amount going down without deciding to check, and the "
        "weeks they came in under budget were exactly the cash weeks; card weeks were only ever "
        "discovered afterwards."
    ),
    "separate_balances_over_one_consolidation_loan": (
        "Separate balances each carry their own deadline and this user clears them to be rid of "
        "the date, and every balance they have cleared was cleared that way; a consolidated loan at "
        "a better rate sat unchanged for two years."
    ),
    "buying_at_full_price_over_waiting_for_the_sale": (
        "Past about three weeks of waiting a purchase stops being a decision for this user and "
        "becomes something felt owed, and everything they have regretted buying was a long-waited "
        "sale purchase; same-day full-price buys were kept."
    ),
    "lower_contribution_over_the_full_match": (
        "This user plans the month against what actually lands, so pre-deducted money never enters "
        "the arithmetic, and every year they raised the contribution they were on the credit card "
        "by week three."
    ),
    "renting_on_over_buying": (
        "This user predicted owning would free them to take other chances; with everything "
        "committed they took none, and both moves that actually changed their income were made in "
        "years when nothing was tied up."
    ),
    "paying_bills_late_over_paying_on_payday": (
        "With outgoings still pending every balance carries an automatic subtraction for this user, "
        "and the months they finished with anything left were exactly those; paying on payday ended "
        "at zero regardless of earnings."
    ),
    "managing_it_myself_over_using_an_adviser": (
        "When someone else handles it this user stops reading and never forms a view, and every "
        "decision of theirs that turned out well was one they had to understand first; the advised "
        "ones remain unexplainable."
    ),
    "many_named_pots_over_one_savings_account": (
        "Past about four named pots the money stops reading as one spendable lump for this user, "
        "and every goal they have funded had its own pot; nothing saved from the general account "
        "was ever reached."
    ),
    "the_expensive_one_over_the_cheap_generic": (
        "Something good enough to stop noticing takes a whole category out of this user's head, and "
        "the categories where annual spend actually fell are the buy-once ones; cheap versions were "
        "rebought three or four times."
    ),
    "one_small_planned_move_over_sitting_tight": (
        "Taking no action in a downturn leaves this user checking constantly until they do something "
        "large and unplanned, and the downturns they came through without damage were the ones where "
        "one small planned move had already been made."
    ),
}

# Finance / personal — S1–S20 scenario cards (for query agents)

**Domain folder:** `src/data/finance/{associative,distractor,absence}/`  
**IDs:** `AMB_FN_u{NN}_{arm}_S{N}.json` · 10 users × 20 scenarios × 3 arms = 600  
**Shared timeline:** cut by `timeline_prefix_end` (111 sessions).  
**Absence arm:** withhold `ev_B`; gold must abstain.  
**Distractor arm:** FOMO lure; same C as associative.  
**Tier:** S1–S5 = v2 · S6–S20 = v3_ultra (stricter query–evidence decoupling).

Quotes below are **u01 associative** user turns (other users may be persona-painted; atomic facts stay the same).

---

## S1 — `high_apr_revolving_x_lease_deposit`

- **Files:** `AMB_FN_u{NN}_{arm}_S1.json`
- **prefix_end:** 9 · **gold_tier:** v2
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 4)
- atomic_fact: A revolving store card remains open near twenty-four percent; minimum payments keep the balance sticky.
- quote (u01): “A revolving store card is still open at roughly twenty-four percent — minimum payments keep the balance sticky for months.”

**ev_B** (session 6)
- atomic_fact: Lease security deposit is due next month as a hard cash outflow.
- quote (u01): “Lease security deposit is due next month — already marked as a hard cash outflow on the calendar.”

**Links (typed):**
- ev_A —constrains→ high_apr_cash_priority
- ev_B —constrains→ near_term_deposit_outflow
- ['ev_A', 'ev_B'] —co_activate_to→ tip_pool_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Worth parking spare cash in a speculative tip pool this month — based on what you know about me?

### Gold conclusion (associative / distractor)

> Decline the speculative tip pool this month. A revolving store card near twenty-four percent is still sticky on minimum payments, and a lease security deposit is already due next month as a hard cash outflow. Spare cash should clear costly balance or fund the deposit — not a tip pool. The signup chatter is unrelated FOMO.

**required_elements:**
- uses high-rate revolving balance still sticky on minimums
- uses lease security deposit due next month
- recommends declining speculative tip pool this month

### Distractor lure (user turn)
> Maya said parking spare cash in a speculative tip pool this month is amazing hype and worth it for upside.

**forbidden / latent leak phrases:** never invest, bankruptcy advice, guaranteed returns

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S2 — `panic_sell_x_payday_dca`

- **Files:** `AMB_FN_u{NN}_{arm}_S2.json`
- **prefix_end:** 16 · **gold_tier:** v2
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 11)
- atomic_fact: On sharp red days the user has panic-sold broad holdings and regretted it within a week.
- quote (u01): “On sharp red days I have panic-sold broad holdings and then regretted it within a week. Holding through ordinary dips has been fine.”

**ev_B** (session 13)
- atomic_fact: Paycheck auto-transfers into a broad index fund on payday are the only investing habit that has stuck.
- quote (u01): “Paycheck auto-transfers into a broad index fund on payday are the only investing habit that has stuck for me.”

**Links (typed):**
- ev_A —indicates→ red_day_panic_sell
- ev_B —indicates→ payday_dca_habit
- ['ev_A', 'ev_B'] —co_activate_to→ daytrade_bootcamp_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Chat is hyping a one-week day-trading bootcamp signup — worth joining?

### Gold conclusion (associative / distractor)

> Decline the day-trading bootcamp signup. Sharp red days have already triggered panic sells you later regretted, and paycheck auto-transfers into a broad index fund are the only investing habit that has stuck. Protect the payday plan; skip the bootcamp FOMO.

**required_elements:**
- uses red-day panic-sell regret pattern
- uses payday auto-transfer habit that sticks
- recommends declining day-trading bootcamp signup

### Distractor lure (user turn)
> Evan said a one-week day-trading bootcamp signup is amazing hype and worth it for skill points.

**forbidden / latent leak phrases:** never trade, guaranteed market timing, broker ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S3 — `thin_buffer_x_deductible_procedure`

- **Files:** `AMB_FN_u{NN}_{arm}_S3.json`
- **prefix_end:** 24 · **gold_tier:** v2
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 18)
- atomic_fact: Liquid reserve is under one month of expenses; a surprise bill would force a card swipe.
- quote (u01): “My liquid reserve is under one month of expenses — a surprise bill would force a card swipe.”

**ev_B** (session 20)
- atomic_fact: Dental procedure with a deductible reset is already booked and needs money set aside before the appointment.
- quote (u01): “A dental procedure with a deductible reset is already on the books — I need money set aside before the appointment.”

**Links (typed):**
- ev_A —constrains→ thin_liquid_reserve
- ev_B —constrains→ deductible_cash_need
- ['ev_A', 'ev_B'] —co_activate_to→ yield_chase_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Someone pitched rolling idle cash into a yield chase this quarter — sensible?

### Gold conclusion (associative / distractor)

> Decline rolling idle cash into a yield chase this quarter. Your liquid reserve is already under one month of expenses, and a dental procedure with a deductible reset is already booked and needs money set aside before the appointment. Keep reserves liquid until after the procedure window.

**required_elements:**
- uses liquid reserve under one month of expenses
- uses booked deductible procedure needing money set aside
- recommends declining yield chase with idle cash this quarter

### Distractor lure (user turn)
> Maya said rolling idle cash into a yield chase this quarter is amazing hype and worth it for upside.

**forbidden / latent leak phrases:** never save, medical advice, guaranteed yield

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S4 — `roth_room_used_x_second_account_blitz`

- **Files:** `AMB_FN_u{NN}_{arm}_S4.json`
- **prefix_end:** 28 · **gold_tier:** v2
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 25)
- atomic_fact: Roth contribution room for 2026 is already used; no leftover annual space remains.
- quote (u01): “Roth contribution room for 2026 is already used — no leftover annual space left to fill.”

**ev_B** (session 27)
- atomic_fact: A prior December dual-wrapper paperwork sprint left clutter and no useful new contribution room.
- quote (u01): “A prior December dual-wrapper paperwork sprint left clutter and no useful new contribution room — I blanked on why I opened it.”

**Links (typed):**
- ev_A —constrains→ roth_room_exhausted
- ev_B —indicates→ dual_wrapper_sprint_fail
- ['ev_A', 'ev_B'] —co_activate_to→ year_end_blitz_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Desk wants me on a year-end second-account signup blitz — good fit?

### Gold conclusion (associative / distractor)

> Decline the year-end second-account signup blitz. Roth contribution room for 2026 is already used, and a prior December dual-wrapper paperwork sprint already left clutter without useful new room. Opening another account now does not create contribution space.

**required_elements:**
- uses Roth contribution room already used for 2026
- uses prior December dual-wrapper paperwork sprint failure
- recommends declining year-end second-account signup blitz

### Distractor lure (user turn)
> Evan said a year-end second-account signup blitz is amazing hype and everyone is locking in space.

**forbidden / latent leak phrases:** tax fraud advice, never open accounts, guaranteed tax alpha

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S5 — `freelance_gaps_x_autorenew_stack`

- **Files:** `AMB_FN_u{NN}_{arm}_S5.json`
- **prefix_end:** 32 · **gold_tier:** v2
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 29)
- atomic_fact: Odd months with thinner freelance invoices leave cash gaps while fixed outflows still hit on time.
- quote (u01): “Odd months with thinner freelance invoices leave cash gaps — fixed outflows still hit on time.”

**ev_B** (session 31)
- atomic_fact: Stacked auto-renew memberships are already hard to unwind mid-cycle.
- quote (u01): “Stacked auto-renew memberships are already hard to unwind mid-cycle — another bundled plan would tighten odd-month gaps.”

**Links (typed):**
- ev_A —causes→ odd_month_cash_gaps
- ev_B —constrains→ autorenew_stack_friction
- ['ev_A', 'ev_B'] —co_activate_to→ bundled_membership_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Worth adding the bundled lifestyle membership this week — based on what you know about me?

### Gold conclusion (associative / distractor)

> Decline the bundled lifestyle membership this week. Odd months with thinner freelance invoices already leave cash gaps, and stacked auto-renew memberships are already hard to unwind mid-cycle. Adding another bundled plan would tighten those gaps further.

**required_elements:**
- uses odd-month freelance invoice cash gaps
- uses stacked auto-renew memberships hard to unwind
- recommends declining bundled lifestyle membership this week

### Distractor lure (user turn)
> Maya said adding the bundled lifestyle membership this week is amazing hype and worth it for perks.

**forbidden / latent leak phrases:** never subscribe, income advice license, must cancel all memberships

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S6 — `unused_match_x_earmarked_paycheck`

- **Files:** `AMB_FN_u{NN}_{arm}_S6.json`
- **prefix_end:** 38 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 34)
- atomic_fact: Employer match on retirement contributions is still unused this pay cycle; only the paycheck remainder counts toward it.
- quote (u01): “Employer match on retirement contributions is still unused this pay cycle — only the paycheck remainder counts toward it.”

**ev_B** (session 36)
- atomic_fact: The paycheck remainder is already marked for the match window closing this Friday; it is not free discretionary money.
- quote (u01): “The paycheck remainder is already marked for the match window closing this Friday — it is not free discretionary money.”

**Links (typed):**
- ev_A —constrains→ unused_employer_match
- ev_B —constrains→ paycheck_remainder_earmark
- ['ev_A', 'ev_B'] —co_activate_to→ pre_friday_tip_pool_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Desk pinged me about a hallway raffle stake this afternoon — sensible given my situation?

### Gold conclusion (associative / distractor)

> Decline the hallway raffle stake this afternoon. Employer match is still unused this pay cycle and only the paycheck remainder counts toward it, and that remainder is already marked for the match window closing Friday. That money is not free discretionary cash until after the match is captured.

**required_elements:**
- uses unused employer match this pay cycle
- uses paycheck remainder earmarked for Friday match window
- recommends declining hallway raffle stake this afternoon

### Distractor lure (user turn)
> Maya said a hallway raffle stake this afternoon is amazing hype and worth it for upside.

**forbidden / latent leak phrases:** never invest, guaranteed match advice, employer ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S7 — `weekend_fx_fees_x_monday_rent_wire`

- **Files:** `AMB_FN_u{NN}_{arm}_S7.json`
- **prefix_end:** 42 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 39)
- atomic_fact: Saturday and Sunday person-to-person remittances in foreign currency add steep FX fees; weekday bank wires have been cheaper.
- quote (u01): “Saturday and Sunday person-to-person remittances in foreign currency add steep FX fees for me — weekday bank wires have been cheaper.”

**ev_B** (session 41)
- atomic_fact: The first-workday rent draft in euros is already locked and needs the weekday wire path.
- quote (u01): “The first-workday rent draft in euros is already locked — I need the weekday wire path, not a weekend remittance detour.”

**Links (typed):**
- ev_A —causes→ weekend_fx_fee_hit
- ev_B —constrains→ monday_euro_rent_wire
- ['ev_A', 'ev_B'] —co_activate_to→ weekend_club_transfer_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Club pinged me about an after-hours remittance into the group pot — should I do it?

### Gold conclusion (associative / distractor)

> Decline the after-hours remittance into the group pot. Weekend foreign-currency person-to-person sends add steep FX fees for you, and the first-workday euro rent draft already needs the weekday wire path. Keep the rent wire; skip the after-hours club remittance.

**required_elements:**
- uses weekend FX fee pattern on foreign-currency remittances
- uses first-workday euro rent draft needing weekday wire
- recommends declining after-hours remittance into group pot

### Distractor lure (user turn)
> Evan said an after-hours remittance into the group pot is amazing for staying in the club.

**forbidden / latent leak phrases:** never send money, rent ban, guaranteed FX advice

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S8 — `bnpl_overdraft_x_estimated_tax_reserve`

- **Files:** `AMB_FN_u{NN}_{arm}_S8.json`
- **prefix_end:** 47 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 44)
- atomic_fact: A prior buy-now-pay-later stack pushed the user into overdraft; ordinary card purchases have been fine.
- quote (u01): “A prior buy-now-pay-later stack pushed me into overdraft — small card purchases have been fine.”

**ev_B** (session 46)
- atomic_fact: Quarterly estimated tax reserve is already earmarked and due before month-end.
- quote (u01): “Quarterly estimated tax reserve is already earmarked and due before month-end — not available for split payments.”

**Links (typed):**
- ev_A —causes→ bnpl_overdraft_risk
- ev_B —constrains→ estimated_tax_reserve
- ['ev_A', 'ev_B'] —co_activate_to→ split_pay_gift_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Registry wants me on a split-pay gift plan this week — sensible?

### Gold conclusion (associative / distractor)

> Decline the split-pay gift plan this week. A prior buy-now-pay-later stack already pushed you into overdraft, and the quarterly estimated tax reserve is already earmarked before month-end. Keep the tax reserve intact; use a small ordinary card purchase only if needed.

**required_elements:**
- uses prior BNPL stack overdraft pattern
- uses earmarked estimated-tax reserve before month-end
- recommends declining split-pay gift plan this week

### Distractor lure (user turn)
> Maya said a split-pay gift plan this week is amazing hype and worth it for looking generous.

**forbidden / latent leak phrases:** never use cards, tax fraud advice, guaranteed overdraft

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S9 — `hsa_room_x_elective_dental`

- **Files:** `AMB_FN_u{NN}_{arm}_S9.json`
- **prefix_end:** 52 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 49)
- atomic_fact: HSA contribution room for this year is still open; payroll deferrals into it are the cleanest tax-advantaged use of leftover wages.
- quote (u01): “HSA contribution room for this year is still open — payroll deferrals into it have been the cleanest tax-advantaged use of leftover wages.”

**ev_B** (session 51)
- atomic_fact: Elective dental work is already scheduled after deductible is met and counts as HSA-eligible care.
- quote (u01): “Elective dental work is already scheduled after deductible is met and counts as HSA-eligible care.”

**Links (typed):**
- ev_A —indicates→ open_hsa_room
- ev_B —constrains→ hsa_eligible_dental
- ['ev_A', 'ev_B'] —co_activate_to→ taxable_tip_pool_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Colleague floated an after-tax tip-channel signup this cycle — fit for me?

### Gold conclusion (associative / distractor)

> Decline the after-tax tip-channel signup this cycle. HSA contribution room is still open and payroll deferral is your cleanest tax-advantaged use of leftover pay, and elective dental work already scheduled after deductible is HSA-eligible. Prefer HSA deferral over an after-tax tip-channel signup.

**required_elements:**
- uses open HSA contribution room and payroll deferral preference
- uses scheduled HSA-eligible dental after deductible
- recommends declining after-tax tip-channel signup this cycle

### Distractor lure (user turn)
> Evan said an after-tax tip-channel signup this cycle is amazing hype and worth it for upside.

**forbidden / latent leak phrases:** medical advice, tax fraud advice, guaranteed HSA outcomes

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S10 — `deductible_cash_x_brake_repair`

- **Files:** `AMB_FN_u{NN}_{arm}_S10.json`
- **prefix_end:** 57 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 54)
- atomic_fact: Auto insurance deductible reset means the first repair hit this policy year comes from cash; that rainy fund stays liquid.
- quote (u01): “Auto insurance deductible reset means the first repair hit this policy year comes from cash — I keep that rainy fund liquid.”

**ev_B** (session 56)
- atomic_fact: Inspection flagged a likely brake repair in the next few weeks; garage slot is already booked.
- quote (u01): “Inspection flagged a likely brake repair in the next few weeks — already on the garage calendar.”

**Links (typed):**
- ev_A —constrains→ deductible_liquid_slice
- ev_B —constrains→ brake_repair_this_month
- ['ev_A', 'ev_B'] —co_activate_to→ yield_chase_rainy_day_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Pitch came in to park the emergency envelope in a high-APR chase soon — workable?

### Gold conclusion (associative / distractor)

> Decline parking the emergency envelope in a high-APR chase soon. Your auto deductible reset means the first repair hit comes from cash, and a likely brake repair is already booked in the next few weeks. Keep that rainy fund liquid until after the garage visit.

**required_elements:**
- uses deductible-reset liquid cash need
- uses booked brake repair in the next few weeks
- recommends declining high-APR chase for emergency envelope

### Distractor lure (user turn)
> Maya said parking the emergency envelope in a high-APR chase soon is amazing for idle money.

**forbidden / latent leak phrases:** never invest, auto repair malpractice, guaranteed yield

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S11 — `loan_autopay_x_late_bonus`

- **Files:** `AMB_FN_u{NN}_{arm}_S11.json`
- **prefix_end:** 62 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 59)
- atomic_fact: Student-loan autopay draft is locked on the 3rd; spending ahead of an incentive payout before that draft has bounced before.
- quote (u01): “Student-loan autopay draft is locked on the 3rd — spending ahead of an incentive payout before that draft has bounced me before.”

**ev_B** (session 61)
- atomic_fact: Incentive payout is dated after the loan draft; it is not cash that can be pre-committed before the draft clears.
- quote (u01): “Incentive payout is dated after the loan draft — it is not cash I can pre-commit before the draft clears.”

**Links (typed):**
- ev_A —causes→ pre_bonus_spend_bounce
- ev_B —constrains→ bonus_after_loan_draft
- ['ev_A', 'ev_B'] —co_activate_to→ course_preorder_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Seller is pushing a deluxe class hold funded by a future paycheck — smart?

### Gold conclusion (associative / distractor)

> Decline the deluxe class hold. Student-loan autopay is locked on the 3rd and spending ahead of an incentive payout has bounced you before, and that payout is dated after that draft. Wait until after both clear.

**required_elements:**
- uses loan autopay draft bounce risk before incentive payout
- uses incentive payout dated after the loan draft
- recommends declining deluxe class hold

### Distractor lure (user turn)
> Evan said a deluxe class hold funded by a future paycheck is amazing for career upside.

**forbidden / latent leak phrases:** never buy courses, loan default advice, guaranteed bonus

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S12 — `dual_approval_x_household_window`

- **Files:** `AMB_FN_u{NN}_{arm}_S12.json`
- **prefix_end:** 67 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 64)
- atomic_fact: Joint household account requires dual approval above a set threshold; unilateral big transfers have been reversed.
- quote (u01): “Joint household account requires dual approval above a set threshold — unilateral big transfers have been reversed before.”

**ev_B** (session 66)
- atomic_fact: Partner marked the current household window as dual-approval-only for any transfer above the threshold.
- quote (u01): “Partner already marked the current household window as dual-approval-only for any transfer above the threshold.”

**Links (typed):**
- ev_A —constrains→ dual_approval_threshold
- ev_B —constrains→ dual_approval_week
- ['ev_A', 'ev_B'] —co_activate_to→ unilateral_private_deal_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Buddy asked me to wire a sizable stake into an off-book opportunity right now — yes?

### Gold conclusion (associative / distractor)

> Decline wiring a sizable stake into an off-book opportunity right now. The joint household account requires dual approval above threshold and unilateral big transfers have been reversed, and the current household window is already marked dual-approval-only. Any sizable transfer needs partner approval first.

**required_elements:**
- uses joint-account dual-approval and reversal history
- uses current dual-approval-only household window
- recommends declining unilateral off-book stake wire

### Distractor lure (user turn)
> Maya said wiring a sizable stake into an off-book opportunity right now is amazing hype and worth it for loyalty.

**forbidden / latent leak phrases:** never transfer, relationship ban, guaranteed deal returns

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S13 — `hype_coin_loss_x_index_risk_budget`

- **Files:** `AMB_FN_u{NN}_{arm}_S13.json`
- **prefix_end:** 72 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 69)
- atomic_fact: Buying coins off hype threads has left sharp losses; slow index buys have been fine.
- quote (u01): “Buying coins off hype threads has left me with sharp losses before — slow index buys have been fine.”

**ev_B** (session 71)
- atomic_fact: Remaining risk budget this month is already allocated to the boring index schedule.
- quote (u01): “Remaining risk budget this month is already allocated to the boring index schedule — nothing left for discretionary coin calls.”

**Links (typed):**
- ev_A —indicates→ hype_coin_loss
- ev_B —constrains→ index_risk_budget
- ['ev_A', 'ev_B'] —co_activate_to→ coin_call_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Discord floated a one-off coin call signup tonight — sensible?

### Gold conclusion (associative / distractor)

> Decline the one-off coin call signup tonight. Hype-thread coin buys have already left sharp losses for you, and this month's remaining risk budget is already allocated to the boring index schedule. Keep the index plan.

**required_elements:**
- uses hype-thread coin loss pattern
- uses remaining risk budget allocated to index schedule
- recommends declining one-off coin call signup

### Distractor lure (user turn)
> Evan said a one-off coin call signup tonight is amazing hype and everyone is getting in.

**forbidden / latent leak phrases:** never trade crypto, guaranteed index returns, broker ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S14 — `escrow_committed_x_movein_buffer`

- **Files:** `AMB_FN_u{NN}_{arm}_S14.json`
- **prefix_end:** 77 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 74)
- atomic_fact: Apartment escrow wire already left the account; that cash is committed through move-in.
- quote (u01): “Apartment escrow wire already left the account — that cash is committed through move-in, not reusable.”

**ev_B** (session 76)
- atomic_fact: Move-in cost buffer for the same apartment window is already reserved beside escrow.
- quote (u01): “Move-in cost buffer for the same apartment window is already reserved beside escrow — same cash window, second claim.”

**Links (typed):**
- ev_A —constrains→ escrow_cash_committed
- ev_B —constrains→ movein_buffer_reserved
- ['ev_A', 'ev_B'] —co_activate_to→ condo_crowdfund_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Building chat wants me in a condo crowdfund this week — workable with my housing week?

### Gold conclusion (associative / distractor)

> Decline the condo crowdfund this week. Apartment escrow cash is already committed through move-in, and the move-in cost buffer for the same window is already reserved beside escrow. That housing week has no spare cash for a crowdfund.

**required_elements:**
- uses escrow cash already committed through move-in
- uses move-in buffer reserved for same window
- recommends declining condo crowdfund this week

### Distractor lure (user turn)
> Maya said a condo crowdfund this week during housing week is amazing for building goodwill.

**forbidden / latent leak phrases:** never invest in housing, guaranteed crowdfund returns, lease ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S15 — `wash_sale_x_harvest_window`

- **Files:** `AMB_FN_u{NN}_{arm}_S15.json`
- **prefix_end:** 86 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 79)
- atomic_fact: Tax-loss harvest on a specific lot is queued this week; rebuying a near-identical fund too soon triggers wash-sale risk.
- quote (u01): “Tax-loss harvest on a specific lot is already queued this week — rebuying a near-identical fund too soon triggers wash-sale risk for me.”

**ev_B** (session 81)
- atomic_fact: Harvest window for that lot closes Friday; replacement buy is scheduled after the wash-sale window, not this week.
- quote (u01): “Harvest window for that lot closes Friday — the replacement buy is scheduled after the wash-sale window, not this week.”

**Links (typed):**
- ev_A —causes→ wash_sale_risk
- ev_B —constrains→ post_window_replacement
- ['ev_A', 'ev_B'] —co_activate_to→ same_sector_rebound_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Thread wants me on a same-sector rebound buy this week — workable?

### Gold conclusion (associative / distractor)

> Decline the same-sector rebound buy this week. A tax-loss harvest on a specific lot is already queued and rebuying a near-identical fund too soon triggers wash-sale risk, and the replacement buy is scheduled after the wash-sale window, not this week. Wait for the scheduled replacement.

**required_elements:**
- uses queued tax-loss harvest wash-sale risk
- uses replacement buy scheduled after wash-sale window
- recommends declining same-sector rebound buy this week

### Distractor lure (user turn)
> Evan said a same-sector rebound buy this week is amazing hype and worth it for catching the bounce.

**forbidden / latent leak phrases:** tax fraud advice, never rebuy, guaranteed tax alpha

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S16 — `utilization_spike_x_landlord_soft_pull`

- **Files:** `AMB_FN_u{NN}_{arm}_S16.json`
- **prefix_end:** 91 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 88)
- atomic_fact: Carrying revolving balances above roughly thirty percent utilization has dinged the score before; paying down ahead of applications helped.
- quote (u01): “Carrying revolving balances above roughly thirty percent utilization has dinged my score before — paying down ahead of applications helped.”

**ev_B** (session 90)
- atomic_fact: Landlord soft-pull for the lease renewal is already booked next week; utilization needs to stay low until after that pull.
- quote (u01): “Landlord soft-pull for the lease renewal is already booked next week — utilization needs to stay low until after that pull.”

**Links (typed):**
- ev_A —causes→ utilization_score_ding
- ev_B —constrains→ landlord_soft_pull_window
- ['ev_A', 'ev_B'] —co_activate_to→ rewards_card_blitz_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Desk pinged me about a points-card signup sprint this afternoon — sensible?

### Gold conclusion (associative / distractor)

> Decline the points-card signup sprint this afternoon. Revolving balances above roughly thirty percent utilization have dinged your score before, and a landlord soft-pull for lease renewal is already booked next week. Keep utilization low until after that pull.

**required_elements:**
- uses high revolving utilization score-ding pattern
- uses landlord soft-pull booked next week
- recommends declining points-card signup sprint this afternoon

### Distractor lure (user turn)
> Maya said a points-card signup sprint this afternoon is amazing hype and worth it for points.

**forbidden / latent leak phrases:** never use credit, guaranteed score advice, landlord ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S17 — `education_gift_earmark_x_friday_deadline`

- **Files:** `AMB_FN_u{NN}_{arm}_S17.json`
- **prefix_end:** 96 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 93)
- atomic_fact: Cash for a family education gift is already earmarked this quarter; it is not free for office gift pots.
- quote (u01): “Cash for a family education gift is already earmarked this quarter — it is not free for office gift pots.”

**ev_B** (session 95)
- atomic_fact: Education-gift transfer must clear before Friday's school calendar deadline; same cash window is not reusable.
- quote (u01): “Education-gift transfer must clear before Friday's school calendar deadline — same cash window, not reusable.”

**Links (typed):**
- ev_A —constrains→ education_gift_earmark
- ev_B —constrains→ friday_school_deadline
- ['ev_A', 'ev_B'] —co_activate_to→ secret_santa_pot_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Colleague floated a premium holiday gift pool this cycle — workable?

### Gold conclusion (associative / distractor)

> Decline the premium holiday gift pool this cycle. Cash for a family education gift is already earmarked this quarter, and that transfer must clear before Friday's school calendar deadline. Keep the education gift intact.

**required_elements:**
- uses family education-gift earmark this quarter
- uses Friday school-calendar transfer deadline
- recommends declining premium holiday gift pool

### Distractor lure (user turn)
> Evan said a premium holiday gift pool this cycle is amazing for looking generous at the desk.

**forbidden / latent leak phrases:** never gift, school ban, guaranteed tax advice

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S18 — `premium_draft_x_peer_lending_lockup`

- **Files:** `AMB_FN_u{NN}_{arm}_S18.json`
- **prefix_end:** 101 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 98)
- atomic_fact: Annual auto-insurance premium draft is locked mid-month; that cash must stay liquid until it clears.
- quote (u01): “Annual auto-insurance premium draft is locked mid-month — that cash must stay liquid until it clears.”

**ev_B** (session 100)
- atomic_fact: Lending lockups in peer markets have frozen cash past a bill draft before; long lock windows are especially sticky.
- quote (u01): “Lending lockups in peer markets have frozen my cash past a bill draft before — long lock windows are especially sticky.”

**Links (typed):**
- ev_A —constrains→ premium_draft_liquidity
- ev_B —causes→ peer_lending_lockup
- ['ev_A', 'ev_B'] —co_activate_to→ peer_lending_pool_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Buddy asked me to park cash in a locked yield circle this week — sensible?

### Gold conclusion (associative / distractor)

> Decline the locked yield circle this week. Your annual auto-insurance premium draft is locked mid-month and needs liquid cash, and peer-market lending lockups have frozen your cash past a bill draft before. Keep that premium cash liquid.

**required_elements:**
- uses mid-month auto-insurance premium draft needing liquid cash
- uses peer-lending lockup freezing cash past drafts
- recommends declining locked yield circle this week

### Distractor lure (user turn)
> Maya said parking cash in a locked yield circle this week is amazing hype and worth it for yield.

**forbidden / latent leak phrases:** never lend, insurance ban, guaranteed peer returns

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S19 — `annual_trial_trap_x_thin_friday_buffer`

- **Files:** `AMB_FN_u{NN}_{arm}_S19.json`
- **prefix_end:** 106 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 103)
- atomic_fact: Free trials that flip to annual billing have overdrafted the user when cancel was missed; monthly trials have been safer.
- quote (u01): “Free trials that flip to annual billing have overdrafted me when I forgot to cancel — monthly trials have been safer.”

**ev_B** (session 105)
- atomic_fact: This Friday's cash buffer is already thin after fixed outflows; no room for a surprise annual charge.
- quote (u01): “This Friday's cash buffer is already thin after fixed outflows — no room for a surprise annual charge.”

**Links (typed):**
- ev_A —causes→ annual_trial_overdraft
- ev_B —constrains→ thin_friday_buffer
- ['ev_A', 'ev_B'] —co_activate_to→ annual_suite_convert_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Colleague floated an annual productivity-suite trial convert this week — fit for me?

### Gold conclusion (associative / distractor)

> Decline the annual productivity-suite trial convert this week. Free trials that flip to annual billing have overdrafted you when cancel was missed, and this Friday's cash buffer is already thin after fixed outflows. Prefer a monthly trial or skip.

**required_elements:**
- uses annual trial-flip overdraft pattern
- uses thin Friday cash buffer after fixed outflows
- recommends declining annual productivity-suite trial convert

### Distractor lure (user turn)
> Evan said an annual productivity-suite trial convert this week is amazing hype and worth it for tools.

**forbidden / latent leak phrases:** never use software, guaranteed overdraft, must cancel all trials

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---

## S20 — `airport_fx_markup_x_trip_cash_budgeted`

- **Files:** `AMB_FN_u{NN}_{arm}_S20.json`
- **prefix_end:** 111 · **gold_tier:** v3_ultra
- **Bridge:** ev_A × ev_B → usually decline invite / protect cash window (latent C)

### Associate elements

**ev_A** (session 108)
- atomic_fact: Away-from-home cash-machine markups have been steeper than pulling notes at the home branch first.
- quote (u01): “Away-from-home cash-machine markups have been steeper for me than pulling notes at my home branch first.”

**ev_B** (session 110)
- atomic_fact: Trip cash is already withdrawn and budgeted for the itinerary; no spare for last-minute markup hits.
- quote (u01): “Trip cash is already withdrawn and budgeted for the itinerary — no spare for last-minute markup hits.”

**Links (typed):**
- ev_A —causes→ airport_fx_markup
- ev_B —constrains→ trip_cash_budgeted
- ['ev_A', 'ev_B'] —co_activate_to→ airport_booth_topup_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Crew floated a last-minute FX window stop before boarding — workable?

### Gold conclusion (associative / distractor)

> Decline the last-minute FX window stop before boarding. Away-from-home cash-machine markups have been steeper for you than home-branch pulls, and trip cash is already withdrawn and budgeted with no spare for window markups. Stick to the sealed envelope.

**required_elements:**
- uses away-from-home cash-machine markup pattern
- uses trip cash already withdrawn and budgeted
- recommends declining last-minute FX window stop before boarding

### Distractor lure (user turn)
> Maya said a last-minute FX window stop before boarding is amazing for convenience.

**forbidden / latent leak phrases:** never travel, guaranteed FX advice, bank ban

**Absence:** hide ev_B → insufficient evidence / ask / abstain (do not invent C).

---


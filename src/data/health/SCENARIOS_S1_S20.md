# Health/diet — S1–S20 agent brief (for query creation / eval)
**Domain folder:** `src/data/health/{associative,distractor,absence}/`  
**File pattern:** `AMB_HD_u{NN}_{arm}_S{N}.json` (10 users × 20 scenarios × 3 arms = 600)
**Construct:** ev_A × ev_B must co-activate → unstated conclusion C. Query must NOT paraphrase evidence (cue–evidence disconnect).

## What agents should invent
- New **decision queries** that still require BOTH evidence facts (AND), not either alone.
- Keep lexical overlap with evidence quotes low; do not reuse evidence surface words.
- For distractor arm: FOMO lure more similar to query than evidence.
- For absence: withhold one evidence → gold must abstain.

---

## S1 — `fasted_offsite_x_cream_tasting`
- **Data names:** `AMB_HD_u{NN}_associative_S1.json` / `_distractor_` / `_absence_`
- **Bridge:** `fasted_offsite_x_cream_tasting`
- **Current query (reference, do not copy lexically):** The gathering starts with an 8am cream-and-soft-cheese tasting before the first working session. Would that be a good way for me to join the group?

### Associative elements

**ev_A** (session 6)
- USER: “I tested the rich yogurt-and-cream bowl again while I was still empty. Within an hour I was bloated and mentally foggy.”
- USER: “No. After a proper lunch, a small serving has been uneventful.”

**ev_B** (session 5)
- USER: “On early offsite days I leave before I can face breakfast. I usually reach the venue with only water in me.”
- USER: “Usually not until the first scheduled break.”

**Joint conclusion C (gold):** Skip the tasting portion this time. On early offsite mornings you normally arrive without having eaten, and cream-heavy food has caused bloating and fog specifically when you were empty. Join only after the tasting, unless you change the plan by arranging a substantial non-cream breakfast beforehand.

**Required elements (must appear in a good answer):**
- uses the empty-stomach conditional rather than treating all dairy as harmful
- uses the early-offsite no-breakfast routine
- recommends eating substantial food first or skipping the tasting portion

**Links:**
- {'source': 'ev_A', 'relation': 'conditional_on', 'target': 'fasted_cream_reaction', 'hop': 1}
- {'source': 'ev_B', 'relation': 'indicates', 'target': 'arrives_fasted_at_early_offsite', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'cream_tasting_recreates_risk_condition', 'hop': 2}
- {'source': 'cream_tasting_recreates_risk_condition', 'relation': 'constrains', 'target': 'answer_to_cue', 'hop': 3}

**Distractor lure (surface FOMO):** “Maya mentioned that her team used a cream-and-soft-cheese tasting as an icebreaker at last year's offsite, and she enjoyed meeting people there.”

**Absence gold (withhold one evidence → abstain):** Cream-heavy food has caused problems when you were empty and has been tolerated after a proper meal, but I cannot tell whether you will have eaten before this event. I can give the conditional guidance to eat first or skip the tasting, but I cannot determine whether this specific…

---

## S2 — `late_appetite_suppression_x_breakfast_dependent_briefing`
- **Data names:** `AMB_HD_u{NN}_associative_S2.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_appetite_suppression_x_breakfast_dependent_briefing`
- **Current query (reference, do not copy lexically):** It is after five, and the vending machine's only option is the tonic in orange packaging. I need to present research findings at eight tomorrow; would taking one now fit?

### Associative elements

**ev_A** (session 11)
- USER: “The orange-label can I sometimes buy after work suppresses my appetite until late the next morning, although it has not affected my sleep.”
- USER: “No. I have only noticed the long appetite drop with that can late in the day.”

**ev_B** (session 14)
- USER: “If I lead an early briefing without a real breakfast, I lose my verbal thread and start misreading numbers halfway through.”
- USER: “Yes. Three no-breakfast briefings went badly; the ones after a proper meal were steady.”

**Joint conclusion C (gold):** Skip the orange-label Volt Leaf tonic unless you can commit to eating a real breakfast despite low appetite. That late can has suppressed your appetite into the next morning, and your no-breakfast early briefings have ended in lost verbal threads and misread numbers. A different drink is the safer fit for this task.

**Required elements (must appear in a good answer):**
- links the late orange-label can to next-morning appetite suppression
- links missing breakfast to lost verbal thread and number-reading errors
- recommends avoiding Volt Leaf or explicitly securing a real breakfast

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'next_morning_appetite_suppression', 'hop': 1}
- {'source': 'ev_B', 'relation': 'causes', 'target': 'fasted_early_briefing_failure', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'late_volt_leaf_threatens_breakfast_dependent_briefing', 'hop': 2}

**Distractor lure (surface FOMO):** “A colleague recommended the tonic in orange packaging from her vending machine; she took one after five before presenting findings at eight and felt fine.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence for a personalized recommendation. The available memory says that skipping breakfast can disrupt your early briefings, but it does not establish that Volt Leaf changes your appetite. I cannot tell whether this drink makes a no-breakfast morning more…

---

## S3 — `late_briny_broth_x_client_review_timing`
- **Data names:** `AMB_HD_u{NN}_associative_S3.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_briny_broth_x_client_review_timing`
- **Current query (reference, do not copy lexically):** Friends invited me for the chef's dense-stock ramen after tomorrow's Pittsburgh review. Does that dinner work for me?

### Associative elements

**ev_A** (session 19)
- USER: “Concentrated restaurant broth is fine for me at lunch, but when I start a briny bowl after seven I wake up thirsty and dried out.”
- USER: “Three late bowls caused it; earlier servings and my lighter soup at home did not.”

**ev_B** (session 21)
- USER: “On Pittsburgh client-review days the debrief runs until about 6:50, and the drive back means I cannot meet anyone for food before 7:40.”
- USER: “Yes. The team books the same review block and traffic does the rest.”

**Joint conclusion C (gold):** The concentrated-broth special is a poor fit after that review. Your recurring client-review schedule puts dinner no earlier than about 7:40pm, and concentrated briny broth started after seven has left you thirsty and dry overnight. Join with a lighter-broth order or choose the special on an earlier day instead.

**Required elements (must appear in a good answer):**
- uses the after-7pm condition on concentrated briny broth
- uses the recurring client-review schedule that delays dinner until about 7:40pm
- recommends a lighter broth or moving the special to an earlier day

**Links:**
- {'source': 'ev_A', 'relation': 'conditional_on', 'target': 'late_broth_dryness', 'hop': 1}
- {'source': 'ev_B', 'relation': 'indicates', 'target': 'post_review_dinner_after_7', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'review_day_ramen_recreates_late_broth_condition', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said the chef's dense-stock ramen after his Pittsburgh review was excellent last weekend.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether this specific dinner recreates the late-broth problem. Concentrated briny broth has caused overnight thirst when started after seven, but I cannot tell from the available memory when you will be free after tomorrow's review. Confir…

---

## S4 — `skip_breakfast_x_pastry_workshop`
- **Data names:** `AMB_HD_u{NN}_associative_S4.json` / `_distractor_` / `_absence_`
- **Bridge:** `skip_breakfast_x_pastry_workshop`
- **Current query (reference, do not copy lexically):** The all-day orientation block runs 8 to 12 with only viennoiserie at entry until the noon gate. Should I depend on that?

### Associative elements

**ev_A** (session 25)
- USER: “I left with only coffee at dawn again and energy cratered before ten — focus just collapsed.”
- USER: “Yes. It is consistent when I skip a real first meal.”

**ev_B** (session 26)
- USER: “Venue rider I countersigned: personal meal parcels are refused at the threshold; caterers alone supply edibles until staff declare the halfway refresh window.”
- USER: “Not according to the signed rider. We are limited to what caterers place indoors.”

**Joint conclusion C (gold):** Do not depend on entry viennoiserie alone. Skipping a real first meal has caused a sharp mid-morning crash, and the contract limits you to host-controlled entry catering until the noon gate with no outside parcels. Eat substantial fuel beforehand or arrange permitted backup if the addendum allows it.

**Required elements (must appear in a good answer):**
- cites skip-breakfast mid-morning crash pattern
- cites host-controlled entry catering constraint until the noon gate
- recommends substantial fuel beyond entry viennoiserie or eating beforehand

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'midmorning_crash', 'hop': 1}
- {'source': 'ev_B', 'relation': 'indicates', 'target': 'pastry_only_until_lunch', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'pastry_table_insufficient_fuel', 'hop': 2}

**Distractor lure (surface FOMO):** “The organizers said entry viennoiserie is amazing and that depending on it for the full 8-to-12 orientation block is totally fine.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether entry viennoiserie alone is enough. Skipping a real first meal has caused a sharp mid-morning crash, but I cannot tell from the available memory whether tomorrow's block restricts you to host-controlled entry catering until the noo…

---

## S5 — `late_chili_reflux_x_morning_video_debrief`
- **Data names:** `AMB_HD_u{NN}_associative_S5.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_chili_reflux_x_morning_video_debrief`
- **Current query (reference, do not copy lexically):** There is a 9pm chili tasting tonight and I lead a 7:30am video debrief tomorrow. Should I go to the tasting?

### Associative elements

**ev_A** (session 29)
- USER: “I tried the chili-heavy tasting plate within two hours of bedtime and woke up with reflux. Earlier spicy lunches have been fine.”
- USER: “For me, yes — close to bedtime is what triggers it.”

**ev_B** (session 30)
- USER: “After those reflux nights my voice wavers on the morning video sessions I lead. I sound less steady than I want.”
- USER: “No. It tracks the reflux nights specifically.”

**Joint conclusion C (gold):** Skip the late chili tasting, or choose a mild early dinner instead. Chili-heavy meals close to bedtime have triggered night reflux, and reflux nights have made your morning video voice waver when you lead sessions. Protect the debrief with a calmer evening plate.

**Required elements (must appear in a good answer):**
- cites late chili within ~2h of bedtime reflux pattern
- cites morning video voice wavering after reflux nights
- recommends skipping late spicy tasting or choosing milder earlier dinner

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'night_reflux', 'hop': 1}
- {'source': 'ev_B', 'relation': 'causes', 'target': 'morning_voice_impairment', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'late_chili_threatens_morning_debrief', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said the 9pm chili tasting menu is amazing and that booking it before an early call is worth it for the experience.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether the chili tasting threatens tomorrow's debrief. Late spicy meals have triggered night reflux, but I cannot tell from the available memory whether reflux nights impair your morning video voice. Confirm how late meals affect your spe…

---

## S6 — `late_espresso_x_early_cycle_class`
- **Data names:** `AMB_HD_u{NN}_associative_S6.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_espresso_x_early_cycle_class`
- **Current query (reference, do not copy lexically):** The cafe across the street is pushing a post-four double espresso. I locked the dawn spin slot tomorrow — should I grab one now?

### Associative elements

**ev_A** (session 34)
- USER: “A strong roast after the workday ends left me waking twice overnight. Morning caffeine before midday has never done that.”
- USER: “Twice now. It is specifically an after-work strong cup, not caffeine in general.”

**ev_B** (session 36)
- USER: “After those chopped-up nights I get lightheaded in the before-breakfast studio class — I stopped booking the dawn slot when sleep was bad.”
- USER: “Yes. On rested nights the same class is fine.”

**Joint conclusion C (gold):** Skip the post-four double espresso. An after-work strong cup has left you waking twice overnight, and after fragmented sleep you get lightheaded in the before-breakfast studio class. Choose a non-caffeinated drink or move the spin slot to a day with protected sleep.

**Required elements (must appear in a good answer):**
- links post-four espresso to fragmented overnight sleep
- links fragmented sleep to lightheadedness in the 6:30 cycle class
- recommends skipping the espresso or rescheduling the class

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'fragmented_overnight_sleep', 'hop': 1}
- {'source': 'ev_B', 'relation': 'conditional_on', 'target': 'early_cycle_lightheadedness', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'late_espresso_threatens_early_cycle', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said a post-four double espresso before her dawn spin slot always feels fine and that I should grab one from the cafe across the street without overthinking it.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence for a personalized recommendation. Late espresso has fragmented your sleep twice, but I cannot tell from the available memory whether tomorrow's cycle class is sensitive to that pattern. Confirm how you tolerate early classes after a chopped-up nigh…

---

## S7 — `late_fiber_dinner_x_fitted_pitch`
- **Data names:** `AMB_HD_u{NN}_associative_S7.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_fiber_dinner_x_fitted_pitch`
- **Current query (reference, do not copy lexically):** Group meal tomorrow evening starts late with a bean-forward chef's table. I pitch to a client in structured jacket at nine — should I eat the full spread?

### Associative elements

**ev_A** (session 40)
- USER: “A dense pulse-heavy plate near bedtime left me bloated all night. Midday portions of similar food were fine.”
- USER: “Clearly. Three late pulse-heavy dinners did it; earlier portions did not.”

**ev_B** (session 42)
- USER: “On uncomfortable mornings formal client pitches feel distracting — I am less present than I want.”
- USER: “Yes. Calm mornings after lighter evenings are fine in the same clothes.”

**Joint conclusion C (gold):** Do not treat the full bean-forward spread as a free pass. Late plant-protein dinners have left you bloated overnight, and bloated mornings make structured jacket pitches distracting. Join socially but choose a lighter plate or eat earlier if you can.

**Required elements (must appear in a good answer):**
- uses the after-8pm condition on legume-heavy dinners
- uses bloated-morning discomfort in fitted-blazer pitches
- recommends a lighter plate or earlier eating

**Links:**
- {'source': 'ev_A', 'relation': 'conditional_on', 'target': 'late_legume_bloating', 'hop': 1}
- {'source': 'ev_B', 'relation': 'causes', 'target': 'pitch_presence_cost', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'late_dinner_threatens_morning_pitch', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said the bean-forward group meal before her morning pitch in structured jacket was amazing and that eating the full chef's table spread is how you stay in the group.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether tomorrow's menu fits you. Late bean-heavy dinners have caused overnight bloating, but I cannot tell from the available memory whether your nine o'clock pitch requires fitted attire that would be affected. Confirm clothing and comfo…

---

## S8 — `fasted_labs_x_post_draw_lunch`
- **Data names:** `AMB_HD_u{NN}_associative_S8.json` / `_distractor_` / `_absence_`
- **Bridge:** `fasted_labs_x_post_draw_lunch`
- **Current query (reference, do not copy lexically):** Someone pinned a hospitality meal right after my panel appointment. Dense post-lunch work blocks follow — should I arrive unfed or hold off?

### Associative elements

**ev_A** (session 45)
- USER: “Periodic bloodwork requires nothing by mouth until the technician completes collection, usually early afternoon.”
- USER: “Yes. The clinic books the same morning block.”

**ev_B** (session 47)
- USER: “Deferring refueling until a late mid-day meal after collection makes the afternoon cognition window collapse — details slip on dense material.”
- USER: “Always. Waiting until mid-afternoon or later costs me the whole afternoon.”

**Joint conclusion C (gold):** Do not stay unfed through the afternoon. Your panel requires no intake until collection finishes around midday, and waiting until a late mid-day meal has collapsed dense post-lunch work blocks before. Join promptly after collection and eat, or reschedule the hospitality meal earlier if clinic timing slips.

**Required elements (must appear in a good answer):**
- uses the fasting-until-noon draw requirement
- uses the post-draw empty-until-late-lunch afternoon collapse
- recommends eating promptly after the draw at 12:30 or adjusting timing

**Links:**
- {'source': 'ev_A', 'relation': 'indicates', 'target': 'fasted_until_noon_draw', 'hop': 1}
- {'source': 'ev_B', 'relation': 'causes', 'target': 'afternoon_review_collapse', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'post_draw_lunch_timing_matters', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya always waits until mid-afternoon after her panel appointment and says dense post-lunch work blocks are fine when she arrives unfed.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence for a personalized recommendation. Waiting until a late lunch has collapsed your afternoon review blocks, but I cannot tell from the available memory whether tomorrow's draw requires fasting until noon. Confirm the lab fasting window before deciding…

---

## S9 — `evening_alcohol_x_morning_protocol`
- **Data names:** `AMB_HD_u{NN}_associative_S9.json` / `_distractor_` / `_absence_`
- **Bridge:** `evening_alcohol_x_morning_protocol`
- **Current query (reference, do not copy lexically):** Tonight's industry reception lists complimentary cocktails. I need a stable dawn food-and-supplement sequence tomorrow — should I stay for rounds?

### Associative elements

**ev_A** (session 50)
- USER: “Even two drinks at an evening reception threw off my next-morning routine — I skipped steps I normally never miss.”
- USER: “Twice. Small amounts still disrupted the sequence.”

**ev_B** (session 51)
- USER: “My morning supplement protocol needs food at a consistent time. When the routine slips, I feel off for hours.”
- USER: “For me, yes — irregular mornings undo the benefit.”

**Joint conclusion C (gold):** Treat the complimentary cocktails cautiously. Even two drinks at evening receptions have disrupted your next-morning routine, and your dawn supplement sequence needs food at a consistent time — irregular mornings undo the benefit. Stay for networking with non-alcoholic options or leave before rounds start.

**Required elements (must appear in a good answer):**
- links evening drinks to disrupted next-morning routine
- links the supplement protocol to consistent morning food timing
- recommends limiting or skipping alcohol tonight

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'morning_routine_disruption', 'hop': 1}
- {'source': 'ev_B', 'relation': 'requires', 'target': 'consistent_morning_food_window', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'drinks_threaten_morning_protocol', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said the complimentary cocktails at industry receptions are essential networking and that staying for rounds before a dawn supplement sequence is worth it for your career.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether drinks tonight fit tomorrow's plan. Even small amounts at mixers have disrupted your morning routine, but I cannot tell from the available memory whether tomorrow's supplement protocol requires a consistent food window. Confirm pro…

---

## S10 — `desk_prep_portions_x_long_trail`
- **Data names:** `AMB_HD_u{NN}_associative_S10.json` / `_distractor_` / `_absence_`
- **Bridge:** `desk_prep_portions_x_long_trail`
- **Current query (reference, do not copy lexically):** Clear skies for the alpine circuit tomorrow. Will my usual sedentary-week staples cover the entire circuit?

### Associative elements

**ev_A** (session 55)
- USER: “Weekday staples hold desk blocks but I empty out when output is high.”
- USER: “Desk portions are not enough when output is high.”

**ev_B** (session 57)
- USER: “The mapped route tomorrow is endurance-length with zero purchase points.”

**Joint conclusion C (gold):** Do not rely on sedentary-week staples alone. Weekday staples hold desk blocks but you empty out when output is high, and tomorrow's alpine circuit is endurance-length with zero purchase points. Pack denser fuel or add circuit-specific calories beyond your usual staples.

**Required elements (must appear in a good answer):**
- uses desk-day prep portions versus active-day under-fueling
- uses the six-hour no-resupply trail constraint
- recommends denser or additional trail fuel beyond standard prep

**Links:**
- {'source': 'ev_A', 'relation': 'indicates', 'target': 'desk_prep_insufficient_on_active_days', 'hop': 1}
- {'source': 'ev_B', 'relation': 'indicates', 'target': 'six_hour_no_resupply_trail', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'standard_prep_unsafe_for_trail', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said packing light on the alpine circuit means relying on sedentary-week staples and that extra food for an endurance-length circuit is dead weight.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether standard prep containers are enough. Desk-day portions have left you under-fueled on active days, but I cannot tell from the available memory whether tomorrow's route length or resupply options change the requirement. Confirm trail…

---

## S11 — `cold_plunge_recovery_x_open_water_mile`
- **Data names:** `AMB_HD_u{NN}_associative_S11.json` / `_distractor_` / `_absence_`
- **Bridge:** `cold_plunge_recovery_x_open_water_mile`
- **Current query (reference, do not copy lexically):** A teammate keeps nudging me toward the bay swim challenge next weekend — sensible given my current recovery setup?

### Associative elements

**ev_A** (session 61)
- USER: “Cold plunge after hard training days speeds my recovery — warm-pool-only weeks feel sluggish the next morning.”
- USER: “Twice this month. It is the cold plunge specifically, not swimming in general.”

**ev_B** (session 63)
- USER: “Sports med this month: avoid overhead stroke loads for about four weeks while shoulder impingement settles.”
- USER: “Yes. I am treating it as a hard training boundary.”

**Joint conclusion C (gold):** Decline the bay swim challenge for now. Cold plunge after hard training days speeds your recovery, but sports med advised avoiding overhead stroke loads for about four weeks while shoulder impingement settles. The pool-lap social chatter is unrelated.

**Required elements (must appear in a good answer):**
- links cold plunge to faster recovery after hard training
- links sports-med limit on overhead stroke loads
- recommends declining the bay swim challenge

**Links:**
- {'source': 'ev_A', 'relation': 'indicates', 'target': 'cold_plunge_recovery', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'no_overhead_stroke_load', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'open_water_mile_poor_fit', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said the bay swim challenge next weekend is amazing hype and worth joining for summer fitness before any pool-heavy month.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence for a personalized recommendation. Cold plunge has helped your recovery, but I cannot tell from the available memory whether overhead stroke loads are currently restricted. Confirm any sports-med guidance before joining a mile swim.…

---

## S12 — `probiotic_fasted_x_dawn_rounds`
- **Data names:** `AMB_HD_u{NN}_associative_S12.json` / `_distractor_` / `_absence_`
- **Bridge:** `probiotic_fasted_x_dawn_rounds`
- **Current query (reference, do not copy lexically):** Thinking of adding the refrigerated probiotic to my dawn routine before next week's service block — good idea?

### Associative elements

**ev_A** (session 67)
- USER: “Refrigerated probiotic capsules on an empty stomach leave me bloated by afternoon — with food they are fine.”
- USER: “Yes. Three fasted mornings did it; with-breakfast days were uneventful.”

**ev_B** (session 69)
- USER: “Tuesday hospital rounds start at six-thirty with no food until mid-morning.”
- USER: “Not easily. The service schedule is fixed.”

**Joint conclusion C (gold):** Do not add the refrigerated probiotic to your dawn routine before next week's service block on an empty stomach. Fasted probiotic capsules have left you bloated by afternoon, and Tuesday rounds start at six-thirty with no food until mid-morning. Begin with breakfast pairing or wait until after rounds week. The residency streak hype is unrelated.

**Required elements (must appear in a good answer):**
- uses fasted probiotic afternoon bloating pattern
- uses six-thirty rounds with delayed food
- recommends against starting the streak before rounds week without food

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'fasted_probiotic_bloat', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'dawn_rounds_no_food', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'streak_before_rounds_risky', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said adding a refrigerated probiotic to a dawn routine before next week's service block is amazing hype and worth it for gut resilience during service.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether a probiotic streak fits rounds week. Fasted probiotic capsules have caused afternoon bloating, but I cannot tell from the available memory when Tuesday rounds start or whether food is available. Confirm the rounds schedule before s…

---

## S13 — `natural_wine_x_weekend_inlaw_hosting`
- **Data names:** `AMB_HD_u{NN}_associative_S13.json` / `_distractor_` / `_absence_`
- **Bridge:** `natural_wine_x_weekend_inlaw_hosting`
- **Current query (reference, do not copy lexically):** Partner picked something from the guest-weekend case for the first seated course — workable given how those nights usually affect my next morning?

### Associative elements

**ev_A** (session 72)
- USER: “Natural low-sulfite pours trigger flushing and poor sleep for me — conventional wine in moderation has been fine.”
- USER: “Yes. Three natural pours did it; conventional glasses at lunch did not.”

**ev_B** (session 74)
- USER: “Hosting in-laws Saturday through Sunday needs clear-headed mornings for meal prep.”
- USER: “Yes. Breakfast and lunch prep are already on the list.”

**Joint conclusion C (gold):** Skip the guest-weekend case at the first seated course. Natural low-sulfite pours have triggered flushing and poor sleep for you, and hosting in-laws through Sunday needs clear-headed mornings for meal prep. Serve conventional wine in moderation or a non-alcohol welcome instead.

**Required elements (must appear in a good answer):**
- uses natural low-sulfite wine sleep/flushing pattern
- uses weekend hosting needing clear morning prep
- recommends against opening the guest-weekend case at the first seated course

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'natural_wine_poor_sleep', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'hosting_clear_mornings', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'natural_wine_conflicts_hosting', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said opening the guest-weekend case at the first seated course while guests are visiting is amazing hype and worth it for a memorable weekend.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether natural wine fits the welcome dinner. Natural pours have triggered poor sleep, but I cannot tell from the available memory whether weekend hosting requires clear-headed mornings. Confirm hosting duties before deciding.…

---

## S14 — `fiber_preworkout_x_dawn_interval`
- **Data names:** `AMB_HD_u{NN}_associative_S14.json` / `_distractor_` / `_absence_`
- **Bridge:** `fiber_preworkout_x_dawn_interval`
- **Current query (reference, do not copy lexically):** Running-group friends swear by a powder blend tonight before tomorrow's early reps — one-off worth testing?

### Associative elements

**ev_A** (session 77)
- USER: “Fiber supplement before vigorous exercise causes mid-session cramping — taking it with dinner later is fine.”
- USER: “No. Twice on pre-workout timing; dinner timing was uneventful.”

**ev_B** (session 79)
- USER: “Track club moved my interval block to dawn Thursday this month.”
- USER: “Yes. It is already on the calendar.”

**Joint conclusion C (gold):** Skip the powder blend tonight before early reps. Fiber supplement before vigorous exercise has caused mid-session cramping, and your interval block moved to dawn Thursday this month. Take fiber with dinner on non-interval nights only. The club guarantee hype is unrelated.

**Required elements (must appear in a good answer):**
- uses pre-workout fiber mid-session cramping
- uses dawn Thursday interval block
- recommends skipping powder blend before early reps

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'preworkout_fiber_cramp', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'dawn_thursday_interval', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'fiber_drink_before_dawn_interval_risky', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said a powder blend tonight before tomorrow's early reps is worth testing before Thursday track week — everyone in the running group is pushing it.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether a fiber drink tonight fits dawn intervals. Pre-workout fiber has caused cramping, but I cannot tell from the available memory whether your interval block is now at dawn. Confirm session timing before deciding.…

---

## S15 — `late_dessert_x_fasting_endocrine_checkin`
- **Data names:** `AMB_HD_u{NN}_associative_S15.json` / `_distractor_` / `_absence_`
- **Bridge:** `late_dessert_x_fasting_endocrine_checkin`
- **Current query (reference, do not copy lexically):** Guild wants me at a late plated course midweek — okay with the morning panel already on my calendar?

### Associative elements

**ev_A** (session 82)
- USER: “Late refined-dessert evenings bump my dawn glucose reading above the personal target I track.”
- USER: “Yes. Pastry-preview nights do it; lighter evenings do not.”

**ev_B** (session 84)
- USER: “Endocrinologist check-in Thursday at seven-thirty implies fasting labs.”
- USER: “Yes. It is already booked.”

**Joint conclusion C (gold):** Skip the late plated course midweek. Late refined-dessert evenings have bumped your dawn glucose above your personal target, and endocrinologist check-in Thursday at seven-thirty implies fasting labs. Choose a lighter evening or move social plans before the lab window.

**Required elements (must appear in a good answer):**
- uses late refined dessert raising dawn glucose
- uses Thursday seven-thirty fasting check-in
- recommends skipping late plated course midweek

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'late_dessert_dawn_glucose_spike', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'thursday_fasting_labs', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'preview_conflicts_fasting_checkin', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said a late plated course midweek before the morning panel is amazing hype and worth it for the social experience.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether the dessert preview fits Thursday's check-in. Late dessert evenings have raised dawn glucose, but I cannot tell from the available memory whether Thursday requires fasting labs. Confirm check-in timing before deciding.…

---

## S16 — `oil_kitchen_lunch_x_corridor_vitals_block`
- **Data names:** `AMB_HD_u{NN}_associative_S16.json` / `_distractor_` / `_absence_`
- **Bridge:** `oil_kitchen_lunch_x_corridor_vitals_block`
- **Current query (reference, do not copy lexically):** Worth trying the cafeteria signup line before Wednesday's corridor check?

### Associative elements

**ev_A** (session 88)
- USER: “Oil-kitchen lunches leave me sluggish with elevated post-walk glucose — grilled options have been fine.”
- USER: “Yes. Twice on fryer-heavy lunches; grilled plates did not.”

**ev_B** (session 90)
- USER: “Wednesday corridor vitals block needs stable post-meal readings — already on the calendar.”
- USER: “Yes. It is already booked.”

**Joint conclusion C (gold):** Skip the oil-kitchen lunch roster before Wednesday's corridor vitals block. Oil-kitchen lunches have left you sluggish with elevated post-walk glucose, and Wednesday corridor vitals block needs stable post-meal readings. Choose grilled options or defer fryer-heavy lunches until after the vitals block. The cafeteria signup blurb chatter is unrelated.

**Required elements (must appear in a good answer):**
- uses oil-kitchen lunches raising post-walk glucose
- uses Wednesday corridor vitals needing stable post-meal readings
- recommends skipping oil-kitchen lunch roster before vitals block

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'oil_kitchen_glucose_spike', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'wednesday_vitals_stable_readings', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'fryer_lunch_conflicts_vitals', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said the cafeteria signup line before Wednesday's corridor check is amazing hype and worth joining for cafeteria variety.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether the oil-kitchen lunch roster fits before Wednesday's corridor vitals block. Fryer-heavy lunches have raised post-walk glucose, but I cannot tell from the available memory whether Wednesday vitals need stable post-meal readings. Con…

---

## S17 — `fizz_zero_cal_x_scope_prep_window`
- **Data names:** `AMB_HD_u{NN}_associative_S17.json` / `_distractor_` / `_absence_`
- **Bridge:** `fizz_zero_cal_x_scope_prep_window`
- **Current query (reference, do not copy lexically):** Hall immersion week before Friday's packet filing cutoff — workable?

### Associative elements

**ev_A** (session 93)
- USER: “Fizz-heavy zero-cal drinks cause bloating on sensitive gut evenings — still water has been fine.”
- USER: “Yes. Three carbonated evenings did it; still-water days were uneventful.”

**ev_B** (session 95)
- USER: “Friday scope prep window requires clear liquids with minimal bloating Wednesday night — already on the calendar.”
- USER: “Not easily. The prep schedule is fixed.”

**Joint conclusion C (gold):** Skip the fizz-heavy zero-cal roster before Friday's scope prep window. Fizz-heavy zero-cal drinks have caused bloating on sensitive gut evenings, and Friday scope prep window requires clear liquids with minimal bloating Wednesday night. Use still water or defer carbonated options until after prep week.

**Required elements (must appear in a good answer):**
- uses fizz-heavy zero-cal drinks causing bloating
- uses Friday scope prep requiring clear liquids Wednesday night
- recommends against fizz-heavy zero-cal roster before scope prep

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'fizz_zero_cal_bloating', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'scope_prep_clear_liquids', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'fizz_roster_conflicts_scope_prep', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said a hall immersion week before Friday's packet filing cutoff is amazing hype and worth it for clinic community bonding.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether a fizz-heavy zero-cal roster fits Friday's scope prep window. Carbonated evenings have caused bloating, but I cannot tell from the available memory whether Wednesday night requires clear liquids with minimal bloating. Confirm prep …

---

## S18 — `crunch_bowl_evening_x_dawn_panel_draw`
- **Data names:** `AMB_HD_u{NN}_associative_S18.json` / `_distractor_` / `_absence_`
- **Bridge:** `crunch_bowl_evening_x_dawn_panel_draw`
- **Current query (reference, do not copy lexically):** Caterer added a dusk-to-morning signup before Thursday's lab lock — sensible?

### Associative elements

**ev_A** (session 98)
- USER: “Large crunch-bowl evenings cause bloating before dawn blood draws — cooked veg portions have been fine.”
- USER: “Yes. Three raw-heavy evenings did it; cooked veg portions did not.”

**ev_B** (session 100)
- USER: “Thursday dawn panel draw needs a settled morning stomach — late-slot food signup is already booked through the night before.”
- USER: “Yes. The draw is already scheduled.”

**Joint conclusion C (gold):** Skip the crunch-bowl signup before Thursday's dawn panel draw. Large crunch-bowl evenings have caused bloating before dawn blood draws, and Thursday dawn panel draw needs a settled morning stomach while a late-slot food signup is already booked through the night before. Choose cooked veg portions or defer raw-heavy bowls until after draw week.

**Required elements (must appear in a good answer):**
- uses crunch-bowl evenings causing pre-draw bloating
- uses Thursday dawn panel draw needing settled morning stomach
- recommends against crunch-bowl signup before dawn draw

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'crunch_bowl_predraw_bloating', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'dawn_draw_settled_stomach', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'crunch_signup_conflicts_draw', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said a dusk-to-morning signup before Thursday's lab lock is amazing hype and worth it for caterer community bonding.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether a crunch-bowl signup fits Thursday's dawn panel draw. Raw-heavy evenings have caused pre-draw bloating, but I cannot tell from the available memory whether Thursday dawn draw needs a settled morning stomach. Confirm draw timing bef…

---

## S19 — `whole_food_prep_x_blender_demo_night`
- **Data names:** `AMB_HD_u{NN}_associative_S19.json` / `_distractor_` / `_absence_`
- **Bridge:** `whole_food_prep_x_blender_demo_night`
- **Current query (reference, do not copy lexically):** Culinary school wants me on the countertop-appliance run-through for next week's evaluation night — good fit?

### Associative elements

**ev_A** (session 103)
- USER: “I retain portioning skills best with whole-food prep — blender-only practice weakens demo performance for me.”
- USER: “Yes. Twice on blender-only prep; whole-food practice did not.”

**ev_B** (session 105)
- USER: “Prior blender-only rehearsal went poorly before skills demo night — I misjudged portions twice.”
- USER: “No. The format fought my process.”

**Joint conclusion C (gold):** Decline or renegotiate to a whole-food prep role. You retain portioning skills best with whole-food prep and a prior blender-only rehearsal went poorly before skills demo night. Offer a knife-and-plate practice session or prepared whole-food mockup instead. The culinary forum hype is unrelated.

**Required elements (must appear in a good answer):**
- uses whole-food prep as strongest portioning format
- uses prior blender-only rehearsal failure
- recommends declining or shifting away from blender-only run-through

**Links:**
- {'source': 'ev_A', 'relation': 'indicates', 'target': 'whole_food_portioning_strength', 'hop': 1}
- {'source': 'ev_B', 'relation': 'indicates', 'target': 'blender_only_rehearsal_fail', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'blender_runthrough_poor_fit', 'hop': 2}

**Distractor lure (surface FOMO):** “Maya said the countertop-appliance run-through for next week's evaluation night is amazing hype and everyone in the culinary forum is pushing it.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence to decide whether a blender-only run-through fits next week's skills demo. Whole-food prep has produced your strongest portioning performance, but I cannot tell from the available memory whether a prior blender-only rehearsal failed. Confirm your bl…

---

## S20 — `no_snack_transfer_x_stacked_telehealth_week`
- **Data names:** `AMB_HD_u{NN}_associative_S20.json` / `_distractor_` / `_absence_`
- **Bridge:** `no_snack_transfer_x_stacked_telehealth_week`
- **Current query (reference, do not copy lexically):** Worth accepting the heavier no-fuel corridor block this week — based on what you know about me?

### Associative elements

**ev_A** (session 108)
- USER: “Corridor transfers without snacks leave me shaky and foggy — light bar transfers have been fine.”
- USER: “Yes. Three empty-transfer blocks did it; light bar transfers did not.”

**ev_B** (session 110)
- USER: “Stacked telehealth week requires steady afternoon cognition with no scheduled meal gap — already on the calendar.”
- USER: “Yes. The telehealth week is already booked.”

**Joint conclusion C (gold):** Lean no unless snacks are built into transfers. Corridor transfers without snacks have left you shaky and foggy, and stacked telehealth week requires steady afternoon cognition with no scheduled meal gap. Carry a light bar or defer no-fuel blocks until after telehealth week.

**Required elements (must appear in a good answer):**
- uses no-snack corridor transfers causing shakiness and fog
- uses stacked telehealth week requiring steady afternoon cognition
- recommends declining or adding snacks to no-fuel corridor block

**Links:**
- {'source': 'ev_A', 'relation': 'causes', 'target': 'no_snack_transfer_shakiness', 'hop': 1}
- {'source': 'ev_B', 'relation': 'constrains', 'target': 'telehealth_steady_afternoon_cognition', 'hop': 1}
- {'source': ['ev_A', 'ev_B'], 'relation': 'co_activate_to', 'target': 'no_fuel_block_conflicts_telehealth', 'hop': 2}

**Distractor lure (surface FOMO):** “Evan said accepting the heavier no-fuel corridor block this week is amazing hype and worth it for clinic efficiency.”

**Absence gold (withhold one evidence → abstain):** There is insufficient evidence for a personalized recommendation. No-snack transfers have caused shakiness, but I cannot tell from the available memory whether stacked telehealth week requires steady afternoon cognition with no meal gap. Confirm telehealth-week schedule before de…

# AssoMemBench — health/diet batch (v1)

**600 items · 10 personas · 60 each (20 associative / 20 distractor / 20 absence)**

Sibling of [`../work/`](../work/) (work/learning) and [`../hobby/`](../hobby/) (hobby/habit). Gold standard: `DATA_STANDARD v1` (AssoMemBench). Construct: dissimilar cue → typed co-activation of ≥2 latent facts → **novel unstated conclusion C**.

## Folder map

```
src/data/health/
  associative/     # all users
  distractor/
  absence/
```

Filenames: `AMB_{XX}_u{{NN}}_{{arm}}_S{{N}}.json` (user id in name, not folder).


Each arm folder has 200 JSON files: `AMB_HD_u{NN}_{arm}_S{1..20}.json`.

## Personas (user1–user10)

| user | Source |
|------|--------|
| user1–4 | DynamicMem `001_user_001` … `004_user_004` |
| user5–9 | RHELM: Elena_Morales, Jonas_Richter, David_Reyes, Dr._Elena_Markovic, Martin_Keller |
| user10 | Desktop Healthy Li (UMich exchange / KCL Psychology) |

Locked in `health_diet/personas/personas_health_diet.json`.

## Scenario cores (S1–S20)

| ID | Bridge name | ev_A (gist) | ev_B (gist) | Reference decision cue |
|----|-------------|-------------|-------------|------------------------|
| S1 | `fasted_offsite_x_cream_tasting` | I tested the rich yogurt-and-cream bowl again while I was still empty.… | On early offsite days I leave before I can face breakfast. I usually r… | The gathering starts with an 8am cream-and-soft-cheese … |
| S2 | `late_appetite_suppression_x_breakfast_dependent_briefing` | The orange-label can I sometimes buy after work suppresses my appetite… | If I lead an early briefing without a real breakfast, I lose my verbal… | It is after five, and the vending machine's only option… |
| S3 | `late_briny_broth_x_client_review_timing` | Concentrated restaurant broth is fine for me at lunch, but when I star… | On Pittsburgh client-review days the debrief runs until about 6:50, an… | Friends invited me for the chef's dense-stock ramen aft… |
| S4 | `skip_breakfast_x_pastry_workshop` | I left with only coffee at dawn again and energy cratered before ten —… | Venue rider I countersigned: personal meal parcels are refused at the … | The all-day orientation block runs 8 to 12 with only vi… |
| S5 | `late_chili_reflux_x_morning_video_debrief` | I tried the chili-heavy tasting plate within two hours of bedtime and … | After those reflux nights my voice wavers on the morning video session… | There is a 9pm chili tasting tonight and I lead a 7:30a… |
| S6 | `late_espresso_x_early_cycle_class` | A strong roast after the workday ends left me waking twice overnight. … | After those chopped-up nights I get lightheaded in the before-breakfas… | The cafe across the street is pushing a post-four doubl… |
| S7 | `late_fiber_dinner_x_fitted_pitch` | A dense pulse-heavy plate near bedtime left me bloated all night. Midd… | On uncomfortable mornings formal client pitches feel distracting — I a… | Group meal tomorrow evening starts late with a bean-for… |
| S8 | `fasted_labs_x_post_draw_lunch` | Periodic bloodwork requires nothing by mouth until the technician comp… | Deferring refueling until a late mid-day meal after collection makes t… | Someone pinned a hospitality meal right after my panel … |
| S9 | `evening_alcohol_x_morning_protocol` | Even two drinks at an evening reception threw off my next-morning rout… | My morning supplement protocol needs food at a consistent time. When t… | Tonight's industry reception lists complimentary cockta… |
| S10 | `desk_prep_portions_x_long_trail` | Weekday staples hold desk blocks but I empty out when output is high.… | The mapped route tomorrow is endurance-length with zero purchase point… | Clear skies for the alpine circuit tomorrow. Will my us… |
| S11 | `cold_plunge_recovery_x_open_water_mile` | Cold plunge after hard training days speeds my recovery — warm-pool-on… | Sports med this month: avoid overhead stroke loads for about four week… | A teammate keeps nudging me toward the bay swim challen… |
| S12 | `probiotic_fasted_x_dawn_rounds` | Refrigerated probiotic capsules on an empty stomach leave me bloated b… | Tuesday hospital rounds start at six-thirty with no food until mid-mor… | Thinking of adding the refrigerated probiotic to my daw… |
| S13 | `natural_wine_x_weekend_inlaw_hosting` | Natural low-sulfite pours trigger flushing and poor sleep for me — con… | Hosting in-laws Saturday through Sunday needs clear-headed mornings fo… | Partner picked something from the guest-weekend case fo… |
| S14 | `fiber_preworkout_x_dawn_interval` | Fiber supplement before vigorous exercise causes mid-session cramping … | Track club moved my interval block to dawn Thursday this month.… | Running-group friends swear by a powder blend tonight b… |
| S15 | `late_dessert_x_fasting_endocrine_checkin` | Late refined-dessert evenings bump my dawn glucose reading above the p… | Endocrinologist check-in Thursday at seven-thirty implies fasting labs… | Guild wants me at a late plated course midweek — okay w… |
| S16 | `oil_kitchen_lunch_x_corridor_vitals_block` | Oil-kitchen lunches leave me sluggish with elevated post-walk glucose … | Wednesday corridor vitals block needs stable post-meal readings — alre… | Worth trying the cafeteria signup line before Wednesday… |
| S17 | `fizz_zero_cal_x_scope_prep_window` | Fizz-heavy zero-cal drinks cause bloating on sensitive gut evenings — … | Friday scope prep window requires clear liquids with minimal bloating … | Hall immersion week before Friday's packet filing cutof… |
| S18 | `crunch_bowl_evening_x_dawn_panel_draw` | Large crunch-bowl evenings cause bloating before dawn blood draws — co… | Thursday dawn panel draw needs a settled morning stomach — late-slot f… | Caterer added a dusk-to-morning signup before Thursday'… |
| S19 | `whole_food_prep_x_blender_demo_night` | I retain portioning skills best with whole-food prep — blender-only pr… | Prior blender-only rehearsal went poorly before skills demo night — I … | Culinary school wants me on the countertop-appliance ru… |
| S20 | `no_snack_transfer_x_stacked_telehealth_week` | Corridor transfers without snacks leave me shaky and foggy — light bar… | Stacked telehealth week requires steady afternoon cognition with no sc… | Worth accepting the heavier no-fuel corridor block this… |

Full evidence quotes + gold + distractor: [`SCENARIOS_S1_S20.md`](SCENARIOS_S1_S20.md).

**Scale:** 600 items (10 users × 20 scenarios × 3 arms).

## Arms

| Arm | `association_type` | Evidence | Gold |
|-----|--------------------|----------|------|
| `associative` | `A3_cross_domain` | ev_A + ev_B | associative recommendation |
| `distractor` | `A3_cross_domain` | ev_A + ev_B + labeled distractor | same C; must ignore lure |
| `absence` | `A5_absence_control` | none | abstain / insufficient evidence |

## Validity gates (measurable)

Stamped in each item’s `validity_metrics` (local TF-IDF proxy; same thresholds as `assomem_pilot/validity_gate.py`):

- **V1** (associative & distractor): Jaccard(query, evidence) ≤ 0.08 · TF-IDF cosine ≤ 0.22 · `flat_rag_hit_top3 == false`
- **V2** (distractor only): `distractor_cosine_query ≥ evidence_cosine_query`
- **Schema**: context turns = `{role, content}` only; `query` ≡ final user turn; no `evolving_state` / forbidden phrases in dialogue

Surface-lure **fillers** (annotation `surface_lure=true`) share query decision vocabulary so flat retrieval tops cue+lures, not evidence — same pattern as the WL/HH pilot.

## Reproduce

```bash
cd assomem_pilot/health_diet
python3 bin/generate_health_diet_batch.py
# → writes ../health/diet_*_user*/ + manifests/; expects SUMMARY 150/150 PASS
```

Loader for model eval (do **not** leak annotation into the prompt):

1. Serialize `context[].dialogue` with only `role` + `content`
2. Strip `annotation`, `persona.evolving_state`, `latent_forbidden_phrases`, `associative_links`, `validity_metrics` from the model-visible input
3. Present `query` as the last user turn (already identical when `query_source=final_turn`)
4. Score answer vs `gold_answer` + `required_elements`
5. Report arm-wise: associative accuracy, distractor resistance, absence abstention rate

## Scoring intent (what a valid AssoMem score means)

- **Associative high**: model co-activates both evidence facts and states the unstated C (not mere keyword RAG).
- **Distractor high**: same C despite a higher surface-similarity lure toward “say yes”.
- **Absence high**: abstains when evidence is missing (no hallucinated bodily pattern).

A model that only does flat lexical retrieval should fail V1-discriminating items; architectures claiming associative memory should lift associative (+ distractor) without collapsing absence.

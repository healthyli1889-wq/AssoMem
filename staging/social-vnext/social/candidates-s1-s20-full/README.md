# Social S1–S20 full batch (20 scenarios × 10 MemoryQuest users × 3 arms)

**600 files** = 20 scenarios × 10 users × 3 arms (`associative` / `distractor` /
`absence`), schema `social-vnext-1.0`. The harness materialises 6 evaluation
conditions per pair, so 1,200 solver-visible conversations.

```
candidates-s1-s20-full/
  associative/AMB_SC_S{1..20}_U{01..10}_associative.json   # 200
  distractor/AMB_SC_S{1..20}_U{01..10}_distractor.json     # 200
  absence/AMB_SC_S{1..20}_U{01..10}_absence.json           # 200
```

Regenerate: `python3 ../generator/generate_s1_s10_full.py`
Audit (Stage 5): `PYTHONPATH=../../vnext_common:generator python3 ../../vnext_common/audit.py --candidates candidates-s1-s20-full --prefix SC`
Ladder (Stages 6–7): `python3 ../../../../experiments/assomem_harness/screen_vnext.py --per-polarity 50`
Aggregate: `python3 ../../vnext_common/aggregate_ladder.py ../review/ladder_full_200.json`

Structure is shared with the hobby batch through `staging/vnext_common/engine.py`;
this tree holds only content.

## The design decision that matters

Every target proposition is **counter-conventional**: A and B jointly license the
answer that generic social advice gets wrong.

- `reject` items propose the conventionally sensible option, which this user's
  episodes show is a poor fit *for them specifically*.
- `accept` items propose the conventionally reckless option, which their episodes
  show actually works.

This is not a stylistic choice. The first version used conventional propositions
("do not go to a big dinner the night before a hard conversation") and failed its
own Stage 7 screen: with both target episodes removed the solver still answered
`yes` on 11 of 16 items. The background was not leaking the episodes — the
proposition simply needed no memory of this person. Every scenario records the
`convention_contradicted` it inverts.

Three structural rules come from measurement, each recorded in the commit that
introduced it:

1. **B does not restate A's antecedent.** A gives trigger → mediator state; B gives
   mediator state → outcome. Neither half alone completes the chain.
2. **Mediator states are valence-neutral.** When A described the state as good or
   bad, ev_A alone carried the conclusion.
3. **`conditional` and `non_decision` bound on a scope condition from ev_A**, not on
   the mediator. Phrased around the mediator, ev_B alone affirmed them.

The `supporting_constraint` sessions of the first version were dropped after an
ablation showed they leaked. The session budget is now exactly DATA CRITERIA §3:
2 targets + 2 counterexamples + 15 background + 1 cue.

## Measured ladder

GPT-5.6-Terra as solver, 164-item stratified sample, all six arms plus the
query-only screen (`../review/ladder_full_200_summary.txt`).

| arm | gold | target-positive rate | | arm | gold | target-positive rate |
|---|---|---|---|---|---|---|
| zero_evidence | no | **0.000** | | link_broken | no | 0.238 |
| full | yes | 0.738 | | a_only | no | 0.341 |
| distractor | yes | 0.744 | | b_only | no | 0.567 |
| | | | | absence | no | 0.055 |

Paired bootstrap over items, 95% CI:

| | point | CI |
|---|---|---|
| Δ_mem = full − absence | **+0.683** | [+0.610, +0.756] |
| Δ_assoc = full − link_broken | **+0.500** | [+0.427, +0.579] |
| full − a_only | +0.396 | [+0.323, +0.470] |
| full − b_only | +0.171 | [+0.104, +0.244] |

All four exclude zero. Δ_assoc excluding zero is the condition for calling this
associative rather than ordinary multi-hop retrieval. Per-scenario Δ_mem is in
`../review/ladder_full_200_summary.txt`.

**Known weakness:** `b_only` at 0.610 is the leakiest arm, concentrated in `accept`
(0.72) and `reject` (0.80). ev_B alone still carries many of those items, so the
full − b_only interval is the narrowest of the four.

## How this differs from the finance batch

| | finance-vnext-2.0 | social-vnext-1.0 |
|---|---|---|
| polarity spread | `reject` 50/100 — breaches the ≤40% rule | 68/68/32/32, within the scaled bands |
| query types | four types at exactly 20/100 | max 36/200 = 18% |
| ev_A / ev_B position | fixed at sessions 6 and 14 batch-wide | varies per scenario |
| bridge types | not recorded | all five, four times each |
| `arm_gold` | `expected_mode` + `binary_decision` only | plus `required_elements` and `rationale` |
| a_only / b_only | rendered by deleting the session | matched neutral replacement, 0.96–1.01 of `full` |
| target proposition | always a decline/defer, whatever the polarity | counter-conventional in both directions |

## Persona anchors

Authoring aids only. No demographic, corpus or location metadata reaches visible
dialogue; the audit fails the batch on any such term.

| Profile | file | anchor | Profile | file | anchor |
|---|---|---|---|---|---|
| U01 | `user0.json` | `mq_user0` | U06 | `user25.json` | `mq_user25` |
| U02 | `user5.json` | `mq_user5` | U07 | `user30.json` | `mq_user30` |
| U03 | `user10.json` | `mq_user10` | U08 | `user35.json` | `mq_user35` |
| U04 | `user15.json` | `mq_user15` | U09 | `user40.json` | `mq_user40` |
| U05 | `user20.json` | `mq_user20` | U10 | `user44.json` | `mq_user44` |

## Scenario families

| S | Family | Bridge type | Convention it inverts |
|---|---|---|---|
| S1 | large-group warm-up vs a rested start before a repair conversation | state_dependent | arrive rested |
| S2 | efficient broadcast updates vs unedited one-to-one rambling | strategy_outcome | clear updates keep people close |
| S3 | one planned sit-down vs several unpolished short catch-ups | threshold_context | one proper dinner beats rushed coffees |
| S4 | a carefully written card vs speaking unprepared | preference_constraint | write it down, it's safer |
| S5 | protected solo recharge vs a house with people in it | prediction_calibration | protect your alone time |
| S6 | an early night vs short sleep before an early commitment | state_dependent | get an early night |
| S7 | a protected clear day vs a day whose plan has broken | threshold_context | keep the day clear to focus |
| S8 | the composed monthly letter vs uncomposed daily reactions | strategy_outcome | a long letter shows real care |
| S9 | an empty house vs company the night before giving guidance | preference_constraint | rest so you give your best advice |
| S10 | arriving fresh vs arriving talked-out at a reunion | prediction_calibration | clear your week, arrive fresh |
| S11 | settling a disagreement in writing vs face to face | state_dependent | do it face to face |
| S12 | constant availability vs scarce, batched attention | strategy_outcome | always be available |
| S13 | keeping a group to its regulars vs bringing a newcomer | threshold_context | don't bring an outsider |
| S14 | turning up out of obligation vs declining once | preference_constraint | just show up |
| S15 | early warning vs telling people once it's settled | prediction_calibration | give people time to prepare |
| S16 | meeting somewhere booked vs hosting unprepared | state_dependent | if you can't host properly, meet out |
| S17 | a one-to-one weekend vs a group trip with a task | strategy_outcome | go one-to-one to reconnect |
| S18 | arriving at the start vs walking into a room already going | threshold_context | arrive early |
| S19 | handling it alone vs asking for help you didn't need | preference_constraint | don't burden friends |
| S20 | abandoning a flop vs running it a second time | prediction_calibration | try something different |

## Status

`review_candidate_only`. Stage 5 passes 200/200, Stage 6 passes 164/164. The batch
has **not** passed Human Gate 1 and is not yet experiment-ready.

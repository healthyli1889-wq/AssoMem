# Social S1–S10 full batch (10 MemoryQuest users × 3 arms)

**300 files** = 10 scenarios × 10 users × 3 arms (`associative` / `distractor` / `absence`),
schema `social-vnext-1.0`. The harness materialises 6 evaluation conditions per pair,
so 600 solver-visible conversations.

```
candidates-s1-s10-full/
  associative/AMB_SC_S{1..10}_U{01..10}_associative.json   # 100
  distractor/AMB_SC_S{1..10}_U{01..10}_distractor.json     # 100
  absence/AMB_SC_S{1..10}_U{01..10}_absence.json           # 100
```

Regenerate: `python3 ../generator/generate_s1_s10_full.py`
Audit (Stage 5): `python3 ../generator/audit_batch.py` → `../review/generation_audit.csv`
Screen (Stages 6–7): `python3 ../../../../experiments/assomem_harness/screen_vnext.py`

## The design decision that matters

Every target proposition is **counter-conventional**: A and B jointly license the
answer that generic social advice gets wrong.

- `reject` items propose the conventionally sensible option, which this user's
  episodes show is a poor fit *for them specifically*.
- `accept` items propose the conventionally reckless option, which their episodes
  show actually works.

This is not a stylistic choice. The first version of this batch used conventional
propositions ("do not go to a big dinner the night before a hard conversation"),
and measured against GPT-5.6-Terra it failed its own Stage 7 screen: with both
target episodes removed the solver still answered `yes` on 11 of 16 items, while
answering `no` on all 16 with an empty context. The background was not leaking the
episodes — the proposition simply needed no memory of this person. Every scenario
therefore records the `convention_contradicted` it inverts.

Two structural rules come from the same failure:

1. **B does not restate A's antecedent.** A gives trigger → mediator state; B gives
   mediator state → outcome. Neither half alone completes the chain.
2. **Counterexamples are not contrastive foils.** Lines like "so it isn't the hour,
   no" presuppose the target pattern and hand it over; they are now ordinary
   neutral episodes.

The v1 `supporting_constraint` sessions were dropped: ablating them showed they
leaked (absence answered `yes` 9/10 with them, 7/10 without). The session budget is
now exactly DATA CRITERIA §3: 2 targets + 2 counterexamples + 15 background + 1 cue.

## How this differs from the finance batch

| | finance-vnext-2.0 | social-vnext-1.0 |
|---|---|---|
| polarity spread | `reject` 50/100 — breaches the ≤40% rule | 34/34/16/16, all within the scaled bands |
| query types | four types at exactly 20/100 | max 18/100 |
| ev_A / ev_B position | fixed at sessions 6 and 14 batch-wide | varies per scenario, so position alone cannot locate targets |
| bridge types | not recorded | all five, twice each |
| `arm_gold` | `expected_mode` + `binary_decision` only | plus `required_elements` and `rationale`, which the harness needs |
| a_only / b_only | rendered by deleting the session | matched neutral replacement, 0.96–1.01 of `full` by length |
| target proposition | always a decline/defer, whatever the polarity | counter-conventional in both directions |

## Persona anchors

Authoring aids only. No demographic, corpus or location metadata reaches visible
dialogue; the audit fails the batch on any such term.

| Profile | MemoryQuest file | anchor | Profile | MemoryQuest file | anchor |
|---|---|---|---|---|---|
| U01 | `user0.json` | `mq_user0` | U06 | `user25.json` | `mq_user25` |
| U02 | `user5.json` | `mq_user5` | U07 | `user30.json` | `mq_user30` |
| U03 | `user10.json` | `mq_user10` | U08 | `user35.json` | `mq_user35` |
| U04 | `user15.json` | `mq_user15` | U09 | `user40.json` | `mq_user40` |
| U05 | `user20.json` | `mq_user20` | U10 | `user44.json` | `mq_user44` |

## Scenario families

| S | Family | Bridge type | Convention it inverts |
|---|---|---|---|
| S1 | large-group warm-up vs a rested start before a repair conversation | state_dependent_operation | arrive rested |
| S2 | efficient broadcast updates vs unedited one-to-one rambling | strategy_outcome_contingency | clear regular updates keep people close |
| S3 | one planned sit-down vs several unpolished short catch-ups | threshold_context_interaction | one proper dinner beats rushed coffees |
| S4 | a carefully written card vs speaking unprepared | preference_constraint_fit | write it down, it's safer |
| S5 | protected solo recharge vs a house with people in it | prediction_calibration | protect your alone time |
| S6 | an early night vs short sleep before an early commitment | state_dependent_operation | get an early night |
| S7 | a protected clear day vs a day whose plan has broken | threshold_context_interaction | keep the day clear to focus |
| S8 | the composed monthly letter vs uncomposed daily reactions | strategy_outcome_contingency | a long letter shows real care |
| S9 | an empty house vs company the night before giving guidance | preference_constraint_fit | rest so you give your best advice |
| S10 | arriving fresh vs arriving talked-out at a reunion | prediction_calibration | clear your week, arrive fresh |

## Status

`review_candidate_only`. Stage 5 passes 100/100. Stages 6–7 measured on a
16-item stratified sample are recorded in the run notes; the batch has **not**
passed Human Gate 1 and is not experiment-ready.

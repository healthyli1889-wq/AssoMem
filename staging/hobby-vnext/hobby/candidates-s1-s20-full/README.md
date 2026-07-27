# Hobby S1–S20 full batch (20 scenarios × 10 MemoryQuest users × 3 arms)

**600 files** = 20 scenarios × 10 users × 3 arms (`associative` / `distractor` /
`absence`), schema `hobby-vnext-1.0`. The harness materialises 6 evaluation
conditions per pair, so 1,200 solver-visible conversations.

```
candidates-s1-s20-full/
  associative/AMB_HB_S{1..20}_U{01..10}_associative.json   # 200
  distractor/AMB_HB_S{1..20}_U{01..10}_distractor.json     # 200
  absence/AMB_HB_S{1..20}_U{01..10}_absence.json           # 200
```

Regenerate: `python3 ../generator/generate_hobby_full.py`
Audit (Stage 5): `PYTHONPATH=../../vnext_common:generator python3 ../../vnext_common/audit.py --candidates candidates-s1-s20-full --prefix HB`
Ladder (Stages 6–7): `python3 ../../../../experiments/assomem_harness/screen_vnext.py --per-polarity 50`

Structure is shared with the social batch through `staging/vnext_common/engine.py`;
this tree holds only content (scenarios, roster, filler, proposition templates).

## Why hobby suits this construct

Every target proposition is **counter-conventional**: A and B jointly license the
answer that generic advice gets wrong. Hobby practice is unusually dense with folk
maxims — "little and often", "buy decent tools", "finish what you start", "join a
group", "practise when fresh" — which is exactly what the design needs. A solver
with no memory of the person applies the maxim and answers `no`, which is gold for
every ablation arm. Only A+B together flip it to `yes`.

- `reject` items propose the conventionally sensible option, which this user's
  episodes show is a poor fit *for them specifically*.
- `accept` items propose the conventionally unwise option, which their episodes
  show actually works.

Each scenario records the `convention_contradicted` it inverts.

Structural rules, each adopted after a measured failure on the social batch:

1. **B does not restate A's antecedent.** A gives trigger → mediator state and
   fixes the scope of that state; B gives mediator state → outcome.
2. **Mediator states are valence-neutral.** When A said whether the state was good
   or bad, ev_A alone carried the conclusion.
3. **`conditional` and `non_decision` bound on the scope condition from ev_A**, not
   on the mediator, which ev_B alone establishes.
4. **Counterexamples are ordinary neutral episodes**, never contrastive foils.

## Measured ladder

GPT-5.6-Terra as solver, 164-item stratified sample, all six arms plus the
query-only screen (`../review/ladder_full_200_summary.txt`).

| arm | gold | target-positive rate | | arm | gold | target-positive rate |
|---|---|---|---|---|---|---|
| zero_evidence | no | **0.000** | | link_broken | no | 0.311 |
| full | yes | 0.866 | | a_only | no | 0.616 |
| distractor | yes | 0.835 | | b_only | no | 0.640 |
| | | | | absence | no | 0.091 |

Paired bootstrap over items, 95% CI:

| | point | CI |
|---|---|---|
| Δ_mem = full − absence | **+0.774** | [+0.707, +0.835] |
| Δ_assoc = full − link_broken | **+0.555** | [+0.476, +0.634] |
| full − a_only | +0.250 | [+0.183, +0.323] |
| full − b_only | +0.226 | [+0.159, +0.293] |

All four exclude zero. Compared with the social batch this one has a higher
ceiling (`full` 0.866 against 0.744), a larger Δ_assoc, and — the more useful
difference — **balanced single-evidence arms**: a_only and b_only sit within 0.024
of each other, where social's b_only leaked far more than its a_only.

**Known weakness:** both single-evidence arms are high in absolute terms, driven by
`reject` (a_only 0.80, b_only 0.86) and by `accept` on b_only (0.92). `conditional`
and `non_decision` are the cleanest polarities here (absence 0.00 on both).

## Persona anchors

The same MemoryQuest respondents as the social batch, read through their Games /
Music / Sports / Shopping summaries so each profile gets a craft they practise.
Authoring aids only: no demographic, corpus or location metadata reaches visible
dialogue, and the audit fails the batch on any such term.

| Profile | file | craft | Profile | file | craft |
|---|---|---|---|---|---|
| U01 | `user0.json` | guitar | U06 | `user25.json` | production |
| U02 | `user5.json` | producing | U07 | `user30.json` | sampler |
| U03 | `user10.json` | bass | U08 | `user35.json` | fiddle |
| U04 | `user15.json` | mandolin | U09 | `user40.json` | keyboard |
| U05 | `user20.json` | pottery wheel | U10 | `user44.json` | modular synth |

## Scenario families

| S | Family | Bridge type | Convention it inverts |
|---|---|---|---|
| S1 | practising fresh vs practising worn out | state_dependent | practise when fresh |
| S2 | finishing vs abandoning and cannibalising | strategy_outcome | finish what you start |
| S3 | thirty minutes daily vs one long block | threshold_context | little and often |
| S4 | the weekly group vs solo practice | preference_constraint | join a group |
| S5 | buying decent gear vs keeping the battered one | prediction_calibration | buy decent tools |
| S6 | a quiet studio vs a busy room | state_dependent | set up a quiet space |
| S7 | one project at a time vs a second alongside | threshold_context | one thing at a time |
| S8 | a structured course vs going in blind | strategy_outcome | follow a proper course |
| S9 | keeping work private vs posting it rough | preference_constraint | don't share until it's good |
| S10 | open-ended time vs a hard deadline | prediction_calibration | creative work needs no pressure |
| S11 | better players vs being the strongest present | state_dependent | play with people better than you |
| S12 | keeping a practice log vs not measuring | strategy_outcome | what gets measured gets improved |
| S13 | sticking to one pursuit vs several at once | threshold_context | pick one thing |
| S14 | working at your level vs teaching a beginner | preference_constraint | don't waste time on beginners |
| S15 | ticking over vs a long lay-off | prediction_calibration | don't take long breaks |
| S16 | first thing in the morning vs very late | state_dependent | work in the morning |
| S17 | original from scratch vs copying closely | strategy_outcome | don't copy others |
| S18 | using what you have vs buying far too much | threshold_context | buying more is procrastination |
| S19 | keeping it for fun vs being judged by strangers | preference_constraint | keep hobbies non-competitive |
| S20 | new repertoire vs repeating one piece | prediction_calibration | keep learning new material |

## Status

`review_candidate_only`. Stage 5 passes 200/200, Stage 6 passes 164/164. The batch
has **not** passed Human Gate 1 and is not yet experiment-ready.

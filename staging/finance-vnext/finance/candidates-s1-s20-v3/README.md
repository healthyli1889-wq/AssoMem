# Finance S1–S20 v3 batch (20 scenarios × 10 MemoryQuest users × 3 arms)

**600 files** = 20 scenarios × 10 users × 3 arms (`associative` / `distractor` /
`absence`), schema `finance-vnext-3.0`. Six evaluation conditions per pair, so
1,200 solver-visible conversations.

```
candidates-s1-s20-v3/
  associative/AMB_FN_S{1..20}_U{01..10}_associative.json   # 200
  distractor/AMB_FN_S{1..20}_U{01..10}_distractor.json     # 200
  absence/AMB_FN_S{1..20}_U{01..10}_absence.json           # 200
```

Regenerate: `python3 ../generator/generate_finance_full.py`
Audit (Stage 5): `PYTHONPATH=../../vnext_common:generator python3 ../../vnext_common/audit.py --candidates candidates-s1-s20-v3 --prefix FN`
Ladder: `python3 ../../../../experiments/assomem_harness/screen_vnext.py --per-polarity 50`

## Why this is a rebuild and not an edit

`finance-vnext-2.0` (300 files, S1–S10) was measured against GPT-5.6-Terra on its
own published run. Recomputed with the same quantity on both arms:

| | v2 | **v3** |
|---|---|---|
| Δ_assoc = full − link_broken | +0.068 (**+0.000** under kimi-k3 alone) | **+0.506** |
| Δ_mem = full − absence | +0.403 | **+0.768** |
| absence target-positive | 0.589 | **0.110** |
| link_broken target-positive | 0.920 | 0.372 |

v2's problem was not the harness. Every v2 `latent_C` was a decline-or-defer
whatever the polarity, so ordinary financial caution answered the batch with no
memory of the person: the absence arm still asserted the target on 59% of items.
Re-running v2 could not have fixed that.

## The design

Every target proposition is **counter-conventional**: A and B jointly license the
answer generic financial advice gets wrong. Personal finance is the densest
folk-wisdom domain of the five — automate your savings, budget every category,
never lend to friends, always take the match — which makes the answer a
memory-less solver reaches for sharply defined. Each scenario records the
`convention_contradicted` it inverts.

- `reject` items propose the conventionally sensible option, which this user's
  episodes show is a poor fit *for them*.
- `accept` items propose the conventionally unwise option, which works for them.

Structural rules carried over from the social and hobby batches, each adopted
after a measured failure: B never restates A's antecedent; mediator states are
valence-neutral; `conditional` and `non_decision` bound on a scope condition from
ev_A; counterexamples are neutral episodes rather than contrastive foils. The v2
`supporting_constraint` sessions are gone — ablating the equivalent sessions in
the social batch showed they leak.

Several propositions invert advice that is sound in aggregate (taking the full
employer match, consolidating debt). The claims are bounded to one person and one
stated goal, which `calibrated_language` carries. This is a memory benchmark, not
financial guidance.

## Measured ladder

GPT-5.6-Terra, 164-item stratified sample, six arms plus the query-only screen
(`../review/ladder_v3_200_summary.txt`).

| arm | gold | rate | | arm | gold | rate |
|---|---|---|---|---|---|---|
| zero_evidence | no | **0.000** | | link_broken | no | 0.372 |
| full | yes | 0.878 | | a_only | no | 0.640 |
| distractor | yes | 0.866 | | b_only | no | 0.720 |
| | | | | absence | no | 0.110 |

| | point | CI |
|---|---|---|
| Δ_mem = full − absence | **+0.768** | [+0.701, +0.829] |
| Δ_assoc = full − link_broken | **+0.506** | [+0.427, +0.585] |
| full − a_only | +0.238 | [+0.171, +0.311] |
| full − b_only | +0.159 | [+0.091, +0.226] |

All four exclude zero.

**Known weakness:** the `reject` polarity leaks badly on both single-evidence arms
(a_only 0.92, b_only 0.98) while `conditional` and `non_decision` are clean
(absence 0.00 on both). The same pattern appears in social and hobby, so it is a
property of the reject framing rather than of this domain.

## Scenario families

| S | Convention it inverts | S | Convention it inverts |
|---|---|---|---|
| S1 | automate your savings | S11 | pay by card, it's tracked |
| S2 | one account, keep it simple | S12 | consolidate at a lower rate |
| S3 | don't check often, you'll panic-sell | S13 | never pay full price |
| S4 | keep your finances private | S14 | always take the full match |
| S5 | budget every category | S15 | buying beats renting |
| S6 | pay annually for the discount | S16 | pay bills on payday |
| S7 | keep a buffer in the current account | S17 | get a financial adviser |
| S8 | track every expense | S18 | one savings account |
| S9 | never lend to friends | S19 | buy the cheap generic |
| S10 | buy in bulk | S20 | sit tight through a downturn |

## Status

`review_candidate_only`. Stage 5 passes 200/200, Stage 6 passes 164/164. Not yet
through Human Gate 1. The v2 batch is left in place at
`../candidates-s1-s10-full/` for comparison.

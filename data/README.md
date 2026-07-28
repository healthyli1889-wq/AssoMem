# Benchmark items

3,000 JSON records: 5 domains × 200 units × 3 source arms.

```
data/<domain>/associative/<PAIR_ID>_associative.json    # 200 per domain
data/<domain>/distractor/<PAIR_ID>_distractor.json      # 200
data/<domain>/absence/<PAIR_ID>_absence.json            # 200
```

| domain | schema_version | pair ids | structure |
|---|---|---|---|
| social | `social-vnext-1.0` | `AMB_SC_S{1..20}_U{01..10}` | 20 scenarios × 10 profiles |
| hobby | `hobby-vnext-1.0` | `AMB_HB_S{1..20}_U{01..10}` | 20 scenarios × 10 profiles |
| finance | `finance-vnext-3.0` | `AMB_FN_S{1..20}_U{01..10}` | 20 scenarios × 10 profiles |
| work | `work-vnext-2.0` | `AMB_WV_S{01..20}_U{01..10}` | 20 scenarios × 10 profiles |
| health | `assomem-vnext-1.2` | `AMB_HV_<slug>_<nnn>` | 200 individually-slugged units |

The three files of a pair agree on `pair_id`, `domain`, `user_id`, `query`,
`query_type`, `polarity`, `latent_C` and `answer_contract`; they differ only in the
context, per the arm rules in `../code/spec/DATA_CRITERIA.md` §5.

## Record shape

Solver-visible: `context` (20 dated sessions of `{role, content}` turns) and
`query` (identical to the final user turn). Everything else is held back by
`dataset.solver_input`, which also passes `answer_contract.target_proposition` —
the question, never the answer.

Review-only fields:

| field | what it is for |
|---|---|
| `evidence.ev_A` / `ev_B` | the two target episodes, with owner and session id |
| `episode_annotations` | per-session role: `ev_A`, `ev_B`, `background_memory`, `nearby_counterexample`, `supporting_constraint`, `distractor`, `retrieval_cue`, plus five event elements on each target |
| `relational_connector` | the relation, and which evidence it requires |
| `connector_spans` | the exact visible quote in each target that instantiates it |
| `relation_specificity` | a nearby relation that must *not* license C, and why |
| `coactivation_bridge` | why A+B jointly license C and nothing else does |
| `latent_C` | the inference, and the calibrated language it must stay inside |
| `answer_contract` | the binary proposition, allowed decisions, decision semantics |
| `arm_gold` | expected mode and binary decision per condition |
| `single_evidence_replacements` | matched neutral sessions for `a_only` / `b_only` |
| `link_broken` | B-prime: same owner, date and turn count, relation removed |
| `distractor_note` / `absence_note` | which session was swapped, and why |
| `convention_contradicted` | social / hobby / finance only: the maxim the proposition inverts |
| `sub_scenario` | family, role, bridge type, one-line summary |

Five bridge types are used, four scenarios each in the grid domains:
`state_dependent_operation`, `strategy_outcome_contingency`,
`threshold_context_interaction`, `preference_constraint_fit`,
`prediction_calibration`.

## Quotas

Query type and polarity are frozen before any dialogue is written
(`../code/generators/vnext_common/allocation.py`), and `audit.py` fails the batch
on a breach.

| | social / hobby / finance | work | health |
|---|---|---|---|
| accept | 68 | 60 | 41 |
| reject | 68 | 80 | 80 |
| conditional | 32 | 40 | 39 |
| non_decision | 32 | 20 | 40 |
| max query type | 36 (18%) | 36 (18%) | 40 (20%) |
| min query type | 32 (16%) | 32 (16%) | **1 (0.5%)** |

health's `preference_generalization` appears once in 200 items; the other five
types sit at 39–40. The ≤20% ceiling holds, but that type is effectively untested
there.

## The design decision behind social, hobby and finance

Every target proposition in those three domains is **counter-conventional**: A and
B jointly license the answer that generic domain advice gets wrong. `reject` items
propose the conventionally sensible option and the person's episodes show it is a
poor fit for them; `accept` items propose the conventionally unwise option that
works for them. `convention_contradicted` records the maxim inverted.

This was not a stylistic choice. An earlier social batch used conventional
propositions and failed its own single-evidence screen: with both target episodes
removed, the solver still asserted the target on 11 of 16 items while answering
"no" on all 16 with an empty context. The background was not leaking the episodes —
the proposition simply needed no memory of the person. Three structural rules come
from the same measurement:

1. **B does not restate A's antecedent.** A gives trigger → mediator state and
   fixes the scope of that state; B gives mediator state → outcome. Neither half
   alone completes the chain.
2. **Mediator states are valence-neutral.** When A said whether the state was good
   or bad, ev_A alone carried the conclusion.
3. **`conditional` and `non_decision` propositions bound on a scope condition drawn
   from ev_A**, not on the mediator — ev_B alone establishes the mediator.

Counterexample sessions are ordinary neutral episodes, never contrastive foils: a
line like "so it isn't the hour, no" presupposes the target pattern and hands it to
the solver.

## Regenerating

social, hobby and finance are fully deterministic — no model calls, no randomness,
no clock:

```bash
cd code/generators/social && python3 generate_s1_s10_full.py --out /tmp/social
cd ../hobby   && python3 generate_hobby_full.py   --out /tmp/hobby
cd ../finance && python3 generate_finance_full.py --out /tmp/finance
cd .. && PYTHONPATH=vnext_common:social python3 vnext_common/audit.py \
        --candidates /tmp/social --prefix SC --scenarios 20
```

work and health were authored separately and ship as data only. The work B-prime in
this release was rebuilt by `code/tools/rewrite_bprime.py`, which derives each
replacement from the item's own event elements; the original is recoverable by not
applying it.

## Fields removed for this release

Authoring aids and bookkeeping that no code here reads and that bear on no result:
`provenance.voice`, `provenance.external_folder_tag`, and on health
`available_evaluation_conditions` plus `provenance.{source_person_name,
source_corpus, materialized_from, authoring_method, created_at,
anonymous_submission, source_data_arm, release_eligible, gate_0_review_path,
gate_0_review_unit}`. Fields that document the construct are kept even where no
code reads them, because a reviewer does.

## Provenance and anonymisation

`provenance.persona_anchor` records which respondent of a public longitudinal
survey corpus a profile was grounded in during authoring. No demographic, corpus or
location metadata reaches any visible dialogue turn; `audit.py` fails the batch on
any such term, and the release was scanned again on assembly.

Dialogue is shipped exactly as authored. One work item gives a synthetic co-worker
an invented first name; it identifies nobody and was left as written.

All items carry `provenance.status: review_candidate_only`.

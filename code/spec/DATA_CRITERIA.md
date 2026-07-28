# Work vNext S1–S5, ten-profile, three-source-arm generation criteria

## 0. Scope, count, and non-goals

### Deliverable count

This batch has **50 base associative-memory units**:

```text
5 scenario families (S1–S5) × 10 anonymous user profiles (U01–U10) = 50 units
50 units × 3 source data arms = 150 JSON files
```

The three **source data arms** are:

1. `associative`
2. `distractor`
3. `absence`

They are not the same as solver evaluation conditions. The `associative` source
supports four associative ablations:

1. `full`: both A and B are available;
2. `a_only`: B is replaced by a neutral, matched-length non-target session;
3. `b_only`: A is replaced by a neutral, matched-length non-target session;
4. `link_broken`: B is replaced by B-prime, which preserves the user, chronology,
   session form, and approximate length while breaking the A–B connector.

Every source context contains exactly 20 dated dialogue sessions. Derived
ablations preserve the same session count through matched neutral replacements.
The `distractor` and `absence` files remain separate source controls; their
evaluation scheduling is outside the scope of this generation criterion.

`query_only` is a pre-screening gate, not a source arm or a fifth evaluation
condition. The solver sees Q without dialogue context; an item that succeeds above
the pre-registered guessing baseline must be revised or rejected.

### What this batch does not do

- It does not reuse legacy `src/data/work` items.
- It does not copy the old pre-Gate-0 illustrative candidate.
- It does not run the full solver/validator pipeline.
- It does not claim a neural or biological measurement. It creates a behavioral
  proxy for person-bound relational inference.
- It does not use `source_swap`; source monitoring is outside this three-source-arm
  batch.

## 1. Directory and naming contract

All new files live only below:

```text
staging/work-vnext/v2/
├── DATA CRITERIA_new.md
├── matrix/
│   ├── scenario_matrix.csv
│   ├── profile_matrix.csv
│   └── allocation_audit.csv
├── candidates/
│   ├── associative/
│   ├── distractor/
│   └── absence/
├── review/
│   ├── gate_0_scenario_matrix.csv
│   ├── gate_1_source_data.csv
│   └── generation_audit.csv
└── artifacts/
    └── <pair_id>/
```

File and pair naming:

```text
pair_id:       AMB_WV_S{01..05}_U{01..10}
associative:   candidates/associative/AMB_WV_S##_U##_associative.json
distractor:    candidates/distractor/AMB_WV_S##_U##_distractor.json
absence:       candidates/absence/AMB_WV_S##_U##_absence.json
```

No runtime logs, API configuration, keys, archive files, or legacy source data may
be written into this tree.

## 2. Data-unit criterion: what every one of 50 units must prove

Each base unit must contain five distinct elements:

| Element | Required content | Rejection rule |
|---|---|---|
| A | One dated, user-owned episodic event with person, context/time, goal, action, outcome/affect. | It is merely a generic trait, preference, or static persona label. |
| B | A different dated, user-owned episodic event with the same five event elements. | It occurs in the same session as A, belongs to someone else, or repeats A. |
| Bridge R | A recoverable relation/contingency between A and B, grounded in visible spans from both. | It is only an author assertion such as “both imply C.” |
| C | A novel, calibrated, binary target proposition about the same user. | It is explicitly stated or nearly paraphrased in context/query, or is a broad identity claim. |
| Q | A natural work-domain recall cue requesting a binary decision about C without naming A, B, R, or C. | It exposes the answer, names the episodes, or is answerable by generic workplace advice alone. |

The central logical requirements are mandatory:

```text
A alone does not support C.
B alone does not support C.
A + B jointly support C.
A + B-prime no longer supports C.
No target episode supports C in absence.
```

## 3. Person-bound associative-memory criterion

### Required event structure

For both A and B, annotate:

```text
person
time/context
goal_or_prediction
action
outcome_or_affect
```

The user must have a multi-session work history beyond A and B. Every source and
every rendered ablation context contains **exactly 20 dated sessions**:

- 2 target episodes (A and B);
- 16 ordinary background episodes spanning at least three distinct work
  contexts/times;
- 2 nearby counterexamples that constrain overgeneralization.

Background must be relevant enough to establish a person, but insufficient to
replace A or B. It must never state C, a diagnosis, a stable trait label, or a
hidden “correct preference.”

The 20-session requirement is a length-control contract. In `a_only`, `b_only`,
`link_broken`, `distractor`, and `absence`, any removed or changed session must be
replaced with a dated, same-user, non-target session of comparable turn count and
length. A condition may not gain or lose sessions merely because of the
intervention.

### Valid bridge types

Every bridge must be one of these operational forms, with an explicit
counterfactual B-prime:

1. **State-dependent operation:** A identifies a stable work/recovery state; B
   shows a selective performance consequence under a matching demand.
2. **Strategy–outcome contingency:** A shows how the user preserves performance;
   B shows failure when a required setting blocks that strategy.
3. **Threshold/context interaction:** A identifies a demand threshold; B identifies
   a different episode crossing that threshold with a specific consequence.
4. **Preference–constraint fit:** A shows a recurring value/strategy; B shows a
   concrete cost when a work arrangement violates it.
5. **Prediction calibration:** A shows a past self-prediction and outcome; B gives
   a second event that calibrates when that prediction generalizes.

Invalid bridge forms:

- two independent negatives pointing to “reject”;
- keyword/topic overlap without a shared contingency;
- two facts from different people;
- generic world knowledge such as “sleep deprivation is bad”;
- a relation declared only in metadata.

## 4. Scenario, profile, query, and polarity allocation

### Scenario families (S1–S5)

Each scenario ID represents one work-demand family, not one repeated answer shape:

| Scenario | Work-demand family | Required difference from S1 |
|---|---|---|
| S1 | Fixed early live dependency prioritization | Time/complexity fit |
| S2 | Escalation ownership under ambiguous evidence | Uncertainty calibration |
| S3 | Interrupt-driven task switching | Context-switch threshold |
| S4 | Asynchronous versus live collaboration | Communication-medium fit |
| S5 | Deadline compression with quality tradeoffs | Speed/accuracy threshold |

A scenario family is rejected if its ten profiles only substitute a job title,
clock time, or object while preserving the same A/B/R/C logic.

### Ten user profiles per scenario

For each scenario, U01–U10 must differ in their **event histories and bridge**, not
only their names. At least three of the following must change across profiles:

- work role/context;
- A’s operation or strategy;
- B’s demand/failure or outcome;
- bridge type;
- query wording;
- target polarity;
- nearby counterexample.

Do not make a profile a demographic label. Use anonymous IDs only and never include
names, source locations, corpus identifiers, or personal metadata.

### Query-type quota across 50 base units

| Query type | Required count |
|---|---:|
| `preference_generalization` | 8 |
| `situational_fit` | 8 |
| `recommendation_ranking` | 8 |
| `predicted_reaction` | 8 |
| `behavior_explanation` | 9 |
| `conditional_recommendation` | 9 |

No query type exceeds 20% of the batch. Query wording must not follow one repeated
template such as “should the user reject X?”

### Polarity quota

Across the 50 full conditions, no polarity exceeds 40%:

- `accept`: 15–20
- `reject`: 15–20
- `conditional`: 5–15
- `non_decision`: 5–15

Every target remains binary at evaluation time. For a conditional/non-decision
query, write a specific proposition that can still be answered `yes` or `no`;
do not output `conditional` as a solver decision.

## 5. Three source-arm construction rules

### 5.1 Associative source

**Action:** Author the complete 20-session same-user history, A/B annotations,
bridge, C, query, binary contract, B-prime replacement dialogue, and four core
gold entries.

**Must contain**

- `full = yes` only when A+B support C;
- `a_only = no`;
- `b_only = no`;
- `link_broken = no`;
- matched neutral replacement sessions for both `a_only` and `b_only`;
- exact `connector_spans` for A and B;
- a nearby relation that does not license C;
- B-prime with matched chronology, owner, task shape, approximate turn/length, and
  a changed connector only.

**Reject if**

- either single-evidence gold is `yes`;
- C can be recovered from background alone;
- an A-only/B-only replacement exposes a paraphrase of the removed target episode
  or changes context length;
- B-prime deletes B, changes speaker, changes context length, makes obvious
  formatting changes, or changes multiple causal factors;
- the query contains C or a direct paraphrase.

### 5.2 Distractor source

**Action:** Clone the associative source and replace one pre-designated neutral
background session with one dated, user-owned distractor session that is plausibly
relevant to the query but does not support R or C. The source remains exactly
20 sessions long.

**Must preserve**

- A/B sessions, their IDs, query, answer contract, full target, and the 20-session
  count;
- `distractor = yes` where the associative full condition is yes;
- one `why_distractor` explanation identifying why it is tempting and why it is
  non-diagnostic.

**Reject if**

- the distractor restates A, B, R, C, or a direct summary;
- it changes context length, A/B, the target connector, or the answer contract;
- it makes the answer trivially more obvious;
- it is irrelevant enough that no realistic solver would attend to it.

### 5.3 Absence source

**Action:** Start from the associative history; replace both target sessions A and
B with two dated, same-user, neutral sessions matched in approximate turn count and
length. Retain the background history, query, and binary contract. The source
remains exactly 20 sessions long.

**Must contain**

- `target_evidence_ids: []`;
- explicit withheld IDs `ev_A`, `ev_B`;
- `absence = no`;
- background that remains coherent without the target episodes.

**Reject if**

- either A/B content, paraphrase, assistant summary, or bridge survives;
- either replacement session is visibly marked as a placeholder or changes the
  session count;
- absence has no meaningful user history;
- `no` is incorrectly framed as “the work arrangement is good.”

## 6. Required JSON fields and pair-consistency audit

Every source JSON must include:

```text
schema_version, candidate_id, pair_id, data_arm, domain, user_id,
query_type, polarity, context, query, evidence, episode_annotations,
relational_connector, connector_spans, retrieval_cue, relation_specificity,
coactivation_bridge, latent_C, answer_contract, arm_gold, provenance
```

The three files in one pair must agree on:

```text
pair_id, domain, user_id, query, query_type, polarity,
latent_C, answer_contract, shared timeline structure, and session count
```

The context and target-evidence visibility differ only according to the arm rules
in Section 5. The absence file may not retain target evidence IDs or target facts.

## 7. Generation workflow: exact actions and stop rules

| Stage | Concrete action | Output | Stop / reject criterion |
|---|---|---|---|
| 0. Batch freeze | Create scenario/profile/allocation matrices before writing dialogue. | 50-row matrix with scenario, profile, bridge, query type, polarity. | Any quota breach or repeated underlying logic. |
| 1. Scenario gate | Write one short construct card for each S1–S5: A role, B role, bridge, C boundary, query family, B-prime mechanism. | 5 scenario cards. | C is a generic preference or scenario repeats another family. |
| 2. Profile outline | For each scenario, outline ten non-clone user histories with exactly 20 dated sessions. | 50 A/B/R/C/Q outlines. | A/B are not event-complete, the session count differs from 20, or no nearby counterexample exists. |
| 3. Associative authoring | Author the associative JSON and its four core arm gold entries. | 50 associative JSONs. | Schema failure, direct C leak, single-evidence sufficiency, invalid B-prime. |
| 4. Source derivation | Produce one distractor and one absence JSON from each validated associative source. | 50 distractor + 50 absence JSONs. | Pair fields diverge; distractor diagnoses C; absence retains target evidence. |
| 5. Deterministic audit | Validate schema, timestamps, source consistency, 20-session counts, arm gold, matched replacements, connector span visibility, and anonymization. | `generation_audit.csv`. | Any error blocks that pair. |
| 6. Query-only screen | Run the solver on Q with empty context for the defined trial count. | Per-pair zero-evidence artifact. | Target-positive rate above the pre-registered threshold (default 0). |
| 7. Single-evidence screen | Run solver on rendered A-only and B-only after zero-evidence passes. | Per-pair control artifact. | Either single-evidence condition shows materially above-chance target-positive behavior. |
| 8. Human Gate 1 | Reviewer reads A/B/R/C/Q and all three source files; records explicit clauses. | Signed `gate_1_source_data.csv`. | Any clause missing, failed, or lacks reviewer name. |
| 9. Link-broken audit | Render B-prime and compare owner, timestamps, session count, turn count, length, query, and surface task with full. Audit the neutral A-only/B-only replacements by the same length and naturalness criteria. | Link-broken audit record. | Difference is source, format, broad content, or context length rather than connector. |
| 10. Exemplar learning gate | Review S1 results and document concrete revisions before authoring the remaining batch at scale. | S1 learning record + explicit automation authorization. | No signed authorization; later scenarios remain drafts only. |

Stages 6–10 are evaluation gates, not permission to silently edit source data after
seeing model scores. A failed item is quarantined, revised under a new candidate
version, and re-audited from Stage 3.

## 8. Human review checklist for every generated pair

The reviewer must answer every item `pass` or `fail`, with notes:

1. Are A and B temporally distinct, same-user, event-complete memories?
2. Is R visible/recoverable from exact spans in both A and B?
3. Does A alone fail to support C?
4. Does B alone fail to support C?
5. Does full A+B support only the calibrated C, not a broader claim?
6. Does Q naturally retrieve R without leaking A, B, R, C, or gold direction?
7. Does B-prime break R while preserving user, chronology, task form, and surface
   plausibility?
8. Does distractor plausibly compete for attention while remaining non-evidential?
9. Does absence remove all target evidence while retaining coherent background?
10. Is every field anonymous and free of source-path, name, or corpus leakage?
11. Do query-type and polarity allocations remain within batch quota?
12. Is the item distinct from the other nine profiles in its scenario and from the
    other four scenario families?
13. Does every source and every rendered associative ablation retain exactly 20 natural,
    dated sessions, including matched neutral replacements where required?

## 9. Batch completion definition

The generation phase is complete only when:

```text
50 associative + 50 distractor + 50 absence JSONs exist;
every source file has exactly 20 dated sessions;
all 50 associative sources render full, A-only, B-only, and link-broken contexts
with exactly 20 sessions each;
all 50 pairs pass deterministic validation;
all 50 pairs have allocation and provenance records;
no legacy item, archive, API key, or runtime log is in v2;
S1 has an approved learning record before broad automation proceeds.
```

The batch is not “experiment-ready” until the relevant human and model gates in
Section 7 have passed.

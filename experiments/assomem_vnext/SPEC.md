# Work vNext: same-person associative-memory specification

## Purpose

Work vNext measures whether an agent can jointly retrieve two temporally separate
memories about **one person** to make a calibrated, previously unstated inference.
It does not measure whether an agent can add two independent reasons to reject an
option, nor whether it can keep two speakers' facts separate.

## Unit of data

Each candidate contains:

```text
A: one dated, user-owned episodic fact
B: a different dated, user-owned episodic fact
bridge: the explicit relational rationale linking A and B
C: a novel, calibrated inference about that same user
Q: a natural recall cue that calls for C
```

The benchmark must establish all of the following:

1. A alone does not license C.
2. B alone does not license C.
3. A and B jointly license C.
4. C is not stated or near-paraphrased in any visible pre-query session.
5. Q does not name A, B, or C and is a realistic reason to recall the user.

Example:

```text
A: The user repeatedly chooses Japanese food for celebrations.
B: Tokyo is the user's favorite city and they revisit it in planning conversations.
C: A Japanese-culture activity is likely to be a strong fit.
Q: Which cultural activity should I prioritize for this person?
```

C is a calibrated recommendation ("likely", "worth prioritizing"), not a claim that
the user explicitly stated a broad Japanese-culture identity.

## Mechanistic operationalization and its limit

This is a **behavioral proxy**, not a neural measurement. Text-only evaluation cannot
show hippocampal replay, CA1 activity, or biological co-activation. The defensible
claim is narrower: a response exhibits the behavioral signature expected from
relational memory if a partial, natural cue requires retrieval and recombination of
two distinct person-bound episodes, and matched controls remove that relation.

For every eligible candidate, each evidence episode must annotate:

```text
person + time/context + goal or prediction + action + outcome/affect
```

The candidate must additionally expose, for review (but not necessarily to the
solver as metadata):

```text
relational_connector: the shared event role/contingency that links A and B
connector_spans: exact visible spans from A and B that instantiate it
retrieval_cue: why Q can retrieve the connector without restating A, B, or C
relation_specificity: a nearby, semantically similar relation that must not license C
```

The connector cannot be merely an author-written summary such as “both show a
feedback loop.” It must be recoverable from the two visible episodes. `link_broken`
changes that connector only; it does not replace the topic, owner, or narrative
format. The answer rubric must require evidence from **both** episode spans and
reject a generic-prior answer that reaches C without them.

## Arm semantics

| Arm | Visible memory | Expected behavior | What it tests |
|---|---|---|---|
| `full` | A and B, same user | Make calibrated C | joint co-activation |
| `a_only` | A only | Do not establish C | A insufficiency |
| `b_only` | B only | Do not establish C | B insufficiency |
| `link_broken` | A and B remain user-owned and matched, but their relation no longer licenses C | Do not establish original C | relation/bridge necessity |
| `source_swap` | One fact is attributed to another person | Do not bind it to the user | source monitoring only |

`source_swap` is deliberately not a synonym for `link_broken`.

## Link-broken requirements

A link-broken arm must preserve:

- the user's identity and speaker ownership;
- approximate number of sessions, turn count, chronology, and context length;
- an A-like and B-like personal fact;
- query wording and expected response format.

It must change only the relational feature that makes A+B support C. A hard textual
prefix, deleting an evidence session, or reassigning a fact to a friend is not a
valid link-broken transformation.

## Query taxonomy and quotas

Every candidate receives exactly one query type:

1. `preference_generalization`
2. `situational_fit`
3. `recommendation_ranking`
4. `predicted_reaction`
5. `behavior_explanation`
6. `conditional_recommendation`

At release, no type or polarity (`accept`, `reject`, `conditional`, `non_decision`)
may exceed 40% of a batch. The former "two constraints → decline" pattern is
prohibited.

## Gates

The first eligible exemplar is manually reviewed at every node. The normative
automation boundary is in [HUMAN_GATES.md](HUMAN_GATES.md); actual decisions live
with the candidate under `artifacts/<candidate_id>/review/gate_0.csv` through
`gate_5.csv`.

Its status sequence is:

```text
human_gate_0 → author → human_gate_1 → independent_evaluator
             → human_gate_2 → rendered_arm_audit → human_gate_3
             → behavioral_proof → human_gate_4 → exemplar_freeze
             → human_gate_5 → release_candidate
```

Only a signed `automation_authorization.json`, written after a frozen exemplar has
produced a documented learning record, can relax a specified *non-publication*
step for later candidates. An evaluator average is never sufficient: every core
clause must score at least 96/100.

## What reviewers see

Each gate receives a compact packet containing A, B, bridge, C, Q, all rendered
arms, deterministic findings, strict evaluator scores and evidence spans. Reviewers
approve individual clauses; they do not approve a vague overall impression.

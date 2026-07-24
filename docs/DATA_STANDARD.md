# AssoMemBench Data Standard

## 1. Purpose

AssoMemBench measures **associative personal memory**, not generic semantic association,
ordinary multi-hop question answering, or advice quality.

A valid item asks whether a system can use two temporally separate memories about the
**same target user** to co-activate an unstated, user-specific conclusion.

```text
ev_A(user) + ev_B(user) --typed relation--> latent_C(user) --> answer
```

The conclusion must be unsupported if either necessary memory is removed, replaced, or
attributed to somebody other than the target user.

## 2. Associative Memory Is Not Generic Association

Semantic association may span people. Associative personal memory is person-indexed.

Example:

```text
Alex likes Japanese food.
The target user's favorite city is Tokyo.
```

These facts may activate related concepts about Japan, but they do **not** support:

```text
The target user likes Japanese culture.
```

The food preference belongs to Alex, not the target user. A model that reaches that
conclusion commits `source_misattribution`.

In contrast:

```text
The target user likes Japanese food.
The target user's favorite city is Tokyo.
```

may support a calibrated hypothesis about the target user's Japanese-culture interest,
provided the item passes the counterfactual checks below.

## 3. Core Concepts

| Term | Definition |
|---|---|
| Target user | The person the final query asks about. All user-specific conclusions refer to this person. |
| `ev_A`, `ev_B` | Two temporally separated atomic memories. Each must provide a distinct necessary contribution. |
| Typed relation | The relation connecting memories: causal, temporal, constraint, analogical, or source/identity. “Related” is not enough. |
| `latent_C` | A user-specific inference not explicitly stated in the visible conversation. |
| Co-activation | Retrieval of one evidence makes the other relevant under a typed relation, enabling `latent_C`. |
| Association | Semantic or lexical relatedness. It can occur across people and is insufficient by itself. |
| Source identity | Who a fact is about. It is part of a memory, not optional metadata. |

## 4. Valid FULL Item Requirements

Every FULL item must satisfy all of the following.

1. **Same-person binding**: `ev_A.owner == ev_B.owner == target_user`.
2. **Distinct contribution**: `ev_A` and `ev_B` are not duplicate support for the same
   proposition.
3. **Joint necessity**: neither evidence alone supports the original gold conclusion.
4. **Latent conclusion**: `latent_C` is absent from all visible turns and the query.
5. **Person specificity**: a generic person should not receive the same answer.
6. **Natural query**: the query is a plausible later user request, without session,
   evidence, or benchmark references.
7. **Decidable gold**: the answer contract specifies one calibrated decision and required
   elements.
8. **Low surface leakage**: query wording must not rehearse the target evidence or latent
   conclusion.

The required counterfactual table is:

| Visible condition | Original `C_user` supported? |
|---|---|
| Query only / prior | No |
| `ev_A` only | No |
| `ev_B` only | No |
| FULL: `ev_A + ev_B`, same target user | Yes |

If either single-evidence row supports the original answer, the item is not associative
under this standard.

## 5. Evidence Annotation Contract

For every evidence item, store:

```json
{
  "evidence_id": "ev_A",
  "session_id": 5,
  "owner": "u_017",
  "atomic_fact": "The user gets headaches after pre-6am calls.",
  "typed_relation_role": "physical_constraint",
  "necessary_for": "latent_C"
}
```

`owner` must be explicit. The model does not see hidden annotations; annotators and the
judge do.

## 6. Evaluation Arms

### FULL

Both `ev_A` and `ev_B` belong to the target user. The expected mode is `infer_C`.

### A-only / B-only

Remove exactly one target evidence while preserving timeline coherence. The expected mode
is `withhold_C`.

### No-target

Remove both target evidence sessions. The solver-visible input must contain only:

```json
{
  "context": [...],
  "query": "..."
}
```

It must not contain item IDs, arm names, filenames, hidden annotations, gold, required
elements, source labels, or target metadata.

The arm must pass:

```text
exact-leak audit
synonym/summary audit
human visible-field audit
```

### Link-broken

`link_broken` tests co-activation, not source identity. Both evidence memories still
belong to the target user, but the relation that made their joint inference valid is
replaced by a matched, natural dialogue such that `latent_C` is no longer supported.

The replacement must preserve as much as practical:

```text
speaker structure
turn count
time position
style
length
query
target-user ownership
```

It must change the relation-specific connector, not merely add strange wording.

### Source-swap

`source_swap` tests person-indexed memory. The semantic content of one evidence is
preserved but naturally attributed to a named other person.

Example:

```text
FULL:
The user says they do their clearest work after midnight.

SOURCE-SWAP:
The user says, “My friend Alex told me they do their clearest work after midnight.”
```

The expected mode is `source_withhold`: the model must not use Alex's pattern as the
target user's pattern.

`source_swap` is not a replacement for `link_broken`; report both when both claims are
made.

### Distractor

Add a query-relevant, semantically tempting but evidentially irrelevant memory. It must
not add either required fact or independently support the gold.

### Absence

Ship a naturally coherent context where a necessary evidence is unavailable. Expected
mode is `abstain` or a calibrated request for clarification. If the retained evidence
alone supports the original decision, the absence arm is invalid.

### Add-evidence

Restore the missing necessary evidence to an absence item. The expected behavior must
flip from withholding to inferencing the original `C_user`.

## 7. Solver Visibility Boundary

The solver receives only:

```json
{
  "context": [
    {
      "session_id": 1,
      "timestamp": "...",
      "dialogue": [{"role": "user", "content": "..." }]
    }
  ],
  "query": "..."
}
```

The solver must never receive:

```text
gold_answer
required_elements
annotation
evidence_id
owner
arm
item_id
data filename
latent_C
association_type
evolving_state
source contract
```

The solver prompt must state that it may combine evidence only when it belongs to the
same target person. It must not infer user traits from another person's experiences.

## 8. Ground Truth and Judge Contract

The judge sees the solver answer plus hidden:

```text
gold_answer
required_elements
expected_mode
evidence_contract
source identity contract
```

The judge returns:

```json
{
  "conclusion_correct": true,
  "recommendation_correct": true,
  "required_elements": [
    {"hit": true, "evidence_grounded": true, "support": "..."}
  ],
  "evidence_usage": {
    "ev_A_used": true,
    "ev_B_used": true,
    "h_k": 2,
    "source_misattribution": false
  },
  "abstention": {
    "abstains": false,
    "asserts_absent_pattern": false
  },
  "condition_correct": true,
  "failure_tags": [],
  "reason": "..."
}
```

Evidence is credited only when the answer explicitly quotes or unambiguously paraphrases
the evidence's distinctive fact. Generic traits do not count.

## 9. Metrics

### Required-Element Accuracy

```text
REA_item = AND(required_element.hit)
REA_arm = mean(REA_item)
```

### Joint Evidence Recall

```text
JER_item = 1[ev_A_used AND ev_B_used]
```

Report `h_0`, `h_1`, and `h_2` distributions.

### Memory Necessity

```text
Delta_mem = REA_full - REA_no_target
```

### Associative-Link Necessity

```text
Delta_assoc = REA_full - REA_link_broken
```

Interpret `Delta_assoc` only after the link-broken intervention passes E1.

### Source Integrity

Report source-swap errors separately:

```text
source_misattribution_rate
source_withhold_accuracy
```

Do not call source-swap performance `Delta_assoc`.

### Controls

Report:

```text
DIR / FoolRate
AbC
add-evidence flip rate
```

## 10. Human Gates

### E1: Pre-run Intervention Audit

Before model calls, reviewers inspect FULL, no-target, link-broken, source-swap,
distractor, and absence.

E1 confirms:

```text
FULL dual necessity
no target leakage
natural link replacement
natural source attribution
distractor irrelevance
absence withholding validity
```

### E2: Post-run Judgment Audit

After model calls, reviewers inspect:

```text
all source-swap and link-broken outputs
all no-target REA=1 outputs
all invalid/error attempts
random FULL outputs
```

E2 checks REA, JER, source attribution, abstention, and judge agreement.

## 11. Run Governance

Every run must have:

```text
item_manifest.json
profile hash
data-file hashes
prompt contract version
solver configuration hash
validator configuration hash
attempt ledger
duplicate audit
usage records
E1 and E2 review files
```

Only `status=scored` records count as completed. Errors remain retryable. Aggregation must
refuse duplicate scored attempts until a documented resolution exists.

## 12. Release Criteria

An item may enter a full run only when:

```text
E1 passes
solver input boundary passes
source and link controls are natural
no-target leakage audit passes
judge schema is valid
metric contract is frozen
```

An experiment may support an associative-personal-memory claim only when clean paired
results show:

```text
REA_full > REA_no_target
REA_full > REA_link_broken
source-swap does not permit user-specific inference
distractors do not systematically flip correct answers
absence produces calibrated withholding
```

These results support a behavioral construct claim in this benchmark. They do not prove a
biological memory mechanism or universal real-world agent memory.

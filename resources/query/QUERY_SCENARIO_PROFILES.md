# Query Scenario Profiles — addendum to QUERY_STANDARD.md

> Principle: the CORE standard (Answer Table §0, red-lines §2, scorecard §5) is
> **scenario-invariant** — do NOT fork it. Keeping the test identical across domains is
> what makes cross-scenario results comparable (a construct-validity requirement).
> What varies per scenario is the **query profile**: which types dominate, the natural
> query surface, the distractor flavor, source salience, and gold form.

## Per-scenario query profiles

| Scenario | Dominant type(s) | Natural query surface | Plausible-answer trap flavor | Source salience | Gold form | Absence (T5) weight |
|---|---|---|---|---|---|---|
| **Work / learning** | T1 (C2 capacity/skill), T4 (C3 method transfer) | "Should I take on / commit to X?" · "How should I approach [new task]?" | career-advice trap ("great growth opp — say yes") | medium (manager/colleague) | do/don't · method | medium |
| **Hobby / leisure** | T2 (C3 preference), T4 (C3 transfer) | "Which of these should I pick?" · "What should I try?" | surface taste-match (likes cooking → cooking class) | medium (friend rec) | selection (MCQ natural) | low |
| **Health / wellness** | T1 (C2 condition→restriction), **T5 absence**, **update (V4)** | "Should I take / do X?" (risk decisions) | generic health advice / social pressure ("everyone does it") | **HIGH** (doctor vs friend vs self) | do/don't · **abstain-heavy** | **HIGH** (over-answering is dangerous) |
| **Social / relationships** | **T6 source**, T3/T1 (C1 recurring interpersonal pattern) | "Should I say yes to X's ask?" · "Was this my idea or theirs?" | **source-confusion** (a friend's want read as yours) | **MAXIMAL** (home domain of source memory) | decision hinging on **who** | medium |
| **Finance / planning** | T3 (C1 pattern→outcome), T1 (C2 budget/commitment) | "Should I commit to this spend/subscription?" · "What happens if I do Y now?" | anchoring / finance tip ("on sale, worth it") | medium (advisor/friend) | decision · prediction | medium |

## Scenario-aware type mix (tune the 50-query blueprint allocation)
Keep the global type set (T1–T6); shift emphasis by scenario so each domain tests what it
naturally stresses:
- **Health** → over-weight **T5 absence** + **update** (safety: a model must abstain / suppress a superseded restriction).
- **Social** → over-weight **T6 source** (attribution is the failure mode here).
- **Finance** → over-weight **T3 prediction** (recurring-pattern → outcome).
- **Hobby** → over-weight **T2/T4 MCQ** (preference/transfer — MCQ enforces necessity best).
- **Work** → over-weight **T1/T4** (constraint decisions + method transfer).

## What stays identical (do not scenario-tune)
- The 4-row Associative Answer Table (§0) — every query, every scenario.
- Red-lines Q1–Q6, the scorecard, the per-query ablation variants.
- The requirement that each query ships its own **oracle-verified gold** (see below).

## Ground-truth rule (reinforced)
Every query MUST ship: `gold` + `required_elements` + the **Answer-Table result** proving
only "both evidences" yields gold. The gold is not just authored — it is **oracle-verified**:
`P_oracle` (query + the two evidences) must reproduce the gold. A gold that the oracle
solver cannot reproduce from the evidence is wrong evidence or wrong gold → fix before ship.

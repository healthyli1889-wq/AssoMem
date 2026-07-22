# Work S1 — Gate 0 construct freeze

**Review unit:** `work_s1_relational_v1`  
**Status:** `awaiting_human_gate_0`  
**Scope:** construct only. This is not an authored candidate, solver payload, gold
record, or execution request.

## What S1 is intended to test

S1 is a behavioral test of **person-bound relational inference under a partial
staffing cue**. It does not measure biological co-activation, and it does not treat
two reasons to reject a job as associative memory.

The proposed latent relation is:

```text
stable late cognitive-activation / recovery pattern
    + early, live priority-integration impairment
    -> phase-misalignment risk for a fixed daily dawn collaboration schedule
```

The inference is deliberately narrow. It concerns a *fixed, daily, early
synchronous reasoning demand*; it must not become “the user cannot work mornings”
or “the user must decline any role with an early meeting.”

## Proposed episode roles (skeleton only)

No dialogue wording is frozen at Gate 0. Later authoring must supply dated,
same-user episodes with context, goal/prediction, action, outcome, and affect.

### A — cognitive activation and recovery

At a separate date, the user handles a technically nested task after midnight.
They report that this period is when they can keep multiple dependencies active,
and they use a later recovery period rather than an early start the next day.

A establishes a stable activation/recovery signature. It does **not** establish
that an early meeting causes meaningful impairment.

### B — early live-prioritization impairment

At another date, an abrupt pre-6am live prioritization call produces a specific,
transient failure in ordering or integrating issues; later in the day the user can
complete low-complexity work. B must not say that the problem is caused by working
late, that the user is a night owl, or that a dawn schedule is unsuitable.

B establishes a functionally relevant early-call episode. It does **not** establish
that the episode is a stable phase-misalignment pattern rather than a temporary or
environmental problem.

### R — the relational connector

The solver-visible details must make the following relation recoverable:

```text
An early synchronous demand lands before this user's stable activation/recovery
cycle, and the affected operation is live priority integration rather than all
morning work.
```

Reviewer metadata must identify one indispensable visible span from A and one from
B. It may describe R, but cannot be the only source of R.

### C — calibrated personalized inference

For a role whose standard collaboration window starts at 06:15 every workday, a
fixed daily dawn live-prioritization requirement is **likely a poor default fit**.
The response should clarify whether the time is fixed, whether work can be shifted,
and whether a monitored accommodation or trial is available. It must not prescribe
automatic rejection.

### Q — natural retrieval cue

> The platform pod’s standard collaboration window begins at 06:15 local time.
> What should we clarify before deciding whether this is a sustainable fit?

Q names the new staffing situation, but not midnight work, headache, phase
misalignment, or the recommended answer.

## Four core arms

| Arm | Visible evidence | Expected response mode | Diagnostic claim |
|---|---|---|---|
| `full` | A + B, same user | Calibrated C; use one detail from each episode and state R | A+B relation supports C |
| `a_only` | A; B unavailable | Withhold C; ask about actual early-call tolerance/impairment | A alone is insufficient |
| `b_only` | B; A unavailable | Withhold C; ask about sleep timing and recurrence | B alone is insufficient |
| `link_broken` | A + matched B′, same user | Withhold original C; discuss only the changed local factor if relevant | relation R, not topic/format, is necessary |

`no_target` is intentionally outside this minimal four-arm test. It is useful later
for broad memory-dependence checks, but cannot establish whether A, B, or R was
necessary.

## Link-broken design constraint

B′ preserves all of these:

- same user, date position, session count, dialogue roles, approximate length;
- an early call, a headache-like transient impairment, and live task context;
- the user's ability to work later;
- no source/ownership change and no topic switch.

Only the causal connector changes: B′ supplies an environmental explanation that is
absent in comparable early calls elsewhere (for example, a specific display/lighting
condition). With A unchanged, the record no longer supports a stable
phase-misalignment explanation or the original schedule-fit C.

## Gate 0 rejection criteria

Reject the construct if any applies:

1. A or B alone reliably licenses C.
2. The answer can be produced from generic “night owl” or “early calls are bad”
   prior knowledge without retrieving both episodes.
3. Q restates the answer structure or names the hidden relation.
4. B′ changes source, topic, context length, or formatting rather than R.
5. C is an absolute prohibition instead of a qualified schedule-fit inference.
6. The design is described as direct evidence of hippocampal or biological
   co-activation.

## Required approval before authoring

Reviewers must complete `review/gate_0.csv`. Every row requires `human_pass=pass`,
a named reviewer, and an evidence-based note. A rejected or incomplete row blocks
all authored S1 data.

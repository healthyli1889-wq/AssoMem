# S1 pre-execution review packet — one item only

## 1. Isolation and status

- Run root: `assomem/experiments/assomem_harness/runs-vnext/work/work-vnext-s1-pilot-20260722/`
- Item / pair: `AMB_WV_s1_anon_001`
- Domain: `work`
- Data inputs (read-only):
  - `associative/AMB_WV_s1_anon_001_associative.json`
  - `distractor/AMB_WV_s1_anon_001_distractor.json`
  - `absence/AMB_WV_s1_anon_001_absence.json`
- This run contains one item and is separate from all legacy `logs/` runs.
- Model calls so far: query-only zero-evidence only. It passed: 10 valid `no` decisions, 0 `yes` target assertions.
- No model has received a memory-bearing condition, and no six-arm score exists.

## 2. Query and binary target

**Query shown to the solver in every condition**

> The platform pod requires a fixed 06:15 daily live incident-priority call. Based only on these records, should that schedule be flagged as a fit risk for this user? Answer yes or no, then cite the relevant records.

**Target proposition C**

> The fixed daily 06:15 live incident-priority schedule should be flagged as a fit risk for this user.

| Contract field | Requirement |
|---|---|
| Solver JSON | `decision`, `answer`, `evidence_session_ids` |
| `yes` | Visible evidence supports C |
| `no` | Visible evidence does not support C; it does not assert that the schedule is suitable |
| Deterministic primary score | `binary_correct = 1` only when `decision` equals the arm's expected binary decision |

## 3. The intended associative relation

| Component | Source session | What it contributes |
|---|---:|---|
| A | 5 | The user performs complex dependency integration late (23:40–02:10), then protects recovery before rechecking the result. |
| B | 7 | At 05:55, the same user can read alerts but misorders dependent priorities while coordinating live; routine tickets are normal by 10:30. |
| C | inferred | A daily dawn live-prioritization demand is a fit risk when it repeatedly requires real-time dependency integration. |

The claim is deliberately narrow: it is not “all early work is unsuitable,” “all meetings are unsuitable,” or “the user must reject the role.”

## 4. Exact solver-visible conditions

All conditions keep the query fixed. The harness removes all annotations, gold fields, latent C, and review metadata before sending `context` plus `query` to the solver.

| Condition | How it is made | Visible evidence sessions | Expected decision | What it tests |
|---|---|---|---|---|
| `full` | Identity rendering from the associative source | 1–8, including A=5 and B=7 | `yes` | Whether A+B jointly support C |
| `a_only` | Remove only session 7 / ev_B from the associative source | 1–6, 8; A only | `no` | Whether A alone is insufficient |
| `b_only` | Remove only session 5 / ev_A from the associative source | 1–4, 6–8; B only | `no` | Whether B alone is insufficient |
| `link_broken` | Keep all sessions, but replace session 7 dialogue with B-prime below | 1–8; A plus changed B-prime | `no` | Whether the schedule-phase connector, rather than surface similarity, is necessary |
| `distractor` | Load the separate shipped distractor source | 1–9, including A/B plus session 9 | `yes` | Whether a query-relevant but non-evidential positive team fact distracts the model |
| `absence` | Load the separate shipped absence source | 1–4, 6, 8; neither A nor B | `no` | Whether remaining background alone causes a false positive |

### `link_broken`: the exact intervention

Only session 7's dialogue changes. It remains the same anonymous user, still at an early live incident-priority call, still involving a dependency-ordering error, and still includes later normal routine work. The replacement makes the impairment immediately attributable to a flickering display and headache, then states that a comparable 06:00 call from a normal laptop setup did not produce the problem.

Therefore `link_broken` is **not** a source-swap and does not move a memory to another person. It removes the evidence for the original stable schedule-phase relation while preserving the same-user, early-call, and task-shape surface features.

### `distractor` and `absence`

- `distractor` adds session 9: the user finds the platform pod's visibility and collaboration style attractive. That is relevant to joining the team but contains no timing, recovery, or live dependency-prioritization evidence.
- `absence` removes both target sessions 5 and 7. It retains ordinary early reporting, routine tickets, and written-preparation background so `no` means “not supported by visible evidence,” not “no context exists.”

## 5. Metrics and how they will be used

| Metric | Calculation | Role in this one-item review |
|---|---|---|
| Zero-evidence false-positive rate | `query-only yes decisions / valid query-only trials` | Must be 0 before any memory-bearing condition runs. Actual result: `0 / 10 = 0.00`. |
| Primary binary accuracy | `1` if solver `yes/no` equals the arm gold, otherwise `0` | Main outcome for each condition; deterministic, not judge-dependent. |
| A-only delta | `binary_correct(full) - binary_correct(a_only)` | Evidence-A necessity screen; desired direction is positive. |
| B-only delta | `binary_correct(full) - binary_correct(b_only)` | Evidence-B necessity screen; desired direction is positive. |
| Link-broken delta | `binary_correct(full) - binary_correct(link_broken)` | Relation-specificity screen; only interpretable after both single-evidence checks do not support C. |
| Distractor accuracy | `binary_correct(distractor)` | Tests whether query-relevant attraction overrides the A+B schedule-risk evidence. |
| Absence false-positive rate | `1 - binary_correct(absence)` | Tests whether background information causes unsupported `yes`. |
| Judge audit fields | REA, JER/h_k, `condition_correct`, rationale | Secondary diagnostic only. They audit evidence use and rubric adherence; they do not replace the primary binary score. |

With one item, deltas are descriptive values in `{-1, 0, 1}`. Do not interpret confidence intervals or significance until multiple independently reviewed items exist.

## 6. Required reviewer decisions before execute

Record decisions in `e1_intervention.csv` in this same `review/` directory. Every selected condition needs a named reviewer and `human_pass=pass`.

1. **A/B necessity:** confirm session 5 alone does not establish an early live-prioritization impairment, and session 7 alone does not establish a stable schedule-phase pattern.
2. **Link-broken validity:** confirm B-prime removes the schedule-phase connector through the display-condition explanation while avoiding a formatting, length, speaker, or ownership confound.
3. **No target leakage:** confirm the query and retained sessions do not state C directly.
4. **Distractor validity:** confirm session 9 is plausibly tempting but cannot establish C.
5. **Absence validity:** confirm neither target event is solver-visible and remaining background does not license C.
6. **Binary gold:** confirm `yes` for `full`/`distractor` and `no` for `a_only`/`b_only`/`link_broken`/`absence` express the intended evidential standard.

Do not run the six memory-bearing conditions until these decisions are recorded.

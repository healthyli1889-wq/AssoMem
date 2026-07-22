# Work vNext human-control policy

This file is the normative process policy for Work vNext. It controls the
automation boundary; `SPEC.md` defines the construct, and each candidate's
`review/gate_N.csv` records the actual human decision.

## Default: first exemplar is entirely human-gated

No model may author, evaluate, render, execute, freeze, release, or batch-generate
the first eligible Work vNext item until the preceding human gate is explicitly
passed. “Pass” means every required row in the gate CSV has `human_pass=pass`, a
named reviewer, and an evidence-based note. Empty, omitted, or aggregate-only
decisions are failures.

| Node | Human decision required before the next action | Decision file |
|---|---|---|
| 0: construct freeze | construct, arm semantics, query taxonomy, rubric | `staging/work-vnext/v1/<scenario>/review/gate_0.csv` |
| 1: authoring | A, B, bridge, C, Q, arm-specific gold | `artifacts/<id>/review/gate_1.csv` |
| 2: independent audit | every score, cited span, disagreement | `artifacts/<id>/review/gate_2.csv` |
| 3: rendered arms | solver-visible FULL/A-only/B-only/link-broken; source-swap only if in scope | `artifacts/<id>/review/gate_3.csv` |
| 4: behavioral proof | every solver answer, judge verdict, false positives | `artifacts/<id>/review/gate_4.csv` |
| 5: exemplar freeze | provenance hashes, signed package, learning record | `artifacts/<id>/review/gate_5.csv` |

## What “learned enough” means

The first exemplar does not authorize automation merely by passing. Before any
subsequent item can use automation, reviewers must create and sign:

```text
staging/work-vnext/v1/automation_authorization.json
```

It must record:

1. the frozen exemplar ID and version;
2. concrete failure modes observed and the correction made;
3. which operation may become automated (authoring, deterministic rendering, or
   evaluator pre-screening); all other operations remain human-gated;
4. a fixed sampling plan for human double-review across query types and polarity;
5. an expiry condition: any new failure mode, prompt/schema/model change, or
   false-positive control result revokes the authorization.

Until that signed record exists, **batch generation is disabled** and every
candidate repeats Gates 0–5. Even after authorization, publication and behavioral
proof always retain human review.

## Enforcement

- The pipeline refuses evaluator execution without Gates 0 and 1.
- The behavioral proof refuses to run without Gates 0–3.
- Release validation requires Gates 0–5, a passing independent audit, and a clean
  behavioral proof.
- A candidate authored before Gate 0 is illustrative only and may not be released.
- Gate 0 is scenario-level and must exist before a candidate ID exists; later
  candidate provenance must cite the approved scenario-level Gate 0 review.

# Strict match eval: RHELM vs MyPCBench

Rubric: 10 criteria × 0–5 = **/50** (same as DynamicMem). Construct = Associative Personal Memory + DATA_STANDARD controls.

## Scores

| Dataset | Overall | % | Core AssoMem (crit 2–5 /20) |
|---|---:|---:|---:|
| **microsoft/RHELM** | **33/50** | **66%** | **10/20 (50%)** |
| **ljang0/MyPCBench-tasks** | **22/50** | **44%** | **9/20 (45%)** |
| DynamicMem (prior) | 24/50 | 48% | ~11/20 |

## Strict verdict

Neither is drop-in AssoMem. **RHELM is clearly better** for your topic: memory-QA modality, evolving personas, temporal + hallucination/misleading controls, adaptable conversation/QA schema. **MyPCBench** is a personal multi-app CUA environment (N=1 persona); strong for agent action / cross-app records, weak as associative-memory construct test.

## Criterion table (RHELM / MyPC)

1. Complete evolving profile — **4 / 3**
2. Evidence not explicitly stated — **3 / 3**
3. Cue ≠ target (V1) — **3 / 2**
4. Typed relational link — **2 / 2**
5. Novel latent C (A3) — **2 / 2**
6. Temporal (A4) — **4 / 2**
7. Distractor (V2) — **3 / 3**
8. Absence (V4/A5) — **4 / 2**
9. AssoMem schema readiness — **4 / 1**
10. Scale (users×items) — **4 / 2**

## What fails A3 on both (strict)

- RHELM multi-hop mostly recovers **stated** facts via intermediates; Misleading applies known constraints — not co-activate A∧B → unstated C.
- MyPCBench `pattern_inference` (11/184) is statistical habit (“usual tip”); `cross_source_reconciliation` is affordability/contradiction — not typed cross-domain latent blend.

## If adapting one

**RHELM first.** Keep temporal / hallucination / misleading strata; rewrite a multi-hop subset into A3 with typed `associative_links` + V1/V2 gates; map conversations→`context`, evidence refs→`annotation`.

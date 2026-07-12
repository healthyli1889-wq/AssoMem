# AssoMemBench Pilot Data Autoresearch

Autonomous loop for generating **construct-validation** pilot items (not coverage).
Target: ~30 handmade golden samples. Do not expand to 50+.

## What we are testing

Associative Personal Memory: upon a retrieval cue that is **lexically/semantically
dissimilar** to a target memory, co-activate that target through a **typed**
relational link (temporal / causal / analogical), and apply it to produce a
conclusion that was **never explicitly stated**.

Load-bearing terms:
1. **co-activation** — Hebbian / spreading activation
2. **typed link** — causes / constrains / co_occurs / analogous (not vague "related")
3. **not explicitly stated** — latent conclusion C is absent from dialogue

## Pilot matrix (this run)

Domains (2):
- `work/learning` → domain_tags from {work/career, learning/education}
- `hobby/habit` → domain_tags from {hobbies/leisure} (+ habit-adjacent health/household ok as secondary)

Per domain × 15 = **30 items**:

| Arm | N | association_type | Validity focus |
|---|---|---|---|
| associative | 5 | A3 (majority) or A2 | V1 discriminant: flat lexical/TF-IDF must miss evidence |
| distractor | 5 | A3 + distractor_ids | V2 interference: distractor_sim ≥ evidence_sim |
| absence | 5 | A5_absence_control | V4 inhibitory: gold = abstain / insufficient |

Map legacy C1/C2 → A2/A3. Never invent a sixth taxonomy.

## Hard schema rules (DATA_STANDARD v1)

1. `context[].dialogue` may contain ONLY `role` + `content` (+ session `timestamp`).
   All `evidence_id` / `atomic_fact` / `role_setup` / `why_distractor` live in top-level `annotation`.
2. `query_source: "final_turn"` ⇒ `query` === last user turn `content` exactly.
3. `context_length_tokens` computed by tiktoken, never hand-typed.
4. `status: "rendered"` only when dialogue is fully written and tokens recomputed.
5. No `control_flags`. Encode controls via `distractor_ids` + `validity_metrics` + A5 type.
6. `evolving_state` never appears in agent-visible context.
7. Every free-text `gold_answer` has non-empty `required_elements`.
8. `counterfactual_variants` are materializable objects with `variant_id`.

## Loop (NEVER STOP until 30 pass or human interrupts)

1. Generate / edit one item under `items/`.
2. Run `python validity_gate.py --item <path>`.
3. If FAIL → fix and re-run (do not keep broken items).
4. Log keep/discard to `results.tsv`.
5. Advance only when gate PASS.
6. After all 30: run `python validity_gate.py --all` and write `SUMMARY.md`.

## Keep criterion

PASS all applicable gates:
- schema / annotation separation
- query == final user turn
- required_elements non-empty
- latent conclusion not stated in any dialogue turn
- V1: lexical Jaccard(query, evidence) ≤ 0.08 AND TF-IDF cosine ≤ 0.22 AND flat top3 miss
- V2 (distractor arm only): max distractor cosine ≥ evidence cosine
- V4 (absence arm only): no target evidence in context; gold abstains

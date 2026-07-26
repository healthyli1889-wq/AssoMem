# Work-vnext staging (cleaned 2026-07-24)

All rejected and superseded batches (v1 pilot, v2 clone batch, templated S11-S20 v3, their manifests/matrices/audits) have been deleted. What remains is only the current, valid pipeline state.

## Contents

| Path | What it is | Status |
|---|---|---|
| `candidates-s1-s5-review/` | S1-S5 batch: 50 hand-authored sub-scenarios x 3 source conditions = 150 JSON files, plus a README with the full sub-scenario map | awaiting human approval |
| `candidates-s6-s10-review/` | S6-S10 batch: 50 new hand-authored sub-scenarios x 3 source conditions = 150 JSON files, plus a README with the full sub-scenario map | awaiting human approval |
| `harness-root-s1-s10/` | Read-only merged copy of both batches (300 files) used as `ASSOMEM_DATA_ROOT` for assomem_harness runs; rebuild with `cp candidates-s{1-s5,6-s10}-review/<arm>/*.json harness-root-s1-s10/<arm>/` after any regeneration | derived, never edit by hand |
| `generate_s1_s5_review_batch.py` | Reproducible S1-S5 generator; all 50 sub-scenario specs embedded | current |
| `generate_s6_s10_review_batch.py` | Reproducible S6-S10 generator; reuses the S1-S5 machinery, adds a cross-batch uniqueness audit | current |
| `review/A_S11_U01_HUMAN_REVIEW_PACKET.md` | The approved exemplar packet that defines the format (evidence layers, arm logic, controls) | approved reference |
| `review/s1_s5_generation_audit.json` | Per-item deterministic scores for the S1-S5 files (all >= 95) | current |
| `review/s6_s10_generation_audit.json` | Per-item deterministic scores for the S6-S10 files (all >= 95) | current |
| `SCENARIOS_S1_S20.md` | Scenario family definitions S1-S20 | reference |
| `SCENARIO_CARDS_S11_S20.md` | Draft scenario cards for the future S11-S20 redesign | on hold until S1-S10 is approved |

## Gates passed by both batches

- Deterministic score >= 95 on all 300 items.
- Per-batch audit: A/B/query uniqueness across all 50 units; query-type quota 8/8/8/8/9/9; polarity quota accept 15 / reject 20 / conditional 10 / non_decision 5.
- Cross-batch audit: zero shared dialogue lines in key sessions and zero shared timestamps between the two batches.
- `schema.py` validation on all 300 files; `render_arms` succeeds for all 100 associative items.

## Next steps

1. Human review of both batch READMEs (sub-scenario tables) plus spot-reads.
2. On approval of S1-S10: redesign S11-S20 with the same 50-spec hand-written process.

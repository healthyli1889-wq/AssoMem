# AssoMemBench Pilot Batch v1 — SUMMARY

Generated 2026-07-11 via autoresearch-style self-iteration (`program_data.md` → assemble → `validity_gate.py` → rewrite → keep).

## Scale (construct validation, not coverage)

| Domain | Associative | Distractor (V2) | Absence (V4/A5) | Total |
|---|---:|---:|---:|---:|
| work/learning | 5 | 5 | 5 | 15 |
| hobby/habit | 5 | 5 | 5 | 15 |
| **Total** | **10** | **10** | **10** | **30** |

Association types: A3 majority on associative+distractor arms; A2×2 per domain in associative arm; A5×5 per domain for absence.

## What each arm tests

1. **associative** — co-activation via typed links → latent conclusion never stated (V1 discriminant: lexical/TF-IDF miss + flat top3 miss).
2. **distractor** — same associative structure + surface-similar lure with `distractor_cosine ≥ evidence_cosine` (V2 interference).
3. **absence** — query shape preserved, evidence wiped; gold abstains (V4 inhibitory).

## Gate result

**30/30 PASS** (`gates/last_report.json`).

Validity method: stopword Jaccard + local TF-IDF cosine proxy (no external embedder). Stamp fields follow DATA_STANDARD `validity_metrics` shape; `embedder` noted as `tfidf-local-proxy`.

## Format fixes vs AMB_C2_0001 sample

- Annotation separated into top-level `annotation` (no leak into `context`).
- `query_source: final_turn` with query ≡ last user turn.
- Real `context_length_tokens` via tiktoken (short-bucket pilot; not fake 41k).
- No `control_flags`; controls encoded by arm + `distractor_ids` + A5 type.
- C1/C2 mapped to A2/A3; taxonomy is A1–A5 only.
- Counterfactuals are materializable objects with `variant_id`.

## Artifacts

- `items/AMB_*.json` — 30 rendered items
- `items/pilot_batch_v1.jsonl` — combined
- `results.tsv` — keep/discard log (all keep)
- `validity_gate.py` / `assemble.py` / `blueprints_*.py` — reproducible rebuild via `python build_all.py`

## Next (human)

1. IAA accept/reject pass on all 30; ~10–15% double-annotate for κ.
2. Optional: swap TF-IDF proxy for `text-embedding-3-small` in `discriminant_gate.py` before paper numbers.
3. Expand fillers to medium/long token buckets only after construct holds.

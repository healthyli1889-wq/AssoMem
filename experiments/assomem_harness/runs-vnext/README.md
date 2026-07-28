# Published vNext harness runs

These run directories were previously gitignored under `experiments/assomem_harness/runs-vnext/`.
This PR force-publishes completed finance + work evaluation artifacts.

## Work (complete: 240/240 each)

| Run | Path | Checkpoint | Scoring |
|---|---|---|---|
| S1–S10 | `work/work-vnext-s1-s10-expand40-20260726/` | `checkpoint.jsonl` (240) | `out/table_a.md`, `out/table_b.md`, `out/*_scores.csv` |
| S11–S15 | `work/work-vnext-s11-s15-expand40-20260726/` | `checkpoint.jsonl` (240) | same |
| S16–S20 | `work/work-vnext-s16-s20-expand40-20260726/` | `checkpoint.jsonl` (240) | same |

Shared pooled metrics summary: `work/WORK_EXPAND40_METRICS_5.json`

Each work run also includes:
- `review/e1_intervention.csv`, `review/e2_judgment.csv`
- `records/` (per-trial scored JSON)
- `item_manifest.json`, `run_manifest.json`, `PROGRESS.txt`

## Finance (partial: 447 scored / 153 validator_error)

| Run | Path | Notes |
|---|---|---|
| S1–S10 | `finance/finance-vnext-s1-s10-20260727/` | 600 checkpoint lines; 153 HTTP 403 validator failures still need retry |

Includes `checkpoint.jsonl`, `records/`, `review/*.csv`, manifests.

`attempts/` directories are omitted from this PR to reduce size (records/checkpoint are sufficient for scoring).

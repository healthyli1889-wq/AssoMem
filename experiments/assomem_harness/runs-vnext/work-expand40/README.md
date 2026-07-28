# Work vNext expand40 suite (S1–S20)

One package for the three completed work evaluation splits (40 items × 6 arms = 240 trials each).

| Split | Dir | Trials | Status |
|---|---|---|---|
| S1–S10 | `s1-s10/` | 240/240 | scored |
| S11–S15 | `s11-s15/` | 240/240 | scored |
| S16–S20 | `s16-s20/` | 240/240 | scored |

Pooled 5-metric summary: `METRICS_5.json`

## Per-split file set (identical)

Each of `s1-s10/`, `s11-s15/`, `s16-s20/` contains:

- `checkpoint.jsonl` — trial checkpoint log
- `records/` — per-trial scored JSON
- `review/e1_intervention.csv`, `review/e2_judgment.csv`
- `out/` — scoring tables (`table_a.md`, `table_b.md`, `*_scores.csv`, `scores.json`, …)
- `item_manifest.json`, `run_manifest.json`, `PROGRESS.txt`, `results.tsv`
- `by_condition/`, `log/`, `zero_evidence/`

Original run ids:
- `work-vnext-s1-s10-expand40-20260726`
- `work-vnext-s11-s15-expand40-20260726`
- `work-vnext-s16-s20-expand40-20260726`

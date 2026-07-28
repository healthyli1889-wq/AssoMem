# Published vNext harness results

## Work (one suite, 3 splits)

`work-expand40/` — S1–S20 expand40, all scored. See `work-expand40/README.md`.

## Finance

`finance/s1-s10/` — original `finance-vnext-s1-s10-20260727`.

| Artifact | Present |
|---|---|
| `checkpoint.jsonl` | yes (600) |
| `records/` | yes (600; 447 scored / 153 validator_error) |
| `review/*.csv` | yes |
| `out/` | **no** (scoring incomplete until 403 retries finish) |
| manifests / PROGRESS / by_condition / log / zero_evidence | yes |

## Required file set per run folder

```
checkpoint.jsonl
records/
review/e1_intervention.csv
review/e2_judgment.csv
out/                    # work complete; finance pending
item_manifest.json
run_manifest.json
PROGRESS.txt
results.tsv
by_condition/
log/
zero_evidence/
```

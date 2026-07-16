# AssoMemBench Pilot — Directory Layout

## Top level

```
assomem_pilot/
├── src/
│   └── data/           # DATA — rendered JSON samples
│       ├── hobby/      # 600 items
│       ├── health/     # 600 items
│       └── work/       # 600 items
├── tools/              # GENERATORS — personas + batch scripts
├── manifests/          # REPORTS — gate summaries, model_inputs jsonl
├── logs/               # RUN LOGS per domain
├── docs/               # DOCS — standards, program notes
├── gates/              # Global gate snapshot (legacy v1)
├── external/           # External reference (not pilot data)
└── rubbish/            # Local archive only (not pushed to GitHub)
```

## Data (`src/data/`)

```
src/data/hobby/hobby_associative_user{1..10}/AMB_HH_u{NN}_associative_S{N}.json
src/data/health/diet_associative_user{1..10}/...
src/data/work/work_associative_user{1..10}/...
```

## Tools (`tools/`)

| Path | Role |
|------|------|
| `tools/shared/gold_lib.py` | Shared v2 builder, gates, scoring |
| `tools/hobby/bin/generate_hobby_habit_gold_batch.py` | Hobby S1–S20 |
| `tools/health/bin/generate_health_diet_gold_batch.py` | Health S1–S20 |
| `tools/work/bin/generate_work_learn_gold_batch.py` | Work S1–S20 |

```bash
python3 tools/hobby/bin/generate_hobby_habit_gold_batch.py --scenarios S1-S20
```

Writes JSON → `src/data/{domain}/`. Reports → `manifests/{domain}/`.

## Manifests & logs

- `manifests/` — `*_gold_*_report.json`, `*_model_inputs.jsonl`
- `logs/` — `generate_log.txt`, `results.tsv` per domain

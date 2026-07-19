# AssoMemBench — Directory Layout

## Top level

```
.
├── src/
│   └── data/                 # gold JSON (arm-first)
│       ├── work/
│       ├── hobby/
│       ├── health/
│       ├── social/
│       └── finance/
├── tools/                    # generators (personas + batch scripts)
├── manifests/                # gate / release reports
├── logs/                     # run logs per domain
├── docs/                     # standards, program notes (related docs go here)
├── judge/
│   └── LLM judge/
│       └── LLM judge prompts/   # drop judge prompts here
├── gates/                    # global gate snapshot (legacy)
└── rubbish/                  # local archive only (not for release)
```

## Data (`src/data/`)

Arm-first: all users for one arm share one folder. User identity stays in the filename.

```
src/data/{work,hobby,health,social,finance}/
  associative/AMB_*_u{NN}_associative_S{N}.json
  distractor/AMB_*_u{NN}_distractor_S{N}.json
  absence/AMB_*_u{NN}_absence_S{N}.json
```

Each domain: 10 users × 20 scenarios × 3 arms = **600** items.

## Tools (`tools/`)

| Path | Role |
|------|------|
| `tools/shared/gold_lib.py` | Shared builder, gates, scoring, `output_path` |
| `tools/{domain}/bin/generate_*_gold_batch.py` | Domain generators |

```bash
python3 tools/finance/bin/generate_finance_gold_batch.py --scenarios S16-S20
```

Writes JSON → `src/data/{domain}/{arm}/`. Reports → `manifests/{domain}/`.

## Judge (`judge/`)

LLM-as-judge assets. Prompts go under `judge/LLM judge/LLM judge prompts/`.

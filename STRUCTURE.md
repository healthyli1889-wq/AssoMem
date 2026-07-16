# AssoMemBench Pilot — Directory Layout

Clean layout after 2026-07-16 reorg. **Data**, **tools**, **manifests**, and **logs** are separated.

## Top level

```
assomem_pilot/
├── hobby/          # DATA — rendered JSON samples (600 items, S1–S20 × 3 arms × 10 users)
├── health/         # DATA — rendered JSON samples (600 items)
├── work/           # DATA — rendered JSON samples (600 items)
├── tools/          # GENERATORS — personas + batch scripts (no JSON samples here)
├── manifests/      # REPORTS — gate summaries, model_inputs jsonl, per-batch reports
├── logs/           # RUN LOGS — generate_log.txt, results.tsv per domain
├── docs/           # DOCS — standards, program notes, archived summaries
├── gates/          # Global gate snapshot (legacy v1: last_report.json)
├── external/       # External reference / eval notes (not pilot data)
└── rubbish/        # Archived duplicates & deprecated trees (safe to delete after review)
```

## Data (`hobby/`, `health/`, `work/`)

Only **deliverable JSON items**. No generators, no gate reports.

```
hobby/
  hobby_associative_user{1..10}/AMB_HH_u{NN}_associative_S{N}.json
  hobby_distractor_user{1..10}/...
  hobby_absence_user{1..10}/...
```

Same pattern for `health/diet_*` and `work/work_*`.

## Tools (`tools/`)

| Path | Role |
|------|------|
| `tools/shared/gold_lib.py` | Shared v2 gold builder, gates, scoring |
| `tools/hobby/bin/generate_hobby_habit_gold_batch.py` | Hobby S1–S20 generator |
| `tools/hobby/personas/personas_hobby_habit.json` | Hobby personas |
| `tools/health/bin/generate_health_diet_gold_batch.py` | Health S1–S20 generator |
| `tools/health/personas/personas_health_diet.json` | Health personas |
| `tools/work/bin/generate_work_learn_gold_batch.py` | Work S1–S20 generator |
| `tools/work/personas/personas_work_learn.json` | Work personas |

```bash
# Regenerate hobby S1–S5 gold
python3 tools/hobby/bin/generate_hobby_habit_gold_batch.py --scenarios S1-S5

# Regenerate all health
python3 tools/health/bin/generate_health_diet_gold_batch.py --scenarios S1-S20
```

Writes JSON → `hobby/` (or `health/`, `work/`).  
Writes reports → `manifests/{domain}/`.

## Manifests (`manifests/`)

**Run artifacts & audit reports** — not sample data.

- `*_gold_*_report.json` — per-batch hard-gate + score distribution
- `*_model_inputs.jsonl` — flattened model eval inputs
- Do **not** put DATA_STANDARD or README here (see `docs/`).

## Logs (`logs/`)

Per-domain run logs copied from old `*/manifests/generate_log.txt` and `results.tsv`.

## Docs (`docs/`)

- `program_data.md` — autoresearch program spec
- `INTRO_AAAI_DRAFT.md` — paper draft
- `archive/SUMMARY_v1_pilot.md` — original 30-item pilot summary

## Rubbish (`rubbish/`)

| Subfolder | Contents |
|-----------|----------|
| `legacy_domain_folders/` | Old `hobby_habit/`, `health_diet/`, `work_learn/` (duplicate of `tools/` + stale manifests) |
| `v1_pipeline/` | `assemble.py`, `blueprints_*.py`, `build_all.py`, `validity_gate.py` |
| `v1_pilot_items/` | Original 30-item `items/` tree + zip |
| `manifests_superseded/` | v1 jsonl, user1-only pilots, old gate_report copies |
| `pycache/` | `__pycache__` dirs |

Review `rubbish/` then delete when satisfied.

## What was wrong before

1. **Duplicate domain roots** — `hobby/` (data) vs `hobby_habit/` (tools) confused delivery vs codegen.
2. **Manifests mixed with standards** — reports, jsonl, logs, and README lived under `*_habit/manifests/`.
3. **v1 + v2 coexisting** — 30-item pilot pipeline at repo root beside 1800-item v2 gold.
4. **`__pycache__` / `.DS_Store`** scattered in tree.

## Current scale (v2 gold)

| Domain | Files | Hard-gate |
|--------|------:|----------:|
| hobby | 600 | 600/600 |
| health | 600 | 600/600 |
| work | 600 | 600/600 |

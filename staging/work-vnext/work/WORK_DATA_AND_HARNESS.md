# Work-vNext Data + Harness Guide

This document inventories the **work-domain vNext** files created for S1–S20,
and explains how to **generate data** and **run the harness** with the same
record format used by the S16–S20 / S11–S15 pilots.

Repo root for these paths is the AssoMem checkout (`assomem/`), not the outer
autoresearch workspace.

---

## 1. Directory map

```text
staging/work-vnext/work/
├── WORK_DATA_AND_HARNESS.md          ← this file
├── SCENARIO_CARDS_S11_S20.md         scenario cards
├── SCENARIOS_S1_S20.md
├── README.md
│
├── # Specs (hand-authored A/B/E1/E2/B′/query/target)
├── s11_s15_specs_s11.py … s15.py
├── s16_s20_specs_s16.py … s20.py
│
├── # Generators → candidates-* JSON batches
├── generate_s1_s5_review_batch.py
├── generate_s6_s10_review_batch.py
├── generate_s11_s15_review_batch.py      # v1 (superseded for pilots)
├── generate_s11_s15_review_batch_v2.py
├── generate_s16_s20_review_batch.py      # construct-valid v2 contract
├── generate_s11_u01_pilot.py             # early single-unit pilot helper
│
├── # Shipped candidate batches (50 pairs × 3 arms = 150 JSON each)
├── candidates-s1-s5-review/
├── candidates-s6-s10-review/
├── candidates-s11-s15-review/            # older S11–S15
├── candidates-s11-s15-review-v2/         # current S11–S15 review set
├── candidates-s16-s20-review/            # older S16–S20 (construct FAIL)
├── candidates-s16-s20-review-v2/         # current S16–S20 (construct rewrite)
│   ├── associative/
│   ├── distractor/
│   ├── absence/
│   └── README.md
│
├── # Harness data roots (copied/patched for ASSOMEM_DATA_ROOT)
├── harness-root-s1-s10/
├── harness-root-s16-s20/                 # old
├── harness-root-s16-s20-v2/              # S16–S20 pilot data root
├── harness-root-s11-s15-v2/              # S11–S15 pilot data root
│                                         # (mode contract patched)
│
└── review/                               # generation + construct audits
    ├── s1_s5_generation_audit.json
    ├── s6_s10_generation_audit.json
    ├── s11_s15_generation_audit.json
    ├── s11_s15_generation_audit_v2.json
    ├── s16_s20_generation_audit.json
    ├── s16_s20_generation_audit_v2.json
    └── s16-s20-v2/                       # arm packets + construct CSV
```

Harness code (evaluation, not gold JSON):

```text
experiments/assomem_harness/
├── run.py, arms.py, protocol.py, workflow.py, zero_evidence.py, …
├── profiles/work-vnext-1.json
├── config.example.sh
├── config.work-vnext*.example.sh         # templates (no secrets)
├── my_config.sh                          # LOCAL ONLY — gitignored
└── runs-vnext/work/                      # LOCAL run artifacts — gitignored
    ├── work-vnext-s16-s20-pilot-v2-20260725/
    └── work-vnext-s11-s15-pilot-v2-20260726/
```

---

## 2. How data is generated

### Contract (work-vnext-2.0)

Each pair ships three source arms: `associative` / `distractor` / `absence`.
Each JSON has 20 dated sessions. Core ablation invariant:

| Visible evidence | Must not yield calibrated C alone |
|---|---|
| A only | ✗ |
| B only | ✗ |
| E1+E2 | ✗ (logistical calibration only) |
| A+E1+E2 | ✗ |
| B+E1+E2 | ✗ |
| A+B′+E1+E2 | ✗ (B′ breaks connector) |
| **A+B+E1+E2** | **→ calibrated C** |

Solver-facing output fields (current harness):

```json
{"mode":"answer"|"withhold","answer":string,"evidence_session_ids":[int]}
```

### Generate a batch

From AssoMem root:

```bash
cd staging/work-vnext/work

# Example: regenerate S16–S20 v2
python3 generate_s16_s20_review_batch.py

# Example: regenerate S11–S15 v2
python3 generate_s11_s15_review_batch_v2.py
```

Generators:

1. Load per-scenario specs (`s16_s20_specs_s16.py`, …).
2. Expand each unit into associative / distractor / absence JSON.
3. Write under `candidates-<batch>/`.
4. Run schema / render / quota / leak audits → `review/*_generation_audit*.json`.

### Build a harness data root

Copy the candidate batch (optionally patch `answer_contract.required_output_fields`
to `["mode","answer","evidence_session_ids"]`):

```bash
SRC=candidates-s16-s20-review-v2
DST=harness-root-s16-s20-v2
rm -rf "$DST" && mkdir -p "$DST"
cp -R "$SRC/associative" "$SRC/distractor" "$SRC/absence" "$DST/"
cp "$SRC/README.md" "$DST/"
```

S11–S15 v2 was copied to `harness-root-s11-s15-v2` and had `required_output_fields`
patched from `decision` → `mode` for harness parity.

---

## 3. How the harness works

Profile: `experiments/assomem_harness/profiles/work-vnext-1.json`.

Evaluation arms materialized from associative gold:

`full`, `a_only`, `b_only`, `link_broken`, `distractor`, `absence`

Pipeline (fixed order):

1. **dry-run** → freeze `item_manifest.json` + empty E1/E2 CSVs  
2. **E1** human intervention CSV (`human_pass=pass`)  
3. **zero-evidence** query-only gate  
4. **execute** → `checkpoint.jsonl`, `records/`, `attempts/`, `log/results.jsonl`  
5. **E2** judgment CSV (`judge_agrees=yes|pass`)  
6. **aggregate** → `out/table_a.md`, `out/table_b.md`, `per_item_scores.csv`

### Run a 10-pair pilot (same format as S16–S20 v2)

```bash
# copy config.example → local my_config.sh (never commit keys)
source experiments/assomem_harness/my_config.sh
export ASSOMEM_DATA_ROOT="$PWD/staging/work-vnext/work/harness-root-s16-s20-v2"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/work-vnext-1.json"
export ASSOMEM_DOMAIN=work
export ASSOMEM_RUN_ID=work-vnext-s16-s20-pilot-v2-20260725
export ASSOMEM_LOG_ROOT="$PWD/experiments/assomem_harness/runs-vnext"

python3 experiments/assomem_harness/run.py --dry-run --max-items 10
# fill review/e1_intervention.csv
python3 experiments/assomem_harness/run.py --zero-evidence --zero-evidence-trials 1 \
  --item-manifest experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/item_manifest.json
python3 experiments/assomem_harness/run.py --execute \
  --arms full,a_only,b_only,link_broken,distractor,absence \
  --item-manifest experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/item_manifest.json \
  --e1-review experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/review/e1_intervention.csv
# fill e2_judgment.csv, then:
python3 experiments/assomem_harness/aggregate.py \
  experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/log/results.jsonl \
  experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/out \
  --e2-review experiments/assomem_harness/runs-vnext/work/$ASSOMEM_RUN_ID/review/e2_judgment.csv
```

Selection method for `--max-items 10`: `pair_id_even_stride` → typically
`Sxx_U01` and `Sxx_U06` across five scenarios (10 pairs × 6 arms = **60 checkpoints**).

### Run record layout (one run directory)

```text
runs-vnext/work/<RUN_ID>/
├── item_manifest.json      frozen pairs + source hashes
├── run_manifest.json
├── PROGRESS.txt            e.g. 60/60
├── checkpoint.jsonl        one scored line per arm trial
├── records/*.json          hashed checkpoint records
├── attempts/*.json         immutable attempt mirrors
├── log/results.jsonl
├── zero_evidence/
├── review/e1_intervention.csv
├── review/e2_judgment.csv
└── out/table_a.md, table_b.md, …
```

---

## 4. Current pilot status (local)

| Run ID | Data root | Checkpoints | Notes |
|---|---|---|---|
| `work-vnext-s16-s20-pilot-v2-20260725` | `harness-root-s16-s20-v2` | **60/60 complete** | Aggregated under `out/` |
| `work-vnext-s11-s15-pilot-v2-20260726` | `harness-root-s11-s15-v2` | in progress / resume | Same format |

Solver / validator are configured only via local env (`my_config.sh`), not in git.

---

## 5. Preferred vs superseded artifacts

| Prefer | Avoid for new pilots |
|---|---|
| `candidates-s16-s20-review-v2` | `candidates-s16-s20-review` |
| `harness-root-s16-s20-v2` | `harness-root-s16-s20` |
| `candidates-s11-s15-review-v2` + `harness-root-s11-s15-v2` | bare `candidates-s11-s15-review` without mode patch |

Older S16–S20 review data failed construct validity (A/B/E1/E2 still licensed C).
V2 specs rewrite E1/E2 to logistical calibration only.

# Running Work vNext

This package is isolated from legacy `src/data/work/` and legacy logs. The current
file is an **illustrative pre-Gate-0 critique target**, not an eligible candidate:

```text
staging/work-vnext/v1/candidates/work-vnext-001.json
```

The human-control policy is [HUMAN_GATES.md](HUMAN_GATES.md). It requires named
review before every node for the first eligible exemplar, and permits later
automation only through a separately signed `automation_authorization.json`.

## Prepare deterministic and human-review artifacts

```bash
python3 experiments/assomem_vnext/pipeline.py prepare \
  staging/work-vnext/v1/candidates/work-vnext-001.json
```

This creates:

```text
staging/work-vnext/v1/artifacts/work-vnext-001/
  deterministic_audit.json
  rendered_arms.json
  review_packet.md
  review/gate_0.csv ... review/gate_4.csv
```

Fill only the appropriate current gate's `human_pass` values with `pass`; each row
also needs a reviewer and notes. The pipeline intentionally refuses to infer a
human approval from an empty file. It also refuses independent evaluation before
the approved scenario-level Gate 0 and candidate Gate 1, and behavioral proof
before Gate 1–3.

## Independent semantic evaluator

Use a third model: it must differ from both `ASSOMEM_SOLVER_MODEL` and
`ASSOMEM_VALIDATOR_MODEL`.

```bash
export ASSOMEM_QUALITY_PROVIDER=openai-chat
export ASSOMEM_QUALITY_MODEL='independent-quality-model'
export ASSOMEM_QUALITY_API_KEY='...'
export ASSOMEM_QUALITY_BASE_URL='.../v1'
export ASSOMEM_QUALITY_TEMPERATURE=0

python3 experiments/assomem_vnext/pipeline.py evaluate \
  staging/work-vnext/v1/candidates/work-vnext-001.json
```

The evaluator must give every core criterion at least 96/100. It does not write a
release decision.

## Behavioral proof

After Gate 3 is explicitly passed, use frozen solver and validator configuration:

```bash
python3 experiments/assomem_vnext/pipeline.py prove \
  staging/work-vnext/v1/candidates/work-vnext-001.json
```

The command produces one immutable attempt and one record for each of `full`,
`a_only`, `b_only`, `link_broken`, and `source_swap`. Any control that asserts the
original C blocks release.

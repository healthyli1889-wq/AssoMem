# Data: the "special map" — why each input, and how they connect

This benchmark **unifies four base datasets** into one clean, vertical dataset for
**associative memory** (inferring *new* user preferences from stored facts, and using
memory to drive *actions*). Each dataset is chosen to cover one capability the others miss.

## Why each dataset (rationale)

| Dataset | What it uniquely contributes | Scenario it feeds | Verified source |
|---|---|---|---|
| **PersonaMem** | Ready-made *inference* items: question types "suggest new ideas / preference-aligned recommendation / generalize to new scenario" are literally "infer a NEW preference", with MC gold + distance-to-evidence difficulty metadata. MIT-licensed. | `associative` | [arXiv 2504.14225](https://arxiv.org/abs/2504.14225) · [GitHub](https://github.com/bowen-upenn/PersonaMem) · [HF](https://huggingface.co/datasets/bowen-upenn/PersonaMem) |
| **LoCoMo** | Timestamped multi-session dialogue with **per-fact evidence IDs** and event graphs → lets us chain cross-session facts into *long-horizon* associative items with traceable ground truth. | `long_horizon` | [arXiv 2402.17753](https://arxiv.org/abs/2402.17753) · [GitHub](https://github.com/snap-research/locomo) |
| **PerLTQA** | The most *structured* base: profile + social relations + dated events + **span-level memory anchors** → clean authored inference items with exact-match grounding. | `associative` | [arXiv 2402.16288](https://arxiv.org/abs/2402.16288) · [GitHub](https://github.com/Elvin-Yiming-Du/PerLTQA) |
| **MemoryArena** | Couples memory to **downstream action quality** across interdependent multi-session subtasks (esp. `group_travel_planner`, preference-constrained) → supplies `action_gold`. | `memory_to_action` | [arXiv 2602.16313](https://arxiv.org/abs/2602.16313) · [HF](https://huggingface.co/datasets/ZexueHe/memoryarena) |

> Methodological blueprint for the action layer: **Memory-R1** ([arXiv 2508.19828](https://arxiv.org/abs/2508.19828)) treats memory operations {ADD, UPDATE, DELETE, NOOP} as learned actions — we reuse this as the framing for action-quality scoring.

## How they connect → one schema (`BenchItem`)

```
PersonaMem ─┐  (infer new preference, MC)            ┌─> scenario="associative"
PerLTQA   ──┤  (infer from profile+events, anchored) ┤
LoCoMo    ──┤  (chain cross-session facts)           ┼─> scenario="long_horizon"
MemoryArena ┘  (preference → action)                 └─> scenario="memory_to_action"

           ALL ─> BenchItem{ stored_context, query, gold, options?,
                             evidence_ids, constraints, action_gold?,
                             question_type, is_answerable }
```

Every record, regardless of source, becomes a `BenchItem` (see `src/assomem/schema.py`).
The transform lives in `build_dataset.py`; the extraction fields per dataset are documented
there and in `docs/METHOD.*`.

## Reproduce

```bash
python data/download.py --all            # pulls the 4 real datasets into data/raw/
python data/build_dataset.py             # -> data/build/items.jsonl  (unified)
```

If you have no network / API access, a **synthetic sample** that mimics the unified schema
(all three scenarios + an abstention control) ships at `data/sample/sample_items.jsonl`
(regenerate with `python scripts/make_sample.py`).

## Licensing note
PersonaMem = MIT (clean). LoCoMo = custom research `LICENSE.txt` (verify before redistribution;
images not included). PerLTQA and MemoryArena: confirm the repo/HF license before
redistribution. We redistribute **no** raw data — only loaders + transforms.

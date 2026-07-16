# DynamicMem × AssoMem match eval

Sources: [HF dataset](https://huggingface.co/datasets/xiewenya/dynamicmem), [project page](https://wenyaxie023.github.io/DynamicMem/), [arXiv:2606.22877](https://arxiv.org/abs/2606.22877), inspected `user_001` `task_packs.json` + `app_log_large.json` (viewer-truncated).

## Verdict

| Lens | Match |
|---|---|
| Overall construct match | **~48%** |
| As complete-profile substrate | **~70%** |
| As drop-in AssoMem test | **~30%** |

DynamicMem is a strong long-horizon **user-profile** benchmark (attributes / habits / preferences, typed updates, multi-app logs). It is only a **partial** match to Associative Personal Memory (co-activation + typed link + novel latent conclusion). Best use: mine profiles and event chains, then **inject** A3/A2 probes and V2/V4 controls — do not treat State Completion as your construct.

## What it contains

- 10 synthetic users × 15 months × ~2.2M tokens/user × 16 apps
- Profile = attributes + habits + preferences over 6 life domains
- Typed deltas (Add/Modify/Acquire/Shift…) driven by seasons/life events
- Evidence = API app logs (Fitbit, Chase, Gmail…), not chat dumps of the profile
- Tasks: **State Completion** (fill schema) + **Personalized Service** (act on withheld state)

## vs your three load-bearing terms

| Term | DynamicMem |
|---|---|
| co-activation under dissimilar cue | PS scenarios are low-leakage (good). SC **names** the state key (fails your V1 discriminant). |
| typed link | Typed **state deltas** + intent chains exist; no gold associative **path** between memories. |
| not-explicitly-stated novel C | Preferences are implicit (good). Tasks recover/apply a stored profile field — not bridge A+B → novel C (your A3). |

## Taxonomy map

- **A4 temporal** — strong, first-class
- **A2 cue→one fact** — medium via Personalized Service
- **A3 cross-domain latent** — weak in tasks (seeds exist in synthesis)
- **A5 / V2 distractor** — largely missing

## Recommended next step

Adapter: `app_log_large` → AssoMem `context`; inject A3 queries needing ≥2 cross-domain evidence logs; keep DynamicMem snapshot gold in `annotation` only.

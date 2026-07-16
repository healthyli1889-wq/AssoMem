# Pilot data

Rendered AssoMemBench v2 gold JSON samples.

| Folder | Items | ID pattern |
|--------|------:|------------|
| `hobby/` | 600 | `AMB_HH_u{NN}_{arm}_S{N}.json` |
| `health/` | 600 | `AMB_HD_u{NN}_{arm}_S{N}.json` |
| `work/` | 600 | `AMB_WL_u{NN}_{arm}_S{N}.json` |

Each domain: 10 users × 20 scenarios × 3 arms (associative / distractor / absence).

Generators live in [`../../tools/`](../../tools/). Reports in [`../../manifests/`](../../manifests/).

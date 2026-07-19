# Pilot data

Rendered AssoMemBench gold JSON samples (arm-first layout).

| Folder | Items | Layout |
|--------|------:|--------|
| `work/` | 600 | `{associative,distractor,absence}/AMB_WL_…` |
| `hobby/` | 600 | `{associative,distractor,absence}/AMB_HH_…` |
| `health/` | 600 | `{associative,distractor,absence}/AMB_HD_…` |
| `social/` | 600 | `{associative,distractor,absence}/AMB_SC_…` |
| `finance/` | 600 | `{associative,distractor,absence}/AMB_FN_…` |

Each domain: 10 users × 20 scenarios × 3 arms. User id is in the filename (`u{NN}`), not the folder.

Generators: [`../../tools/`](../../tools/). Reports: [`../../manifests/`](../../manifests/).

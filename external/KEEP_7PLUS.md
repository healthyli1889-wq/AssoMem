# KEEP ≥7/10 — retained match cells only

Threshold: **score ≥ 7 / 10** on the unified AssoMem rubric (`scores_10pt.json`).  
Everything below 7 is **dropped** from the keep-set (still visible in the full matrix, not actionable for adaptation).

---

## 0. What survives

| Dataset | # cells ≥7 | Keep? | Role if kept |
|---|---:|---|---|
| **DynamicMem** | 4 | Yes (partial) | Profile + A4 substrate |
| **RHELM** | 5 | Yes (partial) | Schema-ready memory corpus + A4/A5 strata |
| **MyPCBench** | **0** | **No** | Discard as primary source under this threshold |
| **Native AMB pilot** | 7 | Reference gold | Construct-true baseline (not an external corpus) |

---

## 1. Retained cells (only)

### DynamicMem — keep these capabilities
| ID | Criterion | Score | What to reuse |
|---|---|---:|---|
| C01 | Complete evolving user profile | 10 | attr / habit / pref snapshots across 6 domains |
| C02 | Evidence not explicitly stated | 8 | app-log behavioral traces (not profile dumps) |
| C06 | Temporal consistency (A4) | 10 | quarterly checkpoints + typed state deltas |
| C10 | Scale | 10 | 10 users × ~15 months × ~2.2M tok |

**Dropped from DynamicMem:** V1 cue-dissimilarity, typed *memory-path* links, A3 latent C, V2 distractor, A5 absence, AssoMem schema readiness.

### RHELM — keep these capabilities
| ID | Criterion | Score | What to reuse |
|---|---|---:|---|
| C01 | Complete evolving user profile | 8 | 10 LOOP personas, year-long coherent trajectories |
| C06 | Temporal consistency (A4) | 8 | `temporal` QA stratum (~185) |
| C08 | Absence / abstention (A5/V4) | 8 | `hallucination` + fabrication + absence detection (~197) |
| C09 | AssoMem schema readiness | 8 | `conversations/*.json` + QA `supporting_evidence` |
| C10 | Scale | 8 | 1,305 QA · sessions/emails/attachments |

**Dropped from RHELM:** full claim of C02/C03 (only 6), typed path (4), A3 latent C (4), V2 distractor as gated (6).

### MyPCBench — keep nothing at ≥7
All 10 criteria ≤6. Optional *non-keep* notes only (do not count as retained):
- cross-app seeded records / planted contradictions = useful *ideas*, not retained match cells.

### Native AMB pilot — reference keep (≥7 construct cells)
| ID | Criterion | Score |
|---|---|---:|
| C02 | Evidence not explicitly stated | 9 |
| C03 | Cue ≠ target (V1) | 9 |
| C04 | Typed relational link | 9 |
| C05 | Novel latent C (A3) | 9 |
| C07 | Distractor interference (V2) | 9 |
| C08 | Absence (A5) | 9 |
| C09 | Schema readiness | 10 |

**Native weak (<7):** C01 profile depth (5), C06 temporal (4), C10 scale (3).

---

## 2. Actionable keep-set (adaptation policy)

```
KEEP_SOURCE = DynamicMem[C01,C02,C06,C10] ∪ RHELM[C01,C06,C08,C09,C10]
DROP_SOURCE = MyPCBench (entire) + all cells <7
NATIVE_GOLD = AMB pilot construct arms (associative / distractor / absence)
```

Do **not** import external items as finished AssoMem samples unless they also satisfy native C03–C05 after rewrite (those are <7 on externals).

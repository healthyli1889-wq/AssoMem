# AssoMemBench — hobby/habit batch (v1)

**150 items · 10 personas · 15 each (5 associative / 5 distractor / 5 absence) · validity gate 150/150 PASS**

**Priority domain:** most mundane everyday leisure/habit tradeoffs — the slice most likely to be downloaded and stress-tested. Same `DATA_STANDARD v1` format as [`../health/`](../health/) and [`../work/`](../work/).

## Folder map

```
assomem_pilot/src/data/hobby/           # DATA — items only
  hobby_associative_user{1..10}/
  hobby_distractor_user{1..10}/
  hobby_absence_user{1..10}/

assomem_pilot/tools/hobby/              # GENERATOR (reports → manifests/hobby/)
  personas/personas_hobby_habit.json
  bin/generate_hobby_habit_gold_batch.py
```

IDs: `AMB_HH_uXX_{arm}_S{1..5}.json`.

## Personas (consistent across domains)

| user | Source | Notes |
|------|--------|--------|
| user1–4 | DynamicMem ×4 | newly generated |
| user5–9 | RHELM ×5 | newly generated |
| **user10** | **Desktop Healthy Li** | **migrated from pilot HH** |

## Scenario cores (user1–9) — mundane A3

| ID | Bridge (latent facts) | Cue (FOMO / signup) |
|----|------------------------|---------------------|
| S1 | flat-path knee OK × clinic gentle-elevation | mountain race team signup |
| S2 | spend freeze until April × weekend-only outdoor light | Wednesday coastal borrowed-body outing |
| S3 | weekly meal-prep load-bearing × family travel afternoons | standing Sunday building dinner host |
| S4 | late wheel nights past 11 × pre-dawn loaf shifts | extra late studio class before bakery mornings |
| S5 | small home tabletop habit × roommate quiet evenings | loud party-game night at the apartment |

**Construct:** dissimilar cue → co-activate ≥2 habit facts → unstated C (usually decline / relocate / protect the habit). Distractors are **near-miss mundane decisions** (flat 5K, gift-shop camera, restaurant seat, weekend workshop, cafe ticket) that share “amazing / worth it / signup” language but are not the capacity evidence.

**user10 note:** migrated pilot keeps original surfaces; associative S4–S5 are pilot A2 items (climbing max-hang; bedtime e-ink). Arms still 5/5/5.

## Arms & gates (identical across health / work / hobby)

| Arm | Type | Gold |
|-----|------|------|
| associative | `A3_cross_domain` | associative recommendation |
| distractor | `A3_cross_domain` + labeled distractor | same C; ignore FOMO lure |
| absence | `A5_absence_control` | abstain / insufficient evidence |

- **V1:** Jaccard≤0.08 · TF-IDF cosine≤0.22 · `flat_rag_hit_top3=false`
- **V2 (distractor):** distractor cosine ≥ evidence cosine
- **Schema:** context turns = `{role, content}` only; `query` ≡ final user turn

## Reproduce

```bash
cd assomem_pilot/hobby_habit
python3 bin/generate_hobby_habit_batch.py
# regenerates user1–9; re-validates user10; expects 150/150 PASS
```

**Loader (do not leak labels):** serialize `context[].dialogue` with only `role`+`content`; strip `annotation`, `evolving_state`, `associative_links`, `validity_metrics` from model-visible input; score vs `gold_answer` + `required_elements` per arm.

## Why this domain is a hard AssoMem test

Surface FOMO (“amazing”, “worth it”, “signup”) is lexically close to the cue, while the real constraints live in quiet habit talk (knees, meal-prep, roommate noise). Flat RAG should retrieve the lure sessions; associative architectures must co-activate the two habit facts and state C without inventing them under absence.

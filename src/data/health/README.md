# AssoMemBench — health/diet batch (v1)

**150 items · 10 personas · 15 each (5 associative / 5 distractor / 5 absence) · validity gate 150/150 PASS**

Sibling of [`../work/`](../work/) (work/learning) and [`../hobby/`](../hobby/) (hobby/habit). Gold standard: `DATA_STANDARD v1` (AssoMemBench). Construct: dissimilar cue → typed co-activation of ≥2 latent facts → **novel unstated conclusion C**.

## Folder map

```
assomem_pilot/src/data/health/         # DATA — items only
  diet_associative_user{1..10}/
  diet_distractor_user{1..10}/
  diet_absence_user{1..10}/

assomem_pilot/tools/health/              # GENERATOR (reports → manifests/health/)
  personas/personas_health_diet.json
  bin/generate_health_diet_gold_batch.py
```

Each folder has 5 JSON files: `AMB_HD_uXX_{arm}_S{1..5}.json`.

## Personas (user1–user10)

| user | Source |
|------|--------|
| user1–4 | DynamicMem `001_user_001` … `004_user_004` |
| user5–9 | RHELM: Elena_Morales, Jonas_Richter, David_Reyes, Dr._Elena_Markovic, Martin_Keller |
| user10 | Desktop Healthy Li (UMich exchange / KCL Psychology) |

Locked in `health_diet/personas/personas_health_diet.json`.

## Scenario cores (S1–S5)

Shared A3 logic; surface text is paraphrased so **query ≉ evidence** (V1):

| ID | Bridge | Cue decision |
|----|--------|----------------|
| S1 | morning milk-fat GI cost × late social appetite | 8am cheese/cream tasting |
| S2 | post-afternoon stimulant → fragmented sleep × morning focus collapse | late energy drink before 8am |
| S3 | high-sodium → headache × half-day focus loss | midnight ramen crawl |
| S4 | skip first meal crash × bakery-only insufficiency | pastry-only workshop |
| S5 | late chili → reflux/sleep × early voice fragility | late spicy tasting before 7:30am call |

## Arms

| Arm | `association_type` | Evidence | Gold |
|-----|--------------------|----------|------|
| `associative` | `A3_cross_domain` | ev_A + ev_B | associative recommendation |
| `distractor` | `A3_cross_domain` | ev_A + ev_B + labeled distractor | same C; must ignore lure |
| `absence` | `A5_absence_control` | none | abstain / insufficient evidence |

## Validity gates (measurable)

Stamped in each item’s `validity_metrics` (local TF-IDF proxy; same thresholds as `assomem_pilot/validity_gate.py`):

- **V1** (associative & distractor): Jaccard(query, evidence) ≤ 0.08 · TF-IDF cosine ≤ 0.22 · `flat_rag_hit_top3 == false`
- **V2** (distractor only): `distractor_cosine_query ≥ evidence_cosine_query`
- **Schema**: context turns = `{role, content}` only; `query` ≡ final user turn; no `evolving_state` / forbidden phrases in dialogue

Surface-lure **fillers** (annotation `surface_lure=true`) share query decision vocabulary so flat retrieval tops cue+lures, not evidence — same pattern as the WL/HH pilot.

## Reproduce

```bash
cd assomem_pilot/health_diet
python3 bin/generate_health_diet_batch.py
# → writes ../health/diet_*_user*/ + manifests/; expects SUMMARY 150/150 PASS
```

Loader for model eval (do **not** leak annotation into the prompt):

1. Serialize `context[].dialogue` with only `role` + `content`
2. Strip `annotation`, `persona.evolving_state`, `latent_forbidden_phrases`, `associative_links`, `validity_metrics` from the model-visible input
3. Present `query` as the last user turn (already identical when `query_source=final_turn`)
4. Score answer vs `gold_answer` + `required_elements`
5. Report arm-wise: associative accuracy, distractor resistance, absence abstention rate

## Scoring intent (what a valid AssoMem score means)

- **Associative high**: model co-activates both evidence facts and states the unstated C (not mere keyword RAG).
- **Distractor high**: same C despite a higher surface-similarity lure toward “say yes”.
- **Absence high**: abstains when evidence is missing (no hallucinated bodily pattern).

A model that only does flat lexical retrieval should fail V1-discriminating items; architectures claiming associative memory should lift associative (+ distractor) without collapsing absence.

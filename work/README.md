# AssoMemBench — work/learning batch (v1)

**150 items · 10 personas · 15 each (5 associative / 5 distractor / 5 absence) · validity gate 150/150 PASS**

Sibling to [`../health/`](../health/) and [`../hobby/`](../hobby/). Gold standard: `DATA_STANDARD v1`.

## Folder map

```
assomem_pilot/work/                      # DATA — items only
  work_associative_user{1..10}/
  work_distractor_user{1..10}/
  work_absence_user{1..10}/

assomem_pilot/tools/work/                # GENERATOR (reports → manifests/work/)
  personas/personas_work_learn.json
  bin/generate_work_learn_gold_batch.py
```

IDs: `AMB_WL_uXX_{arm}_S{1..5}.json`.

## Personas

| user | Source | Notes |
|------|--------|--------|
| user1–4 | DynamicMem ×4 | newly generated |
| user5–9 | RHELM ×5 | newly generated |
| **user10** | **Desktop Healthy Li** | **migrated from pilot `items/pilot data_S1 work:learn + S2 hobby/` (WL only; HH left in pilot)** |

## Scenario cores (user1–9, aligned)

| ID | Bridge | Cue decision |
|----|--------|----------------|
| S1 | early-rising headache × late deep-work peak | mandatory 7am standup / platform pod |
| S2 | build-to-learn × lecture-video dropout | stipend Track Alpha vs Beta |
| S3 | post-2pm crash × prior late review fail | late client workshop 3:30–5:30 |
| S4 | handwriting retention × digital-slate fail | tablet-only bootcamp |
| S5 | night-alert sleep debt × unbroken-sleep need | SRE rotation |

**user10 note:** migrated pilot keeps original surface text. Associative S4–S5 are the pilot A2 items (async remote; stakeholder walkthroughs); distractor/absence S3–S5 follow the table above. Arms still each have 5/5/5.

## Arms & gates

Same as health/diet: A3 associative · A3+V2 distractor · A5 absence; V1 Jaccard≤0.08 / cosine≤0.22 / `flat_rag_hit_top3=false`; V2 distractor≥evidence.

## Reproduce

```bash
cd assomem_pilot/work_learn
python3 bin/generate_work_learn_batch.py
# regenerates user1–9; re-validates (does not invent) user10; expects 150/150 PASS
```

Loader: serialize `context[].dialogue` with only `role`+`content`; strip annotation / evolving_state / links from model-visible input; score vs `gold_answer` + `required_elements` per arm.

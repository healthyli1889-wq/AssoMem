# WORKABILITY — making the dataset runnable for future models & ablations

> Governing principle: **every element a future experiment might remove must be (1) named,
> (2) independently removable by a stable ID, and (3) paired with a declared expected
> outcome.** Satisfy this and both "run a new model" and "ablate an element and still get
> interpretable signal" are true.

---

## 1. The runnable contract (so ANY architecture can run the sample)

- **Frozen I/O.** Model input = `context` serialized to `role+content` only. Everything
  else (`annotation`, `evidence_id`, `role_setup`, `evolving_state`,
  `latent_forbidden_phrases`, `associative_links`) is stripped. Output = answer text (or
  MCQ choice) + optional `used_session_ids`.
- **Three ingestion modes, one sample.** Sessions are timestamped and separable, so the
  same sample serves: long-context (concatenate all), RAG (chunk + retrieve), and memory-
  agent (ingest session-by-session, let it consolidate). Never encode the task in a way
  that assumes only one mode.
- **Deterministic scoring.** `answer_vs_gold` + `required_elements` hit-rate + fixed judge.
  Frozen, versioned (`standard`), temp 0.

## 2. The interpretability contract (so a score decomposes)
Ship, per sample, the hidden graph + tags: `target_evidence_ids`, `associative_links`
(typed), `association_type`/`control_arm`, `domain_tags`, hop count. Report per-stage:
**evidence-retrieval recall · path correctness · answer accuracy** — so when a consumer
ablates their retriever, retrieval-recall moves and explains the answer drop.

## 3. The ablation contract — the 5-row pairing table (CORE)

Every sample ships these concrete variants, each with a **declared expected outcome**. A
data ablation is "workable" only because the expected direction is pre-declared; otherwise
the resulting number is uninterpretable.

| # | Variant id suffix | What is removed / changed | Declared expected outcome | Proves |
|---|---|---|---|---|
| 1 | `_cf_drop_evA` | delete the ev_A session(s) | gold **flips / abstains** | ev_A necessary (multi-hop) |
| 2 | `_cf_drop_evB` | delete the ev_B session(s) | gold **flips / abstains** | ev_B necessary (multi-hop) |
| 3 | `_cf_no_distractor` | delete the distractor session(s) | **same gold, higher solver accuracy** | distractor does work |
| 4 | `_cf_temporal_shuffle` | randomize session order | **C1/temporal accuracy drops; C2/C3 stable** | temporal construct is real |
| 5 | `_cf_add_evidence` (absence only) | insert the real evidence sessions | **abstain → answerable** (gold provided) | the absence control has a live twin |

Notes:
- Variants 1–2 are **required for every positive sample**; 5 is **required for every absence
  sample**; 3 required whenever a distractor exists; 4 required for C1/temporal items.
- Each variant is a **concrete, runnable object** (its removed_session_ids + its own
  `expected_gold`), not a prose promise. (The old samples failed here — vague single variant.)

## 4. The two ablation planes (keep distinct)
- **System ablation** — the consumer removes a component of THEIR model (e.g. turns off
  spreading activation). Data is unchanged; our **per-stage metrics** attribute the drop.
- **Data ablation** — remove an element of the sample (table above). Our **paired variants +
  declared outcomes** define the expected result.

## 5. The headline experiment (what a consumer runs on us)
```
For each (profile, query) over the frozen test set:
  run solver under arms: FULL · DROP-evA · DROP-evB · NO-DISTRACTOR · ORACLE · SOURCE-SWAP
  associative_lift = Acc(FULL) − Acc(DROP-ev*)          # the number that matters
Validity of the benchmark itself:
  require  Acc(DROP-ev*) ≈ chance   AND   Acc(NO-DISTRACTOR) > Acc(FULL)
  any item violating this is auto-retired.
Splits: split by PROFILE (no profile leaks across train/dev/test); ablation is within-item on test.
```

## 6. Source-memory probe (orthogonal to ablation — do not skip)
Beyond ablation, ship a **source arm**: re-attribute an evidence fact to someone else
(friend/assistant) and re-ask. A model with source memory changes its answer; one without
treats others' words as the user's. Failure here is invisible to the ablation arms, so it
is a separate required probe.

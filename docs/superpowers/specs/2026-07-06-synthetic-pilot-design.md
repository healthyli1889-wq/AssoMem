# Synthetic Associative-Memory Pilot (25 items) — Design

## Purpose

`known_bugs.md` / project memory notes that LoCoMo's cross-session ("strong F9")
evidence is only 32 items — too small an N to carry the paper's core claim that the
ASSOCIATE step beats a retrieval-only baseline on multi-hop inference. This pilot
validates a synthetic-generation pipeline that can later be scaled to ~1000
conversations with controlled 2-hop associative structure, before spending API
budget on real LLM generation.

This is a **structure pilot**, not a text-quality pilot: it validates that the
data flow (persona → causal graph → sessions → haystack → QA → `BenchItem`)
produces well-formed, verifiable items. Prose is templated, not natural language.

## Scope

- 25 synthetic `BenchItem`s, `source="synthetic"`.
- One `association_type`: `A2_cue_chain` (2-hop bridge: question mentions A and K,
  answer requires B, which is never mentioned in the question).
- One counterfactual probe: `remove_bridge`.
- Deterministic (fixed `random.seed`), offline, no LLM API calls.
- Explicitly out of scope: natural-language dialogue generation, A3/A4/A5 types,
  running `eval/judge.py` against these items, merging into `data/build/items.jsonl`.

## Data flow

1. **Persona** — sample name + 3-4 traits/interests from a small fixed vocabulary.
2. **Causal event graph** — 6-8 events per persona, `{id, event, date, caused_by}`,
   guaranteed to contain at least one 2-hop chain `E_A -> E_B -> E_K`
   (`caused_by` edges), mirroring `data/raw/locomo/prompt_examples/causal_event_kg_example_1.json`.
3. **Render to sessions** — one templated sentence per event
   ("{name} mentioned that {event} on {date}."), each event becomes one session.
4. **QA construction** — pick the 2-hop chain; question references A and K only;
   gold answer requires B. Reject chains where B shares surface tokens with the
   question (must not be findable by literal keyword/embedding overlap).
5. **Haystack insertion** — insert the three answer sessions (A, B, K) among the
   persona's other (unrelated) event sessions at controlled depth (e.g. positions
   ~3, ~12, ~20 of a ~25-session haystack), mirroring
   `data/raw/longmemeval/data/custom_history/sample_haystack_and_timestamp.py`.
6. **Counterfactual probe** — `remove_bridge`: a second `stored_context` variant
   with the session containing B removed.
7. **BenchItem mapping** — `source="synthetic"`, `scenario="long_horizon"`,
   `association_type="A2_cue_chain"`, `counterfactual_probes=["remove_bridge"]`,
   `evidence_ids` = session ids for A and K, `meta.causal_graph` = full graph (for
   human audit of the 25 items).

## Output

- `data/synthetic/build_pilot.py` — standalone script, does not touch
  `data/build_dataset.py` (currently mid-flight with uncommitted changes).
- `data/synthetic/pilot_items.jsonl` — 25 items.
- Schema note: restore `synthetic` to the `source` field comment in
  `src/assomem/schema.py` (currently only lists
  personamem/locomo/perltqa/memoryarena/longmemeval).

## Testing

`tests/test_pilot_synthetic.py`:
- every item's evidence sessions (A, K) appear verbatim in `stored_context`.
- the `remove_bridge` probe variant's `stored_context` does not contain the
  B session.
- the bridge event B shares no tokens with the question text (guards against
  accidentally-trivial associative items).
- all 25 items validate against `BenchItem` required fields (no empty
  `stored_context`, non-empty `gold`).

## Follow-up (not in this pilot)

- Human spot-check of the 25 causal graphs/QA pairs for sense (same pattern as
  `annotated_100.csv`).
- Swap templated rendering for a real LLM backend once structure is validated,
  to scale toward ~1000 conversations.
- Extend to A3_cross_domain / A4_temporal_consistency association types.

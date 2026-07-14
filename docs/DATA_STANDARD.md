# AssoMemBench Data Standard v1 (deploy now — confirm by text, don't rewrite)

Locked 2026-07-09. Applies to (a) new partner-generated conversations, (b) LoCoMo/LongMemEval
items being retrofitted with injected associative elements. Every item any teammate produces
from this point on must satisfy this doc or it doesn't go in the pilot set.

Three things this standard exists to guarantee (do not trade these off against each other):
1. **Concept validity** — the item actually requires associative retrieval, not lexical/semantic
   shortcut, not long-context luck.
2. **Everyday-ness + diversity** — items look like real assistant use, spread across domains,
   so later architecture/algorithm studies on this corpus generalize.
3. **One output format** — every teammate's items parse with the same loader, no per-person
   schema drift.

---

## 1. Canonical construct taxonomy — use these five, nothing else

Reuses the repo's existing `association_type` vocabulary (`src/assomem/schema.py`,
`data/dataset_labels.md`). If you generated items using a different local name (e.g. `C1`/`C2`),
map it now, don't invent a sixth system:

| Code | Definition | Grounding | Shuffle-sensitive? |
|---|---|---|---|
| **A1** relational_binding | ≥2 facts co-present in the *same* session must be bound together to answer | Eichenbaum relational memory | No |
| **A2** cue_chain | A cue in the current turn triggers a *single* linked fact from an earlier, separate session | Hebbian spreading activation | Weakly (recency can be a confound — see §4) |
| **A3** cross_domain | ≥2 facts from *different* topic domains (health, work, finance...) must be bridged into a novel inference in a third domain the facts never mention | Schema theory / conceptual blending | No — causal/logical, not order-dependent |
| **A4** temporal_consistency | An earlier stated belief/preference is superseded by a later one; must track *which is current* | Memory updating/consolidation | Yes — this is the one type where shuffle *should* break it |
| **A5** absence_control | No true evidence exists; correct behavior is abstention | Negative/false-positive control | N/A |

**Mapping decision for the C1/C2 sample already drafted:** `C2_causal_constraint` → **A3**
(headache/chronotype example is a flagship A3 case — keep it as the template). `C1_temporal_co_occurrence`
→ **A2** (temporal adjacency that *aids* a single-hop cue chain is a property of A2, not a new type).
Confirm this mapping with whoever drafted `AMB_C2_0001` before they generate more — 5-minute call, not a redesign.

Target mix across the new+modified corpus (this is the "diversity" requirement in §3):
**A1 20% · A2 30% · A3 30% · A4 15% · A5 5%.** A3 gets the largest deliberate share because it's
the construct existing benchmarks (LoCoMo, LongMemEval, PersonaMem) under-cover — it's the paper's
novelty claim, so it needs enough N to report a stratified result on its own.

---

## 2. Output schema — one JSON shape, hard separation of agent-visible vs annotation-only

**The single most important rule, non-negotiable:** the `context` array that gets serialized into
the agent's `stored_context` must contain *only* `role` and `content` (+ optional `timestamp`).
No `evidence_id`, `atomic_fact`, `role_setup`, `distractor_id`, or `why_distractor` field may ever
sit inside a session object that gets rendered into the prompt. Put all of that in the separate
top-level `annotation` block, keyed by `session_id`. (This is the exact bug risk found in the
`AMB_C2_0001` review — annotation labels were co-located with dialogue and would leak into the
model's context if a loader serialized the session object directly.)

```json
{
  "sample_id": "AMB_A3_0001",
  "source": "partner_generated",
  "status": "rendered",
  "association_type": "A3_cross_domain",
  "secondary_association_type": "A2_cue_chain",
  "domain_tags": ["health", "career"],
  "context_length_tokens": 41200,

  "persona": {
    "user_id": "u_017",
    "stable_traits": ["software engineer", "lives alone", "values autonomy"],
    "evolving_state": {"chronotype": "evening"}
  },

  "context": [
    {"session_id": 1, "timestamp": "2026-01-06T21:10:00Z",
     "dialogue": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]},
    {"session_id": 2, "timestamp": "2026-01-13T22:40:00Z",
     "dialogue": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
  ],

  "query": "...",
  "query_source": "final_turn",
  "gold_answer": "...",
  "required_elements": [
    "cites early-rising -> headache fact",
    "cites late-night peak-productivity fact",
    "recommendation is negative or explicitly conditional, not an unconditional yes"
  ],

  "target_evidence_ids": ["ev_A", "ev_B"],
  "associative_cue_id": "cue_1",
  "distractor_ids": ["dist_1"],
  "associative_links": [
    {"source": "ev_A", "source_text": "Early rising (before 6am) causes morning headaches.",
     "relation": "causes", "target": "morning_impairment",
     "target_text": "Working an early-morning shift makes the user impaired/unwell.", "hop": 1},
    {"source": "ev_B", "source_text": "Peak productivity is midnight-3am.",
     "relation": "co_occurs", "target": "evening_chronotype",
     "target_text": "The user's natural rhythm runs late at night.", "hop": 1},
    {"source": ["ev_A", "ev_B"], "relation": "constrains", "target": "night_oriented_pattern", "hop": 2}
  ],

  "annotation": {
    "1": {"role_setup": "filler"},
    "2": {"role_setup": "target_evidence", "evidence_id": "ev_A",
          "atomic_fact": "Early rising (before 6am) causes morning headaches."},
    "6": {"role_setup": "distractor", "distractor_id": "dist_1",
          "why_distractor": "shares 'team'/decision framing with the query; must be MORE surface-similar to the query than ev_A/ev_B (see §4) or it doesn't count as a distractor"},
    "8": {"role_setup": "associative_cue"}
  },

  "counterfactual_variants": [
    {"variant_id": "AMB_A3_0001_cf_no_evidence", "type": "evidence_removed",
     "removed_session_ids": [2, 5], "expected_gold": "insufficient evidence / neutral"},
    {"variant_id": "AMB_A3_0001_cf_stale", "type": "evidence_replaced",
     "replace_session_id": 5, "replacement_dialogue": "...",
     "also_remove_session_ids": [2],
     "expected_gold": "yes, likely thrives"}
  ],

  "validity_metrics": {
    "lexical_jaccard_query_evidence": 0.02,
    "embed_cosine_query_evidence": 0.09,
    "flat_rag_hit_top3": false,
    "distractor_cosine_query": 0.15,
    "evidence_cosine_query": 0.09,
    "validity_method": {"embedder": "text-embedding-3-small", "lexical": "jaccard-stopword-filtered",
                          "computed_by": "data/discriminant_gate.py", "computed_at": "2026-07-09"}
  },

  "provenance": {"generator": "planned+rendered", "generated_by": "<name>"},
  "dataset_meta": {"human_verified_by": [], "iaa_cohort_kappa": null, "iaa_n_overlap": null}
}
```

Fields resolved from the `AMB_C2_0001` draft that were dropped rather than fixed in the first
pass of this doc — putting them back with the rule attached:

- **`persona`** — kept, it's useful for keeping the character consistent across sessions during
  generation. Visibility rule: `stable_traits` may appear in dialogue naturally (the user says
  things a software engineer living alone would say) but `evolving_state` is the ground-truth
  label the item is testing for — it must **never** appear in `context`, in a system prompt built
  from `persona`, or anywhere else agent-visible. If your loader builds a persona-summary system
  prompt from this block, it must strip `evolving_state` the same way `context` strips `annotation`.
- **`context_length_tokens`** — must be the *actual* token count of the serialized `context`
  payload, computed by the build script (e.g. tiktoken), never hand-typed by the generator. Pair
  with **`status`**: `"draft_template"` while filler sessions are still outlines/placeholders,
  `"rendered"` once the full dialogue is written and the token count has been recomputed to match.
  Items don't count toward the 1000–1500 quota or the §3 coverage table until `status: "rendered"`.
  (This directly fixes the `AMB_C2_0001` draft, which declared 41200 tokens against a payload of a
  few hundred — that's fine for a `draft_template`, not fine for something counted as finished data.)
- **`query_source`** — `"final_turn"` (default) means `query` is character-identical to the last
  user turn's `content` in `context` — one register, natural first-person chat, no separate
  analyst-style paraphrase. Only use `"explicit_probe"` if the scenario genuinely needs a
  non-conversational evaluation prompt in addition to the natural last turn, and if you do, say why
  in `annotation` — don't silently carry two differently-worded versions of the question, which is
  what the `AMB_C2_0001` draft did (in-dialogue first-person turn vs. a separately worded top-level
  `query` field).
- **`control_flags`** (e.g. `V1_discriminant`, `V2_interference`, `V4_inhibitory_available`) —
  **dropped, don't add these.** Every concern they gestured at already has a concrete field:
  discriminant validity → `validity_metrics.flat_rag_hit_top3`; interference/inhibition →
  `distractor_ids` + the §4 rule that distractor cosine ≥ evidence cosine. A freeform tag with no
  backing computation is exactly the kind of self-reported claim §4 exists to eliminate. If you
  think you need a control that none of the existing fields capture, that's a real gap — raise it
  as a schema change for the whole team, don't add a private tag to your own items.
- **`associative_links`** (with `hop` counts) — analysis/case-study aid only. `eval/judge.py`
  currently scores the final answer against `gold_answer` + `required_elements`; it does not verify
  the agent's rationale traversed this exact path. Don't over-engineer hop-path realism beyond what
  a human reviewer needs to sanity-check the chain — process-level scoring is out of scope for v1.
  **`relation` must be one of the canonical six** (updated 2026-07-11, replaces the earlier draft's
  ad hoc `"indicates"`/`"co_activate_to"`): `co_occurs | causes | constrains | updates |
  analogous_to | suppresses`. Every `hop: 1` edge (source and target are both concrete evidence
  facts) needs `source_text`/`target_text` so `eval/quality_audit.py` TASK 3 can blind-classify it
  and check agreement with your label. `hop >= 2` edges (target is a latent/inferred node like
  `night_oriented_pattern`, not a stated fact) don't get `source_text`/`target_text` and are
  correctly skipped by TASK 3 — there's no ground truth to blind-classify against for a node that
  was never actually said out loud.

Maps onto the repo's `BenchItem` (`src/assomem/schema.py`) as: `context`→`stored_context` (after
the loader strips to `"role: content"` strings), `query`→`query`, `gold_answer`→`gold`,
`target_evidence_ids`→`evidence_ids`, `association_type` unchanged, **`required_elements`→`constraints`**
(reuse the existing field — it's already exactly "ordered list the answer must satisfy," which is
what `eval/judge.py`'s `constraint_satisfaction` already scores; don't add a parallel field for the
same thing). **New field to add to `BenchItem`:** `distractor_ids: List[str]`. Everything else
(`associative_links`, `annotation`, `counterfactual_variants`, `validity_metrics`, `domain_tags`,
`persona` [with `evolving_state` stripped at build time — see the leakage rule above],
`status`/`context_length_tokens`) goes in the existing `meta: Dict` — don't add more top-level
dataclass fields than that, keep the loader stable.

**Rule for `counterfactual_variants`:** every entry must have its own `variant_id` and be
materializable into a standalone item by a script (not left as prose). If a variant changes one
session, it must explicitly list *every* other session that also needs to change to keep the gold
answer logically consistent (the `evidence_replaced` example above shows the fix for the bug found
in `AMB_C2_0001`, where swapping S5 without also removing S2 left a contradiction).

---

## 3. Diversity / representativeness requirement

**Domain taxonomy — updated 2026-07-11, supersedes the original 10-item list.** Teammate proposal
(grounded in LongBench's subtask categories, reviewed 2026-07-11) is adopted as canonical:

1. `hobby_habit`
2. `work_learning`
3. `health_diet`
4. `travel`
5. `finance`

This collapses the original list's `hobbies/leisure`+`learning/education` → `hobby_habit`/`work_learning`,
and `health/wellness` → `health_diet`. **One gap from the collapse: `relationships/social` and
`household/logistics`/`shopping/purchases` have no home in the 5.** This isn't just a taxonomy
nicety — LoCoMo's entire corpus is friendship/family dialogue, i.e. relationship-context items, and
dropping that as a domain risks losing coverage of exactly the kind of conversation your largest
existing data source already is. Don't block today's `hobby_habit`/`work_learning` batches on this
— but before finance/travel batches go out, decide: (a) fold relationships in as a 6th domain, or
(b) treat it as a cross-cutting `domain_tags` addition alongside one of the 5 (e.g. a work_learning
item can also be tagged `relationships` if a coworker is the associative bridge), not a replacement
top-level domain. Recommend (b) — keeps the clean 5-way split for reporting, doesn't lose coverage.

Every batch should be checkable against this list before it's counted toward the 1000–1500 quota.
No domain >25% of a person's batch (5 domains, so aim close to even rather than the old ≥8-domain
20% rule).

**Hop count:** 1-hop (A1/A2 majority) : 2-hop : 3-hop ≈ 50% : 35% : 15%. Don't let everything be
2-hop just because the template example was — 1-hop items matter as an easier calibration point,
3-hop items are what separates you from LoCoMo/PersonaMem.

**Context length buckets** (mirrors PersonaMem's design, gives you a difficulty axis for the
architecture-optimization studies this dataset is meant to support later): short (~8–15k tokens),
medium (~25–40k), long (~60k+). Don't cluster everything at one length.

---

## 4. Validity & quality gates — an item is not "in" until it passes all of these

1. **`flat_rag_hit_top3 == false`**, computed by `data/discriminant_gate.py` (or its extension for
   this schema) — not self-reported. This is the discriminant-validity gate already built and run
   against the existing corpus (see `results/discriminant_gate_summary.md` for the current
   baseline: LoCoMo 63.2% pass, the 32-item "strong F9" flagship subset only 50% — that subset is
   priority #1 for query-rewrite before anything new gets generated, since it's the paper's
   existing showcase).
2. **Exempt from gate #1: A4 items.** Temporal-consistency queries are supposed to be topically
   close to their evidence (that's the point — the difficulty is in tracking *which* belief is
   current, not in finding the topic). Report A4 separately, never blended into the headline pass rate.
3. **Distractor rule:** `distractor_cosine_query >= evidence_cosine_query` for at least one
   distractor per A3 item. A distractor that is *less* surface-similar to the query than the real
   evidence (as in the `AMB_C2_0001` draft, where distractor jaccard 0.028 ≈ evidence jaccard
   0.022–0.023) doesn't test inhibition of a competing lure — it's just a random irrelevant fact.
4. **Shuffle diagnostic only required for A4** (and reported, not required, for A1–A3 — see the
   taxonomy table's "shuffle-sensitive" column). Don't gate A3 items on shuffle degradation.
5. **`required_elements` rubric present and non-empty** for every free-text `gold_answer`.
6. **IAA, not self-report — two different checks, don't conflate them:**
   - **(a) Difficulty/sanity check** — what's described in the 2026-07-11 team update ("自己核对答案
     看是否和agent的一致，顺便看 distractor 是否有效"): you write/know the gold answer, run it against
     an actual agent, and see if the agent gets it wrong while a human wouldn't. This is exactly the
     original plan's pilot-difficulty step (`validity_metrics.human_easy` from the `AMB_C2_0001`
     draft) — valuable, keep doing it, and it doubles as an informal distractor-effectiveness read.
   - **(b) Inter-annotator agreement** — a *different* question: do two independent people agree
     this item actually requires associative retrieval / is well-constructed. (a) does not substitute
     for (b) — one person deciding "the agent got this wrong so the item is good" says nothing about
     whether a second person would independently label it the same way. Cheapest way to get (b)
     without doubling anyone's workload: pick a ~10–15% random slice (100–150 items per 1000) and have
     a second teammate run *their own* accept/reject + distractor-check pass over that slice (their
     existing per-item review, just pointed at someone else's items instead of only their own).
     Compute Cohen's kappa on that slice with `eval/metrics.py::cohen_kappa` (already implemented).
     Target κ ≥ 0.7 on "does this item require associative retrieval"; κ < 0.6 → stop and simplify
     the construct/query before generating more, don't just discard the disagreeing items and continue.
   - LLM-judge score is a first-pass cheap filter to catch obviously broken items before a human
     ever sees them — treat it as a pre-filter, not evidence of quality (self-preference bias: a
     model tends to rate its own generations well). See §7 for the judge's actual output contract.

---

## 5. Ablation protocol (starts 2026-07-10 evening)

Goal: show existing benchmarks (unmodified LoCoMo etc.) don't sufficiently exercise associative
memory, and that removing your injected elements collapses performance back toward that baseline —
this *is* the novelty claim, so the ablation needs to be run exactly this way, not just "remove
some stuff and see":

- **Ablation A — no injected associative_links:** run on the *original unmodified* LoCoMo/LongMemEval
  items (pre-injection) vs. the same conversations after your team's A3 injection. Delta should be
  large; if it isn't, the injection didn't add what it claims to.
- **Ablation B — no distractor:** same item, distractor session removed. Tests whether the
  distractor was doing real interference work (ties to §4 rule 3).
- **Ablation C — counterfactual variants:** run the materialized `evidence_removed` /
  `evidence_replaced` / `cue_removed` variants (§2) and confirm gold-answer flips as specified.
- **Ablation D — pipeline-level:** reuse the existing `full` / `memory_only` / `no_assoc` /
  `no_reflect` ablations already in the harness (`eval/run_eval_trace.py`) on the new A3-heavy
  subset specifically, not just the whole corpus average — the effect should be *sharper* on A3
  than on the corpus overall, since A3 is exactly the construct `no_assoc` should hurt most.

Report effect sizes (not just significance) given small-N strata; use paired bootstrap or McNemar
since the same items are reused across ablation conditions.

---

## 6. Two judges — don't confuse them

**`eval/judge.py`** grades an **agent's answer during a benchmark run** (was GPT-4o's
pipeline-produced answer correct, feeds the results table). **`eval/quality_audit.py`** audits
**whether a candidate sample is well-constructed**, run once per item during data curation, before
it enters the corpus — this is the Heptabase design (pasted 2026-07-11), reconciled below. Same
underlying `LLM` class, different question, different lifecycle stage. Don't run one where the
other belongs — quality_audit's REJECT/REVISE/PASS decides what goes in `data/build/items.jsonl`
in the first place; judge.py only ever sees items that already made it in.

### 6a. `eval/judge.py` output format (implemented 2026-07-11)

Team ask was: clear return format, with accuracy / is-it-associative / target-evidence as the
three metrics that matter, everything else optional. `eval/judge.py::judge_answer()` now returns
exactly this (backward-compatible with existing keys `score01`/`verdict`/`constraint_satisfaction`
so `eval/run_eval.py` doesn't break):

```json
{
  "score01": 0.8,
  "verdict": "yes",
  "constraint_satisfaction": [1, 1, 0],
  "is_associative": 1,
  "target_evidence_used": {"ev_A": 1, "ev_B": 1},
  "target_evidence_coverage": 1.0,
  "raw_score": 4.0
}
```

- **accuracy** = `score01`/`verdict` (existing, unchanged).
- **is_associative** — 1 only if answering correctly required *combining* ≥2 target evidence ids
  via a non-obvious bridge; 0 if a single fact or generic knowledge would have sufficed. This is
  the field that lets you report "% of correct answers that were actually associative" separately
  from raw accuracy — an agent can get the right answer for the wrong (non-associative) reason.
- **target_evidence_used** — per `evidence_id`, whether the judge believes the reasoning genuinely
  relied on it. Aggregates to `target_evidence_coverage`.

Also fixed while wiring this up: the judge prompt was truncating `stored_context` to the first 40
lines before grading (`eval/judge.py`, pre-2026-07-11). For long LoCoMo conversations (up to 720
lines) with evidence in later sessions, the judge literally couldn't see what it was supposed to
grade — same failure class as the truncation bug already fixed in `build_locomo()`
(`known_bugs.md` Bug 1), just recurring one layer up in the judge instead of the builder. Fixed by
always passing the full target-evidence text separately (guaranteed untruncated) alongside the
(still-truncated, for cost) general context.

### 6b. `eval/quality_audit.py` — the Heptabase design, implemented 2026-07-11

Pasted prompt is the data-curation auditor, correctly scoped as a *separate* tool from 6a — it
answers "is this sample even valid to include," not "did the agent answer it correctly." Reconciled
and implemented as `eval/quality_audit.py`, reusing `data/discriminant_gate.py`'s chunking/matching
so D1 isn't a third reimplementation of the same cosine check:

| Dimension | Source | Notes |
|---|---|---|
| D1_discriminant (20) | reuses `discriminant_gate.py` cosine proxy | static surface-similarity check |
| D2_shortcut (20) | TASK 1, `query_only`/`last_2_sessions` runs | **critical** if either succeeds — a real behavioral shortcut test, stronger than D1 |
| D3_path_necessity (15) | TASK 1 `full_dialogue` run, evidence_recall | needs real `session_id`s to be trustworthy — see convention note below |
| D4_distractor (10) | TASK 1 `full_dialogue`, uses_distractor | NA (not 0) if item has no distractor at all |
| D5_human_answerability (15) | **manual** — pass `human_answer=` | code can't automate this one, matches what your teammate already does by hand |
| D6_leakage (10) | pure code check, no LLM call | scans `stored_context` for the exact annotation-field leakage class found in `AMB_C2_0001`, plus verbatim-gold-in-context |
| D7_typed_link (5) | TASK 3, blind relation classification | only runs on `hop:1` edges with `source_text`/`target_text` — see §2 relation-vocab note |
| D8_temporal | **not implemented**, `status: "NA"` | matches the Heptabase spec's own placeholder — this is the shuffle-diagnostic from §4 rule 4, build it if/when A4 coverage needs it, not blocking now |

`overall_decision` = REJECT if `critical_fail` (D2/D6/no-evidence/no-cue-when-required/unfaithful
rationale), else PASS if `normalized_total >= 0.8` and distractor wasn't defeated, else REVISE —
v1 decision rule, tune the threshold once you've run it against a real batch.

**Session-id convention this depends on:** TASK 1 asks the model to report `used_session_ids` as
integers, which the code then cross-references against which sessions actually hold the target
evidence / distractors. That only works if `stored_context` session headers are real ids, not
positions. **New rule: render session headers as `[session_id: N | ISO-timestamp]`** (the exact
format in the Heptabase SESSIONS spec) so this is unambiguous. Legacy LoCoMo/LongMemEval items
don't have this and fall back to 1-indexed chunk position — treat their D3 scores as lower
confidence, don't block on retrofitting them.

Smoke-tested against 8 real LoCoMo items with `--backend mock` (plumbing only, not real
shortcut/faithfulness signal — that needs `--backend openai`): `python eval/quality_audit.py
--items data/build/items.jsonl --n 20 --backend openai` is the actual next command to run once a
key is available, on the first-20 pilot batch.

---

## 7. What's explicitly out of scope for this v1 (don't block on these)

- Full re-annotation of A1/A2 taxonomy for old LoCoMo items — already done (`dataset_labels.md`).
- Fixing the LongMemEval multi-session placeholder-constraint bug (`build_dataset.py:376-377`) —
  useful but not on the critical path to 7/12; do it during the 7/13–15 evaluation window if time allows.
- MemoryArena discriminant-validity scoring — structurally out of scope for this gate (see
  `results/discriminant_gate_summary.md` §"data pipeline gaps"), don't spend time on it now.

# Method (draft v2 — 2026-07-12)

Reconciles `Method_AssociativeMemory.docx` (original draft) against everything locked this week
(`docs/DATA_STANDARD.md`, `eval/judge.py`, `eval/quality_audit.py`, `data/discriminant_gate.py`).
**Text marked "[REUSE]" is copied near-verbatim from the original docx — it's still correct, just
needs to sit under a different heading now.** Text marked "[NEW]" didn't exist before this week.

One terminology collision to resolve before anyone writes prose: the original docx uses
**"scenario"** for the *data-source task format* (associative / long_horizon / memory_to_action —
this is `BenchItem.scenario` in code). Your outline's "scenarios — 5 sub-tasks" is a different
axis — the **A1–A5 construct taxonomy** (`association_type` in code). Don't call both of them
"scenario" in the paper or reviewers will trip on it. Suggested fix: keep "scenario" for the
3-way task-format split (§Dataset), and call A1–A5 **"association types"** or **"constructs"**
throughout. That's the convention used below.

---

## 1. Scenarios — five association types and rationale [mostly NEW]

We organize the benchmark around five association types, each isolating a distinct mechanism by
which human associative memory connects stored facts to a novel inference. This taxonomy — not
the source dataset — is the primary axis for reporting results, because it is what determines
*whether an item tests associative memory at all* rather than which corpus it happened to come from.

| Type | What it tests | Cognitive grounding |
|---|---|---|
| **A1 Relational Binding** | ≥2 facts co-present in the *same* session must be bound together to answer | Eichenbaum's relational memory theory (Eichenbaum, 2000) — episodic memory as bound item-context representations |
| **A2 Cue-Triggered Chain** | A cue in the current turn triggers a linked fact from an earlier, separate session | Hebbian spreading activation (Hebb, 1949/2005; Collins & Loftus, 1975) — "neurons that fire together wire together," reactivation along associative pathways |
| **A3 Cross-Domain Bridging** | ≥2 facts from *different* topic domains must be bridged into a novel inference in a third domain neither fact mentions | Schema theory / conceptual blending (Bartlett, 1932; Fauconnier & Turner, 2002) — combining independent knowledge structures into an emergent inference |
| **A4 Temporal Consistency** | An earlier stated belief/preference is superseded by a later one; agent must track which is current | Memory updating and interference (McCloskey & Cohen, 1989) |
| **A5 Absence Control** | No true evidence exists; correct behavior is abstention | Negative/false-positive validity control (Guo et al., 2017 calibration framing) |

**Why A3 is the flagship construct.** A1, A2, and A4 are, to varying degrees, already exercised by
LoCoMo's multi-hop/open-ended categories and LongMemEval's multi-session/knowledge-update splits.
A3 is not: reviewing HeLa-Mem (Zhu et al., 2026), MemoryArena (He et al., 2026), and PersonaMem
(Jiang et al., 2025) turned up no existing benchmark item that requires bridging two *independently
introduced, topically unrelated* facts (e.g., a health constraint and a work-habit fact) into a
recommendation in a third domain. This is the gap the injected/retrofitted data closes, and it is
where the paper's ablation (§4) needs to show the sharpest effect.

**Target distribution across the corpus:** A1 20% · A2 30% · A3 30% · A4 15% · A5 5% (matches
`DATA_STANDARD.md` §1 — A3 gets outsized share deliberately, since it needs enough N to report a
stratified result on its own).

---

## 2. Dataset

### 2a. Associative memory mechanism design [REUSE, recontextualized]

We operationalize associative memory as a graph-structured, three-mechanism agent, each mechanism
mapped onto one or more of the five association types above:

- **Graph-structured association** (serves A1, A2) — stored facts are connected into an associative
  graph following A-MEM's agentic note-linking (Xu et al., 2025) and Zep/Graphiti's bi-temporal fact
  edges (Rasmussen et al., 2025). Rationale: association in humans is relational, so memory must be
  a graph, not a list.
- **Spreading activation** (serves A2, A3) — given a query, activation spreads from directly-retrieved
  facts to graph-neighboring facts via personalized PageRank, following HippoRAG's hippocampal-indexing
  model (Gutiérrez et al., 2024). This is the mechanism that should surface a bridging fact in a
  different domain than the query — the substrate A3 tests directly.
- **Reflective consolidation** (serves A4) — the agent periodically reflects over activated memories
  to synthesize higher-level insights, following Generative Agents' reflection loop (Park et al.,
  2023); stale memories decay via an Ebbinghaus curve following MemoryBank (Zhong et al., 2024).
  Rationale: tracking which belief is current requires consolidating and deprioritizing superseded
  detail, not just storing everything.

**Positioning against HeLa-Mem (Zhu et al., 2026):** HeLa-Mem proposes an architecture built on
the same Hebbian/spreading-activation principle and reports gains on LoCoMo's native multi-hop split.
We do not compete with it as an architecture — we treat it as a baseline (§4) and as evidence for
our construct-validity argument: its own ablation shows spreading activation moves LoCoMo multi-hop
F1 by only ~2 points (36.04→33.88), consistent with our finding (§3) that LoCoMo's native multi-hop
split is largely solvable via naive retrieval and therefore does not cleanly isolate the mechanism
either paper cares about.

### 2b. Core elements within the data [NEW]

Every item is a unified record (`BenchItem`, `src/assomem/schema.py`) with a hard separation between
what the evaluated agent is allowed to see and what exists only for scoring/analysis:

- **Agent-visible:** `stored_context` (session dialogue, `role: content` only — no annotation
  labels), `query`.
- **Scoring-only (`meta`):** `target_evidence_ids` (facts required for the answer),
  `associative_cue_id` (the turn that triggers retrieval), `distractor_ids` (injected lures),
  `associative_links` (typed graph edges between evidence nodes, six-way relation vocabulary:
  `co_occurs | causes | constrains | updates | analogous_to | suppresses`), `counterfactual_variants`
  (materialized sibling items for the ablations in §4), `validity_metrics` (discriminant-validity
  scores, computed not asserted — see §3).

Sources: the original four (PersonaMem, LoCoMo, PerLTQA, MemoryArena) plus LongMemEval (oracle
split, added for its explicit knowledge-update category — feeds A4), plus new partner-generated
conversations and LoCoMo items retrofitted with injected A3 bridges where the original discriminant-
validity audit (§3) found the native item solvable via shortcut.

[REUSE the per-source contribution table from the original docx here — PersonaMem/LoCoMo/PerLTQA/
MemoryArena rows are unchanged; add a LongMemEval row: "multi-session + knowledge-update splits,
oracle evidence sessions" → feeds A1/A4.]

---

## 3. Controls [NEW section — didn't exist in v1]

Three controls, applied to every item before it counts as part of the released corpus (full
criteria: `DATA_STANDARD.md` §4):

**Discriminant validity.** An item must not be answerable via surface-level shortcut. We measure
this two ways: (i) a static proxy — lexical Jaccard and embedding cosine between the query and the
target-evidence text (`data/discriminant_gate.py`); (ii) a behavioral test — the same LLM is asked
to answer the item three times at increasing context levels (`query_only`, `last_2_sessions`,
`full_dialogue`); if it succeeds at either of the first two levels without abstaining, the item is
rejected regardless of what the static proxy says (`eval/quality_audit.py`, TASK 1). The behavioral
test is the harder bar and the one we report against baselines. On the audited LoCoMo subset, this
rules out roughly a third of the native multi-hop split — see §4 for how that number motivates the
ablation.

**Leakage prevention.** Because annotation fields (`evidence_id`, `atomic_fact`, `distractor_id`,
`why_distractor`) are structurally separated from `stored_context`, the discriminant-validity audit
also checks the built corpus for the label ever appearing in agent-visible text (`quality_audit.py`
D6). This catches an authoring bug class we found directly: a draft item had `role_setup`/
`atomic_fact` annotation co-located inside the session object that would have been serialized
straight into the agent's prompt.

**Interference validity (distractors).** A distractor session is only counted as a valid lure if
its embedding cosine to the query is *at least as high* as the true evidence's cosine to the query
— otherwise it is not competitive with the correct answer and doesn't test inhibition of a plausible-
but-wrong alternative. We verify this rather than assume it: an early hand-authored item had a
distractor with *lower* surface similarity than the real evidence (0.028 vs. 0.022–0.023 lexical
Jaccard), which would not have functioned as a real lure.

---

## 4. Ablation

**Ablation 1 — associative-link injection (headline ablation).** For each A3 item retrofitted onto
an existing LoCoMo conversation, we run the full agent pipeline on two versions of the same
conversation: (a) the original, unmodified session set, and (b) the session set after injecting the
associative cue, bridge, and distractor described in §2b. *How this works mechanically*: injection
does not add new evidence content to what the conversation already implies — it makes the *query*
require combining two facts that were already present but never jointly queried, and adds a
distractor session that shares surface features with the query but not the correct inference. The
prediction: accuracy and `is_associative` (§5) should be near floor on the original conversation
(no cue exists to trigger the bridge) and should show a large, construct-specific jump on the
injected version — with the jump concentrated on A3 items, not uniform across A1/A2/A4, since the
injection targets exactly the cross-domain bridging mechanism. A jump that is *not* A3-specific
would indicate the injection changed something other than what it claims to (a negative result
worth reporting either way).

**Ablation 2 — distractor removal.** Same item, distractor session deleted. Tests whether the
distractor was doing real interference work (ties to the §3 cosine-parity control) — if removing it
doesn't change agent behavior, the distractor wasn't functioning as a lure regardless of what its
static similarity score said.

**Ablation 3 — counterfactual variants.** Run the materialized `evidence_removed` / `evidence_replaced`
/ `cue_removed` siblings and confirm the gold answer flips as specified. This is the necessity/
sufficiency check: if the answer doesn't flip when the evidence is removed, the item wasn't actually
requiring that evidence.

**Ablation 4 — pipeline components** [REUSE from v1's "Experiment Setup"]: full AM agent vs.
memory-only (retrieval without association or reflection — the conventional RAG baseline), no-
association, no-reflection. Run this specifically on the A3-heavy subset in addition to the
corpus-wide average, since A3 is exactly the construct the association/spreading-activation step
should matter most for — the effect should be sharper there than on the corpus average.

Report effect sizes (not just significance) given small-N strata; paired bootstrap or McNemar,
since the same items recur across ablation conditions.

---

## 5. Judge

### 5a. Human [REUSE + one addition]

A panel of PhD and professional-program students evaluates a stratified subset. For MC items,
raters compare each agent answer to ground truth; for open-ended inferences, raters apply a fixed
rubric (supported, not contradicted, helpful — now formalized per-item as `required_elements`,
mapped onto `BenchItem.constraints`). Inter-rater reliability is reported as Cohen's κ.

**[NEW]** Two distinct human passes, not one: (i) a difficulty/sanity pass — every item gets one
reviewer who independently answers it and checks agreement with the eventual agent output (this is
the workflow already in use for the first-20 pilot batch); (ii) an inter-annotator-agreement pass —
a random 10–15% slice gets a *second* independent reviewer, and κ is computed on that overlap
(`eval/metrics.py::cohen_kappa`). Target κ ≥ 0.7 on "does this item require associative retrieval";
κ < 0.6 on the overlap sample means stop and simplify the construct before generating more, not
discard the disagreeing items and continue.

### 5b. LLM [REUSE core design + NEW output contract; prompts in Appendix]

Reference-guided, chain-of-thought judge following G-Eval (Liu et al., 2023) and the strict-format
protocol of MT-Bench (Zheng et al., 2023). Bias controls, unchanged from v1: non-self judge (different
model family than the agent under test), swap-and-require-agreement for pairwise comparisons,
explicit verbosity guard.

**[NEW]** The judge's output contract now returns the three metrics in §6 directly, not just a
scalar score (`eval/judge.py::judge_answer`, full prompt template in Appendix): `constraint_satisfaction`
(existing), `target_evidence_used` (per-evidence-id boolean — did the rationale genuinely rely on
it), `is_associative` (did the answer require combining ≥2 evidence pieces via a non-obvious bridge,
vs. a single fact or generic knowledge sufficing). We also fixed a truncation bug while extending
this: the judge previously saw only the first 40 lines of `stored_context`, which silently hid the
evidence for long LoCoMo conversations; target-evidence text is now always passed in full regardless
of general-context truncation.

**Note for scoping:** there is a *second* LLM-based tool, the data-quality auditor
(`eval/quality_audit.py`), which runs once per candidate item during corpus construction (not
during agent evaluation) — it's the mechanism behind the discriminant-validity and leakage checks
in §3, not part of the agent-facing judge. Keep these two described separately in the paper; they
answer different questions ("is this item valid to include" vs. "did the agent answer correctly")
and conflating them in the writeup will confuse reviewers the same way it briefly confused the
implementation.

---

## 6. Evaluation Metrics — three core metrics [restructured; RS reused as a component]

**(1) Accuracy.** For atomic items: exact-match / token-F1 / MC-correctness against gold. For
long-horizon, multi-constraint items, accuracy is computed via the **Reasoning Score (RS)** — reused
unchanged from v1:

RS = (1−λ)·Σₖ w̃ₖxₖ + λ·∏ₖxₖ − β·(p̂−g)², with w̃ₖ = γ^(k−1)/Σⱼγ^(j−1), g = ∏ₖxₖ

where xₖ ∈ [0,1] is per-constraint satisfaction, p̂ is the agent's self-reported confidence all
constraints hold, λ blends strict joint-EM (λ=1) against partial credit (λ=0), and the last term
(grounded in ECE/Brier calibration measures — Guo et al., 2017) penalizes confident-but-wrong
answers. [Keep the worked numeric example from v1 — K=4, x=[1,1,0,1], p̂=0.7 → RS=0.225 — it's a
good concrete illustration, no change needed.]

**(2) Associativity Rate.** Fraction of correct answers for which `is_associative = 1` — i.e., the
answer was correct *and* the judge determined it required genuinely combining ≥2 target evidence
pieces, not a single fact or generic-knowledge guess. This is the metric that directly answers the
paper's construct-validity question: an agent can be accurate for the wrong (non-associative)
reason, and this metric is what separates that from genuine associative reasoning — the same design
move as π-Bench's (Zhang et al., 2026) split between task completeness and proactivity, cited as
methodological precedent for reporting two metrics that can diverge rather than collapsing to one.

**(3) Target-Evidence Coverage.** Mean of `target_evidence_used` across an item's `target_evidence_ids`,
aggregated per condition/model. Gives a continuous, per-evidence-piece diagnostic (which specific
facts get missed) rather than the binary associativity rate alone — useful for the failure-mode
case studies in the appendix.

**Replicability.** All three are computed by a single open-sourced entry point
(`eval/judge.py::judge_answer`, invoked via `eval/run_eval.py`), with a fixed system prompt (full
text in Appendix), deterministic JSON parsing with a documented fallback path, and a swappable LLM
backend (`mock` for offline/CI reproduction of the harness logic, `openai`/real models for reported
numbers) — so the exact judge call that produced any reported number can be rerun by a reviewer.

**[REUSE as secondary metric]** Abstention-aware calibration (AURC + ECE on A5 items) — unchanged
from v1, still the right secondary metric for "does the agent know when its memory doesn't support
an answer."

# Method & Experiment Setup — AAAI Draft (2026-07-16)

Paper-ready prose for §3 (Method) and §4 (Experiment Setup), continuing the numbering from
`assomem_pilot/docs/INTRO_AAAI_DRAFT.md` (§1 Introduction, §2 Related Works). Reconciles
`docs/METHOD_v2_draft.md` and `docs/DATA_STANDARD.md` into submission prose and grounds every
factual claim against the current codebase and corpus on disk as of this date — see the
**Grounding notes** at the end for exactly what was checked and what is still open.

---

## 3 Method

### 3.1 Associative Memory Design

§2.2 defines associative success as co-activation of a target memory through a typed relational
link, triggered by a cue that does not restate it. We do not redefine the construct here; this
section states how each item operationalizes it.

**The bridge.** Every associative item is built around $ev_A \times ev_B \rightarrow C$: two
independently introduced experiences, neither individually sufficient to answer the eventual cue,
whose joint interpretation supports a conclusion $C$ that is never stated verbatim anywhere in the
item. Concretely (health domain): $ev_A$ = "cream-heavy dairy before noon causes bloating and
fog within an hour," $ev_B$ = "social energy and appetite peak after 9pm, not in the morning,"
$C$ = an 8am cheese-and-cream tasting is a poor fit — stated nowhere, derivable only from both.
Links carry an explicit hop count: hop-1 connects the cue to $ev_A$ and to $ev_B$ directly — this
is the co-activation step itself; hop-2 connects the co-activated pair to $C$ — the step that is
unobservable from either experience alone and what both judges (§3.3) specifically check for.

**Domain-specific bridge themes.** The kind of constraint a bridge draws on is domain-specific,
and shapes what counts as a plausible distractor (§3.2) as much as what counts as valid evidence:
health items bridge on physiological constraints, work items on cognitive-load and schedule
constraints, hobby items on body/energy rhythm and activity pacing, social items on relationship
energy and social-obligation load, finance items on cash-flow timing and account/debt constraints.
Only health, hobby, and work are populated on disk today; social and finance are target domains,
not yet-built ones (§3.2).

**Relation typing.** §2.2 represents links as temporal, causal, or analogical relations — an
expository three-category grouping over six machine-checkable labels the corpus actually
annotates (`co_occurs`, `causes`, `constrains`, `updates`, `analogous_to`, `suppresses`): `updates`
is temporal; `causes`/`constrains`/`suppresses` are causal; `co_occurs`/`analogous_to` are
analogical. These three categories are not claimed to exhaust human association; per Limitations,
social and spatial relation types are planned extensions, not present in the current corpus.

### 3.2 Data Construction

**Item Schema.** Every item enforces a hard separation between what the evaluated agent may see
and what exists only for scoring — the boundary the controls below depend on, since a control
loses its force the moment a manipulated field could leak into agent-visible text. Agent-visible
fields are limited to a session-structured dialogue history (`role`/`content`, optionally a
timestamp) and a query that is character-identical to the final user turn: the indirect cue
(§1.1–§1.2), not a restatement of $ev_A$/$ev_B$. Scoring-only fields — evidence ids, the
associative cue id, distractor ids, typed links, counterfactual variants, and validity metrics —
sit in a separate annotation block a compliant loader never serializes into the prompt.

**Personas.** Ten user profiles per domain are drawn from three sources rather than authored from
scratch: four adapted from DynamicMem, five from RHELM, and one desktop-collected profile
(internally "Healthy Li"). Everything built on top of these profiles — the sessions, the bridges,
the distractors, the absence variants — is original; the profiles themselves are the one input we
modify rather than invent, so that persona style is not an artifact of a single generation pass.

**Corpus Scale.** Each persona is instantiated under three experimental conditions — associative,
distractor, absence — described in the Quality Gate below. The target release is 3,000 items
across five domains on this design; on disk today this comprises 450 items across the three
populated domains (health/diet, hobby/habit, work/learning) plus a second wave adding 150 further
hobby/habit items under the same personas [PEER REVIEW: 3,000 is the stated target, not yet
verified on disk — see summary].

**Multi-Session Coherence.** Carried over from an earlier construction requirement, not in the
distilled outline this rewrite is based on — flag if it should be cut. Every persona's episodic
history within a domain is built as one non-contradictory timeline shared across that persona's
probe items, so domain-relevant information accumulates across probes instead of resetting with
each one; this is enforced at generation time, not checked post hoc.

**Quality Gate.** Two of the three conditions above are themselves controls, not just data: the
distractor condition adds a lure whose embedding cosine to the query is at least as high as the
true evidence's, so it is competitive rather than a random irrelevant fact; the absence condition
removes the evidence entirely and requires abstention. Every candidate item, regardless of
condition, is then scored by the judge (§3.3) against evidence presence, link validity, and
leakage/shortcut criteria; only items scoring above the release threshold become a binary
pass and enter the corpus. [PEER REVIEW: the team's stated threshold is a score >90; the
threshold implemented in `quality_audit.py` today is `normalized_total >= 0.8` on a 0–1 scale —
confirm which is current before this number goes in the paper.]

### 3.3 Judge

Two distinct judges certify a candidate item before release — not to be confused with the
agent-answer judge in §4.4, which grades a model's response during evaluation, not a candidate
item during construction.

**Human Judge.** A reviewer checks three properties directly: whether real evidence is present
(not a placeholder), whether the associative link between $ev_A$ and $ev_B$ is valid and correctly
typed (§3.1), and whether the latent conclusion $C$ is genuinely supported yet never explicitly
stated anywhere in agent-visible text. Failing any of the three is sufficient to reject the item
regardless of the other two.

**LLM Judge.** The same three properties are checked by an LLM at scale, as a cheap pre-filter
ahead of human review rather than a substitute for it (self-preference bias means a model tends to
rate its own generations well): evidence presence is checked behaviorally, by having the model
answer the item three times at increasing context — query only, the two most recent sessions, and
the full dialogue — and flagging it if the item is answered correctly without abstaining at either
of the first two levels (a shortcut indicates weak evidence separation, regardless of what a static
lexical/embedding proxy over the query and evidence text would separately suggest); link
validity is checked by blind classification of each typed edge, compared against the label the
item's construction assigned; latent-conclusion faithfulness is checked by scanning whether the
rationale a full-context answer would need is actually supported by cited evidence and never
appears verbatim in agent-visible text. Full prompts for all three checks are in the appendix.

---

## 4 Experiment Setup

### 4.1 Models

We evaluate three classes of system: long-context single-pass baselines (full history in context,
no external memory), retrieval-augmented baselines (flat top-*k* RAG over the same stored facts),
and external-memory agents, instantiated as described below. Models are drawn from both
proprietary and open-weight families, the latter served through Hugging Face, so that later
comparisons across model generations (e.g., a newer release against its predecessor) reuse the
identical harness rather than requiring a separate evaluation path per provider.

**External-memory baseline implementation.** AssoMemBench does not propose a new agent
architecture — §1.5 lists a benchmark, an evaluation pipeline, and baselines as the contribution,
not a novel system. The external-memory class above still needs a concrete instantiation to be run
at all, and we build it entirely from mechanisms with independent prior grounding: atomic-fact
extraction and deduplication (Mem0-style), graph-structured note linking (A-MEM; Xu et al. 2025),
spreading activation via personalized PageRank over that graph (HippoRAG; Gutiérrez et al. 2024),
recency-relevance-importance retrieval and importance-gated reflective insight generation
(Generative Agents; Park et al. 2023), and Ebbinghaus-curve memory consolidation (MemoryBank;
Zhong et al. 2024) — reimplemented from the retention form specified in the original paper
($R = \exp(-t/S)$) rather than the published reference code, whose retention computation reduces
to $\exp(-(t/5)\cdot S)$ under standard operator precedence and would make stronger memories decay
faster. The instantiation exists so the pipeline-component ablations (§4.2) have concrete,
independently-motivated mechanisms to isolate; it is infrastructure for the ablation study, not a
result in its own right. Graph linking and spreading activation serve the co-activation/bridge
mechanism (§3.1) and are treated as one ablatable unit rather than two — linking with activation
disabled produces an empty working graph, which collapses to the same downstream behavior as
activation with linking disabled, so a standalone "no-links" condition would be redundant by
construction. Reflective insight generation and consolidation serve temporal (`updates`-typed)
items and are independent code paths with no such collapse, so both get their own single-factor
ablation condition (§4.2).

Before committing a model or a newly generated data batch to a full run, we pass it through a
fixed pilot query set, held out from the main corpus so results are comparable across models and
batches without being re-selected per run. Because pilot-set accuracy alone cannot distinguish
genuine association from a correct guess, each pilot pass is scored at the same three context
levels used for discriminant validity (§3.3: query only, partial history, full history) rather
than full-context accuracy alone, so a pilot pass already yields a preliminary associative-
difficulty estimate before a model is scaled to the full corpus. The pilot set is being scaled to
50 queries; an initial smoke pass has been run at smaller scale against one open-weight model to
validate the protocol end to end.

**The `memory_only` ablation and the retrieval-augmented baseline are not the same condition.**
The `memory_only` pipeline-component ablation in §4.2 disables association, linking, reflection,
and consolidation on the external-memory baseline (§4.1), but it still retrieves through the same
recency-relevance-importance scoring as the full pipeline — it is not a naive top-*k*
similarity retriever. The retrieval-augmented baseline in this section is a separate, independently
implemented system using flat cosine top-*k* only. We report both because they answer different
questions: `memory_only` isolates which mechanism of the external-memory baseline matters, holding
the retrieval scorer fixed; the flat-RAG baseline asks whether a conventional, externally-recognizable RAG system
clears the bar at all. Collapsing them into one row would understate the ablation's precision.

### 4.2 Ablation Protocol

Five ablations isolate different sources of the target capability. The first three operate on the
data, in decreasing order of scope (item-level, then one component of the item, then one piece of
evidence within it); the remaining two operate on the external-memory baseline's pipeline (§4.1).

| Ablation | Manipulation | Tests |
|---|---|---|
| **Association injection** (headline) | Same conversation, with vs. without the injected cue/bridge/distractor, length- and position-matched (below) | Whether performance rises specifically on the bridge construct post-injection, not uniformly — tested as a condition × relation-type interaction, not by inspection. [PEER REVIEW: data source unresolved, see prose below] |
| **Distractor removal** | Same item, lure session replaced by a length-matched neutral filler session (not deleted) | Whether the distractor was doing real interference work, isolated from any effect of shortening the context — reported as Distractor Invariance Rate (§4.3) |
| **Counterfactual variants** | Materialized `evidence_removed` / `evidence_replaced` / `cue_removed` siblings | Two distinct checks (below): the gold label flips as specified, *and* the model's answer flips accordingly — the second is reported as Counterfactual Flip Consistency (§4.3) |
| **`no_assoc`** | External-memory baseline, spreading activation disabled (linking left on; §4.1 argues this also covers a standalone "no-links" condition) | Whether the co-activation/bridge mechanism (§3.1) specifically drives performance |
| **`no_reflect` / `no_forget`** | External-memory baseline, reflective insight generation disabled / Ebbinghaus consolidation disabled, each independently | Whether insight generation and whether decay of superseded beliefs each independently drive performance on temporal (`updates`-typed) items |

**Content-matched controls.** Injection and distractor removal both change context length if
implemented as naive insertion/deletion; either change could shift performance on its own,
independent of the associative relation being tested. We therefore require the non-injected /
distractor-removed condition to be padded with neutral filler of matched token length, and the
injected cue's session position to be drawn from the same position distribution as in the
non-injected condition (not fixed at a constant offset), so a model cannot solve the ablation by
learning "check near the end" rather than by finding the cue.

**Specificity as a statistical test, not a plot.** "Rises specifically on the bridge construct" is
tested as an interaction contrast — (post-injection $-$ pre-injection) on injected items vs. the
same delta on a non-bridge control — rather than reported as two bar heights that look different.
A jump that is not significant is a negative result for the injection's construct validity and is
reported as such (§3.1), not smoothed over. [PEER REVIEW: both this paragraph and the injection
row above presuppose an "original, pre-injection" sibling item, which an earlier draft's
LoCoMo-retrofit track supplied. §3.2 in this pass describes only the native pilot corpus per the
distilled outline; confirm whether the retrofit track still exists elsewhere before this ablation
is run — if not, it needs a native-corpus-only redesign (e.g., associative arm vs. distractor arm
as a same-persona proxy for "with vs. without a competing bridge," which is a different
manipulation and should be named as such, not silently substituted).]

**Counterfactual variants, two distinct uses.** (i) At construction time, a human reviewer confirms
the materialized gold label is internally consistent with the removed/replaced evidence — this is
a corpus-QA check, run once per item before release. (ii) At evaluation time, the same variant is
run through every model under test, and we score whether *the model's* answer changes in the
predicted direction, not only whether the annotation says it should. For `evidence_removed`
variants specifically, we additionally split "correctly abstained" from "answered confidently and
wrongly" (via the calibration metric, §4.3) rather than collapsing both into one failure count,
since only the second is evidence the model is fabricating personalization from plausibility.

**Oracle-evidence condition, defined precisely per system.** For the external-memory baseline,
oracle evidence means seeding working memory directly with the item's target-evidence notes and
running `REASON` unchanged, bypassing `RETRIEVE`/`ASSOCIATE` entirely — this isolates
combination/usage failure from retrieval failure by construction, not by inference from a score
delta. *This bypass path does not exist in the current codebase* (`AssociativeMemoryAgent.
answer()` always calls `retrieve()`; see Grounding notes) and needs a small addition before this
condition is runnable. For systems without an inspectable retrieval stage (proprietary APIs,
long-context baselines), the equivalent operationalization is a reduced context containing only the
target-evidence sessions — mechanically different from the external-memory-baseline bypass, but
answering the same question ("given the evidence, can it be combined correctly"), and we state
explicitly in any results table which
operationalization produced which number, since the two are not interchangeable at the
implementation level even though they are at the question level.

**Contamination cross-check.** [PEER REVIEW: this entire check, as previously drafted, presupposed
a LoCoMo-retrofit track that drew on public corpora a model may have seen in pretraining, and
required the injection ablation's headline result to replicate on a fully native, unpublished
subset before being trusted. §3.2 in this pass no longer describes a retrofit track. If one still
exists outside this document, restate it in §3.2 so this check has a data source; if the corpus is
now native-only by design, the contamination concern this check existed to address may not apply
at all — worth confirming rather than silently dropping the check.]

**Scope.** The `no_assoc`/`no_reflect`/`no_forget` conditions are defined only for the
external-memory baseline (§4.1); proprietary and long-context baselines have no internal mechanism
to toggle, so this row of any results table will only ever contain external-memory-baseline
numbers, by construction rather than by omission. All five ablations are additionally run under
both the standard-retrieval and oracle-evidence conditions above, and all are run on the corpus
overall and broken out by domain (§3.1), since domain-specific bridge themes (physiological,
cognitive, social, financial) are not assumed equally difficult.

**Confirmatory vs. exploratory, and a floor on N.** The injection ablation's bridge-specificity
interaction test is the paper's one confirmatory hypothesis (contingent on the data-source
question flagged above); every other comparison in this section is exploratory and reported
without multiple-comparison correction, but labeled as exploratory rather than presented at equal
evidentiary weight. We do not report an effect size, confirmatory or exploratory, for any stratum with fewer
than 30 items; strata below that floor are reported as raw counts only.

### 4.3 Evaluation Metrics

We report one headline composite, five metrics that feed it, and three supporting diagnostics that
do not — collapsing the five into one number risks hiding exactly the failure modes §1.2–§1.3
argue final-answer accuracy already hides, so each component is also reported on its own. All are
computed from a single judge call's output contract (`score01`, `constraint_satisfaction`,
`is_associative`, `target_evidence_used`; §4.4), so no metric requires a second pass over the data.

**Associative Reasoning Index (ARI), headline.** A weighted composite over the five model-behavior
metrics below, minus a calibration penalty on the same self-reported-confidence signal used in the
Reasoning Score (below):

$$ARI = \tfrac{1}{5}\big(REA + JER + DIR + F1_{abstain} + CFC\big) - \beta(\hat p - g)^2$$

with $\beta$ and $g$ (joint correctness) defined as in the Reasoning Score. Equal weighting is the
default for transparency; report a weighted variant only alongside the equal-weighted number, not
in its place. **Leakage/Shortcut Rate (below) is deliberately excluded from ARI**: it measures
corpus quality, not model behavior, and a model cannot improve it — folding it into a
model-comparison composite would conflate the two.

**Required-Element Accuracy (REA).** Mean per-constraint satisfaction, $\frac{1}{K}\sum_k x_k$,
unweighted — the simplest possible reading of "how much of the required answer did the model get,"
reported for every item with `required_elements`/`constraints`. This is deliberately the
un-discounted sibling of the Reasoning Score below: REA is the headline number precisely because it
needs no explanation of step-discounting to read.

**Joint Evidence Recall (JER) and Target-Evidence Coverage.** JER is the strict, conjunctive
reading — $\prod_k \text{target\_evidence\_used}_k$, i.e. 1 only if the judge credits the rationale
with using *every* target evidence id, 0 otherwise. Target-Evidence Coverage is its partial
sibling — the mean of the same per-evidence booleans — kept as a continuous diagnostic for
failure-mode case studies (which specific evidence piece gets missed) rather than folded into the
headline pair. This is the same partial/strict duality as the Reasoning Score's $x_k$ vs.
$\prod_k x_k$, applied one level down at the evidence-recall stage instead of the answer stage.

**Distractor Invariance Rate (DIR).** For distractor-arm items only: the fraction where the
judge-cited rationale does not rely on the labeled distractor, i.e. $1 - \text{Fool Rate}$. Reuses
the same `uses_distractor` check `eval/quality_audit.py` already computes during corpus
construction (`pred_idxs & distractor_idxs`), applied here at evaluation time to a model's answer
rather than at construction time to a corpus candidate — same test, different subject.

**Abstention Precision/Recall/F1.** For absence-condition items (§3.2): treat "should abstain"
(`is_answerable=False`) as the positive class and "did abstain" as the prediction, and report
standard precision/recall/F1 rather than a single accuracy number, since the two failure directions
are not equally costly — answering confidently when unsupported (hallucinated personalization) is
the more serious error and is visible as low precision, not low recall. $F1_{abstain}$ is the ARI
input; precision and recall are reported alongside it, not summarized away.

**Counterfactual Flip Consistency (CFC).** Formalizes the eval-time half of the counterfactual
check already described in §4.2: the fraction of `evidence_removed`/`evidence_replaced`/
`cue_removed` variant pairs where the model's own prediction changes in the direction the
materialized `expected_gold` specifies. This is derived, not judged directly — it is a function of
the base item's outcome and the variant's outcome, both already scored by the same judge call.

**Supporting diagnostics, not part of ARI.**
- **Associativity Rate** — the fraction of *correct* answers where the judge's `is_associative`
  flag is 1, i.e. success required genuinely combining evidence rather than a lucky single-fact or
  generic-knowledge guess. Nothing in REA/JER/DIR/CFC captures this "right answer, wrong reason"
  distinction on its own — REA credits a constraint as satisfied regardless of *why* it was
  satisfied — so this is retained from the previous draft rather than superseded by the new suite.
  [TODO: the precedent for reporting two metrics that can diverge rather than one is π-Bench's
  task-completeness / proactivity split; confirm the correct citation before submission — the
  working-draft key `Zhang et al., 2026` currently collides with the "AssoMem" system cited in
  §2.1, which is a different paper under the same key.]
- **Reasoning Score (RS)** — retained as the per-item score for *step-ordered* long-horizon items
  specifically (e.g. LongMemEval knowledge-update chains, where constraint order encodes which
  belief supersedes which), rather than as the corpus-wide headline metric. For multi-constraint
  items, per-constraint satisfaction $x_k \in [0,1]$ combines with step-discounted weights
  $\tilde w_k = \gamma^{k-1}/\sum_j \gamma^{j-1}$ and self-reported confidence $\hat p$ that all
  constraints hold:

  $$RS = (1-\lambda)\sum_k \tilde w_k x_k + \lambda\prod_k x_k - \beta(\hat p - g)^2, \quad g=\prod_k x_k$$

  Worked example: $K=4$, $x=[1,1,0,1]$, $\hat p=0.7$ gives $RS=0.225$ — three of four steps
  satisfied, but the calibration penalty removes nearly half the partial credit because reported
  confidence overshoots the true joint correctness ($g=0$). Constraint order affects this score by
  construction (step-discounting is order-sensitive), so RS is only meaningful where the item's
  constraint list has a real narrative order — most items do not, which is why REA (order-blind) is
  the default and RS is scoped to the subset where order is part of the construct.
- **Calibration (ECE / Brier).** Expected calibration error and Brier score over confidence
  gradients, distinct from Abstention P/R/F1 above: P/R/F1 scores the binary abstain/answer
  *decision*, ECE/Brier scores whether the model's *reported confidence* is trustworthy across its
  full range, including on items it does answer. Both are needed; neither substitutes for the
  other.

**Leakage / Shortcut Rate (LSR) — corpus health, not a model metric.** A deterministic,
judge-free scan (no LLM call) for the two authoring-bug classes in §3.3: an annotation field or the
gold answer appearing verbatim in agent-visible context. Computed once per corpus release, expected
near-zero on any released item by construction (§3.3 rejects items that fail this check before
release), and reported as a corpus-health statistic in the data section rather than a per-model
result — a model's LSR-relevant behavior is actually measured by the three-context-level shortcut
probe in §4.1/§3.3, which is a different, per-model quantity that happens to reuse similar
machinery. Reporting both under one name would conflate a corpus property with a model property;
they are kept separate here for that reason.

**Associative Difficulty Gap.** Named as a contribution in §1.5 but not previously given a formula.
§3.1 no longer distinguishes direct-cue from cross-domain item types (every associative item is a
bridge, §3.1), so we define the gap using the oracle-evidence contrast already required for every
ablation (§4.2) instead: the REA delta, per domain and persona, between the oracle-evidence
condition (the cue is effectively made direct — the evidence is handed to the model) and the
standard-retrieval condition (the cue stays indirect):

$$\Delta_{assoc} = \overline{REA}_{oracle} - \overline{REA}_{standard}$$

computed per model rather than pooled, so that comparing a newer model generation against its
predecessor (§4.1) asks whether $\Delta_{assoc}$ *narrows* — the model got specifically better at
combining/using evidence once it has it, i.e. more associative, not just a better retriever —
rather than whether raw accuracy rose, which a model can do by retrieving better without the
combination step itself improving. A narrower $\Delta_{assoc}$ with flat oracle-condition
performance is the signature we want; a model that raises both conditions equally is evidence of
general capability improvement, not construct-specific improvement, and should be reported as such
rather than folded into one "model got better" claim. [PEER REVIEW: this redefinition follows
directly from removing the A1–A5 taxonomy from §3.1 in this pass; confirm it still matches what
§1.5 intends by "direct-cue and associative conditions" before it goes in a submission — the
oracle/standard contrast is the most literal reading available given the current corpus design,
but it is a reinterpretation, not a restatement, of the original contribution language.] (Defined
on REA rather than RS because REA is the order-blind default — §4.3 above; recomputing
$\Delta_{assoc}$ on RS for the step-ordered subset is a reasonable secondary cut, not the headline
number.)

### 4.4 Judge Protocol

**Human.** A panel evaluates a stratified subset across two passes: a difficulty/sanity pass, in
which every item receives one independent reviewer answer compared against the eventual agent
output, and an inter-annotator-agreement pass, in which a random 10–15% slice receives a second
independent reviewer and Cohen's $\kappa$ is computed on the overlap. We treat $\kappa \geq 0.7$ on
"does this item require associative retrieval" as the bar for proceeding, and $\kappa < 0.6$ as a
signal to simplify the construct rather than discard disagreeing items and continue.

**LLM.** A reference-guided, chain-of-thought judge (following G-Eval; Liu et al. 2023) with the
strict-output-format protocol of MT-Bench (Zheng et al. 2023). Bias controls: the judge is drawn
from a different model family than the agent under test, pairwise comparisons require agreement
under order-swap, and the prompt includes an explicit verbosity guard. The judge always receives
the full, untruncated target-evidence text regardless of how the general context is truncated for
length, and returns accuracy, associativity, and per-evidence usage in a single structured call so
every reported number traces to one deterministic entry point.

### 4.5 Implementation and Reproducibility

The harness runs against a swappable backend: a deterministic offline backend for reproducing
harness logic in CI without an API key, and real model backends (proprietary APIs and Hugging
Face-served open weights) for all reported numbers. Confidence intervals are percentile bootstrap
over items; all metrics, prompts, and the judge's output contract are implemented behind a single
entry point so that any reported number can be regenerated from the released code and corpus.

---

## Grounding notes (2026-07-16, not for the paper)

What this draft's factual claims were checked against, and what is still open. Kept here rather
than silently fixed so nothing gets lost before submission.

- **Corpus counts.** 1,909 legacy-track items confirmed via `data/build/items.jsonl` (locomo 937 /
  longmemeval 241 / memoryarena 701 / partner_generated 30). Native-pilot track: `assomem_pilot/`
  base confirmed at 450 (150 × health/hobby/work). The `hobby copy/` batch confirmed at 300 files,
  of which 150 share `sample_id`s with the existing `assomem_pilot/hobby` batch and 150 are
  genuinely new — matching the "150 new in hobby" figure from the team update. **The reported
  total of 900 could not be verified on disk**: only the hobby-domain extension exists as a
  separate folder right now; no equivalent `health copy` / `work copy` extension is present in this
  checkout. Recommend confirming with whoever generated the other two domains' extensions before
  this number goes in a paper.
- **Multi-session coherence status.** The `hobby copy` S6–S10 extension no longer reproduces the
  cross-file date contradiction found in the original `assomem_pilot` batch (session dates that
  collided with different content in each sibling file) — spot-checked `AMB_HH_u01_associative_S6`
  vs `S7`, filler sessions now match verbatim rather than conflicting. This is real progress, but
  the fix is still "reuse identical filler," not "accumulate new information" — the abundance
  half of the original feedback (§3.2 "Multi-session coherence") is not yet addressed by this
  batch. Text above states the requirement as adopted; it does not claim the extension already
  satisfies it.
- **External-memory baseline mechanisms.** Cross-checked against `src/assomem/{store,associate,
  retrieve,reason,consolidate}.py` docstrings directly, including the Ebbinghaus retention-formula
  correction, which is a real, verifiable difference from the cited reference implementation, not
  an inference.
- **Ablation presets and metric formulas.** Verified against `src/assomem/agent.py`
  (`AgentConfig.memory_only()`, `use_association`/`use_reflection` flags) and `eval/metrics.py`
  (`reasoning_score`, `bootstrap_ci`, `cohen_kappa`) line by line; formulas above match the code
  exactly.
- **Judge protocol.** Verified against `eval/judge.py` (`JUDGE_SYSTEM`, `JUDGE_USER_TMPL`,
  `judge_answer` return contract) and `data/discriminant_gate.py` / `eval/quality_audit.py` for the
  three-context-level shortcut probe reused in §4.1.
- **Found but not used — flagging, not included above.** `src/assomem/dataset_normalizer.py`,
  `dataset_schema.py`, `dataset_adapters.py`, and `dataset_extraction.py` implement a second,
  independent case schema (`BenchmarkCase`/`MemoryEvent`/`RelationCandidate`, schema version
  `assomem-unified-v0.2`, supporting a `longbench` source not mentioned anywhere else in the
  project). Nothing in `eval/`, `data/build_dataset.py`, or `src/assomem/__init__.py` imports or
  reads its output. It is not referenced in this draft because it is not part of the pipeline that
  actually produces reported numbers; worth a five-minute check with whoever wrote it (commit
  `c44fff8`) to confirm it is superseded rather than something that got missed.
- **π-Bench citation.** Left as an inline TODO in §4.3 rather than guessed — resolving it also
  resolves the `Zhang et al., 2026` key collision with the "AssoMem" system cited in Related Works.

### 2026-07-16, second pass — hardening the ablation design

Added after re-reading §4.2 adversarially (assume a strict reviewer is trying to find the weakest
point in the design, not just checking numbers against the code). Two code-grounded findings and
two implementation gaps this pass surfaced:

- **`no_links` redundancy is a code fact, not a design opinion.** Verified in `agent.py`:
  `associate()` only runs `if self.cfg.use_association and self.edges`, and `self.edges` is only
  populated `if self.cfg.use_links`. Setting `use_links=False` therefore leaves `self.edges` empty,
  which makes the `use_association` branch false regardless of its own value — identical downstream
  behavior to `use_assoc=False`. A standalone `no_links` ablation would measure nothing that
  `no_assoc` doesn't already measure. This justified merging them in §3.4/§4.2 rather than adding a
  sixth condition.
- **`no_forget` was a real gap, now closed in the design.** The previous draft attributed A4
  performance to "reflective consolidation" as one mechanism, but only `no_reflect` existed as an
  ablation — consolidation (`consolidate.py`, the Ebbinghaus decay step) had no matching condition.
  Fixed by splitting the claim into two independent mechanisms (§3.4) and adding `no_forget` as a
  fifth ablation condition (§4.2).
- **Implementation gap 1 — oracle-evidence bypass does not exist yet.** `AssociativeMemoryAgent.
  answer()` (`agent.py`) unconditionally calls `RT.retrieve(...)`; there is no parameter or method
  to seed working memory directly from `target_evidence_ids` and skip retrieval. §4.2's
  oracle-evidence definition for the external-memory baseline describes the intended behavior; it
  needs a new method (e.g. `answer_with_oracle_evidence(item)`) before it is runnable, not just a
  CLI flag.
- **Implementation gap 2 — `no_forget` is not a registered ablation choice.** `eval/run_eval.py`
  and `eval/run_eval_trace.py` both hard-code `choices=["full", "memory_only", "no_assoc",
  "no_reflect"]` for `--ablation`. Adding `no_forget` to the design (above) requires adding it to
  both argparse choices and the corresponding `AgentConfig(use_forgetting=False)` branch in each
  script — small, but not yet done, so §4.2 as written describes five conditions of which only
  four currently have a runnable flag.
- **Not yet grounded — left as designed-but-unverified.** The content-matched-control token-length
  padding, the position-randomization requirement for injected cues, and the ≥30-item floor on
  reported strata are new requirements this pass added to close confound holes; none has been
  checked against what the `assomem_pilot` generators (`blueprints_health/hobby/work.py`) actually
  do today. Treat §4.2's confound-control paragraphs as the target design, same status as the
  multi-session-coherence requirement in §3.2 — stated, not yet verified as implemented.

### 2026-07-18, third pass — metrics suite reconciliation

The team supplied a new metric list (REA / JER / DIR / Abstention P-R-F1 / CFC / LSR / ARI)
independently of this draft's original three-metric framing (RS / Associativity Rate /
Target-Evidence Coverage). §4.3 is rewritten around the new suite; nothing from the old framing was
silently dropped — each old metric is either kept as a named diagnostic (Associativity Rate, RS,
ECE/Brier) or repositioned as the partial/strict sibling of a new one (Target-Evidence Coverage ↔
JER). Two judgment calls made in reconciling them, flagged here rather than presented as settled:

- **ARI's formula and equal weighting are proposed, not specified upstream.** The team's list
  labeled ARI "weighted composite" with no formula. The equal-weight-of-five-minus-calibration-
  penalty form above is one reasonable choice grounded in what's already implemented
  (`reasoning_score`'s calibration term), not a number handed down — confirm the weighting (equal
  vs. learned vs. task-specific) before this goes in a submission.
- **LSR's exclusion from ARI is a correctness argument, not a style preference.** A composite meant
  to compare *models* should not include a quantity that only reflects *corpus* quality, since no
  model's behavior can move it. Worth double-checking this was the intent before assuming it — if
  LSR was meant to also capture a model's tendency to exploit leaked strings when present, that is
  a different, still-undefined metric and would need its own name.
- **Associative Difficulty Gap redefined on REA instead of RS** (previously RS) now that REA is the
  order-blind default metric — flagged in §4.3 itself, repeated here since it changes a formula
  introduced in an earlier pass.

### 2026-07-18, fourth pass — data construction rewrite; "Reference Agent" reframed

Two explicit instructions this pass: (1) keep every §3.2 subheading under 300 words — verified by
word count, see below; (2) the project has no reference agent, so §3.4 and every cross-reference to
it needed reframing, not just a rename.

- **§3.2 word counts, verified, not estimated.** Item Schema 124, Retrofit Sources 117, Native
  Pilot Corpus 100, Relation Typing 176, Multi-Session Coherence 99 — all under the 300-word cap.
  Split "Sources" into "Retrofit Sources" and "Native Pilot Corpus" and added a new "Relation
  Typing" subheading; net five subheadings, none over the cap.
- **"Reference Agent" → "External-Memory Baseline Implementation."** Reframed as infrastructure
  the ablation study needs, not a contribution, matching §1.5's actual contribution list (benchmark
  + pipeline + baselines, no novel architecture claimed). Every downstream cross-reference —
  §4.1's model-class description, the `memory_only`-vs-flat-RAG disambiguation, the ablation table,
  the oracle-evidence definition, the scope note, and two Grounding-notes entries — was updated to
  match; grepped the file afterward for "reference agent" / "reference pipeline" and confirmed zero
  remaining occurrences.
- **New unresolved item found while grounding §3.2 against the Introduction and Limitations text.**
  The Limitations' "Generalization" paragraph names "3 current categories" expanding to "(1) social
  (2) spatial," and separately lists spatial context and social relationships again inside its
  *relation-types* enumeration (temporal/causal/analogical + spatial/social/affective/goal/
  procedural/schema). These read as two different axes — domains (health/diet, hobby/habit,
  work/learning, +2 more) vs. relation types (temporal/causal/analogical, +2 more) — that happen to
  reuse the words "social" and "spatial" for both. §3.2 now states only the confirmed 3 domains and
  does not guess what fills the remaining domain slots; §3.2's Relation Typing subheading places
  the social/spatial extension where the source text supports it more directly (the relation-type
  list). This is flagged, not resolved — confirm with whoever wrote the Limitations section which
  axis "social" and "spatial" actually belong to, since as written it can be read either way.

### 2026-07-18, fifth pass — restructured around the distilled outline (3.1 design / 3.2 data / 3.3 judge)

This pass replaced the entire §3 with the user's own distilled structure and removed everything not
in it, rather than incrementally editing. Two things this resolved, two new things it opened up.

- **Domain list resolved.** The previous entry above (fourth pass) flagged "social" and "spatial"
  as ambiguous between the domain axis and the relation-type axis. This message's outline states
  the domain list directly: health, work, hobby, social, finance. §3.1/§3.2 now use this list;
  "spatial" is not a domain in this version, only a possible future relation type (§3.1's Relation
  Typing subheading, carried over unchanged). Treat the domain-axis ambiguity as resolved by this
  message; the relation-type-axis question (does "spatial" ever get added there too) is unaffected
  and still open.
- **A1–A5 taxonomy removed, not hidden.** The distilled outline operationalizes one construct
  (co-activation via $ev_A \times ev_B \rightarrow C$, hop-1/hop-2) rather than five association
  types, which also matches what the native pilot corpus actually labels — every associative/
  distractor item in `assomem_pilot` is `association_type: A3_cross_domain` and every absence item
  is `A5_absence_control`; A1/A2/A4 were never populated by this track. Removing the taxonomy from
  §3.1 makes the Method section match the corpus, not just the outline.
- **New problem: removing the retrofit track breaks three things in §4.2 that depended on it.**
  The distilled §3.2 outline describes only the persona-based native corpus, with no mention of the
  four-corpus retrofit track (LoCoMo/LongMemEval/MemoryArena, 1,909 items) that earlier passes'
  §3.2 described. Following the outline literally, this pass removed that track from §3.2 — but
  the injection-ablation row, its specificity test, and the contamination cross-check in §4.2 all
  explicitly depended on comparing an "original" retrofit-track conversation against an injected
  version of it. All three are now marked `[PEER REVIEW]` in place rather than silently rewritten,
  because there are three genuinely different resolutions (retrofit track still exists and should
  be restated in §3.2; retrofit track is gone and these three need a native-corpus-only redesign;
  or the injection ablation is being retired) and guessing wrong would be worse than leaving it
  open. The Associative Difficulty Gap formula (§4.3) was also redefined away from an A1∪A2-vs-A3
  contrast (which no longer has a referent) to an oracle-vs-standard-retrieval contrast, which is
  independently grounded in machinery §4.2 already requires — flagged in place as a
  reinterpretation of §1.5's contribution language, not a restatement of it.
- **Quality-gate threshold stated as a discrepancy, not picked.** The message describes a >90,
  binary pass/fail gate. `quality_audit.py`'s implemented threshold is `normalized_total >= 0.8`
  (an 80% cut on a 0–1 scale). These may be the same rule described on different scales, or two
  different rules — `annotated_100.csv` separately has a `fitness_score` column on a 0–100 scale
  where the one confirmed PASS example scores 91, which is consistent with a ">90" reading that
  `quality_audit.py`'s 0.8 does not obviously match. Stated as an open discrepancy in §3.2 rather
  than resolved by assuming which system is authoritative.
- **External-Memory Baseline Implementation relocated, not deleted.** Since Method is now strictly
  3.1–3.3, the system description that used to be §3.4 moved into §4.1 (Models) as an
  "external-memory baseline implementation" subsection, with its mechanism-to-construct mapping
  restated in the new vocabulary (co-activation/bridge; temporal `updates`-typed items) instead of
  A1–A5. All internal §3.4 cross-references were repointed to §4.1; grepped afterward to confirm
  none remain.

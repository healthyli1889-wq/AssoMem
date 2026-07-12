# AssoMem — Introduction (AAAI-oriented draft)

**Status.** Camera-ready English Introduction, rewritten to the 6-paragraph causal chain in the review feedback. Experimental numbers marked `[EXP: …]` until model evals land.  
**Repo context.** Native pilot: 450 items · 3 domains (health/diet, work/learn, hobby/habit) · 10 personas · 5/5/5 arms · DATA_STANDARD v1.

---

## 0. Framework extracted from AAAI / NeurIPS outstanding papers (what we copied)

Top-tier intros (AAAI Outstanding / NeurIPS D&B construct papers such as *Misspecification in IRL*, *DivShift*, *Measuring what Matters*) share a **topic-tailored** skeleton, not boilerplate motivation:

| Step | Pattern | How we instantiate it for AssoMem |
|------|---------|-----------------------------------|
| 1 | **Observable failure in the deployment regime**, not a slogan | Memory that “pipes” facts ≠ agents that *act* from incomplete user cues (STATE-Bench; MemoryArena) |
| 2 | **Name the mechanism**, with a formal contrast | Retrieval (query→nearest stored chunk) vs associative **pattern completion** (partial cue→attractor→full bound pattern) |
| 3 | **Field gap as construct invalidity**, not “papers exist” | Benchmarks organize by *task/setting*; they do not operationalize cue-driven binding under controlled cue–target disconnect + interference arms |
| 4 | **Borrow a validated measurement toolbox** (construct validity) | Hippocampal multi-element binding / pattern-completion paradigms → agent tasks + V1/V2/A5 controls (Bean et al. NeurIPS’25: operationalize the phenomenon) |
| 5 | **One construct + one quantitative preview** | AssoMem + associative difficulty gap / last-mile binding bottleneck `[EXP]` |
| 6 | **Falsifiable prediction + auditably scoped contributions** | Binding—not retrieval capacity—will dominate long-horizon autonomy; 3 bullets only |

**Causal glue inside each paragraph:** *failure phenomenon → mechanism diagnosis → structural gap → construct / instrument*. Biology appears only after the field gap, as **construct separability + measurement tools**, never as primary motivation.

---

## 1. Introduction

Modern LLM agents are increasingly expected to accumulate and reuse user-specific knowledge across weeks and months, not only within a single conversation. In that regime, “having memory” is not optional: long-horizon decisions depend on reactivating past interactions rather than re-deriving constraints from scratch each time. Yet production-oriented evaluations show that the bottleneck is rarely a missing fact in isolation. STATE-Bench argues that most memory benchmarks are retrieval tests—“That tells you the pipe works. It doesn’t tell you that the agent performs better”—while enterprise failures arise when agents botch procedures, skip policy checks, or reuse incomplete user state (Microsoft, 2026). MemoryArena makes the same cut for agentic settings: systems near-saturated on static long-context memory benchmarks still fail when memory must guide interdependent, multi-session decisions (Hu et al., 2026). The operative failure mode for *personal* agents is therefore not amnesia of isolated facts, but **associative failure**: a partial, lexically dissimilar cue that should reinstate a bound user pattern (habits, constraints, prior outcomes) fails to do so, and downstream action degrades.

Existing agent memory stacks largely inherit an **information-retrieval** view of memory: given a query, retrieve the most similar past chunk, treating memory as a key–value store (surveyed in Hu et al., 2026a; Zhang et al., 2025). Cognitive science and computational associative memory draw a sharp contrast. In multi-element episodic memory, events are stored as coherent bound representations; a partial cue can reinstate the full pattern through **pattern completion**, with behavioral dependency across elements of the same event (Horner & Burgess, 2013, 2014; Horner et al., 2015). Modern Dense Associative Memory / Hopfield-style models formalize the same idea as energy-based attractor dynamics: degraded or incomplete inputs settle into stored basins rather than nearest-neighbor lookup alone (Krotov & Hopfield, 2016; Hoover et al., 2024). This is not rhetorical biology. It specifies a computational signature that retrieval-only systems are not required to exhibit: **partial-cue, low-overlap, multi-element reinstatement**.

Recent benchmarks are increasingly cognitively motivated, but they remain organized around broad tasks or application settings rather than a controlled operationalization of cue-driven associative binding. We group them into two overlapping divisions. *(i) Long-context conversational memory*—LoCoMo (Maharana et al., 2024), LoCoMo-Plus (Lee et al., 2026), LongMemEval and related suites—stress retention, multi-hop QA, temporal reasoning, and, in LoCoMo-Plus, cue–trigger semantic disconnect for latent constraints. *(ii) Agentic memory*—MemoryAgentBench (Hu et al., 2025), MemoryArena (Hu et al., 2026), STATE-Bench (Microsoft, 2026)—decompose competencies such as accurate retrieval, test-time learning, long-range understanding, conflict resolution, or memory–action coupling in multi-session loops. These advances matter. Still, across both divisions, evaluation is typically structured as directed retrieval or constraint application when the target is reachable by semantic proximity, explicit instruction, or an already-named state key. Even when cue and trigger diverge lexically, the construct under test is rarely **associative binding itself**: pattern completion from partial cues across bound feature combinations, under interference that flat similarity ranking prefers the wrong session, and under absence controls that demand abstention when evidence was never stored. Table 1 summarizes this landscape: retention, revision, and long-horizon action are covered; controlled pattern completion with matched direct-cue vs associative difficulty is not.

Biology is not our motivation; it is our source of **construct validity**. Cognitive neuroscience shows that associative binding is supported by dedicated hippocampal–cortical circuitry and exhibits distinct behavioral signatures—holistic multi-element reinstatement and cue-driven completion—that have been measured for decades with partial-cue and closed-loop association paradigms (Horner & Burgess, 2013, 2014; Horner et al., 2015). Concurrently, the LLM evaluation literature warns that many benchmarks fail construct validity: abstract phenomena are under-defined, and tasks are borrowed without proving they measure what they claim (Bean et al., 2025). The hippocampal literature supplies what ad hoc agent tasks usually lack: a **validated measurement toolbox**—partial cues, multi-element dependency, interference, and negative controls—that can be adapted into agent benchmarks instead of inventing metrics from scratch. In short: the field gap is the missing construct; biology supplies separability and instruments.

In this work we introduce **AssoMem** (Associative Memory Benchmark), the first agent memory benchmark that isolates **cue-driven associative binding** as a distinct capability. AssoMem translates classic pattern-completion logic into multi-session personal-agent tasks: evidence sessions encode ≥2 latent facts that never state the conclusion; the query is a decision cue that does not lexically restate those facts; success requires co-activating the bound pattern and producing a novel, unstated recommendation (or abstaining when evidence is absent). We release a DATA_STANDARD-aligned pilot spanning three mundane-to-professional domains—health/diet, work/learning, and hobby/habit—with 10 personas, 450 items, and three arms per scenario (associative, surface-distractor, absence), plus validity gates that enforce cue–evidence disconnect and flat-retrieval miss. Parallel systems that improve associative *retrieval graphs* (e.g., AssoMem-style multi-signal retrieval; Zhang et al., 2025) or time/location-aware Memory-QA (Wang et al., 2025) remain valuable, but without a construct-specific testbed, gains cannot be attributed to binding rather than stronger retrieval or reasoning. `[EXP: Across X agents—including long-context LLMs, RAG, and external-memory systems—accuracy under high-interference associative conditions remains below Y% of human / ceiling performance even with oracle target-memory injection, revealing a last-mile binding bottleneck that existing memory scores do not expose.]`

We predict that as agents move toward long-horizon personal deployments, performance will be governed less by retrieval capacity—already saturating on several long-context memory suites—and more by **associative binding**: completing degraded patterns and reinstating latent user constraints across sessions when queries do not restating the triggering experience (cf. Hu et al., 2026a; Zhang et al., 2025). AssoMem provides an instrument to test that prediction. Our contributions are threefold:

1. **Construct.** We formalize associative binding for LLM agents by adapting pattern-completion paradigms into multi-session tasks with controlled cue–target disconnect, typed co-activation of ≥2 evidence facts, novel unstated conclusions, and matched distractor/absence arms.
2. **Benchmark.** We release AssoMem with 450 curated items across 3 domains and 10 personas, a reproducible validity pipeline (lexical/TF-IDF disconnect, flat top-3 miss, distractor≥evidence), and loaders that strip annotation leakage from model-visible context.
3. **Mechanism.** We specify an oracle/ablation suite—current-turn, full history, BM25/dense/hybrid RAG, agent memory systems, oracle target memory, oracle association path, shuffled edges, removed target, and matched direct-cue variants—that isolates retrieval, path discovery, path utilization, and binding quality, enabling an associative difficulty gap between direct-cue and associative conditions (detailed in Experiments).

---

## 2. Table 1 — Landscape (Intro-facing sketch)

| Benchmark | Setting | Retention / QA | Cue–target disconnect | Action / multi-session | Interference distractor arm | Absence / abstain | Pattern completion / multi-element binding |
|-----------|---------|----------------|----------------------|------------------------|-----------------------------|-------------------|---------------------------------------------|
| LoCoMo | Long conversation | ✓ | △ | ✗ | △ | △ | ✗ |
| LoCoMo-Plus | Long conversation | ✓ | ✓ (cognitive constraints) | ✗ | △ | △ | ✗ (constraint apply ≠ multi-element completion) |
| LongMemEval / related | Long context | ✓ | △ | ✗ | △ | △ | ✗ |
| MemoryAgentBench | Agent memory skills | ✓ | △ | △ | △ (conflict) | △ | ✗ |
| MemoryArena | Memory–Agent–Env loop | △ | △ | ✓ | △ | △ | ✗ |
| STATE-Bench | Enterprise procedures | △ | △ | ✓ | △ | △ | ✗ |
| **AssoMem (ours)** | Personal multi-session | ✓ | ✓ (V1 gated) | ✓ (decision cue) | ✓ (V2 arm) | ✓ (A5 arm) | ✓ (A3 co-activation → unstated C) |

✓ = first-class; △ = partial / not construct-controlled; ✗ = not operationalized.

---

## 3. Sentence-level map (feedback → draft)

| Feedback node | Where it lives | Causal job |
|---------------|----------------|------------|
| STATE-Bench / MemoryArena failure | ¶1 | Hook: pipe ≠ performance; associative failure |
| Retrieval vs pattern completion + DAM/Hopfield | ¶2 | Mechanism diagnosis |
| Two divisions of benchmarks + shared IR paradigm | ¶3 | Field gap |
| Biology as construct validity / toolbox | ¶4 | Separability + measurement (not motivation) |
| AssoMem definition + `[EXP]` finding | ¶5 | Proposal + preview |
| Prediction + 3 contributions; ablations deferred | ¶6 | Falsifiable claim + audit scope |

**Moved / deleted from your prior draft (as requested):**
- Deleted consensus boilerplate (“toward fully autonomous agents…”).
- Moved “few are biology-driven” out of the problem statement into ¶4.
- Replaced consequence waffle (“unable to flexibly source…”) with mechanistic diagnosis (partial cue, similarity-brittle retrieval, missing binding dynamics).
- Kept “queries do not lexically restate…” as the spine of ¶2–¶5.
- Ablation table kept as **contribution preview only**; full condition×isolate design belongs in Experiments.

---

## 4. Key references (Intro)

- Bean et al. (2025). *Measuring what Matters: Construct Validity in Large Language Model Benchmarks.* NeurIPS D&B.  
- Hoover et al. (2024). *Dense Associative Memory Through the Lens of Random Features.* NeurIPS.  
- Horner & Burgess (2013). *The associative structure of memory for multi-element events.* JEP:General.  
- Horner & Burgess (2014). *Pattern completion in multielement event engrams.* Current Biology.  
- Horner et al. (2015). *Evidence for holistic episodic recollection via hippocampal pattern completion.* Nature Communications.  
- Hu et al. (2025). *MemoryAgentBench.* arXiv:2507.05257.  
- Hu et al. (2026). *MemoryArena.* arXiv:2602.16313.  
- Lee et al. (2026). *LoCoMo-Plus.* ACL / arXiv:2602.10715.  
- Maharana et al. (2024). *LoCoMo.* arXiv:2402.17753.  
- Microsoft (2026). *STATE-Bench* (Open Source Blog / benchmark release).  
- Zhang et al. (2025). *AssoMem* (associative retrieval system; distinct from this benchmark). arXiv:2510.10397.  

*(Add Krotov & Hopfield 2016; surveys arXiv:2603.07670 / 2512.13564 in camera-ready bibliography as needed.)*

---

## 5. Next fill-ins before submission

1. Replace `[EXP: …]` with real numbers from the oracle / matched direct-cue / shuffled-edge suite.  
2. Promote Table 1 into LaTeX with citation cells.  
3. Add a 1-panel figure: *partial cue → failed nearest-neighbor → successful attractor completion* (Intro Figure 1).  
4. Decide naming collision with Zhang et al. 2025 “AssoMem” (retrieval paper)—e.g., **AssoMemBench** in the camera-ready title if needed.

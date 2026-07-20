# METRICS — the associative-memory evaluation suite

> One causal ladder, not a flat list. The three condition-based metrics (REA, Δ_mem,
> Δ_assoc) form the spine — "can answer → needs memory → needs association" — where each
> layer removes one confound before the next is claimed. JER reads the *mechanism* under
> the spine; DIR/AbC/SAA are three orthogonal controls the ladder cannot see.
>
> Δ_mem and Δ_assoc are **not separately measured** — they are arithmetic differences of
> REA across conditions. Report per-condition REA as primary; the Δ's are derived columns.

---

## The metrics table

| Metric | One-line definition | Goal — what it tests | How to compute |
|---|---|---|---|
| **REA** — Required-Element Accuracy | Fraction of items where **every** required element of the gold is satisfied (AND, not soft-average). | **L1 — task success.** Can the model reach the gold conclusion that needs *both* evidences, with full history? | Per item: `rea = ∏_i 1[judge(elem_i)=YES]` ∈ {0,1}. Dataset: `REA = mean_x rea(x)`. Run under each condition (FULL / no-target / broken-link) → REA_full, REA_noTgt, REA_brokenLink. |
| **Δ_mem** — Memory necessity | Drop in REA when the target evidence sessions are deleted. | **L2 — does the answer depend on stored memory, or on priors/shortcuts?** | `Δ_mem = REA_full − REA_noTgt` (derived). Paired bootstrap over items → 95% CI. Item validity requires `REA_noTgt ≈ chance`. |
| **Δ_assoc** — Association necessity ★ | Drop in REA when both evidences stay present but are made **un-bindable** (persona-split). | **L3 (the crux) — does the model need to *bind* the two facts, or just have both in context?** Separates association from single-hop co-presence. | `Δ_assoc = REA_full − REA_brokenLink` (derived). Paired bootstrap → CI. Significant iff CI excludes 0. This is the benchmark's load-bearing number. |
| **JER** — Joint Evidence Recall (+ h_k) | Did the reasoning actually cite/use **both** anchor evidences (not just land on the right answer)? | **Mechanism under L1.** Catches "right answer, no real binding" — REA can be right for the wrong reason. | `jer = ∏_{j=1}^{p} 1[cite(e_j)]` ∈ {0,1}, p≥2. `JER = mean over items`. Also report **h_k histogram**: `h_k = |{x: Σ_j cite = k}| / N` (h0 = retrieval miss, h1 = single-hop, h2 = both bound) → diagnoses *how* it failed. |
| **DIR** / **FoolRate** — Distractor invariance | Does a hammer distractor (similar but irrelevant memory) flip a previously-correct answer? | **Robustness / false-association** — the opposite failure the ladder can't see (grabbing the wrong memory). | Condition on base-correct: `DIR(g) = 1[REA(a_g)=REA(d_g) ∧ JER(a_g)=JER(d_g)]` over items where REA(a_g)=1; `DIR = mean_g`. `FoolRate = mean_g 1[check3_distractor_reliance = FAIL]`. |
| **AbC** — Abstention Correctness (T5) | On absence items (evidence genuinely missing), does the model **abstain** instead of hallucinating an association? | **Negative control** — separates true association from confident guessing. | `AbC = mean over T5 items 1[abstains ∧ ¬asserts absent causal pattern]`. Paired `add-evidence` twin must flip abstain → answerable (report `flip_rate`). |
| **SAA** — Source Attribution Accuracy (T6) | Same fact attributed to the **user** vs a **friend** must yield different golds — does the model track who said it? | **Source memory** — a failure invisible to every ablation arm. | Run FULL vs **source-swap** arm; `SAA = mean over T6 items 1[answer matches source-correct gold in both attributions]`. |

★ = the metric that makes this an *associative*-memory benchmark rather than a multi-hop QA benchmark.

---

## How the three conditions produce the ladder (main table A)

Rows = the 3 systems (base LLMs under full-history long-context: GPT-oss-20b, Gemma-4-31b,
Qwen-3.6-35b). Columns = per-condition REA; last two columns derived. Every cell `REA [95% CI]`.

| Model | FULL | no-target | broken-link | Δ_mem = FULL−noTgt | Δ_assoc = FULL−brokenLink |
|---|---|---|---|---|---|
| GPT-oss-20b | .72 [.60,.83] | .31 [.20,.43] | .43 [.31,.55] | .41 [.28,.53] ✓ | .29 [.16,.42] ✓ |
| Gemma-4-31b | .68 [.55,.79] | .34 [.22,.46] | .47 [.35,.59] | .34 [.21,.47] ✓ | .21 [.09,.34] ✓ |
| Qwen-3.6-35b | .76 [.64,.86] | .29 [.18,.41] | .51 [.39,.63] | .47 [.34,.59] ✓ | .25 [.12,.38] ✓ |

*(illustrative; ✓ = paired-bootstrap CI excludes 0.)* Read one row left→right: FULL high →
drops to chance at no-target (answer is memory-driven, L2) → still drops at broken-link even
though both facts remain (answer is binding-driven, L3). Three drops present = the item truly
tests associative memory.

## Mechanism + controls (table B — single-condition, NOT differences)

| Model | JER (FULL) | DIR / FoolRate | AbC (T5) | SAA (T6) |
|---|---|---|---|---|
| GPT-oss-20b | .55 | .81 / .19 | .68 | .60 |
| … | | | | |

`—— benchmark validity: discrimination spread · human ceiling · judge κ ——`

---

## Conditions (arms) each item ships

| Arm | Operation | Feeds |
|---|---|---|
| **FULL** | original history | REA_full, JER, DIR base |
| **no-target** | delete ev_A + ev_B sessions | REA_noTgt → Δ_mem |
| **broken-link** | keep both evidences, **persona-split**: reassign ev_A and ev_B to two different personas (surface tokens unchanged, only ownership changes → un-bindable) | REA_brokenLink → Δ_assoc |
| **no-distractor** | delete hammer distractor | DIR |
| **source-swap** (T6) | re-attribute an evidence to a friend | SAA |
| **add-evidence** (T5) | insert the real evidence into an absence item | AbC flip_rate |
| **restore** | re-add removed sessions | reversibility check: REA should return to REA_full's CI band |

## Reporting rules
- **Primary = per-condition REA with 95% bootstrap CI** (Wilson acceptable for the proportion).
- **Δ's = paired bootstrap over items**; "significant" = CI excludes 0 (this is the evidence
  for L2/L3, cleaner than a p-value). Do not report SD± as the headline for a proportion —
  show the item-level h_k histogram for spread instead.
- **Benchmark-validity row** (tests the *ruler*, not the model): discrimination spread
  (top−bottom REA; too tight ⇒ items don't separate systems), human ceiling, judge κ (2
  independent judge LLMs scored against gold + required_elements — κ, not circular peer-grading).

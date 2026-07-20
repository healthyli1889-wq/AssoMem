# AMB Sample Evaluation Instrument (SOTA, executable)

> Purpose: given ONE benchmark sample JSON, produce a reproducible 0–100 validity score
> + a ship verdict. The instrument is **solver-based**, not vibe-based: a sample is valid
> only if a battery of cheap "shortcut solvers" all FAIL and an oracle solver SUCCEEDS.
> Applies to positive (associative) and negative (absence/control) samples alike.

Model roles used below (any capable LLM, temp 0):
- **Solver** = the model-under-test stand-in, used to probe the sample.
- **Judge** = closed-rubric scorer (J1 grounded / J2 faithful / J3 relation), meta-validated.
- **Embedder** = a REAL sentence embedder (e.g. a modern text-embedding model), **never a
  tf-idf proxy** — the current samples' `tfidf-local-proxy` with all-0.0 cosines is invalid.

---

## Tier 0 — Red-line gates (binary; any FAIL ⇒ REJECT, score capped at 50)

| G | Gate | Executable check | FAIL if |
|---|---|---|---|
| **G1 Gold correctness & coherence** | oracle solver on evidence-only reaches gold; every entity in gold appears in context | run `P_oracle` (query + gold evidence sessions); string-check gold's named entities ⊆ context | oracle ≠ gold, OR gold cites anything absent from context (phantom evidence) |
| **G2 No leakage** | strip `annotation, evidence_id, role_setup, evolving_state, latent_forbidden_phrases`; confirm none appears in model-visible input; confirm no visible field alone yields the answer | diff serialized input vs raw JSON; run `P_prior_plus_persona` (query+options+persona only) | any latent/answer token visible, OR persona-only solver reaches gold |
| **G3 Associative necessity** (positive samples) | removing either evidence node breaks the answer | run `P_LOO_A` and `P_LOO_B` (full minus ev_A / minus ev_B) | either leave-one-out still yields gold (⇒ single-hop) |
| **G3′ Absence pairing** (negative/abstain samples) | the paired *evidence-added* twin exists as a concrete runnable sample and flips to answerable | load the `evidence_added` variant; run `P_oracle` on it | pairing is only asserted (no concrete added sessions + gold) |
| **G4 Not prior-solvable** | world-knowledge/priors alone cannot pick gold | run `P_prior` (query+options ONLY, no conversation) | prior solver reaches gold (⇒ tests priors, not memory — the cherry-blossom failure) |

---

## Tier 1 — Graded dimensions (weighted, 100 pts)

### 1. Associative necessity & sufficiency — 25 pts  ★CORE
- **1a Sufficiency (10):** `P_oracle` (evidence-only) reaches gold cleanly. Full = 10; needs unstated assumption (e.g. AMB_HH's unstated "Sunday") = partial.
- **1b Necessity (15):** both `P_LOO_A`, `P_LOO_B` flip to abstain/wrong. Score = 15 × (fraction of evidence nodes whose removal breaks the answer). A convergent/additive item where one node alone suffices scores low.

### 2. Shortcut-resistance battery — 25 pts  ★CORE
Run each cheap solver; each MUST fail. Award pts for each that fails:
| Solver | Input | Must | pts |
|---|---|---|---|
| `P_flatrag` | top-3 sessions by Embedder(query) | miss ≥1 evidence node → fail | 6 |
| `P_singlehop` | query + each single session (best-of) | none yields gold | 6 |
| `P_recency` | query + last 2 sessions | fail | 4 |
| `P_lexical` | Embedder cos(query, each evidence) | all < 0.15 (REAL embedder) | 5 |
| `P_sourceconf` | treat others'/assistant statements as user's | not yield gold | 4 |

### 3. Distractor hardness — 15 pts
- **INVERSION** = max cos(query, distractor) − max cos(query, evidence) > 0.20, REAL embedder (6).
- ≥1 **plausible-answer** distractor = the option a shortcut/prior would pick (5).
- ≥1 **source-confusion** distractor (someone else's statement as if the user's) (4).
- Auto-zero if `distractor_ids` empty while surface lures exist (registration inconsistency).

### 4. Grounding & coherence (whole-person) — 15 pts
- **Persona coherence (5):** facets plausibly co-occur in one real person; **no persona↔scenario mismatch** (AMB_HD's consultant-vs-campus = deduct).
- **Fact reality / provenance (6):** each evidence entity resolves to a real source (D9); `provenance` complete.
- **Gold↔required_elements consistency (4):** gold contains exactly the required elements, no extras.

### 5. Source-memory structure — 8 pts
- Others'/assistant statements present and correctly NOT to be adopted as the user's (4).
- A **source-attribution probe** or **source-swap control** variant exists (4).

### 6. Ablation / workability affordances — 7 pts
- Every removable element has a stable ID and is independently removable (2).
- **Concrete** counterfactual variants with **declared expected outcomes** (leave-one-out→abstain; add-evidence→answerable; shuffle→C1 drop) (3).
- `associative_lift = Acc(FULL) − Acc(ABLATE)` is computable from shipped fields (2).

### 7. Format & leakage hygiene — 5 pts
- Relations ∈ closed 6-set {co_occurs, causes, constrains, updates, analogous_to, suppresses} (2) — `indicates`/`co_activate_to` = fail.
- `association_type` matches the actual mechanism; control arms tagged separately from constructs C1/C2/C3 (1).
- `validity_metrics` computed with REAL embedder, non-zero, method disclosed (2).

---

## Tier 2 — Meta (must pass to ship; reported separately)
- **Human answerability / IAA:** ≥3 annotators, blind-before-gold, reach gold; Cohen's/Fleiss' κ ≥ 0.6.
- **Judge validity:** the scoring judge passes JUDGE_VALIDITY ≥ 0.90 on its calibration set.

---

## Aggregation & verdict
```
if any Tier-0 gate FAILS:        verdict = REJECT (score = min(50, Σ))
else score = Σ Tier-1 (0–100)
verdict:  ≥97 SHIP-AS-GOLD · 90–96 MINOR-REVISE · 75–89 MAJOR-REVISE · <75 REJECT
Tier-2 (κ, judge) required before any SHIP.
```

## Scorecard output schema
```json
{
  "sample_id": "...",
  "tier0_gates": {"G1":"pass|fail", "G2":..., "G3":..., "G4":...},
  "tier1": {"assoc_necessity": {"score":0,"of":25,"notes":""}, "...": {}},
  "tier1_total": 0,
  "tier2": {"iaa_kappa": null, "judge_validity": null},
  "verdict": "REJECT|MAJOR_REVISE|MINOR_REVISE|SHIP",
  "blocking_fixes": ["..."]
}
```

---

## Worked application — `AMB_HD_u01_absence_S2` (absence/abstain sample)

**Tier 0 gates**
- **G1 Gold coherence** — PASS. Gold ("insufficient evidence… ask about past late-caffeine nights") is coherent; no phantom entity (unlike AMB_HH's prix-fixe).
- **G2 No leakage** — ⚠ BORDERLINE-PASS. Answer trait `stimulant_cutoff: post_14h_fragile` is in `evolving_state` (stripped ✓). But `stable_traits` ("data-driven health tracker, Oura Ring") stay visible; a solver could argue "you're caffeine-sensitive → no," which is arguably *correct*, threatening the abstain gold. Flag, not hard-fail.
- **G3′ Absence pairing** — **FAIL.** `counterfactual_variants` only asserts "evidence_added → answerable" with **no concrete added sessions and no added-gold**. An absence control without its instantiated positive twin has no teeth. → **Tier-0 FAIL ⇒ REJECT, cap 50.**
- **G4 Not prior-solvable** — PARTIAL. A prior solver would say "no, caffeine before sleep is bad" — a *substantive* answer, not "abstain," so it doesn't reproduce gold exactly; but the gold/​prior boundary (abstain vs. "no") is fragile.

**Tier 1 (graded, informational since Tier-0 failed)**
| Dim | Score | Note |
|---|---|---|
| 1 Necessity/sufficiency (absence variant) | 13/25 | valid absence concept; twin not instantiated |
| 2 Shortcut battery | 13/25 | surface lures present but **unverified** (tfidf 0.0); source-conf lure good |
| 3 Distractor hardness | 6/15 | INVERSION not verified; no registered plausible-answer distractor |
| 4 Grounding/coherence | 9/15 | gold coherent (+); **persona↔scenario mismatch** (coatings consultant vs "campus/study room/8am session/slides") (−) |
| 5 Source-memory | 4/8 | "friends say" source-trap present; no explicit attribution probe |
| 6 Ablation/workability | 3/7 | IDs ok; counterfactual vague, no declared outcomes |
| 7 Format/hygiene | 3/5 | empties consistent; **fake validity_metrics**; `A5` in `association_type` (control≠construct); `distractor_ids` empty vs lures |
| **Tier-1 total** | **51/100** | |

**Verdict: REJECT (Tier-0 G3′ fail; capped 50). Tier-1≈51 confirms major-revise even absent the gate.**

**Blocking fixes (ranked):**
1. Instantiate the positive twin (concrete `evidence_added` sessions + its own gold) — an absence control ships only as a PAIR. [G3′]
2. Verify shortcut-resistance with a REAL embedder; prove surface-lure cosine is HIGH (tempting) while evidence is genuinely absent. [Dim 2, format]
3. Close the persona channel: ensure no visible field lets a solver derive the answer, or the abstain gold is contestable. [G2]
4. Fix persona↔scenario coherence (professional context, not campus/student). [Dim 4]
5. Register lures as distractors / add a plausible-answer distractor; move `A5` to a `control_arm` field. [Dim 3, 7]

> Note: this instrument scores AMB_HD **lower (~51, REJECT) than an eyeball pass (~68)** — deliberately. The gap is the value: it refuses to credit *asserted* validity (pairing, low-overlap, distractor pull) that isn't *verified by a solver*.

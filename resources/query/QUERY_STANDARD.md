# Query Standard — writing gold queries that truly test associative memory  (v2, final)

> Scope: the PROBE QUESTION (final-turn query + its gold + MCQ options + the arms it ships).
> Distinct from the sample standard (GENERATION_CRITERIA.md). Use this to author every
> gold query in the 3k set. The governing test in §0 is executable — never ship a query you
> have not run through it. §8 is the clean record schema every query must serialize to.
>
> **What changed in v2:** the Answer Table is now wired to the eval **arms + metrics**
> (§0.1); the MCQ standard defaults to the **2×2 single-hop** design (§4); each query
> declares the **arms** it ships so REA / Δ_mem / Δ_assoc / JER / DIR / AbC / SAA are all
> computable from it (§8); scenario emphasis follows QUERY_SCENARIO_PROFILES (§6).

---

## 0. The one definition that governs everything — the Associative Answer Table

A query tests associative memory **iff its answer equals the gold ONLY when both evidences
are present** — not from priors, not from either evidence alone. Author every query to
satisfy this 4-row table (run a temp-0 solver in each condition):

| Condition given to solver | Expected answer | If it yields gold → |
|---|---|---|
| **∅ (query + options only, no conversation)** | **NOT gold** (a trap answer) | query is **prior-solvable** → reject |
| **ev_A only** | **NOT gold** | query is **single-hop on A** → reject |
| **ev_B only** | **NOT gold** | query is **single-hop on B** → reject |
| **ev_A ∧ ev_B (in full context)** | **GOLD** | ✅ valid associative query |

- This IS the definition of "the naive answer is a trap and the truth needs binding."
- For **absence/abstain** (T5) queries the table inverts: shipped condition has **no**
  evidence → gold = *abstain*; ∅/prior must **not** produce a confident substantive answer;
  the paired *add-evidence* twin must move "both" → answerable.
- For **source** (T6) queries: the same fact attributed to the USER vs. a FRIEND must yield
  **different** golds; a model without source memory gives the same answer to both.

**If a query passes this table, it is associative. Everything below makes it hard, clean,
diagnostic, and measurable.**

### 0.1 How the Answer Table becomes the eval arms & metrics (read once — it's the spine)

The authoring-time table rows correspond to the runtime **arms** in METRICS.md. Design the
query so these hold, and every metric is computable from the one item:

| Answer-Table row | Runtime arm | Feeds metric | Passing signal |
|---|---|---|---|
| ev_A ∧ ev_B (shipped) | **FULL** | **REA** (∏ required_elements) + **JER** (cited both) | REA high, JER high |
| ev_A / ev_B only | **no-target** (delete both ev sessions) | **Δ_mem** = REA_full − REA_noTgt | REA_noTgt ≈ chance |
| both present but **un-bindable** | **broken-link** (persona-split: ev_A→personX, ev_B→personY, surface tokens unchanged) | **Δ_assoc** = REA_full − REA_brokenLink ★ | drop present, CI excludes 0 |
| hammer distractor present | **no-distractor** | **DIR / FoolRate** | REA rises when distractor removed |
| (T5) evidence absent | **add-evidence** twin | **AbC** flip_rate | abstain → answerable |
| (T6) fact re-attributed | **source-swap** | **SAA** | gold changes with source |

★ **Δ_assoc is the load-bearing number** — it is the ONLY arm that separates "needs to bind
two facts" from "needs both facts nearby". A query that survives no-target but NOT
broken-link is real associative; one that survives broken-link too is only multi-fact
retrieval → weak. Author toward a large Δ_assoc.

---

## 1. Query types (MECE) — pick one per query, tag it

| Type | Construct | The query asks… | Gold is… | Primary metric |
|---|---|---|---|---|
| **T1 Decision** | C2 constraint | "Should I do X?" where X collides/aligns with bound facts | do / don't, forced by the two facts | REA, Δ_assoc |
| **T2 Preference-inference** | C3 analogical | "Which of these would I most like / go for?" | the option implied by binding two tastes/patterns | REA, Δ_assoc |
| **T3 Prediction** | C1 temporal | "What's likely if I do X now?" | outcome implied by a bound recurring pattern | REA, Δ_assoc |
| **T4 Transfer** | C3 analogical | "How should I approach [new situation]?" | apply a method the user uses elsewhere | REA, Δ_assoc |
| **T5 Absence (control)** | — | a T1–T4 question whose supporting evidence is ABSENT | abstain / "insufficient — ask X" | **AbC** |
| **T6 Source-attribution (probe)** | — | "Was X my call or someone else's?" / decision hinging on who said it | depends on the true source | **SAA** |

Every 50-query profile set MUST include T5 and T6 (they catch failures the ladder can't see).

---

## 2. RED-LINE criteria (violate any ⇒ rewrite the query)

- **Q1 Passes the Answer Table** (§0). The single non-negotiable.
- **Q2 Person-specific.** The gold must depend on THIS user's idiosyncratic facts, not
  general good advice. *Test:* would the gold be the same for a random person? If yes → reject.
- **Q3 Low surface overlap.** The query must NOT echo the evidence's words. *Test:* embedder
  cos(query, each evidence) < 0.15; no shared content nouns. The query introduces a **new
  situation** the evidence bears on — it never restates the evidence.
- **Q4 Decidable gold.** A human given both evidences agrees on one answer (or "abstain").
  No two defensible golds. *Test:* 3 humans, same answer (κ≥0.6).
- **Q5 Natural utterance.** Reads as a real thing the user would say in the final turn —
  never "Based on sessions 3 and 5, …". No meta-references to the data.
- **Q6 Each evidence load-bearing & bindable.** ev_A-only and ev_B-only both ≠ gold, AND the
  two evidences must contribute DISTINCT necessary pieces that only *combine* to force the
  gold (this is what makes broken-link/Δ_assoc bite). Same point stated twice → reject.
- **Q7 Not medically/factually single-hop-sufficient.** A restriction, rule, or fact that
  alone decides the answer fails Q1 (single-hop). Phrase such facts generically so the
  binding partner is still required (see the S11 fix in health_queries).

---

## 3. Construction recipe (author one query in 6 steps)

```
1. PICK a coherent person (one profile) + a type T1–T6.
2. CHOOSE two evidence facts of that person that INTERACT (constraint / analogy / pattern),
   each contributing a DIFFERENT necessary piece (Q6).
3. INVENT a NEW situation/decision (the query) that neither fact mentions but both bear on
   -> low overlap by construction (Q3).
4. WRITE the gold = the answer forced only by binding both; fill required_elements
   (each becomes one AND-conjunct judged YES/NO -> REA).
5. BUILD the 2x2 options (§4): gold / prior-surface / single-hop-A / single-hop-B.
   PLANT one hammer distractor session (interference -> DIR).
6. RUN the Answer Table (§0) with a solver in all four conditions. If any row misbehaves,
   fix the weakest evidence or the query framing and repeat. Ship only on a clean table.
```

---

## 4. MCQ option-design standard — DEFAULT is the 2×2 single-hop

Ship 4 options built as a **2×2 over the two evidences** — `[uses ev_A] × [uses ev_B]`. The
wrong option a model picks tells you EXACTLY which memory failure it has:

| Option | features (ev_A, ev_B) | Role | A model that picks it… |
|---|---|---|---|
| **(A) GOLD** | ✅ ✅ | needs ev_A ∧ ev_B | has associative memory ✅ |
| **(B) PRIOR / SURFACE** | ❌ ❌ | world-knowledge / surface default | guesses from priors; must be the *tempting* pick |
| **(C) SINGLE-HOP A** | ✅ ❌ | uses only ev_A | grabbed one fact, failed to bind |
| **(D) SINGLE-HOP B** | ❌ ✅ | uses only ev_B | grabbed the other fact, failed to bind |

Why this beats the old source/unsupported set: **C and D are the two single-hops**, so a wrong
pick pinpoints *which* evidence was used alone — the sharpest possible diagnosis of
"no binding". This mirrors the Answer Table 1:1.

**Variants (swap in only when the type calls for it):**
- **T6 source items:** replace **C or D** with a **SOURCE-CONFUSION** option (what you'd pick
  if a friend's statement were treated as the user's) — that's the failure T6 targets.
- **Hallucination-sensitive items:** make **D** an **UNSUPPORTED** option (plausible, never
  stated) to also probe fabrication.

**Rules:** options equal length/specificity (no giveaway); exactly one correct; (B) is the
tempting default; **randomize order at serve time** (store the mapping); always also keep an
**open-ended gold** (`gold_open`) for the harder free-text arm and for REA/JER scoring.

---

## 5. Per-query quality scorecard (grade each query, 0–100)

| Dim | pts | Check |
|---|---|---|
| Answer-Table clean (§0) | 40 | ∅ / A-only / B-only all ≠ gold; both = gold (★ hard gate: <40 ⇒ reject) |
| Association-necessity (Δ_assoc) | 10 | under persona-split (broken-link) the gold should NOT be reachable |
| Person-specificity (Q2) | 12 | gold changes if persona changes |
| Low overlap (Q3) | 8 | cos<0.15, no shared content nouns |
| Decidable gold + IAA (Q4) | 8 | 3 humans agree (κ≥0.6) |
| 2×2 option quality (§4) | 10 | A/B/C/D fill the 2×2; C,D are true single-hops; (B) tempting |
| Naturalness (Q5) | 4 | reads as a real final turn |
| Difficulty controls logged | 8 | temporal gap, interference strength, hop type recorded |
Ship a query at ≥90; the 40-pt Answer-Table dim is a hard gate.

---

## 6. The set blueprint (per profile × N profiles, balanced)

- **Unit = (profile, query).** Each query binds 2 evidences **within its own profile**
  (whole-person: never stitch evidence across profiles).
- **Per profile: 5 queries**, each a DIFFERENT evidence pair (no reuse).
- **Type mix** (per 50-query block, so the set yields interpretable Δ_assoc):
  | T1 Decision (C2) | T2/T4 (C3) | T3 Prediction (C1) | T5 Absence | T6 Source |
  |---|---|---|---|---|
  | 14 | 14 | 10 | 6 | 6 |
- **Scenario emphasis** (from QUERY_SCENARIO_PROFILES — keep the CORE standard invariant,
  only shift the mix): Health → over-weight **T5 + update**; Social → **T6**; Finance →
  **T3**; Hobby → **T2/T4 MCQ**; Work → **T1/T4**.
- **Difficulty spread:** vary temporal gap (evidence 2 vs 20 sessions apart) and interference
  (weak vs hammer distractor) across the set; log per query so results slice by difficulty.
- **Split:** by PROFILE for any train/dev/test use; ablation is within-item on test.
- Each query ships its **arms** (§0.1 / §8 / WORKABILITY 6-row) so all metrics are computable.

---

## 7. Worked examples (the canonical clean references)

### ✅ CANONICAL — T2 Preference-inference (C3), full 2×2  ← the bonsai item
Profile: apartment-with-balcony person who loves slow/patient work and dislikes fast,
high-intensity activity, looking for a new hobby. (Rendered sample: `samples/AMB_HB_u01_preference_S1.json`.)
- **ev_A** (session 2): *"The part of cooking I love is the low-and-slow stuff — braises, proofing, things that reward patience. Fast high-heat cooking just stresses me out."*  → taste = slow/patient, anti-fast.
- **ev_B** (session 6): *"I keep thinking I want a hands-on hobby I can do out on my balcony."*  → constraint = balcony + hands-on.
- **Query** (session 8): *"There's a beginners' weekend workshop fair near me — which one should I go for?"*
  - (A) a bonsai-growing starter workshop — **✅slow ✅balcony → GOLD**
  - (B) a wok stir-fry cooking class — ❌fast ❌kitchen → prior/surface ("you like cooking")
  - (C) a sourdough & slow-fermentation baking class — ✅slow ❌kitchen → single-hop A
  - (D) a fast-turnover balcony microgreens class (harvest & replant every few days) — ❌fast ✅balcony → single-hop B
- **Gold:** (A) bonsai — the only option that is both the patient/slow work you enjoy AND a
  hands-on balcony hobby.
- **Answer Table:** ∅→spreads/B (bonsai isn't a prior default) ✓ · ev_A-only→A or C ambiguous ✓
  · ev_B-only→A or D ambiguous ✓ · both→**A** ✓.  Clean.

### ✅ T1 Decision (C2) — the health pattern (see health_queries S1–S20)
- **ev_A:** "a strong evening energy drink kills my appetite the next morning."
- **ev_B:** "skipping breakfast before a briefing makes me lose words and misread figures."
- **Query:** "The team's handing out strong energy drinks for tonight's deck push before my
  8 a.m. briefing — grab one?"  **Gold: No** (drink suppresses tomorrow's appetite → skipped
  breakfast → botched briefing). Table: ∅→"sure, power through"; A-only→"go easy on caffeine";
  B-only→"just eat breakfast"; both→**No**. ✓

### ❌ Bad — the cherry-blossom query (why it fails)
"Likes cherry blossoms + favorite food sushi → which do they most like? (incl. a Japan option)."
Answer Table: **∅ (prior only) → picks Japan = gold.** Fails row 1 → tests cultural priors,
not memory of THIS user. Reject. (Fix: make the gold hinge on an idiosyncratic personal fact
a prior can't supply.)

---

## 8. The clean query record schema (every one of the 3k queries serializes to this)

Keep this shape identical across the whole set — it is what makes 3k queries loadable,
scorable, and ablatable without special-casing. (Full context lives in the sample file; the
query record references it by `profile_id` + evidence ids.)

```json
{
  "query_id": "AMB_<domain>_<profile>_S<n>_<type>",
  "profile_id": "hobby_u01",
  "type": "T2",                       // T1..T6
  "construct": "C3_analogical",       // C1_temporal | C2_constraint | C3_analogical | —
  "scenario": "slow_taste_x_balcony_handson",
  "query": "…natural final-turn utterance…",
  "options": {                        // 2×2 MCQ; features = which evidence it uses
    "A": {"text": "…", "role": "gold",         "features": {"ev_A": true,  "ev_B": true}},
    "B": {"text": "…", "role": "prior_surface","features": {"ev_A": false, "ev_B": false}},
    "C": {"text": "…", "role": "single_hop_A", "features": {"ev_A": true,  "ev_B": false}},
    "D": {"text": "…", "role": "single_hop_B", "features": {"ev_A": false, "ev_B": true}}
  },
  "gold_choice": "A",
  "gold_open": "…free-text gold for the harder arm & REA/JER scoring…",
  "required_elements": ["…AND-conjunct 1…", "…AND-conjunct 2…"],   // -> REA
  "target_evidence_ids": ["ev_A", "ev_B"],                          // -> JER
  "answer_table": {"empty":"not_gold","ev_A_only":"not_gold","ev_B_only":"not_gold","both":"gold"},
  "arms": {                            // -> the metric each produces (see METRICS §0.1)
    "full": true,
    "no_target": {"remove_evidence_ids": ["ev_A","ev_B"]},         // Δ_mem
    "broken_link": {"persona_split": {"ev_A":"personX","ev_B":"personY"}}, // Δ_assoc
    "no_distractor": {"remove_session_ids": [4]},                  // DIR
    "add_evidence": null,              // set for T5 only
    "source_swap": null                // set for T6 only
  },
  "difficulty": {"temporal_gap_sessions": 4, "interference": "weak", "hop": 2},
  "validity_metrics": {"embed_cosine_query_evidence_max": null, "flat_rag_hit_top3": null,
                        "distractor_cosine_query": null, "inversion": null}
}
```

**Format contract (self-linter — run before adding any query to the 3k set):**
1. `answer_table` has exactly the 4 keys, and `both == gold`, the other three `!= gold`.
2. `options` has exactly A/B/C/D; roles = {gold, prior_surface, single_hop_A, single_hop_B}
   (or the T6/hallucination variant); the 2×2 `features` are all four distinct corners.
3. `required_elements` are independent AND-conjuncts (dropping either changes the gold).
4. `target_evidence_ids` length ≥ 2 and every id appears in the referenced sample context.
5. `arms.no_target` and `arms.broken_link` are present for every T1–T4 item;
   `add_evidence` set iff T5; `source_swap` set iff T6.
6. `validity_metrics` regenerated with the REAL embedder before ship: evidence cos < 0.15,
   `flat_rag_hit_top3 == false`, distractor cos high (lure tempting).
7. No meta-reference to sessions/data in `query` (Q5); cos(query, each ev) < 0.15 (Q3).
```
```

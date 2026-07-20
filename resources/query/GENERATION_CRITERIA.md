# AMB Generation Criteria — the checklist your generator MUST satisfy

> Use this as the generation prompt / self-check. Every sample you produce is scored by
> EVAL_RUBRIC.md; this doc tells you how to PASS it. Rule of thumb: **do not ASSERT
> validity — engineer it, then verify it with the named solver.** A field you can't
> back with a solver result does not count.
>
> A capable LLM plays three throwaway "shortcut solvers" during generation; the sample is
> only kept if they behave as specified. Embedder = a REAL sentence-embedding model
> (never tf-idf; never all-zero cosines).

---

## 0. The one sentence that governs everything
A valid sample is one where **the naive/prior answer is a trap, and the correct answer is
recoverable ONLY by binding ≥2 dispersed, low-overlap facts about THIS person.** If any
cheap solver can reach the gold without binding both facts, the sample is invalid.

---

## 1. RED-LINE rules (violate any ⇒ sample is thrown away, no partial credit)

- **R1 — Gold is correct and self-contained.** Every entity/claim in `gold_answer` must
  appear in the conversation. *Self-check:* string-search each noun in the gold against
  `context`. ❌ The old AMB_HH cited a "restaurant prix-fixe" that never appeared — auto-kill.
- **R2 — No leakage.** The model sees ONLY serialized `role+content`. `annotation`,
  `evidence_id`, `role_setup`, `evolving_state`, `latent_forbidden_phrases` are stripped.
  No *visible* field (incl. `stable_traits`) may alone imply the answer.
- **R3 — Associative necessity (positive samples).** Deleting EITHER evidence session must
  change the gold. *Self-check:* run `solver(query + context − ev_A)` and `− ev_B`; both
  must fail/flip. If one evidence alone still yields gold → it's single-hop → kill.
- **R3′ — Absence pairing (abstain samples).** Ship the concrete positive twin
  (`evidence_added` with real added sessions AND its own gold) in the same file. An abstain
  sample without an instantiated answerable twin is invalid.
- **R4 — Not prior-solvable.** `solver(query + options, NO conversation)` must NOT reach
  gold. If world knowledge alone picks it (cherry-blossom + sushi → Japan), kill it.

---

## 2. CORE quality (engineer these, then verify)

- **C1 — Two dispersed, low-overlap evidences.** ev_A and ev_B in **different sessions**,
  neither in the final 2 sessions. *Verify:* Embedder cos(query, each evidence) **< 0.15**;
  entity overlap 0. Put the real numbers in `validity_metrics`.
- **C2 — Each evidence strictly necessary (clean 2-hop, not additive).** Design so ev_A and
  ev_B each contribute a DISTINCT missing piece (e.g. ev_A = a fact is important/immovable;
  ev_B = it can only happen in the contested slot). Avoid "both point at the same thing"
  convergence, where one alone suffices.
- **C3 — Flat-RAG must miss.** *Verify:* top-3 sessions by Embedder(query) must NOT contain
  both evidences; set `flat_rag_hit_top3=false`.
- **C4 — A plausible-answer HAMMER distractor.** Include ≥1 in-context session that supports
  the WRONG answer (the option a shortcut/prior would pick), register it in `distractor_ids`.
  *Verify:* INVERSION = cos(query, distractor) − cos(query, evidence) **> 0.20**.
- **C5 — Source-memory trap.** ≥1 fact must come from someone ELSE (friend/neighbor/doctor/
  the assistant), which must NOT be adopted as the user's own. Mark `source_role` on it.

---

## 3. Grounding & coherence (whole-person)

- **G1 — One coherent person.** Facets must plausibly co-occur; the load-bearing facets must
  be USED in the reasoning, not decorative. ❌ AMB_HD's "coatings consultant" + "campus /
  study-room / 8am session / slide prep" is a professional-vs-student mismatch — fix the
  scenario to the persona (or vice-versa).
- **G2 — Real, traceable facts.** Prefer entities resolvable to a real source; fill
  `provenance` and, where used, an entity URL (enables the D9 "fact is real" check).
- **G3 — gold ⟺ required_elements.** `required_elements` lists exactly what the gold must
  contain; the gold contains those and nothing unsupported.

---

## 4. Format & hygiene (mechanical, but auto-deducted)

- **F1 — Typed relations ∈ closed 6-set:** `co_occurs, causes, constrains, updates,
  analogous_to, suppresses`. ❌ `indicates`, `co_activate_to` are illegal.
- **F2 — Label the mechanism honestly.** `association_type` must match what the reasoning
  actually does (constraint-binding = C2, temporal co-occurrence = C1, analogy = C3).
  Control conditions (absence, inhibitory) go in a separate `control_arm` field, NOT in
  `association_type`.
- **F3 — Real validity metrics.** `validity_metrics` computed by a real embedder, non-zero,
  method disclosed. No `tfidf-local-proxy` with 0.0 cosines.
- **F4 — Consistent distractor registration.** If a session is a lure, it appears in
  `distractor_ids` with a type; `distractor_ids: []` while lures exist is inconsistent.

---

## 5. WORKABILITY (so future ablation experiments run — see WORKABILITY.md)
Every sample ships the **concrete ablation variants** with **declared expected outcomes**
(the 5-row pairing table). Minimum required variants:
- `evidence_removed:ev_A` → expected gold flips/abstains
- `evidence_removed:ev_B` → expected gold flips/abstains
- `distractor_removed` → expected easier (same gold, higher solver accuracy)
- `temporal_shuffle` (if C1/temporal) → expected C1 accuracy drops
- (absence) `evidence_added` → expected becomes answerable

---

## 6. Generator self-check loop (run before emitting each sample)
```
1. build stripped input; run P_prior            → must FAIL   (R4)
2. run P_oracle (evidence only)                 → must PASS   (gold correct/sufficient)
3. run P_LOO_A, P_LOO_B                          → both must FLIP (R3)
4. run P_flatrag (top-3 by embedder)            → must MISS   (C3)
5. embed cos(query, ev) < 0.15 ; INVERSION>0.20 → compute, store (C1,C4)
6. string-check gold entities ⊆ context         → must PASS   (R1)
7. if any check fails → repair & retry (max K); else emit + attach scorecard
```
Emit the sample ONLY if steps 1–6 pass. Attach the resulting numbers in `validity_metrics`
and the variants in `counterfactual_variants`. This is exactly what EVAL_RUBRIC.md re-checks.

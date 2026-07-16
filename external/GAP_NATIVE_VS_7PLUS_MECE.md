# MECE gap: Native AMB pilot vs retained ≥7 external capabilities

**Question:** After keeping only external match cells ≥7/10, what still differs from the **native** AssoMem pilot we already generated (`assomem_pilot/items`, 30 rendered items)?

**Scope**
- Native = partner_generated AMB pilot (DATA_STANDARD v1), arms: associative / distractor / absence.
- External keep-set = DynamicMem{C01,C02,C06,C10} ∪ RHELM{C01,C06,C08,C09,C10}.
- MyPCBench excluded (0 cells ≥7).

Partition below is **MECE**: mutually exclusive categories, jointly exhaustive for “what differs.”

---

## Block A — Construct definition (what the item is testing)

| | Native AMB pilot | Retained external ≥7 |
|---|---|---|
| **Primary construct** | Associative Personal Memory: dissimilar cue → typed co-activation → **novel unstated conclusion C** | Profile recovery / temporal tracking / refuse-on-false (RHELM) or state reconstruction (DynamicMem) |
| **A3 latent bridge** | First-class (`A3_cross_domain`, hop≥2 `associative_links`) | **Absent from keep-set** (externals score ≤4 on C05) |
| **A2 cue chain** | Present (4 items) | Not retained as ≥7 cell; RHELM multi-hop is not gated as A2 |
| **Success criterion** | Gold needs citing ≥2 typed facts + conditional recommendation / abstain | Fill schema field, answer temporal fact, or refuse hallucination |

**Gap (A):** Externals you are allowed to keep **do not carry the A3 construct**. Native is the only place where “co-activate A∧B → C never stated” is the scored behavior.

---

## Block B — Validity controls (how we know it’s the right construct)

| Control | Native | Retained external ≥7 |
|---|---|---|
| **V1 discriminant** (`flat_rag_hit_top3=false`, low Jaccard/cosine) | Hard gate in `validity_gate.py`; items rewritten until pass | **Not in keep-set** (DynamicMem SC names keys; RHELM C03=6) |
| **V2 distractor** (`distractor_cosine ≥ evidence_cosine`, annotated `distractor_ids`) | 10/30 items, explicit `why_distractor` | **Not retained** (RHELM misleading=6; DynamicMem=2) |
| **V4 / A5 absence** | 10/30 items, gold abstains | **RHELM C08=8 kept** — hallucination/fabrication/absence QA |
| **Latent forbidden phrases** | `evolving_state` + `latent_forbidden_phrases` never in dialogue | DynamicMem has latent prefs in logs (C02=8) but no native-style forbidden list / annotation split |

**Gap (B):**  
- Native uniquely owns **V1 + V2 as measurable gates**.  
- External keep-set uniquely contributes a **larger A5-like refuse stratum (RHELM)** than native’s 10 hand items.  
- DynamicMem’s “implicit evidence” (C02) is kept, but without V1 it can still be answered by topical retrieval of the named habit key.

---

## Block C — Schema & agent-visible surface

| | Native | Retained external ≥7 |
|---|---|---|
| **Unit** | Multi-session chat `context[]` with `role`/`content` only | RHELM: sessions + emails + attachments; DynamicMem: API `app_log` JSON |
| **Annotation separation** | Hard rule: evidence/distractor meta only in top-level `annotation` | RHELM QA has `supporting_evidence` (good, C09=8); DynamicMem packs mix gold snapshot with tasks (schema readiness dropped) |
| **Query identity** | `query_source: final_turn` ≡ last user utterance | RHELM: separate analyst-style `question`; DynamicMem SC: schema cloze named by key |
| **Gold form** | Free-text + `required_elements` rubric | Structured field fill / short phrase / refuse |
| **Associative graph** | `associative_links` with `relation` + `hop` | Not retained as ≥7 (no gold typed path) |
| **Counterfactuals** | Materializable `variant_id` objects | DynamicMem checkpoints ≈ natural A4 variants; RHELM not packaged as CF variants |

**Gap (C):** Native is the **canonical loader contract**. RHELM is the only retained external that is **close enough to adapt** (C09=8). DynamicMem is retained for **content**, not for drop-in schema.

---

## Block D — Persona & world richness

| | Native | Retained external ≥7 |
|---|---|---|
| **Persona depth** | Light: few `stable_traits` + latent `evolving_state` (C01 native=5) | **DynamicMem C01=10**, **RHELM C01=8** — full year trajectories, multi-domain lives |
| **Domains covered** | Pilot: work/learning + hobby/habit only | DynamicMem: 6 life domains; RHELM: daily life + hetero docs |
| **Evidence ecology** | Short rendered dialogues (~0.4–0.8k tok/item) | DynamicMem ~2.2M tok/user; RHELM ~0.5–1M/persona |
| **Cross-app / hetero sources** | Chat-only | DynamicMem 16 apps; RHELM emails+attachments (**kept via C01/C10, not as AssoMem tasks**) |

**Gap (D):** Keep-set **wins on world/profile depth and length**. Native **loses on realism/scale of the memory store**, by design of a 30-item construct pilot.

---

## Block E — Temporal dynamics

| | Native | Retained external ≥7 |
|---|---|---|
| **A4 as primary arm** | Weak (C06=4); only CF stubs / secondary | **DynamicMem C06=10**, **RHELM C06=8** — first-class |
| **Belief supersession** | Not systematically sampled | DynamicMem typed deltas Add/Modify/Acquire/Shift; RHELM temporal + state-dependent attributes |
| **Evaluation axis** | Difficulty ≈ hop / distractor / absence | Difficulty ≈ history length / update vs retention |

**Gap (E):** If the paper needs a **temporal-update stratum**, the keep-set supplies it; native does not (yet). That is additive, not a replacement for A3.

---

## Block F — Experimental design matrix

| Axis | Native pilot | Retained external ≥7 |
|---|---|---|
| **Arms** | 3 balanced: associative / distractor / absence (10 each) | Unbalanced: profile+A4 (DynamicMem), A4+A5+schema (RHELM) |
| **Association types** | A3×16, A5×10, A2×4 | No guaranteed A3; A4/A5-like only |
| **Users** | 30 light personas | 10+10 deep personas |
| **Items** | 30 golden rendered | Thousands of tasks/logs (not construct-filtered) |
| **Gate** | Automated validity_gate before keep | Paper metrics ≠ your V1/V2/V4 gates |

**Gap (F):** Native = **construct-balanced micro-pilot**. Keep-set = **capability fragments** you may graft on — not a second balanced AssoMem corpus.

---

## Block G — What to do with the difference (decision table)

| Need | Prefer | Why |
|---|---|---|
| Prove A3 associative co-activation | **Native** | Only ≥7 on C03–C05 |
| Prove V1/V2 measurable validity | **Native** | Externals <7 on these |
| Prove A5 abstention at scale | **RHELM keep (C08)** + native template | RHELM has volume; native has schema |
| Prove A4 update/retention | **DynamicMem keep (C06)** + RHELM temporal | Native weak |
| Fill long realistic history under persona | **DynamicMem/RHELM C01+C10** | Native short context |
| Ship DATA_STANDARD JSON tomorrow | **Native** (+ RHELM adapter later) | C09 native=10, RHELM=8, DynamicMem=2 |

---

## One-sentence MECE summary

- **Native owns construct + validity gates + schema** (A3/V1/V2/A5 packaging).  
- **Keep-set owns deep profile, long horizon, and A4/A5 volume**.  
- **Nothing in the ≥7 keep-set replaces native A3**; MyPCBench adds no ≥7 cell.  
- Closing the gap = **graft keep-set substrate/strata onto native item templates**, not the reverse.

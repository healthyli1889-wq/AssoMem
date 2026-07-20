# Persona Data Strategy — the whole person as the atomic unit

> Supersedes the per-domain framing in PERSONA_DATA_SOURCES.md / PERSONA_GROUNDING_HYBRID.md.
> Audience: co-authors sourcing and constructing data for the associative-memory benchmark.
> One question this doc answers: *how do we source and build persona data so that
> associative (cross-facet) memory can be validly measured at scale?*
> HF ids and links verified 2026-07-11. Access: 🟢 open `load_dataset` · 🟡 reg/gate · 🔴 off-HF.

---

## A. The principle — the atomic unit is a *person*, not a *domain*

**Rule (quotable):** *A complete user profile is the atomic unit of this benchmark.
`finance / health / work / learning / hobby / habit` are not categories to source
separately — they are **projections of one coherent person**. Sourcing one facet per
dataset means stitching facets from **different** people, which fabricates the very
cross-facet associations we intend to measure.*

**Why this block exists (what it prevents).** It blocks the intuitive-but-fatal move
"just grab one dataset per domain and combine." For an *associative* benchmark that move
is not merely suboptimal — it is a **construct-validity failure**: if a persona's health
trace comes from person A and their finance trace from person B, any "health×finance"
association we plant is incoherent and unreal, and a careful annotator or reviewer can
expose it. Only a single, attribute-correlated real person guarantees the planted
association is a *real* associable relation. This is the same standard our provenance/D9
auditor enforces downstream (§F).

---

## B. The profile object — what one complete person contains (schema)

A profile is one real, coherent person represented as:

1. **Facets as projections** (not silos): `health, diet, work, learning, finance, hobby,
   habit` — each a *view* onto the same person, sharing one identity and timeline.
2. **Static vs. dynamic attributes** (PersonaMem-style split):
   - *Static* (never change): demographics, occupation, background — the anchor.
   - *Dynamic* (revealable / updatable over sessions): preferences, habits, goals,
     constraints, states — the material for `updates`/temporal constructs.
3. **The load-bearing asset — real cross-facet correlations.** The facets are *not
   independent*: a night-owl chronotype (health) correlates with occupation (work),
   coffee/alcohol purchases (diet), late gaming (hobby), and spending rhythm (finance).
   **These correlations are the one thing that cannot be faked** — and they are precisely
   what makes cross-facet association real. They are our moat vs. LoCoMo/PersonaMem, whose
   facets are LLM-invented and therefore uncorrelated except by accident.
4. **A timeline.** Events are timestamped so facets can be *dispersed across sessions*
   (a hard requirement for the disconnected-reasoning property in §C).

**Why this block exists.** It defines the target object we manufacture, and names the
non-negotiable property (correlation) that separates a *coherent person* from a *bag of
attributes*. It blocks "what fields does a persona need and where do they come from."

---

## C. The associative overlay — how "association" is defined *on one profile*

This is what turns a persona into a *test item*. Everything is defined over a single
profile P:

- **Evidence** = **≥2 facets of the same person P** that jointly imply a conclusion never
  stated. `E_A ∈ facet_i(P)`, `E_B ∈ facet_j(P)`, placed in **different sessions**, with
  **low lexical overlap** (cos(query, E)<0.15). The answer is the **latent ConceptNode**
  binding them.
- **Distractor** = **a facet drawn from a *different* person Q**, inserted as if it could
  belong to P — plausible, topically near the query, but off-P's-path. This is elegant:
  we **do not synthesize distractors**; we reuse *real* facets from the per-domain pools
  (§D), which automatically clear the hammer-distractor gate (INVERSION > 0.20, §F).
- **The 3 constructs, restated as cross-facet bindings:**
  - **C1 temporal co-occurrence** — two facet-events of P recur together in time.
  - **C2 causal / constraint binding** — one facet of P constrains/causes another
    (e.g., health condition → dietary constraint → decline an option).
  - **C3 cross-domain analogical transfer** — a pattern in facet_i of P maps to facet_j.
- **Control axes (V1–V4)** attach here: V1 discriminant (low overlap), V2 interference
  (the other-person distractor), V3 temporal (shuffle-paired copy for `updates` items),
  V4 inhibitory (a superseded facet of P that must be suppressed).

**Why this block exists.** It is the benchmark-specific core — the bridge from "a person"
to "a solvable associative item." It blocks "how is this different from any persona
dataset." Highlight: **distractor = another person's real facet** is both the cheapest and
the most realistic interference design available.

---

## D. Sources — tiered by *whole-person completeness*, not by domain

### Tier 1 — true all-domain, correlated persons (ideal; off-HF)
One record = a coherent person across health, work, finance, family, hobby, tracked over
time, with **real** within-person correlations. **This is the §A/§B ideal.**
- **MIDUS** 🔴 — health + Big-Five personality + work + family + finance + daily-stress
  diaries; ~7,100 people; **pure public download** (ICPSR/NACDA). https://midus.wisc.edu/data-access/
- **UKHLS / Understanding Society** 🟡 — broadest single-record domain coverage (health,
  diet/exercise, work, education, finances, hobbies, family); ~100k people, 15 annual
  waves; free UK Data Service registration (SN 6614). https://www.understandingsociety.ac.uk/
- (HRS, NLSY, PSID, SOEP as alternates — see prior notes.)
- **Cost:** not on HF → one-time download + field-mapping to our profile schema.

### Tier 2 — whole-person on HF, but within the health/lifestyle sphere
One *real* person across multiple facets (health+diet+habit+mood), longitudinal — just
missing work/finance.
- **`aai530-group6/pmdata`** 🟡 CC-BY-NC — 16 people × 5 months: HR/steps/sleep + mood/
  fatigue/stress + **meals + weight + alcohol + injuries + training**. The richest
  multi-facet real person here, BUT ⚠ **`load_dataset()` default config returns only a
  food-photo image column** — the behavioral tabular streams are raw per-participant
  files in the repo → **budget manual file parsing**, not a clean one-line load.
  https://huggingface.co/datasets/aai530-group6/pmdata
- **`wellness10/LifeSnaps_dataset`** 🟢 MIT — ~71 people × 4 months: wearable + PANAS
  affect + STAI anxiety + BREQ-2 motivation + personality. Loads cleanly per subset →
  **the best *directly-loadable* HF whole-person (health-sphere) source.** https://huggingface.co/datasets/wellness10/LifeSnaps_dataset
- *Gap:* no HF dataset offers a clean `load_dataset`-native daily physiological/time-use
  lifelog (sleep+steps+mood+meals per subject, timestamped). pmdata is closest but
  images-only as loaded. If required, plan for manual parsing.

### Tier 3 — the authors' own multi-app crawl (whole-person, tiny N)
Real, truly all-domain (computer-use crawl across your own apps), highest fidelity, N≈5.
→ Use as **gold anchors** (one hand-built exemplar per construct×domain cell), not scale.

### Demoted — per-domain datasets → *facet texture* + *distractor pool*
No longer backbones. Two uses: (a) enrich a facet with **real vocabulary/entities**;
(b) supply **other-person facets as distractors** (§C). All 🟢 loadable:
| Facet | Dataset (link) | Use |
|---|---|---|
| diet | `McAuley-Lab/Amazon-Reviews-2023` (`raw_review_Grocery_and_Gourmet_Food`) — https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 | food buys/reactions; filter users ≥N |
| learning | `mgor/EDNet` — https://huggingface.co/datasets/mgor/EDNet | per-student study traces |
| learning | `ASSISTments/FoundationalASSIST` 🟡gated — https://huggingface.co/datasets/ASSISTments/FoundationalASSIST | skill-mastery arcs |
| work | `datasetmaster/resumes` — https://huggingface.co/datasets/datasetmaster/resumes | full-resume attributes |
| work | `lukebarousse/data_jobs` — https://huggingface.co/datasets/lukebarousse/data_jobs | real skills/salary/role vocab |
| habit/hobby | `matthewfranglen/lastfm-1k` (🥇 ~21k timestamped events/user + demographics) — https://huggingface.co/datasets/matthewfranglen/lastfm-1k | listening rhythm; strong temporal dispersal |
| habit/mobility | `w11wo/LLM4POI` (Apache-2.0, timestamped check-ins, needs config) — https://huggingface.co/datasets/w11wo/LLM4POI | daily routine/location habits |
| habit/shopping | `McAuley-Lab/Amazon-Reviews-2023` (any category, filter ≥20) | life-stage/shopping habits (timestamped) |
| hobby | `ashraq/movielens_ratings` (⚠ no timestamps → static taste only) — https://huggingface.co/datasets/ashraq/movielens_ratings | film taste (distractor pool only) |
| finance | `pointe77/credit-card-transaction` (synthetic) — https://huggingface.co/datasets/pointe77/credit-card-transaction | longitudinal txn sequence |
| finance | `scikit-learn/credit-card-clients` (real) — https://huggingface.co/datasets/scikit-learn/credit-card-clients | 6-month repayment panel |

**Selection standard (a source qualifies as a backbone only if):** S1 per-user grouping ·
S2 depth (≥~20 events or ≥~15 attrs/person) · S3 longitudinal/timestamped · S4 concrete
real entities · S5 HF-loadable (or Tier-1 acceptable off-HF) · S6 research license · S7
demonstrable associability (name 2 facets → 1 latent conclusion).

**The decision (recommended = C):**
- **(A) HF-only** → whole-person limited to health/lifestyle (Tier 2); work/finance would
  be stitched → association confined to the health sphere. *Rejected: too narrow.*
- **(B) Off-HF backbone** → MIDUS/UKHLS true all-domain persons; one-time processing cost.
- **(C) Hybrid (recommended)** → **MIDUS/UKHLS backbone** (all-domain correlated person)
  **+ PMData/LifeSnaps** for health-sphere day-level texture **+ per-domain pools** for
  facet vocabulary & distractors **+ author crawl** for gold anchors.

**Why this block exists.** It answers "which link do I click" while enforcing §A. It
surfaces the real tradeoff (HF-loadable vs. truly all-domain) as an explicit co-author
decision rather than hiding it. Honest gap: **finance is the thinnest facet** — real
multi-year per-person transactions require off-HF (Berka, Kaggle); true all-domain
correlated persons are **not on HF at all**.

---

## E. Construction pipeline — from one record to one benchmark sample

```
1. DRAW      one Tier-1 record (a coherent person) → structured facet fields
2. CARD      LLM elaborates → persona card, split static / dynamic (facets as projections)
3. TEXTURE   enrich each facet with REAL entities from the demoted pools + Web APIs
             (O*NET occupation, Open Food Facts product, FRED rate, Last.fm artist …)
4. OVERLAY   choose construct (C1/C2/C3); pick E_A ∈ facet_i, E_B ∈ facet_j of THIS person
             → latent ConceptNode; pull distractors = facets of OTHER people (pool)
5. GRAPH     build LoCoMo-style event-graph timeline; disperse E_A, E_B, distractors,
             filler across 12–16 sessions on a reveal schedule (E never in final 2 sessions)
6. DIALOGUE  generate multi-session conversation over the timeline; Generator–Critic
             faithfulness check per session (persona persisted)
7. PROVENANCE stamp every evidence node with {source_id, record_id, entity_url}
```

Output = a schema-conformant sample + its latent graph + provenance. Steps 1–4 = the
reusable `persona_seed.py`.

**Why this block exists.** Turns §A–D into executable steps (the `persona_seed.py` spec).
Blocks "I understand the idea but not the how."

---

## F. Validation, decision resolution, coverage (operational)

### Auditor D-checks (in `prepare.py`; a sample ships only if all pass)
- **Coherence** — the two evidence facets are *plausibly correlated in one real person*
  (Tier-1 provenance makes this automatic; flag if facets came from different records).
- **D9 entity resolution (grounding)** — every evidence entity URL resolves → the fact is
  **real**, not hallucinated. *No prior benchmark supports this check.*
- **INVERSION > 0.20** — the other-person distractor out-retrieves the gold (hammer gate).
- **Disconnected-reasoning / leave-one-out** — removing either E_A or E_B breaks the
  answer → the item is genuinely multi-hop (rejected if single-hop-solvable).
- **Low overlap** — cos(query, E)<0.15, entity overlap 0.

### Recommended source plan (decision C, made concrete)
| Facet | Backbone (person) | Texture / entities | Distractor pool |
|---|---|---|---|
| health, diet, habit | MIDUS/UKHLS row → PMData/LifeSnaps texture | Open Food Facts, openFDA | other PMData users, Amazon Grocery |
| work, learning | MIDUS/UKHLS row | O*NET, EDNet, resumes | other resumes / EDNet students |
| finance, planning | MIDUS/UKHLS row | FRED, credit panels | other credit-card-clients rows |
| hobby | MIDUS/UKHLS row | Last.fm, MovieLens, Steam | other lastfm/steam users |

### Coverage plan
- Frame: 3 constructs × 5 domain-projections = 15 cells; V1/V2 embedded per sample,
  V3/V4 as derived subsets.
- Tiers: **pilot 5/cell = 75** (validate pipeline+judge) · **v1 20/cell = 300**
  (per-construct claims, ±5%) · **full 40/cell = 600**.
- Each cell gets **one Tier-3 hand-built gold anchor** before batch generation.

### Honest gaps (state in the paper)
- True all-domain correlated persons are **not on HF** → Tier-1 is off-HF (one-time cost).
- **Finance** is the thinnest facet; real longitudinal transactions need off-HF fusion.
- Tier-2 HF whole-persons cover only the health/lifestyle sphere (N≈16/71).

**Why this block exists.** Makes the data *trustworthy* (coherent person, real facts, hard
distractors, true multi-hop) and *operational* (who feeds what, how many). Blocks "how is
this not just more invented data" and "how much do we actually need."

---

## Spine (recite after reading)
*A real, correlated whole person is the atomic unit (A); it is many correlated facet-
projections with a timeline (B); an item binds two facets of that person, with another
person's facet as the distractor (C); persons come from tiered sources — all-domain panels
as backbone, HF lifelogs for texture, per-domain sets demoted to texture+distractors (D);
a pipeline turns one record into a sample with provenance (E); the auditor guarantees the
person is coherent, the facts are real, the distractors are hard, and the hop is genuine (F).*

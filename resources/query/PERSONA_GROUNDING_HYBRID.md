# Hybrid Persona Grounding — HF ⊕ Real-World Web (the innovation)

> Supersedes the portal-heavy list in PERSONA_DATA_SOURCES.md for *operational* use.
> Everything here is either `load_dataset("<id>")`-able or a **free public API**.
> All HF IDs and API endpoints verified via web July 2026.

---

## 0. The contribution (and why it's novel)

**Claim.** Existing long-term-memory benchmarks (LoCoMo, PersonaMem, PersonaBench)
generate personas by letting an LLM *invent* details from a seed. Those details are
**unverifiable, homogeneous, and untraceable** — a reviewer cannot check whether "I
switched to a keto diet" corresponds to anything real, and the generator drifts to
generic tropes. That is a construct-validity hole: if evidence is model-invented, you
can't be sure the "associable fact" is a real fact rather than a hallucinated one.

**Our move — Hybrid Grounding.** Every persona fact is produced by fusing two layers,
and carries a **provenance pointer**:

```
persona_fact = draw(HF structured dataset)          # scalable, clean, reproducible distribution
             ⊕ resolve(real-world Web API/entity)    # fresh, specific, long-tail, checkable
             + provenance{hf_id, record_id, web_url}  # ← the thing incumbents don't have
```

- **HF layer** gives the *distributional truth* at scale, reproducibly (a reviewer re-runs it).
- **Web layer** resolves each fact to a *real entity* (a real product barcode, a real
  occupation SOC code, a real fund ticker, a real drug) — so evidence is concrete and
  **verifiable**, and the generator can't drift to invented generics.
- **Provenance** lets `prepare.py`'s auditor **verify the fact exists in the world** (new
  D-check: entity resolves) — directly answering the reviewer's "real fact or hallucination?"

### Novelty positioning (must cite + differentiate)
| Prior work | What it grounds | Why we're different |
|---|---|---|
| **Synthia** (2507.14922, 2025) — *closest* | personas, from ONE social-media source | no HF/structured fusion, target is social-sim not memory, **no per-fact traceability** |
| **PersonaHub** (2406.20094) | web-scale personas | personas are **abstract LLM descriptions**, not source-traceable real entities |
| **Source2Synth** (2409.08239) | QA/data from real tables/docs | grounds *data*, **not personas** |
| **WebGLM / WebGPT** | QA answers w/ web citations | grounds *answers*, not persona identity |
| **LoCoMo / PersonaMem / PersonaBench** | — | personas fully **synthetic & unverifiable** ← our wedge |

**One-line wedge:** *fuse structured HF datasets with live web so each persona fact is
fresh, specific, and traceable to a real entity — for a long-term memory benchmark.* No
prior work combines all three (fusion + traceability + memory-benchmark target).

---

## 1. HF-sufficiency map — where to lean HF vs. where Web fusion is mandatory

| Domain | Real per-person on HF? | Verdict | Web fusion role |
|---|---|---|---|
| **Hobby/leisure** | abundant, longitudinal | 🟢 **HF-sufficient** | optional (real titles/entities) |
| **Learning** | massive behavioral logs | 🟢 **HF-sufficient** | optional |
| **Diet — preferences** | Amazon Grocery, 7M users | 🟢 **HF-sufficient** | product realism |
| **Diet — meal/calorie logs** | missing (Kaggle only) | 🟡 **needs fusion** | logs + nutrition |
| **Health/body** | deep but tiny N (~87 ppl) | 🔴 **needs fusion** | population diversity + real conditions/drugs |
| **Work/career** | small resume snapshots | 🔴 **needs fusion** | occupations, salaries, dev signals, arcs |
| **Finance** | only credit snapshots | 🔴 **needs fusion (thinnest)** | spending, funds, cost-of-living |

**The honest research narrative:** HF is strong where the world already logs behavior at
scale (media consumption, e-commerce, ed-tech). It's thin exactly where data is private
(health, personal finance, career arcs) — **which is precisely where Web fusion + our
provenance mechanism is the contribution, not a workaround.**

---

## 2. Per-domain: HF dataset ⊕ paired Web source

### Health/body 🔴
- **HF (seed depth):** `aai530-group6/pmdata` (16 ppl, multimodal Fitbit+meals+mood diaries, CC-BY-NC) · `wellness10/LifeSnaps_dataset` (71 ppl, exercise-motivation/affect/anxiety + wellness, MIT).
- **Web (breadth + real entities):** ClinicalTrials.gov API v2 `[free]` (real conditions/interventions) · openFDA `[free]` (real drugs/dosages) · MedlinePlus web services `[free]` (symptom vocab) · Strava API `[OAuth, ToS: no bulk store]` (real races/gear).
- **Fuse:** PMData gives a real daily quantified-self *rhythm*; openFDA/ClinicalTrials resolve the persona's condition + medication to **real named drugs/conditions** → chronotype/health evidence is concrete and checkable.

### Diet/food 🟡
- **HF:** `McAuley-Lab/Amazon-Reviews-2023` config `Grocery_and_Gourmet_Food` (7.0M users, real food-buying histories) · `openfoodfacts/product-database` (4.67M products, nutrition, AGPL/ODbL) · `corbt/all-recipes` (2.15M recipes, content).
- **Web:** USDA FoodData Central API `[free key]` (real foods + FDC IDs, traceable) · Open Food Facts API `[free, ODbL share-alike]` (real barcoded products) · TheMealDB `[free]` (named dishes).
- **Gap:** true meal/calorie **diaries** (MyFitnessPal) are Kaggle-only → fuse from web/Kaggle if you need day-level eating logs.

### Work/career 🔴
- **HF:** `datasetmaster/resumes` (whole-resume-per-row, richest per-person; ⚠ viewer flaky, load parquet/JSON directly, MIT) · `lukebarousse/data_jobs` (786k roles: skills/salary/remote, Apache-2.0) · `gpriday/job-titles` (65k occupation vocab, cleanest O*NET-ish mirror).
- **Web:** **O*NET Web Services** `[free reg]` (900+ real occupations→tasks/skills/SOC) · BLS API `[free]` (real wages by occupation) · GitHub API `[free]` (real repos/languages for dev personas) · Stack Exchange API `[free]` (real tags a persona struggles with).
- **Gap:** developer-survey demographics + LinkedIn arcs not on HF → Stack Overflow survey (Kaggle) + O*NET API fusion.

### Learning 🟢
- **HF:** `mgor/EDNet` (372M interactions, per-learner study traces, non-commercial) · `ASSISTments/FoundationalASSIST` (5k students + real problem text, ⚠ gated, CC-BY-NC) · `mstz/student_performance` (3k, demographics+scores).
- **Web (optional):** Khan/Coursera/edX catalog pages `[scrape, ToS]` for real named courses.

### Hobby/leisure 🟢
- **HF:** `McAuley-Lab/Amazon-Reviews-2023` (any vertical: `Books`/`Movies_and_TV`/`Video_Games`/`CDs_and_Vinyl`, per-user taste streams) · `matthewfranglen/lastfm-1k` (794 users, listening + demographics — rare both-signals) · `ashraq/movielens_ratings` (film) · `recommender-system/steam-review-and-bundle-dataset` (playtime libraries, ⚠ needs .json.gz parsing).
- **Web (optional real entities):** Open Library API `[free]` (real books/ISBNs, the Goodreads-API replacement) · MusicBrainz `[free]` · Last.fm API `[free]` · Steam store `[free]` · BoardGameGeek XML API `[free]`.

### Finance/planning 🔴 (thinnest)
- **HF:** `scikit-learn/credit-card-clients` (30k real cardholders, 6-mo repayment, CC0) · `AiresPucrs/german-credit-data` (1k real applicants). *All transaction-scale HF data is synthetic or has no user grouping — do not use for real personas.*
- **Web:** SEC EDGAR API `[free]` (real tickers/holdings) · FRED API `[free]` (real mortgage rates/CPI a planner cites) · r/personalfinance/Bogleheads `[Reddit ToS]` (real funds like VTSAX, FIRE numbers) · Numbeo `[paid]` (cost-of-living).
- **Fuse:** credit-card-clients gives a real repayment *behavior pattern*; FRED/EDGAR resolve the persona's plan to **real rates/funds** → financial evidence is concrete.

### Persona seeds + conversational voice (all HF, all confirmed)
- **Seeds:** `proj-persona/PersonaHub` (billion-scale; PersonaMem's own seed source) · `google/Synthetic-Persona-Chat` (+ Generator–Critic loop to copy).
- **Voice/style:** `allenai/WildChat-1M` (real messy user turns, ODC-BY) · `daily_dialog` (human-to-human cadence).
- **Comparables to beat:** `snap-research/locomo` · `bowen-upenn/PersonaMem`.

---

## 3. The fusion mechanism (what actually ships in each sample)

```
1. BACKBONE  draw one coherent record  →  MIDUS/UKHLS row  OR  a per-person HF record
             (e.g. lastfm-1k user #412: 34, F, Germany, indie/electronic, 15k plays)
2. ATTRIBUTES split static vs dynamic (PersonaMem-style) from HF fields
3. ENTITY-RESOLVE each concrete fact against a Web API  →  real entity + URL
             "buys keto snacks"  →  Open Food Facts  →  real product + barcode
             "software dev, Rust"  →  O*NET 15-1252 + GitHub Rust repos
             "index investor"      →  FRED 30yr-rate + EDGAR VTSAX
4. PROVENANCE store {hf_id, record_id, web_entity_url} on every evidence node
5. GENERATE  multi-session dialogue (LoCoMo event-graph timeline) revealing the facts
6. AUDIT     prepare.py D1–D8 + NEW D9: every evidence entity URL resolves (fact is real)
```

**Why this is the paper's defensible core:** LoCoMo/PersonaMem cannot run step 6-D9 —
their facts have no external referent. Provenance = the mechanism that turns "realistic-
looking" into "verifiably real," and it's cheap to add.

---

## 4. License / ToS landmines (read before shipping)

| Source | Landmine |
|---|---|
| **Reddit Data API** | free non-commercial only; **commercial = signed contract ~$0.24/1k**; **AI-training use needs explicit consent** — risky if benchmark is redistributed |
| **Open Food Facts** | ODbL **share-alike**: a combined DB must be re-released as open data |
| **Yelp Fusion** | now **fully paid** ($7.99–14.99/1k) — dropped in favor of free venue sources |
| **Goodreads API** | dead (no new keys since Dec 2020) → use **Open Library** |
| **EdNet / FoundationalASSIST / PMData / LifeSnaps(paper)** | CC-BY-**NC** — research only |
| **Amazon-Reviews-2023** | license not stated on card (McAuley research terms) — verify before commercial |
| **datasetmaster/resumes** | HF viewer crashes; load files directly |
| **Steam HF set** | malformed json.gz; needs manual parse |
| **BrightData/Goodreads-Books** | restrictive Master Service Agreement |

---

## 5. Fastest all-open build (zero gating, ship today)

**Stack:** `proj-persona/PersonaHub` seeds → per-person HF backbone
(`matthewfranglen/lastfm-1k` hobby · `mgor/EDNet` learning · Amazon-Reviews-2023 Grocery diet
· `datasetmaster/resumes` work · `scikit-learn/credit-card-clients` finance ·
`aai530-group6/pmdata` health) → **free Web APIs** (USDA FDC, O*NET, FRED, Open Library,
openFDA) for entity resolution + provenance → `allenai/WildChat-1M` style → generate →
audit with D9 entity-resolution check.

Work/health/finance lean on the Web layer (HF-thin); hobby/learning/diet-preferences lean
on HF. That asymmetry **is** the story: fusion is load-bearing exactly where private-domain
data is scarce, and provenance is what makes it publishable.

**Next artifacts to build:** (a) `persona_seed.py` implementing steps 1–4 with the
provenance field; (b) the D9 entity-resolution auditor check in `prepare.py`; (c) a
one-domain end-to-end worked sample (lastfm-1k user → grounded persona → 12-session
dialogue → audit) to prove the pipeline.

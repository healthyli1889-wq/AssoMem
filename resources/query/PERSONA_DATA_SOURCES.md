# Persona Data Sources — grounding deep, realistic personas for AssocMemBench

> Problem this solves: seeding personas from your own personal data gives **small N**
> and personas the generator doesn't "know" deeply → thin, repetitive dialogue with
> **no real detail for evidence to associate across**. Associative memory is precisely
> the signal *between* a person's real details, so shallow personas kill the benchmark.
>
> All URLs verified via web July 2026. Access friction is marked explicitly:
> 🟢 open direct download · 🟡 free registration/request · 🔴 application/contract.

---

## 0. The recipe — two-layer grounding (do this, not silo-stitching)

Do **not** find 5 isolated datasets and staple a person together — the attributes
won't be realistically correlated. Instead:

1. **BACKBONE (one coherent whole person).** Draw one respondent record from a
   **longitudinal multi-domain panel** (§2). One row already ties job↔income↔health
   ↔diet↔family↔hobbies with *real within-person correlations*, tracked over time.
   → a persona whose "took up cycling after a health scare, then switched jobs"
   comes from real data, not invention.
2. **FLESH (per-domain texture + voice).** Layer domain-specific datasets (§1) to add
   real vocabulary, specific tastes, and day-level rhythm — the concrete details that
   become associable evidence.
3. **BUDGET (realism governor).** Use **ATUS** time-use to cap how much time the
   persona plausibly spends per activity, so you don't generate a "4 hobbies × 3h/day"
   impossible person.
4. **SEED SCALE + VOICE.** Use **PersonaHub** for scale/diversity of seeds and
   **WildChat/DailyDialog** to make the dialogue *sound* human (§3).

---

## 1. Per-domain datasets (5 scenarios)

### 1A. Health / body
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **All of Us** ⭐ TOP | EHR conditions+meds + lifestyle surveys + body measures + **daily Fitbit** on same person; ~59k with wearables | 🔴 free but gated (Researcher Workbench, ID verify, training, in-cloud only) | researchallofus.org |
| **NHANES** ⭐ open fallback | diet + labs + meds + sleep/PHQ-9 + 7-day accelerometry; per-person cross-section | 🟢 public domain, no reg | wwwn.cdc.gov/nchs/nhanes |
| **LifeSnaps** | 4mo Fitbit Sense (HR/HRV/SpO2/sleep/stress) + Big-Five/PANAS/anxiety + daily EMA; 71 ppl | 🟡 Zenodo login + request | zenodo.org/records/6832186 |
| **PMData** | 5mo Fitbit + daily mood/fatigue/soreness/stress + meal+injury logs; 16 ppl | 🟢 CC BY-NC | osf.io/vx4bk |
| **SHHS** | full overnight PSG + cardiometabolic phenotype + Epworth; deepest sleep/chronotype | 🔴 free NSRR DUA | sleepdata.org/datasets/shhs |
| **MIMIC-IV** | real diagnosis+meds+labs trajectories (hospital-centric, no daily life) | 🔴 PhysioNet credential + CITI | physionet.org/content/mimiciv |

Chronotype note (your night-owl anchor): **SHHS** (clinical sleep) or **NHANES
accelerometry / LifeSnaps** (behavioral sleep timing) are the grounded sources.

### 1B. Diet / food
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **MyFitnessPal Food Diary** ⭐ TOP | ~9.9k users × up to **6mo daily meal logs** + portions + nutrition + weight-loss goal; real adherence/relapse arc | 🟡 SMU LARC data-use request | smu.edu.sg …/myfitnesspal-food-diary-dataset.html |
| **Food.com Recipes & Interactions** | 18yr user–recipe reviews/ratings/text → cuisine/ingredient/skill preferences | 🟢 Kaggle | kaggle.com/…/food-com-recipes-and-user-interactions |
| **NHANES WWEIA** | 2× 24h recalls, every food coded, health+demographics linkable | 🟢 public domain | wwwn.cdc.gov/nchs/nhanes/tutorials/dietaryanalyses.aspx |
| **UK NDNS** | 3–4 day diaries + biomarkers; non-US personas | 🟡 UK Data Service EUL | ukdataservice series 2000033 |
| **Amazon Grocery Reviews '23** | per-user grocery purchase+review history → brand loyalty, dietary lifestyle | 🟢 HF / McAuley | amazon-reviews-2023.github.io |
| **USDA FoodData Central** | food→nutrition/portion reference (vocabulary layer, not people) | 🟢 CC0 | fdc.nal.usda.gov/download-datasets |

### 1C. Work / learning  *(your urgent domain — see §5 for the immediate plan)*
> **Key distinction:** O*NET describes **occupations, not people** — it's a persona
> *dictionary*. Per-**person** samples = Stack Overflow / Kaggle / PIAAC (one rich row
> per real person) or NLSY/EdNet/OULAD (same person over time). Draw the person from a
> per-person set, then enrich job-talk with O*NET.

**WORK/CAREER**
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **Stack Overflow Developer Survey** ⭐ WORK top | one rich row/real dev: DevType, exact language/tool/cloud stack, comp(USD), org-size, remote, learning methods, AI-tool use; ~65–90k/yr × 15 waves | 🟢 open CSV, ODbL | survey.stackoverflow.co |
| **NLSY79/97** (longitudinal arc) | per-person **career biography over 25–45yr**: every job, wage growth, layoffs, return-to-school + AFQT cognition; 12,686 / 8,984 ppl | 🟡 free account (Investigator) | nlsinfo.org/investigator |
| **PIAAC** (OECD adult skills) | assessed literacy/numeracy/problem-solving + **skill-use at work** (ISCO occ, task discretion); ~250k adults, 30+ countries | 🟢 open PUFs | oecd.org/en/data/datasets/piaac-2nd-cycle-database.html |
| **O*NET** (occupation dictionary) | per-occupation tasks/tools/work-context/work-styles — enrich a person's job-talk | 🟢 open, CC BY | onetcenter.org/database.html |
| Kaggle ML & DS Survey | DS-flavored per-respondent snapshot | 🟢 Kaggle | kaggle.com/c/kaggle-survey-2021/data |

**LEARNING/EDUCATION**
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **EdNet** (Riiid) ⭐ LEARNING top | **131M interactions / 784k students**, 2yr; per-tap trace (response time, explanation-reads, lecture-watch, purchases) = study-behavior fingerprint | 🟢 open, no reg, CC BY-NC | github.com/riiid/ednet |
| **OULAD** | demographics→daily clicks→assessments→outcome; ties background↔behavior↔result; 32,593 students, 10.6M clicks | 🟢 open, CC BY | analyse.kmi.open.ac.uk/open_dataset |
| **ASSISTments** | fine-grained **skill mastery** curves (math KCs, hints, mastery events) | 🟢 free | sites.google.com/site/assistmentsdata |
| **Junyi Academy** | ~16M attempts / 72k students + prerequisite knowledge-map | 🟢 Kaggle | kaggle.com/datasets/junyiacademy/learning-activity-public-dataset-by-junyi-academy |
| **HarvardX–MITx / PISA** | MOOC person-course (641k rows) / 15-yr-old skills+attitudes (~600k) | 🟢 open | dataverse.harvard.edu (DVN/26147) / oecd.org/en/data/datasets/pisa-2022-database.html |

### 1D. Hobby / leisure
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **ATUS** ⭐ budget backbone | how real people allocate leisure minutes (TV/read/exercise/social) by demographic — the realism governor | 🟢 open, no reg | bls.gov/tus |
| **LFM-1b/2b (Last.fm)** ⭐ deepest silo | >1B scrobbles, 120k users, 15yr → daily rhythm + genre arc | 🟡 JKU request | cp.jku.at/datasets |
| **MovieLens 25M** | 162k users, ratings+self-authored tags → cinephile fingerprint | 🟢 open | grouplens.org/datasets/movielens/25m |
| **Goodreads (UCSD)** | 229M interactions + **review text (reader's own voice)** | 🟢 open academic | mengtingwan.github.io/data/goodreads.html |
| **Steam (UCSD)** | **playtime hours** per game (honest intensity) + reviews | 🟢 open | cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data |
| **Yelp Open Dataset** | venue/dining taste + written voice + going-out cadence | 🟡 license click-through | yelp.com/dataset |
| **PMData** | fitness/activity daily texture (also in Health) | 🟢 CC BY-NC | osf.io/vx4bk |

### 1E. Finance / planning
| Dataset | Depth | Access | URL |
|---|---|---|---|
| **SCF (Fed)** ⭐ TOP | full household balance sheet + income + **saving motives/risk tolerance/budgeting** (the "why") | 🟢 open, no reg | federalreserve.gov/econres/scfindex.htm |
| **CEX Diary (BLS)** ⭐ texture | **daily itemized spending diaries** — weekly basket down to coffee/takeout | 🟢 open | bls.gov/cex/pumd_data.htm |
| **PSID** | decades of income/wealth/job/home arcs + family lineage (life-arc backstory) | 🟡 free reg | psidonline.isr.umich.edu |
| **UK WAS (ONS)** | wealth/debt + **retirement-planning attitudes**; non-US | 🔴 free reg (safeguarded) | ukdataservice study 7215 |
| **UCI Credit-Card Default** | 6-month monthly repayment behavior series; 30k clients | 🟢 CC BY | archive.ics.uci.edu/dataset/350 |
| **LendingClub (Kaggle mirror)** | per-borrower loan purpose + credit narrative under stress | 🟡 Kaggle, unofficial provenance | kaggle.com/…/lending-club |

---

## 2. BACKBONE — longitudinal whole-person panels (pick ONE as the spine)

| Panel | Domains in one record | Span | Access | URL |
|---|---|---|---|---|
| **Understanding Society / UKHLS** ⭐ TOP | health+diet/exercise, work+earnings, education, finances, hobbies, family, psychosocial | 15 waves, 2009– | 🟡 UK Data Service EUL (SN 6614), non-UK OK | understandingsociety.ac.uk |
| **MIDUS** ⭐ richest interior | health, personality(Big-Five), daily-stress diaries, work, family, finance | 3 waves, 1995–2014 | 🟢 **pure public download** ICPSR | midus.wisc.edu/data-access |
| **HRS** | health↔work↔wealth↔retirement (midlife+); RAND harmonized file | biennial 1992– | 🟡 free reg | hrsdata.isr.umich.edu |
| **PSID** | income/wealth/work/education/family, multi-generational | 1968– | 🟡 free reg | psidonline.isr.umich.edu |
| **NLSY79/97** | week-by-week job history + AFQT cognition + schooling from youth | 1979/1997– | 🟡 free account | nlsinfo.org |
| **SOEP** (DE) | UKHLS-like breadth + personality; Europe | 1984– | 🔴 contract | diw.de/en/soep |
| **HILDA** (AU) | full 5-domain + strong time-use; Australia | 2001– | 🔴 deed poll | melbourneinstitute.unimelb.edu.au/hilda |

**Decision:** UKHLS = best breadth + genuinely open. MIDUS = zero-friction + best inner
life (use when persona needs believable personality). HRS = midlife+ finance/health realism.

---

## 3. Persona seeds, style, and the 3 comparables to beat

**Seeds (scale):** **PersonaHub** (proj-persona/PersonaHub, HF) — billion-scale, purpose-built,
*the same seed source PersonaMem uses* → parity by default. CC-BY-NC-SA.
Also: PERSONA-CHAT (1,155 human personas, format template), Synthetic-Persona-Chat
(Google, **Generator–Critic loop to copy for faithfulness**).

**Style (human voice):** **WildChat-1M** (allenai, ODC-BY) — real messy user turns +
incidental self-disclosure. **DailyDialog** — human-to-human cadence (closer to your
"persona reveals to a partner" setting). LMSYS-Chat-1M for breadth.

**The 3 comparables — how they build personas (match/exceed):**
- **MSC**: human persona + **grows across sessions** (append new facts) + time-gap+summary. Ceiling 5 sessions.
- **LoCoMo**: MSC seed → GPT expands to detailed profile → **causal event-graph (~25 life events) drives the timeline** → ≤32 sessions. Only 50 personas.
- **PersonaMem**: PersonaHub seed → **static attributes vs dynamic preferences** split → timed reveal/reinforce/**update** at week/month/year offsets + `distance_to_ref` metric. Only 180 histories, MCQ-only.

**Recommended stack (beats each on its weakest axis):**
`PersonaHub seeds → UKHLS/MIDUS backbone for real correlations → LoCoMo event-graph timeline
+ PersonaMem static/dynamic split & timed updates → domain datasets (§1) for texture
→ WildChat/DailyDialog style → Synthetic-Persona-Chat Generator–Critic for faithfulness.`

---

## 4. Access-friction cheat sheet (start today with zero gating)

🟢 **Download right now, no account:** NHANES (health+diet), MIDUS (whole-person backbone),
ATUS (leisure budget), MovieLens, Steam, Goodreads, Food.com, Amazon Reviews, FoodData Central,
SCF, CEX, UCI Credit-Card Default, O*NET, PISA, PIAAC, EdNet, OULAD, PersonaHub, WildChat, DailyDialog.

🟡 **Quick free registration/request:** UKHLS, HRS, PSID, NLSY, LifeSnaps, MyFitnessPal, NDNS, LFM-1b, Yelp.

🔴 **Application/contract (slow):** All of Us, MIMIC-IV, SHHS, SOEP, HILDA, UK WAS.

**Fastest publishable path:** MIDUS backbone + NHANES(health/diet) + ATUS(leisure) +
O*NET/EdNet(work/learning) + SCF/CEX(finance) + PersonaHub seeds + WildChat style — all 🟢.

---

## 5. Turning a data row into a deep persona — the pipeline (`persona_seed.py`)

For work/learning **right now** (your blocker), and generalizable to all domains:

```
STEP 1  DRAW BACKBONE ROW
        sample 1 respondent from MIDUS/UKHLS (or NLSY for work-arc) → structured fields
        e.g. {age:34, occ_code:"15-1252 software dev", income_band, education, health_flags,
              big_five, weekly_hours, sleep_hours, ...}

STEP 2  ELABORATE → PERSONA CARD  (LLM)
        translate fields to natural person + split PersonaMem-style:
        - STATIC (never change): name, age, occupation, background
        - DYNAMIC (revealable/updatable): preferences, habits, current goals, constraints
        attach VOICE seed from WildChat/DailyDialog register

STEP 3  LAYER DOMAIN TEXTURE  (real vocabulary, not model-invented)
        work    → O*NET real task/skill strings for occ_code; SO-survey real tool names
        learning→ EdNet/OULAD study-behavior pattern
        (diet→Food.com/NHANES foods; hobby→LFM/Steam titles; finance→SCF/CEX items)

STEP 4  BUILD EVENT-GRAPH TIMELINE  (LoCoMo-style)
        ~15-25 causal life events over 6-12 months that will surface the
        associative evidence pair (E_A, E_B) + distractors, on a reveal schedule

STEP 5  GENERATE MULTI-SESSION DIALOGUE over the timeline, persona persisted,
        Generator-Critic faithfulness check per session (Synthetic-Persona-Chat)

STEP 6  AUDIT (prepare.py D1-D8 + INVERSION>0.20) → keep/repair
```

Output of Steps 1–3 = a reusable **persona JSON** (static/dynamic + texture). This is
the artifact that makes the generator "truly know the person," and it scales N far
beyond your own personal data.

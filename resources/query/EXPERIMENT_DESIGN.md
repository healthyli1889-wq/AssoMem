# Experiment Design — plain-language spec (v2)

> Read this top to bottom and you can run the whole experiment. No prior context needed.
> Every term is defined the first time it appears. Companion files: METRICS.md (the exact
> formulas), QUERY_STANDARD.md (how each question is written), WORKABILITY.md (the per-item
> ablation variants).

---

## 1. What we are proving (in one breath)

We built a memory test for AI assistants. Each test item is a long chat history between a
user and an assistant, plus one final question. To answer that question correctly, the model
has to **connect two separate things the user said in earlier sessions** — neither fact alone
is enough, and general knowledge doesn't help. We call that skill **associative memory**.

The experiment answers three questions, in order:
1. **Can the model answer at all** when it has the full history?
2. **Does it actually use its memory**, or is it guessing from common sense?
3. **Does it truly connect the two facts**, or is it just lucky that both facts are lying
   around nearby?

Question 3 is the whole point. A model can have both facts in front of it and still fail to
*link* them. Our design isolates exactly that.

---

## 2. The one rule every question obeys

A question is a valid associative-memory question **only if the correct answer appears ONLY
when both facts are present** — not from priors, not from either fact alone.

We check this by feeding a model four versions and looking at its answer:

| What the model sees | Should it get the right answer? |
|---|---|
| Just the question (no history) | **No** — if yes, it's answerable by common sense → throw the question out |
| Only fact A | **No** — if yes, it's a one-fact question → throw it out |
| Only fact B | **No** — if yes, same problem → throw it out |
| Both fact A and fact B | **Yes** ✅ — this is what makes it associative |

If a question passes this table, it's a real associative question. Everything else in this
doc is about running it cleanly and measuring it.

(Two special question kinds flip the rule: **absence** questions ship with the facts
*missing* and the right answer is "I don't have enough to say"; **source** questions change
the right answer depending on *who* said the fact — you vs. a friend. More in §4.)

---

## 3. What one test item looks like

```
- A chat history: 12–16 sessions, most of them small talk ("filler").
- Two of those sessions each hold one key fact (fact A, fact B), placed far apart,
  never in the last two sessions.
- At least one "distractor" session: something that looks relevant and tempts a wrong
  answer, but is off-track.
- A final question the user asks.
- The question comes in two answer formats (we score both):
    · MULTIPLE CHOICE (4 options) — see the 2×2 below.
    · TRUE / FALSE — a one-line claim the model marks true or false.
- The gold answer + a short list of "required elements" the answer must contain.
```

**The 4 multiple-choice options are a 2×2** — each wrong option tells us *which* mistake the
model made:

| Option | Uses fact A? | Uses fact B? | Picking it means the model… |
|---|---|---|---|
| **A (correct)** | yes | yes | connected both facts ✅ |
| **B** | no | no | guessed from common sense / surface words |
| **C** | yes | no | grabbed only fact A, didn't connect |
| **D** | no | yes | grabbed only fact B, didn't connect |

Worked example (a hobby item):
- Fact A (session 2): "I love slow, patient cooking; fast high-heat stuff stresses me out."
- Fact B (session 6): "I want a hands-on hobby I can do on my balcony."
- Question (final turn): "There's a weekend workshop fair — which should I go for?"
  - A: bonsai workshop → slow ✅ + balcony ✅ → **correct**
  - B: wok stir-fry class → fast, kitchen → common-sense "you like cooking" trap
  - C: sourdough baking → slow but kitchen → used only fact A
  - D: fast-turnover balcony microgreens → balcony but fast → used only fact B
- True/False version: *"I should sign up for the bonsai workshop." → True.*

---

## 4. The seven "conditions" we run each item under (the arms)

An **arm** = one version of the item we feed the model. We run every item under several arms
and compare the scores. This is the engine of the whole experiment.

| Arm | What we change | What comparing it tells us |
|---|---|---|
| **FULL** | nothing — the real item | the baseline score |
| **no-target** | delete the two fact sessions | did the answer actually depend on memory? |
| **broken-link** | keep both facts, but move fact A into person X's history and fact B into person Y's — same words, different owners, so they can't be linked | **did the model need to CONNECT them?** ← the key arm |
| **no-distractor** | delete the tempting distractor | was the distractor actually fooling it? |
| **restore** | put the deleted sessions back | sanity check: score should bounce back |
| **add-evidence** (absence items only) | insert the missing facts | the "I don't know" answer should now become a real answer |
| **source-swap** (source items only) | re-label a fact as said by a friend | the right answer should change |

**Why broken-link is the star.** Removing the facts (no-target) tells you the model needs the
facts. But a model that just retrieves both facts and pastes them side by side isn't really
*associating* — it might get lucky whenever both are nearby. broken-link keeps both facts
present but makes them un-linkable (they belong to different people now). If the score still
drops, the model genuinely needed to *bind* them. That drop is our headline evidence.

---

## 5. The seven numbers we report (the metrics)

Plain definitions. Exact formulas live in METRICS.md.

| Metric | Plain meaning | Built from which arm(s) |
|---|---|---|
| **REA** (Required-Element Accuracy) | Did the answer contain **every** required piece? All-or-nothing per item, then averaged. This is "the score." | FULL |
| **Δ_mem** (memory dependence) | How much the score drops when we delete the facts. Big drop = it really used memory. | FULL minus no-target |
| **Δ_assoc** (association dependence) ★ | How much the score drops when the facts are present but un-linkable. Big drop = it really connected them. **The number the paper rests on.** | FULL minus broken-link |
| **JER** (Joint Evidence Recall) | Did the model's reasoning actually mention BOTH facts (not just land on the right answer by luck)? | FULL |
| **DIR / FoolRate** | Does a tempting distractor flip a right answer to wrong? (robustness) | FULL vs no-distractor |
| **AbC** (Abstention Correctness) | On absence items, does it correctly say "not enough info" instead of making something up? | absence items |
| **SAA** (Source Attribution Accuracy) | Does it get the answer right for both "you said it" and "a friend said it"? | source-swap |

**Δ_mem and Δ_assoc are not separate measurements — they are just subtractions** between the
arm scores. So the primary thing we report is the plain REA under each arm; the deltas fall
out of those.

---

## 6. The models we test (3 systems = 3 rows)

We put three open models through the exact same items, each with the full chat history in its
context:
- **GPT-oss-20b**
- **Gemma-4-31b**
- **Qwen-3.6-35b**

They are the **rows** of the results table. (This first table holds the "memory approach"
fixed — full history in context — and varies the base model. A second table, later, can hold
the base model fixed and vary the memory approach: plain long-context vs. retrieval vs. a
memory agent. Don't mix the two in one table.)

**Running protocol (do this literally):**
```
1. Freeze the dataset. No edits after this point.
2. For each model, for each item, for each arm (FULL, no-target, broken-link,
   no-distractor, restore, + add-evidence/source-swap where they apply):
      - feed the chat history for that arm + the question (both MCQ and TF formats)
      - record the raw answer. Do not grade yet.
   Temperature 0. One pass. Save everything.
3. Grade all recorded answers (see §7).
4. Compute the metrics per (model × question-type × arm).
```
Grade *after* collecting, so grading is uniform and re-runnable.

---

## 7. How we grade an answer

We do **not** hand the model the gold answer to grade against itself. We grade like this:

1. Each item ships a short list of **required elements** (e.g. "cites the slow-cooking taste",
   "cites the balcony wish", "picks bonsai"). An answer is correct only if it hits **all** of
   them — that's REA.
2. Two independent **judge models** each read the answer and mark each required element
   yes/no, against the gold. We report how much the two judges agree (**Cohen's κ**); κ ≥ 0.6
   or we fix the rubric.
3. Multiple choice is graded automatically (did it pick option A?). True/False the same.
   Free-text answers go through the two judges. The three views should agree; disagreements
   get flagged.

The judges are **auditors with a checklist**, not free reasoners. They must not reward long
or fluent answers, must not fill gaps with world knowledge, and must not see the author's
hidden labels. (Full judge-validation loop — a 60-item calibration set of known-good,
known-bad, and adversarial answers, plus bias checks — is in §9 and unchanged from v1.)

---

## 8. What the results table looks like

Rows = the 3 models. Columns = the score under each arm, then the two subtractions. Every cell
is `REA [95% confidence interval]`.

| Model | FULL | no-target | broken-link | Δ_mem (FULL−no-target) | Δ_assoc (FULL−broken-link) |
|---|---|---|---|---|---|
| GPT-oss-20b | .72 [.60,.83] | .31 [.20,.43] | .43 [.31,.55] | .41 ✓ | .29 ✓ |
| Gemma-4-31b | … | … | … | … | … |
| Qwen-3.6-35b | … | … | … | … | … |

*(numbers illustrative; ✓ = the drop's confidence interval doesn't include 0, i.e. it's real.)*

**How to read one row, left to right:** high FULL = it can answer → drops near chance at
no-target = it used memory, not common sense → still drops at broken-link even though both
facts are present = it truly connected them. Three drops = genuine associative memory.

A **second small table** holds the other four metrics (JER, DIR/FoolRate, AbC, SAA), one
column each, one number per model.

**Reporting rules:**
- Report the score under each arm with a **95% confidence interval** (bootstrap over the
  ~50 items). With only ~50 items and 3 models, without the interval you can't tell a real
  gap from noise.
- The two deltas get a **paired** confidence interval; "significant" means that interval
  excludes 0. That single fact is the evidence for questions 2 and 3 from §1.
- Don't headline a ± standard deviation for a pass/fail rate; if you want to show spread,
  show the histogram of "how many facts did it cite" (0, 1, or 2).

---

## 9. Proving the benchmark itself is fair (not just the models)

A skeptic will ask: maybe the questions are broken, not the models. We answer with four
checks, reported alongside the main table:

1. **Spread across models** — the three models should get visibly different scores. If they
   all score the same, the items don't separate anyone → the ruler is too blunt.
2. **Human ceiling** — a person given the full history should score high (say ≥ .90). If
   humans can't do it either, the question is unfair, not hard.
3. **Judge agreement (κ)** — the two auto-judges agree with each other and with a human
   sample at κ ≥ 0.6.
4. **Per-item validity gates** (run *before* an item ships):
   - The four-row table in §2 comes out clean.
   - The distractor is genuinely tempting: under a standard retriever, the distractor is
     *more* retrievable than the real facts (we call the margin **INVERSION**; require it > 0.20).
     A distractor nobody would retrieve isn't doing its job.
   - The question doesn't echo the facts' wording (embedding similarity < 0.15).
   - Deleting either fact changes the answer (both facts are load-bearing).
   Any item failing a gate is fixed or dropped.

**Judge trust, in full.** We don't just use the judges — we test them on a 60-item bench:
20 known-good answers they must accept, 20 known-bad (fluent-but-wrong, terse-but-right,
world-knowledge-only, one-fact-guess) they must sort correctly, and 20 adversarial
(right answer with a fake citation, or a distractor dressed up as the answer) they must catch.
We also swap answer order and pad answers with filler to confirm the judge isn't fooled by
position or length. We keep patching the judge's checklist until it clears κ ≥ 0.6 and stays
consistent across reruns, then freeze it. The paper reports these judge numbers — most memory
benchmarks report an auto-judge score with no proof the judge works; we show the proof.

---

## 10. The whole thing, first step to last

```
1.  Define the skill  → the four-row rule in §2.
2.  Source real people → whole-person profiles (see PERSONA_DATA_STRATEGY.md), so the facts
                         we bind are genuine, not invented.
3.  Write the questions → each obeys §2, ships MCQ + TF + required elements
                         (see QUERY_STANDARD.md). ~50 per profile domain.
4.  Build the arms     → for every item, generate no-target, broken-link, no-distractor,
                         restore (+ add-evidence / source-swap where relevant).
5.  Pass the gates     → §9 item checks; fix or drop failures.
6.  FREEZE the dataset.
7.  Run the 3 models   → every item, every arm, both formats, temp 0, save raw outputs.
8.  Grade              → two judges + auto-scoring; check κ.
9.  Compute metrics    → REA per arm, then Δ_mem and Δ_assoc by subtraction, plus JER, DIR,
                         AbC, SAA; attach 95% confidence intervals.
10. Fill the table     → 3 models × arms; read the three-drop story (§8).
11. Report validity    → spread, human ceiling, judge κ (§9).
12. Write the findings → who's best, whether memory helps, whether models truly associate,
                         and where they fail (using JER, the cite-count histogram, and DIR).
```

Steps 1–6 build the ruler. Steps 7–12 use it. If step 11 fails, the step-10 numbers don't
count — so validity comes before leaderboard.

---

## Appendix — which confound each design choice kills (for reviewers)

| The cheap shortcut a model might use | What blocks it |
|---|---|
| Answer from general knowledge | §2 rule: question is person-specific; empty-history run must fail |
| One fact already contains the answer | §2 rule + no-target arm: one-fact runs must fail |
| Both facts nearby, no real linking | **broken-link arm + Δ_assoc** — the core defense |
| Matching the question's words to the facts | similarity gate < 0.15 (§9) |
| Just reading a huge context | history capped below long-context size; no-target/oracle arms |
| Answering with the last/most recent thing | facts placed early/mid, never last two sessions |
| Looking good only because nothing competes | tempting distractor with INVERSION > 0.20 (§9) |
| A fluent-but-wrong answer scored as right | two validated judges + required-element checklist (§7, §9) |

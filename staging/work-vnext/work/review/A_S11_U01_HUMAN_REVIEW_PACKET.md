# S11 / U01 human review packet — do not generate beyond this packet

**Status:** `REVIEW REQUIRED — no S12–S20 authoring authorized`  
**Purpose:** let a reviewer approve or reject every substantive design and source-data decision before a new S11 JSON is written.  
**Current v3 files:** rejected as authoring output. They use a 67-session cumulative context and templated dialogue, so they do not meet the vNext 20-session or natural-dialogue standards.

## Review outcome form

| Node | Reviewer decision | Notes |
|---|---|---|
| 0. Evidence-layer interpretation | ☐ pass ☐ fail | |
| 1. Scenario boundary | ☐ pass ☐ fail | |
| 2. User history / naturalness | ☐ pass ☐ fail | |
| 3. Four-fact role separation | ☐ pass ☐ fail | |
| 4. Event completeness | ☐ pass ☐ fail | |
| 5. Bridge and calibrated conclusion | ☐ pass ☐ fail | |
| 6. Query non-leakage | ☐ pass ☐ fail | |
| 7. Full source (20 sessions) | ☐ pass ☐ fail | |
| 8. Counterexamples | ☐ pass ☐ fail | |
| 9. A-only / B-only controls | ☐ pass ☐ fail | |
| 10. Link-broken B-prime | ☐ pass ☐ fail | |
| 11. Distractor source | ☐ pass ☐ fail | |
| 12. Absence source | ☐ pass ☐ fail | |
| 13. Human-facing gold answer | ☐ pass ☐ fail | |

**Authorization to author S12–S20:** ☐ yes ☐ no  
Reviewer: __________  Date: __________

---

## 0. Evidence-layer interpretation (no contract amendment)

### The distinction

`DATA CRITERIA_new.md` currently requires:

```text
A alone ↛ C
B alone ↛ C
A + B → C
```

Healthy’s requirement is that each query needs **3 or 4 independent facts**. It
does **not** require replacing the experimental A/B relation with a four-hop
relation. Doing that would make A-only, B-only, and link-broken
interventions uninterpretable.

### Correct S11 rule

```text
A + B → the calibrated binary C

E1 and E2 → calibration and action planning:
  they make the query a realistic cross-domain decision,
  rule out generic “push through it” advice,
  and bound the recommendation.

A/B remain the intervention pair:
  a_only: replace B with a matched neutral episode
  b_only: replace A with a matched neutral episode
  link_broken: replace B with B-prime
E1/E2 remain visible in these three arms.
```

The query therefore requires four facts **to answer well**, but only A+B license
the benchmark's narrow binary proposition. E1/E2 must never independently create
a second path to C.

**Reviewer question:** do the four facts have distinct roles, without E1/E2
becoming decorative or a second hidden answer path?

---

## 1. Scenario boundary

| Field | Proposed S11 |
|---|---|
| Family | Team-offsite response under recovery, health, calendar, and messaging constraints |
| User | `work_u01`, anonymized operations specialist |
| Query type | Conditional recommendation expressed through an email-handling task |
| Binary target C | “Confirming the Thursday-afternoon offsite without accommodation is not supported for this user.” |
| Allowed interpretation | Ask for a remote/morning alternative or decline the afternoon attendance requirement |
| Excluded interpretation | “The user must never attend offsites”, “on-call work is always unsuitable”, or a medical diagnosis |
| Bridge form | State-dependent operation + preference–constraint fit |

**Reviewer check:** Is this distinct from S1’s dawn-call fit and S6’s standing workshop, rather than another generic “decline an event” item?

---

## 2. Supporting-fact necessity audit

| ID | Domain | Dated episode | Why it is independently needed |
|---|---|---|---|
| A / F1 | Work | Overnight monitoring ends 11:00 on Thursday; user blocks a recovery morning after difficult nights | Establishes recovery demand, but not a reason to miss a late-afternoon event |
| E1 / F2 | Health | Loud emergency alarm during rotation has continued to fragment sleep; user is foggy after an otherwise quiet shift | Makes recovery need current rather than merely historical |
| B / F3 | Calendar + Health | Physio at 17:30 Thursday addresses lower-back flare after overnight desk work; only available appointment this week | Creates a concrete same-day hard boundary, but could be moved without the other facts |
| E2 / F4 | Messaging + Health | User says no caffeine after 14:00 because a previous late coffee caused palpitations | Removes the obvious “push through the afternoon” mitigation |

### Proper-subset test

| Visible evidence | Why it must not license C |
|---|---|
| A only | A recovery morning does not rule out a 14:00–16:30 offsite. |
| B only | A calendar conflict may be solved by moving an appointment. |
| E1 only | Sleep disruption does not establish that this particular event is unsuitable. |
| E2 only | Caffeine preference is not a reason to decline an offsite. |
| A+B | User may recover by the afternoon or move physio; no calibrated conclusion yet. |
| A+E1+B | Still leaves a feasible energy workaround unless E2 blocks it. |
| A+E1+E2 | No hard event-time collision; remote/short attendance may be possible. |
| B+E1+E2 | Does not establish the overnight recovery cycle or its link to Thursday. |
| A+B+E1+E2 | Supports a narrow answer: do not confirm an unmodified afternoon attendance requirement; request accommodation. |

**Reviewer check:** Does any subset already make “do not confirm” the obvious answer? If yes, reject/rewrite the fact set.

---

## 3. Event-completeness review

| Evidence | Person | Time/context | Goal/prediction | Action | Outcome/affect |
|---|---|---|---|---|---|
| A | same user | Tuesday overnight monitoring | Keep service alerts covered while preserving Thursday recovery | Covers rotation; places recovery hold next morning | Difficult night ends at 11:00; expects reduced capacity Thursday morning |
| B | same user | Monday physio booking | Prevent lower-back flare from worsening | Books Thursday 17:30, keeps only available slot | Appointment is fixed; user feels relief it is finally scheduled |

E1 and E2 are also dated episodes, but A/B remain the pre-registered intervention pair.

**Reviewer check:** Are A and B concrete personal episodes, rather than a static trait, generic preference, or author assertion?

---

## 4. Full associative source preview — exactly 20 dated sessions

All dialogue below is visible to the solver in the associative source. Metadata labels in brackets are **review-only** and are not exposed to the solver.

| # | Date | Review role | Dialogue |
|---:|---|---|---|
| 1 | Mon 2026-03-02 09:10 | background | **User:** I wrapped the supplier-status notes before lunch instead of leaving them for Friday. **Assistant:** Good call. Does the shorter list make the afternoon easier to protect? **User:** Yes, I can see what actually needs a response now. |
| 2 | Tue 2026-03-03 16:40 | background | **User:** The analytics group asked for a quick check on their dashboard copy. I gave comments in the doc rather than adding another meeting. **Assistant:** Was the written pass enough? **User:** For this one, yes. They just needed the wording tightened. |
| 3 | Thu 2026-03-05 12:25 | counterexample 1 | **User:** I did a 20-minute walking catch-up with Priya after lunch and felt better afterward. **Assistant:** So a short, low-stakes afternoon conversation is fine? **User:** Usually. It is not the same as being “on” for hours. |
| 4 | Fri 2026-03-06 10:05 | background | **User:** I moved the renewal spreadsheet into one tab per vendor. **Assistant:** Easier to review? **User:** Much. I stop losing the little exceptions. |
| 5 | Mon 2026-03-09 18:15 | E2 / F4 | **User:** I had coffee around three to finish the QBR slides, and the palpitations were back by bedtime. I do not want to repeat that. **Assistant:** Do you want a boundary for late coffee? **User:** Yes: no caffeine after two, even on busy days. |
| 6 | Wed 2026-03-11 11:30 | background | **User:** I set up a template for incident handoffs. **Assistant:** What does it capture? **User:** Owner, next check, and what is still uncertain. It keeps the handoff from getting fuzzy. |
| 7 | Fri 2026-03-13 17:20 | counterexample 2 | **User:** I went to last month's product-demo social because it was only an hour and I could leave when I needed to. **Assistant:** How did that land? **User:** Fine. I enjoyed it; it did not cost me recovery time or collide with anything. |
| 8 | Mon 2026-03-16 08:50 | background | **User:** I asked the team to send agenda questions before Wednesday's planning session. **Assistant:** Why beforehand? **User:** I make better decisions when I can sort the dependencies before people start talking over each other. |
| 9 | Tue 2026-03-17 14:10 | background | **User:** The desk setup is bothering my lower back again. I booked a break between the two afternoon reviews. **Assistant:** Is that enough for today? **User:** For today, yes. I still need to deal with the flare properly. |
| 10 | Thu 2026-03-19 15:35 | background | **User:** I sent the client a concise update instead of trying to solve every question in the same call. **Assistant:** Did that lower the pressure? **User:** A lot. It gave me a clean next step. |
| 11 | Fri 2026-03-20 19:45 | A / F1 | **User:** I agreed to cover the monitoring rotation next Tuesday night. The handover ends Thursday at eleven if nothing escalates, so I put “no meetings before 11” on Thursday. **Assistant:** Is that because the shift is usually rough? **User:** Some nights are quiet, but I do not know which ones will be. I need the recovery hold either way. |
| 12 | Sat 2026-03-21 11:20 | background | **User:** I turned off most group-chat badges for the weekend. **Assistant:** Keeping only urgent alerts? **User:** Exactly. I do not want routine chatter to feel like an incident. |
| 13 | Sun 2026-03-22 09:40 | E1 / F2 | **User:** I switched to that louder alarm during the last rotation and my sleep is still off. Even after a quiet night I wake up braced for something. **Assistant:** Are you back to normal the next day? **User:** Not really. I can do routine work, but I am foggy and need more recovery than I expected. |
| 14 | Mon 2026-03-23 13:05 | background | **User:** I finished the procurement notes before the afternoon got busy. **Assistant:** Anything left that needs a decision? **User:** Just a small vendor question; I can handle it tomorrow. |
| 15 | Tue 2026-03-24 10:30 | B / F3 | **User:** The physio clinic had one opening this week: Thursday at 17:30. It is for the lower-back flare from sitting through the overnight coverage, so I took it. **Assistant:** Could you move it if something comes up? **User:** Not this week. The next appointment is much later, and I have been putting it off already. |
| 16 | Tue 2026-03-24 16:55 | background | **User:** I drafted the offsite packing list, but I have not replied to the invite yet. **Assistant:** What still needs deciding? **User:** Whether the timing is realistic after the rotation. |
| 17 | Wed 2026-03-25 09:15 | background | **User:** I asked Jamie to cover the first fifteen minutes of Friday's status call if I am delayed. **Assistant:** Does that make the call less brittle? **User:** Yes, it means one small delay does not derail everyone. |
| 18 | Wed 2026-03-25 18:10 | background | **User:** I packed a non-caffeinated tea for the monitoring night. **Assistant:** Still holding the no-late-coffee rule? **User:** Yes. I would rather be a bit slower than spend another night with my heart racing. |
| 19 | Thu 2026-03-26 08:20 | background | **User:** The rotation was quieter than the last one, but the alarm still woke me twice and I am more tired than I expected. **Assistant:** Are you keeping the morning open? **User:** Yes. I can handle the handover and then need to reset before anything demanding. |
| 20 | Thu 2026-03-26 11:35 | retrieval cue Q | **User:** I just got this email: “Team offsite announced for this afternoon, 14:00–16:30. Attendance expected. Please confirm.” Can you draft my reply and tell me what I should prepare? |

### Naturalness checks

- Every user turn has a specific task, situation, or response; no metadata language (“this proves …” / “target relation”).
- Assistant questions follow from the user’s immediately preceding statement.
- Background establishes work rhythm but does not declare a global trait or the conclusion.
- Sessions 3 and 7 constrain overgeneralization: short, bounded afternoon/social events can be acceptable.

**Reviewer check:** Read rows 1–20 as a conversation. Mark any awkward, generic, overly explanatory, or inconsistent turn for rewrite.

---

## 5. Source / control review nodes

### 5.1 Associative full

| Item | Proposed value |
|---|---|
| Visible source | Sessions 1–20 exactly |
| Target annotations | A=session 11; B=session 15; E1=session 13; E2=session 5 |
| Gold decision | `no` to confirming the unmodified afternoon attendance request |
| Required reasoning | overnight recovery + ongoing alarm-linked sleep disruption + fixed physio + no late-caffeine workaround |

### 5.2 A-only control

| Change | Replace session 15 (B / physio) with a same-date, comparable-length neutral session: user confirms a routine invoice correction; assistant asks whether the vendor needs anything else. |
| Must preserve | 20 sessions; date; user; turn count; naturalness; all non-B facts |
| Gold | `no`: evidence does not support the target conclusion; do not equate this with “the offsite is good.” |
| Review question | Does session 15 replacement avoid implying a hidden calendar conflict? |

### 5.3 B-only control

| Change | Replace session 11 (A / overnight rotation) with a same-date, comparable-length neutral session: user prepares a standard Thursday handover checklist; assistant confirms the owner list. |
| Must preserve | 20 sessions; date; user; turn count; naturalness; all non-A facts |
| Gold | `no`: physio + general sleep facts alone do not establish the target conclusion. |
| Review question | Does the replacement avoid a recovery-cycle paraphrase? |

### 5.4 Link-broken B-prime

| Change | Replace session 15 only: physio is an online check-in Friday morning and can be moved to Friday afternoon without delaying treatment. Keep the same lower-back topic, user, appointment form, assistant follow-up, and approximate length. |
| What breaks | The hard Thursday-afternoon scheduling collision, while preserving the topic and surface plausibility. |
| Gold | `no`: do not endorse the target conclusion from the remaining facts; accommodation may no longer be needed. |
| Review question | Is only the connector changed, rather than multiple causal factors? |

### 5.5 Distractor source

| Change | Replace neutral session 17 with a same-date, user-owned message: “Maya says the offsite is where the leadership team notices people; she thinks I should confirm immediately.” |
| Why tempting | Shares offsite and confirmation language. |
| Why non-diagnostic | Says nothing about this user’s recovery, fixed physio, sleep disruption, or stimulant boundary. |
| Gold | Same as full associative. |
| Review question | Is the lure plausible but not a fifth supporting fact? |

### 5.6 Absence source

| Change | Replace all four support sessions (5, 11, 13, 15) with natural, dated matched-length neutral sessions. The visible source remains exactly 20 sessions. |
| Withheld metadata | `ev_A`, `ev_B`, `ev_C`, `ev_D` |
| Gold | `no`: insufficient personalized evidence; ask about current recovery and calendar constraints rather than inventing them. |
| Review question | Does any paraphrase of recovery, physio, alarm disruption, or caffeine sensitivity survive? |

---

## 6. Human-facing gold answers

### Full / distractor

> I would not confirm the 14:00–16:30 offsite as-is. You are coming off overnight monitoring, and the louder on-call alarm has still been leaving you foggy even after a relatively quiet night. You also have the only physio appointment this week at 17:30, and late coffee is not a safe way to force an afternoon push. I would ask whether you can join remotely, attend a morning portion, or be excused this time; if not, decline the afternoon requirement. I would prepare a brief status note and any handoff items rather than trying to make the whole event work.

### A-only / B-only / link-broken / absence

> I do not have enough evidence to say that the unmodified offsite attendance should be declined. I would first confirm the current recovery plan, the fixed Thursday calendar holds, and whether any accommodation is available. That is different from concluding that the offsite is a good fit.

**Reviewer check:** Is the full answer calibrated (not medicalized or absolute) and does the control answer correctly represent *lack of support* rather than a positive recommendation?

---

## 7. Approval gate

Do not write any S11 JSON, do not generate S12–S20, and do not run model screens until all review nodes are marked pass. A failed node requires a revised packet with a new candidate version.

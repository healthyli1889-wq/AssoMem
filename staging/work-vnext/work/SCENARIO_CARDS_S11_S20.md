# Work domain — S11–S20 scenario cards (vNext redesign)

**Status:** Gate 0 cards + v3 JSON written under `assomem/src/data/work/` (S11–S20 only). Human Gate 0/1 still open.
**Procedure:** `GENERATION_PLAN.md`
**Contract sources:** `DATA CRITERIA_new.md` + Healthy pre-3k feedback (2026-07-23).
**Compared against:** legacy ladder `src/data/work/SCENARIOS_S1_S20.md` S1–S10.
**Batch:** `WL_GOLD_S11_S20_2026-07-24_v3` (300 files; legacy S11–S20 archived).

## Design deltas vs S1–S10 (batch-level)

| Axis | S1–S10 (legacy ladder) | S11–S20 (this redesign) |
|---|---|---|
| Critical evidence count | Exactly 2 (`ev_A`, `ev_B`) | **3 or 4 independent facts**; never exactly 2 |
| Domains of facts | Usually same work/learning stream | Facts spread across ≥3 of Work / Health / Calendar / Messaging |
| Query form | Often “Worth joining X?” close to C | Situational task cue (email, invite, nomination) that does **not** paraphrase C |
| Insufficiency | A alone / B alone claimed, but B often nearly sufficient | Any proper subset of the fact set fails; only full set + R supports C |
| Bridge types | Mostly “decline / protect calendar” | Must map to criteria forms 1–5 |
| Polarity | Near-uniform reject | Mix of reject / conditional / accept-with-guardrail (binary yes/no at eval) |
| B-prime | Often format/source swap risk | Environment-specific connector break only |

### Fact-set rule (mandatory for every S11–S20 item)

```text
supporting_facts = 3 or 4 independent, same-user episodic facts
critical_pair ⊂ supporting_facts   # size 2; A and B for ablation rendering
extra_constraints = supporting_facts \ critical_pair   # size 1 or 2

A alone ↛ C
B alone ↛ C
any 2-of-3 or 3-of-4 subset ↛ C   # when N≥3
full set + R → C
full set with B-prime ↛ C
```

Ablations still render **matched 20-session** contexts: A-only / B-only replace the critical pair members; extras remain visible unless a dedicated control says otherwise.

---

## S11 — `offsite_confirm_x_recovery_stack`

| Field | Content |
|---|---|
| Work-demand family | Confirm / decline an announced team offsite under stacked recovery + health + calendar constraints |
| Bridge type | Preference–constraint fit + state-dependent operation |
| Facts (4) | **F1 Work:** overnight monitoring rotation ends mid-morning on offsite day. **F2 Health:** ongoing sleep disruption after louder alarms. **F3 Calendar:** physio 17:30 same afternoon. **F4 Messaging/Health:** avoids late caffeine after palpitations. |
| Critical pair | F1 (A), F3 (B); extras F2, F4 tighten recovery/energy reading |
| Query (not C) | Email: “Team offsite announced for next Thursday afternoon. Attendance expected. Please confirm.” — handle response and prep. |
| Latent C | Confirming attendance as-is is not supported; response should request schedule accommodation or decline the afternoon block. |
| Why subset fails | F1 alone → maybe tired, still could attend. F3 alone → calendar clash only. F1+F3 without F2/F4 → clash solvable by moving physio. Full stack → recovery + clash + energy limit. |
| B-prime | Physio becomes a flexible telehealth slot movable to Friday; connector “hard same-afternoon clash” breaks. |
| Diff vs S1–10 | Not dawn-checkin (S1) or standing workshop (S6); multi-domain offsite confirmation like MemoryQuest user15. |

---

## S12 — `demo_rehearsal_x_voice_clarity_stack`

| Field | Content |
|---|---|
| Work-demand family | Accept stacked lens-on rehearsals before a fixed client demo |
| Bridge type | State-dependent operation |
| Facts (4) | **F1 Work:** back-to-back video days leave next-day presentation voice strained. **F2 Calendar:** client keynote dry-run Thursday 09:00 is fixed. **F3 Health:** allergy meds cause morning fog unless sleep is protected. **F4 Work:** async memo prep preserves clarity without voice load. |
| Critical pair | F1 (A), F2 (B) |
| Query | PM: “Can we add two consecutive lens-on rehearsal blocks Wednesday for Thursday’s client dry-run?” |
| Latent C | Adding consecutive Wednesday lens-on blocks is not supported; keep async prep and at most one short sync. |
| Why subset fails | F2 alone → need prep, not which kind. F1 alone → avoid video in general (overbroad). F1+F2 without F3/F4 → might still choose live drills. |
| B-prime | Dry-run moves to Friday; Wednesday video no longer threatens the fixed slot. |
| Diff vs S1–10 | Not live-panel moderation (S8); rehearsal load × protected demo day with health/async extras. |

---

## S13 — `apac_verbal_handoff_x_uncertainty_doc`

| Field | Content |
|---|---|
| Work-demand family | Immediate verbal ownership of ambiguous APAC handoffs |
| Bridge type | Prediction calibration / strategy–outcome contingency |
| Facts (3) | **F1 Work:** calibrated ownership only after writing observed vs inferred vs unconfirmed. **F2 Work:** prior forced verbal ownership before logs caused wrong rollback. **F3 Calendar:** only available overlap is 06:00–06:25 APAC bridge. |
| Critical pair | F1 (A), F2 (B); F3 is the demand slot |
| Query | Partner lead: “Can you take the 06:00 APAC verbal handoff ownership this week when logs may still be incomplete?” |
| Latent C | Accepting pure verbal 06:00 ownership under incomplete evidence is not supported; require a written uncertainty handoff first. |
| Why subset fails | F1 alone → preference, not failure under demand. F2 alone → one bad incident, maybe fixed. F3 alone → early meeting inconvenience only. |
| B-prime | Prior failure attributed to missing ticket attachment restored later; same verbal form then succeeded. |
| Diff vs S1–10 | Closest to escalation ownership (vNext S2), not in legacy S1–10; distinct from night-alert rotation (S5). |

---

## S14 — `audit_hotdesk_x_quiet_draft`

| Field | Content |
|---|---|
| Work-demand family | Hot-desk / floor-hopping during compliance draft week |
| Bridge type | Strategy–outcome contingency |
| Facts (4) | **F1 Work:** open-office hot-desk destroys dense policy-draft focus. **F2 Calendar:** quiet compliance memo due Wednesday needs deep writing block. **F3 Work:** VPN migration Tuesday breaks reliable home quiet setup. **F4 Messaging:** audit war-channel floods with non-actionable pings during draft windows. |
| Critical pair | F1 (A), F2 (B) |
| Query | Facilities: “Please hot-desk Tue–Wed this week for the audit visibility walk.” |
| Latent C | Hot-desking through Wednesday draft window is not supported; protect a quiet remote (or booked room) block for the memo. |
| Why subset fails | F2 alone → need focus time, location underspecified. F1 alone → avoid office always (overbroad). Without F3/F4, alternate quiet desks may look fine. |
| B-prime | Memo deadline moves to Friday after VPN stabilizes; Tue–Wed hot-desk no longer collides with draft connector. |
| Diff vs S1–10 | Extends hot-desk idea beyond S14-legacy clones; adds VPN + channel flood so two facts never suffice. |

---

## S15 — `sev1_warroom_lead_x_overnight_debt`

| Field | Content |
|---|---|
| Work-demand family | Lead a night Sev-1 war room after recovery debt |
| Bridge type | State-dependent operation + threshold/context interaction |
| Facts (4) | **F1 Work:** reliable live prioritization only after writing a dependency map. **F2 Work:** prior map-less early live call misordered interdependent incidents. **F3 Work/Health:** overnight rotation left multi-day sleep debt. **F4 Health:** late caffeine avoided due to palpitations (limits night alertness aids). |
| Critical pair | F1 (A), F2 (B) |
| Query | Incident commander nomination: “Lead Thursday 22:00 Sev-1 war room; expect live priority calls without a prep doc.” |
| Latent C | Accepting that nomination as stated is not supported; require prep map and/or a non-overnight slot after recovery. |
| Why subset fails | F2 alone ≈ B-sufficiency trap if query names live priority failure — avoided by keeping query as nomination + “no prep doc.” F3 alone → tiredness. F1+F2 without F3/F4 → daytime war room with map might be fine. |
| B-prime | Prior misorder caused by duplicated dashboard row; after fix, map-less call succeeded. |
| Diff vs S1–10 | Not generic on-call join (S5); war-room lead × map strategy × overnight debt. |

---

## S16 — `hiring_panel_marathon_x_judgment_block`

| Field | Content |
|---|---|
| Work-demand family | Consecutive hiring panels before a judgment-heavy review |
| Bridge type | Threshold/context interaction |
| Facts (3) | **F1 Work:** decision quality drops sharply after the third consecutive panel. **F2 Calendar:** architecture review Friday needs sharp comparative judgment. **F3 Health:** standing-flare limit — panels without sit breaks tighten back next morning. |
| Critical pair | F1 (A), F2 (B) |
| Query | Recruiting: “Can you take five consecutive Thursday panels? We are behind on the pipeline.” |
| Latent C | A five-panel Thursday marathon is not supported before Friday’s architecture review; cap at two–three with breaks or split days. |
| Why subset fails | F1 alone → general panel limit. F2 alone → protect Friday, Thursday load unclear. F1+F2 without F3 → maybe four seated panels look OK. |
| B-prime | Architecture review slips two weeks; panel marathon no longer threatens the judgment block. |
| Diff vs S1–10 | New family; not desk-side sprint (S10) or standing workshop (S6). |

---

## S17 — `vendor_onsite_lab_x_retention_constraints`

| Field | Content |
|---|---|
| Work-demand family | Full-day vendor lab that is screen-first, standing, and post-lunch |
| Bridge type | Preference–constraint fit |
| Facts (4) | **F1 Work/Learning:** retains skills by handwriting + small builds, not talking-head slides. **F2 Work:** prior digital-slate-only cohort produced blank recall. **F3 Health:** hard crash after 14:00 for detailed review. **F4 Health:** consecutive standing capped during flare weeks. |
| Critical pair | F1 (A), F2 (B) |
| Query | Vendor invite: “Full-day Friday lab — screen-only materials, standing stations, deep dive 14:00–17:30. RSVP.” |
| Latent C | RSVP yes as-is is not supported; need paper/build track, sit breaks, and/or morning deep-dive. |
| Why subset fails | Any single constraint suggests tweak, not refusal. Two learning facts without time/standing still allow a morning seated screen lab. |
| B-prime | Lab offers paper worksheets + seated morning track; connector “screen-only standing afternoon” breaks. |
| Diff vs S1–10 | Combines S2/S4/S3/S6 themes into one multi-constraint RSVP; S1–10 kept them as separate 2-fact items. |

---

## S18 — `release_conductor_x_verification_guard`

| Field | Content |
|---|---|
| Work-demand family | Release-conductor role under compressed ship + open interrupt channel |
| Bridge type | Strategy–outcome contingency |
| Facts (4) | **F1 Work:** quality holds when staged verification checklist is kept. **F2 Work:** prior compression that removed verification failed the same compatibility gap. **F3 Work:** interrupt-driven Slack triage reopens settled release decisions. **F4 Calendar:** protected verification block Tue–Thu already booked. |
| Critical pair | F1 (A), F2 (B) |
| Query | Eng manager: “Be Friday release conductor — ship window is compressed; keep #release open for live triage all day.” |
| Latent C | Accepting conductor duties under compressed ship **and** all-day live triage is not supported unless verification stage and a protected block remain. |
| Why subset fails | F2 alone → fear compression (B-sufficient if query says “skip checks”). Query instead offers role+channel. F1+F2 without F3/F4 → compression with quiet verification might pass. |
| B-prime | Prior failure blamed on broken staging env later restored; compressed ship with verification succeeded. |
| Diff vs S1–10 | Merges deadline quality (vNext S5) with interrupt switching (vNext S3); not in S1–10 as a single family. |

---

## S19 — `pm_office_hours_x_evidence_gate`

| Field | Content |
|---|---|
| Work-demand family | Recurring afternoon ambiguous-escalation office hours |
| Bridge type | Prediction calibration |
| Facts (3) | **F1 Work:** ownership after uncertainty list is calibrated. **F2 Work:** ownership before evidence separation named a false cause. **F3 Health/Calendar:** post-14:00 crash; 15:30 recurring slot proposed. |
| Critical pair | F1 (A), F2 (B) |
| Query | Support lead: “Add you to daily 15:30 ambiguous-escalation office hours starting Monday?” |
| Latent C | Daily 15:30 ambiguous office hours are not supported; morning slot with an evidence checklist would be. |
| Why subset fails | F3 alone → move the meeting. F1+F2 without F3 → afternoon might still work. F2 alone without F1 → overgeneral “never own escalations.” |
| B-prime | Prior false cause came from a copied ticket missing logs; with logs present, fast ownership succeeded. |
| Diff vs S1–10 | Not late facilitation visibility (S3); evidence-gate × afternoon physiology. |

---

## S20 — `client_onsite_days_x_commute_energy`

| Field | Content |
|---|---|
| Work-demand family | Multi-day distant client onsite during deep-work deadline week |
| Bridge type | Preference–constraint fit + state-dependent operation |
| Facts (4) | **F1 Work:** long rush-hour commuting drains pre-deep-work energy. **F2 Calendar:** new site needs ~90 minutes each way on collab days. **F3 Work:** architecture design-doc due Friday needs protected solo blocks. **F4 Health:** early departures after recent sleep-schedule switch leave user exhausted. |
| Critical pair | F1 (A), F3 (B) |
| Query | Client PM: “We need you onsite Mon/Wed/Fri next week for collaboration days — please confirm.” |
| Latent C | Confirming three onsite days that week is not supported; at most one onsite + remote deep-work days for the doc. |
| Why subset fails | F1+F2 alone → commute cost without deadline. F3 alone → protect focus, location free. Without F4, two onsite days might look tolerable. |
| B-prime | Design-doc deadline moves out two weeks; onsite week no longer collides with solo-writing connector. |
| Diff vs S1–10 | Upgrades legacy S20 from 2-fact commute dislike to 4-fact week planning; query is confirmation email, not “is distant site a poor fit?” |

---

## Allocation sketch (for later matrix freeze)

| Scenario | Query type (suggested) | Polarity (suggested) | Fact N |
|---|---|---|---:|
| S11 | conditional_recommendation | conditional | 4 |
| S12 | situational_fit | reject | 4 |
| S13 | conditional_recommendation | conditional | 3 |
| S14 | situational_fit | reject | 4 |
| S15 | conditional_recommendation | conditional | 4 |
| S16 | recommendation_ranking | reject | 3 |
| S17 | preference_generalization | conditional | 4 |
| S18 | behavior_explanation | conditional | 4 |
| S19 | predicted_reaction | reject | 3 |
| S20 | situational_fit | reject | 4 |

Next Gate 0 action: human pass/fail on these ten cards before any 20-session authoring.

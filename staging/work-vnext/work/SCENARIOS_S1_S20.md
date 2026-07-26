# Work / learning — S1–S20 scenario cards (for query agents)

**Domain folder:** `src/data/work/{associative,distractor,absence}/`  
**IDs:** `AMB_WL_u{NN}_{arm}_S{N}.json` · 10 users × 20 scenarios × 3 arms = 600  
**Shared timeline:** cut by `timeline_prefix_end`; evidence = two earlier sessions (`ev_A`, `ev_B`).  
**Absence arm:** withhold `ev_B` (partial = `ev_A` only); gold must abstain.  
**Distractor arm:** FOMO lure session inserted; gold same C as associative, ignore lure.

Quotes below are **u01 associative** user turns (persona paint may paraphrase other users; atomic facts stay the same).

---

## S1 — `early_headache_x_late_deepwork`

- **Files:** `AMB_WL_u{NN}_{arm}_S1.json`
- **prefix_end:** 9
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 4)
- atomic_fact: Rising before 6am for early calls causes dull morning headaches that ease by noon.
- quote (u01): “Keep getting dull headaches when I am up before six for those early calls.”

**ev_B** (session 6)
- atomic_fact: The user's peak deep-work window is roughly midnight to 3am.
- quote (u01): “It is past midnight and I just finished a clean refactor. This window is when my brain actually locks in.”

**Links (typed):**
- ev_A —causes→ morning_impairment
- ev_B —indicates→ evening_peak
- ['ev_A', 'ev_B'] —co_activate_to→ dawn_checkin_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Manager offered a move onto the platform pod with a mandatory daily dawn check-in — would I thrive there based on what you know about me?

### Gold conclusion (associative / distractor)

> Probably not as-is. Rising before 6am for early calls already causes dull morning headaches, and your peak deep-work window is roughly midnight to 3am, so a man…

**required_elements:**
- uses early-rising headache pattern
- uses late-night peak deep-work window
- recommends declining or negotiating away mandatory dawn check-in

### Distractor lure (user turn)
> I really love my current team though. Honestly I would do almost anything to work more closely with Maya's crew — they are amazing.

**forbidden / latent leak phrases:** night_oriented_pattern, must never work mornings, decline all team moves

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S2 — `project_learning_x_video_dropout`

- **Files:** `AMB_WL_u{NN}_{arm}_S2.json`
- **prefix_end:** 16
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 11)
- atomic_fact: The user retains skills by building small projects, not by passive reading.
- quote (u01): “Python finally stuck after I rebuilt a tiny ETL script myself. Tutorials alone never lasted.”

**ev_B** (session 13)
- atomic_fact: Long recorded lecture videos cause the user to zone out and quit courses.
- quote (u01): “Abandoned another course full of forty-minute talking-head recordings. I kept drifting and then felt lost.”

**Links (typed):**
- ev_A —indicates→ build_based_retention
- ev_B —causes→ lecture_dropout
- ['ev_A', 'ev_B'] —co_activate_to→ prefer_lab_track

### Current gold query (reference; agents may paraphrase surface only)

> For the learning stipend, should I pick the theory-module track or the live build cohort? A friend says the theory track is amazing.

### Gold conclusion (associative / distractor)

> Choose the live build cohort despite the friend's theory-track praise. You retain skills by building small projects and abandon long talking-head recordings; ce…

**required_elements:**
- uses project-based learning preference
- uses lecture-video abandonment pattern
- recommends live build cohort over theory-module track

### Distractor lure (user turn)
> A friend said the theory-module stipend track is amazing — everyone at her company picks it because the certificate looks great.

**forbidden / latent leak phrases:** always choose beta, learning style diagnosis, must reject all theory

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S3 — `afternoon_crash_x_late_workshop`

- **Files:** `AMB_WL_u{NN}_{arm}_S3.json`
- **prefix_end:** 24
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 18)
- atomic_fact: After a morning coffee peak, the user crashes hard after 2pm and cannot sustain detailed review work.
- quote (u01): “My coffee high dies after two o'clock. After that I am foggy and slow no matter what I drink.”

**ev_B** (session 20)
- atomic_fact: A prior late-afternoon account review went poorly because the user was already cognitively empty.
- quote (u01): “That 4pm account review last month was embarrassing. I lost the thread twice and someone else had to rescue the room.”

**Links (typed):**
- ev_A —causes→ post_2pm_crash
- ev_B —indicates→ late_slot_failure
- ['ev_A', 'ev_B'] —co_activate_to→ avoid_late_workshop_block

### Current gold query (reference; agents may paraphrase surface only)

> Worth leading the recurring late facilitation block after mid-afternoon? A senior said those blocks are amazing for visibility.

### Gold conclusion (associative / distractor)

> Lean no or renegotiate to a morning slot. You crash hard after 2pm and already failed a late account review while cognitively empty; visibility talk does not ov…

**required_elements:**
- uses post-2pm crash pattern
- uses prior late-afternoon review failure
- recommends declining or shifting the late facilitation block

### Distractor lure (user turn)
> Evan said late facilitation blocks are amazing for visibility — if you want to grow, you should say yes to every late invite for the career story.

**forbidden / latent leak phrases:** ADHD diagnosis, must decline all visibility, never take late meetings

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S4 — `handwriting_x_tablet_bootcamp`

- **Files:** `AMB_WL_u{NN}_{arm}_S4.json`
- **prefix_end:** 28
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 25)
- atomic_fact: The user remembers material best when handwriting notes in a paper notebook.
- quote (u01): “Handwriting notes in my paper notebook is still how I remember anything. Typing feels like it slides off.”

**ev_B** (session 27)
- atomic_fact: A prior digital-slate study experiment failed; the user could not retain material.
- quote (u01): “That digital-slate highlighting experiment last fall was a disaster. I marked forever and still blanked on the quiz.”

**Links (typed):**
- ev_A —indicates→ paper_retention
- ev_B —indicates→ digital_fail
- ['ev_A', 'ev_B'] —constrains→ tablet_only_program

### Current gold query (reference; agents may paraphrase surface only)

> Worth enrolling in the vendor's screen-first skills cohort? Marketing says the digital refresh is amazing.

### Gold conclusion (associative / distractor)

> Do not choose the screen-only program as-is. Handwritten notebook notes are how you retain material, and a prior digital-slate experiment failed; marketing abou…

**required_elements:**
- uses handwriting/notebook retention preference
- uses prior digital-slate failure
- recommends against screen-only program or requires paper accommodation

### Distractor lure (user turn)
> A classmate said the vendor's screen-first cohort is amazing — sleek app, automatic sync, and everyone says the digital refresh is worth it.

**forbidden / latent leak phrases:** dyslexia diagnosis, never use tablets, paper ban forever

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S5 — `night_alert_x_sre_rotation`

- **Files:** `AMB_WL_u{NN}_{arm}_S5.json`
- **prefix_end:** 32
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 29)
- atomic_fact: A prior night-alert stretch caused multi-night sleep disruption and lingering daytime impairment.
- quote (u01): “That two-week night-alert stretch last year wrecked me. I woke at every buzz and felt useless the next days.”

**ev_B** (session 31)
- atomic_fact: The user needs unbroken night sleep to stay effective; fragmented nights cascade into sloppy mistakes.
- quote (u01): “If my night gets chopped up, the next day I ship sloppy mistakes. Unbroken sleep is non-negotiable for me.”

**Links (typed):**
- ev_A —causes→ alert_sleep_debt
- ev_B —constrains→ work_quality
- ['ev_A', 'ev_B'] —co_activate_to→ ops_rotation_risky

### Current gold query (reference; agents may paraphrase surface only)

> Six-week callback roster just landed. Friend keeps saying the crew is amazing — worth joining based on what you know about me?

### Gold conclusion (associative / distractor)

> Lean no unless overnight callbacks are protected. A prior night-alert stretch caused multi-week impairment, and unbroken night sleep is non-negotiable for your …

**required_elements:**
- uses prior night-alert sleep disruption
- uses unbroken-sleep requirement for work quality
- recommends declining or heavily conditioning the rotation

### Distractor lure (user turn)
> A friend on the duty crew said the callback roster is amazing — fast promotion path, you should take it if you want career growth.

**forbidden / latent leak phrases:** insomnia diagnosis, never do on-call, must reject all ops roles

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S6 — `standing_back_flare_x_full_day_workshop`

- **Files:** `AMB_WL_u{NN}_{arm}_S6.json`
- **prefix_end:** 38
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 34)
- atomic_fact: Extended standing-desk stretches without sit breaks leave the user's lower back tight the next morning; walking one-on-ones are fine.
- quote (u01): “Extended standing-desk stretches without sit breaks leave my lower back tight the next morning. Walking one-on-ones do not.”

**ev_B** (session 36)
- atomic_fact: Chiropractor advised capping consecutive standing hours during flare weeks.
- quote (u01): “Chiropractor this week: cap consecutive standing hours during flare weeks — treat it as a hard boundary.”

**Links (typed):**
- ev_A —indicates→ standing_back_flare
- ev_B —constrains→ consecutive_standing_cap
- ['ev_A', 'ev_B'] —co_activate_to→ standing_workshop_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Facilities is hyping a full-day standing onsite workshop next week. Worth signing up?

### Gold conclusion (associative / distractor)

> Decline the full-day standing onsite workshop for now. Extended standing-desk stretches without sit breaks have left your lower back tight the next morning, and…

**required_elements:**
- links extended standing-desk blocks to next-morning lower-back tightness
- links chiropractor guidance to cap consecutive standing hours
- recommends declining the full-day standing workshop signup

### Distractor lure (user turn)
> Maya said a full-day standing onsite workshop signup next week is amazing hype and worth signing up for career visibility — everyone is pushing it.

**forbidden / latent leak phrases:** back ban forever, must never stand, skip all workshops

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S7 — `morning_focus_block_x_tuesday_exec_sync`

- **Files:** `AMB_WL_u{NN}_{arm}_S7.json`
- **prefix_end:** 44
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 40)
- atomic_fact: Dense spec review needs an uninterrupted 8-11am block; mid-morning pings wreck nested context.
- quote (u01): “Dense spec review needs an uninterrupted 8-11am block; mid-morning pings wreck nested context.”

**ev_B** (session 42)
- atomic_fact: Manager scheduled a weekly leadership opener at the start of Tuesday blocks.
- quote (u01): “Manager scheduled a weekly leadership opener at the start of Tuesday blocks — already recurring.”

**Links (typed):**
- ev_A —requires→ uninterrupted_morning_block
- ev_B —constrains→ tuesday_9am_exec_sync
- ['ev_A', 'ev_B'] —co_activate_to→ exec_sync_threatens_focus

### Current gold query (reference; agents may paraphrase surface only)

> Leadership keeps adding a nine-o'clock Tuesday visibility opener to my calendar. Worth keeping it?

### Gold conclusion (associative / distractor)

> Push back or negotiate moving the nine-o'clock Tuesday visibility opener. Dense spec review needs an uninterrupted 8-11am block and mid-morning pings wreck nest…

**required_elements:**
- uses dense morning review needing an uninterrupted 8-11am block
- uses weekly Tuesday leadership opener on the calendar
- recommends pushing back or protecting the focus block

### Distractor lure (user turn)
> Evan said a Friday social coffee sync signup is amazing hype and worth keeping as optional visibility before a busy Tuesday week with leadership calendar adds.

**forbidden / latent leak phrases:** never attend meetings, must quit leadership sync, meetings always bad

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S8 — `async_writing_strength_x_live_panel_moderation`

- **Files:** `AMB_WL_u{NN}_{arm}_S8.json`
- **prefix_end:** 49
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 45)
- atomic_fact: Best client memos come from async written prep, not live improvisation under lights.
- quote (u01): “Best client memos come from async written prep, not live improvisation under lights.”

**ev_B** (session 47)
- atomic_fact: Last live panel moderation went poorly — the user lost the thread and client follow-up suffered.
- quote (u01): “Last live panel moderation went poorly — I lost the thread and client follow-up suffered.”

**Links (typed):**
- ev_A —indicates→ async_written_strength
- ev_B —indicates→ live_moderation_weakness
- ['ev_A', 'ev_B'] —co_activate_to→ live_panel_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Client team wants me to moderate their live panel next Thursday. Worth volunteering?

### Gold conclusion (associative / distractor)

> Decline or renegotiate to an async written role. Your best client memos come from async written prep, not live improvisation, and your last live panel moderatio…

**required_elements:**
- uses async written prep as strongest client output format
- uses prior live panel moderation failure and weak follow-up
- recommends declining or shifting to async written contribution

### Distractor lure (user turn)
> Maya said volunteering to moderate the client's live panel slot next Thursday is amazing hype and worth it for visibility — the team is pushing it hard.

**forbidden / latent leak phrases:** never speak in public, must reject all clients, live format always fails

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S9 — `red_eye_jetlag_x_monday_board_dryrun`

- **Files:** `AMB_WL_u{NN}_{arm}_S9.json`
- **prefix_end:** 54
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 50)
- atomic_fact: Overnight return flights leave the user cognitively flat through the next full workday.
- quote (u01): “Overnight return flights leave me cognitively flat through the next full workday — details slip on dense material.”

**ev_B** (session 52)
- atomic_fact: Board rehearsal is locked Monday 10am right after the weekend trip.
- quote (u01): “Board rehearsal is locked Monday 10am right after the weekend trip.”

**Links (typed):**
- ev_A —causes→ next_day_cognitive_flat
- ev_B —constrains→ monday_board_dryrun
- ['ev_A', 'ev_B'] —co_activate_to→ red_eye_conflicts_board_prep

### Current gold query (reference; agents may paraphrase surface only)

> Worth taking a late Sunday return flight to make Monday's board rehearsal?

### Gold conclusion (associative / distractor)

> Do not take the late Sunday return flight for Monday's board rehearsal. Overnight return flights leave you cognitively flat through the next full workday, and t…

**required_elements:**
- uses overnight return flight causing next-day cognitive flatness
- uses Monday 10am board rehearsal deadline
- recommends against the late Sunday return for Monday rehearsal

### Distractor lure (user turn)
> Evan said a Sunday afternoon keynote ticket signup is amazing hype and worth grabbing before Monday's board week for visibility.

**forbidden / latent leak phrases:** never travel, cancel the board meeting, flying is always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S10 — `channel_interrupts_x_desk_side_sprint`

- **Files:** `AMB_WL_u{NN}_{arm}_S10.json`
- **prefix_end:** 59
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 55)
- atomic_fact: Constant channel pings during focus blocks make the user lose nested context and ship sloppy commits.
- quote (u01): “Constant channel pings during focus blocks make me lose nested context — sloppy commits follow.”

**ev_B** (session 57)
- atomic_fact: Prior constant-interruption sprint week correlated with a measurable defect and rollback spike.
- quote (u01): “Prior constant-interruption sprint week correlated with a measurable defect and rollback spike on my lane.”

**Links (typed):**
- ev_A —causes→ slack_interrupt_context_loss
- ev_B —indicates→ war_room_quality_spike
- ['ev_A', 'ev_B'] —co_activate_to→ war_room_threatens_quality

### Current gold query (reference; agents may paraphrase surface only)

> Platform team is hyping a five-day desk-side collaboration sprint signup. Worth joining?

### Gold conclusion (associative / distractor)

> Skip the five-day desk-side collaboration sprint signup. Constant channel pings during focus blocks make you lose nested context and ship sloppy commits, and a …

**required_elements:**
- uses channel pings during focus blocks harming nested context
- uses prior constant-interruption sprint week defect/rollback spike
- recommends skipping the five-day desk-side sprint signup

### Distractor lure (user turn)
> Maya said a five-day desk-side collaboration sprint signup is amazing hype and worth joining before the release review week — everyone on the platform team is pushing it.

**forbidden / latent leak phrases:** never use Slack, cancel the sprint, team collaboration is unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---


---

## S11–S20 — v3 redesign (3–4 independent facts)

> **Batch:** `WL_GOLD_S11_S20_2026-07-24_v3`  
> **Plan:** `assomem/staging/work-vnext/s11-20/GENERATION_PLAN.md`  
> **Cards:** `assomem/staging/work-vnext/s11-20/SCENARIO_CARDS.md`  
> **Legacy backup:** `assomem/staging/work-vnext/s11-20/archive/pre_v3_s11_s20/`  
> S1–S10 above are unchanged (2-fact ladder). S11–S20 JSON on disk were regenerated in place.

| ID | Tag | N | Query cue |
|---|---|---:|---|
| S11 | `offsite_confirm_x_recovery_stack` | 4 | Confirm Thursday afternoon offsite email |
| S12 | `demo_rehearsal_x_voice_clarity_stack` | 4 | Add two Wed lens-on rehearsals? |
| S13 | `apac_verbal_handoff_x_uncertainty_doc` | 3 | Take 06:00 APAC verbal ownership? |
| S14 | `audit_hotdesk_x_quiet_draft` | 4 | Hot-desk Tue–Wed for audit walk? |
| S15 | `sev1_warroom_lead_x_overnight_debt` | 4 | Lead Thu 22:00 war room without prep doc? |
| S16 | `hiring_panel_marathon_x_judgment_block` | 3 | Five consecutive Thursday panels? |
| S17 | `vendor_onsite_lab_x_retention_constraints` | 4 | RSVP full-day screen-only standing lab? |
| S18 | `release_conductor_x_verification_guard` | 4 | Be Fri conductor under compressed ship + live triage? |
| S19 | `pm_office_hours_x_evidence_gate` | 3 | Add daily 15:30 ambiguous office hours? |
| S20 | `client_onsite_days_x_commute_energy` | 4 | Confirm Mon/Wed/Fri distant onsite days? |

**Contract deltas vs S1–S10:** N∈{3,4} facts; situational query (not C paraphrase); any proper subset ↛ C; `gold_tier=v3`; `target_evidence_ids` lists all N ids.

Regenerate:

```bash
python3 assomem/tools/work/bin/generate_work_s11_s20_v3.py --backup-only
python3 assomem/tools/work/bin/generate_work_s11_s20_v3.py --generate --also-mirror-src
python3 assomem/tools/work/bin/generate_work_s11_s20_v3.py --audit
```


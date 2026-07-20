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

## S11 — `video_call_strain_x_client_keynote_dryrun`

- **Files:** `AMB_WL_u{NN}_{arm}_S11.json`
- **prefix_end:** 65
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 61)
- atomic_fact: Back-to-back video-call days leave the user's voice strained for next-day presentations; async memo days are fine.
- quote (u01): “Back-to-back video-call days leave my voice strained for next-day presentations — async memo days do not.”

**ev_B** (session 63)
- atomic_fact: Client keynote dry-run Thursday at nine is non-negotiable.
- quote (u01): “Client keynote dry-run Thursday at nine is non-negotiable — I am treating it as a hard calendar boundary.”

**Links (typed):**
- ev_A —indicates→ video_call_voice_strain
- ev_B —constrains→ thursday_keynote_dryrun
- ['ev_A', 'ev_B'] —co_activate_to→ camera_blocks_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Worth accepting consecutive lens-on blocks this week given Thursday's client presentation rehearsal?

### Gold conclusion (associative / distractor)

> Decline the consecutive lens-on blocks for now. Back-to-back video-call days have left your voice strained for next-day presentations, but client keynote dry-ru…

**required_elements:**
- links stacked video-call days to next-day voice strain
- links Thursday client keynote dry-run as non-negotiable
- recommends declining consecutive lens-on blocks

### Distractor lure (user turn)
> Maya said consecutive lens-on blocks this week are amazing hype and worth accepting for team visibility before Thursday's client week.

**forbidden / latent leak phrases:** video ban forever, must never present, skip all client work

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S12 — `pair_programming_x_design_doc_deadline`

- **Files:** `AMB_WL_u{NN}_{arm}_S12.json`
- **prefix_end:** 71
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 67)
- atomic_fact: Afternoon pair-programming rotations wreck the user's solo architecture focus for hours; short syncs are fine.
- quote (u01): “Afternoon pair-programming rotations wreck my solo architecture focus for hours — short syncs are fine.”

**ev_B** (session 69)
- atomic_fact: Architecture design-doc deadline Friday noon requires protected solo blocks Wednesday and Thursday.
- quote (u01): “Architecture design-doc deadline Friday noon requires protected solo blocks Wednesday and Thursday.”

**Links (typed):**
- ev_A —causes→ pairing_wrecks_solo_focus
- ev_B —constrains→ design_doc_solo_blocks
- ['ev_A', 'ev_B'] —co_activate_to→ pairing_before_writeup_risky

### Current gold query (reference; agents may paraphrase surface only)

> Thinking of adding the afternoon shared-keyboard block before this week's architecture write-up push — good idea?

### Gold conclusion (associative / distractor)

> Do not add the afternoon shared-keyboard block before this week's architecture write-up push. Afternoon pair-programming rotations have wrecked your solo archit…

**required_elements:**
- uses afternoon pairing wrecking solo architecture focus
- uses Friday design-doc deadline needing protected solo blocks
- recommends against afternoon shared-keyboard block before write-up push

### Distractor lure (user turn)
> Evan said adding an afternoon shared-keyboard block before this week's architecture write-up push is amazing hype and worth it for team bonding.

**forbidden / latent leak phrases:** pairing always harmful, must skip collaboration, deadlines always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S13 — `late_cert_cram_x_oncall_rotation`

- **Files:** `AMB_WL_u{NN}_{arm}_S13.json`
- **prefix_end:** 76
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 72)
- atomic_fact: Late-night certification cram sessions wreck the user's alert responsiveness the next morning; morning study blocks are fine.
- quote (u01): “Late-night certification cram sessions wreck my alert responsiveness the next morning — morning study blocks have been fine.”

**ev_B** (session 74)
- atomic_fact: On-call rotation starts Monday with strict paging expectations.
- quote (u01): “On-call rotation starts Monday with strict paging expectations — I need reliable morning alert response.”

**Links (typed):**
- ev_A —causes→ late_cram_wrecks_alert_response
- ev_B —constrains→ monday_oncall_strict_paging
- ['ev_A', 'ev_B'] —co_activate_to→ late_study_conflicts_oncall

### Current gold query (reference; agents may paraphrase surface only)

> Training group added midnight skill drills before next week's duty roster — one-off worth testing?

### Gold conclusion (associative / distractor)

> Skip the midnight skill drills before next week's duty roster. Late-night certification cram sessions have wrecked your alert responsiveness the next morning, a…

**required_elements:**
- uses late-night cert cram wrecking morning alert response
- uses Monday on-call rotation with strict paging
- recommends against midnight skill drills before duty roster

### Distractor lure (user turn)
> Maya said midnight skill drills before next week's duty roster are amazing hype and worth it for credential momentum.

**forbidden / latent leak phrases:** cert ban, must skip on-call, study always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S14 — `hot_desk_noise_x_policy_draft_deadline`

- **Files:** `AMB_WL_u{NN}_{arm}_S14.json`
- **prefix_end:** 81
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 77)
- atomic_fact: Open-office hot-desk days destroy focus for dense policy drafting; quiet home blocks are fine.
- quote (u01): “Open-office hot-desk days destroy focus for dense policy drafting — quiet home blocks are fine.”

**ev_B** (session 79)
- atomic_fact: Quiet policy draft is due Wednesday and needs a deep writing block without open-office churn.
- quote (u01): “Quiet policy draft is due Wednesday and needs a deep writing block without open-office churn.”

**Links (typed):**
- ev_A —causes→ hot_desk_destroys_draft_focus
- ev_B —constrains→ wednesday_quiet_policy_draft
- ['ev_A', 'ev_B'] —co_activate_to→ shared_desk_before_deadline_risky

### Current gold query (reference; agents may paraphrase surface only)

> Worth trying floor-hopping days before this week's compliance memo deadline?

### Gold conclusion (associative / distractor)

> Skip the floor-hopping days before this week's compliance memo deadline. Open-office hot-desk days have destroyed focus for dense policy drafting, and the quiet…

**required_elements:**
- uses hot-desk days destroying policy drafting focus
- uses Wednesday policy draft needing quiet deep-writing block
- recommends skipping floor-hopping days before compliance memo deadline

### Distractor lure (user turn)
> Maya said floor-hopping days before this week's compliance memo deadline are worth testing and everyone in the facilities forum is pushing them.

**forbidden / latent leak phrases:** office ban, must skip all facilities events, drafting always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S15 — `weekend_inbox_blitz_x_sabbatical_planning_week`

- **Files:** `AMB_WL_u{NN}_{arm}_S15.json`
- **prefix_end:** 86
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 82)
- atomic_fact: Weekend inbox catch-up blitzes bleed into protected personal planning blocks; weekday triage is fine.
- quote (u01): “Weekend inbox catch-up blitzes bleed into protected personal planning blocks — weekday triage has been fine.”

**ev_B** (session 84)
- atomic_fact: Sabbatical planning week requires protected Monday half-day blocks for structured planning work.
- quote (u01): “Sabbatical planning week requires protected Monday half-day blocks for structured planning work.”

**Links (typed):**
- ev_A —causes→ weekend_blitz_bleeds_planning
- ev_B —constrains→ monday_halfday_planning_blocks
- ['ev_A', 'ev_B'] —co_activate_to→ weekend_sweep_conflicts_planning

### Current gold query (reference; agents may paraphrase surface only)

> One-off Sunday admin session before next week's personal roadmap week — sensible?

### Gold conclusion (associative / distractor)

> Skip the Sunday admin session before next week's personal roadmap week. Weekend catch-up blitzes have bled into protected personal planning blocks, and sabbatic…

**required_elements:**
- uses weekend inbox blitz bleeding into protected planning blocks
- uses sabbatical planning week requiring Monday half-day blocks
- recommends skipping Sunday admin session before roadmap week

### Distractor lure (user turn)
> Evan said a Sunday admin session before next week's personal roadmap week is amazing hype and worth it for ops visibility.

**forbidden / latent leak phrases:** inbox ban forever, must cancel sabbatical, weekend work always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S16 — `bullpen_chatter_x_diagram_sprint`

- **Files:** `AMB_WL_u{NN}_{arm}_S16.json`
- **prefix_end:** 91
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 88)
- atomic_fact: Open-bullpen ambient chatter wrecks the user's architecture diagramming; quiet-room blocks are fine.
- quote (u01): “Open-bullpen ambient chatter wrecks my architecture diagramming — quiet-room blocks are fine.”

**ev_B** (session 90)
- atomic_fact: Diagram sprint week needs protected morning solo blocks Tuesday through Thursday.
- quote (u01): “Diagram sprint week needs protected morning solo blocks Tuesday through Thursday — already on the calendar.”

**Links (typed):**
- ev_A —causes→ bullpen_wrecks_diagramming
- ev_B —constrains→ diagram_sprint_solo_blocks
- ['ev_A', 'ev_B'] —co_activate_to→ floor_circle_conflicts_sprint

### Current gold query (reference; agents may paraphrase surface only)

> Worth trying the standing huddle loop before Thursday's blueprint lock?

### Gold conclusion (associative / distractor)

> Skip the standing huddle loop before Thursday's blueprint lock. Open-bullpen ambient chatter has wrecked your architecture diagramming, and diagram sprint week …

**required_elements:**
- uses bullpen chatter wrecking architecture diagramming
- uses diagram sprint week needing protected morning solo blocks
- recommends skipping standing huddle loop before blueprint lock

### Distractor lure (user turn)
> Maya said the standing huddle loop before Thursday's blueprint lock is amazing hype and worth joining for team visibility.

**forbidden / latent leak phrases:** office ban forever, must skip all facilities events, diagramming always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S17 — `full_day_shadowing_x_advancement_dossier`

- **Files:** `AMB_WL_u{NN}_{arm}_S17.json`
- **prefix_end:** 96
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 93)
- atomic_fact: Full-day mentor shadowing leaves the user too drained to finish own deliverables; short office hours are fine.
- quote (u01): “Full-day mentor shadowing leaves me too drained to finish my own deliverables — short office hours are fine.”

**ev_B** (session 95)
- atomic_fact: Advancement dossier due Friday needs three solo evening writing blocks.
- quote (u01): “Advancement dossier due Friday needs three solo evening writing blocks — already on the calendar.”

**Links (typed):**
- ev_A —causes→ shadowing_drains_deliverables
- ev_B —constrains→ dossier_solo_evening_blocks
- ['ev_A', 'ev_B'] —co_activate_to→ ridealong_conflicts_dossier

### Current gold query (reference; agents may paraphrase surface only)

> Bench-adjacent immersion week before Friday's packet filing cutoff — workable?

### Gold conclusion (associative / distractor)

> Do not add a bench-adjacent immersion week before Friday's packet filing cutoff. Full-day mentor shadowing has left you too drained to finish your own deliverab…

**required_elements:**
- uses full-day shadowing draining deliverable energy
- uses Friday advancement dossier needing solo evening blocks
- recommends against bench-adjacent immersion week before filing cutoff

### Distractor lure (user turn)
> Evan said a bench-adjacent immersion week before Friday's packet filing cutoff is amazing hype and worth it for career visibility.

**forbidden / latent leak phrases:** mentorship ban, must skip all shadowing, deadlines always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S18 — `afternoon_espresso_x_weekend_build_sprint`

- **Files:** `AMB_WL_u{NN}_{arm}_S18.json`
- **prefix_end:** 101
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 98)
- atomic_fact: Extra espresso after 2pm causes jittery nights and ruins next-morning clarity; morning tea is fine.
- quote (u01): “Extra espresso after two o'clock gives me jittery nights and ruins next-morning clarity — morning tea is fine.”

**ev_B** (session 100)
- atomic_fact: Midweek readiness checkpoint needs sharp morning clarity; a late-slot obligation is booked through the night before.
- quote (u01): “Midweek readiness checkpoint needs a sharp morning clarity block — a late-slot obligation is already booked through the night before.”

**Links (typed):**
- ev_A —causes→ late_espresso_wrecks_morning_clarity
- ev_B —constrains→ monday_review_sharp_morning
- ['ev_A', 'ev_B'] —co_activate_to→ weekend_sprint_conflicts_review

### Current gold query (reference; agents may paraphrase surface only)

> Hall crew added a dusk-to-dawn maker signup — sensible with Thursday's review lock ahead?

### Gold conclusion (associative / distractor)

> Skip the dusk-to-dawn maker signup before Thursday's review lock. Extra espresso after 2pm has caused jittery nights and ruined next-morning clarity, and midwee…

**required_elements:**
- uses afternoon espresso ruining next-morning clarity
- uses midweek readiness checkpoint needing sharp morning clarity
- recommends against dusk-to-dawn maker signup before review lock

### Distractor lure (user turn)
> Maya said the dusk-to-dawn maker signup before Thursday's review lock is amazing hype and worth it for credential momentum.

**forbidden / latent leak phrases:** caffeine ban forever, must skip all vendor events, review always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S19 — `spreadsheet_grid_x_figures_briefing`

- **Files:** `AMB_WL_u{NN}_{arm}_S19.json`
- **prefix_end:** 106
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 103)
- atomic_fact: The user thinks best in spreadsheet grid layouts; wall-chart-only prep sessions produce weak outputs.
- quote (u01): “I think best in spreadsheet grid layouts — wall-chart-only prep sessions produce weak outputs for me.”

**ev_B** (session 105)
- atomic_fact: A prior wall-chart-only figures rehearsal went poorly before the exec briefing.
- quote (u01): “Prior wall-chart-only figures rehearsal went poorly before the exec briefing — I lost the thread twice.”

**Links (typed):**
- ev_A —indicates→ spreadsheet_grid_strength
- ev_B —indicates→ wall_chart_rehearsal_fail
- ['ev_A', 'ev_B'] —co_activate_to→ wall_chart_walkthrough_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Leadership wants me on the poster-board run-through for next week's numbers session — good fit?

### Gold conclusion (associative / distractor)

> Decline or renegotiate to a spreadsheet-grid prep role. You think best in spreadsheet grid layouts and a prior wall-chart-only figures rehearsal went poorly bef…

**required_elements:**
- uses spreadsheet grid layouts as strongest prep format
- uses prior wall-chart-only figures rehearsal failure
- recommends declining or shifting away from poster-board run-through

### Distractor lure (user turn)
> Maya said the poster-board run-through for next week's numbers session is amazing hype and everyone in the leadership forum is pushing it.

**forbidden / latent leak phrases:** spreadsheet ban, must skip all briefings, presentations always unsafe

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---

## S20 — `rush_hour_commute_x_distant_client_site`

- **Files:** `AMB_WL_u{NN}_{arm}_S20.json`
- **prefix_end:** 111
- **Bridge:** ev_A × ev_B → decline / protect calendar (latent C)

### Associate elements

**ev_A** (session 108)
- atomic_fact: Long rush-hour commutes drain the user's cognitive energy before deep work; short bike rides are fine.
- quote (u01): “Long rush-hour commutes drain my cognitive energy before deep work starts — short bike rides are fine.”

**ev_B** (session 110)
- atomic_fact: New client site rhythm requires ninety-minute each-way transit on collaboration days.
- quote (u01): “New client site rhythm requires ninety-minute each-way transit on collaboration days — already on the calendar.”

**Links (typed):**
- ev_A —causes→ commute_drains_cognitive_energy
- ev_B —constrains→ ninety_min_each_way_transit
- ['ev_A', 'ev_B'] —co_activate_to→ distant_site_poor_fit

### Current gold query (reference; agents may paraphrase surface only)

> Worth accepting the heavier daily corridor time for the relocated account cadence — based on what you know about me?

### Gold conclusion (associative / distractor)

> Lean no unless corridor time is shortened or collaboration days are reduced. Long rush-hour commutes have drained your cognitive energy before deep work, and th…

**required_elements:**
- uses long rush-hour commute draining cognitive energy
- uses new client site requiring ninety-minute each-way transit
- recommends declining or negotiating away heavier daily corridor time

### Distractor lure (user turn)
> Evan said accepting the heavier daily corridor time for the relocated account cadence is amazing hype and worth it for career visibility on the account.

**forbidden / latent leak phrases:** commute ban forever, must reject all client sites, remote only forever

**Absence:** hide ev_B → answer must say insufficient evidence / ask / abstain (not invent C).

---


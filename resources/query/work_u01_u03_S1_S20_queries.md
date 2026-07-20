# Work · u01–u03 · S1–S20 tailored queries

Format matches `query/query_sample.md` exactly for every item.
Type is **T1** (Work decision) per `query/query_standard.md`.

| Field | Rule |
|-------|------|
| `query` | One complete natural final-turn utterance |
| `options` | Four complete choice phrases (A=gold / B=prior / C=single-hop A / D=single-hop B) |
| `gold` | `A` |
| `evidence` | The two facts that must bind |

Persona paint changes **surface wording** only; atomic facts stay the same as gold data.

---

## work_u01 (DM-user_001 · coatings consultant, Pittsburgh suburbs)

### S1 `early_headache_x_late_deepwork`

```json
{
  "query_id": "AMB_WL_u01_S1_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The plant manager offered me a seat on the coatings platform pod, but it comes with a fixed 5:45 a.m. stand-up with the East Coast plants every day. Should I take it?",
  "options": {
    "A": "Decline unless they remove the mandatory dawn stand-up",
    "B": "Accept the move for a bigger book of plant business",
    "C": "Accept the move and treat the early headaches as a separate problem",
    "D": "Accept the move because late-night focus means mornings are free anyway"
  },
  "gold": "A",
  "evidence": [
    "ev_A: pre-6am early calls cause morning headaches",
    "ev_B: peak deep-work window is midnight to 3am"
  ]
}
```

### S2 `project_learning_x_video_dropout`

```json
{
  "query_id": "AMB_WL_u01_S2_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "I need to spend the company learning stipend. Should I put it on the coatings theory pack or the live build lab? A peer says the theory certificate looks better on proposals.",
  "options": {
    "A": "Choose the live build lab",
    "B": "Choose the theory pack for the certificate",
    "C": "Choose the theory pack and rebuild a tiny script after each module",
    "D": "Choose the live build lab only to avoid talking-head videos"
  },
  "gold": "A",
  "evidence": [
    "ev_A: retains skills by building small projects",
    "ev_B: abandons long recorded lecture videos"
  ]
}
```

### S3 `afternoon_crash_x_late_workshop`

```json
{
  "query_id": "AMB_WL_u01_S3_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "They want me to own the recurring 4 p.m. customer-review facilitation for the coatings account. A senior says those blocks are great for visibility. Should I say yes?",
  "options": {
    "A": "Decline or move the block to a morning slot",
    "B": "Accept for visibility with plant customers",
    "C": "Accept and add another coffee before 4 p.m.",
    "D": "Decline only because one late review went badly"
  },
  "gold": "A",
  "evidence": [
    "ev_A: crashes hard after 2pm",
    "ev_B: prior late-afternoon account review failed"
  ]
}
```

### S4 `handwriting_x_tablet_bootcamp`

```json
{
  "query_id": "AMB_WL_u01_S4_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The vendor is pushing a screen-only coatings skills cohort for the stipend, and the marketing deck looks slick. Should I enroll?",
  "options": {
    "A": "Skip it, or enroll only if paper notes are allowed",
    "B": "Enroll because the digital format looks more professional",
    "C": "Enroll and print every slide afterward",
    "D": "Skip it only because the digital-slate experiment failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: remembers best with handwritten notebook notes",
    "ev_B: prior digital-slate study experiment failed"
  ]
}
```

### S5 `night_alert_x_sre_rotation`

```json
{
  "query_id": "AMB_WL_u01_S5_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Ops asked me onto a six-week overnight callback roster for the plant systems. A friend on the crew says it is a promotion lane. Should I join?",
  "options": {
    "A": "Decline unless overnight callbacks are protected",
    "B": "Join for the promotion path",
    "C": "Join and nap after every alert",
    "D": "Decline only because sleep matters in general"
  },
  "gold": "A",
  "evidence": [
    "ev_A: prior night-alert stretch wrecked sleep and next days",
    "ev_B: unbroken night sleep is required for clean work"
  ]
}
```

### S6 `standing_back_flare_x_full_day_workshop`

```json
{
  "query_id": "AMB_WL_u01_S6_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Facilities is promoting a full-day standing onsite workshop at the Pittsburgh campus next week. Should I sign up?",
  "options": {
    "A": "Decline the full-day standing workshop",
    "B": "Sign up for onsite visibility with plant leads",
    "C": "Sign up and wear a back brace",
    "D": "Decline only because of this week's chiropractor note"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long standing without breaks flares lower back next morning",
    "ev_B: chiropractor capped consecutive standing hours"
  ]
}
```

### S7 `morning_focus_block_x_tuesday_exec_sync`

```json
{
  "query_id": "AMB_WL_u01_S7_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Leadership keeps putting a 9 a.m. Tuesday visibility opener on my calendar. Should I keep it?",
  "options": {
    "A": "Push back or move the Tuesday opener off the morning focus block",
    "B": "Keep it for leadership face time",
    "C": "Keep it and do dense review after lunch",
    "D": "Push back only because it falls on Tuesday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: dense review needs uninterrupted 8-11am",
    "ev_B: weekly Tuesday leadership opener already on calendar"
  ]
}
```

### S8 `async_writing_strength_x_live_panel_moderation`

```json
{
  "query_id": "AMB_WL_u01_S8_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The client team wants me to moderate their live panel next Thursday. Should I volunteer?",
  "options": {
    "A": "Decline, or switch to an async written contribution",
    "B": "Volunteer for live visibility with the buyer",
    "C": "Volunteer with a fully scripted outline",
    "D": "Decline only because the last live panel went poorly"
  },
  "gold": "A",
  "evidence": [
    "ev_A: best client work comes from async written prep",
    "ev_B: prior live panel moderation failed"
  ]
}
```

### S9 `red_eye_jetlag_x_monday_board_dryrun`

```json
{
  "query_id": "AMB_WL_u01_S9_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Can I take a late Sunday return flight into Pittsburgh and still make Monday's 10 a.m. board dry-run?",
  "options": {
    "A": "Do not take the late Sunday return for Monday's rehearsal",
    "B": "Take the late return to keep the weekend with the plant",
    "C": "Take the late return and sleep on the plane",
    "D": "Skip the flight only because Monday morning is already booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: overnight return flights flatten the next workday",
    "ev_B: Monday 10am board rehearsal is locked"
  ]
}
```

### S10 `channel_interrupts_x_desk_side_sprint`

```json
{
  "query_id": "AMB_WL_u01_S10_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The platform crew is selling a five-day desk-side collaboration sprint before the release review. Should I join?",
  "options": {
    "A": "Skip the five-day desk-side sprint",
    "B": "Join for collaboration optics with plant IT",
    "C": "Join but mute channels for half of each day",
    "D": "Skip it only because of the prior defect spike"
  },
  "gold": "A",
  "evidence": [
    "ev_A: channel pings during focus cause sloppy work",
    "ev_B: prior interrupt-heavy sprint spiked defects"
  ]
}
```

### S11 `video_call_strain_x_client_keynote_dryrun`

```json
{
  "query_id": "AMB_WL_u01_S11_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "They stacked camera-on meeting blocks all week ahead of Thursday's 9 a.m. client keynote dry-run. Should I accept that stack?",
  "options": {
    "A": "Decline the consecutive camera-on blocks",
    "B": "Accept them for more face time with the plant",
    "C": "Accept them and rest the voice somehow",
    "D": "Decline them only to protect Thursday morning"
  },
  "gold": "A",
  "evidence": [
    "ev_A: stacked video-call days strain voice for next-day presenting",
    "ev_B: Thursday 9am client keynote dry-run is locked"
  ]
}
```

### S12 `pair_programming_x_design_doc_deadline`

```json
{
  "query_id": "AMB_WL_u01_S12_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "I am thinking of adding an afternoon shared-keyboard block before this week's architecture write-up. Is that a good idea?",
  "options": {
    "A": "Do not add the afternoon shared-keyboard block",
    "B": "Add it for pairing culture on the platform team",
    "C": "Add it only if each session stays under twenty minutes",
    "D": "Skip it only because of Friday's design-doc deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: afternoon pairing wrecks solo architecture focus",
    "ev_B: Friday design-doc needs protected solo blocks Wed/Thu"
  ]
}
```

### S13 `late_cert_cram_x_oncall_rotation`

```json
{
  "query_id": "AMB_WL_u01_S13_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Training added midnight skill drills before next week's duty roster. Is a one-off worth trying?",
  "options": {
    "A": "Skip the midnight skill drills",
    "B": "Try them for credential momentum on plant bids",
    "C": "Try them and use caffeine at dawn",
    "D": "Skip them only because Monday on-call starts"
  },
  "gold": "A",
  "evidence": [
    "ev_A: late-night cert cram wrecks morning alertness",
    "ev_B: Monday on-call needs reliable morning paging"
  ]
}
```

### S14 `hot_desk_noise_x_policy_draft_deadline`

```json
{
  "query_id": "AMB_WL_u01_S14_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Facilities wants me on floor-hopping hot-desk days before Wednesday's compliance memo. Is that worth testing?",
  "options": {
    "A": "Skip the floor-hopping hot-desk days",
    "B": "Test them for floor visibility",
    "C": "Test them with noise-cancelling headphones",
    "D": "Skip them only because of Wednesday's deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: open hot-desk days destroy policy-drafting focus",
    "ev_B: Wednesday quiet policy draft needs a deep writing block"
  ]
}
```

### S15 `weekend_inbox_blitz_x_sabbatical_planning_week`

```json
{
  "query_id": "AMB_WL_u01_S15_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Would a one-off Sunday inbox sweep be sensible before next week's personal roadmap and sabbatical planning?",
  "options": {
    "A": "Skip the Sunday inbox sweep",
    "B": "Do the sweep so planning week starts with a clean inbox",
    "C": "Do a shorter Sunday sweep only",
    "D": "Skip it only to protect Monday's planning blocks"
  },
  "gold": "A",
  "evidence": [
    "ev_A: weekend inbox blitzes bleed into protected planning",
    "ev_B: sabbatical planning needs Monday half-day blocks"
  ]
}
```

### S16 `bullpen_chatter_x_diagram_sprint`

```json
{
  "query_id": "AMB_WL_u01_S16_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Is it worth joining the standing huddle loop before Thursday's blueprint lock?",
  "options": {
    "A": "Skip the standing huddle loop",
    "B": "Join for team visibility before lock",
    "C": "Join and finish diagrams at night instead",
    "D": "Skip it only because diagram-sprint mornings are already booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: bullpen chatter wrecks architecture diagramming",
    "ev_B: diagram sprint needs protected morning solo blocks Tue-Thu"
  ]
}
```

### S17 `full_day_shadowing_x_advancement_dossier`

```json
{
  "query_id": "AMB_WL_u01_S17_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Would a bench-adjacent full-day immersion week work before Friday's advancement packet cutoff?",
  "options": {
    "A": "Do not add the full-day immersion week",
    "B": "Add it because immersion looks strong on advancement packets",
    "C": "Shadow only in the mornings",
    "D": "Skip it only because Friday's dossier is due"
  },
  "gold": "A",
  "evidence": [
    "ev_A: full-day shadowing drains energy for own deliverables",
    "ev_B: Friday advancement dossier needs solo evening writing blocks"
  ]
}
```

### S18 `afternoon_espresso_x_weekend_build_sprint`

```json
{
  "query_id": "AMB_WL_u01_S18_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The hall crew added a dusk-to-dawn maker signup. Is that sensible with Thursday's readiness review locked?",
  "options": {
    "A": "Skip the dusk-to-dawn maker signup",
    "B": "Join for the coatings innovation story",
    "C": "Join but switch to decaf after 2 p.m.",
    "D": "Skip it only to protect Thursday morning"
  },
  "gold": "A",
  "evidence": [
    "ev_A: espresso after 2pm wrecks next-morning clarity",
    "ev_B: midweek readiness checkpoint needs a sharp morning"
  ]
}
```

### S19 `spreadsheet_grid_x_figures_briefing`

```json
{
  "query_id": "AMB_WL_u01_S19_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "Leadership wants me on the poster-board numbers run-through for next week's exec session. Is that a good fit?",
  "options": {
    "A": "Decline, or renegotiate to spreadsheet-grid prep",
    "B": "Accept because poster boards look executive",
    "C": "Accept and bring a laptop grid as backup",
    "D": "Decline only because the prior wall-chart rehearsal failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: thinks best in spreadsheet grid layouts",
    "ev_B: prior wall-chart-only figures rehearsal failed"
  ]
}
```

### S20 `rush_hour_commute_x_distant_client_site`

```json
{
  "query_id": "AMB_WL_u01_S20_T1",
  "profile_id": "work_u01",
  "type": "T1",
  "query": "The relocated account wants heavier daily corridor time — about ninety minutes each way on collaboration days. Should I accept that, given how I work?",
  "options": {
    "A": "Decline or negotiate the corridor time down",
    "B": "Accept for face time at the new site",
    "C": "Accept and work from the car or train",
    "D": "Decline only because of the ninety-minute transit figure"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long rush-hour commutes drain energy before deep work",
    "ev_B: new client site needs ninety-minute each-way transit"
  ]
}
```

---

## work_u02 (DM-user_002 · Netherlands-based, structured weekdays)

### S1 `early_headache_x_late_deepwork`

```json
{
  "query_id": "AMB_WL_u02_S1_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "My manager proposed moving me onto the platform pod, with a mandatory daily 05:45 CET check-in. Does that fit how I run my week?",
  "options": {
    "A": "Decline unless they remove the mandatory dawn check-in",
    "B": "Accept because the platform pod is the high-growth lane",
    "C": "Accept and treat early headaches as a separate issue",
    "D": "Accept because late-night focus leaves the morning free"
  },
  "gold": "A",
  "evidence": [
    "ev_A: pre-6am early calls cause morning headaches",
    "ev_B: peak deep-work window is midnight to 3am"
  ]
}
```

### S2 `project_learning_x_video_dropout`

```json
{
  "query_id": "AMB_WL_u02_S2_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "For the learning stipend, should I choose the theory-module track or the live build cohort? A colleague prefers the theory track for the certificate.",
  "options": {
    "A": "Choose the live build cohort",
    "B": "Choose the theory-module track for the certificate",
    "C": "Choose the theory track and rebuild a small system after each module",
    "D": "Choose the live build cohort only to avoid lecture videos"
  },
  "gold": "A",
  "evidence": [
    "ev_A: retains skills by building small projects",
    "ev_B: abandons long recorded lecture videos"
  ]
}
```

### S3 `afternoon_crash_x_late_workshop`

```json
{
  "query_id": "AMB_WL_u02_S3_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "They asked me to lead a recurring facilitation block after 14:00. A senior says it is good for visibility. Should I keep it?",
  "options": {
    "A": "Decline or move it to a morning slot",
    "B": "Keep it for visibility",
    "C": "Keep it and add another coffee beforehand",
    "D": "Decline only because one late review went poorly"
  },
  "gold": "A",
  "evidence": [
    "ev_A: crashes hard after 2pm",
    "ev_B: prior late-afternoon account review failed"
  ]
}
```

### S4 `handwriting_x_tablet_bootcamp`

```json
{
  "query_id": "AMB_WL_u02_S4_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "There is a screen-first vendor cohort available for upskilling. Should I enroll?",
  "options": {
    "A": "Skip it, or enroll only with paper-note accommodation",
    "B": "Enroll for modern tooling",
    "C": "Enroll and print the slides afterward",
    "D": "Skip it only because the digital-slate experiment failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: remembers best with handwritten notebook notes",
    "ev_B: prior digital-slate study experiment failed"
  ]
}
```

### S5 `night_alert_x_sre_rotation`

```json
{
  "query_id": "AMB_WL_u02_S5_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "A six-week overnight callback roster just opened, and a friend says it helps promotion. Should I join?",
  "options": {
    "A": "Decline unless overnight callbacks are protected",
    "B": "Join for the promotion path",
    "C": "Join and plan naps after alerts",
    "D": "Decline only for general sleep hygiene"
  },
  "gold": "A",
  "evidence": [
    "ev_A: prior night-alert stretch wrecked sleep and next days",
    "ev_B: unbroken night sleep is required for clean work"
  ]
}
```

### S6 `standing_back_flare_x_full_day_workshop`

```json
{
  "query_id": "AMB_WL_u02_S6_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Facilities is advertising a full-day standing onsite workshop. Should I sign up?",
  "options": {
    "A": "Decline the full-day standing workshop",
    "B": "Sign up for onsite presence",
    "C": "Sign up and use a back brace",
    "D": "Decline only because of the chiropractor's standing cap"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long standing without breaks flares lower back next morning",
    "ev_B: chiropractor capped consecutive standing hours"
  ]
}
```

### S7 `morning_focus_block_x_tuesday_exec_sync`

```json
{
  "query_id": "AMB_WL_u02_S7_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Leadership added a weekly 09:00 Tuesday visibility opener to my calendar. Should I keep it?",
  "options": {
    "A": "Push back or move it off the morning focus block",
    "B": "Keep it as a leadership signal",
    "C": "Keep it and shift dense review to later",
    "D": "Push back only because it is on Tuesday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: dense review needs uninterrupted 8-11am",
    "ev_B: weekly Tuesday leadership opener already on calendar"
  ]
}
```

### S8 `async_writing_strength_x_live_panel_moderation`

```json
{
  "query_id": "AMB_WL_u02_S8_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "A client asked me to moderate a live panel on Thursday. Should I volunteer?",
  "options": {
    "A": "Decline, or offer an async written contribution instead",
    "B": "Volunteer for visibility",
    "C": "Volunteer with a full script prepared",
    "D": "Decline only because the last live moderation failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: best client work comes from async written prep",
    "ev_B: prior live panel moderation failed"
  ]
}
```

### S9 `red_eye_jetlag_x_monday_board_dryrun`

```json
{
  "query_id": "AMB_WL_u02_S9_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Should I take a late Sunday return flight in order to make Monday's 10:00 board dry-run?",
  "options": {
    "A": "Do not take the late Sunday return",
    "B": "Take it to keep more of the weekend free",
    "C": "Take it and sleep on the flight",
    "D": "Skip the flight only because Monday morning is booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: overnight return flights flatten the next workday",
    "ev_B: Monday 10am board rehearsal is locked"
  ]
}
```

### S10 `channel_interrupts_x_desk_side_sprint`

```json
{
  "query_id": "AMB_WL_u02_S10_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "The platform team is promoting a five-day desk-side collaboration sprint. Should I join?",
  "options": {
    "A": "Skip the five-day desk-side sprint",
    "B": "Join for collaboration optics",
    "C": "Join but mute channels for part of each day",
    "D": "Skip it only because of the prior defect spike"
  },
  "gold": "A",
  "evidence": [
    "ev_A: channel pings during focus cause sloppy work",
    "ev_B: prior interrupt-heavy sprint spiked defects"
  ]
}
```

### S11 `video_call_strain_x_client_keynote_dryrun`

```json
{
  "query_id": "AMB_WL_u02_S11_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "They want consecutive camera-on blocks this week before Thursday's 09:00 keynote dry-run. Should I accept?",
  "options": {
    "A": "Decline the consecutive camera-on blocks",
    "B": "Accept them for presence",
    "C": "Accept them and rest the voice between calls",
    "D": "Decline them only to protect Thursday morning"
  },
  "gold": "A",
  "evidence": [
    "ev_A: stacked video-call days strain voice for next-day presenting",
    "ev_B: Thursday 9am client keynote dry-run is locked"
  ]
}
```

### S12 `pair_programming_x_design_doc_deadline`

```json
{
  "query_id": "AMB_WL_u02_S12_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Should I add an afternoon shared-keyboard block before this week's architecture write-up?",
  "options": {
    "A": "Do not add the afternoon shared-keyboard block",
    "B": "Add it for pairing culture",
    "C": "Add it only if the sessions stay short",
    "D": "Skip it only because of Friday's design-doc deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: afternoon pairing wrecks solo architecture focus",
    "ev_B: Friday design-doc needs protected solo blocks Wed/Thu"
  ]
}
```

### S13 `late_cert_cram_x_oncall_rotation`

```json
{
  "query_id": "AMB_WL_u02_S13_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Training scheduled midnight skill drills before Monday's on-call. Is a one-off worth trying?",
  "options": {
    "A": "Skip the midnight skill drills",
    "B": "Try them for credentials",
    "C": "Try them with caffeine at dawn",
    "D": "Skip them only because on-call starts Monday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: late-night cert cram wrecks morning alertness",
    "ev_B: Monday on-call needs reliable morning paging"
  ]
}
```

### S14 `hot_desk_noise_x_policy_draft_deadline`

```json
{
  "query_id": "AMB_WL_u02_S14_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Should I try floor-hopping hot-desk days before Wednesday's compliance memo?",
  "options": {
    "A": "Skip the floor-hopping hot-desk days",
    "B": "Try them for floor visibility",
    "C": "Try them with headphones",
    "D": "Skip them only because of Wednesday's deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: open hot-desk days destroy policy-drafting focus",
    "ev_B: Wednesday quiet policy draft needs a deep writing block"
  ]
}
```

### S15 `weekend_inbox_blitz_x_sabbatical_planning_week`

```json
{
  "query_id": "AMB_WL_u02_S15_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Is a Sunday admin sweep sensible before next week's sabbatical planning?",
  "options": {
    "A": "Skip the Sunday admin sweep",
    "B": "Do it so planning week starts clean",
    "C": "Do a shorter Sunday sweep only",
    "D": "Skip it only to protect Monday's planning blocks"
  },
  "gold": "A",
  "evidence": [
    "ev_A: weekend inbox blitzes bleed into protected planning",
    "ev_B: sabbatical planning needs Monday half-day blocks"
  ]
}
```

### S16 `bullpen_chatter_x_diagram_sprint`

```json
{
  "query_id": "AMB_WL_u02_S16_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Should I join the standing huddle loop before Thursday's blueprint lock?",
  "options": {
    "A": "Skip the standing huddle loop",
    "B": "Join for the team loop",
    "C": "Join and move diagramming to the evening",
    "D": "Skip it only because the diagram-sprint mornings are booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: bullpen chatter wrecks architecture diagramming",
    "ev_B: diagram sprint needs protected morning solo blocks Tue-Thu"
  ]
}
```

### S17 `full_day_shadowing_x_advancement_dossier`

```json
{
  "query_id": "AMB_WL_u02_S17_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Would a full-day mentor immersion work before Friday's advancement dossier cutoff?",
  "options": {
    "A": "Do not add the full-day immersion",
    "B": "Add it for advancement optics",
    "C": "Shadow in the mornings only",
    "D": "Skip it only because Friday's dossier is due"
  },
  "gold": "A",
  "evidence": [
    "ev_A: full-day shadowing drains energy for own deliverables",
    "ev_B: Friday advancement dossier needs solo evening writing blocks"
  ]
}
```

### S18 `afternoon_espresso_x_weekend_build_sprint`

```json
{
  "query_id": "AMB_WL_u02_S18_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "There is a dusk-to-dawn maker signup before Thursday's readiness review. Should I join?",
  "options": {
    "A": "Skip the dusk-to-dawn maker signup",
    "B": "Join for the maker story",
    "C": "Join but avoid late caffeine",
    "D": "Skip it only to protect Thursday morning"
  },
  "gold": "A",
  "evidence": [
    "ev_A: espresso after 2pm wrecks next-morning clarity",
    "ev_B: midweek readiness checkpoint needs a sharp morning"
  ]
}
```

### S19 `spreadsheet_grid_x_figures_briefing`

```json
{
  "query_id": "AMB_WL_u02_S19_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "Leadership wants me on a poster-board run-through for next week's numbers session. Is that a good fit?",
  "options": {
    "A": "Decline, or switch to spreadsheet-grid prep",
    "B": "Accept for an executive look",
    "C": "Accept and bring a laptop grid as backup",
    "D": "Decline only because the prior wall-chart rehearsal failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: thinks best in spreadsheet grid layouts",
    "ev_B: prior wall-chart-only figures rehearsal failed"
  ]
}
```

### S20 `rush_hour_commute_x_distant_client_site`

```json
{
  "query_id": "AMB_WL_u02_S20_T1",
  "profile_id": "work_u02",
  "type": "T1",
  "query": "The relocated site wants heavier daily corridor time of about ninety minutes each way. Should I accept?",
  "options": {
    "A": "Decline or negotiate the corridor time down",
    "B": "Accept for site face time",
    "C": "Accept and work during the commute",
    "D": "Decline only because of the ninety-minute figure"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long rush-hour commutes drain energy before deep work",
    "ev_B: new client site needs ninety-minute each-way transit"
  ]
}
```

---

## work_u03 (DM-user_003 · urban knowledge worker, meeting-averse)

### S1 `early_headache_x_late_deepwork`

```json
{
  "query_id": "AMB_WL_u03_S1_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Manager offered a platform-pod move with a mandatory daily dawn check-in. Should I take it?",
  "options": {
    "A": "Decline unless they drop the dawn check-in",
    "B": "Take it for growth on the pod",
    "C": "Take it and manage the early headaches separately",
    "D": "Take it because late-night focus leaves mornings free"
  },
  "gold": "A",
  "evidence": [
    "ev_A: pre-6am early calls cause morning headaches",
    "ev_B: peak deep-work window is midnight to 3am"
  ]
}
```

### S2 `project_learning_x_video_dropout`

```json
{
  "query_id": "AMB_WL_u03_S2_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "For the learning stipend, should I pick the theory-module track or the live build cohort? A friend says the theory certificate looks better.",
  "options": {
    "A": "Pick the live build cohort",
    "B": "Pick the theory-module track for the certificate",
    "C": "Pick the theory track and rebuild something after each module",
    "D": "Pick the live build cohort only to avoid lecture videos"
  },
  "gold": "A",
  "evidence": [
    "ev_A: retains skills by building small projects",
    "ev_B: abandons long recorded lecture videos"
  ]
}
```

### S3 `afternoon_crash_x_late_workshop`

```json
{
  "query_id": "AMB_WL_u03_S3_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "They want me to own the recurring late facilitation block after mid-afternoon. A senior says it is great for visibility. Should I say yes?",
  "options": {
    "A": "Decline or move it to a morning slot",
    "B": "Say yes for visibility",
    "C": "Say yes and add more caffeine beforehand",
    "D": "Say no only because one late review went badly"
  },
  "gold": "A",
  "evidence": [
    "ev_A: crashes hard after 2pm",
    "ev_B: prior late-afternoon account review failed"
  ]
}
```

### S4 `handwriting_x_tablet_bootcamp`

```json
{
  "query_id": "AMB_WL_u03_S4_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I enroll in the vendor's screen-first skills cohort? Marketing says the digital refresh is amazing.",
  "options": {
    "A": "Skip it, or enroll only if paper notes are allowed",
    "B": "Enroll because it looks modern",
    "C": "Enroll and print every slide afterward",
    "D": "Skip it only because the digital-slate experiment failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: remembers best with handwritten notebook notes",
    "ev_B: prior digital-slate study experiment failed"
  ]
}
```

### S5 `night_alert_x_sre_rotation`

```json
{
  "query_id": "AMB_WL_u03_S5_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "A six-week overnight callback roster just landed, and a friend says the crew is a promotion path. Should I join?",
  "options": {
    "A": "Decline unless overnight callbacks are protected",
    "B": "Join for the promotion path",
    "C": "Join and nap after alerts",
    "D": "Decline only because sleep matters in general"
  },
  "gold": "A",
  "evidence": [
    "ev_A: prior night-alert stretch wrecked sleep and next days",
    "ev_B: unbroken night sleep is required for clean work"
  ]
}
```

### S6 `standing_back_flare_x_full_day_workshop`

```json
{
  "query_id": "AMB_WL_u03_S6_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Facilities is hyping a full-day standing onsite workshop next week. Should I sign up?",
  "options": {
    "A": "Decline the full-day standing workshop",
    "B": "Sign up for visibility",
    "C": "Sign up and wear a back brace",
    "D": "Decline only because of the chiropractor's standing cap"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long standing without breaks flares lower back next morning",
    "ev_B: chiropractor capped consecutive standing hours"
  ]
}
```

### S7 `morning_focus_block_x_tuesday_exec_sync`

```json
{
  "query_id": "AMB_WL_u03_S7_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Leadership keeps adding a 9 a.m. Tuesday visibility opener to my calendar. Should I keep it?",
  "options": {
    "A": "Push back or move it off the morning focus block",
    "B": "Keep it for politics",
    "C": "Keep it and do dense review later",
    "D": "Push back only because it is on Tuesday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: dense review needs uninterrupted 8-11am",
    "ev_B: weekly Tuesday leadership opener already on calendar"
  ]
}
```

### S8 `async_writing_strength_x_live_panel_moderation`

```json
{
  "query_id": "AMB_WL_u03_S8_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "The client wants me to moderate their live panel next Thursday. Should I volunteer?",
  "options": {
    "A": "Decline, or switch to an async written role",
    "B": "Volunteer for clout",
    "C": "Volunteer with a full script",
    "D": "Decline only because the last live moderation failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: best client work comes from async written prep",
    "ev_B: prior live panel moderation failed"
  ]
}
```

### S9 `red_eye_jetlag_x_monday_board_dryrun`

```json
{
  "query_id": "AMB_WL_u03_S9_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I take a late Sunday return flight to make Monday's 10 a.m. board dry-run?",
  "options": {
    "A": "Do not take the late Sunday return",
    "B": "Take it to keep the weekend",
    "C": "Take it and sleep on the plane",
    "D": "Skip it only because Monday morning is booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: overnight return flights flatten the next workday",
    "ev_B: Monday 10am board rehearsal is locked"
  ]
}
```

### S10 `channel_interrupts_x_desk_side_sprint`

```json
{
  "query_id": "AMB_WL_u03_S10_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "The platform team is hyping a five-day desk-side collaboration sprint. Should I join?",
  "options": {
    "A": "Skip the five-day desk-side sprint",
    "B": "Join for team vibes",
    "C": "Join but mute channels part of the day",
    "D": "Skip it only because of the prior rollback spike"
  },
  "gold": "A",
  "evidence": [
    "ev_A: channel pings during focus cause sloppy work",
    "ev_B: prior interrupt-heavy sprint spiked defects"
  ]
}
```

### S11 `video_call_strain_x_client_keynote_dryrun`

```json
{
  "query_id": "AMB_WL_u03_S11_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I accept consecutive camera-on blocks this week given Thursday's 9 a.m. client keynote dry-run?",
  "options": {
    "A": "Decline the consecutive camera-on blocks",
    "B": "Accept them for presence",
    "C": "Accept them and rest the voice between calls",
    "D": "Decline them only to protect Thursday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: stacked video-call days strain voice for next-day presenting",
    "ev_B: Thursday 9am client keynote dry-run is locked"
  ]
}
```

### S12 `pair_programming_x_design_doc_deadline`

```json
{
  "query_id": "AMB_WL_u03_S12_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I add an afternoon shared-keyboard block before this week's architecture write-up?",
  "options": {
    "A": "Do not add the afternoon shared-keyboard block",
    "B": "Add it for bonding",
    "C": "Add it only if sessions stay short",
    "D": "Skip it only because of Friday's design-doc deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: afternoon pairing wrecks solo architecture focus",
    "ev_B: Friday design-doc needs protected solo blocks Wed/Thu"
  ]
}
```

### S13 `late_cert_cram_x_oncall_rotation`

```json
{
  "query_id": "AMB_WL_u03_S13_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Training added midnight skill drills before next week's duty roster. Is a one-off worth testing?",
  "options": {
    "A": "Skip the midnight skill drills",
    "B": "Try them for the credential",
    "C": "Try them with caffeine at dawn",
    "D": "Skip them only because on-call starts Monday"
  },
  "gold": "A",
  "evidence": [
    "ev_A: late-night cert cram wrecks morning alertness",
    "ev_B: Monday on-call needs reliable morning paging"
  ]
}
```

### S14 `hot_desk_noise_x_policy_draft_deadline`

```json
{
  "query_id": "AMB_WL_u03_S14_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I try floor-hopping hot-desk days before this week's compliance memo deadline?",
  "options": {
    "A": "Skip the floor-hopping hot-desk days",
    "B": "Try them for visibility",
    "C": "Try them with headphones",
    "D": "Skip them only because of Wednesday's deadline"
  },
  "gold": "A",
  "evidence": [
    "ev_A: open hot-desk days destroy policy-drafting focus",
    "ev_B: Wednesday quiet policy draft needs a deep writing block"
  ]
}
```

### S15 `weekend_inbox_blitz_x_sabbatical_planning_week`

```json
{
  "query_id": "AMB_WL_u03_S15_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Is a one-off Sunday admin session sensible before next week's personal roadmap week?",
  "options": {
    "A": "Skip the Sunday admin session",
    "B": "Do it for a clean inbox",
    "C": "Do a shorter Sunday session only",
    "D": "Skip it only to protect Monday's planning blocks"
  },
  "gold": "A",
  "evidence": [
    "ev_A: weekend inbox blitzes bleed into protected planning",
    "ev_B: sabbatical planning needs Monday half-day blocks"
  ]
}
```

### S16 `bullpen_chatter_x_diagram_sprint`

```json
{
  "query_id": "AMB_WL_u03_S16_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I try the standing huddle loop before Thursday's blueprint lock?",
  "options": {
    "A": "Skip the standing huddle loop",
    "B": "Join for the team loop",
    "C": "Join and do diagrams at night",
    "D": "Skip it only because diagram-sprint mornings are booked"
  },
  "gold": "A",
  "evidence": [
    "ev_A: bullpen chatter wrecks architecture diagramming",
    "ev_B: diagram sprint needs protected morning solo blocks Tue-Thu"
  ]
}
```

### S17 `full_day_shadowing_x_advancement_dossier`

```json
{
  "query_id": "AMB_WL_u03_S17_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Would a bench-adjacent immersion week work before Friday's packet filing cutoff?",
  "options": {
    "A": "Do not add the immersion week",
    "B": "Add it for the packet story",
    "C": "Shadow in the mornings only",
    "D": "Skip it only because Friday's packet is due"
  },
  "gold": "A",
  "evidence": [
    "ev_A: full-day shadowing drains energy for own deliverables",
    "ev_B: Friday advancement dossier needs solo evening writing blocks"
  ]
}
```

### S18 `afternoon_espresso_x_weekend_build_sprint`

```json
{
  "query_id": "AMB_WL_u03_S18_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "The hall crew added a dusk-to-dawn maker signup. Is that sensible with Thursday's review lock ahead?",
  "options": {
    "A": "Skip the dusk-to-dawn maker signup",
    "B": "Join for hustle points",
    "C": "Join but skip late espresso",
    "D": "Skip it only to protect Thursday morning"
  },
  "gold": "A",
  "evidence": [
    "ev_A: espresso after 2pm wrecks next-morning clarity",
    "ev_B: midweek readiness checkpoint needs a sharp morning"
  ]
}
```

### S19 `spreadsheet_grid_x_figures_briefing`

```json
{
  "query_id": "AMB_WL_u03_S19_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Leadership wants me on the poster-board run-through for next week's numbers session. Is that a good fit?",
  "options": {
    "A": "Decline, or switch to spreadsheet-grid prep",
    "B": "Accept for the executive look",
    "C": "Accept and bring a laptop grid as backup",
    "D": "Decline only because the prior wall-chart rehearsal failed"
  },
  "gold": "A",
  "evidence": [
    "ev_A: thinks best in spreadsheet grid layouts",
    "ev_B: prior wall-chart-only figures rehearsal failed"
  ]
}
```

### S20 `rush_hour_commute_x_distant_client_site`

```json
{
  "query_id": "AMB_WL_u03_S20_T1",
  "profile_id": "work_u03",
  "type": "T1",
  "query": "Should I accept the heavier daily corridor time for the relocated account cadence, given how I work?",
  "options": {
    "A": "Decline or negotiate the corridor time down",
    "B": "Accept for face time on the account",
    "C": "Accept and work during the commute",
    "D": "Decline only because of the ninety-minute each-way transit"
  },
  "gold": "A",
  "evidence": [
    "ev_A: long rush-hour commutes drain energy before deep work",
    "ev_B: new client site needs ninety-minute each-way transit"
  ]
}
```

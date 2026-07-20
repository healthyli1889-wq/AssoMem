# AssoMemBench — work/learning (S1–S20)

**600 items · 10 users · 20 scenarios × 3 arms**

## Folder map

```
src/data/work/
  associative/     # all users
  distractor/
  absence/
```

Filenames: `AMB_WL_u{NN}_{arm}_S{N}.json`

Full scenario cards (evidence quotes, links, distractors) for query agents:  
→ [`SCENARIOS_S1_S20.md`](SCENARIOS_S1_S20.md)

## Personas

| user | Source |
|------|--------|
| user1–4 | DynamicMem ×4 |
| user5–9 | RHELM ×5 |
| user10 | Desktop Healthy Li |

## Scenario cores (S1–S20)

| ID | Bridge (ev_A × ev_B) | Decoupled query (surface) |
|----|----------------------|---------------------------|
| S1 | early-rising headache × late deep-work peak | mandatory dawn check-in / platform pod |
| S2 | build-to-learn × lecture-video dropout | stipend theory track vs live build cohort |
| S3 | post-2pm crash × prior late review fail | late facilitation block |
| S4 | handwriting retention × digital-slate fail | screen-first skills cohort |
| S5 | night-alert sleep debt × unbroken-sleep need | six-week callback / SRE roster |
| S6 | standing-desk back flare × cap standing hours | full-day standing onsite workshop |
| S7 | 8–11am focus block × Tuesday leadership opener | keep nine-o'clock Tuesday visibility opener |
| S8 | async written prep × live panel fail | moderate live panel |
| S9 | overnight-flight flatness × Monday board dry-run | late Sunday return flight |
| S10 | channel-ping context loss × interrupt sprint defects | five-day desk-side collaboration sprint |
| S11 | back-to-back video voice strain × Thu keynote dry-run | consecutive lens-on blocks |
| S12 | afternoon pair-programming drain × Fri design-doc | afternoon shared-keyboard block |
| S13 | late-night cert cram × Mon on-call paging | midnight skill drills before duty roster |
| S14 | hot-desk noise × Wed policy draft | floor-hopping days before compliance memo |
| S15 | weekend inbox blitz × sabbatical planning Mon | Sunday admin before personal roadmap week |
| S16 | bullpen chatter × diagram sprint mornings | standing huddle loop before blueprint lock |
| S17 | full-day mentor shadowing × Fri advancement dossier | bench-adjacent immersion before packet cutoff |
| S18 | post-2pm espresso / jitter × midweek clarity checkpoint | dusk-to-dawn maker signup |
| S19 | spreadsheet-grid thinking × wall-chart rehearsal fail | poster-board run-through for numbers session |
| S20 | rush-hour commute drain × long client-site transit | heavier daily corridor for relocated account |

## Arms

- **associative** — both evidences visible; gold needs co-activation → usually decline / protect calendar
- **distractor** — FOMO lure; same C; must ignore lure
- **absence** — withhold ev_B; gold abstains

## Loader (do not leak labels)

Serialize `context[].dialogue` with only `role`+`content`. Strip `annotation`, `associative_links`, `gold_answer`, `validity_metrics` from model-visible input.

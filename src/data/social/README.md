# Social / relationships — S1–S20 gold (v2)

**600 items · 10 users · 20 scenarios × 3 arms · hard-gate 600/600 PASS**

Shared timeline (111 sessions). Each scenario cuts via `timeline_prefix_end` — cumulative history, no same-date conflicts across S1–S20.

Generator: `tools/social/bin/generate_social_gold_batch.py`  
Reports: `manifests/social/social_gold_s{1_s5,6_s15,16_s20}_report.json`

## Scenarios

| ID | Bridge (ev_A × ev_B) | Decoupled query |
|----|----------------------|-----------------|
| S1 | large-gathering drain × roommate quiet evenings | heavier weekend hosting block |
| S2 | reply-storm anxiety × slow one-on-one check-in | always-on reunion chat lead |
| S3 | coffee-hang stacking hollow × Thursday repair presence | midweek catch-ups before hard talk |
| S4 | public-compliment freeze × prior live shoutout fail | live recognition round at dinner |
| S5 | solo Saturday recharge × family visit booked | heavier neighborhood morning block |
| S6 | late multi-hour dinner flat × early Sat bike energy | seated supper past bedtime |
| S7 | unannounced drop-in wreck × Tuesday sibling check-in | spontaneous Tuesday pop-ins |
| S8 | private written thanks × prior live gift-toast fail | on-the-spot goodbye tribute |
| S9 | overnight guest next-day flat × Monday mentoring | stay the night before coaching slot |
| S10 | status-ping presence loss × friend letter evening | continuous presence roster |
| S11 | stacked video hangs thin × Thursday reunion lunch | lens-on hangouts before reunion |
| S12 | afternoon mixer listening wreck × Friday repair call | hallway networking before hard talk |
| S13 | late-party alertness wreck × dawn airport pickup | midnight send-off before airport favor |
| S14 | open-house writing wreck × friendship letter deadline | walk-through hosting midweek |
| S15 | weekend inbox-blitz bleed × Sunday family-call recovery | Saturday message catch-up blitz |
| S16 | noisy hangout planning wreck × friendship check-in solo mornings | standing hang loop before check-in lock |
| S17 | full-day immersion drain × recommendation-letter evenings | bench-adjacent hang marathon before packet cutoff |
| S18 | late drinks clarity wreck × midweek hard-talk clarity | dusk-to-dawn maker signup before review lock |
| S19 | private-notes prep × prior flipchart toast fail | poster-board run-through for farewell briefing |
| S20 | long rush-hour transit drain × distant meetup rhythm | heavier corridor time for relocated meetup cadence |

## Arms

- **associative** — both evidence sessions visible; gold requires co-activation
- **distractor** — FOMO lure with cosine ≥ evidence
- **absence** — withhold ev_B; gold abstains

IDs: `AMB_SC_u{NN}_{arm}_S{N}.json`

## Folder map

```
src/data/social/
  associative/     # all users
  distractor/
  absence/
```

Filenames: `AMB_{XX}_u{{NN}}_{{arm}}_S{{N}}.json` (user id in name, not folder).


# Finance / personal — S1–S20 gold

**600 items · 10 users · 20 scenarios × 3 arms**

| Batch | Scenarios | Tier | Release rule | Status |
|-------|-----------|------|--------------|--------|
| S1–S5 | 150 | v2 | hard-gate PASS | 150/150 |
| S6–S15 | 300 | **v3_ultra** | hard-gate PASS **and score ≥ 95** | **300/300 @ 100.0** |
| S16–S20 | 150 | **v3_ultra** | hard-gate PASS **and score ≥ 95** | **150/150 @ 100.0** |

Shared cumulative timeline (111 sessions). Each scenario cuts via `timeline_prefix_end`.

## Folder map

```
src/data/finance/
  associative/     # all users
  distractor/
  absence/
```

Filenames: `AMB_FN_u{NN}_{arm}_S{N}.json`

Full scenario cards (evidence quotes, links, distractors) for query agents:  
→ [`SCENARIOS_S1_S20.md`](SCENARIOS_S1_S20.md)

Generator: `tools/finance/bin/generate_finance_gold_batch.py`  
Reports: `manifests/finance/finance_gold_s{1_s5,6_s15,16_s20}_report.json`

## Scenario cores (S1–S20)

| ID | Bridge (ev_A × ev_B) | Decoupled query (surface) |
|----|----------------------|---------------------------|
| S1 | high apr revolving × lease deposit | Worth parking spare cash in a speculative tip pool th… |
| S2 | panic sell × payday dca | Chat is hyping a one-week day-trading bootcamp signup |
| S3 | thin buffer × deductible procedure | Someone pitched rolling idle cash into a yield chase … |
| S4 | roth room used × second account blitz | Desk wants me on a year-end second-account signup blitz |
| S5 | freelance gaps × autorenew stack | Worth adding the bundled lifestyle membership this week |
| S6 | unused match × earmarked paycheck | Desk pinged me about a hallway raffle stake this afte… |
| S7 | weekend fx fees × monday rent wire | Club pinged me about an after-hours remittance into t… |
| S8 | bnpl overdraft × estimated tax reserve | Registry wants me on a split-pay gift plan this week |
| S9 | hsa room × elective dental | Colleague floated an after-tax tip-channel signup thi… |
| S10 | deductible cash × brake repair | Pitch came in to park the emergency envelope in a hig… |
| S11 | loan autopay × late bonus | Seller is pushing a deluxe class hold funded by a fut… |
| S12 | dual approval × household window | Buddy asked me to wire a sizable stake into an off-bo… |
| S13 | hype coin loss × index risk budget | Discord floated a one-off coin call signup tonight |
| S14 | escrow committed × movein buffer | Building chat wants me in a condo crowdfund this week |
| S15 | wash sale × harvest window | Thread wants me on a same-sector rebound buy this week |
| S16 | utilization spike × landlord soft pull | Desk pinged me about a points-card signup sprint this… |
| S17 | education gift earmark × friday deadline | Colleague floated a premium holiday gift pool this cycle |
| S18 | premium draft × peer lending lockup | Buddy asked me to park cash in a locked yield circle … |
| S19 | annual trial trap × thin friday buffer | Colleague floated an annual productivity-suite trial … |
| S20 | airport fx markup × trip cash budgeted | Crew floated a last-minute FX window stop before boar… |

## Arms

- **associative** — both evidence sessions visible; gold requires co-activation
- **distractor** — FOMO lure with cosine ≥ evidence (+0.05 margin on v3_ultra)
- **absence** — withhold ev_B; gold abstains

## v3_ultra bar (S6–S20)

- query↔evidence lexical jaccard ≤ 0.06
- distractor cosine margin ≥ 0.05 above evidence
- query↔history surface jaccard < 0.30
- flat TF-IDF top-3 miss on target evidence

## Loader (do not leak labels)

Serialize `context[].dialogue` with only `role`+`content`. Strip `annotation`, `associative_links`, `gold_answer`, `validity_metrics` from model-visible input.

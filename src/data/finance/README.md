# Finance / personal — S1–S20 gold

**600 items · 10 users · 20 scenarios × 3 arms**

| Batch | Scenarios | Tier | Release rule | Status |
|-------|-----------|------|--------------|--------|
| S1–S5 | 150 | v2 | hard-gate PASS | 150/150 |
| S6–S15 | 300 | **v3_ultra** | hard-gate PASS **and score ≥ 95** | **300/300 @ 100.0** |
| S16–S20 | 150 | **v3_ultra** | hard-gate PASS **and score ≥ 95** | **150/150 @ 100.0** |

Shared cumulative timeline (111 sessions). Each scenario cuts via `timeline_prefix_end`.

Generator: `tools/finance/bin/generate_finance_gold_batch.py`  
Reports: `manifests/finance/finance_gold_s{1_s5,6_s15,16_s20}_report.json`

## Scenarios

| ID | Bridge (ev_A × ev_B) | Decoupled query |
|----|----------------------|-----------------|
| S1 | high-APR revolving sticky × lease deposit next month | speculative tip pool this month |
| S2 | red-day panic sells × payday auto index transfers | one-week day-trading bootcamp |
| S3 | liquid reserve <1 month × deductible dental booked | idle cash into yield chase |
| S4 | Roth room used for 2026 × prior December dual-wrapper fail | year-end second-account signup blitz |
| S5 | odd-month freelance gaps × auto-renew stack hard to unwind | bundled lifestyle membership |
| S6 | unused employer match × Friday match-window earmark | hallway raffle stake this afternoon |
| S7 | weekend FX remittance fees × first-workday euro rent wire | after-hours remittance into group pot |
| S8 | prior BNPL overdraft × estimated-tax reserve earmarked | split-pay gift plan this week |
| S9 | open HSA room × HSA-eligible dental scheduled | after-tax tip-channel signup this cycle |
| S10 | deductible-reset liquid fund × brake repair booked | high-APR chase for emergency envelope |
| S11 | loan autopay bounce before payout × incentive after draft | deluxe class hold on future paycheck |
| S12 | dual-approval joint account × dual-approval-only window | off-book stake wire right now |
| S13 | hype-thread coin losses × index risk budget allocated | one-off coin call signup tonight |
| S14 | escrow cash committed × move-in buffer reserved | condo crowdfund this housing week |
| S15 | wash-sale risk on queued harvest × post-window replacement | same-sector rebound buy this week |
| S16 | high utilization score-ding × landlord soft-pull next week | points-card signup sprint this afternoon |
| S17 | education-gift earmark × Friday school-calendar deadline | premium holiday gift pool this cycle |
| S18 | mid-month insurance premium draft × peer-lending lockup | locked yield circle this week |
| S19 | annual trial-flip overdraft × thin Friday cash buffer | annual productivity-suite trial convert |
| S20 | away-from-home cash-machine markups × trip cash budgeted | last-minute FX window stop before boarding |

## Arms

- **associative** — both evidence sessions visible; gold requires co-activation
- **distractor** — FOMO lure with cosine ≥ evidence (+0.05 margin on v3_ultra)
- **absence** — withhold ev_B; gold abstains

## v3_ultra bar (S6–S20)

- query↔evidence lexical jaccard ≤ 0.06
- distractor cosine margin ≥ 0.05 above evidence
- query↔history surface jaccard < 0.30
- flat TF-IDF top-3 miss on target evidence
- generator only writes items with autograder **total ≥ 95**

IDs: `AMB_FN_u{NN}_{arm}_S{N}.json`

## Folder map

```
src/data/finance/
  associative/     # all users
  distractor/
  absence/
```

Filenames: `AMB_{XX}_u{{NN}}_{{arm}}_S{{N}}.json` (user id in name, not folder).


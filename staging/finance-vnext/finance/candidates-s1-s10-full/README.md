# Finance S1–S10 full batch (10 MemoryQuest users × 3 conditions)

**300 files** = 10 scenarios × 10 users × 3 arms (`associative` / `distractor` / `absence`).

Layout:
```
candidates-s1-s10-full/
  associative/AMB_FN_S{1..10}_U{01..10}_associative.json   # 100
  distractor/AMB_FN_S{1..10}_U{01..10}_distractor.json     # 100
  absence/AMB_FN_S{1..10}_U{01..10}_absence.json           # 100
```

Persona anchors (visible dialogue stays anonymized):
| Profile | MemoryQuest file | persona_anchor |
|---|---|---|
| U01 | `user0.json` | `mq_user0` |
| U02 | `user5.json` | `mq_user5` |
| U03 | `user10.json` | `mq_user10` |
| U04 | `user15.json` | `mq_user15` |
| U05 | `user20.json` | `mq_user20` |
| U06 | `user25.json` | `mq_user25` |
| U07 | `user30.json` | `mq_user30` |
| U08 | `user35.json` | `mq_user35` |
| U09 | `user40.json` | `mq_user40` |
| U10 | `user44.json` | `mq_user44` |

| Scenario | Family |
|---|---|
| S1 | hard cash claim versus high-cost drag or speculative diversion |
| S2 | volatility panic versus systematic payday investing |
| S3 | thin emergency reserve versus booked near-term expense |
| S4 | exhausted tax-advantaged room versus year-end account blitz |
| S5 | income volatility versus sticky auto-renew stacks |
| S6 | unused employer match versus paycheck-remainder side bets |
| S7 | weekend remittance fees versus weekday rent wires |
| S8 | BNPL overdraft patterns versus earmarked tax reserves |
| S9 | open HSA contribution room versus after-tax speculative signups |
| S10 | deductible repair cash versus high-APR emergency-envelope chases |

Regenerate: `python3 generate_s1_s10_full.py`  
See `TONE_GUIDE.md`, `memoryquest_roster.py`.

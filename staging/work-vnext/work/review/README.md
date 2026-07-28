# work-vNext S1–S20 re-run under the corrected harness

The work candidate data is **not** in this branch; it lives on `main` at
`staging/work-vnext/work/harness-root-{s1-s10,s11-s15-v2,s16-s20-v2}`. Only the
run artifacts are here, so the gold stays owned by one branch.

Reproduce:

```bash
mkdir -p /tmp/work_data/{associative,distractor,absence}
git archive origin/main staging/work-vnext/work | tar -x -C /tmp/work_extract
for root in harness-root-s1-s10 harness-root-s11-s15-v2 harness-root-s16-s20-v2; do
  for arm in associative distractor absence; do
    cp /tmp/work_extract/staging/work-vnext/work/$root/$arm/*.json /tmp/work_data/$arm/
  done
done
source my_config.sh
export ASSOMEM_DATA_ROOT=/tmp/work_data ASSOMEM_DOMAIN=work \
       ASSOMEM_PROFILE=$PWD/experiments/assomem_harness/profiles/work-vnext-1.json
python3 -u experiments/assomem_harness/screen_vnext.py --per-polarity 80 --workers 8 \
        --out staging/work-vnext/work/review/ladder_rerun_200.json
python3 staging/vnext_common/aggregate_ladder.py \
        staging/work-vnext/work/review/ladder_rerun_200.json
```

All 200 pairs, one solver (`Vendor2/GPT-5.6-Terra`), one judge (`kimi/kimi-k3`),
`target_proposition` supplied, a_only/b_only rendered by matched replacement
(0.90–1.05 of `full` by length) rather than deletion.

## Result

| arm | gold | target-positive | | arm | gold | target-positive |
|---|---|---|---|---|---|---|
| zero_evidence | no | **0.000** (200/200) | | link_broken | no | 0.770 |
| full | yes | 0.920 | | a_only | no | 0.640 |
| distractor | yes | 0.915 | | b_only | no | 0.810 |
| | | | | absence | no | 0.265 |

| | point | CI |
|---|---|---|
| Δ_mem = full − absence | **+0.655** | [+0.590, +0.720] |
| Δ_assoc = full − link_broken | **+0.150** | [+0.085, +0.215] |
| full − a_only | +0.280 | [+0.215, +0.350] |
| full − b_only | +0.110 | [+0.060, +0.165] |

Memory necessity is solid and holds per scenario (18 of 20 have a Δ_mem interval
excluding zero; S17 +0.200 and S18 +0.100 are the weak ones). **Δ_assoc is weak**:
the link-broken arm still asserts the target on 77% of items, so the intervention
barely moves the solver. This is the finding the very first review of this project
suspected, now measured at n=200 on a clean harness.

## Why link_broken does not bite

Not a copy-paste problem: B-prime retains only 22% of ev_B's distinctive
vocabulary on average, so the episode really is rewritten. The issue is semantic —
**B-prime removes the obstacle instead of severing the A–B contingency**, and the
target proposition is about the arrangement, so it stays true after the obstacle
is fixed. From S01_U01:

- target: "Taking the standing 06:00 incident bridge *as currently run, with
  overnight notes arriving after it starts*, is a poor fit for this user."
- B-prime: "The tooling change shipped: overnight notes now publish at 05:15, so
  the dependency picture is ready before the 06:00 bridge starts."

A solver can still answer yes — the bridge *as currently run* was a poor fit, and
here is the fix. ev_A plus the background carries that on its own.

Compare a B-prime that negates the second link directly, from social S1: "I've
gone into those conversations planned and unplanned by now, and it made no odds
either way — the state just doesn't touch it." A+B-prime then cannot license C.

Second contributor to the a_only 0.640 / b_only 0.810 leak: several targets are
generic recommendations — "Ask colleagues to batch nonurgent questions and
preserve a protected evidence-review block", "Ask for a shorter, remote, or
rescheduled offsite option before confirming" — which are sensible for anyone.
That is the same conventional-proposition problem the finance v2 batch had, and
the reason the social, hobby and finance v3 batches make every proposition
counter-conventional.

## Comparison

| | work | social | hobby | finance v3 |
|---|---|---|---|---|
| n | 200 | 164 | 164 | 164 |
| full | 0.920 | 0.738 | 0.866 | 0.878 |
| Δ_mem | +0.655 | +0.683 | +0.774 | +0.768 |
| **Δ_assoc** | **+0.150** | +0.500 | +0.555 | +0.506 |
| link_broken | 0.770 | 0.238 | 0.311 | 0.372 |

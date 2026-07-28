# health-vNext re-run (200 pairs)

Health had never been run: no branch carried a zero-evidence artifact, records
directory or ladder for it. (`logs/health/results.tsv` on every branch is the
legacy `AMB_HD_*` health-diet gate log from July, unrelated to this batch.)

Data stays on `origin/claire/health-vnext` at `staging/health-vnext/v1/s1/candidates`;
only run artifacts are here. Reproduce:

```bash
git archive origin/claire/health-vnext staging/health-vnext | tar -x -C /tmp/health_extract
cp -r /tmp/health_extract/staging/health-vnext/v1/s1/candidates /tmp/health_data
rm -rf /tmp/health_data/artifacts
source my_config.sh
export ASSOMEM_DATA_ROOT=/tmp/health_data ASSOMEM_DOMAIN=health \
       ASSOMEM_PROFILE=$PWD/experiments/assomem_harness/profiles/health-vnext-1.json
python3 -u experiments/assomem_harness/screen_vnext.py --per-polarity 80 --workers 8 \
        --out staging/health-vnext/health/review/ladder_200.json
python3 staging/vnext_common/aggregate_ladder.py staging/health-vnext/health/review/ladder_200.json
```

All 600 files pass `validate_candidate`. One solver (`Vendor2/GPT-5.6-Terra`), one
judge (`kimi/kimi-k3`), `target_proposition` supplied.

## Result

| arm | gold | target-positive | | arm | gold | target-positive |
|---|---|---|---|---|---|---|
| zero_evidence | no | **0.000** (200/200) | | link_broken | no | 0.205 |
| full | yes | 0.700 | | a_only | no | 0.245 |
| distractor | yes | 0.730 | | b_only | no | **0.050** |
| | | | | absence | no | **0.000** (200/200) |

| | point | CI |
|---|---|---|
| Δ_mem = full − absence | **+0.700** | [+0.635, +0.765] |
| Δ_assoc = full − link_broken | **+0.495** | [+0.415, +0.570] |
| full − a_only | +0.455 | [+0.375, +0.535] |
| full − b_only | **+0.650** | [+0.580, +0.720] |

**These are the cleanest ablation arms of any of the five domains.** Absence is
0.000 across all 200 items and b_only is 0.050, so the single-evidence controls
genuinely hold — the thing every other batch struggles with. `arm_gold` also
carries `required_elements` and `rationale`, which work and finance v2 omit.

The weakness is the top of the ladder: `full` is 0.700, and only 0.50 on the
`reject` half, so the solver often fails to reach C even with everything visible.
Δ is large partly because the floor is low.

## Two data issues worth fixing

**1. No `single_evidence_replacements` (0 of 200).** `render_arms` therefore
deletes the session for a_only and b_only instead of swapping in a matched neutral
one, so both arms run at **19 sessions against full's 20** and the lineage records
`session_count_preserved: false`. Some of the a_only/b_only drop could be a
reaction to a shorter context rather than to the missing evidence. Adding a matched
neutral session per arm — as work already does — removes the confound; the harness
picks them up automatically.

**2. Query-type quota is badly skewed.**

| query type | count |
|---|---|
| situational_fit | 40 |
| recommendation_ranking | 40 |
| predicted_reaction | 40 |
| behavior_explanation | 40 |
| conditional_recommendation | 39 |
| **preference_generalization** | **1** |

DATA CRITERIA §4 wants the six roughly balanced (32/32/32/32/36/36 at n=200). The
"no type above 20%" ceiling is technically met, but one type at 0.5% means the
batch does not exercise preference generalisation at all.

Polarity is fine: reject 80, accept 41, non_decision 40, conditional 39.

**3. Not a scenario × user grid.** 200 slug-named items over 136 distinct slugs and
200 distinct users, so there is no per-scenario or per-user breakdown to report,
and no "same person across scenarios" structure.

## Five domains side by side

| | health | work | social | hobby | finance v3 |
|---|---|---|---|---|---|
| n | 200 | 200 | 164 | 164 | 164 |
| full | 0.700 | **0.920** | 0.738 | 0.866 | 0.878 |
| Δ_mem | +0.700 | +0.655 | +0.683 | **+0.774** | +0.768 |
| Δ_assoc | +0.495 | **+0.150** | +0.500 | **+0.555** | +0.506 |
| a_only | **0.245** | 0.640 | 0.341 | 0.616 | 0.640 |
| b_only | **0.050** | 0.810 | 0.567 | 0.640 | 0.720 |
| absence | **0.000** | 0.265 | 0.055 | 0.091 | 0.110 |

# Person-bound associative memory: benchmark items, harness, and measured results

Anonymous release for review. Three top-level folders:

| folder | what is in it |
|---|---|
| `data/` | 3,000 benchmark items — 5 domains × 200 units × 3 source arms |
| `code/` | the generators, the evaluation harness, the prompts, and the spec |
| `results/` | the measured ladder for each domain, as run |

## What the benchmark asks

Each unit contains two dated episodes belonging to the **same person**, `ev_A` and
`ev_B`, a relation between them, and a binary proposition `C` about that person
that neither episode licenses alone. The construct requirement is:

```
ev_A alone does not support C.
ev_B alone does not support C.
ev_A + ev_B jointly support C.
ev_A + B-prime no longer supports C.
No target episode supports C at all in absence.
```

A solver sees 20 dated dialogue sessions, a final-turn query, and the proposition,
and returns `{"decision": "yes"|"no", "answer": ..., "evidence_session_ids": [...]}`.
Six conditions are rendered per unit from three shipped source arms:

| condition | visible | gold |
|---|---|---|
| `full` | both episodes | assert C |
| `distractor` | both, plus a query-relevant non-evidential session | assert C |
| `a_only` | ev_B swapped for a matched neutral session | withhold C |
| `b_only` | ev_A swapped for a matched neutral session | withhold C |
| `link_broken` | ev_B replaced by B-prime, relation removed | withhold C |
| `absence` | both episodes swapped for matched neutral sessions | withhold C |
| `zero_evidence` | the query alone, empty context | withhold C |

The headline quantity is **Δ_assoc = P(assert \| full) − P(assert \| link_broken)**.
Both terms are the *same* measurement on two conditions, so a solver that always
asserts scores 0 rather than full marks — see
`code/assomem_harness/tests/test_reporting_deltas.py`.

## Results

One solver and one judge per run, both held fixed within a run. 164–200 items per
domain, stratified by polarity. Target-positive rate per condition:

| | health | work | social | hobby | finance |
|---|---|---|---|---|---|
| n | 200 | 200 | 164 | 164 | 164 |
| zero_evidence | **0.000** | **0.000** | **0.000** | **0.000** | **0.000** |
| full | 0.700 | **0.910** | 0.738 | 0.866 | 0.878 |
| distractor | 0.730 | 0.925 | 0.744 | 0.835 | 0.866 |
| link_broken | 0.205 | 0.470 | 0.238 | 0.311 | 0.372 |
| a_only | **0.245** | 0.690 | 0.341 | 0.616 | 0.640 |
| b_only | **0.050** | 0.820 | 0.567 | 0.640 | 0.720 |
| absence | **0.000** | 0.280 | 0.055 | 0.091 | 0.110 |

Paired bootstrap over items, 95% CI:

| | health | work | social | hobby | finance |
|---|---|---|---|---|---|
| Δ_mem = full − absence | +0.700 | +0.630 | +0.683 | **+0.774** | +0.768 |
| **Δ_assoc = full − link_broken** | +0.495 | +0.440 | +0.500 | **+0.555** | +0.506 |
| full − a_only | +0.455 | +0.220 | +0.396 | +0.250 | +0.238 |
| full − b_only | **+0.650** | +0.090 | +0.171 | +0.226 | +0.159 |

Every interval excludes zero in every domain, and the query-only screen is clean
on all 928 screened items. Δ_assoc excluding zero is the condition for calling the
task associative rather than ordinary multi-hop retrieval.

## Limitations, stated plainly

- **Single solver.** Every number above comes from one solver model. Nothing here
  supports a claim about models in general.
- **The single-evidence controls are not uniformly clean.** `b_only` ranges from
  0.050 (health) to 0.820 (work). Where it is high, one episode plus ordinary
  domain sense reaches the proposition, and the corresponding Δ is correspondingly
  small. The cause is identified: propositions phrased as generic good advice are
  reachable without the person's history, which is why the social, hobby and
  finance items make every proposition counter-conventional. The work items were
  not rewritten this way.
- **health renders two conditions one session short.** It ships no
  `single_evidence_replacements`, so `a_only` and `b_only` are produced by deleting
  the target session rather than swapping in a matched neutral one, and run at 19
  sessions against `full`'s 20. Part of that drop may be a reaction to a shorter
  context. Every other domain holds all six conditions at 20 sessions, within
  0.90–1.09 of `full` by character count.
- **health's query-type mix is skewed.** Five of the six approved query types
  appear 39–40 times in 200 items; `preference_generalization` appears once.
- **health is not a scenario × user grid.** 200 individually-slugged items over 200
  distinct users, so it supports no per-scenario or per-user breakdown, and no
  same-person-across-scenarios structure.
- **No human gate has been passed.** All items carry
  `provenance.status: review_candidate_only`. The deterministic audit and the
  query-only screen pass; the reviewer checklist in
  `code/spec/DATA_CRITERIA.md` §8 has not been signed off.
- **`source_swap` is out of scope**, so source-monitoring (SAA) is not measured.

## Reproducing

```bash
cd code
PYTHONPATH=. python3 -m pytest assomem_harness/tests -q      # no model calls

cp config.example.sh my_config.sh    # fill in two endpoints and two keys
source my_config.sh
python3 -u assomem_harness/screen_vnext.py --per-polarity 80 --workers 8 \
        --out /tmp/ladder.json
python3 generators/vnext_common/aggregate_ladder.py /tmp/ladder.json
```

The solver and the judge must be different models; `models.py` refuses otherwise.
`aggregate.py` refuses to aggregate a run scored by more than one judge, because
judges disagree most on exactly the conditions that set Δ_assoc.

See `data/README.md` for the item schema and per-domain design, and
`code/README.md` for the module layout.

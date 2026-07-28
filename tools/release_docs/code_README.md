# Code, scripts, and prompts

Pure standard library — no third-party dependency, no package install. Everything
runs from this directory with `PYTHONPATH=.`.

```
code/
├── config.example.sh          copy to my_config.sh and fill in
├── spec/DATA_CRITERIA.md      the generation contract the items are built against
├── prompts/                   the live prompts, rendered readable
│   ├── solver.md              what the evaluated model sees
│   ├── judge.md               what the independent validator sees
│   └── author.md              the per-item authoring prompt
├── assomem_vnext/schema.py    validate a record; render the six conditions
├── assomem_harness/           run and score
├── model_client/clients.py    dependency-free OpenAI-/Anthropic-compatible client
├── generators/                deterministic item generation
└── tools/rewrite_bprime.py    rebuild B-prime from an item's own event elements
```

## The harness

| module | responsibility |
|---|---|
| `dataset.py` | discover the three-file pairs; build the solver-visible payload |
| `arms.py` | materialize the six conditions with their gold |
| `protocol.py` | the solver and judge prompt contracts |
| `models.py` | two model slots from the environment; refuses solver == judge |
| `workflow.py` | validate a solver response; turn a judge verdict into scores |
| `scoring.py` | Wilson intervals; paired bootstrap over items |
| `reporting.py` | Table A / Table B |
| `aggregate.py` | per-record logs → tables, with the run audit |
| `zero_evidence.py` | the query-only screen |
| `screen_vnext.py` | run the whole ladder over a batch, with progress and resume |
| `smoke_vnext.py` | one item across all conditions, for wiring checks |
| `run.py` | the gated three-stage runner: dry-run → zero-evidence → execute |
| `profiles/*.json` | one data-only profile per domain |

### Two things worth knowing before reading numbers

**The Δ is a difference of the same measurement.** `reporting.target_assertion`
converts each condition's correctness into the target-assertion rate before
subtracting, because correctness means opposite things on the two halves of the
ladder: on `full` a correct answer asserts the proposition, on `a_only` a correct
answer withholds it. Subtracting raw accuracies gives a solver that always asserts
a perfect Δ of 1.00 for zero discrimination.
`tests/test_reporting_deltas.py` pins all four boundary cases.

**One judge per run.** `aggregate()` refuses a run scored by more than one
validator. Judges agree closely on `full` and `distractor` and disagree sharply on
the ablation conditions, so a mixed-judge run yields a Δ that reflects the judge
mix rather than the data.

`run_audit.json` records scored and unscored counts and the solver and judge
census; aggregation warns when records are missing, because the denominator is
every planned trial rather than the ones that came back.

## The solver never sees gold

`dataset.solver_input` deep-copies the context, pops every annotation, and returns
exactly `{context, query, target_proposition, prompt_hash}`.
`tests/test_release_data.py::test_solver_never_sees_gold` asserts that on every
condition of every domain.

`target_proposition` is the question, not the answer. Withholding it leaves the
binary decision undefined — the solver has to guess which proposition it is being
scored against from the query — and pushes that guess onto the judge, which is
where judges diverge.

## Generation

```
generators/
├── vnext_common/    engine.py  allocation.py  audit.py  aggregate_ladder.py
├── social/          social_spec.py  social_spec_s11_s20.py  memoryquest_roster.py  generate_*.py
├── hobby/           hobby_spec.py   hobby_spec_s11_s20.py   hobby_roster.py        generate_*.py
└── finance/         finance_spec.py finance_spec_s11_s20.py finance_roster.py      generate_*.py
```

`engine.py` owns everything structural — the 20-session budget, the arm
construction rules, the length-matched neutral replacements, the arm gold. A domain
pack supplies content only. `allocation.py` freezes the query-type and polarity
grid before any dialogue is written and asserts the quotas. `audit.py` is the
deterministic pre-model audit: schema, pair consistency, session counts, matched
replacement lengths, connector-span visibility, anonymisation, and surface-language
hazards that templating introduces.

Adding a domain means adding a pack and a profile, not editing the engine.

## Running it

```bash
cd code
PYTHONPATH=. python3 -m pytest assomem_harness/tests -q     # no model calls

cp config.example.sh my_config.sh && $EDITOR my_config.sh
source my_config.sh
PYTHONPATH=. python3 assomem_harness/smoke_vnext.py --pair AMB_SC_S1_U01
PYTHONPATH=. python3 -u assomem_harness/screen_vnext.py \
        --per-polarity 80 --workers 8 --out /tmp/ladder.json
python3 generators/vnext_common/aggregate_ladder.py /tmp/ladder.json
```

`screen_vnext.py` appends each finished item to a sidecar JSONL and prints a
counter with elapsed and ETA, so an interrupted run resumes rather than restarts;
`--restart` ignores the sidecar.

`run.py` is the stricter path and enforces the gate order from
`spec/DATA_CRITERIA.md` §7: a dry run freezes an item manifest, the query-only
screen must pass per item, a reviewed intervention audit must be signed, and only
then will it execute. The results in `results/` were produced by `screen_vnext.py`,
which runs the same six conditions and the same prompts without the human gates.

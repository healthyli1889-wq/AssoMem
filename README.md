# AssoMemBench — Associative Memory Benchmark for Personal Agents



### Background 

> **Can an agent use what it stores about you to infer *new*, plausible preferences — and act on them?**
> Most "memory" agents only *retrieve* stored facts. This benchmark + reference agent test
> **associative user understanding**, inspired by human associative memory.

[python]() [license]()



### Contribution

1. a **reference associative-memory agent** with a biologically-grounded pipeline
  (`STORE → RETRIEVE → ASSOCIATE → REASON → ACT`), each stage borrowed from a verified SOTA codebase;
2. a **unified dataset builder** over PersonaMem + LoCoMo + PerLTQA + MemoryArena;
3. an **evaluation harness**: MC accuracy, an LLM-judge, a graded **Reasoning Score (RS)**,
  abstention, calibration (ECE/Brier) and bootstrap CIs.

The whole thing **runs offline** with a deterministic mock LLM (no API key), and scales to
real models + real data by flipping `--backend openai` and running the downloaders.

---

## Quickstart (offline, ~5 seconds, no API key)

```bash
git clone <your-repo-url> assomembench && cd assomembench
python scripts/make_sample.py                       # writes data/sample/sample_items.jsonl
python eval/run_eval.py --data data/sample/sample_items.jsonl --backend mock
python -m pytest -q                                  # 6 tests
```

Compare the associative agent against the **store-only ablation** (the gap is the point):

```bash
python eval/run_eval.py --backend mock --ablation full
python eval/run_eval.py --backend mock --ablation memory_only
```



## Real run (real data + real models)

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python data/download.py --all                        # PersonaMem, LoCoMo, PerLTQA, MemoryArena
python data/build_dataset.py                          # -> data/build/items.jsonl
python eval/run_eval.py --data data/build/items.jsonl --backend openai --judge-backend openai
```

---

## The architecture (the "special map")

```
 raw user turns
      │  STORE         store.extract_facts → make_notes            [Mem0]
      ▼
 MemoryNotes ──ASSOCIATE associate.build_links  (graph edges)      [A-MEM]
      │
      │   (a query / request arrives)
      ▼
 RETRIEVE   retrieve.retrieve  =  recency × relevance × importance [Generative Agents]
      ▼
 ASSOCIATE  associate.associate = Personalized PageRank spread     [HippoRAG]
      ▼                            (surfaces facts that are *linked* but not directly matched
      │                             → the substrate for a NEW inferred preference)
 REASON     reason.answer_item / reflect_insight                   [Generative Agents reflection]
      ▼                            (insight stored back WITH evidence ids → explainable)
 ACT/UPDATE consolidate (Ebbinghaus forgetting) → AgentAnswer      [MemoryBank]
```

Every block maps to a specific file in a SOTA repo — see `docs/architecture_map.html`
(interactive) for the side-by-side "borrowed code → our code" teardown.


| Stage            | File                         | Borrowed from (verified)                        |
| ---------------- | ---------------------------- | ----------------------------------------------- |
| STORE            | `src/assomem/store.py`       | Mem0 `FACT_RETRIEVAL_PROMPT`, `_create_memory`  |
| RETRIEVE / MATCH | `src/assomem/retrieve.py`    | Generative Agents `new_retrieve`                |
| ASSOCIATE        | `src/assomem/associate.py`   | A-MEM `process_memory` + HippoRAG `run_ppr`     |
| REASON           | `src/assomem/reason.py`      | Generative Agents `run_reflect`                 |
| CONSOLIDATE      | `src/assomem/consolidate.py` | MemoryBank Ebbinghaus curve (bug-fixed)         |
| JUDGE            | `eval/judge.py`              | G-Eval + MT-Bench/FastChat swap                 |
| METRICS (RS)     | `eval/metrics.py`            | HotpotQA joint-EM, IFEval, FollowBench, PRM800K |


## Repository layout

```
associative-memory-bench/
├── README.md                  ← you are here
├── requirements.txt
├── config/default.yaml
├── data/
│   ├── README.md              ← the "special map": why each dataset + how they connect
│   ├── download.py            ← pull the 4 REAL datasets
│   ├── build_dataset.py       ← transform → unified BenchItems
│   └── sample/sample_items.jsonl
├── src/assomem/               ← the agent (one file per pipeline stage)
│   ├── schema.py  store.py  retrieve.py  associate.py  reason.py
│   ├── consolidate.py  agent.py  llm.py  __init__.py
├── eval/
│   ├── metrics.py  judge.py  run_eval.py
├── tests/test_pipeline.py
├── scripts/make_sample.py
└── docs/
    ├── METHOD.md              ← the paper Method section (also delivered as .docx)
    └── architecture_map.html  ← interactive teardown + special map
```



## The Reasoning Score (RS)

For a long-horizon item where step *k* adds constraint *c_k* and the final answer must
satisfy all of them (xₖ ∈ [0,1] satisfaction, p̂ = self-reported confidence, g = ∏ xₖ):

```
w̃ₖ = γ^(k-1) / Σ γ^(j-1)
RS  = (1-λ)·Σ w̃ₖ·xₖ  +  λ·∏ xₖ  −  β·(p̂ − g)²
```

λ=1 → strict joint-EM (HotpotQA); λ=0 → pure partial credit (IFEval/FollowBench).
The report also prints accuracy, abstention, ECE/Brier calibration, and bootstrap CIs.

## Ablations (which biological component matters?)

`--ablation full | memory_only | no_assoc | no_reflect`. `memory_only` is plain RAG
(store + retrieve, no association/reflection) — the "stores facts but can't infer" baseline
the research question targets.

## Citing the sources

See `docs/METHOD.md` and `data/README.md` for the full verified citation list
(PersonaMem, LoCoMo, PerLTQA, MemoryArena, Mem0, A-MEM, HippoRAG, Generative Agents,
MemoryBank, Zep/Graphiti, Modern Hopfield, HotpotQA, IFEval, FollowBench, G-Eval, MT-Bench).
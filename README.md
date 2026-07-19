# AssoMem — Associative Memory Benchmark

Gold data across five everyday domains (600 items each): work, hobby, health, social, finance.

```
src/data/{domain}/{associative|distractor|absence}/
tools/                        # generators
manifests/                    # gate / release reports
judge/LLM judge/…             # LLM-as-judge prompts (to be added)
docs/                         # related documentation
```

See [STRUCTURE.md](STRUCTURE.md).

```bash
python3 tools/hobby/bin/generate_hobby_habit_gold_batch.py --scenarios S1-S20
```

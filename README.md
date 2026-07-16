# AssoMem — Associative Memory Benchmark Pilot

v2 gold pilot data (hobby / health / work), 600 items per domain.

```
src/data/hobby|health|work/   # JSON samples
tools/                        # generators
manifests/                    # gate reports
```

See [STRUCTURE.md](STRUCTURE.md).

```bash
python3 tools/hobby/bin/generate_hobby_habit_gold_batch.py --scenarios S1-S20
```

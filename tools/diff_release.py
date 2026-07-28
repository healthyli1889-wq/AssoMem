"""Exact diff between the source records and what the release ships.

Reports every key removed, every value changed, and the count of records affected,
per domain — so the transformations can be reviewed rather than taken on trust.

    python3 tools/diff_release.py --release /tmp/final_release
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

SOURCES = {
    "social": "staging/social-vnext/social/candidates-s1-s20-full",
    "hobby": "staging/hobby-vnext/hobby/candidates-s1-s20-full",
    "finance": "staging/finance-vnext/finance/candidates-s1-s20-v3",
    "work": "/tmp/work_data",
    "health": "/tmp/health_data",
}


def flatten(node, prefix="") -> dict[str, object]:
    out: dict[str, object] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                out.update(flatten(value, path))
            else:
                out[path] = value
    elif isinstance(node, list):
        for index, value in enumerate(node):
            path = f"{prefix}[{index}]"
            if isinstance(value, (dict, list)):
                out.update(flatten(value, path))
            else:
                out[path] = value
    return out


def generalise(path: str) -> str:
    """context[3].dialogue[0].content -> context[].dialogue[].content"""
    out, depth = [], 0
    for char in path:
        if char == "[":
            depth += 1
            out.append("[")
        elif char == "]":
            depth -= 1
            out.append("]")
        elif depth == 0:
            out.append(char)
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, required=True)
    args = parser.parse_args()
    repo = Path.cwd()

    for domain, source_root in SOURCES.items():
        source_root = Path(source_root) if source_root.startswith("/") else repo / source_root
        removed: Counter = Counter()
        added: Counter = Counter()
        changed: Counter = Counter()
        changed_examples: dict[str, tuple] = {}
        records_touched: set[str] = set()
        total = 0

        for arm in ("associative", "distractor", "absence"):
            for path in sorted((source_root / arm).glob("*.json")):
                release_path = args.release / "data" / domain / arm / path.name
                if not release_path.is_file():
                    print(f"  MISSING in release: {domain}/{arm}/{path.name}")
                    continue
                total += 1
                before = flatten(json.loads(path.read_text(encoding="utf-8")))
                after = flatten(json.loads(release_path.read_text(encoding="utf-8")))
                touched = False
                for key in before.keys() - after.keys():
                    removed[generalise(key)] += 1
                    touched = True
                for key in after.keys() - before.keys():
                    added[generalise(key)] += 1
                    touched = True
                for key in before.keys() & after.keys():
                    if before[key] != after[key]:
                        general = generalise(key)
                        changed[general] += 1
                        changed_examples.setdefault(general, (path.name, before[key], after[key]))
                        touched = True
                if touched:
                    records_touched.add(path.name)

        print(f"\n{'='*84}\n{domain}: {total} records, {len(records_touched)} touched")
        if removed:
            print("  keys REMOVED (count of records):")
            for key, n in sorted(removed.items()):
                print(f"    - {key:52s} {n}")
        if added:
            print("  keys ADDED:")
            for key, n in sorted(added.items()):
                print(f"    + {key:52s} {n}")
        if changed:
            print("  values CHANGED:")
            for key, n in sorted(changed.items()):
                name, b, a = changed_examples[key]
                print(f"    ~ {key:52s} {n}")
                print(f"        in {name}")
                print(f"        before: {str(b)[:110]}")
                print(f"        after : {str(a)[:110]}")
        if not (removed or added or changed):
            print("  identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

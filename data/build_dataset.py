"""
Transform the four RAW base datasets into ONE unified set of BenchItems
(the "first organized, clean, vertical dataset for associative memory").

    python data/build_dataset.py --out data/build/items.jsonl

Each source is mapped onto the BenchItem schema (see data/README.md for the special map):

  PersonaMem  -> associative / generalize items: stored_context = persona history slice;
                 keep question_type in {suggest_new, recommend, generalize}; options + gold.
  LoCoMo      -> long_horizon items: stored_context = sessions; constraints = chained
                 cross-session event facts; evidence_ids from `qa.evidence`.
  PerLTQA     -> associative items from profile+events; evidence = memory anchor.
  MemoryArena -> memory_to_action items: early subtasks = stored prefs; later subtask
                 answer = action_gold.

This script is defensive: each loader is wrapped so a missing dataset is skipped with a
warning rather than crashing the build.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# question types we keep from PersonaMem because they require INFERENCE, not recall
INFER_TYPES = {"suggest new ideas", "provide preference-aligned recommendations",
               "generalize to new scenarios", "suggest_new", "recommend", "generalize"}


def _load_jsonl(path: str) -> List[Dict]:
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_personamem() -> List[Dict]:
    items = []
    base = os.path.join(RAW, "personamem")
    rows = []
    if os.path.isdir(base):
        for fn in os.listdir(base):
            rows += _load_jsonl(os.path.join(base, fn))
    for i, r in enumerate(rows):
        qtype = str(r.get("question_type", "")).lower()
        if INFER_TYPES and qtype and qtype not in INFER_TYPES:
            continue
        ctx = r.get("shared_context") or r.get("context") or []
        if isinstance(ctx, str):
            ctx = [ctx]
        opts = r.get("all_options") or r.get("options") or []
        items.append(dict(
            item_id=f"personamem-{i}", source="personamem", scenario="associative",
            stored_context=[str(c) for c in ctx][:200],
            query=r.get("user_question_or_message") or r.get("question") or "",
            gold=r.get("correct_answer") or r.get("answer") or "",
            options=[str(o) for o in opts],
            question_type=qtype or "suggest_new",
            meta={"topic": r.get("topic"), "distance": r.get("distance_to_ref_in_tokens")},
        ))
    return items


def build_locomo() -> List[Dict]:
    items = []
    path = os.path.join(RAW, "locomo", "data", "locomo10.json")
    if not os.path.exists(path):
        return items
    data = json.load(open(path))
    for ci, conv in enumerate(data):
        sessions, c = [], conv.get("conversation", {})
        for k in sorted(k for k in c if k.startswith("session_") and not k.endswith("date_time")):
            for turn in c[k]:
                sessions.append(f"{turn.get('speaker','')}: {turn.get('text','')}")
        for qi, qa in enumerate(conv.get("qa", [])):
            ev = qa.get("evidence", [])
            constraints = [str(e) for e in ev] if isinstance(ev, list) else []
            items.append(dict(
                item_id=f"locomo-{ci}-{qi}", source="locomo", scenario="long_horizon",
                stored_context=sessions[:400], query=qa.get("question", ""),
                gold=str(qa.get("answer", "")), options=[],
                evidence_ids=[str(e) for e in ev] if isinstance(ev, list) else [],
                constraints=constraints[:6],
                question_type=f"category_{qa.get('category','')}",
                is_answerable=(qa.get("category") != 5),       # category 5 = adversarial
            ))
    return items


def build_perltqa() -> List[Dict]:
    items, base = [], os.path.join(RAW, "PerLTQA")
    if not os.path.isdir(base):
        return items
    # PerLTQA ships JSON under data/; we scan for QA-like files defensively.
    for root, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith(".json"):
                continue
            try:
                data = json.load(open(os.path.join(root, fn)))
            except Exception:
                continue
            rows = data if isinstance(data, list) else data.get("data", [])
            if not isinstance(rows, list):
                continue
            for i, r in enumerate(rows):
                if not isinstance(r, dict) or "question" not in r:
                    continue
                items.append(dict(
                    item_id=f"perltqa-{fn}-{i}", source="perltqa", scenario="associative",
                    stored_context=[str(r.get("reference memory") or r.get("reference") or "")],
                    query=r.get("question", ""), gold=str(r.get("answer", "")), options=[],
                    evidence_ids=[str(r.get("memory anchor", ""))],
                    question_type="associative_recall",
                ))
            if items:
                break
    return items


def build_memoryarena() -> List[Dict]:
    items, base = [], os.path.join(RAW, "memoryarena")
    if not os.path.isdir(base):
        return items
    for fn in os.listdir(base):
        for i, r in enumerate(_load_jsonl(os.path.join(base, fn))):
            qs = r.get("questions") or []
            ans = r.get("answers") or []
            bg = r.get("backgrounds")
            ctx = ([bg] if isinstance(bg, str) else list(bg or [])) + [str(q) for q in qs[:-1]]
            items.append(dict(
                item_id=f"memarena-{fn}-{i}", source="memoryarena", scenario="memory_to_action",
                stored_context=[str(c) for c in ctx][:200],
                query=str(qs[-1]) if qs else "", gold=str(ans[-1]) if ans else "",
                options=[], action_gold=str(ans[-1]) if ans else None,
                constraints=[str(a) for a in ans[:-1]][:6],
                question_type="memory_to_action",
            ))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "build", "items.jsonl"))
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    all_items: List[Dict] = []
    for name, fn in [("PersonaMem", build_personamem), ("LoCoMo", build_locomo),
                     ("PerLTQA", build_perltqa), ("MemoryArena", build_memoryarena)]:
        try:
            got = fn()
            print(f"[{name}] built {len(got)} items")
            all_items += got
        except Exception as e:
            print(f"[{name}] skipped: {e}")

    if not all_items:
        print("\nNo raw data found. Run `python data/download.py --all` first, "
              "or use the bundled sample at data/sample/sample_items.jsonl.")
        return
    with open(args.out, "w") as f:
        for it in all_items:
            f.write(json.dumps(it) + "\n")
    print(f"\nWrote {len(all_items)} unified items -> {args.out}")


if __name__ == "__main__":
    main()

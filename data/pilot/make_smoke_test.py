"""
Generate smoke test annotation CSV for 50 items (LoCoMo + LongMemEval).

    python data/pilot/make_smoke_test.py

Output: data/pilot/smoke_test_50.csv

Columns split into three groups:
  [AUTO]  pre-filled from build_dataset.py logic
  [MANUAL] annotator fills in; blank = to-be-determined
  [DECISION] PASS/FAIL + exclusion reason

Sampling strategy (50 total):
  LoCoMo (25 items):
    - 12 strong-F9 / cross-session  (A2 priority)
    - 8  A1 relational_binding (cat=3, same-session, evidence≥2)
    - 5  cat=4 open-ended preference (A2 cue_chain)
  LongMemEval (25 items):
    - 10 multi-session A1
    - 8  knowledge-update A4
    - 4  single-session-preference A2 (F9=False → working_memory_ctrl)
    - 3  abstention A5_absence
"""
import csv
import json
import os
import random

random.seed(42)

ITEMS_PATH = os.path.join(os.path.dirname(__file__), "..", "build", "items.jsonl")
OUT_PATH = os.path.join(os.path.dirname(__file__), "smoke_test_50.csv")

COLS = [
    # identity
    "item_id", "source", "question_type",
    # [AUTO] annotation labels
    "association_type",     # A1/A2/A3/A4 (auto)
    "a1_nodes",             # evidence graph size (auto; proxy for connectivity)
    "f9_persistent_memory", # bool (auto)
    "f9_strength",          # strong/weak/absent (auto, LoCoMo only)
    "temporal_state_op",    # update/deletion/conflict/... (auto where applicable)
    "a5_probes_auto",       # auto-detected probe types
    # item content (truncated)
    "query",
    "gold",
    "stored_context_5lines",
    # [MANUAL] A1 — Relational Binding
    "a1_graph_connected",   # bool: is the evidence graph connected? (manual)
    "a1_remove_node_breaks",# bool: removing any key evidence node changes answer? (manual)
    # [MANUAL] A2 — Cue Indirection Path
    "a2_cue_node",          # text: the query cue that triggers memory retrieval (manual)
    "a2_bridge_nodes",      # text: intermediate memory nodes (csv: node1|node2) (manual)
    "a2_answer_node",       # text: the final memory node that yields the answer (manual)
    # [MANUAL] A3 — Cross-Context Bridge
    "a3_bridge_in_memory",  # bool: bridge rule comes from memory, not world knowledge (manual)
    # [MANUAL] A4 — Temporal State Operator
    "a4_op_confirmed",      # text: confirm/correct the auto temporal_state_op (manual)
    "a4_valid_time",        # text: when was the state valid? (e.g. "session 1 date") (manual)
    # [MANUAL] A5 — Counterfactual Necessity (at least 1 must be True to PASS)
    "a5_no_memory_fails",       # bool: remove all memory → answer changes? (manual)
    "a5_remove_bridge_fails",   # bool: remove bridge node → answer changes? (manual)
    "a5_stale_memory_fails",    # bool: use only outdated memory → wrong answer? (manual)
    "a5_distractor_swap_fails", # bool: swap distractor in → answer changes? (manual)
    # [DECISION]
    "verdict",              # PASS / FAIL / BORDERLINE
    "exclusion_reason",     # if FAIL: F9_same_session | A1_missing_edge | A3_world_knowledge |
                            #          A5_no_probe | insufficient_evidence | other
    "notes",                # free text
]


def load_items():
    items = []
    with open(ITEMS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def sample_locomo(items):
    loc = [d for d in items if d["source"] == "locomo"]

    strong_f9 = [d for d in loc
                 if d["meta"].get("f9_strength") == "strong"]
    a1_items = [d for d in loc
                if d["meta"].get("association_type") == "A1_relational_binding"]
    cat4 = [d for d in loc
            if d["question_type"] == "open_ended_preference"
            and d["meta"].get("f9_strength") != "strong"]

    sampled = []
    sampled += random.sample(strong_f9, min(12, len(strong_f9)))
    # Fill remaining from A1 (cat3, same-session, ≥2 evidence)
    a1_sorted = sorted(a1_items, key=lambda d: d["meta"].get("a1_nodes", 0), reverse=True)
    already = {d["item_id"] for d in sampled}
    sampled += [d for d in a1_sorted if d["item_id"] not in already][:8]
    already = {d["item_id"] for d in sampled}
    sampled += random.sample([d for d in cat4 if d["item_id"] not in already],
                             min(5, len(cat4)))
    return sampled[:25]


def sample_lme(items):
    lme = [d for d in items if d["source"] == "longmemeval"]

    a1 = [d for d in lme if d["meta"]["association_type"] == "A1_relational_binding"]
    a4 = [d for d in lme if d["meta"]["association_type"] == "A4_temporal_consistency"]
    a2_wm = [d for d in lme if d["meta"]["association_type"] == "A2_cue_chain"]
    a5_abs = [d for d in lme if d["meta"]["association_type"] == "A5_absence_control"]

    sampled = []
    sampled += random.sample(a1, min(10, len(a1)))
    sampled += random.sample(a4, min(8, len(a4)))
    sampled += random.sample(a2_wm, min(4, len(a2_wm)))
    sampled += random.sample(a5_abs, min(3, len(a5_abs)))
    return sampled[:25]


def make_row(d):
    meta = d.get("meta", {})
    ctx = d.get("stored_context", [])
    # First 5 lines, joined; newlines replaced with pipe for CSV safety
    ctx5 = " | ".join(str(l) for l in ctx[:5]).replace("\n", " ")

    return {
        "item_id": d["item_id"],
        "source": d["source"],
        "question_type": d.get("question_type", ""),
        # AUTO labels
        "association_type": meta.get("association_type", ""),
        "a1_nodes": meta.get("a1_nodes", ""),
        "f9_persistent_memory": meta.get("f9_persistent_memory", ""),
        "f9_strength": meta.get("f9_strength", ""),
        "temporal_state_op": meta.get("temporal_state_operator", ""),
        "a5_probes_auto": "|".join(meta.get("a5_probes", [])),
        # content
        "query": d.get("query", ""),
        "gold": d.get("gold", ""),
        "stored_context_5lines": ctx5,
        # MANUAL — blanks for annotator
        "a1_graph_connected": "",
        "a1_remove_node_breaks": "",
        "a2_cue_node": "",
        "a2_bridge_nodes": "",
        "a2_answer_node": "",
        "a3_bridge_in_memory": "",
        "a4_op_confirmed": "",
        "a4_valid_time": "",
        "a5_no_memory_fails": "",
        "a5_remove_bridge_fails": "",
        "a5_stale_memory_fails": "",
        "a5_distractor_swap_fails": "",
        # DECISION
        "verdict": "",
        "exclusion_reason": "",
        "notes": "",
    }


def main():
    items = load_items()
    loc_sample = sample_locomo(items)
    lme_sample = sample_lme(items)
    combined = loc_sample + lme_sample
    print(f"Sampled: LoCoMo={len(loc_sample)}, LongMemEval={len(lme_sample)}, total={len(combined)}")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLS)
        writer.writeheader()
        for d in combined:
            writer.writerow(make_row(d))

    print(f"Wrote {OUT_PATH}")
    print()

    # Summary stats
    from collections import Counter
    loc = [d for d in combined if d["source"] == "locomo"]
    lme = [d for d in combined if d["source"] == "longmemeval"]
    print("LoCoMo breakdown:")
    print("  assoc_type:", Counter(d["meta"]["association_type"] for d in loc))
    print("  f9_strength:", Counter(d["meta"]["f9_strength"] for d in loc))
    print("LongMemEval breakdown:")
    print("  assoc_type:", Counter(d["meta"]["association_type"] for d in lme))
    print("  f9:", Counter(d["meta"]["f9_persistent_memory"] for d in lme))


if __name__ == "__main__":
    main()

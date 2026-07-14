"""
Full-loop tracer: runs the STORE→RETRIEVE→ASSOCIATE→REASON→JUDGE pipeline
on a small pilot set and prints every intermediate stage so you can see
exactly what the agent does at each step.

    python eval/run_eval_trace.py --data data/pilot/pilot_30.jsonl --n 6

Shows:
  1. STORE   : facts extracted + notes embedded
  2. LINKS   : A-MEM graph edges built
  3. REFLECT : Generative Agents insight generated
  4. RETRIEVE: top-k notes scored (recency × relevance × importance)
  5. ASSOCIATE: PPR-spread notes that weren't directly retrieved
  6. REASON  : answer produced from working memory
  7. JUDGE   : score vs gold
  8. METRICS : RS, accuracy, abstention, calibration per item + aggregate
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)

from assomem import AgentConfig, AssociativeMemoryAgent, BenchItem, LLM
import assomem.store as S
import assomem.associate as A
import assomem.retrieve as RT
import assomem.reason as R
import assomem.consolidate as C
import metrics as M
from judge import judge_answer

W = 90  # display width


def hr(char="─"):
    print(char * W)


def wrap(text, indent=4):
    return textwrap.fill(str(text), width=W - indent, initial_indent=" " * indent,
                         subsequent_indent=" " * indent)


def run_trace(item: BenchItem, llm: LLM, cfg: AgentConfig, judge_llm: LLM):
    hr("═")
    print(f"  ITEM  {item.item_id}")
    print(f"  src={item.source}  scenario={item.scenario}  qtype={item.question_type}"
          f"  answerable={item.is_answerable}")
    hr()
    print(wrap(f"QUERY : {item.query}"))
    print(wrap(f"GOLD  : {item.gold}"))
    hr()

    # ── STORE ──────────────────────────────────────────────────────────────────
    print("▶ STAGE 1 · STORE  (Mem0: extract atomic facts → embed → deduplicate)")
    facts = S.extract_facts(item.stored_context, llm)
    notes = S.make_notes(facts, llm)
    print(f"  context lines ingested : {len(item.stored_context)}")
    print(f"  facts extracted        : {len(facts)}")
    print(f"  MemoryNotes created    : {len(notes)}")
    for n in notes[:4]:
        print(f"    note [{n.category:10}|poig={n.poignancy:.1f}] {n.content[:70]}")
    if len(notes) > 4:
        print(f"    ... +{len(notes)-4} more")

    # ── FORGETTING ─────────────────────────────────────────────────────────────
    if cfg.use_forgetting:
        before = len(notes)
        notes = C.consolidate(notes)
        pruned = before - len(notes)
        print(f"  Ebbinghaus consolidate : kept {len(notes)}, pruned {pruned} (retention<0.05)")

    # ── LINKS (A-MEM graph) ────────────────────────────────────────────────────
    edges = []
    if cfg.use_links:
        print("\n▶ STAGE 2 · LINKS  (A-MEM: build associative graph edges)")
        edges = A.build_links(notes)
        print(f"  edges built : {len(edges)}")
        for e in edges[:3]:
            print(f"    [{e.relation:12}| w={e.weight:.2f}]  "
                  f"{e.fact[:65]}")
        if len(edges) > 3:
            print(f"    ... +{len(edges)-3} more")

    # ── REFLECT (Generative Agents insight) ───────────────────────────────────
    insight = None
    if cfg.use_reflection:
        print("\n▶ STAGE 3 · REFLECT  (Gen. Agents: infer higher-level preference insight)")
        insight = R.reflect_insight(notes[-12:], llm)
        if insight:
            notes.append(insight)
            print(f"  insight generated : {insight.content[:80]}")
            print(f"  evidence ids      : {insight.evidence}")
        else:
            print("  no insight generated (not enough salient memory)")

    # ── RETRIEVE ───────────────────────────────────────────────────────────────
    print("\n▶ STAGE 4 · RETRIEVE  (Gen. Agents: recency × relevance × importance)")
    retrieved = RT.retrieve(item.query, notes, llm, top_k=cfg.top_k_retrieve)
    print(f"  top-{cfg.top_k_retrieve} retrieved notes:")
    for note, score in retrieved[:5]:
        print(f"    [score={score:.3f}|{note.kind:7}|{note.category:10}] {note.content[:60]}")

    # ── ASSOCIATE (HippoRAG PPR) ───────────────────────────────────────────────
    seed_notes = [n for n, _ in retrieved]
    assoc_notes = []
    if cfg.use_association and edges:
        print("\n▶ STAGE 5 · ASSOCIATE  (HippoRAG: Personalized PageRank spreading activation)")
        assoc = A.associate(seed_notes, notes, edges,
                            damping=cfg.ppr_damping, top_k=cfg.top_k_associate)
        seen = {n.note_id for n in seed_notes}
        assoc_notes = [n for n, _ in assoc if n.note_id not in seen]
        print(f"  seeds (direct matches)  : {len(seed_notes)}")
        print(f"  spread (newly activated): {len(assoc_notes)}  ← these are the 'associated but not retrieved' facts")
        for n, r in [(n, r) for n, r in assoc if n.note_id not in seen][:3]:
            print(f"    [ppr={r:.4f}|{n.category:10}] {n.content[:65]}")
    else:
        print("\n  (association disabled in this ablation)")

    working = seed_notes + assoc_notes

    # ── REASON ─────────────────────────────────────────────────────────────────
    print(f"\n▶ STAGE 6 · REASON  (Gen. Agents: produce answer from {len(working)} working-memory notes)")
    ans = R.answer_item(item, working, llm)
    print(wrap(f"  answer     : {ans.answer}"))
    print(f"  confidence : {ans.confidence:.2f}")
    print(f"  abstained  : {ans.abstained}")
    print(f"  rationale  : {ans.rationale[:80]}")
    print(f"  used notes : {len(ans.used_evidence)} ids")

    # ── JUDGE + METRICS ────────────────────────────────────────────────────────
    print("\n▶ STAGE 7 · JUDGE + METRICS")
    if item.is_mc:
        correct = M.mc_correct(ans.chosen_option_idx, item.options, item.gold)
        verdict = "correct" if correct == 1.0 else "wrong"
        jr = {"verdict": verdict, "score01": correct, "constraint_satisfaction": []}
        print(f"  MC: chosen idx={ans.chosen_option_idx}  correct={correct}")
    else:
        jr = judge_answer(item, ans, judge_llm)
        correct = 1.0 if jr["verdict"] == "yes" else jr["score01"]
        print(f"  judge verdict : {jr['verdict']}  score01={jr['score01']:.2f}")
        print(f"  rationale     : {str(jr.get('rationale',''))[:80]}")

    cs = jr.get("constraint_satisfaction") or []
    if not cs and item.constraints:
        cs = [1.0 if correct >= 0.6 else 0.0] * len(item.constraints)
    rs = M.reasoning_score(cs, confidence=ans.confidence) if cs else \
         {"rs": correct, "rs_strict": correct, "rs_partial": correct,
          "gate": correct, "calib_penalty": 0.0}
    abst = M.abstention_score(answered=not ans.abstained, is_answerable=item.is_answerable)

    print(f"  RS={rs['rs']:.3f}  strict={rs['rs_strict']:.3f}  "
          f"partial={rs['rs_partial']:.3f}  calib_pen={rs['calib_penalty']:.3f}")
    print(f"  abstention_score={abst:.1f}  "
          f"({'correct abstain' if abst==1 and not item.is_answerable else 'answered' if item.is_answerable else 'should have abstained'})")

    return {
        "item_id": item.item_id, "source": item.source,
        "scenario": item.scenario, "question_type": item.question_type,
        "correct": correct, "rs": rs["rs"], "rs_strict": rs["rs_strict"],
        "confidence": ans.confidence, "abstention": abst,
        "answer": ans.answer, "gold": item.gold,
        "num_notes": len(notes), "num_edges": len(edges),
        "num_assoc_notes": len(assoc_notes),
        "judge_verdict": jr.get("verdict", ""),
    }


def print_aggregate(results, ablation):
    hr("═")
    print(f"  AGGREGATE REPORT  —  ablation: {ablation}  (n={len(results)})")
    hr()
    from collections import defaultdict, Counter
    correct_flags = [r["correct"] for r in results]
    rs_vals = [r["rs"] for r in results]
    conf_vals = [r["confidence"] for r in results]
    abst_vals = [r["abstention"] for r in results]

    acc, acc_lo, acc_hi = M.bootstrap_ci(correct_flags)
    rs_m, rs_lo, rs_hi = M.bootstrap_ci(rs_vals)
    ece = M.expected_calibration_error(conf_vals, correct_flags)
    brier = M.brier(conf_vals, correct_flags)

    print(f"  accuracy        : {acc:.3f}  CI95[{acc_lo:.3f}, {acc_hi:.3f}]")
    print(f"  reasoning score : {rs_m:.3f}  CI95[{rs_lo:.3f}, {rs_hi:.3f}]")
    print(f"  abstention      : {sum(abst_vals)/len(abst_vals):.3f}")
    print(f"  ECE             : {ece:.3f}   Brier: {brier:.3f}")
    print()

    by_scenario = defaultdict(list)
    by_qtype = defaultdict(list)
    for r in results:
        by_scenario[r["scenario"]].append(r["rs"])
        by_qtype[r["question_type"]].append(r["correct"])
    print("  RS by scenario:")
    for sc, vals in sorted(by_scenario.items()):
        print(f"    {sc:22} n={len(vals):3}  RS={sum(vals)/len(vals):.3f}")
    print()
    print("  accuracy by question_type:")
    for qt, vals in sorted(by_qtype.items()):
        print(f"    {qt:30} n={len(vals):3}  acc={sum(vals)/len(vals):.3f}")
    print()

    notes_mean = sum(r["num_notes"] for r in results) / len(results)
    edges_mean = sum(r["num_edges"] for r in results) / len(results)
    assoc_mean = sum(r["num_assoc_notes"] for r in results) / len(results)
    print(f"  avg notes/item  : {notes_mean:.1f}")
    print(f"  avg edges/item  : {edges_mean:.1f}")
    print(f"  avg assoc spread: {assoc_mean:.1f}  (notes activated by PPR but not directly retrieved)")
    hr("═")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/pilot/pilot_30.jsonl")
    ap.add_argument("--backend", default="mock", choices=["mock", "openai"])
    ap.add_argument("--judge-backend", default=None)
    ap.add_argument("--ablation", default="full",
                    choices=["full", "memory_only", "no_assoc", "no_reflect"])
    ap.add_argument("--n", type=int, default=None, help="limit to first N items")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    judge_backend = args.judge_backend or args.backend

    items_raw = []
    with open(args.data) as f:
        for line in f:
            line = line.strip()
            if line:
                items_raw.append(BenchItem.from_dict(json.loads(line)))
    if args.n:
        items_raw = items_raw[:args.n]

    agent_llm = LLM(backend=args.backend)
    judge_llm = LLM(backend=judge_backend)

    if args.ablation == "full":
        cfg = AgentConfig()
    elif args.ablation == "memory_only":
        cfg = AgentConfig.memory_only()
    elif args.ablation == "no_assoc":
        cfg = AgentConfig(use_association=False)
    else:
        cfg = AgentConfig(use_reflection=False)

    print()
    print("═" * W)
    print(f"  AssoMemBench · Full-Loop Trace")
    print(f"  ablation={args.ablation}  backend={args.backend}  items={len(items_raw)}")
    print(f"  pipeline flags: association={cfg.use_association}  links={cfg.use_links}"
          f"  reflection={cfg.use_reflection}  forgetting={cfg.use_forgetting}")
    print("═" * W)

    results = []
    for item in items_raw:
        r = run_trace(item, agent_llm, cfg, judge_llm)
        results.append(r)

    print_aggregate(results, args.ablation)

    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w") as f:
            json.dump({"ablation": args.ablation, "n": len(results), "items": results}, f, indent=2)
        print(f"  wrote {args.out}")


if __name__ == "__main__":
    main()

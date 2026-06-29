"""
End-to-end benchmark harness.

    python eval/run_eval.py --data data/sample/sample_items.jsonl --backend mock
    python eval/run_eval.py --data data/build/items.jsonl --backend openai --ablation full

Runs the agent over every BenchItem, scores with MC accuracy / LLM-judge, computes the
Reasoning Score for long-horizon items, abstention, calibration (ECE/Brier) and bootstrap
CIs, and writes a JSON report. Designed to run OFFLINE with --backend mock.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List

# make src/ and eval/ importable when run as a script
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)

from assomem import AgentConfig, AssociativeMemoryAgent, BenchItem, LLM   # noqa: E402
import metrics as M                                                       # noqa: E402
from judge import judge_answer                                           # noqa: E402


def load_items(path: str) -> List[BenchItem]:
    items = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(BenchItem.from_dict(json.loads(line)))
    return items


def constraint_satisfaction(item: BenchItem, ans, judge_llm: LLM) -> List[float]:
    """Per-constraint x_k for the Reasoning Score."""
    if not item.constraints:
        return []
    if item.is_mc:
        # correct option => all constraints satisfied; else none (conservative)
        ok = M.mc_correct(ans.chosen_option_idx, item.options, item.gold)
        return [ok] * len(item.constraints)
    res = judge_answer(item, ans, judge_llm)
    cs = res.get("constraint_satisfaction") or []
    if len(cs) != len(item.constraints):
        base = res["score01"]
        cs = [1.0 if base >= 0.6 else 0.0] * len(item.constraints)
    return cs


def evaluate(items: List[BenchItem], agent_backend: str, judge_backend: str,
             ablation: str) -> Dict:
    agent_llm = LLM(backend=agent_backend)
    judge_llm = LLM(backend=judge_backend)
    cfg = AgentConfig() if ablation == "full" else AgentConfig.memory_only()
    if ablation == "no_assoc":
        cfg = AgentConfig(use_association=False)
    if ablation == "no_reflect":
        cfg = AgentConfig(use_reflection=False)

    agent = AssociativeMemoryAgent(agent_llm, cfg)

    per_item, by_type, by_scenario = [], defaultdict(list), defaultdict(list)
    confidences, correct_flags = [], []
    rs_values, abst_values = [], []

    for item in items:
        agent.reset()
        agent.ingest(item.stored_context)
        ans = agent.answer(item)

        if item.is_mc:
            correct = M.mc_correct(ans.chosen_option_idx, item.options, item.gold)
        else:
            jr = judge_answer(item, ans, judge_llm)
            correct = 1.0 if jr["verdict"] == "yes" else jr["score01"]

        cs = constraint_satisfaction(item, ans, judge_llm)
        rs = M.reasoning_score(cs, confidence=ans.confidence) if cs else \
            {"rs": correct, "rs_strict": correct, "rs_partial": correct,
             "gate": correct, "calib_penalty": 0.0}
        abst = M.abstention_score(answered=not ans.abstained, is_answerable=item.is_answerable)

        per_item.append({"item_id": item.item_id, "source": item.source,
                         "scenario": item.scenario, "question_type": item.question_type,
                         "correct": correct, "rs": rs["rs"], "rs_strict": rs["rs_strict"],
                         "confidence": ans.confidence, "abstention": abst,
                         "answer": ans.answer, "gold": item.gold})
        by_type[item.question_type].append(correct)
        by_scenario[item.scenario].append(rs["rs"])
        confidences.append(ans.confidence)
        correct_flags.append(correct)
        rs_values.append(rs["rs"])
        abst_values.append(abst)

    acc, acc_lo, acc_hi = M.bootstrap_ci(correct_flags)
    rs_mean, rs_lo, rs_hi = M.bootstrap_ci(rs_values)
    report = {
        "ablation": ablation, "n_items": len(items),
        "accuracy": {"mean": acc, "ci95": [acc_lo, acc_hi]},
        "reasoning_score": {"mean": rs_mean, "ci95": [rs_lo, rs_hi]},
        "abstention": sum(abst_values) / len(abst_values) if abst_values else 0.0,
        "calibration": {"ece": M.expected_calibration_error(confidences, correct_flags),
                        "brier": M.brier(confidences, correct_flags)},
        "accuracy_by_question_type": {k: sum(v) / len(v) for k, v in by_type.items()},
        "rs_by_scenario": {k: sum(v) / len(v) for k, v in by_scenario.items()},
        "per_item": per_item,
    }
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(HERE, "..", "data", "sample", "sample_items.jsonl"))
    ap.add_argument("--backend", default="mock", choices=["mock", "openai"])
    ap.add_argument("--judge-backend", default=None, choices=[None, "mock", "openai"])
    ap.add_argument("--ablation", default="full",
                    choices=["full", "memory_only", "no_assoc", "no_reflect"])
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results.json"))
    args = ap.parse_args()
    judge_backend = args.judge_backend or args.backend

    items = load_items(args.data)
    report = evaluate(items, args.backend, judge_backend, args.ablation)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n=== AssoMemBench report ({args.ablation}, backend={args.backend}) ===")
    print(f"items:            {report['n_items']}")
    print(f"accuracy:         {report['accuracy']['mean']:.3f} "
          f"CI95{[round(x,3) for x in report['accuracy']['ci95']]}")
    print(f"reasoning score:  {report['reasoning_score']['mean']:.3f} "
          f"CI95{[round(x,3) for x in report['reasoning_score']['ci95']]}")
    print(f"abstention:       {report['abstention']:.3f}")
    print(f"calibration ECE:  {report['calibration']['ece']:.3f} | Brier: {report['calibration']['brier']:.3f}")
    print(f"acc by type:      {report['accuracy_by_question_type']}")
    print(f"rs by scenario:   { {k: round(v,3) for k,v in report['rs_by_scenario'].items()} }")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()

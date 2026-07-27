"""One-item end-to-end smoke test: solver on every arm, then the validator.

Cheap sanity check before spending a full run. Confirms the profile loads, arms
materialize, both endpoints answer in the required JSON shape, and each arm's
decision matches its gold. Prints token usage so a full run can be costed.

    source my_config.sh && python3 experiments/assomem_harness/smoke_vnext.py --pair AMB_SC_S1_U01
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "query_validity"))

from arms import materialize_vnext_arms  # noqa: E402
from clients import call_model_with_usage  # noqa: E402
from dataset import discover_vnext_items  # noqa: E402
from models import load_roles, validate_solver_validator_independence  # noqa: E402
from profile import load_profile  # noqa: E402
from protocol import score_prompt, solver_prompt  # noqa: E402
from workflow import score_solver_answer, validate_solver_answer  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", default="AMB_SC_S1_U01")
    parser.add_argument("--arms", default="full,a_only,b_only,link_broken,distractor,absence")
    parser.add_argument("--skip-validator", action="store_true")
    args = parser.parse_args()

    import os

    profile = load_profile(Path(os.environ["ASSOMEM_PROFILE"]))
    data_root = Path(os.environ["ASSOMEM_DATA_ROOT"])
    domain = os.environ["ASSOMEM_DOMAIN"]
    roles = load_roles()
    validate_solver_validator_independence(roles)
    print(f"solver    : {roles['solver'].model} @ {roles['solver'].base_url}")
    print(f"validator : {roles['validator'].model} @ {roles['validator'].base_url}")

    items = discover_vnext_items(data_root, profile, domain)
    item = next((row for row in items if row.item_id == args.pair), None)
    if item is None:
        print(f"pair {args.pair} not found among {len(items)} items")
        return 1

    associative = item.arms["associative"]
    print(f"\npair      : {item.item_id}")
    print(f"query_type: {associative['query_type']}   polarity: {associative['polarity']}")
    print(f"query     : {associative['query']}")
    print(f"target    : {associative['answer_contract']['target_proposition']}")

    rendered = materialize_vnext_arms(item, profile)
    totals = {"solver_in": 0, "solver_out": 0, "validator_in": 0, "validator_out": 0}
    agreements = []

    for arm_name in args.arms.split(","):
        arm = rendered[arm_name]
        expected = arm.ground_truth["binary_decision"]
        answer, usage = call_model_with_usage(
            roles["solver"], solver_prompt(arm.visible, profile)
        )
        totals["solver_in"] += usage.get("input_tokens") or 0
        totals["solver_out"] += usage.get("output_tokens") or 0
        problems = validate_solver_answer(answer, profile)
        decision = answer.get("decision")
        match = (decision == "yes") == expected
        agreements.append(match)
        flag = "OK " if match else "MISS"
        print(
            f"\n[{flag}] {arm_name:12s} sessions={len(arm.visible['context']):2d} "
            f"decision={decision!r} expected={'yes' if expected else 'no'} "
            f"cited={answer.get('evidence_session_ids')}"
        )
        if problems:
            print(f"       schema problems: {problems}")
        print(f"       {str(answer.get('answer'))[:220]}")

        if not args.skip_validator and arm_name in {"full", "absence"}:
            judged, v_usage = call_model_with_usage(
                roles["validator"], score_prompt(answer, arm.ground_truth, profile)
            )
            totals["validator_in"] += v_usage.get("input_tokens") or 0
            totals["validator_out"] += v_usage.get("output_tokens") or 0
            scored = score_solver_answer(judged, arm.ground_truth, profile)
            print(f"       validator -> {json.dumps(scored, ensure_ascii=False)}")

    print(f"\narm/gold agreement: {sum(agreements)}/{len(agreements)}")
    print(f"tokens: {totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from behavior import controls_pass
from pipeline import ensure_release_eligible
from quality import deterministic_audit, validate_evaluator_verdict
from review import validate_scenario_gate_0
from schema import CORE_ARMS, render_arms, validate_candidate


REPO = ROOT.parents[1]
CANDIDATE = REPO / "staging/work-vnext/v1/s1/candidates/associative/AMB_WV_s1_anon_001_associative.json"
S1_CANDIDATES = {
    arm: REPO / f"staging/work-vnext/v1/s1/candidates/{arm}/AMB_WV_s1_anon_001_{arm}.json"
    for arm in ("associative", "distractor", "absence")
}


class WorkVnextSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))

    def test_exemplar_passes_structural_validation(self) -> None:
        self.assertEqual(validate_candidate(self.candidate), [])
        audit = deterministic_audit(self.candidate)
        self.assertTrue(audit["pass"])
        self.assertIn("joint_support_for_C", audit["unscored_semantic_clauses"])

    def test_arms_are_distinct_and_source_swap_is_not_link_broken(self) -> None:
        arms = render_arms(self.candidate)
        self.assertTrue(set(CORE_ARMS).issubset(arms))
        self.assertLess(len(arms["a_only"]["context"]), len(arms["full"]["context"]))
        self.assertLess(len(arms["b_only"]["context"]), len(arms["full"]["context"]))
        self.assertTrue(arms["link_broken"]["lineage"]["source_owner_preserved"])
        b_session_id = self.candidate["evidence"]["ev_B"]["session_id"]
        link_broken_session = next(
            s for s in arms["link_broken"]["context"] if s["session_id"] == b_session_id
        )
        self.assertEqual(link_broken_session["speaker_id"], self.candidate["user_id"])
        self.assertNotIn("source_swap", arms)

    def test_rejects_direct_latent_c_leakage(self) -> None:
        invalid = copy.deepcopy(self.candidate)
        invalid["context"][0]["dialogue"][0]["content"] += " " + invalid["latent_C"]["inference"]
        self.assertIn("latent_C is directly leaked in context or query", validate_candidate(invalid))

    def test_schema_accepts_a_nonwork_vnext_domain(self) -> None:
        social = copy.deepcopy(self.candidate)
        social["domain"] = "social"
        self.assertEqual(validate_candidate(social), [])

    def test_evaluator_requires_exact_scores_and_consistent_verdict(self) -> None:
        verdict = {
            "clause_scores": {
                "same_person_temporal_separation": 96,
                "a_only_insufficiency": 96,
                "b_only_insufficiency": 96,
                "joint_support_for_C": 96,
                "C_novelty_no_leakage": 96,
                "query_natural_recall_trigger": 96,
                "link_broken_validity": 96,
                "gold_scoreability": 96,
                "query_taxonomy_compliance": 96,
            },
            "evidence_spans": [],
            "failure_tags": [],
            "revision_instructions": [],
            "overall_verdict": "pass",
        }
        self.assertEqual(validate_evaluator_verdict(verdict), [])
        verdict["clause_scores"]["a_only_insufficiency"] = 95
        self.assertTrue(validate_evaluator_verdict(verdict))

    def test_behavioral_controls_reject_one_control_false_positive(self) -> None:
        records = [
            {
                "arm": arm,
                "expected_mode": "infer_C" if arm == "full" else "withhold_C",
                "status": "scored",
                "validator_verdict": {
                    "condition_correct": True,
                    "asserts_original_C": arm == "full",
                },
            }
            for arm in CORE_ARMS
        ]
        self.assertTrue(controls_pass(records))
        next(record for record in records if record["arm"] == "link_broken")[
            "validator_verdict"
        ]["asserts_original_C"] = True
        self.assertFalse(controls_pass(records))

    def test_release_eligible_candidate_can_advance(self) -> None:
        ensure_release_eligible(self.candidate)

    def test_s1_construct_gate_requires_actual_human_decisions(self) -> None:
        review = REPO / "staging/work-vnext/v1/s1/review/gate_0.csv"
        with self.assertRaisesRegex(ValueError, "scenario Gate 0"):
            validate_scenario_gate_0(review, "work_s1_relational_v1")

    def test_anonymous_s1_is_a_valid_three_file_source_pair(self) -> None:
        candidates = {
            arm: json.loads(path.read_text(encoding="utf-8"))
            for arm, path in S1_CANDIDATES.items()
        }
        for candidate in candidates.values():
            self.assertEqual(validate_candidate(candidate), [])
            self.assertEqual(candidate["pair_id"], "AMB_WV_s1_anon_001")
            self.assertEqual(candidate["provenance"]["source_person_name"], None)
            self.assertEqual(candidate["provenance"]["source_corpus"], None)
        candidate = candidates["associative"]
        self.assertEqual(
            set(render_arms(candidate)),
            set(CORE_ARMS),
        )


if __name__ == "__main__":
    unittest.main()

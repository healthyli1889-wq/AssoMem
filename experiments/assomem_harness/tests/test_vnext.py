import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from arms import materialize_vnext_arms  # noqa: E402
from dataset import discover_vnext_items  # noqa: E402
from profile import load_profile  # noqa: E402
from run import prepare_run  # noqa: E402
from workflow import score_solver_answer, validate_solver_answer  # noqa: E402
from zero_evidence import run_zero_evidence_check  # noqa: E402


class VnextHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile(ROOT / "experiments/assomem_harness/profiles/work-vnext-1.json")
        cls.data_root = ROOT / "staging/work-vnext/v1/s1/candidates"
        cls.item = discover_vnext_items(cls.data_root, cls.profile, "work")[0]

    def test_discovers_and_materializes_the_three_source_pair(self):
        self.assertEqual(set(self.item.arms), {"associative", "distractor", "absence"})
        arms = materialize_vnext_arms(self.item, self.profile)
        self.assertEqual(
            set(arms), {"full", "a_only", "b_only", "link_broken", "distractor", "absence"}
        )
        self.assertEqual(arms["full"].ground_truth["binary_decision"], True)
        self.assertEqual(arms["a_only"].ground_truth["binary_decision"], False)
        self.assertIn(9, [session["session_id"] for session in arms["distractor"].visible["context"]])
        self.assertNotIn(5, [session["session_id"] for session in arms["absence"].visible["context"]])

    def test_binary_contract_requires_decision_and_scores_it_deterministically(self):
        self.assertIsNone(validate_solver_answer(
            {"decision": "yes", "answer": "Supported by sessions 5 and 7.", "evidence_session_ids": [5, 7]},
            self.profile,
        ))
        self.assertIn("decision", validate_solver_answer({"answer": "x"}, self.profile) or "")
        score = score_solver_answer(
            {"required_elements": [{"hit": True}], "binary_decision_correct": True},
            {"decision": "yes", "answer": "x", "evidence_session_ids": [5, 7]},
            {"binary_decision": True},
            self.profile,
        )
        self.assertEqual(score["binary_correct"], 1)

    def test_zero_evidence_rejects_a_target_positive_guess(self):
        result = run_zero_evidence_check(
            self.item.arms["associative"],
            self.profile,
            object(),
            lambda _solver, _prompt: ({"decision": "yes", "answer": "guess", "evidence_session_ids": []}, {}),
            trials=2,
        )
        self.assertFalse(result["pass"])
        self.assertEqual(result["target_false_positive_rate"], 1.0)

    def test_vnext_dry_run_writes_six_condition_inventory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            result = prepare_run(
                self.data_root,
                ROOT / "experiments/assomem_harness/profiles/work-vnext-1.json",
                "work",
                "vnext-test",
                output,
                max_items=1,
            )
            self.assertEqual(result["shipped_conversations"], 6)
            e1 = (output / "work/vnext-test/review/e1_intervention.csv").read_text()
            self.assertIn("a_only", e1)
            self.assertIn("link_broken", e1)


if __name__ == "__main__":
    unittest.main()

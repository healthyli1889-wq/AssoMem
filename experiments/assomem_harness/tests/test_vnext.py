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
        cls.data_root = ROOT / "staging/work-vnext/work/harness-root-s1-s10"
        cls.item = discover_vnext_items(cls.data_root, cls.profile, "work")[0]

    def test_discovers_and_materializes_the_three_source_pair(self):
        self.assertEqual(set(self.item.arms), {"associative", "distractor", "absence"})
        arms = materialize_vnext_arms(self.item, self.profile)
        self.assertEqual(
            set(arms), {"full", "a_only", "b_only", "link_broken", "distractor", "absence"}
        )
        self.assertEqual(arms["full"].ground_truth["binary_decision"], True)
        self.assertEqual(arms["a_only"].ground_truth["binary_decision"], False)
        self.assertEqual(arms["absence"].ground_truth["expected_mode"], "withhold_C")
        self.assertEqual(len(arms["distractor"].visible["context"]), 20)
        self.assertEqual(len(arms["absence"].visible["context"]), 20)
        # a_only must visibly replace the ev_B session rather than delete it.
        full_ids = [session["session_id"] for session in arms["full"].visible["context"]]
        a_only_ids = [session["session_id"] for session in arms["a_only"].visible["context"]]
        self.assertEqual(full_ids, a_only_ids)
        self.assertNotEqual(arms["full"].visible["context"], arms["a_only"].visible["context"])

    def test_binary_contract_requires_mode_and_scores_it_deterministically(self):
        self.assertIsNone(validate_solver_answer(
            {"mode": "answer", "answer": "Supported by sessions 5 and 7.", "evidence_session_ids": [5, 7]},
            self.profile,
        ))
        self.assertIn("mode", validate_solver_answer({"answer": "x"}, self.profile) or "")
        score = score_solver_answer(
            {
                "target_asserted": True,
                "target_evidence_grounded": True,
                "evidence_usage": {
                    "ev_A_used": True,
                    "ev_B_used": True,
                    "h_k": 2,
                    "source_misattribution": False,
                },
                "abstention": {"abstains": False, "asserts_absent_pattern": False},
                "condition_correct": True,
                "failure_tags": [],
                "reason": "Both visible target facts support the answer.",
            },
            {"mode": "answer", "answer": "x", "evidence_session_ids": [5, 7]},
            {
                "binary_decision": True,
                "expected_mode": "infer_C",
                "allowed_evidence_ids": ["ev_A", "ev_B"],
            },
            self.profile,
        )
        self.assertEqual(score["binary_correct"], 1)

    def test_zero_evidence_rejects_a_target_positive_guess(self):
        solver = object()
        validator = object()

        def fake_call(model, _prompt):
            if model is solver:
                return (
                    {"mode": "answer", "answer": "guess", "evidence_session_ids": []},
                    {},
                )
            self.assertIs(model, validator)
            return ({
                "target_asserted": True,
                "target_evidence_grounded": False,
                "evidence_usage": {
                    "ev_A_used": False,
                    "ev_B_used": False,
                    "h_k": 0,
                    "source_misattribution": False,
                },
                "abstention": {"abstains": False, "asserts_absent_pattern": False},
                "condition_correct": False,
                "failure_tags": ["unsupported_target"],
                "reason": "The target was guessed without visible memories.",
            }, {})

        result = run_zero_evidence_check(
            self.item.arms["associative"],
            self.profile,
            solver,
            validator,
            fake_call,
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

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from workflow import score_solver_answer, validate_solver_answer  # noqa: E402


class WorkflowTests(unittest.TestCase):
    def test_solver_score_computes_rea_jer_and_abstention_fields(self):
        score = score_solver_answer({
            "element_hits": [True, True],
            "cited_evidence_count": 2,
            "abstains": False,
            "asserts_absent_pattern": False,
        })
        self.assertEqual(score["rea"], 1)
        self.assertEqual(score["jer"], 1)
        self.assertEqual(score["h_k"], 2)
        self.assertFalse(score["source_misattribution"])

    def test_solver_answer_requires_a_nonempty_answer_string(self):
        self.assertEqual(validate_solver_answer({"answer": "substantive"}), None)
        self.assertIn("answer", validate_solver_answer({"dialogue": []}) or "")
        self.assertIn("empty", validate_solver_answer({"answer": "  "}) or "")


if __name__ == "__main__":
    unittest.main()

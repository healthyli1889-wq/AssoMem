import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from workflow import accept_candidate, score_solver_answer  # noqa: E402


class WorkflowTests(unittest.TestCase):
    def test_candidate_requires_answer_table_and_supported_elements(self):
        verdict = {
            "accept": True,
            "answer_table": {"prior": False, "ev_a_only": False, "ev_b_only": False, "full": True},
            "gold_supported": True,
            "required_elements_supported": [True, True],
        }
        self.assertTrue(accept_candidate(verdict))
        verdict["answer_table"]["prior"] = True
        self.assertFalse(accept_candidate(verdict))

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


if __name__ == "__main__":
    unittest.main()

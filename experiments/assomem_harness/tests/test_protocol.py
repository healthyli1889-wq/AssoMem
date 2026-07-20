import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from protocol import author_prompt, score_prompt, validate_query_prompt  # noqa: E402


class ProtocolTests(unittest.TestCase):
    def test_author_prompt_hides_ground_truth_and_keeps_focus(self):
        visible = {"context": [], "query": "original focus", "data_filename": "x.json"}
        prompt = author_prompt(visible)
        self.assertIn("original focus", prompt)
        self.assertNotIn("gold_answer", prompt)
        self.assertIn("required_elements", prompt)

    def test_validator_scoring_prompt_contains_gt_but_solver_prompt_would_not(self):
        prompt = score_prompt(
            {"answer": "answer"},
            {"gold_answer": "gold", "required_elements": ["one", "two"], "expected_mode": "answer"},
        )
        self.assertIn("gold", prompt)
        self.assertIn("required_elements", prompt)
        validation = validate_query_prompt({"context": [], "query": "q"}, {"query": "q", "gold_answer": "g"})
        self.assertIn("candidate", validation)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from protocol import score_prompt, solver_prompt  # noqa: E402


class ProtocolTests(unittest.TestCase):
    def test_solver_prompt_uses_frozen_query_without_ground_truth(self):
        visible = {"context": [], "query": "original focus", "data_filename": "x.json"}
        prompt = solver_prompt(visible)
        self.assertIn("original focus", prompt)
        self.assertNotIn("gold_answer", prompt)
        self.assertNotIn("required_elements", prompt)
        self.assertIn("key, `answer`", prompt)
        self.assertIn("must not be a placeholder", prompt)
        self.assertIn("must not be a dialogue", prompt)

    def test_validator_scoring_prompt_contains_gt_but_solver_prompt_would_not(self):
        prompt = score_prompt(
            {"answer": "answer"},
            {
                "gold_answer": "gold",
                "required_elements": ["one", "two"],
                "expected_mode": "not_gold",
                "evidence_contract": {"ev_A": {"fact": "A", "source": "user"}},
            },
        )
        self.assertIn("gold", prompt)
        self.assertIn("required_elements", prompt)
        self.assertIn("source_misattribution", prompt)
        self.assertIn("conclusion_correct", prompt)
        self.assertIn("evidence_contract", prompt)
        self.assertIn("same user", prompt)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "query_validity"))

from runner import condition_passes, make_generation_prompt, make_validation_prompt  # noqa: E402


class RunnerTests(unittest.TestCase):
    def test_condition_passes_uses_conservative_expected_classes(self):
        self.assertTrue(condition_passes("both", {"verdict": "gold"}))
        self.assertTrue(condition_passes("distractor", {"verdict": "gold"}))
        self.assertTrue(condition_passes("absence", {"verdict": "abstain"}))
        self.assertTrue(condition_passes("a_only", {"verdict": "abstain"}))
        self.assertFalse(condition_passes("a_only", {"verdict": "gold"}))
        self.assertFalse(condition_passes("both", {"verdict": "abstain"}))

    def test_prompts_do_not_include_private_annotation_keys(self):
        generator_prompt = make_generation_prompt({
            "user_id": "wl_u01",
            "focus_reference": "Would this schedule fit?",
            "context": [{"session_id": 1, "dialogue": [{"role": "user", "content": "hello"}]}],
        })
        self.assertNotIn('"gold_answer":', generator_prompt)
        self.assertNotIn('"annotation":', generator_prompt)
        validation_prompt = make_validation_prompt(
            "both",
            {"context": [], "query": "new?", "gold_answer": "yes", "required_elements": ["x"]},
        )
        self.assertIn("both", validation_prompt)
        self.assertIn("required_elements", validation_prompt)


if __name__ == "__main__":
    unittest.main()

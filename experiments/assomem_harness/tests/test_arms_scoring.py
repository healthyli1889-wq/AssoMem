import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from arms import materialize_arms  # noqa: E402
from dataset import discover_items  # noqa: E402
from profile import load_profile  # noqa: E402
from scoring import paired_delta_ci, rea_item, wilson_interval  # noqa: E402


class ArmsAndScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        profile = load_profile(ROOT / "experiments/assomem_harness/profiles/assomem-v1.json")
        cls.item = discover_items(ROOT / "src/data", profile, "work")[0]
        cls.profile = profile

    def test_materialized_arms_preserve_gold_and_remove_private_fields_from_visible_payload(self):
        arms = materialize_arms(self.item, self.profile, self.item.arms["associative"]["query"])
        self.assertEqual(set(arms), {
            "full", "no_target", "broken_link", "distractor", "absence", "add_evidence"
        })
        self.assertNotEqual(len(arms["full"].visible["context"]), len(arms["no_target"].visible["context"]))
        broken_text = " ".join(
            turn["content"] for session in arms["broken_link"].visible["context"]
            for turn in session["dialogue"]
        )
        self.assertIn("A friend told me:", broken_text)
        self.assertNotIn("annotation", str(arms["broken_link"].visible))
        self.assertEqual(arms["absence"].ground_truth["expected_mode"], "abstain")

    def test_rea_is_and_aggregation_and_delta_ci_is_paired(self):
        self.assertEqual(rea_item([True, True]), 1)
        self.assertEqual(rea_item([True, False]), 0)
        low, high = wilson_interval(7, 10)
        self.assertLess(low, 0.7)
        self.assertGreater(high, 0.7)
        estimate, low, high = paired_delta_ci([1, 1, 1, 1], [0, 0, 0, 1], seed=1, draws=1000)
        self.assertEqual(estimate, 0.75)
        self.assertGreater(low, 0)
        self.assertGreater(high, low)


if __name__ == "__main__":
    unittest.main()

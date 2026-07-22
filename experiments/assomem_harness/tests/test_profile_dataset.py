import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from dataset import discover_items, solver_input  # noqa: E402
from profile import load_profile  # noqa: E402


class ProfileDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile(
            ROOT / "experiments/assomem_harness/profiles/assomem-v1.json"
        )

    def test_work_profile_discovers_all_600_shipped_conversations(self):
        items = discover_items(ROOT / "src/data", self.profile, "work")
        self.assertEqual(len(items), 200)
        self.assertEqual({item.user_id for item in items}, {f"u{i:02d}" for i in range(1, 11)})
        self.assertEqual({item.scenario_id for item in items}, {f"S{i}" for i in range(1, 21)})
        self.assertTrue(all(set(item.arms) == {"associative", "distractor", "absence"} for item in items))

    def test_solver_input_does_not_leak_ground_truth_or_annotations(self):
        item = discover_items(ROOT / "src/data", self.profile, "work")[0]
        payload = solver_input(item.arms["associative"], item.arms["associative"]["query"])
        rendered = str(payload)
        self.assertIn("context", payload)
        self.assertNotIn("data_filename", payload)
        self.assertNotIn("gold_answer", rendered)
        self.assertNotIn("required_elements", rendered)
        self.assertNotIn("annotation", rendered)
        self.assertNotIn("evolving_state", rendered)


if __name__ == "__main__":
    unittest.main()

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "query_validity"))

from core import (  # noqa: E402
    build_conditions,
    load_balanced_selection,
    redact_for_generator,
    redact_for_validator,
)


class CoreExperimentTests(unittest.TestCase):
    def test_selection_is_five_domains_twenty_scenarios_and_balanced_users(self):
        selection = load_balanced_selection(ROOT, seed=17)
        self.assertEqual(len(selection), 100)
        self.assertEqual({item["domain"] for item in selection}, {
            "work", "hobby", "health", "social", "finance"
        })
        for domain in ("work", "hobby", "health", "social", "finance"):
            rows = [item for item in selection if item["domain"] == domain]
            self.assertEqual({item["scenario_id"] for item in rows}, {f"S{i}" for i in range(1, 21)})
            counts = {item["user_id"]: 0 for item in rows}
            for item in rows:
                counts[item["user_id"]] += 1
            self.assertEqual(set(counts.values()), {2})

    def test_redaction_hides_gold_annotation_and_evolving_state(self):
        item = json.loads(
            (ROOT / "src/data/work/associative/AMB_WL_u01_associative_S1.json").read_text()
        )
        generated = redact_for_generator(item)
        self.assertEqual(generated["focus_reference"], item["query"])
        self.assertNotIn("gold_answer", json.dumps(generated))
        self.assertNotIn("required_elements", json.dumps(generated))
        self.assertNotIn("annotation", generated["context"][0])
        self.assertNotIn("evolving_state", json.dumps(generated))

        validated = redact_for_validator(item, item["query"], "A-only")
        self.assertNotIn("gold_answer", json.dumps(validated))
        self.assertNotIn("annotation", json.dumps(validated))
        self.assertNotIn("evolving_state", json.dumps(validated))

    def test_conditions_have_expected_six_arms_and_final_query(self):
        associative = json.loads(
            (ROOT / "src/data/work/associative/AMB_WL_u01_associative_S1.json").read_text()
        )
        distractor = json.loads(
            (ROOT / "src/data/work/distractor/AMB_WL_u01_distractor_S1.json").read_text()
        )
        absence = json.loads(
            (ROOT / "src/data/work/absence/AMB_WL_u01_absence_S1.json").read_text()
        )
        conditions = build_conditions(associative, distractor, absence, "new query")
        self.assertEqual(set(conditions), {"empty", "a_only", "b_only", "both", "distractor", "absence"})
        for condition in conditions.values():
            self.assertEqual(condition["context"][-1]["dialogue"][-1]["content"], "new query")
            self.assertNotIn("annotation", condition)


if __name__ == "__main__":
    unittest.main()

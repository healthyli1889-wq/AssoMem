import json
import tempfile
import sys
import unittest
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from run import acquire_run_lock, completed_checkpoint_ids, parse_arms, prepare_run, validate_e1_gate  # noqa: E402


class RunTests(unittest.TestCase):
    def test_dry_run_writes_inventory_without_touching_gold(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            result = prepare_run(
                ROOT / "src/data",
                ROOT / "experiments/assomem_harness/profiles/assomem-v1.json",
                "work",
                "test-run",
                output,
            )
            self.assertEqual(result["base_items"], 200)
            self.assertEqual(result["shipped_conversations"], 600)
            self.assertTrue((output / "work/test-run/log/inventory.jsonl").is_file())
            self.assertTrue((output / "work/test-run/results.tsv").is_file())
            self.assertTrue((output / "work/test-run/review/e1_intervention.csv").is_file())
            self.assertTrue((output / "work/test-run/review/e2_judgment.csv").is_file())
            self.assertTrue((output / "work/test-run/review/e1_packets.jsonl").is_file())
            self.assertTrue((output / "registry.jsonl").is_file())
            with (output / "work/test-run/review/e1_intervention.csv").open() as handle:
                e1_arms = {row["arm"] for row in csv.DictReader(handle)}
            self.assertIn("full", e1_arms)

    def test_dry_run_can_limit_items_for_inspection(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            result = prepare_run(
                ROOT / "src/data",
                ROOT / "experiments/assomem_harness/profiles/assomem-v1.json",
                "work",
                "partial-run",
                output,
                max_items=3,
            )
            self.assertEqual(result["base_items"], 3)
            self.assertEqual(result["shipped_conversations"], 9)
            inventory = (output / "work/partial-run/log/inventory.jsonl").read_text().splitlines()
            self.assertEqual(len(inventory), 3)

    def test_parse_arms_accepts_single_and_multiple_arms(self):
        self.assertEqual(parse_arms("full"), ("full",))
        self.assertEqual(parse_arms("full,no_target"), ("full", "no_target"))
        with self.assertRaises(ValueError):
            parse_arms("unknown")

    def test_run_lock_rejects_a_second_process_for_same_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary)
            with acquire_run_lock(run_root):
                with self.assertRaises(RuntimeError):
                    with acquire_run_lock(run_root):
                        pass

    def test_only_scored_records_are_completed(self):
        with tempfile.TemporaryDirectory() as temporary:
            records = Path(temporary)
            (records / "scored.json").write_text(json.dumps({
                "checkpoint_id": "done", "status": "scored",
            }))
            (records / "error.json").write_text(json.dumps({
                "checkpoint_id": "retry", "status": "solver_error",
            }))
            self.assertEqual(completed_checkpoint_ids(records), {"done"})

    def test_e1_gate_requires_explicit_pass_for_selected_arms(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "e1.csv"
            path.write_text(
                "item_id,arm,human_pass\n"
                "item-1,full,pass\n"
                "item-1,no_target,pass\n"
                "item-1,broken_link,pass\n"
            )
            validate_e1_gate(path, {"item-1"}, ("full", "no_target", "broken_link"))
            path.write_text(path.read_text().replace("item-1,broken_link,pass", "item-1,broken_link,"))
            with self.assertRaises(ValueError):
                validate_e1_gate(path, {"item-1"}, ("full", "no_target", "broken_link"))


if __name__ == "__main__":
    unittest.main()

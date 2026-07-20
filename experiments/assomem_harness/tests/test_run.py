import tempfile
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from run import prepare_run  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()

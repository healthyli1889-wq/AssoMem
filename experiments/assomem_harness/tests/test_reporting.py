import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from reporting import build_table_a, build_table_b  # noqa: E402


class ReportingTests(unittest.TestCase):
    def test_tables_include_three_solvers_and_deferred_saa(self):
        rows = [
            {
                "solver": "gpt", "full": [1, 1], "no_target": [0, 1],
                "broken_link": [0, 0], "jer": [1, 1], "dir": [1, 0],
                "abc": [1, 1], "fool_rate": [0, 1],
            }
        ]
        table_a = build_table_a(rows, seed=3, draws=100)
        table_b = build_table_b(rows)
        self.assertIn("Δ_assoc", table_a)
        self.assertIn("gpt", table_a)
        self.assertIn("SAA", table_b)
        self.assertIn("deferred", table_b)


if __name__ == "__main__":
    unittest.main()

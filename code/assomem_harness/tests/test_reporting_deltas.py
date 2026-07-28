"""The ladder Δ must measure discrimination, not accuracy against opposite golds."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reporting import build_vnext_table_a, target_assertion  # noqa: E402

ABLATIONS = ("a_only", "b_only", "link_broken")


def _deltas(table: str) -> list[float]:
    """Pull the three Δ point estimates out of the rendered row."""
    row = table.strip().splitlines()[-1]
    cells = [cell.strip() for cell in row.split("|")[1:-1]]
    return [float(re.match(r"(-?\d+\.\d+)", cell).group(1)) for cell in cells[-3:]]


class VnextDeltaTests(unittest.TestCase):
    def test_constant_asserter_scores_zero_delta(self):
        """A solver that always asserts the target discriminates nothing.

        Scored against each arm's own gold it looks perfect on `full` and hopeless
        on the ablations, which is exactly the shape that made the published
        work-expand40 table report Δ_link-broken = 0.70 for a solver asserting the
        target in 70% of link-broken items.
        """
        n = 40
        row = {
            "solver": "always-asserts",
            "full": [1] * n,          # correct, because full's gold is to assert
            "a_only": [0] * n,        # wrong, because a_only's gold is to withhold
            "b_only": [0] * n,
            "link_broken": [0] * n,
        }
        for delta in _deltas(build_vnext_table_a([row], seed=1, draws=200)):
            self.assertEqual(delta, 0.0)

    def test_constant_withholder_scores_zero_delta(self):
        row = {
            "solver": "always-withholds",
            "full": [0] * 40,
            "a_only": [1] * 40,
            "b_only": [1] * 40,
            "link_broken": [1] * 40,
        }
        for delta in _deltas(build_vnext_table_a([row], seed=1, draws=200)):
            self.assertEqual(delta, 0.0)

    def test_perfect_solver_scores_delta_one(self):
        row = {
            "solver": "perfect",
            "full": [1] * 40,
            "a_only": [1] * 40,
            "b_only": [1] * 40,
            "link_broken": [1] * 40,
        }
        for delta in _deltas(build_vnext_table_a([row], seed=1, draws=200)):
            self.assertEqual(delta, 1.0)

    def test_delta_recovers_the_assertion_gap(self):
        """Half the ablation items asserted => Δ is 0.50, not 0.50's complement."""
        n = 40
        row = {
            "solver": "partial",
            "full": [1] * n,
            # correct on half, i.e. asserted the target on the other half
            "a_only": [1] * (n // 2) + [0] * (n // 2),
            "b_only": [1] * (n // 2) + [0] * (n // 2),
            "link_broken": [1] * (n // 2) + [0] * (n // 2),
        }
        for delta in _deltas(build_vnext_table_a([row], seed=1, draws=200)):
            self.assertAlmostEqual(delta, 0.50, places=2)

    def test_target_assertion_flips_only_withhold_arms(self):
        self.assertEqual(target_assertion("full", [1, 0]), [1, 0])
        self.assertEqual(target_assertion("distractor", [1, 0]), [1, 0])
        for arm in ABLATIONS + ("absence",):
            self.assertEqual(target_assertion(arm, [1, 0]), [0, 1])


if __name__ == "__main__":
    unittest.main()

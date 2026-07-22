import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from dataset import discover_items  # noqa: E402
from manifest import build_stratified_manifest, select_manifest_items  # noqa: E402
from profile import load_profile  # noqa: E402


class ManifestTests(unittest.TestCase):
    def test_twenty_item_manifest_covers_all_scenarios_and_balances_users(self):
        profile = load_profile(ROOT / "experiments/assomem_harness/profiles/assomem-v1.json")
        items = discover_items(ROOT / "src/data", profile, "work")
        manifest = build_stratified_manifest(items, profile, ROOT / "src/data", count=20, seed=7)
        selected = manifest["items"]
        self.assertEqual(len(selected), 20)
        self.assertEqual({row["scenario_id"] for row in selected}, {f"S{i}" for i in range(1, 21)})
        user_counts = {}
        for row in selected:
            user_counts[row["user_id"]] = user_counts.get(row["user_id"], 0) + 1
        self.assertEqual(set(user_counts.values()), {2})
        self.assertTrue(all("difficulty" in row for row in selected))
        resolved = select_manifest_items(items, manifest, ROOT / "src/data")
        self.assertEqual([item.item_id for item in resolved], [row["item_id"] for row in selected])

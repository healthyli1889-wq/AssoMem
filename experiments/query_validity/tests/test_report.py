import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "query_validity"))

from report import build_findings  # noqa: E402


class ReportTests(unittest.TestCase):
    def test_report_stays_preliminary_until_human_labels_are_complete(self):
        rows = [
            {"selection_id": "work_u01_S1", "human_valid": "", "domain": "work"}
        ]
        text = build_findings(rows, {"n_completed": 0, "n_pending": 1})
        self.assertIn("等待人工终审", text)
        self.assertNotIn("人工有效：", text)

    def test_report_summarizes_complete_human_labels(self):
        rows = [
            {"selection_id": "work_u01_S1", "human_valid": "true", "domain": "work", "automatic_pass": "true"},
            {"selection_id": "hobby_u01_S1", "human_valid": "false", "domain": "hobby", "automatic_pass": "true"},
        ]
        text = build_findings(rows, {"n_completed": 2, "n_pending": 0})
        self.assertIn("人工有效：1/2", text)
        self.assertIn("自动判定与人工标签不一致：1 条", text)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
HARNESS = ROOT.parents[1] / "experiments" / "assomem_harness"
sys.path.insert(0, str(HARNESS))

from dataset import discover_vnext_items
from generate_social_pilot import build_social_pilot
from profile import load_profile
from schema import render_arms, validate_candidate


class SocialPilotGeneratorTests(unittest.TestCase):
    def test_generates_34_complete_source_triads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            result = build_social_pilot(destination, count=34)
            self.assertEqual(result["base_candidates"], 34)
            files = list(destination.glob("*/*.json"))
            self.assertEqual(len(files), 102)
            associative = sorted(destination.glob("associative/*.json"))
            pairs = [
                json.loads(path.read_text(encoding="utf-8"))
                for path in associative
            ]
            scenario_persona_pairs = {
                (candidate["pair_id"].rsplit("_", 1)[0], candidate["user_id"])
                for candidate in pairs
            }
            self.assertEqual(len(scenario_persona_pairs), 34)
            for path in files:
                candidate = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(candidate["domain"], "social")
                self.assertEqual(validate_candidate(candidate), [])
            profile = load_profile(HARNESS / "profiles/social-vnext-1.json")
            self.assertEqual(len(discover_vnext_items(destination, profile, "social")), 34)

    def test_rebuild_removes_stale_source_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            build_social_pilot(destination, count=34)
            stale = destination / "associative" / "stale.json"
            stale.write_text("{}")
            build_social_pilot(destination, count=34)
            self.assertFalse(stale.exists())

    def test_background_persona_is_not_repeated_in_every_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            build_social_pilot(destination, count=34)
            candidate = json.loads(next((destination / "associative").glob("*.json")).read_text())
            texts = [
                turn["content"]
                for session in candidate["context"]
                for turn in session["dialogue"]
                if turn["role"] == "user"
            ]
            self.assertEqual(sum("As someone who" in text for text in texts), 0)
            self.assertFalse(any(" i " in text for text in texts))

    def test_queries_are_natural_and_do_not_disclose_next_day_connector(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            build_social_pilot(destination, count=34)
            for path in destination.glob("associative/*.json"):
                candidate = json.loads(path.read_text())
                query = candidate["query"].lower()
                self.assertNotIn("based only on these records", query)
                self.assertNotIn("sunday", query)

    def test_staged_social_pilot_has_102_valid_records(self) -> None:
        root = ROOT.parents[1] / "staging/social-vnext/v1/s1/candidates"
        files = list(root.glob("*/*.json"))
        self.assertEqual(len(files), 102)
        for path in files:
            self.assertEqual(validate_candidate(json.loads(path.read_text(encoding="utf-8"))), [])

    def test_social_vnext_requires_extended_construct_fields(self) -> None:
        candidate = json.loads(
            (ROOT.parents[1] / "staging/social-vnext/v1/s1/candidates/associative/AMB_SV_hosting_before_mediation_001_associative.json").read_text()
        )
        del candidate["answer_contract"]
        self.assertIn("v1.1 missing fields: answer_contract", validate_candidate(candidate))

    def test_source_swap_is_natural_other_person_dialogue(self) -> None:
        candidate = json.loads(
            (ROOT.parents[1] / "staging/social-vnext/v1/s1/candidates/associative/AMB_SV_hosting_before_mediation_001_associative.json").read_text()
        )
        source_swap = render_arms(candidate)["source_swap"]
        b_session = next(session for session in source_swap["context"] if session["session_id"] == 12)
        self.assertIn("My friend", b_session["dialogue"][0]["content"])
        self.assertNotIn("Friend (not the user)", b_session["dialogue"][0]["content"])


if __name__ == "__main__":
    unittest.main()

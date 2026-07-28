"""Integration test over the shipped data: discover, render, and check the controls.

Runs against `data/` in this release, so it is the fastest way to confirm the tree
is intact before spending anything on model calls:

    cd code && PYTHONPATH=. python3 -m pytest assomem_harness/tests -q
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[2]
DATA = CODE.parent / "data"
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(CODE / "assomem_harness"))
sys.path.insert(0, str(CODE / "model_client"))

from arms import materialize_vnext_arms  # noqa: E402
from assomem_vnext.schema import validate_candidate  # noqa: E402
from dataset import discover_vnext_items  # noqa: E402
from profile import load_profile  # noqa: E402

DOMAINS = {
    "social": "social-vnext-1",
    "hobby": "hobby-vnext-1",
    "finance": "finance-vnext-3",
    "work": "work-vnext-1",
    "health": "health-vnext-1",
}
CORE_ARMS = ("full", "a_only", "b_only", "link_broken")
GOLD_ASSERTS = {"full": True, "distractor": True,
                "a_only": False, "b_only": False, "link_broken": False, "absence": False}


def _profile(name: str):
    return load_profile(CODE / "assomem_harness" / "profiles" / f"{name}.json")


class ReleaseDataTests(unittest.TestCase):
    def test_every_record_validates(self):
        for domain in DOMAINS:
            paths = sorted((DATA / domain).glob("*/*.json"))
            self.assertEqual(len(paths), 600, domain)
            for path in paths:
                errors = validate_candidate(json.loads(path.read_text(encoding="utf-8")))
                self.assertEqual(errors, [], f"{domain}/{path.name}")

    def test_every_pair_renders_six_arms(self):
        for domain, profile_name in DOMAINS.items():
            profile = _profile(profile_name)
            items = discover_vnext_items(DATA / domain, profile, domain)
            self.assertEqual(len(items), 200, domain)
            arms = materialize_vnext_arms(items[0], profile)
            self.assertEqual(set(arms), set(GOLD_ASSERTS), domain)

    def test_gold_directions_are_opposed_across_the_ladder(self):
        """full and distractor expect the target asserted; the four controls do not."""
        for domain, profile_name in DOMAINS.items():
            profile = _profile(profile_name)
            item = discover_vnext_items(DATA / domain, profile, domain)[0]
            for name, arm in materialize_vnext_arms(item, profile).items():
                self.assertEqual(
                    arm.ground_truth["binary_decision"], GOLD_ASSERTS[name], f"{domain}/{name}"
                )

    def test_solver_never_sees_gold(self):
        """The visible payload carries the question, never the answer.

        Checked on keys rather than on the serialised text: a word like "evidence"
        appears legitimately in dialogue prose ("a protected evidence-review
        block"), so a substring search over the blob reports leaks that are not.
        """
        allowed = {"context", "query", "target_proposition", "prompt_hash"}
        forbidden = {"arm_gold", "latent_C", "episode_annotations", "evidence",
                     "answer_contract", "connector_spans", "relational_connector",
                     "annotation", "coactivation_bridge", "single_evidence_replacements"}

        def keys(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    yield key
                    yield from keys(value)
            elif isinstance(node, list):
                for value in node:
                    yield from keys(value)

        for domain, profile_name in DOMAINS.items():
            profile = _profile(profile_name)
            item = discover_vnext_items(DATA / domain, profile, domain)[0]
            for name, arm in materialize_vnext_arms(item, profile).items():
                self.assertEqual(set(arm.visible), allowed, f"{domain}/{name}")
                present = set(keys(arm.visible))
                self.assertEqual(
                    present & forbidden, set(), f"{domain}/{name} leaks {present & forbidden}"
                )
                session_keys = {"session_id", "timestamp", "speaker_id", "speaker_label",
                                "dialogue", "role", "content"}
                self.assertTrue(
                    set(keys(arm.visible["context"])) <= session_keys,
                    f"{domain}/{name}: unexpected session keys "
                    f"{set(keys(arm.visible['context'])) - session_keys}",
                )

    def test_core_arms_hold_the_session_count(self):
        """A condition may not gain or lose sessions because of the intervention.

        health is the exception and is asserted as such: it ships no
        single_evidence_replacements, so a_only and b_only are rendered by deleting
        the target session and come out one short.
        """
        for domain, profile_name in DOMAINS.items():
            profile = _profile(profile_name)
            item = discover_vnext_items(DATA / domain, profile, domain)[0]
            arms = materialize_vnext_arms(item, profile)
            counts = {name: len(arms[name].visible["context"]) for name in CORE_ARMS}
            if domain == "health":
                self.assertEqual(counts["full"], 20)
                self.assertEqual(counts["a_only"], 19)
                self.assertEqual(counts["b_only"], 19)
            else:
                self.assertEqual(set(counts.values()), {20}, f"{domain}: {counts}")


if __name__ == "__main__":
    unittest.main()

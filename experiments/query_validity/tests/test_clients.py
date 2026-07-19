import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "query_validity"))

from clients import (  # noqa: E402
    ModelConfig,
    extract_json_object,
    request_payload,
)


class ClientTests(unittest.TestCase):
    def test_all_three_protocols_have_distinct_request_shapes(self):
        prompt = "Return JSON."
        configs = [
            ModelConfig("openai-responses", "m", "k", "https://example.test"),
            ModelConfig("openai-chat", "m", "k", "https://example.test"),
            ModelConfig("anthropic", "m", "k", "https://example.test"),
        ]
        payloads = [request_payload(config, prompt) for config in configs]
        self.assertIn("input", payloads[0])
        self.assertIn("messages", payloads[1])
        self.assertIn("system", payloads[2])
        self.assertIn("messages", payloads[2])

    def test_extract_json_object_accepts_fenced_and_plain_json(self):
        self.assertEqual(extract_json_object('```json\n{"ok": true}\n```'), {"ok": True})
        self.assertEqual(extract_json_object('prefix {"ok": 1} suffix'), {"ok": 1})

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            request_payload(ModelConfig("unknown", "m", "k", "https://example.test"), "x")


if __name__ == "__main__":
    unittest.main()

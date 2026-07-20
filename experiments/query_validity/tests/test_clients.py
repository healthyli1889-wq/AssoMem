import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "query_validity"))

from clients import (  # noqa: E402
    ModelConfig,
    normalize_usage,
    _text_from_response,
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

    def test_openai_chat_payload_limits_response_tokens(self):
        config = ModelConfig("openai-chat", "m", "k", "https://example.test")
        self.assertEqual(request_payload(config, "Return JSON.")["max_tokens"], 512)

    def test_openai_chat_falls_back_to_reasoning_when_content_is_empty(self):
        config = ModelConfig("openai-chat", "m", "k", "https://example.test")
        response = {"choices": [{"message": {"content": "", "reasoning_content": "{\"answer\":\"OK\"}"}}]}
        self.assertEqual(_text_from_response(config, response), '{"answer":"OK"}')

    def test_normalize_usage_preserves_billable_token_fields(self):
        usage = normalize_usage({
            "prompt_tokens": 12, "completion_tokens": 34, "total_tokens": 46,
            "completion_tokens_details": {"reasoning_tokens": 20},
        })
        self.assertEqual(usage["input_tokens"], 12)
        self.assertEqual(usage["output_tokens"], 34)
        self.assertEqual(usage["reasoning_tokens"], 20)

    def test_extract_json_object_accepts_fenced_and_plain_json(self):
        self.assertEqual(extract_json_object('```json\n{"ok": true}\n```'), {"ok": True})
        self.assertEqual(extract_json_object('prefix {"ok": 1} suffix'), {"ok": 1})
        self.assertEqual(
            extract_json_object('reasoning {"draft": 1} final {"answer": "OK"}'),
            {"draft": 1},
        )

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            request_payload(ModelConfig("unknown", "m", "k", "https://example.test"), "x")


if __name__ == "__main__":
    unittest.main()

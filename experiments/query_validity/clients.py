"""Minimal dependency-free clients for the supported model APIs."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

SUPPORTED_PROVIDERS = {"openai-responses", "openai-chat", "anthropic"}


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    api_key: str
    base_url: str
    temperature: float = 0.0
    timeout: float = 120.0
    max_retries: int = 3

    def __post_init__(self) -> None:
        if self.provider not in SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {self.provider}")
        if not self.model or not self.api_key:
            raise ValueError("model and api_key are required")


def config_from_env(prefix: str) -> ModelConfig:
    values = {
        "provider": os.environ.get(f"{prefix}_PROVIDER", "openai-chat"),
        "model": os.environ.get(f"{prefix}_MODEL", ""),
        "api_key": os.environ.get(f"{prefix}_API_KEY", ""),
        "base_url": os.environ.get(f"{prefix}_BASE_URL", ""),
        "temperature": float(os.environ.get(f"{prefix}_TEMPERATURE", "0")),
        "timeout": float(os.environ.get(f"{prefix}_TIMEOUT", "120")),
        "max_retries": int(os.environ.get(f"{prefix}_MAX_RETRIES", "3")),
    }
    if not values["base_url"]:
        values["base_url"] = (
            "https://api.anthropic.com/v1"
            if values["provider"] == "anthropic"
            else "https://api.openai.com/v1"
        )
    return ModelConfig(**values)


def request_payload(config: ModelConfig, prompt: str) -> dict[str, Any]:
    if config.provider == "openai-responses":
        return {
            "model": config.model,
            "input": prompt,
            "temperature": config.temperature,
        }
    if config.provider == "openai-chat":
        return {
            "model": config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.temperature,
        }
    if config.provider == "anthropic":
        return {
            "model": config.model,
            "max_tokens": 4096,
            "temperature": config.temperature,
            "system": "Return only valid JSON.",
            "messages": [{"role": "user", "content": prompt}],
        }
    raise ValueError(f"Unsupported provider: {config.provider}")


def _endpoint(config: ModelConfig) -> str:
    base = config.base_url.rstrip("/")
    if config.provider == "openai-responses":
        return base if base.endswith("/responses") else f"{base}/responses"
    if config.provider == "openai-chat":
        return base if base.endswith("/chat/completions") else f"{base}/chat/completions"
    return base if base.endswith("/messages") else f"{base}/messages"


def _headers(config: ModelConfig) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {config.api_key}",
    }
    if config.provider == "anthropic":
        headers.pop("Authorization")
        headers["x-api-key"] = config.api_key
        headers["anthropic-version"] = "2023-06-01"
    return headers


def _text_from_response(config: ModelConfig, response: dict[str, Any]) -> str:
    if config.provider == "openai-responses":
        if response.get("output_text"):
            return response["output_text"]
        parts = []
        for output in response.get("output", []):
            for content in output.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    parts.append(content.get("text", ""))
        return "\n".join(parts)
    if config.provider == "openai-chat":
        return response["choices"][0]["message"]["content"]
    content = response.get("content", [])
    return "\n".join(part.get("text", "") for part in content if part.get("type") == "text")


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.S | re.I)
    candidate = fenced.group(1) if fenced else cleaned
    if not fenced:
        start, end = candidate.find("{"), candidate.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Model response does not contain a JSON object")
        candidate = candidate[start:end + 1]
    value = json.loads(candidate)
    if not isinstance(value, dict):
        raise ValueError("Model response JSON must be an object")
    return value


def call_model(config: ModelConfig, prompt: str) -> dict[str, Any]:
    body = json.dumps(request_payload(config, prompt)).encode("utf-8")
    request = urllib.request.Request(_endpoint(config), data=body, headers=_headers(config))
    last_error: Exception | None = None
    for attempt in range(config.max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=config.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return extract_json_object(_text_from_response(config, payload))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError, ValueError) as exc:
            last_error = exc
            if attempt >= config.max_retries:
                break
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"Model call failed after retries: {last_error}") from last_error

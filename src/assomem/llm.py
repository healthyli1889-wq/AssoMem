"""
LLM + embedding adapter.

Two backends:
  * "mock"   -> deterministic, offline, no API key. Bag-of-words hashed embeddings +
               rule-based chat so the WHOLE harness runs end-to-end and tests pass.
  * "openai" -> real models (set OPENAI_API_KEY). Used for serious runs / the LLM judge.

The mock embedding is a hashed bag-of-words vector (cosine-meaningful), which is enough
for retrieval/association/selection to behave sensibly on the sample data.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from typing import Dict, List, Optional

_DIM = 256
_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> List[str]:
    return _WORD.findall(text.lower())


def mock_embed(text: str, dim: int = _DIM) -> List[float]:
    """Deterministic hashed bag-of-words embedding, L2-normalized."""
    vec = [0.0] * dim
    for tok in _tokens(text):
        h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
        vec[(h // dim) % dim] += 0.5        # a second bucket reduces collisions
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    return sum(x * y for x, y in zip(a, b))


class LLM:
    def __init__(self, backend: str = "mock", chat_model: str = "gpt-4o-mini",
                 embed_model: str = "text-embedding-3-small", temperature: float = 0.0):
        self.backend = backend
        self.chat_model = chat_model
        self.embed_model = embed_model
        self.temperature = temperature
        self._client = None
        if backend == "openai":
            try:
                from openai import OpenAI
                self._client = OpenAI()
            except Exception as e:                       # pragma: no cover
                raise RuntimeError(
                    "openai backend requested but openai SDK / key unavailable: %s" % e)

    # ---------- embeddings ----------
    def embed(self, text: str) -> List[float]:
        if self.backend == "mock":
            return mock_embed(text)
        resp = self._client.embeddings.create(model=self.embed_model, input=text)
        return resp.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if self.backend == "mock":
            return [mock_embed(t) for t in texts]
        resp = self._client.embeddings.create(model=self.embed_model, input=texts)
        return [d.embedding for d in resp.data]

    # ---------- chat ----------
    def chat(self, messages: List[Dict[str, str]], json_mode: bool = False) -> str:
        if self.backend == "mock":
            return self._mock_chat(messages, json_mode)
        kwargs = dict(model=self.chat_model, messages=messages, temperature=self.temperature)
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        return self._client.chat.completions.create(**kwargs).choices[0].message.content

    # ---------- deterministic mock brain ----------
    def _mock_chat(self, messages: List[Dict[str, str]], json_mode: bool) -> str:
        sys = " ".join(m["content"] for m in messages if m["role"] == "system")
        usr = " ".join(m["content"] for m in messages if m["role"] == "user")
        tag = (sys + " " + usr).lower()

        # 1) fact extraction (store.py) -> JSON list of atomic facts
        if "personal information organizer" in tag or "extract" in tag and "facts" in tag:
            facts = []
            for line in re.split(r"[\n\.;]+", usr):
                line = line.strip()
                if len(line.split()) >= 3 and not line.lower().startswith(("output", "input")):
                    facts.append(line[:160])
            return json.dumps({"facts": facts[:12]})

        # 2) reflection / preference inference (reason.py) -> JSON insight
        if "infer" in tag and ("preference" in tag or "insight" in tag):
            # pick the most frequent category word as a cheap "insight"
            kws = [t for t in _tokens(usr) if len(t) > 4]
            top = max(set(kws), key=kws.count) if kws else "personalization"
            return json.dumps({
                "insight": f"the user likely prefers options related to {top}",
                "evidence": [],
            })

        # 3) LLM judge (eval/judge.py) -> JSON {score, verdict}
        if "impartial judge" in tag or "evaluate" in tag and "ground truth" in tag:
            gold = _extract_after(usr, "ground truth")
            ans = _extract_after(usr, "agent answer") or _extract_after(usr, "response")
            score = _token_f1(gold, ans)
            return json.dumps({"score": round(5 * score, 2), "verdict": "yes" if score > 0.5 else "no",
                               "rationale": "mock token-overlap judgement"})

        # 4) default
        return json.dumps({}) if json_mode else "OK"


def _extract_after(text: str, marker: str) -> str:
    idx = text.lower().find(marker.lower())
    if idx < 0:
        return ""
    tail = text[idx + len(marker):]
    return re.split(r"[\n]+", tail.strip(" :\t"))[0][:300]


def _token_f1(gold: str, pred: str) -> float:
    g, p = set(_tokens(gold)), set(_tokens(pred))
    if not g or not p:
        return 0.0
    inter = len(g & p)
    if inter == 0:
        return 0.0
    prec, rec = inter / len(p), inter / len(g)
    return 2 * prec * rec / (prec + rec)

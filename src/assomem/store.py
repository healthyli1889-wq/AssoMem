"""
STORE stage -- turn raw conversation turns into atomic, embedded MemoryNotes.

Borrowed from: Mem0 `FACT_RETRIEVAL_PROMPT` + `_create_memory`
  github.com/mem0ai/mem0/blob/main/mem0/configs/prompts.py
  github.com/mem0ai/mem0/blob/main/mem0/memory/main.py
Why: atomic facts (not raw turns) are the unit that makes retrieval/association/reasoning
tractable. We keep Mem0's md5 dedup + history idea (here: an in-memory set).
"""
from __future__ import annotations

import hashlib
import json
from typing import List

from .llm import LLM
from .schema import MemoryNote

FACT_EXTRACTION_PROMPT = (
    "You are a Personal Information Organizer that extracts atomic facts and preferences "
    "about the user from conversation. Return STRICT JSON: {\"facts\": [\"...\"]}. "
    "Each fact must be self-contained. Drop chit-chat. Extract facts only about the user."
)

# Lightweight category tagger -> drives `category` on each note (used by validity labels).
_CATEGORY_KEYWORDS = {
    "food": ["eat", "food", "coffee", "cuisine", "restaurant", "vegan", "spicy", "cook"],
    "hobby": ["piano", "guitar", "hiking", "football", "game", "read", "paint", "music", "run"],
    "work": ["engineer", "coding", "developer", "work", "job", "research", "study", "career"],
    "travel": ["travel", "trip", "flight", "hotel", "city", "beach", "mountain"],
    "personality": ["introvert", "extrovert", "anxious", "calm", "organized", "spontaneous"],
    "health": ["gym", "diet", "sleep", "exercise", "allergy", "vegetarian"],
}


def _categorize(text: str) -> str:
    low = text.lower()
    best, score = "general", 0
    for cat, kws in _CATEGORY_KEYWORDS.items():
        s = sum(1 for k in kws if k in low)
        if s > score:
            best, score = cat, s
    return best


def extract_facts(turns: List[str], llm: LLM) -> List[str]:
    """LLM fact extraction with a safe rule-based fallback."""
    joined = "\n".join(turns)
    try:
        raw = llm.chat(
            [{"role": "system", "content": FACT_EXTRACTION_PROMPT},
             {"role": "user", "content": joined}],
            json_mode=True,
        )
        facts = json.loads(raw).get("facts", [])
        facts = [f.strip() for f in facts if isinstance(f, str) and len(f.strip()) > 2]
        if facts:
            return facts
    except Exception:
        pass
    # fallback: treat each non-trivial sentence as a fact
    out = []
    for t in turns:
        for s in t.replace(";", ".").split("."):
            s = s.strip()
            if len(s.split()) >= 3:
                out.append(s)
    return out


def make_notes(facts: List[str], llm: LLM) -> List[MemoryNote]:
    """Embed + dedup + categorize facts into MemoryNotes (Mem0 `_create_memory`)."""
    notes: List[MemoryNote] = []
    seen = set()
    if not facts:
        return notes
    embs = llm.embed_batch(facts)
    for fact, emb in zip(facts, embs):
        h = hashlib.md5(fact.lower().encode()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        cat = _categorize(fact)
        poignancy = 2.0 + len(fact.split()) * 0.1     # cheap importance proxy
        notes.append(MemoryNote(content=fact, embedding=emb, category=cat,
                                keywords=[w for w in fact.lower().split() if len(w) > 4][:6],
                                poignancy=min(poignancy, 10.0)))
    return notes

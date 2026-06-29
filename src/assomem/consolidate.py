"""
CONSOLIDATE stage -- Complementary Learning Systems: forgetting + reinforcement.

Borrowed from: MemoryBank Ebbinghaus forgetting curve
  github.com/zhongwanjun/MemoryBank-SiliconFriend (memory_bank/.../forget_memory.py)
NOTE (verified bug fixed here): the original code computes `exp(-t / 5*S)` which Python
parses as exp((-t/5)*S) -- making stronger memories decay FASTER. The paper specifies
R = exp(-t / S). We implement the CORRECT form: retention = exp(-t / (5*S)).

Recall reinforces a note (strength S += 1, last_recall reset). Disused notes decay and,
below a retention threshold, are pruned/deprioritized. This is the "slow" consolidation
half of CLS; reflection (reason.reflect_insight) is the "fast" insight half.
"""
from __future__ import annotations

import math
import time
from typing import List

from .schema import MemoryNote

_DAY = 86400.0


def retention(note: MemoryNote, now: float = None) -> float:
    """Ebbinghaus retention R = exp(-t / (5*S)).  t in days since last recall."""
    now = now or time.time()
    t_days = max(0.0, (now - note.last_recall) / _DAY)
    s = max(note.strength, 1e-3)
    return math.exp(-t_days / (5.0 * s))


def reinforce(note: MemoryNote, now: float = None) -> None:
    """A successful recall strengthens the memory and resets its decay clock."""
    note.strength += 1.0
    note.last_recall = now or time.time()


def consolidate(notes: List[MemoryNote], threshold: float = 0.05,
                now: float = None) -> List[MemoryNote]:
    """Drop notes whose retention has fallen below `threshold` (insights are kept longer)."""
    now = now or time.time()
    kept = []
    for n in notes:
        r = retention(n, now)
        if n.kind == "insight" or r >= threshold:
            kept.append(n)
    return kept

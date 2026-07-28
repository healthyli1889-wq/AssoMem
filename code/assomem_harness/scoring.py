"""Deterministic aggregation for validator-produced item scores."""

from __future__ import annotations

import math
import random
from typing import Iterable


def rea_item(element_hits: Iterable[bool]) -> int:
    hits = list(element_hits)
    return int(bool(hits) and all(hits))


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return (float("nan"), float("nan"))
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    ) / denominator
    return (max(0.0, center - radius), min(1.0, center + radius))


def paired_delta_ci(
    left: list[int], right: list[int], *, seed: int, draws: int = 10_000
) -> tuple[float, float, float]:
    if len(left) != len(right) or not left:
        raise ValueError("paired delta requires equal non-empty arrays")
    observed = sum(a - b for a, b in zip(left, right)) / len(left)
    rng = random.Random(seed)
    samples = []
    for _ in range(draws):
        sample = [rng.randrange(len(left)) for _ in left]
        samples.append(sum(left[index] - right[index] for index in sample) / len(sample))
    samples.sort()
    return observed, samples[int(draws * 0.025)], samples[int(draws * 0.975)]

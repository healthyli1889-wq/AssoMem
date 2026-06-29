"""
Metrics for the Associative Memory Benchmark.

Reasoning Score (RS) -- grounded in verified prior art:
  * conjunctive gate           HotpotQA joint_em (arXiv:1809.09600)
  * strict vs partial credit   IFEval prompt-level vs instruction-level (arXiv:2311.07911)
  * step-discounted weighting   FollowBench CSL (arXiv:2310.20410)
  * product-of-steps option     PRM800K (arXiv:2305.20050)
  * calibration penalty (ECE/Brier)  Guo et al. (arXiv:1706.04599)

For a long-horizon item where step k adds constraint c_k and the final answer must satisfy
all c_1..c_K, with x_k in [0,1] satisfaction and self-reported confidence p_hat that ALL
constraints hold (g = product x_k):

    w_k~  = gamma^(k-1) / sum_j gamma^(j-1)             (step-discounted weights)
    RS = (1-lambda) * sum_k w_k~ x_k  +  lambda * prod_k x_k  -  beta * (p_hat - g)^2

lambda=1 -> strict joint-EM ; lambda=0 -> pure partial credit.
"""
from __future__ import annotations

import math
import random
import re
from typing import Dict, List, Optional, Sequence, Tuple

_WORD = re.compile(r"[a-z0-9]+")


def _toks(s: str) -> List[str]:
    return _WORD.findall((s or "").lower())


# ---------------- base answer correctness ----------------
def exact_match(pred: str, gold: str) -> float:
    return 1.0 if _norm(pred) == _norm(gold) else 0.0


def _norm(s: str) -> str:
    return " ".join(_toks(s))


def token_f1(pred: str, gold: str) -> float:
    p, g = _toks(pred), _toks(gold)
    if not p or not g:
        return 0.0
    common = 0
    gset = list(g)
    for t in p:
        if t in gset:
            gset.remove(t)
            common += 1
    if common == 0:
        return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)


def mc_correct(chosen_idx: Optional[int], options: List[str], gold: str) -> float:
    if chosen_idx is None or chosen_idx >= len(options):
        return 0.0
    return 1.0 if _norm(options[chosen_idx]) == _norm(gold) else 0.0


# ---------------- Reasoning Score ----------------
def reasoning_score(x: Sequence[float], confidence: float = None,
                    gamma: float = 0.8, lam: float = 0.4, beta: float = 0.5) -> Dict[str, float]:
    """Compute RS and its components for one long-horizon item.

    x : per-constraint satisfaction in [0,1], ordered by step.
    confidence : agent's P(all constraints satisfied); if None the calibration term is 0.
    Returns dict with rs, rs_strict, rs_partial, gate, calib_penalty.
    """
    K = len(x)
    if K == 0:
        return {"rs": 0.0, "rs_strict": 0.0, "rs_partial": 0.0, "gate": 0.0, "calib_penalty": 0.0}
    raw = [gamma ** k for k in range(K)]
    z = sum(raw) or 1.0
    w = [r / z for r in raw]
    rs_partial = sum(wk * xk for wk, xk in zip(w, x))
    gate = 1.0
    for xk in x:
        gate *= xk
    calib = 0.0
    if confidence is not None:
        calib = beta * (confidence - gate) ** 2
    rs = (1 - lam) * rs_partial + lam * gate - calib
    return {"rs": rs, "rs_strict": gate, "rs_partial": rs_partial,
            "gate": gate, "calib_penalty": calib}


# ---------------- abstention (validity control) ----------------
def abstention_score(answered: bool, is_answerable: bool) -> float:
    """Reward correct abstention; penalize answering the unanswerable (hallucination)."""
    if not is_answerable:
        return 1.0 if not answered else 0.0
    return 1.0 if answered else 0.0


# ---------------- calibration ----------------
def expected_calibration_error(confidences: List[float], correct: List[float],
                               n_bins: int = 10) -> float:
    if not confidences:
        return 0.0
    bins = [[] for _ in range(n_bins)]
    for c, y in zip(confidences, correct):
        b = min(n_bins - 1, int(c * n_bins))
        bins[b].append((c, y))
    n = len(confidences)
    ece = 0.0
    for b in bins:
        if not b:
            continue
        conf = sum(c for c, _ in b) / len(b)
        acc = sum(y for _, y in b) / len(b)
        ece += (len(b) / n) * abs(acc - conf)
    return ece


def brier(confidences: List[float], correct: List[float]) -> float:
    if not confidences:
        return 0.0
    return sum((c - y) ** 2 for c, y in zip(confidences, correct)) / len(confidences)


# ---------------- significance ----------------
def bootstrap_ci(values: List[float], n_resamples: int = 2000, alpha: float = 0.05,
                 seed: int = 0) -> Tuple[float, float, float]:
    """Percentile bootstrap mean + (lo, hi) CI. (scipy.stats.bootstrap equivalent.)"""
    if not values:
        return 0.0, 0.0, 0.0
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(n_resamples):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int((alpha / 2) * n_resamples)]
    hi = means[int((1 - alpha / 2) * n_resamples) - 1]
    return sum(values) / n, lo, hi


def cohen_kappa(a: List[int], b: List[int]) -> float:
    """Cohen's kappa for two raters over binary/categorical labels."""
    if not a or len(a) != len(b):
        return 0.0
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = 0.0
    for l in labels:
        pa = sum(1 for x in a if x == l) / n
        pb = sum(1 for y in b if y == l) / n
        pe += pa * pb
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

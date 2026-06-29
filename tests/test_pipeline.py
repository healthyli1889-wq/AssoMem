"""Smoke + correctness tests. Run: pytest -q  (or python -m pytest)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "eval"))

from assomem import AssociativeMemoryAgent, AgentConfig, BenchItem, LLM
import metrics as M


def _agent():
    return AssociativeMemoryAgent(LLM(backend="mock"), AgentConfig())


def test_store_and_retrieve():
    a = _agent()
    a.ingest(["User: I love hiking and landscape photography at sunrise."])
    assert len(a.notes) >= 1
    item = BenchItem(item_id="t1", source="syn", scenario="associative",
                     stored_context=[], query="weekend idea?",
                     options=["sunrise mountain photo trek", "casino night"],
                     gold="sunrise mountain photo trek")
    ans = a.answer(item)
    assert ans.chosen_option_idx in (0, 1)


def test_association_adds_notes():
    a = _agent()
    a.ingest(["User: I play piano.", "User: I like jazz.", "User: I prefer quiet nights."])
    assert a.edges, "association should build links between similar notes"


def test_reasoning_score_strict_vs_partial():
    r = M.reasoning_score([1, 1, 0, 1], confidence=0.7)
    assert r["rs_strict"] == 0.0          # one constraint failed -> gate 0
    assert 0.0 < r["rs_partial"] < 1.0
    full = M.reasoning_score([1, 1, 1, 1], confidence=1.0)
    assert abs(full["rs_strict"] - 1.0) < 1e-9
    assert full["rs"] > r["rs"]


def test_abstention():
    assert M.abstention_score(answered=False, is_answerable=False) == 1.0
    assert M.abstention_score(answered=True, is_answerable=False) == 0.0


def test_bootstrap_and_calibration():
    mean, lo, hi = M.bootstrap_ci([1, 1, 0, 1, 0, 1])
    assert lo <= mean <= hi
    ece = M.expected_calibration_error([0.9, 0.2, 0.8], [1, 0, 1])
    assert 0.0 <= ece <= 1.0


def test_ablation_runs():
    a = AssociativeMemoryAgent(LLM(backend="mock"), AgentConfig.memory_only())
    a.ingest(["User: I am vegetarian.", "User: I like spicy food."])
    item = BenchItem(item_id="t2", source="syn", scenario="associative",
                     stored_context=[], query="dinner?",
                     options=["vegan curry", "cheeseburger"], gold="vegan curry")
    ans = a.answer(item)
    assert ans.answer in ("vegan curry", "cheeseburger")

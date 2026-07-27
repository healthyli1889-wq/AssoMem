"""Stage 0 batch freeze: the query-type and polarity allocation over the 10x10 grid.

`DATA CRITERIA_new.md` states its quota for a 50-unit batch. This batch is 200
units (S1-S20 x U01-U10), so every required count is multiplied by four:

    query type      preference_generalization 32   situational_fit 32
                    recommendation_ranking    32   predicted_reaction 32
                    behavior_explanation      36   conditional_recommendation 36
                    -> max 36/200 = 18%, under the 20% ceiling

    polarity        accept 68   reject 68   conditional 32   non_decision 32
                    -> max 68/200 = 34%, under the 40% ceiling
                    -> scaled CRITERIA bands: accept 60-80, reject 60-80,
                       conditional 20-60, non_decision 20-60

The finance batch this one is modelled on breaches both rules (reject at 50/100
and four query types at exactly 20/100), so the grid below is built to the
document rather than copied from that batch.

Two row multisets per axis, rotated by a per-scenario offset, hit the totals
exactly while keeping every column (user) mixed. `verify()` asserts it rather
than trusting the arithmetic.
"""

from __future__ import annotations

from collections import Counter

PG = "preference_generalization"
SF = "situational_fit"
RR = "recommendation_ranking"
PR = "predicted_reaction"
BE = "behavior_explanation"
CR = "conditional_recommendation"

ACCEPT = "accept"
REJECT = "reject"
COND = "conditional"
NON = "non_decision"

# 12 rows of QT_A + 8 rows of QT_B => 2*12+1*8=32 for pg/sf/rr/pr, 1*12+3*8=36 for be/cr
QT_A = (PG, SF, RR, PR, BE, CR, PG, SF, RR, PR)
QT_B = (BE, CR, PG, SF, BE, CR, RR, PR, BE, CR)
QT_B_SCENARIOS = frozenset({3, 6, 8, 10, 12, 14, 16, 18})

# 12 rows of POL_A + 8 rows of POL_B => 3*12+4*8=68 accept/reject, 2*12+1*8=32 cond/non
POL_A = (ACCEPT, REJECT, COND, ACCEPT, REJECT, NON, ACCEPT, REJECT, COND, NON)
POL_B = (REJECT, ACCEPT, REJECT, ACCEPT, NON, REJECT, ACCEPT, COND, REJECT, ACCEPT)
POL_B_SCENARIOS = frozenset({2, 5, 7, 9, 11, 13, 15, 17})

REQUIRED_QUERY_TYPES = {PG: 32, SF: 32, RR: 32, PR: 32, BE: 36, CR: 36}
REQUIRED_POLARITIES = {ACCEPT: 68, REJECT: 68, COND: 32, NON: 32}

# Bridge type per scenario; each of the five CRITERIA forms is used twice.
BRIDGE_TYPES = {
    1: "state_dependent_operation",
    2: "strategy_outcome_contingency",
    3: "threshold_context_interaction",
    4: "preference_constraint_fit",
    5: "prediction_calibration",
    6: "state_dependent_operation",
    7: "threshold_context_interaction",
    8: "strategy_outcome_contingency",
    9: "preference_constraint_fit",
    10: "prediction_calibration",
    11: "state_dependent_operation",
    12: "strategy_outcome_contingency",
    13: "threshold_context_interaction",
    14: "preference_constraint_fit",
    15: "prediction_calibration",
    16: "state_dependent_operation",
    17: "strategy_outcome_contingency",
    18: "threshold_context_interaction",
    19: "preference_constraint_fit",
    20: "prediction_calibration",
}


def _rotate(sequence: tuple[str, ...], offset: int) -> tuple[str, ...]:
    offset %= len(sequence)
    return sequence[offset:] + sequence[:offset]


def query_type(scenario: int, user: int) -> str:
    row = QT_B if scenario in QT_B_SCENARIOS else QT_A
    return _rotate(row, scenario * 3)[user - 1]


def polarity(scenario: int, user: int) -> str:
    row = POL_B if scenario in POL_B_SCENARIOS else POL_A
    return _rotate(row, scenario * 7)[user - 1]


def grid() -> list[dict]:
    return [
        {
            "scenario": s,
            "user": u,
            "pair_id": f"AMB_SC_S{s}_U{u:02d}",
            "query_type": query_type(s, u),
            "polarity": polarity(s, u),
            "bridge_type": BRIDGE_TYPES[s],
        }
        for s in range(1, 21)
        for u in range(1, 11)
    ]


def verify() -> dict[str, Counter]:
    """Fail loudly on any quota breach; Stage 0 blocks the batch otherwise."""
    rows = grid()
    assert len(rows) == 200, f"expected 200 units, got {len(rows)}"

    types = Counter(row["query_type"] for row in rows)
    polarities = Counter(row["polarity"] for row in rows)

    assert dict(types) == REQUIRED_QUERY_TYPES, f"query-type quota breach: {dict(types)}"
    assert dict(polarities) == REQUIRED_POLARITIES, f"polarity quota breach: {dict(polarities)}"
    assert max(types.values()) <= 40, "a query type exceeds 20% of the batch"
    assert max(polarities.values()) <= 80, "a polarity exceeds 40% of the batch"

    # Every scenario must show at least four query types and at least three
    # polarities, so no row degenerates into one repeated answer shape.
    for s in range(1, 21):
        row = [r for r in rows if r["scenario"] == s]
        assert len({r["query_type"] for r in row}) >= 4, f"S{s} query types too narrow"
        assert len({r["polarity"] for r in row}) >= 3, f"S{s} polarities too narrow"

    # Every user must see at least four query types and three polarities across
    # scenarios, so U-index alone never determines the item shape the way it does
    # in the finance batch.
    for u in range(1, 11):
        column = [r for r in rows if r["user"] == u]
        assert len({r["query_type"] for r in column}) >= 4, f"U{u:02d} query types too narrow"
        assert len({r["polarity"] for r in column}) >= 3, f"U{u:02d} polarities too narrow"

    pairs = Counter((row["query_type"], row["polarity"]) for row in rows)
    assert max(pairs.values()) <= 24, f"a query-type/polarity cell is over-concentrated: {pairs.most_common(3)}"

    return {"query_type": types, "polarity": polarities, "cells": pairs}


if __name__ == "__main__":
    summary = verify()
    print("query types:", dict(sorted(summary["query_type"].items())))
    print("polarities :", dict(sorted(summary["polarity"].items())))
    print("cells      :", len(summary["cells"]), "distinct, max", max(summary["cells"].values()))
    print("Stage 0 allocation verified.")

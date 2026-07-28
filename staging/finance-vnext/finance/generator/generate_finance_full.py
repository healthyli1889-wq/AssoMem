"""Generate the finance-vNext v3 S1-S20 x U01-U10 x 3-arm batch (600 JSON).

A rebuild rather than an edit of `finance-vnext-2.0`, which measured Δ_assoc
= +0.068 mixed and +0.000 under kimi-k3 alone. Content lives in `finance_spec.py`
/ `finance_spec_s11_s20.py` and `finance_roster.py`; structure is shared with the
social and hobby batches via `staging/vnext_common/engine.py`.

    python3 generate_finance_full.py [--out <candidates dir>]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "vnext_common"))

import allocation  # noqa: E402
from engine import DomainPack, generate  # noqa: E402
from finance_roster import ANONYMIZATION_NOTE, profile_for  # noqa: E402
from finance_spec import (  # noqa: E402
    C_TEMPLATES,
    FILLER,
    QUERY_TYPE_FRAMES,
    RELATIONS,
    REPLACEMENT_FILLER,
    SCENARIOS,
)
from finance_spec_s11_s20 import RELATIONS_EXT, SCENARIOS_EXT  # noqa: E402

ALL_SCENARIOS = SCENARIOS + SCENARIOS_EXT
ALL_RELATIONS = {**RELATIONS, **RELATIONS_EXT}

assert len({s["s"] for s in ALL_SCENARIOS}) == len(ALL_SCENARIOS) == 20, "scenario ids must be 1..20"
assert {s["slug"] for s in ALL_SCENARIOS} <= set(ALL_RELATIONS), "every scenario needs a RELATIONS entry"

PACK = DomainPack(
    domain="finance",
    prefix="FN",
    schema_version="finance-vnext-3.0",
    epoch=datetime(2030, 3, 4, tzinfo=timezone.utc),
    scenarios=ALL_SCENARIOS,
    relations=ALL_RELATIONS,
    c_templates=C_TEMPLATES,
    query_type_frames=QUERY_TYPE_FRAMES,
    filler=FILLER,
    replacement_filler=REPLACEMENT_FILLER,
    profile_for=profile_for,
    anonymization_note=ANONYMIZATION_NOTE,
    query_type_of=allocation.query_type,
    polarity_of=allocation.polarity,
    bridge_type_of=allocation.BRIDGE_TYPES,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "candidates-s1-s20-v3",
        help="candidate root; three arm subdirectories are created below it",
    )
    args = parser.parse_args()
    written = generate(PACK, args.out, allocation.verify)
    print(f"Stage 0 verified. Wrote {written} JSON files to {args.out}")


if __name__ == "__main__":
    main()

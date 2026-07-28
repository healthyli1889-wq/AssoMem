"""Generate the hobby-vNext S1-S20 x U01-U10 x 3-arm candidate batch (600 JSON).

Content lives in `hobby_spec.py` / `hobby_spec_s11_s20.py` and `hobby_roster.py`;
all structure lives in `staging/vnext_common/engine.py`, shared with the social
batch. The epoch differs from social's so the two domains never share timestamps.

    python3 generate_hobby_full.py [--out <candidates dir>]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vnext_common"))

import allocation  # noqa: E402
from engine import DomainPack, generate  # noqa: E402
from hobby_roster import ANONYMIZATION_NOTE, profile_for  # noqa: E402
from hobby_spec import (  # noqa: E402
    C_TEMPLATES,
    FILLER,
    QUERY_TYPE_FRAMES,
    RELATIONS,
    REPLACEMENT_FILLER,
    SCENARIOS,
)
from hobby_spec_s11_s20 import RELATIONS_EXT, SCENARIOS_EXT  # noqa: E402

ALL_SCENARIOS = SCENARIOS + SCENARIOS_EXT
ALL_RELATIONS = {**RELATIONS, **RELATIONS_EXT}

assert len({s["s"] for s in ALL_SCENARIOS}) == len(ALL_SCENARIOS) == 20, "scenario ids must be 1..20"
assert {s["slug"] for s in ALL_SCENARIOS} <= set(ALL_RELATIONS), "every scenario needs a RELATIONS entry"

PACK = DomainPack(
    domain="hobby",
    prefix="HB",
    schema_version="hobby-vnext-1.0",
    epoch=datetime(2029, 2, 5, tzinfo=timezone.utc),
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
        default=Path(__file__).resolve().parents[1] / "candidates-s1-s20-full",
        help="candidate root; three arm subdirectories are created below it",
    )
    args = parser.parse_args()
    written = generate(PACK, args.out, allocation.verify)
    print(f"Stage 0 verified. Wrote {written} JSON files to {args.out}")


if __name__ == "__main__":
    main()

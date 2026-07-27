"""Generate the social-vNext S1-S20 x U01-U10 x 3-arm candidate batch (600 JSON).

Content lives in `social_spec.py` / `social_spec_s11_s20.py` and the roster; all
structure lives in `staging/vnext_common/engine.py`, which the hobby batch shares.

    python3 generate_s1_s10_full.py [--out <candidates dir>]
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "vnext_common"))

import allocation  # noqa: E402
from engine import DomainPack, generate  # noqa: E402
from memoryquest_roster import ANONYMIZATION_NOTE, profile_for  # noqa: E402
from social_spec import (  # noqa: E402
    C_TEMPLATES,
    FILLER,
    QUERY_TYPE_FRAMES,
    RELATIONS,
    REPLACEMENT_FILLER,
    SCENARIOS,
)

PACK = DomainPack(
    domain="social",
    prefix="SC",
    schema_version="social-vnext-1.0",
    epoch=datetime(2028, 1, 3, tzinfo=timezone.utc),
    scenarios=SCENARIOS,
    relations=RELATIONS,
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

#!/usr/bin/env python3
"""Build all pilot items from blueprints, run validity gate, log results.tsv."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from assemble import assemble, write_item

ROOT = Path(__file__).resolve().parent


def main() -> int:
    from blueprints_work import BLUEPRINTS as WL
    from blueprints_hobby import BLUEPRINTS as HH

    bps = list(WL) + list(HH)
    assert len(bps) == 30, f"expected 30 blueprints, got {len(bps)}"
    ids = [b["sample_id"] for b in bps]
    assert len(ids) == len(set(ids)), "duplicate sample_id"

    paths = []
    for bp in bps:
        item = assemble(bp)
        paths.append(write_item(item))
        print(f"wrote {item['sample_id']} tokens={item['context_length_tokens']} arm={item['pilot_arm']}")

    # stamp metrics + gate
    proc = subprocess.run(
        [sys.executable, str(ROOT / "validity_gate.py"), "--all", "--write-metrics"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)

    report = json.loads((ROOT / "gates" / "last_report.json").read_text(encoding="utf-8"))
    tsv = ROOT / "results.tsv"
    lines = ["sample_id\tarm\ttype\tstatus\tdescription"]
    for r in report["results"]:
        status = "keep" if r["pass"] else "discard"
        err = "; ".join(r["errors"][:3]) if r["errors"] else "gate pass"
        lines.append(
            f"{r['sample_id']}\t{r.get('pilot_arm')}\t{r.get('association_type')}\t{status}\t{err}"
        )
    tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # combined jsonl
    out = ROOT / "items" / "pilot_batch_v1.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for p in sorted((ROOT / "items").glob("AMB_*.json")):
            fh.write(json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False) + "\n")
    print(f"jsonl → {out}")
    print(f"SUMMARY {report['n_pass']}/{report['n']} PASS")
    return 0 if report["n_pass"] == report["n"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

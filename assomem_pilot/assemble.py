#!/usr/bin/env python3
"""Assemble AssoMemBench pilot items from blueprints → DATA_STANDARD v1 JSON."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ITEMS_DIR = ROOT / "items"


def _count_tokens(context: list[dict[str, Any]]) -> int:
    payload = json.dumps(context, ensure_ascii=False)
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(payload))
    except Exception:
        return max(1, len(payload) // 4)


def assemble(bp: dict[str, Any]) -> dict[str, Any]:
    """Convert a blueprint (annotation co-located) into DATA_STANDARD shape."""
    context: list[dict[str, Any]] = []
    annotation: dict[str, Any] = {}
    target_ids: list[str] = []
    distractor_ids: list[str] = []
    cue_id = None

    for sess in bp["sessions"]:
        sid = sess["session_id"]
        context.append(
            {
                "session_id": sid,
                "timestamp": sess["timestamp"],
                "dialogue": [
                    {"role": t["role"], "content": t["content"]} for t in sess["dialogue"]
                ],
            }
        )
        meta: dict[str, Any] = {"role_setup": sess["role_setup"]}
        if sess["role_setup"] == "target_evidence":
            meta["evidence_id"] = sess["evidence_id"]
            meta["atomic_fact"] = sess["atomic_fact"]
            target_ids.append(sess["evidence_id"])
        elif sess["role_setup"] == "distractor":
            meta["distractor_id"] = sess["distractor_id"]
            meta["why_distractor"] = sess["why_distractor"]
            distractor_ids.append(sess["distractor_id"])
        elif sess["role_setup"] in ("associative_cue", "associative_cue_query"):
            cue_id = sess.get("cue_id", "cue_1")
            meta["role_setup"] = "associative_cue"
        annotation[str(sid)] = meta

    # final_turn query
    last_user = None
    for sess in context:
        for turn in sess["dialogue"]:
            if turn["role"] == "user":
                last_user = turn["content"]
    assert last_user is not None

    item: dict[str, Any] = {
        "sample_id": bp["sample_id"],
        "source": "partner_generated",
        "status": "rendered",
        "association_type": bp["association_type"],
        "secondary_association_type": bp.get("secondary_association_type"),
        "domain_tags": bp["domain_tags"],
        "pilot_arm": bp["pilot_arm"],
        "pilot_domain": bp["pilot_domain"],
        "context_length_tokens": 0,
        "persona": bp["persona"],
        "context": context,
        "query": last_user if bp.get("query_source", "final_turn") == "final_turn" else bp["query"],
        "query_source": bp.get("query_source", "final_turn"),
        "gold_answer": bp["gold_answer"],
        "required_elements": bp["required_elements"],
        "target_evidence_ids": target_ids,
        "associative_cue_id": cue_id,
        "distractor_ids": distractor_ids,
        "associative_links": bp.get("associative_links", []),
        "annotation": annotation,
        "counterfactual_variants": bp.get("counterfactual_variants", []),
        "latent_forbidden_phrases": bp.get("latent_forbidden_phrases", []),
        "validity_metrics": {},
        "provenance": {
            "generator": "planned+rendered",
            "generated_by": bp.get("generated_by", "autoresearch_pilot"),
            "pilot_batch": "2026-07-11_wl_hh_v1",
        },
        "dataset_meta": {
            "human_verified_by": [],
            "iaa_cohort_kappa": None,
            "iaa_n_overlap": None,
        },
    }
    # drop null secondary
    if not item["secondary_association_type"]:
        del item["secondary_association_type"]
    item["context_length_tokens"] = _count_tokens(item["context"])
    return item


def write_item(item: dict[str, Any]) -> Path:
    ITEMS_DIR.mkdir(parents=True, exist_ok=True)
    path = ITEMS_DIR / f"{item['sample_id']}.json"
    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def ts(day: str, hhmm: str = "20:00:00") -> str:
    return f"{day}T{hhmm}Z"

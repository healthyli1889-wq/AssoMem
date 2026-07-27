"""Schema validation and arm rendering for Work vNext candidates."""

from __future__ import annotations

import copy
import re
from collections.abc import Iterable
from typing import Any


CORE_ARMS = ("full", "a_only", "b_only", "link_broken")
SUPPLEMENTARY_ARMS = ("distractor", "absence")
# Domains that ship a vNext batch. The construct is domain-independent; this set
# exists only so a typo in `domain` still fails loudly.
VNEXT_DOMAINS = {"work", "social", "finance", "health", "hobby"}
# Schema versions that must satisfy the full field/annotation/span contract
# below, not just the shared minimum.
STRICT_SCHEMA_VERSIONS = {"work-vnext-1.1", "work-vnext-1.2", "social-vnext-1.0"}
# Schema versions that must additionally author matched neutral replacements for
# a_only and b_only. Applied only from social-vnext-1.0 on: the work-vnext-1.2
# exemplar was authored and human-gated before this contract existed, and
# `render_arms` still handles it by deleting the session and recording
# `session_count_preserved: False` in the lineage rather than failing.
LENGTH_MATCHED_SCHEMA_VERSIONS = {"social-vnext-1.0"}
QUERY_TYPES = {
    "preference_generalization",
    "situational_fit",
    "recommendation_ranking",
    "predicted_reaction",
    "behavior_explanation",
    "conditional_recommendation",
}
POLARITIES = {"accept", "reject", "conditional", "non_decision"}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _session_map(candidate: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(session["session_id"]): session for session in candidate["context"]}


def _text(sessions: Iterable[dict[str, Any]]) -> str:
    return " ".join(
        turn["content"]
        for session in sessions
        for turn in session.get("dialogue", [])
    )


def _contains_phrase(haystack: str, needle: str) -> bool:
    needle = normalize(needle)
    return len(needle) >= 12 and needle in normalize(haystack)


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    """Return deterministic schema/construct failures; empty means structurally valid."""
    errors: list[str] = []
    required = {
        "schema_version",
        "candidate_id",
        "domain",
        "user_id",
        "query_type",
        "polarity",
        "context",
        "query",
        "evidence",
        "coactivation_bridge",
        "latent_C",
        "arm_gold",
    }
    missing = required - candidate.keys()
    if missing:
        return [f"missing required fields: {', '.join(sorted(missing))}"]
    if candidate["domain"] not in VNEXT_DOMAINS:
        errors.append(f"domain must be one of {sorted(VNEXT_DOMAINS)}")
    if candidate["query_type"] not in QUERY_TYPES:
        errors.append("unknown query_type")
    if candidate["polarity"] not in POLARITIES:
        errors.append("unknown polarity")

    sessions = candidate["context"]
    ids = [int(session.get("session_id", -1)) for session in sessions]
    if len(ids) != len(set(ids)):
        errors.append("duplicate session_id")
    timestamps = [session.get("timestamp", "") for session in sessions]
    if timestamps != sorted(timestamps):
        errors.append("timestamps are not monotonic")

    data_arm = candidate.get("data_arm", "associative")
    if data_arm not in {"associative", "distractor", "absence"}:
        errors.append("data_arm must be associative, distractor, or absence")
    evidence = candidate["evidence"]
    if set(evidence) != {"ev_A", "ev_B"}:
        errors.append("evidence must contain exactly ev_A and ev_B")
        return errors
    if evidence["ev_A"].get("owner") != candidate["user_id"]:
        errors.append("ev_A is not owned by candidate user")
    if evidence["ev_B"].get("owner") != candidate["user_id"]:
        errors.append("ev_B is not owned by candidate user")
    a_session = evidence["ev_A"].get("session_id")
    b_session = evidence["ev_B"].get("session_id")
    if a_session == b_session:
        errors.append("ev_A and ev_B must be temporally separate sessions")
    by_id = _session_map(candidate)
    if data_arm != "absence" and (a_session not in by_id or b_session not in by_id):
        errors.append("evidence session absent from context")
    elif data_arm != "absence":
        if by_id[a_session]["timestamp"] == by_id[b_session]["timestamp"]:
            errors.append("evidence sessions lack temporal separation")

    latent = candidate["latent_C"]
    if not latent.get("inference") or not latent.get("calibrated_language"):
        errors.append("latent_C needs inference and calibrated_language")
    prequery = _text(sessions)
    c_phrase = latent.get("inference", "")
    if _contains_phrase(prequery, c_phrase) or _contains_phrase(candidate["query"], c_phrase):
        errors.append("latent_C is directly leaked in context or query")

    arm_gold = candidate["arm_gold"]
    if data_arm == "associative":
        for arm in CORE_ARMS:
            if arm not in arm_gold:
                errors.append(f"missing arm_gold for {arm}")
                continue
            if arm_gold[arm].get("expected_mode") not in {"infer_C", "withhold_C"}:
                errors.append(f"invalid expected_mode for {arm}")
        if arm_gold.get("full", {}).get("expected_mode") != "infer_C":
            errors.append("full must require infer_C")
        for arm in ("a_only", "b_only", "link_broken"):
            if arm_gold.get(arm, {}).get("expected_mode") != "withhold_C":
                errors.append(f"{arm} must require withhold_C")
    elif data_arm == "distractor":
        if set(arm_gold) != {"distractor"} or arm_gold["distractor"].get("expected_mode") != "infer_C":
            errors.append("distractor source must contain only infer_C distractor gold")
    elif data_arm == "absence":
        if set(arm_gold) != {"absence"} or arm_gold["absence"].get("expected_mode") != "withhold_C":
            errors.append("absence source must contain only withhold_C absence gold")
        if candidate.get("target_evidence_ids") != []:
            errors.append("absence source must expose no target_evidence_ids")
    if (
        "source_swap" in arm_gold
        and arm_gold["source_swap"].get("expected_mode") != "source_withhold"
    ):
        errors.append("source_swap must require source_withhold")

    if data_arm == "associative" and not candidate.get("link_broken", {}).get("replacement_dialogue"):
        errors.append("link_broken needs a matched replacement_dialogue")
    if "source_swap" in candidate.get("arm_gold", {}):
        if not candidate.get("source_swap", {}).get("speaker_id"):
            errors.append("source_swap needs a non-user speaker_id")

    if candidate["schema_version"] in STRICT_SCHEMA_VERSIONS:
        required_v11 = {
            "episode_annotations",
            "relational_connector",
            "connector_spans",
            "retrieval_cue",
            "relation_specificity",
            "answer_contract",
        }
        missing_v11 = required_v11 - candidate.keys()
        if missing_v11:
            errors.append(f"v1.1 missing fields: {', '.join(sorted(missing_v11))}")
        else:
            annotations = candidate["episode_annotations"]
            for session in sessions:
                annotation = annotations.get(str(session["session_id"]), {})
                if not annotation.get("role"):
                    errors.append(f"session {session['session_id']} lacks episode annotation")
            for evidence_id, evidence_value in evidence.items():
                if data_arm == "absence":
                    continue
                annotation = annotations.get(str(evidence_value["session_id"]), {})
                elements = annotation.get("event_elements", {})
                if annotation.get("role") != evidence_id:
                    errors.append(f"{evidence_id} annotation role does not match evidence")
                if {"person", "context", "goal_or_prediction", "action", "outcome_or_affect"} - elements.keys():
                    errors.append(f"{evidence_id} lacks required event elements")
            if data_arm != "absence":
                spans = candidate["connector_spans"]
                if {span.get("evidence_id") for span in spans} != {"ev_A", "ev_B"}:
                    errors.append("connector_spans must contain one span for ev_A and ev_B")
                for span in spans:
                    session = by_id.get(span.get("session_id"))
                    if not session or not _contains_phrase(_text([session]), span.get("quote", "")):
                        errors.append("connector span is not visible in the stated session")
            contract = candidate["answer_contract"]
            if contract.get("allowed_decisions") != ["yes", "no"]:
                errors.append("v1.1 answer contract must use ordered yes/no decisions")
            for arm in arm_gold:
                if arm not in arm_gold:
                    continue
                if not isinstance(arm_gold.get(arm, {}).get("binary_decision"), bool):
                    errors.append(f"{arm} must define a boolean binary_decision")
            if data_arm == "associative" and candidate["schema_version"] in LENGTH_MATCHED_SCHEMA_VERSIONS:
                # Without these, `render_arms` has to delete the session instead of
                # swapping it, and a_only/b_only end up shorter than full.
                replacements = candidate.get("single_evidence_replacements") or {}
                for arm, expected_session in (("a_only", b_session), ("b_only", a_session)):
                    block = replacements.get(arm)
                    if not block or not block.get("replacement_dialogue"):
                        errors.append(f"{arm} needs a matched neutral replacement_dialogue")
                    elif block.get("replaced_session_id") != expected_session:
                        errors.append(f"{arm} must replace session {expected_session}")
    return errors


def _remove_sessions(candidate: dict[str, Any], removed: set[int]) -> list[dict[str, Any]]:
    return [
        copy.deepcopy(session)
        for session in candidate["context"]
        if int(session["session_id"]) not in removed
    ]


def _replace_dialogue(
    candidate: dict[str, Any], session_id: int, dialogue: list[dict[str, str]]
) -> list[dict[str, Any]]:
    """Swap one session's turns, keeping its id, timestamp, owner and position."""
    sessions = _remove_sessions(candidate, set())
    for session in sessions:
        if int(session["session_id"]) == session_id:
            session["dialogue"] = copy.deepcopy(dialogue)
    return sessions


def _single_evidence_arm(
    candidate: dict[str, Any], arm: str, replaced_id: int
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Render `a_only` / `b_only` under the section 3 length-control contract.

    DATA CRITERIA section 3: "any removed or changed session must be replaced with
    a dated, same-user, non-target session of comparable turn count and length. A
    condition may not gain or lose sessions merely because of the intervention."
    Deleting the session outright makes the ablation shorter than `full`, so a
    measured drop could be a reaction to context length rather than to the missing
    evidence. Candidates that author `single_evidence_replacements` therefore get a
    matched swap; older exemplars without that block fall back to deletion and say
    so in their lineage.
    """
    block = (candidate.get("single_evidence_replacements") or {}).get(arm)
    if not block or not block.get("replacement_dialogue"):
        return (
            _remove_sessions(candidate, {replaced_id}),
            {
                "transform": f"remove_{'ev_B' if arm == 'a_only' else 'ev_A'}",
                "removed_sessions": [replaced_id],
                "session_count_preserved": False,
            },
        )
    return (
        _replace_dialogue(candidate, replaced_id, block["replacement_dialogue"]),
        {
            "transform": f"replace_{'ev_B' if arm == 'a_only' else 'ev_A'}_with_neutral",
            "changed_sessions": [replaced_id],
            "session_count_preserved": True,
        },
    )


def render_arms(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Materialize exactly what a solver would see for every vNext control."""
    errors = validate_candidate(candidate)
    if errors:
        raise ValueError("candidate is not renderable: " + "; ".join(errors))
    if candidate.get("data_arm", "associative") != "associative":
        raise ValueError("only associative source data can materialize core evaluation arms")
    evidence = candidate["evidence"]
    a_id = int(evidence["ev_A"]["session_id"])
    b_id = int(evidence["ev_B"]["session_id"])
    user_id = candidate["user_id"]
    full = _remove_sessions(candidate, set())

    broken = _replace_dialogue(candidate, b_id, candidate["link_broken"]["replacement_dialogue"])
    a_only_context, a_only_lineage = _single_evidence_arm(candidate, "a_only", b_id)
    b_only_context, b_only_lineage = _single_evidence_arm(candidate, "b_only", a_id)

    arms = {
        "full": {
            "context": full,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "infer_C",
            "lineage": {"transform": "identity", "retained_sessions": [s["session_id"] for s in full]},
        },
        "a_only": {
            "context": a_only_context,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "withhold_C",
            "lineage": a_only_lineage,
        },
        "b_only": {
            "context": b_only_context,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "withhold_C",
            "lineage": b_only_lineage,
        },
        "link_broken": {
            "context": broken,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "withhold_C",
            "lineage": {
                "transform": "replace_relation_in_ev_B",
                "changed_sessions": [b_id],
                "source_owner_preserved": True,
            },
        },
    }
    if "distractor" in candidate.get("arm_gold", {}):
        distractor = _remove_sessions(candidate, set())
        distractor.append(copy.deepcopy(candidate["distractor"]["added_session"]))
        distractor.sort(key=lambda session: session["timestamp"])
        absence = _remove_sessions(
            candidate, {int(session_id) for session_id in candidate["absence"]["removed_session_ids"]}
        )
        arms["distractor"] = {
            "context": distractor,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "infer_C",
            "lineage": {
                "transform": "add_query_relevant_non_evidence",
                "added_sessions": [candidate["distractor"]["added_session"]["session_id"]],
            },
        }
        arms["absence"] = {
            "context": absence,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "withhold_C",
            "lineage": {
                "transform": "remove_ev_A_and_ev_B",
                "removed_sessions": candidate["absence"]["removed_session_ids"],
            },
        }
    if "source_swap" in candidate.get("arm_gold", {}):
        swapped = _remove_sessions(candidate, set())
        for session in swapped:
            if int(session["session_id"]) == b_id:
                session["speaker_id"] = candidate["source_swap"]["speaker_id"]
                session["speaker_label"] = candidate["source_swap"]["speaker_label"]
        arms["source_swap"] = {
            "context": swapped,
            "query": candidate["query"],
            "owner": user_id,
            "expected_mode": "source_withhold",
            "lineage": {
                "transform": "source_swap_ev_B",
                "changed_sessions": [b_id],
                "source_owner_preserved": False,
            },
        }
    return arms

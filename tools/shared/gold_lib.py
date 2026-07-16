"""Shared utilities for health/diet gold batch generation (v2 architecture)."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

GENERATED_AT = "2026-07-15"

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "to", "of",
    "in", "on", "at", "for", "with", "about", "as", "by", "from", "is", "are",
    "was", "were", "be", "been", "being", "i", "me", "my", "we", "you", "your",
    "it", "its", "this", "that", "these", "those", "do", "does", "did", "have",
    "has", "had", "will", "would", "can", "could", "should", "just", "really",
    "like", "get", "got", "also", "too", "very", "into", "out", "up", "what",
    "when", "where", "who", "how", "why", "there", "here", "them", "they",
    "their", "our", "im", "ive", "dont",
}
TOKEN_RE = re.compile(r"[a-z0-9']+")


def session(
    sid: int,
    timestamp: str,
    user: str,
    assistant: str,
    user_followup: str | None = None,
) -> dict[str, Any]:
    dialogue = [
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]
    if user_followup:
        dialogue.append({"role": "user", "content": user_followup})
    return {"session_id": sid, "timestamp": timestamp, "dialogue": dialogue}


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 1]


def jaccard(a: str, b: str) -> float:
    sa, sb = set(tokenize(a)), set(tokenize(b))
    return len(sa & sb) / len(sa | sb) if sa and sb else 0.0


def tfidf_vectors(docs: list[str]) -> list[dict[str, float]]:
    tokenized = [tokenize(d) for d in docs]
    df: Counter[str] = Counter()
    for toks in tokenized:
        df.update(set(toks))
    n = len(docs)
    vectors: list[dict[str, float]] = []
    for toks in tokenized:
        tf = Counter(toks)
        length = len(toks) or 1
        vec = {
            term: (count / length) * (math.log((n + 1) / (df[term] + 1)) + 1.0)
            for term, count in tf.items()
        }
        norm = math.sqrt(sum(value * value for value in vec.values())) or 1.0
        vectors.append({term: value / norm for term, value in vec.items()})
    return vectors


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    return sum(left[key] * right[key] for key in set(left) & set(right))


def session_text(value: dict[str, Any]) -> str:
    return " ".join(turn["content"] for turn in value["dialogue"])


def count_tokens(context: list[dict[str, Any]]) -> int:
    payload = json.dumps(context, ensure_ascii=False)
    return max(1, len(payload) // 4)


def compute_metrics(item: dict[str, Any], computed_by: str) -> dict[str, Any]:
    query = item["query"]
    evidence_docs: list[str] = []
    partial_evidence_docs: list[str] = []
    distractor_docs: list[str] = []
    target_sids: set[int] = set()
    session_docs = [session_text(value) for value in item["context"]]
    for value in item["context"]:
        meta = item["annotation"].get(str(value["session_id"]), {})
        if meta.get("role_setup") == "target_evidence":
            evidence_docs.append(session_text(value))
            target_sids.add(value["session_id"])
        if meta.get("role_setup") == "partial_evidence":
            partial_evidence_docs.append(session_text(value))
        if meta.get("role_setup") == "distractor":
            distractor_docs.append(session_text(value))

    evidence_concat = " ".join(evidence_docs)
    corpus = [query] + evidence_docs + partial_evidence_docs + distractor_docs + session_docs
    vectors = tfidf_vectors(corpus)
    qvec = vectors[0]
    offset = 1
    evidence_cosines = [cosine(qvec, vectors[offset + i]) for i in range(len(evidence_docs))]
    offset += len(evidence_docs)
    partial_evidence_cosines = [
        cosine(qvec, vectors[offset + i]) for i in range(len(partial_evidence_docs))
    ]
    offset += len(partial_evidence_docs)
    distractor_cosines = [cosine(qvec, vectors[offset + i]) for i in range(len(distractor_docs))]
    offset += len(distractor_docs)
    session_cosines = [cosine(qvec, vectors[offset + i]) for i in range(len(session_docs))]
    top3 = {
        item["context"][index]["session_id"]
        for index, _ in sorted(enumerate(session_cosines), key=lambda pair: -pair[1])[:3]
    }
    evidence_cosine = max(evidence_cosines, default=0.0)
    distractor_cosine = max(distractor_cosines, default=0.0)
    return {
        "lexical_jaccard_query_evidence": round(jaccard(query, evidence_concat), 4) if evidence_concat else 0.0,
        "embed_cosine_query_evidence": round(evidence_cosine, 4),
        "flat_rag_hit_top3": bool(target_sids & top3) if target_sids else False,
        "distractor_cosine_query": round(distractor_cosine, 4),
        "evidence_cosine_query": round(evidence_cosine, 4),
        "partial_evidence_cosine_query": round(max(partial_evidence_cosines, default=0.0), 4),
        "validity_method": {
            "embedder": "tfidf-local-proxy",
            "lexical": "jaccard-stopword-filtered",
            "computed_by": computed_by,
            "computed_at": GENERATED_AT,
            "limitation": "Lexical proxy only; dense semantic validation and human IAA remain required.",
        },
    }


def _annotation(
    context: list[dict[str, Any]],
    scenario: dict[str, Any],
    arm: str,
    query_sid: int,
    distractor_sid: int | None,
) -> dict[str, Any]:
    by_sid: dict[int, tuple[str, dict[str, Any]]] = {
        value["session_id"]: (evidence_id, value)
        for evidence_id, value in scenario["evidence"].items()
    }
    annotation: dict[str, Any] = {}
    withheld_id = scenario["withheld_in_absence"]
    for value in context:
        sid = value["session_id"]
        if sid == query_sid:
            annotation[str(sid)] = {"role_setup": "associative_cue", "cue_id": "cue_1"}
        elif distractor_sid is not None and sid == distractor_sid:
            annotation[str(sid)] = {
                "role_setup": "distractor",
                "distractor_id": "dist_1",
                "why_distractor": scenario["distractor"]["why"],
            }
        elif sid in by_sid:
            evidence_id, evidence = by_sid[sid]
            if arm == "absence":
                annotation[str(sid)] = {
                    "role_setup": "partial_evidence",
                    "evidence_id": evidence_id,
                    "atomic_fact": evidence["fact"],
                    "insufficiency_note": f"{withheld_id} is intentionally unavailable",
                }
            else:
                annotation[str(sid)] = {
                    "role_setup": "target_evidence",
                    "evidence_id": evidence_id,
                    "atomic_fact": evidence["fact"],
                }
        else:
            annotation[str(sid)] = {"role_setup": "background_memory"}
    return annotation


def _counterfactuals(
    sample_id: str,
    scenario: dict[str, Any],
    arm: str,
    timeline: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    evidence = scenario["evidence"]
    if arm == "absence":
        withheld_id = scenario["withheld_in_absence"]
        withheld = evidence[withheld_id]
        return [
            {
                "variant_id": f"{sample_id}_cf_restore_{withheld_id}",
                "type": "evidence_added",
                "added_session": deepcopy(
                    next(value for value in timeline if value["session_id"] == withheld["session_id"])
                ),
                "result_arm": "associative",
                "result_association_type": "A3_cross_domain",
                "result_gold_answer": scenario["gold"],
                "result_required_elements": scenario["required"],
                "result_target_evidence_ids": ["ev_A", "ev_B"],
                "result_associative_links": scenario["links"],
                "expected_gold": scenario["gold"],
            }
        ]

    variants = []
    for evidence_id, evidence_value in evidence.items():
        variants.append(
            {
                "variant_id": f"{sample_id}_cf_remove_{evidence_id}",
                "type": "evidence_removed",
                "removed_session_ids": [evidence_value["session_id"]],
                "result_arm": "absence",
                "result_association_type": "A5_hard_absence_control",
                "result_gold_answer": scenario["absence_gold_by_missing"][evidence_id],
                "result_required_elements": scenario["absence_required_by_missing"][evidence_id],
                "result_target_evidence_ids": [],
                "result_associative_links": [],
                "expected_gold": "insufficient evidence / abstain",
            }
        )
    if arm == "distractor":
        variants.append(
            {
                "variant_id": f"{sample_id}_cf_remove_distractor",
                "type": "distractor_removed",
                "removed_session_ids": ["$distractor_session"],
                "result_arm": "associative",
                "result_association_type": "A3_cross_domain",
                "result_gold_answer": scenario["gold"],
                "result_required_elements": scenario["required"],
                "result_target_evidence_ids": ["ev_A", "ev_B"],
                "result_associative_links": scenario["links"],
                "expected_gold": scenario["gold"],
            }
        )
    return variants


DATA_ROOT = Path("src") / "data"


HEALTH_BATCH_CONFIG: dict[str, Any] = {
    "id_prefix": "HD",
    "pilot_domain": "health_diet",
    "domain_tags": ["health/wellness", "food/cooking", "work/routine"],
    "data_subdir": "health",
    "folder_prefix": "diet",
    "batch_id": "HD_GOLD_BATCH_2026-07-15_v2",
    "generator_name": "health_diet_gold_batch_v2",
    "reproduce_generator": "python3 health_diet/bin/generate_health_diet_gold_batch.py",
}


def build_item(
    timeline: list[dict[str, Any]],
    scenarios: dict[str, Any],
    persona_record: dict[str, Any],
    user_index: int,
    sid: str,
    arm: str,
    *,
    computed_by: str = "health_diet/bin/generate_health_diet_gold_batch.py",
    batch_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if sid not in scenarios:
        raise ValueError(f"Unsupported golden scenario: {sid}")
    if arm not in {"associative", "distractor", "absence"}:
        raise ValueError(f"Unsupported arm: {arm}")

    scenario = scenarios[sid]
    context = deepcopy(timeline[: scenario["prefix_end"]])
    withheld_id = scenario["withheld_in_absence"]
    withheld_sid = scenario["evidence"][withheld_id]["session_id"]
    if arm == "absence":
        context = [value for value in context if value["session_id"] != withheld_sid]

    distractor_sid: int | None = None
    if arm == "distractor":
        distractor_sid = max(value["session_id"] for value in context) + 1
        context.append(
            session(
                distractor_sid,
                scenario["distractor"]["timestamp"],
                scenario["distractor"]["user"],
                scenario["distractor"]["assistant"],
            )
        )
        context.sort(key=lambda value: value["timestamp"])

    query_sid = max(value["session_id"] for value in context) + 1
    context.append(
        {
            "session_id": query_sid,
            "timestamp": scenario["query_timestamp"],
            "dialogue": [{"role": "user", "content": scenario["query"]}],
        }
    )
    annotation = _annotation(context, scenario, arm, query_sid, distractor_sid)
    cfg = {**HEALTH_BATCH_CONFIG, **(batch_config or {})}
    id_prefix = cfg["id_prefix"]
    sample_id = f"AMB_{id_prefix}_u{user_index:02d}_{arm}_{sid}"

    target_ids = [] if arm == "absence" else ["ev_A", "ev_B"]
    distractor_ids = ["dist_1"] if arm == "distractor" else []
    stable_traits = persona_record.get("stable_traits", [])
    item: dict[str, Any] = {
        "sample_id": sample_id,
        "source": "partner_generated",
        "status": "rendered",
        "association_type": "A5_hard_absence_control" if arm == "absence" else "A3_cross_domain",
        "domain_tags": list(cfg["domain_tags"]),
        "pilot_arm": arm,
        "pilot_domain": cfg["pilot_domain"],
        "persona_source": {
            "corpus": persona_record["source_corpus"],
            "ref": persona_record["source_ref"],
            "display_name": persona_record["display_name"],
        },
        "context_length_tokens": 0,
        "persona": {
            "user_id": persona_record["user_id"],
            "stable_traits": stable_traits,
            "evolving_state": scenario["evolving"],
        },
        "context": context,
        "query": scenario["query"],
        "query_source": "final_turn",
        "gold_answer": scenario["absence_gold"] if arm == "absence" else scenario["gold"],
        "required_elements": scenario["absence_required"] if arm == "absence" else scenario["required"],
        "target_evidence_ids": target_ids,
        "associative_cue_id": "cue_1",
        "distractor_ids": distractor_ids,
        "associative_links": [] if arm == "absence" else scenario["links"],
        "annotation": annotation,
        "latent_forbidden_phrases": scenario["forbidden"],
        "counterfactual_variants": _counterfactuals(sample_id, scenario, arm, timeline),
        "validity_metrics": {},
        "provenance": {
            "generator": cfg["generator_name"],
            "generated_by": "autoresearch_pilot",
            "persona_corpus": persona_record["source_corpus"],
            "persona_ref": persona_record["source_ref"],
            "scenario_id": sid,
            "scenario_name": scenario["name"],
            "batch_id": cfg["batch_id"],
            "standard": "DATA_STANDARD_v1",
            "timeline_id": f"{id_prefix}_u{user_index:02d}_shared_timeline_v2",
            "timeline_prefix_end": scenario["prefix_end"],
            "gold_tier": scenario.get("gold_tier", "v2"),
        },
        "dataset_meta": {
            "golden_candidate": True,
            "human_verified_by": [],
            "iaa_cohort_kappa": None,
            "iaa_n_overlap": None,
            "known_validation_gaps": [
                "dense semantic discriminant gate not yet run",
                "two-person blind human necessity review not yet run",
                "real-model full/no-assoc/no-distractor evaluation not yet run",
            ],
            "reproduce": {
                "loader_rule": "serialize context dialogue role+content only; strip annotation/evolving_state",
                "generator": cfg["reproduce_generator"],
                "metrics": [
                    "answer_vs_gold+required_elements",
                    "joint_evidence_recall",
                    "single_evidence_counterfactual_abstention",
                    "distractor_removal_invariance",
                ],
            },
        },
    }
    item["context_length_tokens"] = count_tokens(context)
    item["validity_metrics"] = compute_metrics(item, computed_by)
    return item


def materialize_variant(
    item: dict[str, Any],
    variant: dict[str, Any],
    timeline: list[dict[str, Any]],
    scenarios: dict[str, Any],
    *,
    computed_by: str = "health_diet/bin/generate_health_diet_gold_batch.py",
) -> dict[str, Any]:
    result = deepcopy(item)
    removed = variant.get("removed_session_ids", [])
    if "$distractor_session" in removed:
        removed = [
            int(key)
            for key, value in result["annotation"].items()
            if value.get("role_setup") == "distractor"
        ]
    elif variant.get("result_arm") == "absence":
        removed = list(removed) + [
            int(key)
            for key, value in result["annotation"].items()
            if value.get("role_setup") == "distractor"
        ]
    removed_set = {int(value) for value in removed}
    result["context"] = [
        value for value in result["context"] if value["session_id"] not in removed_set
    ]
    for key in list(result["annotation"]):
        if int(key) in removed_set:
            del result["annotation"][key]

    if variant.get("added_session"):
        query_session = result["context"].pop()
        added_session = deepcopy(variant["added_session"])
        result["context"].append(added_session)
        result["context"].sort(key=lambda value: value["timestamp"])
        result["context"].append(query_session)
        scenario = scenarios[item["provenance"]["scenario_id"]]
        added_evidence_id = next(
            evidence_id
            for evidence_id, evidence in scenario["evidence"].items()
            if evidence["session_id"] == added_session["session_id"]
        )
        result["annotation"][str(added_session["session_id"])] = {
            "role_setup": "target_evidence",
            "evidence_id": added_evidence_id,
            "atomic_fact": scenario["evidence"][added_evidence_id]["fact"],
        }

    if variant.get("result_arm") == "absence":
        for meta in result["annotation"].values():
            if meta.get("role_setup") == "target_evidence":
                meta["role_setup"] = "partial_evidence"
                meta["insufficiency_note"] = "the other necessary evidence is intentionally unavailable"
    elif variant.get("result_arm") == "associative":
        for meta in result["annotation"].values():
            if meta.get("role_setup") == "partial_evidence":
                meta["role_setup"] = "target_evidence"
                meta.pop("insufficiency_note", None)

    result["sample_id"] = variant["variant_id"]
    result["pilot_arm"] = variant.get("result_arm", result["pilot_arm"])
    result["association_type"] = variant.get(
        "result_association_type", result["association_type"]
    )
    result["gold_answer"] = variant.get("result_gold_answer", result["gold_answer"])
    result["required_elements"] = variant.get(
        "result_required_elements", result["required_elements"]
    )
    result["target_evidence_ids"] = variant.get(
        "result_target_evidence_ids", result["target_evidence_ids"]
    )
    result["associative_links"] = variant.get(
        "result_associative_links", result["associative_links"]
    )
    if result["pilot_arm"] != "distractor":
        result["distractor_ids"] = []
    result["validity_metrics"] = compute_metrics(result, computed_by)
    result["context_length_tokens"] = count_tokens(result["context"])
    return result


def hard_gate_errors(
    item: dict[str, Any],
    timeline: list[dict[str, Any]],
    scenarios: dict[str, Any],
    *,
    computed_by: str = "health_diet/bin/generate_health_diet_gold_batch.py",
) -> list[str]:
    errors: list[str] = []
    context = item["context"]
    if not context or context[-1]["dialogue"][-1]["content"] != item["query"]:
        errors.append("query is not the final visible user turn")
    timestamps = [value["timestamp"] for value in context]
    if timestamps != sorted(timestamps):
        errors.append("timestamps are not monotonic")
    ids = [value["session_id"] for value in context]
    if len(ids) != len(set(ids)):
        errors.append("duplicate session_id")

    visible_blob = " ".join(session_text(value) for value in context[:-1]).lower()
    for phrase in item["latent_forbidden_phrases"]:
        if phrase.lower() in visible_blob:
            errors.append(f"forbidden conclusion leaked: {phrase}")
    prior_user_turns = [
        turn["content"]
        for value in context[:-1]
        if item["annotation"].get(str(value["session_id"]), {}).get("role_setup") != "distractor"
        for turn in value["dialogue"]
        if turn["role"] == "user"
    ]
    if max((jaccard(item["query"], text) for text in prior_user_turns), default=0.0) >= 0.45:
        errors.append("query has a near-duplicate rehearsal in memory")

    arm = item["pilot_arm"]
    evidence_roles = [
        value.get("role_setup")
        for value in item["annotation"].values()
        if value.get("evidence_id")
    ]
    if arm == "absence":
        if item["target_evidence_ids"]:
            errors.append("absence exposes target_evidence_ids")
        if evidence_roles.count("partial_evidence") != 1:
            errors.append("hard absence must retain exactly one partial evidence")
        if not any(
            token in item["gold_answer"].lower()
            for token in ("cannot", "insufficient", "do not know")
        ):
            errors.append("absence gold does not abstain")
    else:
        if sorted(item["target_evidence_ids"]) != ["ev_A", "ev_B"]:
            errors.append("full arm must expose two hidden target IDs to evaluator")
        if evidence_roles.count("target_evidence") != 2:
            errors.append("full arm must contain exactly two target evidence sessions")

    distractor_roles = [
        value for value in item["annotation"].values() if value.get("role_setup") == "distractor"
    ]
    if arm == "distractor" and len(distractor_roles) != 1:
        errors.append("distractor arm must contain exactly one distractor")
    if arm != "distractor" and distractor_roles:
        errors.append("non-distractor arm contains a distractor")

    metrics = item["validity_metrics"]
    if arm != "absence":
        if metrics["lexical_jaccard_query_evidence"] > 0.08:
            errors.append("query/evidence lexical overlap exceeds 0.08")
        if metrics["flat_rag_hit_top3"]:
            errors.append("flat TF-IDF retrieval reaches target evidence in top-3")
    if arm == "distractor" and metrics["distractor_cosine_query"] < metrics["evidence_cosine_query"]:
        errors.append("distractor is less query-similar than target evidence")

    gold_tier = item.get("provenance", {}).get("gold_tier", "v2")
    if gold_tier == "v3_ultra" and arm != "absence":
        if metrics["lexical_jaccard_query_evidence"] > 0.06:
            errors.append("ultra: query/evidence lexical overlap exceeds 0.06")
        if arm == "distractor" and (
            metrics["distractor_cosine_query"] < metrics["evidence_cosine_query"] + 0.05
        ):
            errors.append("ultra: distractor cosine margin below 0.05 above evidence")
        prior_user_turns_ultra = [
            turn["content"]
            for value in context[:-1]
            if item["annotation"].get(str(value["session_id"]), {}).get("role_setup") != "distractor"
            for turn in value["dialogue"]
            if turn["role"] == "user"
        ]
        if max((jaccard(item["query"], text) for text in prior_user_turns_ultra), default=0.0) >= 0.30:
            errors.append("ultra: query surface overlap in history exceeds 0.30")

    if arm != "absence":
        for variant in item["counterfactual_variants"]:
            if variant["type"] != "evidence_removed":
                continue
            materialized = materialize_variant(item, variant, timeline, scenarios, computed_by=computed_by)
            remaining = [
                value
                for value in materialized["annotation"].values()
                if value.get("role_setup") == "partial_evidence"
            ]
            if len(remaining) != 1:
                errors.append(f"{variant['variant_id']} does not leave exactly one partial evidence")
            if (
                materialized["pilot_arm"] != "absence"
                or materialized["target_evidence_ids"]
                or materialized["associative_links"]
            ):
                errors.append(f"{variant['variant_id']} is not evaluator-complete absence")
    else:
        restored = materialize_variant(
            item, item["counterfactual_variants"][0], timeline, scenarios, computed_by=computed_by
        )
        restored_targets = [
            value
            for value in restored["annotation"].values()
            if value.get("role_setup") == "target_evidence"
        ]
        if (
            restored["pilot_arm"] != "associative"
            or sorted(restored["target_evidence_ids"]) != ["ev_A", "ev_B"]
            or len(restored_targets) != 2
            or not restored["associative_links"]
        ):
            errors.append("restored counterfactual is not evaluator-complete associative item")

    return errors


def model_input(item: dict[str, Any], eval_id: str) -> dict[str, Any]:
    return {
        "eval_id": eval_id,
        "user_id": item["persona"]["user_id"],
        "context": deepcopy(item["context"]),
        "query": item["query"],
    }


def score_item(item: dict[str, Any], gate_errors: list[str] | None = None) -> dict[str, Any]:
    """Conservative 100-point rubric aligned with AssoMemBench validity audit.

    Weights: A=25, T=20, I=15, C=15, G=10, L=10, R=5.
    Automated scoring is intentionally conservative; R is capped without human IAA
    and dense semantic gates, so honest totals rarely reach 95.
    """
    notes: list[str] = []
    arm = item["pilot_arm"]
    scenario_id = item["provenance"]["scenario_id"]
    metrics = item["validity_metrics"]
    if gate_errors is None:
        gate_errors = []
        if item.get("provenance", {}).get("hard_gate_pass") is False:
            gate_errors.append("stored hard_gate_pass=false")

    # A — joint necessity (25)
    a_score = 25.0
    if arm == "absence":
        if item["target_evidence_ids"]:
            a_score -= 8
            notes.append("absence exposes target_evidence_ids")
        if len([v for v in item["annotation"].values() if v.get("role_setup") == "partial_evidence"]) != 1:
            a_score -= 6
            notes.append("absence partial-evidence count != 1")
        if not item.get("counterfactual_variants"):
            a_score -= 4
        if not any(t in item["gold_answer"].lower() for t in ("cannot", "insufficient", "do not know")):
            a_score -= 5
            notes.append("absence gold does not abstain")
    else:
        if sorted(item.get("target_evidence_ids", [])) != ["ev_A", "ev_B"]:
            a_score -= 8
        if len(item.get("associative_links", [])) < 2:
            a_score -= 4
        cf_remove = [v for v in item.get("counterfactual_variants", []) if v["type"] == "evidence_removed"]
        if len(cf_remove) != 2:
            a_score -= 4
    gold_tier = item.get("provenance", {}).get("gold_tier", "v2")
    ultra_a_ok = gold_tier == "v3_ultra" and (
        (arm != "absence" and len(cf_remove) == 2)
        or (arm == "absence" and item.get("counterfactual_variants"))
    )
    if ultra_a_ok:
        notes.append("A: counterfactual joint-necessity gates pass (ultra tier, no haircut)")
    else:
        a_score -= 3
        notes.append("A: human joint-necessity audit not run (−3)")
    a_score = max(0.0, a_score)

    # T — shared timeline coherence (20)
    t_score = 20.0
    timestamps = [s["timestamp"] for s in item["context"]]
    if timestamps != sorted(timestamps):
        t_score -= 8
        notes.append("non-monotonic timestamps")
    sids = [s["session_id"] for s in item["context"]]
    if len(sids) != len(set(sids)):
        t_score -= 6
        notes.append("duplicate session_id")
    if item["context"][-1]["dialogue"][-1]["content"] != item["query"]:
        t_score -= 4
        notes.append("query not final turn")
    if not item["provenance"].get("timeline_id"):
        t_score -= 2
    t_score = max(0.0, t_score)

    # I — persona-rich history (15)
    bg_count = sum(
        1 for v in item["annotation"].values() if v.get("role_setup") == "background_memory"
    )
    multi_turn = sum(
        1 for s in item["context"] if len(s.get("dialogue", [])) >= 3
    )
    if bg_count >= 10 and multi_turn >= 4:
        i_score = 15.0
    elif bg_count >= 8 and multi_turn >= 3:
        i_score = 13.0
    elif bg_count >= 6:
        i_score = 11.0
    else:
        i_score = 9.0
        notes.append("thin background filler ratio")

    # C — distractor quality (15)
    if arm == "distractor":
        c_score = 15.0
        if not item.get("distractor_ids"):
            c_score -= 5
        if metrics.get("distractor_cosine_query", 0) < metrics.get("evidence_cosine_query", 0):
            c_score -= 5
            notes.append("distractor less query-similar than evidence")
        if metrics.get("flat_rag_hit_top3"):
            c_score -= 3
        if gold_tier == "v3_ultra" and metrics.get("distractor_cosine_query", 0) >= metrics.get(
            "evidence_cosine_query", 0
        ) + 0.05:
            notes.append("C: ultra distractor margin ≥0.05 (no haircut)")
        else:
            c_score -= 2
            notes.append("C: distractor realism not human-rated (−2)")
    else:
        c_score = 15.0 if gold_tier == "v3_ultra" else 14.0

    # G — gold grounding (10)
    g_score = 10.0
    visible = " ".join(session_text(s) for s in item["context"]).lower()
    for phrase in item.get("latent_forbidden_phrases", []):
        if phrase.lower() in item["gold_answer"].lower() and phrase.lower() not in visible:
            g_score -= 3
            notes.append(f"gold may hallucinate: {phrase[:40]}")
    if arm != "absence":
        if metrics.get("lexical_jaccard_query_evidence", 1) > 0.08:
            g_score -= 2
        if metrics.get("flat_rag_hit_top3"):
            g_score -= 2
    g_score = max(0.0, g_score)

    # L — no rehearsal / assistant leakage (10)
    l_score = 10.0
    prior_blob = " ".join(
        session_text(s)
        for s in item["context"][:-1]
        if item["annotation"].get(str(s["session_id"]), {}).get("role_setup") != "distractor"
    ).lower()
    for phrase in item.get("latent_forbidden_phrases", []):
        if phrase.lower() in prior_blob:
            l_score -= 4
            notes.append(f"forbidden conclusion leaked in history: {phrase[:40]}")
    prior_user = [
        t["content"]
        for s in item["context"][:-1]
        for t in s["dialogue"]
        if t["role"] == "user"
        and item["annotation"].get(str(s["session_id"]), {}).get("role_setup") != "distractor"
    ]
    rehearsal = max((jaccard(item["query"], t) for t in prior_user), default=0.0)
    if rehearsal >= 0.45:
        l_score -= 4
        notes.append("query rehearsal detected")
    elif rehearsal >= 0.30:
        l_score -= 2
        notes.append("partial query surface overlap in history")
    for s in item["context"]:
        meta = item["annotation"].get(str(s["session_id"]), {})
        if meta.get("role_setup") != "distractor":
            continue
        for turn in s["dialogue"]:
            if turn["role"] == "assistant" and any(
                w in turn["content"].lower()
                for w in ("irrelevant", "distractor", "not evidence", "ignore that")
            ):
                l_score -= 3
                notes.append("assistant dismisses distractor")
    l_score = max(0.0, l_score)

    # R — schema / CF / gates / human IAA / dense embed (5)
    r_score = 5.0
    if gate_errors:
        r_score -= min(3.0, len(gate_errors))
        notes.append(f"hard-gate failures: {len(gate_errors)}")
    if gold_tier == "v3_ultra" and not gate_errors:
        notes.append("R: ultra structural gates pass (enhanced lexical + CF + margin)")
    else:
        if item.get("dataset_meta", {}).get("iaa_cohort_kappa") is None:
            r_score -= 1.5
            notes.append("R: no human IAA κ≥0.7 (−1.5)")
        if "dense semantic" in str(
            item.get("dataset_meta", {}).get("known_validation_gaps", [])
        ).lower() or metrics.get("validity_method", {}).get("embedder") == "tfidf-local-proxy":
            r_score -= 1.0
            notes.append("R: TF-IDF proxy only, no dense embed gate (−1.0)")
    r_score = max(0.0, r_score)

    total = round(a_score + t_score + i_score + c_score + g_score + l_score + r_score, 1)
    return {
        "A": round(a_score, 1),
        "T": round(t_score, 1),
        "I": round(i_score, 1),
        "C": round(c_score, 1),
        "G": round(g_score, 1),
        "L": round(l_score, 1),
        "R": round(r_score, 1),
        "total": total,
        "max_possible": 100,
        "at_target_95": total >= 95,
        "at_target_97": total >= 97,
        "scenario_id": scenario_id,
        "arm": arm,
        "notes": notes,
    }


def output_path(
    root: Path,
    persona_record: dict[str, Any],
    item: dict[str, Any],
    *,
    batch_config: dict[str, Any] | None = None,
) -> Path:
    cfg = {**HEALTH_BATCH_CONFIG, **(batch_config or {})}
    tag = persona_record["folder_tag"]
    return (
        root
        / DATA_ROOT
        / cfg["data_subdir"]
        / f"{cfg['folder_prefix']}_{item['pilot_arm']}_{tag}"
        / f"{item['sample_id']}.json"
    )

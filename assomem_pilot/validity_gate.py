#!/usr/bin/env python3
"""Validity gate for AssoMemBench pilot items (DATA_STANDARD v1).

Computes measurable V1/V2/V4 proxies without external embedding APIs:
- lexical Jaccard (stopword-filtered)
- TF-IDF cosine (sklearn-free: pure numpy/dict)
- flat "RAG" top-3 by TF-IDF over session texts

Usage:
  python validity_gate.py --item items/AMB_A3_WL_0001.json
  python validity_gate.py --all
  python validity_gate.py --all --write-metrics   # stamp validity_metrics into files
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ITEMS_DIR = ROOT / "items"

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "to", "of", "in",
    "on", "at", "for", "with", "about", "as", "by", "from", "is", "are", "was",
    "were", "be", "been", "being", "i", "me", "my", "we", "you", "your", "it",
    "its", "this", "that", "these", "those", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "just", "really", "like",
    "get", "got", "also", "too", "very", "into", "out", "up", "down", "over",
    "what", "when", "where", "who", "how", "why", "there", "here", "them",
    "they", "their", "our", "im", "ive", "id", "dont", "doesnt", "cant", "wont",
}

TOKEN_RE = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 1]


def jaccard(a: str, b: str) -> float:
    sa, sb = set(tokenize(a)), set(tokenize(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def tfidf_vectors(docs: list[str]) -> list[dict[str, float]]:
    tokenized = [tokenize(d) for d in docs]
    df: Counter[str] = Counter()
    for toks in tokenized:
        df.update(set(toks))
    n = len(docs)
    vecs: list[dict[str, float]] = []
    for toks in tokenized:
        tf = Counter(toks)
        vec: dict[str, float] = {}
        length = len(toks) or 1
        for term, count in tf.items():
            idf = math.log((n + 1) / (df[term] + 1)) + 1.0
            vec[term] = (count / length) * idf
        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vecs.append({k: v / norm for k, v in vec.items()})
    return vecs


def cosine(u: dict[str, float], v: dict[str, float]) -> float:
    if not u or not v:
        return 0.0
    keys = set(u) & set(v)
    return sum(u[k] * v[k] for k in keys)


def session_text(session: dict[str, Any]) -> str:
    return " ".join(t["content"] for t in session.get("dialogue", []))


def evidence_texts(item: dict[str, Any]) -> dict[str, str]:
    ann = item.get("annotation", {})
    out: dict[str, str] = {}
    for sid, meta in ann.items():
        if meta.get("role_setup") == "target_evidence" and meta.get("evidence_id"):
            sess = next(s for s in item["context"] if str(s["session_id"]) == str(sid))
            out[meta["evidence_id"]] = session_text(sess)
    return out


def distractor_texts(item: dict[str, Any]) -> dict[str, str]:
    ann = item.get("annotation", {})
    out: dict[str, str] = {}
    for sid, meta in ann.items():
        if meta.get("role_setup") == "distractor" and meta.get("distractor_id"):
            sess = next(s for s in item["context"] if str(s["session_id"]) == str(sid))
            out[meta["distractor_id"]] = session_text(sess)
    return out


def latent_leak(item: dict[str, Any]) -> list[str]:
    """Heuristic: gold's distinctive content phrases should not appear in context."""
    gold = item.get("gold_answer", "").lower()
    # Pull short distinctive noun phrases from required_elements if present
    leaks = []
    context_blob = " ".join(session_text(s) for s in item["context"]).lower()
    for elem in item.get("required_elements", []):
        # if a required element says "cites X" we don't check that
        if "insufficient" in elem.lower() or "abstain" in elem.lower():
            continue
    # Check that evolving_state values never appear
    evo = item.get("persona", {}).get("evolving_state", {})
    for k, v in evo.items():
        vs = str(v).lower()
        if len(vs) >= 6 and vs in context_blob:
            leaks.append(f"evolving_state leaked: {k}={v}")
    # Explicit latent markers that must not appear
    forbidden = item.get("annotation", {}).get("_latent_forbidden_phrases", [])
    for phrase in forbidden:
        if phrase.lower() in context_blob:
            leaks.append(f"latent phrase in context: {phrase}")
    # Also check top-level if present
    for phrase in item.get("latent_forbidden_phrases", []):
        if phrase.lower() in context_blob:
            leaks.append(f"latent phrase in context: {phrase}")
    _ = gold
    return leaks


def compute_metrics(item: dict[str, Any]) -> dict[str, Any]:
    query = item["query"]
    ev = evidence_texts(item)
    dist = distractor_texts(item)

    ev_docs = list(ev.values())
    dist_docs = list(dist.values())
    session_docs = [session_text(s) for s in item["context"]]

    # Jaccard query vs concatenated evidence
    ev_concat = " ".join(ev_docs) if ev_docs else ""
    lex = jaccard(query, ev_concat) if ev_concat else 0.0

    # TF-IDF cosine query vs evidence / distractors in a shared space
    corpus = [query] + ev_docs + dist_docs + session_docs
    vecs = tfidf_vectors(corpus)
    qv = vecs[0]
    offset = 1
    ev_cosines = []
    for i in range(len(ev_docs)):
        ev_cosines.append(cosine(qv, vecs[offset + i]))
    offset += len(ev_docs)
    dist_cosines = []
    for i in range(len(dist_docs)):
        dist_cosines.append(cosine(qv, vecs[offset + i]))
    offset += len(dist_docs)
    sess_cosines = [cosine(qv, vecs[offset + i]) for i in range(len(session_docs))]

    evidence_cosine = max(ev_cosines) if ev_cosines else 0.0
    distractor_cosine = max(dist_cosines) if dist_cosines else 0.0

    # flat RAG: rank sessions by cosine; hit if any target_evidence session in top3
    ann = item.get("annotation", {})
    target_sids = {
        int(sid)
        for sid, meta in ann.items()
        if meta.get("role_setup") == "target_evidence"
    }
    ranked = sorted(
        enumerate(sess_cosines),
        key=lambda x: -x[1],
    )
    top3_sids = {item["context"][i]["session_id"] for i, _ in ranked[:3]}
    flat_hit = bool(target_sids & top3_sids) if target_sids else False

    return {
        "lexical_jaccard_query_evidence": round(lex, 4),
        "embed_cosine_query_evidence": round(evidence_cosine, 4),  # TF-IDF proxy
        "flat_rag_hit_top3": flat_hit,
        "distractor_cosine_query": round(distractor_cosine, 4),
        "evidence_cosine_query": round(evidence_cosine, 4),
        "validity_method": {
            "embedder": "tfidf-local-proxy",
            "lexical": "jaccard-stopword-filtered",
            "computed_by": "assomem_pilot/validity_gate.py",
        },
        "_debug": {
            "ev_ids": list(ev.keys()),
            "dist_ids": list(dist.keys()),
            "top3_session_ids": sorted(top3_sids),
            "target_session_ids": sorted(target_sids),
        },
    }


def check_schema(item: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    required = [
        "sample_id", "source", "status", "association_type", "domain_tags",
        "persona", "context", "query", "query_source", "gold_answer",
        "required_elements", "annotation", "provenance",
    ]
    for k in required:
        if k not in item:
            errs.append(f"missing field: {k}")

    # context purity
    for sess in item.get("context", []):
        for bad in ("evidence_id", "atomic_fact", "role_setup", "distractor_id",
                    "why_distractor", "cue_id"):
            if bad in sess:
                errs.append(f"session {sess.get('session_id')} leaks {bad}")
        for turn in sess.get("dialogue", []):
            if set(turn.keys()) - {"role", "content", "timestamp"}:
                errs.append(f"turn has extra keys: {sorted(turn.keys())}")

    # query_source final_turn identity
    if item.get("query_source") == "final_turn":
        last_user = None
        for sess in item.get("context", []):
            for turn in sess.get("dialogue", []):
                if turn["role"] == "user":
                    last_user = turn["content"]
        if last_user is None:
            errs.append("no user turn found for final_turn check")
        elif last_user != item.get("query"):
            errs.append("query != last user turn (query_source=final_turn)")

    if not item.get("required_elements"):
        errs.append("required_elements empty")

    # evolving_state must not be in dialogue
    evo = item.get("persona", {}).get("evolving_state", {})
    blob = " ".join(session_text(s) for s in item.get("context", [])).lower()
    for v in evo.values():
        s = str(v).lower()
        if len(s) >= 8 and s in blob:
            errs.append(f"evolving_state value visible in context: {v}")

    atype = item.get("association_type", "")
    if atype.startswith("A5"):
        # absence: no target_evidence in annotation
        for meta in item.get("annotation", {}).values():
            if isinstance(meta, dict) and meta.get("role_setup") == "target_evidence":
                errs.append("A5 item must not have target_evidence sessions")
                break
        gold_l = item.get("gold_answer", "").lower()
        if not any(x in gold_l for x in ("insufficient", "not enough", "can't tell",
                                         "cannot tell", "abstain", "don't know",
                                         "do not know", "no evidence", "unclear")):
            errs.append("A5 gold_answer should abstain / cite insufficient evidence")

    if item.get("status") != "rendered":
        errs.append("status must be rendered for pilot golden set")

    # counterfactuals shape if present
    for cf in item.get("counterfactual_variants", []) or []:
        if "variant_id" not in cf or "type" not in cf:
            errs.append(f"counterfactual missing variant_id/type: {cf}")

    return errs


def check_validity(item: dict[str, Any], metrics: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    atype = item.get("association_type", "")
    arm = item.get("pilot_arm")  # associative | distractor | absence

    leaks = latent_leak(item)
    errs.extend(leaks)

    # A4 exempt from V1; A5 has no evidence
    if atype.startswith("A5"):
        return errs

    if not atype.startswith("A4"):
        if metrics["lexical_jaccard_query_evidence"] > 0.08:
            errs.append(
                f"V1 lexical jaccard too high: {metrics['lexical_jaccard_query_evidence']}"
            )
        if metrics["embed_cosine_query_evidence"] > 0.22:
            errs.append(
                f"V1 tfidf cosine too high: {metrics['embed_cosine_query_evidence']}"
            )
        if metrics["flat_rag_hit_top3"]:
            # Soft for short contexts: warn-level if arm is associative and sessions few
            # Hard fail for pilot — rewrite query or evidence wording
            errs.append("V1 flat_rag_hit_top3 == true (rewrite query/evidence)")

    if arm == "distractor" or item.get("distractor_ids"):
        if metrics["distractor_cosine_query"] < metrics["evidence_cosine_query"]:
            errs.append(
                "V2 distractor_cosine < evidence_cosine "
                f"({metrics['distractor_cosine_query']} < {metrics['evidence_cosine_query']})"
            )
        if not item.get("distractor_ids"):
            errs.append("distractor arm missing distractor_ids")

    return errs


def evaluate_item(path: Path, write_metrics: bool = False) -> dict[str, Any]:
    item = json.loads(path.read_text(encoding="utf-8"))
    schema_errs = check_schema(item)
    metrics = compute_metrics(item)
    # strip debug before writing
    debug = metrics.pop("_debug", {})
    valid_errs = check_validity(item, metrics) if not schema_errs else []
    all_errs = schema_errs + valid_errs
    ok = not all_errs

    if write_metrics:
        item["validity_metrics"] = {
            **metrics,
            "validity_method": {
                **metrics["validity_method"],
                "computed_at": __import__("datetime").date.today().isoformat(),
            },
        }
        # recompute tokens if tiktoken available
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            payload = json.dumps(item["context"], ensure_ascii=False)
            item["context_length_tokens"] = len(enc.encode(payload))
        except Exception:
            payload = json.dumps(item["context"], ensure_ascii=False)
            item["context_length_tokens"] = max(1, len(payload) // 4)
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "sample_id": item.get("sample_id", path.stem),
        "path": str(path),
        "pass": ok,
        "errors": all_errs,
        "metrics": metrics,
        "debug": debug,
        "pilot_arm": item.get("pilot_arm"),
        "association_type": item.get("association_type"),
        "domain_tags": item.get("domain_tags"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--item", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--write-metrics", action="store_true")
    ap.add_argument("--items-dir", type=Path, default=ITEMS_DIR)
    args = ap.parse_args()

    paths: list[Path]
    if args.all:
        paths = sorted(args.items_dir.glob("AMB_*.json"))
    elif args.item:
        paths = [args.item]
    else:
        ap.error("provide --item or --all")
        return 2

    results = [evaluate_item(p, write_metrics=args.write_metrics) for p in paths]
    n_pass = sum(1 for r in results if r["pass"])
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"{status}\t{r['sample_id']}\t{r.get('pilot_arm')}\t{r.get('association_type')}")
        for e in r["errors"]:
            print(f"  - {e}")
        m = r["metrics"]
        print(
            f"  metrics: lex={m['lexical_jaccard_query_evidence']:.3f} "
            f"cos_ev={m['evidence_cosine_query']:.3f} "
            f"cos_dist={m['distractor_cosine_query']:.3f} "
            f"flat_hit={m['flat_rag_hit_top3']}"
        )

    print(f"\nSUMMARY: {n_pass}/{len(results)} PASS")
    report = {
        "n": len(results),
        "n_pass": n_pass,
        "results": results,
    }
    (ROOT / "gates" / "last_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if n_pass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

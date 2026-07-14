"""
Data-quality auditor for candidate AssoMemBench items -- implements the Heptabase judge
design (2026-07-11), run ONCE per candidate item during data curation to decide
REJECT / REVISE / PASS before it enters the corpus. This is NOT the eval-time agent-answer
judge (that's eval/judge.py, which grades a pipeline's answer during a benchmark run against
gold for the results table). See docs/DATA_STANDARD.md §6 for which judge to use when.

Three LLM tasks, each on the same LLM but a fresh call (no shared conversation state):

  TASK 1 evidence_grounded_answer -- run 3x per item, CONTEXT_LEVEL in
    {query_only, last_2_sessions, full_dialogue}. The first two are shortcut probes (the model
    should fail / abstain); the third lets the model report which sessions it actually used, so
    CODE (not the LLM) can score evidence_recall / uses_distractor against the known evidence and
    distractor session sets.
  TASK 2 faithfulness -- only on the full_dialogue run's cited sessions + its "reason" field,
    checks whether the rationale's claims are actually supported.
  TASK 3 relation_type -- blind classification of each associative_links edge into the six-label
    vocabulary {co_occurs, causes, constrains, updates, analogous_to, suppresses}, compared to the
    label the item's author assigned.

    python eval/quality_audit.py --items data/build/items.jsonl --out results/quality_audit --n 50

Session-id convention this depends on: stored_context session-header lines should be formatted
`[session_id: N | ISO-timestamp]` so TASK 1's `used_session_ids` (integers) can be matched back to
real ids. Older LoCoMo/LongMemEval items don't have that header (see chunk_stored_context) --
those fall back to 1-indexed chunk position, which is a positional proxy, not a true id; treat D3
scores as lower-confidence for those sources until the loader is updated to emit the convention.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "data"))
sys.path.insert(0, HERE)

from assomem.llm import LLM  # noqa: E402
from assomem.schema import BenchItem  # noqa: E402
from discriminant_gate import chunk_stored_context, find_evidence_chunk_idxs_by_meta  # noqa: E402
import metrics as M  # noqa: E402

RELATION_LABELS = ["co_occurs", "causes", "constrains", "updates", "analogous_to", "suppresses"]

AUDITOR_SYSTEM = (
    "You are a strict auditor for an associative-memory benchmark sample.\n\n"
    "Your job is NOT to improve the sample.\n"
    "Your job is NOT to infer missing information.\n"
    "Your job is NOT to be generous.\n\n"
    "Only judge what is explicitly provided.\n\n"
    "Return STRICT JSON only."
)

TASK1_TMPL = (
    "TASK_TYPE: evidence_grounded_answer\n\n"
    "CONTEXT_LEVEL: {level}\n\n"
    "SESSIONS:\n{sessions_block}\n\n"
    "QUESTION:\n{query}\n\n"
    "Answer the question using only the sessions above. Then list which session_id(s) you "
    "actually relied on. If the sessions do not contain enough information, set "
    '"abstained": true and give your best guess anyway in "answer".\n\n'
    "Return this JSON exactly:\n"
    '{{"answer": "one to two sentences", "used_session_ids": [list of integers], '
    '"abstained": true/false, "reason": "one short sentence naming what the answer hinges on"}}'
)

TASK2_TMPL = (
    "TASK_TYPE: faithfulness\n\n"
    "CITED_SESSIONS:\n{cited_sessions}\n\n"
    "RATIONALE:\n{rationale}\n\n"
    "Check whether every claim in RATIONALE is directly stated or one-obvious-step supported by "
    "CITED_SESSIONS. Do not use outside knowledge.\n\n"
    "Return this JSON exactly:\n"
    '{{"faithful": true/false, "unsupported_claims": ["quote each unsupported claim, or empty list"], '
    '"reason": "one short sentence"}}'
)

TASK3_TMPL = (
    "TASK_TYPE: relation_type\n\n"
    "SOURCE:\n{source}\n\n"
    "TARGET:\n{target}\n\n"
    "These two facts about the same user are connected. Pick the ONE relation that best "
    "describes how SOURCE connects to TARGET:\n\n"
    "- co_occurs:     they happen together / co-vary, with no cause between them\n"
    "- causes:        SOURCE directly produces TARGET\n"
    "- constrains:    SOURCE limits the options for TARGET\n"
    "- updates:       SOURCE is a later fact that supersedes TARGET\n"
    "- analogous_to:  structurally similar across different domains\n"
    "- suppresses:    SOURCE actively rules out / inhibits TARGET\n\n"
    "Return this JSON exactly:\n"
    '{{"relation": "one of the six labels", "confidence": 0.0 to 1.0}}'
)

_SESSION_HDR = re.compile(r"^\[session_id:\s*(\d+)\s*\|\s*(.*)\]$")


def _parse_json(raw: str, fallback: Dict) -> Dict:
    try:
        return json.loads(raw)
    except Exception:
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return fallback


def _chunk_ids(chunks: List[str]) -> List[int]:
    """Real session_id if the header matches `[session_id: N | ...]`, else 1-indexed position."""
    ids = []
    for i, c in enumerate(chunks):
        first_line = c.split("\n", 1)[0].strip()
        m = _SESSION_HDR.match(first_line)
        ids.append(int(m.group(1)) if m else i + 1)
    return ids


def _sessions_block(chunks: List[str], chunk_ids: List[int], idxs: List[int]) -> str:
    if not idxs:
        return "(no sessions provided)"
    parts = []
    for i in idxs:
        parts.append(chunks[i] if _SESSION_HDR.match(chunks[i].split("\n", 1)[0].strip())
                     else f"[session_id: {chunk_ids[i]}]\n{chunks[i]}")
    return "\n\n".join(parts)


def run_evidence_grounded_answer(query: str, chunks: List[str], chunk_ids: List[int],
                                  idxs: List[int], level: str, llm: LLM) -> Dict:
    user = TASK1_TMPL.format(level=level, sessions_block=_sessions_block(chunks, chunk_ids, idxs),
                              query=query)
    raw = llm.chat([{"role": "system", "content": AUDITOR_SYSTEM}, {"role": "user", "content": user}],
                   json_mode=True)
    return _parse_json(raw, {"answer": "", "used_session_ids": [], "abstained": True,
                              "reason": "parse-fallback"})


def run_faithfulness(cited_sessions: str, rationale: str, llm: LLM) -> Dict:
    if not cited_sessions.strip() or not rationale.strip():
        return {"faithful": None, "unsupported_claims": [], "reason": "no citation/rationale to check"}
    user = TASK2_TMPL.format(cited_sessions=cited_sessions, rationale=rationale)
    raw = llm.chat([{"role": "system", "content": AUDITOR_SYSTEM}, {"role": "user", "content": user}],
                   json_mode=True)
    return _parse_json(raw, {"faithful": None, "unsupported_claims": [], "reason": "parse-fallback"})


def run_relation_type(source: str, target: str, llm: LLM) -> Dict:
    user = TASK3_TMPL.format(source=source, target=target)
    raw = llm.chat([{"role": "system", "content": AUDITOR_SYSTEM}, {"role": "user", "content": user}],
                   json_mode=True)
    return _parse_json(raw, {"relation": "", "confidence": 0.0})


def _semantic_match(pred: str, gold: str, threshold: float = 0.35) -> bool:
    return M.token_f1(pred, gold) >= threshold


def audit_item(item: BenchItem, llm: LLM, distractor_texts: Optional[List[str]] = None,
               human_answer: Optional[str] = None) -> Dict:
    notes: Dict[str, str] = {}
    failure_tags: List[str] = []

    chunks = chunk_stored_context(item.stored_context)
    chunk_ids = _chunk_ids(chunks)
    evidence_idxs = set(find_evidence_chunk_idxs_by_meta(item.meta, chunks, item.constraints or []))
    distractor_idxs = set(find_evidence_chunk_idxs_by_meta(
        item.meta, chunks, distractor_texts or [], session_ids_key="distractor_session_ids"))

    # ---------- TASK 1 x3 ----------
    all_idxs = list(range(len(chunks)))
    last2_idxs = all_idxs[-2:] if len(all_idxs) >= 2 else all_idxs
    out_query_only = run_evidence_grounded_answer(item.query, chunks, chunk_ids, [], "query_only", llm)
    out_last2 = run_evidence_grounded_answer(item.query, chunks, chunk_ids, last2_idxs,
                                              "last_2_sessions", llm)
    out_full = run_evidence_grounded_answer(item.query, chunks, chunk_ids, all_idxs, "full_dialogue", llm)

    shortcut_query = (not out_query_only.get("abstained", True)) and _semantic_match(
        out_query_only.get("answer", ""), item.gold)
    shortcut_last2 = (not out_last2.get("abstained", True)) and _semantic_match(
        out_last2.get("answer", ""), item.gold)
    d2_fail = shortcut_query or shortcut_last2
    if shortcut_query:
        failure_tags.append("query-only answerable")
    if shortcut_last2:
        failure_tags.append("recent-only answerable")

    pred_ids = set(out_full.get("used_session_ids") or [])
    id_to_idx = {cid: i for i, cid in enumerate(chunk_ids)}
    pred_idxs = {id_to_idx[cid] for cid in pred_ids if cid in id_to_idx}
    evidence_recall = (len(pred_idxs & evidence_idxs) / len(evidence_idxs)) if evidence_idxs else None
    uses_distractor = bool(pred_idxs & distractor_idxs) if distractor_idxs else None
    path_valid = (evidence_recall is not None and evidence_recall >= 0.5) and not uses_distractor

    # ---------- TASK 2 faithfulness (full_dialogue run only) ----------
    cited_text = "\n\n".join(chunks[i] for i in pred_idxs if 0 <= i < len(chunks))
    faith = run_faithfulness(cited_text, out_full.get("reason", ""), llm)

    # ---------- TASK 3 relation_type (per associative_links edge, if present) ----------
    links = (item.meta or {}).get("associative_links") or []
    relation_hits, relation_total = 0, 0
    for link in links:
        gold_rel = link.get("relation")
        src_text, tgt_text = link.get("source_text"), link.get("target_text")
        if not gold_rel or not src_text or not tgt_text:
            continue
        pred = run_relation_type(src_text, tgt_text, llm)
        relation_total += 1
        if str(pred.get("relation", "")).strip() == str(gold_rel).strip():
            relation_hits += 1
    d7_score = round(5 * relation_hits / relation_total) if relation_total else None

    # ---------- D1 discriminant (reuse discriminant_gate's cosine/lexical proxy) ----------
    d1_score = None
    if evidence_idxs and item.constraints:
        q_emb = llm.embed(item.query)
        ev_text = " ".join(item.constraints)
        cos = _cosine_safe(llm, item.query, ev_text)
        d1_score = round(20 * (1 - min(max(cos, 0.0), 1.0)))
        notes["d1"] = f"embed_cosine_query_evidence={cos:.3f}"
    else:
        notes["d1"] = "no target evidence text available -- see build_dataset.py known gaps"

    # ---------- D2 shortcut ----------
    d2_score = 0 if d2_fail else 20

    # ---------- D3 path necessity ----------
    d3_score = round(15 * evidence_recall) if evidence_recall is not None else None
    if evidence_recall is None:
        notes["d3"] = "no target evidence ids on item -- cannot score path necessity"

    # ---------- D4 distractor ----------
    if distractor_idxs:
        d4_score = 0 if uses_distractor else 10
        if uses_distractor:
            failure_tags.append("distractor fooled the model")
    else:
        d4_score = None
        notes["d4"] = "no distractor on item -- NA, not a failure"

    # ---------- D5 human answerability (needs human_answer supplied externally) ----------
    if human_answer is not None:
        d5_score = 15 if _semantic_match(human_answer, item.gold) else 0
    else:
        d5_score = None
        notes["d5"] = "PENDING_HUMAN -- pass human_answer= to score"

    # ---------- D6 leakage (pure code check, no LLM) ----------
    leak_keys = ("evidence_id", "atomic_fact", "role_setup", "distractor_id", "why_distractor")
    leaked = any(any(k in str(line) for k in leak_keys) for line in item.stored_context)
    gold_verbatim_leak = bool(item.gold) and any(item.gold.strip() and item.gold.strip() in str(line)
                                                 for line in item.stored_context)
    d6_fail = leaked or gold_verbatim_leak
    d6_score = 0 if d6_fail else 10
    if leaked:
        failure_tags.append("annotation field leaked into agent-visible context")
    if gold_verbatim_leak:
        failure_tags.append("gold answer appears verbatim in context")

    # ---------- critical_fail / decision ----------
    no_evidence = not evidence_idxs
    # associative_cue_id is a new-schema-only field (see DATA_STANDARD.md); A2/A3 items are the
    # only constructs that structurally require an explicit cue, and legacy LoCoMo/LongMemEval
    # items predate this field entirely -- don't reject items that were never supposed to have it.
    cue_required = item.association_type in ("A2_cue_chain", "A3_cross_domain")
    no_cue = cue_required and not (item.meta or {}).get("associative_cue_id")
    faithful_fail = faith.get("faithful") is False

    critical = d2_fail or d6_fail or no_evidence or faithful_fail or no_cue
    if no_evidence:
        failure_tags.append("no identifiable target evidence")
    if no_cue:
        failure_tags.append("no associative cue on item (meta.associative_cue_id missing)")
    if faithful_fail:
        failure_tags.append("rationale not faithful to cited evidence")

    scores = {"D1_discriminant": (d1_score, 20), "D2_shortcut": (d2_score, 20),
              "D3_path_necessity": (d3_score, 15), "D4_distractor": (d4_score, 10),
              "D5_human_answerability": (d5_score, 15), "D6_leakage": (d6_score, 10),
              "D7_typed_link": (d7_score, 5)}
    earned = sum(s for s, _ in scores.values() if s is not None)
    applicable = sum(m for s, m in scores.values() if s is not None)
    normalized_total = earned / applicable if applicable else 0.0

    if critical:
        decision = "REJECT"
    elif normalized_total >= 0.8 and (d4_score is None or d4_score == 10):
        decision = "PASS"
    else:
        decision = "REVISE"

    dimensions = {
        "D1_discriminant": {"score": d1_score, "max": 20, "critical": False, "notes": notes.get("d1", "")},
        "D2_shortcut": {"score": d2_score, "max": 20, "critical": d2_fail, "notes": "; ".join(
            t for t in failure_tags if "answerable" in t)},
        "D3_path_necessity": {"score": d3_score, "max": 15, "critical": False, "notes": notes.get("d3", "")},
        "D4_distractor": {"score": d4_score, "max": 10, "critical": False, "notes": notes.get("d4", "")},
        "D5_human_answerability": {"score": d5_score, "max": 15, "critical": False, "notes": notes.get("d5", "")},
        "D6_leakage": {"score": d6_score, "max": 10, "critical": d6_fail, "notes": "; ".join(
            t for t in failure_tags if "leak" in t)},
        "D7_typed_link": {"score": d7_score, "max": 5, "critical": False,
                          "notes": f"{relation_hits}/{relation_total} agreed" if relation_total else "no typed edges"},
        "D8_temporal": {"score": None, "max": None, "status": "NA", "notes": "not implemented -- see Heptabase spec"},
    }

    return {
        "sample_id": item.item_id,
        "critical_fail": critical,
        "normalized_total": round(normalized_total, 3),
        "earned_points": earned,
        "applicable_points": applicable,
        "dimensions": dimensions,
        "failure_tags": failure_tags,
        "repair_suggestions": [],
        "overall_decision": decision,
        "_raw": {"task1_query_only": out_query_only, "task1_last_2_sessions": out_last2,
                 "task1_full_dialogue": out_full, "task2_faithfulness": faith},
    }


def _cosine_safe(llm: LLM, a: str, b: str) -> float:
    from assomem.llm import cosine
    return cosine(llm.embed(a), llm.embed(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default=os.path.join(HERE, "..", "data", "build", "items.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results", "quality_audit"))
    ap.add_argument("--backend", default="mock", choices=["mock", "openai"])
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()

    items = []
    with open(args.items) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(BenchItem.from_dict(json.loads(line)))

    llm = LLM(backend=args.backend)
    results = []
    for item in items[:args.n]:
        results.append(audit_item(item, llm))
        print(f"  {item.item_id}: {results[-1]['overall_decision']} "
              f"(total={results[-1]['normalized_total']}, critical={results[-1]['critical_fail']})")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out + ".jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    n_pass = sum(1 for r in results if r["overall_decision"] == "PASS")
    n_revise = sum(1 for r in results if r["overall_decision"] == "REVISE")
    n_reject = sum(1 for r in results if r["overall_decision"] == "REJECT")
    print(f"\n{len(results)} audited -> PASS {n_pass} / REVISE {n_revise} / REJECT {n_reject}")
    print(f"wrote {args.out}.jsonl")


if __name__ == "__main__":
    main()

"""
Transform the RAW base datasets into ONE unified set of BenchItems.

    python data/build_dataset.py --out data/build/items.jsonl

Source → scenario mapping (see data/README.md):

  PersonaMem   -> scenario=associative   (MC inference; keep suggest_new/recommend/generalize)
  LoCoMo       -> scenario=long_horizon  (multi-hop / open-ended categories only;
                                          evidence_ids = dialogue turn IDs for RS metric)
  LongMemEval  -> scenario=long_horizon  (multi-session, knowledge-update)
               -> scenario=associative   (single-session-preference)
               -> is_answerable=False    (abstention items, question_id ends with _abs)
  PerLTQA      -> scenario=associative   (profile+events; evidence = memory anchor)
  MemoryArena  -> scenario=memory_to_action

LoCoMo filtration (category codes from the paper):
  KEEP: category=3 (multi-hop inference requiring ≥2 facts) and category=4 (open-ended)
  EXCLUDE: category=1 (single-hop factoid), category=2 (temporal when/date), category=5 (adversarial)

LongMemEval filtration:
  KEEP: multi-session, knowledge-update, single-session-preference
  EXCLUDE: single-session-user, single-session-assistant (factoid retrieval)
  EXCLUDE: temporal-reasoning (mostly date/order factoids, not preference inference)
  is_answerable=False for question_id ending in _abs (abstention control)

This script is defensive: each loader is wrapped so a missing dataset is skipped with a
warning rather than crashing the build.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# question types we keep from PersonaMem because they require INFERENCE, not recall
INFER_TYPES = {"suggest new ideas", "provide preference-aligned recommendations",
               "generalize to new scenarios", "suggest_new", "recommend", "generalize"}


def _load_jsonl(path: str) -> List[Dict]:
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_personamem() -> List[Dict]:
    items = []
    base = os.path.join(RAW, "personamem")
    rows = []
    if os.path.isdir(base):
        for fn in os.listdir(base):
            rows += _load_jsonl(os.path.join(base, fn))
    for i, r in enumerate(rows):
        qtype = str(r.get("question_type", "")).lower()
        if INFER_TYPES and qtype and qtype not in INFER_TYPES:
            continue
        ctx = r.get("shared_context") or r.get("context") or []
        if isinstance(ctx, str):
            ctx = [ctx]
        opts = r.get("all_options") or r.get("options") or []
        items.append(dict(
            item_id=f"personamem-{i}", source="personamem", scenario="associative",
            stored_context=[str(c) for c in ctx][:200],
            query=r.get("user_question_or_message") or r.get("question") or "",
            gold=r.get("correct_answer") or r.get("answer") or "",
            options=[str(o) for o in opts],
            question_type=qtype or "suggest_new",
            meta={"topic": r.get("topic"), "distance": r.get("distance_to_ref_in_tokens")},
        ))
    return items


def _locomo_association_type(cat: int, ev_sessions: set) -> str:
    """Map LoCoMo QA category + evidence span to A1–A4 label.

    A1 Relational Binding    : cat=3, evidence ≥2 nodes within one session
                               (multi-hop binding within working memory)
    A2 Cue-Triggered Chain   : cat=3, evidence spans ≥2 sessions (true cross-session chain)
                               OR cat=4 open-ended (cue in query → bridge in memory → answer)
    A3 Cross-Domain Bridging : not auto-detectable from structure alone; left for manual smoke-test
    A4 Temporal Consistency  : not present in LoCoMo (no preference-update pattern)
    """
    if cat == 3:
        return "A2_cue_chain" if len(ev_sessions) > 1 else "A1_relational_binding"
    return "A2_cue_chain"   # cat=4: open-ended preference inference


def _locomo_a5_probes(ev_ids: list, ev_sessions: set) -> List[str]:
    """Auto-fill A5 Counterfactual Sensitivity probe types.

    no_memory      : always applicable (remove stored_context → agent must fail)
    remove_bridge  : applicable when evidence_nodes ≥ 2 (removing one node should break answer)
    stale_memory   : not auto-detectable in LoCoMo (no explicit update pattern)
    distractor_swap: not auto-detectable (requires similar-entity injection)
    """
    probes = ["no_memory"]
    if len(ev_ids) >= 2:
        probes.append("remove_bridge")
    return probes


def build_locomo() -> List[Dict]:
    """Build long_horizon items from LoCoMo with refined A1–A5, F9 labels.

    LoCoMo QA category codes (arXiv:2402.17753):
      1 = single-hop factoid                             → EXCLUDE
      2 = temporal (when/where/date)                     → EXCLUDE
      3 = multi-hop inference (≥2 evidence turns)        → KEEP
      4 = open-ended (preference/personality inference)  → KEEP
      5 = adversarial unanswerable                       → EXCLUDE

    Filtration criteria applied here:
      F9 Persistent-Memory Requirement: all LoCoMo items are F9=True because the QA is
        retrospective (asked after all sessions are complete). Evidence is always from a
        past session, never the active context. However, we distinguish:
          f9_strength = "strong" : evidence spans ≥2 distinct sessions (true cross-session)
          f9_strength = "weak"   : evidence within one session (working-memory boundary)
        Both are kept; f9_strength is a metadata field for downstream analysis.

      A1 Relational Binding: evidence_nodes ≥ 2 required for multi-hop items (cat=3).
        Single-evidence cat=3 items are kept but flagged a1_nodes=1.

    association_type uses the A1–A4 taxonomy from the annotation scheme:
      A1 / A2 auto-assigned; A3 / A4 require manual smoke-test annotation.
    """
    items = []
    path = os.path.join(RAW, "locomo", "data", "locomo10.json")
    if not os.path.exists(path):
        return items
    data = json.load(open(path))

    for ci, conv in enumerate(data):
        c = conv.get("conversation", {})
        sid = conv.get("sample_id", f"conv{ci}")

        # Build turn-id → text map and ordered session list with timestamps
        turn_map: Dict[str, str] = {}
        sessions_text: List[str] = []
        for snum in sorted(
            int(k.split("_")[1]) for k in c
            if k.startswith("session_") and not k.endswith("date_time")
        ):
            skey = f"session_{snum}"
            date = c.get(f"session_{snum}_date_time", "")
            if date:
                sessions_text.append(f"[{date}]")
            for turn in c.get(skey, []):
                dia_id = turn.get("dia_id", "")
                text = f"{turn.get('speaker','')}: {turn.get('text','')}"
                sessions_text.append(text)
                if dia_id:
                    turn_map[dia_id] = text

        for qi, qa in enumerate(conv.get("qa", [])):
            cat = qa.get("category")
            if cat not in (3, 4):
                continue

            ev_ids = [str(e) for e in (qa.get("evidence") or []) if str(e)]
            # evidence sessions: Dx prefix from turn IDs like "D3:5"
            ev_sessions = set(e.split(":")[0] for e in ev_ids if ":" in e)

            # F9: cross-session = strong, same-session = weak (both kept)
            f9_strength = "strong" if len(ev_sessions) > 1 else (
                "weak" if ev_sessions else "absent")

            # A1 Relational Binding: evidence graph connectivity
            a1_nodes = len(ev_ids)          # proxy; full graph check requires manual audit

            # association_type (A1–A4 auto-label)
            association_type = _locomo_association_type(cat, ev_sessions)

            # A5 counterfactual probes (structurally auto-detectable)
            a5_probes = _locomo_a5_probes(ev_ids, ev_sessions)

            # constraints = evidence turn texts (RS per-step satisfaction)
            constraints = [turn_map[e] for e in ev_ids if e in turn_map][:6]

            items.append(dict(
                item_id=f"locomo-{sid}-{qi}",
                source="locomo",
                scenario="long_horizon",
                stored_context=sessions_text,   # full context; no truncation (evidence may be in late sessions)
                query=qa.get("question", ""),
                gold=str(qa.get("answer", "")),
                options=[],
                evidence_ids=ev_ids,
                constraints=constraints,
                question_type="multi_hop_inference" if cat == 3 else "open_ended_preference",
                is_answerable=True,
                association_type=association_type,           # top-level A1/A2/A3/A4 label
                counterfactual_probes=a5_probes,             # top-level A5 probe list
                meta={
                    # annotation labels (duplicated for easy meta access)
                    "association_type": association_type,
                    "a1_nodes": a1_nodes,
                    "a5_probes": a5_probes,
                    "f9_persistent_memory": True,
                    "f9_strength": f9_strength,             # strong=cross-session, weak=same-session
                    "temporal_state_operator": None,        # N/A for LoCoMo
                    # raw fields
                    "locomo_category": cat,
                    "ev_sessions": sorted(ev_sessions),
                    "num_evidence": len(ev_ids),
                    "sample_id": sid,
                },
            ))
    return items


def build_perltqa() -> List[Dict]:
    items, base = [], os.path.join(RAW, "PerLTQA")
    if not os.path.isdir(base):
        return items
    # PerLTQA ships JSON under data/; we scan for QA-like files defensively.
    for root, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith(".json"):
                continue
            try:
                data = json.load(open(os.path.join(root, fn)))
            except Exception:
                continue
            rows = data if isinstance(data, list) else data.get("data", [])
            if not isinstance(rows, list):
                continue
            for i, r in enumerate(rows):
                if not isinstance(r, dict) or "question" not in r:
                    continue
                items.append(dict(
                    item_id=f"perltqa-{fn}-{i}", source="perltqa", scenario="associative",
                    stored_context=[str(r.get("reference memory") or r.get("reference") or "")],
                    query=r.get("question", ""), gold=str(r.get("answer", "")), options=[],
                    evidence_ids=[str(r.get("memory anchor", ""))],
                    question_type="associative_recall",
                    is_answerable=True,
                ))
            if items:
                break
    return items


def _lme_association_type(qtype: str, is_abstention: bool) -> str:
    """Map LongMemEval question type to A1–A4 label.

    A1 Relational Binding    : multi-session (connect facts across ≥2 past sessions)
    A2 Cue-Triggered Chain   : single-session-preference (cue in query → bridge → answer)
    A3 Cross-Domain Bridging : not auto-detectable; left for manual smoke-test annotation
    A4 Temporal Consistency  : knowledge-update (old belief → new belief; must track update)
    """
    if is_abstention:
        return "A5_absence_control"
    return {
        "multi-session":           "A1_relational_binding",
        "knowledge-update":        "A4_temporal_consistency",
        "single-session-preference": "A2_cue_chain",
    }.get(qtype, "A1_relational_binding")


def _lme_temporal_op(qtype: str, ev_ids: list) -> Optional[str]:
    """Infer A4 temporal state operator for knowledge-update items.

    knowledge-update always follows: sess1=old_belief, sess2=new_belief → operator=update.
    If the answer supersedes a prior value, that's an "update". "conflict" would require
    contradictory simultaneous beliefs; "stale_fact" is for outdated but not updated.
    For the oracle split, LongMemEval knowledge-update items always have exactly 2 evidence
    sessions — classic update pattern.
    """
    if qtype == "knowledge-update":
        return "update"
    return None


def _lme_a5_probes(qtype: str, is_abstention: bool, ev_ids: list) -> List[str]:
    """Auto-fill A5 Counterfactual Sensitivity probe types for LongMemEval items.

    no_memory      : always applicable (remove stored_context → must fail)
    remove_bridge  : multi-session with ≥2 evidence sessions (removing one breaks the chain)
    stale_memory   : knowledge-update (keep only sess1/old belief → should give wrong answer)
    distractor_swap: multi-session (haystack has noisy sessions that could distract)
    """
    if is_abstention:
        return ["no_memory"]
    probes = ["no_memory"]
    if qtype == "knowledge-update":
        probes.append("stale_memory")   # key A5 probe: old belief should give wrong answer
    if qtype == "multi-session" and len(ev_ids) >= 2:
        probes.append("remove_bridge")
        probes.append("distractor_swap")
    return probes


def build_longmemeval() -> List[Dict]:
    """Build benchmark items from LongMemEval oracle split with refined A1–A5, F9 labels.

    LongMemEval question types (arXiv:2410.10813, ICLR 2025):
      multi-session            → A1 Relational Binding  (cross-session fact linking)     KEEP
      knowledge-update         → A4 Temporal Consistency (old→new belief update)         KEEP
      single-session-preference→ A2 Cue Chain           BUT F9=False → working_mem ctrl  KEEP*
      single-session-user      → factoid recall                                          EXCLUDE
      single-session-assistant → factoid recall                                          EXCLUDE
      temporal-reasoning       → date/order factoids                                     EXCLUDE
      abstention (_abs)        → A5 absence control; is_answerable=False                 KEEP

    (* single-session-preference items have evidence and query in the SAME session context.
       F9 Persistent-Memory Requirement is NOT met: there is no session boundary between
       evidence and query. These items are re-labeled scenario="working_memory_control"
       and kept as a separate working-memory baseline group, not counted in the main
       persistent-memory evaluation. This distinction is documented in the paper appendix.)

    Filtration exclusion criteria applied here:
      F9 (Persistent-Memory): single-session-* excluded from main set (F9=False)
      A4 (Temporal Consistency): knowledge-update items auto-labeled with operator=update
      A5 (Counterfactual): stale_memory probe for knowledge-update; remove_bridge for multi-session
    """
    items = []
    path = os.path.join(RAW, "longmemeval", "data", "longmemeval_oracle.json")
    if not os.path.exists(path):
        return items

    data = json.load(open(path))

    # All types we process (single-session-preference → working_memory_control)
    KEEP_TYPES = {"multi-session", "knowledge-update", "single-session-preference"}

    for item in data:
        qtype = item.get("question_type", "")
        qid = str(item.get("question_id", ""))
        is_abstention = qid.endswith("_abs")

        if qtype not in KEEP_TYPES and not is_abstention:
            continue

        # F9: single-session-preference has evidence in the SAME session as the query context
        # → not a persistent-memory task; relabel scenario so it's separated from main eval
        f9_persistent = qtype not in ("single-session-preference",) or is_abstention

        # Flatten haystack sessions into ordered context (oracle = evidence sessions only)
        ctx: List[str] = []
        dates = item.get("haystack_dates", [])
        for si, sess in enumerate(item.get("haystack_sessions", [])):
            if si < len(dates):
                ctx.append(f"[Session {si+1} — {dates[si]}]")
            for turn in sess:
                ctx.append(f"{turn.get('role','')}: {turn.get('content','')}")

        # Scenario: working_memory_control for F9-failing items; long_horizon otherwise
        if not f9_persistent and not is_abstention:
            scenario = "working_memory_control"
        elif qtype in ("multi-session", "knowledge-update"):
            scenario = "long_horizon"
        else:
            scenario = "associative"

        ev_ids = item.get("answer_session_ids", [])

        # Build constraints for RS per-step scoring
        constraints: List[str] = []
        if qtype == "knowledge-update" and len(ev_ids) > 1:
            sess_ids = item.get("haystack_session_ids", [])
            for sess_id in ev_ids:
                idx = sess_ids.index(sess_id) if sess_id in sess_ids else -1
                if 0 <= idx < len(item.get("haystack_sessions", [])):
                    first_turn = item["haystack_sessions"][idx][0] if item["haystack_sessions"][idx] else {}
                    constraints.append(first_turn.get("content", "")[:120])
        elif qtype == "multi-session":
            constraints = [f"evidence_session_{s}" for s in ev_ids][:6]

        # Only keep abstention items whose base question_type is in KEEP_TYPES.
        # Abstentions from temporal-reasoning / single-session-user have no corresponding
        # main-eval items, so they don't contribute to calibration measurement.
        if is_abstention and qtype not in KEEP_TYPES:
            continue

        # Refined annotation labels
        association_type = _lme_association_type(qtype, is_abstention)
        temporal_op = _lme_temporal_op(qtype, ev_ids)
        a5_probes = _lme_a5_probes(qtype, is_abstention, ev_ids)

        items.append(dict(
            item_id=f"longmemeval-{qid}",
            source="longmemeval",
            scenario=scenario,
            stored_context=ctx,   # full oracle context (max ~65 lines, no truncation needed)
            query=item.get("question", ""),
            gold=str(item.get("answer", "")),
            options=[],
            evidence_ids=ev_ids,
            constraints=constraints[:6],
            question_type=qtype.replace("-", "_"),
            is_answerable=not is_abstention,
            association_type=association_type,           # top-level A1/A2/A4/A5 label
            counterfactual_probes=a5_probes,             # top-level A5 probe list
            meta={
                # annotation labels
                "association_type": association_type,
                "a1_nodes": len(ev_ids),
                "a5_probes": a5_probes,
                "f9_persistent_memory": f9_persistent,
                "temporal_state_operator": temporal_op,
                # raw fields
                "question_date": item.get("question_date", ""),
                "num_sessions": len(item.get("haystack_sessions", [])),
                "is_abstention": is_abstention,
            },
        ))
    return items


def build_memoryarena() -> List[Dict]:
    items, base = [], os.path.join(RAW, "memoryarena")
    if not os.path.isdir(base):
        return items
    for fn in os.listdir(base):
        for i, r in enumerate(_load_jsonl(os.path.join(base, fn))):
            qs = r.get("questions") or []
            ans = r.get("answers") or []
            bg = r.get("backgrounds")
            ctx = ([bg] if isinstance(bg, str) else list(bg or [])) + [str(q) for q in qs[:-1]]
            items.append(dict(
                item_id=f"memarena-{fn}-{i}", source="memoryarena", scenario="memory_to_action",
                stored_context=[str(c) for c in ctx][:200],
                query=str(qs[-1]) if qs else "", gold=str(ans[-1]) if ans else "",
                options=[], action_gold=str(ans[-1]) if ans else None,
                constraints=[str(a) for a in ans[:-1]][:6],
                question_type="memory_to_action",
                is_answerable=True,
            ))
    return items


def build_partner_generated(base_dirs: List[str]) -> List[Dict]:
    """Build BenchItems from the new partner-generated schema (docs/DATA_STANDARD.md §2).

    Flattens the structured `context` (list of {session_id, timestamp, dialogue}) into
    stored_context text lines using the `[session_id: N | ISO-timestamp]` header convention
    that eval/quality_audit.py's TASK 1 depends on for session-id matching. `annotation`,
    `persona.evolving_state`, and every other scoring-only field are dropped from
    stored_context -- only role/content ever reaches what the agent sees.

    `constraints` = evidence text (atomic_fact per target_evidence_id, resolved via
    `annotation`) followed by `required_elements` -- this keeps discriminant_gate.py's
    evidence-chunk matching working (it expects constraints to be evidence text, the
    convention from build_locomo/build_longmemeval) while still giving eval/judge.py the
    full rubric to score against, since extra non-matching rubric strings are harmless for
    chunk matching but not for judging.

    `status` must be "rendered" -- draft_template items don't count toward the corpus yet
    (DATA_STANDARD.md §2, the context_length_tokens/status rule).
    """
    items = []
    for base_dir in base_dirs:
        if not os.path.isdir(base_dir):
            continue
        for fn in sorted(os.listdir(base_dir)):
            if not (fn.startswith("AMB_") and fn.endswith(".json")):
                continue
            d = json.load(open(os.path.join(base_dir, fn)))
            if d.get("status") != "rendered":
                continue

            stored_context: List[str] = []
            annotation = d.get("annotation") or {}
            ev_text_by_id: Dict[str, str] = {}
            ev_session_by_id: Dict[str, int] = {}
            distractor_session_ids: List[int] = []
            for sess in d.get("context", []):
                sid = sess.get("session_id")
                stored_context.append(f"[session_id: {sid} | {sess.get('timestamp', '')}]")
                for turn in sess.get("dialogue", []):
                    stored_context.append(f"{turn.get('role', '')}: {turn.get('content', '')}")
                note = annotation.get(str(sid), {})
                if note.get("evidence_id"):
                    ev_text_by_id[note["evidence_id"]] = note.get("atomic_fact", "")
                    ev_session_by_id[note["evidence_id"]] = sid
                if note.get("distractor_id"):
                    distractor_session_ids.append(sid)

            evidence_ids = d.get("target_evidence_ids", [])
            constraints = [ev_text_by_id[eid] for eid in evidence_ids if eid in ev_text_by_id]
            constraints += list(d.get("required_elements", []))

            items.append(dict(
                item_id=d["sample_id"], source="partner_generated", scenario="associative",
                stored_context=stored_context, query=d.get("query", ""),
                gold=d.get("gold_answer", ""), options=[], evidence_ids=evidence_ids,
                constraints=constraints, question_type="associative_inference",
                is_answerable=True, association_type=d.get("association_type", ""),
                counterfactual_probes=[cv.get("type") for cv in d.get("counterfactual_variants", [])],
                distractor_ids=d.get("distractor_ids") or [],
                meta={
                    "secondary_association_type": d.get("secondary_association_type"),
                    "domain_tags": d.get("domain_tags", []),
                    "pilot_arm": d.get("pilot_arm"), "pilot_domain": d.get("pilot_domain"),
                    "associative_cue_id": d.get("associative_cue_id"),
                    "associative_links": d.get("associative_links", []),
                    "counterfactual_variants": d.get("counterfactual_variants", []),
                    "validity_metrics": d.get("validity_metrics", {}),
                    "latent_forbidden_phrases": d.get("latent_forbidden_phrases", []),
                    "distractor_session_ids": distractor_session_ids,
                    "evidence_session_ids": ev_session_by_id,
                    "required_elements": d.get("required_elements", []),
                    "provenance": d.get("provenance", {}),
                    "dataset_meta": d.get("dataset_meta", {}),
                },
            ))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "build", "items.jsonl"))
    ap.add_argument("--partner-dir", action="append", default=[
        os.path.join(os.path.dirname(__file__), "raw", "partner_generated"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)),
                      "pilot_data_S1_work-learn_S2_hobby"),
    ], help="directory to scan for AMB_*.json partner-generated items; repeatable")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    all_items: List[Dict] = []
    for name, fn in [("PersonaMem", build_personamem), ("LoCoMo", build_locomo),
                     ("LongMemEval", build_longmemeval),
                     ("PerLTQA", build_perltqa), ("MemoryArena", build_memoryarena),
                     ("PartnerGenerated", lambda: build_partner_generated(args.partner_dir))]:
        try:
            got = fn()
            print(f"[{name}] built {len(got)} items")
            all_items += got
        except Exception as e:
            print(f"[{name}] skipped: {e}")

    if not all_items:
        print("\nNo raw data found. Run `python data/download.py --all` first, "
              "or use the bundled sample at data/sample/sample_items.jsonl.")
        return
    with open(args.out, "w") as f:
        for it in all_items:
            f.write(json.dumps(it) + "\n")
    print(f"\nWrote {len(all_items)} unified items -> {args.out}")


if __name__ == "__main__":
    main()

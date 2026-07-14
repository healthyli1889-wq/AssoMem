"""
Discriminant-validity gate for AssoMemBench items.

For each item, checks whether the query could be answered via a *surface-level
shortcut* rather than true associative retrieval:

  lexical_jaccard   : word-set Jaccard(query, evidence_text), stopword-filtered.
                       High overlap -> a keyword/BM25-style retriever would leak the answer.
  embed_cosine      : cosine(embed(query), embed(evidence_text)).
                       High similarity -> a dense retriever would leak the answer.
                       (backend=mock uses the repo's hashed bag-of-words embedding, which is
                       a LEXICAL-family proxy, not true semantic similarity -- see --backend.)
  flat_rag_rank     : rank of the evidence-bearing session/chunk when all chunks of the
                       item's own stored_context are ranked by cosine-to-query.
                       flat_rag_hit@k = the evidence chunk is retrieved in the top k.
                       This directly simulates the "Flat RAG must fail" baseline from
                       Related Work using the same retrieve.py-style embed+cosine scoring.

gate_pass = evidence text was extractable AND flat_rag_hit@3 is False.
flat_rag_hit@3 is the primary binary criterion (no arbitrary cosine cutoff needed); lexical
and cosine numbers are reported for sensitivity / diagnosis, not as a hard gate.

Coverage caveat: an item only has extractable evidence text if `constraints` holds real
text. LoCoMo and LongMemEval knowledge-update items do; LongMemEval multi-session items
currently store placeholder ids (`evidence_session_<id>`), not text -- see build_dataset.py
build_longmemeval(). Those items are reported separately as evidence_unavailable, not
silently counted as pass or fail.

    python data/discriminant_gate.py --items data/build/items.jsonl --out results/discriminant_gate
    python data/discriminant_gate.py --backend openai   # real embeddings, needs OPENAI_API_KEY
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from assomem.llm import LLM, cosine  # noqa: E402

HEADER_RE = re.compile(r"^\[.*\]$")
WORD_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = set("""
a an the this that these those i you he she it we they me him her us them my your his its
our their is am are was were be been being do does did have has had having will would
shall should can could may might must and or but if then than so because as at by for
in into on onto of off to from with without within about over under again further here
there when where why how all any both each few more most other some such no nor not only
own same too very s t just don now
""".split())


def tokenize(text: str) -> set:
    return {w for w in WORD_RE.findall(str(text).lower()) if w not in STOPWORDS and len(w) > 2}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    return inter / len(a | b)


def usable_evidence_text(constraints: Optional[List[str]]) -> List[str]:
    """Filter out placeholder constraints like 'evidence_session_<id>' (no real text)."""
    if not constraints:
        return []
    return [c for c in constraints if c and not str(c).startswith("evidence_session_")]


def chunk_stored_context(lines: List[str]) -> List[str]:
    """Split stored_context into session-level chunks using '[...]' header lines.

    Falls back to one-chunk-per-list-entry when no header lines are present
    (e.g. MemoryArena / flat-list sources).
    """
    if not lines:
        return []
    if any(HEADER_RE.match(str(l).strip()) for l in lines):
        chunks: List[str] = []
        cur: List[str] = []
        for l in lines:
            if HEADER_RE.match(str(l).strip()):
                if cur:
                    chunks.append("\n".join(cur))
                cur = [str(l)]
            else:
                cur.append(str(l))
        if cur:
            chunks.append("\n".join(cur))
        return chunks
    return [str(l) for l in lines]


def find_evidence_chunk_idxs(chunks: List[str], evidence_parts: List[str]) -> List[int]:
    idxs = []
    for i, c in enumerate(chunks):
        for part in evidence_parts:
            probe = str(part)[:80].strip()
            if probe and probe in c:
                idxs.append(i)
                break
    return idxs


_SESSION_HDR = re.compile(r"^\[session_id:\s*(\d+)\s*\|")


def chunk_session_ids(chunks: List[str]) -> List[Optional[int]]:
    """Real session_id parsed from a `[session_id: N | ...]` header line, else None.

    Partner-generated items (see build_partner_generated in build_dataset.py) render this
    header, which lets evidence be located by the known evidence_id->session_id mapping in
    meta.evidence_session_ids instead of substring search -- substring search fails for that
    source because `atomic_fact` is a paraphrase of the evidence turn, not verbatim dialogue
    text, so it never appears as a literal substring of stored_context.
    """
    ids: List[Optional[int]] = []
    for c in chunks:
        m = _SESSION_HDR.match(c.split("\n", 1)[0].strip())
        ids.append(int(m.group(1)) if m else None)
    return ids


def find_evidence_chunk_idxs_by_meta(meta: Optional[Dict], chunks: List[str],
                                     evidence_parts: List[str],
                                     session_ids_key: str = "evidence_session_ids") -> List[int]:
    """find_evidence_chunk_idxs, but prefers meta[session_ids_key] when present.

    meta[session_ids_key] can be a dict of {id: session_id} (evidence_session_ids) or a plain
    list of session ids (distractor_session_ids) -- both come out of build_partner_generated().
    Works for both raw dicts (discriminant_gate) and BenchItem.meta (quality_audit) -- pass
    item.get("meta") or item.meta respectively.
    """
    known = (meta or {}).get(session_ids_key)
    if known:
        wanted = set(known.values()) if isinstance(known, dict) else set(known)
        chunk_ids = chunk_session_ids(chunks)
        return [i for i, sid in enumerate(chunk_ids) if sid in wanted]
    return find_evidence_chunk_idxs(chunks, evidence_parts)


def score_item(item: Dict, llm: LLM, top_k: int) -> Dict:
    row = dict(
        item_id=item["item_id"], source=item["source"], scenario=item.get("scenario", ""),
        association_type=item.get("association_type") or (item.get("meta") or {}).get("association_type", ""),
        f9_strength=(item.get("meta") or {}).get("f9_strength", ""),
        evidence_unavailable=True, lex_jaccard=None, embed_cosine=None,
        num_chunks=0, best_rank=None, flat_rag_hit_top1=None, flat_rag_hit_top3=None,
        gate_pass=None,
    )
    evidence_parts = usable_evidence_text(item.get("constraints"))
    query = item.get("query") or ""
    if not evidence_parts or not query.strip():
        return row

    evidence_text = " ".join(str(p) for p in evidence_parts)
    row["evidence_unavailable"] = False

    row["lex_jaccard"] = round(jaccard(tokenize(query), tokenize(evidence_text)), 4)

    q_emb = llm.embed(query)
    e_emb = llm.embed(evidence_text)
    row["embed_cosine"] = round(cosine(q_emb, e_emb), 4)

    chunks = chunk_stored_context(item.get("stored_context") or [])
    row["num_chunks"] = len(chunks)
    if not chunks:
        return row

    chunk_embs = [llm.embed(c) for c in chunks]
    scored = sorted(range(len(chunks)), key=lambda i: cosine(q_emb, chunk_embs[i]), reverse=True)
    rank_of = {idx: pos + 1 for pos, idx in enumerate(scored)}  # 1-indexed

    ev_idxs = find_evidence_chunk_idxs_by_meta(item.get("meta"), chunks, evidence_parts)
    if not ev_idxs:
        return row  # evidence text didn't match any chunk verbatim; leave rank fields None

    best_rank = min(rank_of[i] for i in ev_idxs)
    row["best_rank"] = best_rank
    row["flat_rag_hit_top1"] = best_rank <= 1
    row["flat_rag_hit_top3"] = best_rank <= top_k
    row["gate_pass"] = not row["flat_rag_hit_top3"]
    return row


def summarize(rows: List[Dict]) -> str:
    lines = []
    total = len(rows)
    unavailable = sum(1 for r in rows if r["evidence_unavailable"])
    scored = [r for r in rows if not r["evidence_unavailable"] and r["best_rank"] is not None]
    passed = [r for r in scored if r["gate_pass"]]

    lines.append(f"# Discriminant-validity gate results\n")
    lines.append(f"Total items: {total}")
    lines.append(f"Evidence unavailable (excluded): {unavailable} ({unavailable/total:.1%})")
    lines.append(f"Evidence available but chunk match failed (excluded): "
                 f"{total - unavailable - len(scored)}")
    lines.append(f"Scored items: {len(scored)}")
    if scored:
        lines.append(f"gate_pass (flat_rag_hit@3 == False): {len(passed)} / {len(scored)} "
                      f"({len(passed)/len(scored):.1%})\n")

    def _breakdown(key: str, title: str):
        lines.append(f"## By {title}\n")
        lines.append("| value | n scored | n unavailable | pass rate | median lex_jaccard | median cosine |")
        lines.append("|---|---|---|---|---|---|")
        groups = defaultdict(list)
        unavail_groups = Counter()
        for r in rows:
            k = r[key] or "(none)"
            if r["evidence_unavailable"] or r["best_rank"] is None:
                unavail_groups[k] += 1
            else:
                groups[k].append(r)
        for k in sorted(set(list(groups.keys()) + list(unavail_groups.keys()))):
            g = groups.get(k, [])
            n = len(g)
            u = unavail_groups.get(k, 0)
            if n:
                pr = sum(1 for r in g if r["gate_pass"]) / n
                lex = sorted(r["lex_jaccard"] for r in g)[n // 2]
                cos = sorted(r["embed_cosine"] for r in g)[n // 2]
                lines.append(f"| {k} | {n} | {u} | {pr:.1%} | {lex:.3f} | {cos:.3f} |")
            else:
                lines.append(f"| {k} | 0 | {u} | n/a | n/a | n/a |")
        lines.append("")

    _breakdown("source", "source")
    _breakdown("association_type", "association_type")
    _breakdown("f9_strength", "f9_strength (LoCoMo only)")

    if scored:
        lines.append("## Threshold sensitivity (embed_cosine, mock=lexical-proxy)\n")
        lines.append("| cosine < threshold | pass rate |")
        lines.append("|---|---|")
        for t in (0.2, 0.3, 0.4, 0.5, 0.6):
            pr = sum(1 for r in scored if r["embed_cosine"] < t) / len(scored)
            lines.append(f"| {t} | {pr:.1%} |")
        lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", default=os.path.join(HERE, "build", "items.jsonl"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results", "discriminant_gate"))
    ap.add_argument("--backend", default="mock", choices=["mock", "openai"])
    ap.add_argument("--top-k", type=int, default=3)
    args = ap.parse_args()

    items = []
    with open(args.items) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))

    llm = LLM(backend=args.backend)
    rows = []
    for i, item in enumerate(items):
        rows.append(score_item(item, llm, args.top_k))
        if (i + 1) % 300 == 0:
            print(f"  scored {i+1}/{len(items)}")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    csv_path = args.out + ".csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {csv_path}")

    summary = summarize(rows)
    md_path = args.out + "_summary.md"
    with open(md_path, "w") as f:
        f.write(summary)
    print(f"wrote {md_path}\n")
    print(summary)


if __name__ == "__main__":
    main()

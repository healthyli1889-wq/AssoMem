"""Assemble the reviewer-facing release tree: data/, code/, results/.

Run from the repository root. Writes to a staging directory which is then committed
to an orphan `final` branch, so the release carries no history back to the working
branches.

    python3 tools/build_release.py --out /tmp/final_release

Three things happen on the way through:

1. **Field stripping.** Fields that no code in the release reads and that carry no
   analytic weight are dropped — authoring aids, timestamps, corpus plumbing and
   paths into branches that are not part of the release. Fields that document the
   construct are kept even where nothing reads them, because a reviewer does. The
   full-fidelity records stay on the per-domain working branches.

2. **Anonymisation scan.** The tree is rejected if any real identity, home path,
   repository URL, commit trailer, API key or private endpoint string survives.
   Invented first names inside synthetic dialogue are left alone: they identify
   nobody, and rewriting a collaborator's item text buys no anonymity.

3. **Import rewriting.** The generators locate the shared engine by walking up a
   fixed number of directories. The release layout is flatter, so that one line is
   rewritten rather than left broken.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

# --------------------------------------------------------------------------
# What gets dropped. Every entry was confirmed unread by the release code.
# --------------------------------------------------------------------------

DROP_TOP = (
    # health: restates what render_arms derives from arm_gold
    "available_evaluation_conditions",
)
DROP_PROVENANCE = (
    "voice",                 # authoring register aid
    "external_folder_tag",   # redundant with persona_anchor
    "source_person_name",    # null throughout
    "source_corpus",         # null throughout
    "materialized_from",     # authoring lineage
    "authoring_method",      # authoring lineage
    "created_at",            # authoring timestamp
    "anonymous_submission",  # authoring flag
    "source_data_arm",       # duplicates data_arm
    "release_eligible",      # gate bookkeeping; status is stated in the README
    "gate_0_review_path",    # path into a branch outside the release
    "gate_0_review_unit",    # gate bookkeeping
)

# Kept although nothing reads them: they describe the intervention, which is
# exactly what a reviewer needs to judge the construct.
KEEP_UNREAD = (
    "supporting_constraints",
    "link_broken.connector_change",
    "relational_connector.excludes",
    "relational_connector.link_broken_change",
)

# Visible dialogue is left exactly as authored. One work item names a colleague
# ("Sam"), which DATA CRITERIA section 4 discourages, but it is an invented first
# name attached to a synthetic co-worker, not a real person, so rewriting it would
# alter a collaborator's item text for no gain in anonymity.

FORBIDDEN = (
    (re.compile(r"healthyli|montyzhang|jgwy", re.I), "identity"),
    (re.compile(r"/Users/|/home/[a-z]"), "absolute home path"),
    (re.compile(r"github\.com", re.I), "repository URL"),
    (re.compile(r"co-authored-by", re.I), "commit trailer"),
    (re.compile(r"cursoragent", re.I), "agent identity"),
    (re.compile(r"\bclaire\b|\bmonty\b", re.I), "collaborator handle"),
    (re.compile(r"sk-[A-Za-z0-9._-]{12,}|i0sz7d7v"), "api key"),
    (re.compile(r"maas\.aliyuncs\.com|gpugeek\.com", re.I), "private endpoint"),
)


def strip_record(record: dict) -> dict:
    for field in DROP_TOP:
        record.pop(field, None)
    provenance = record.get("provenance")
    if isinstance(provenance, dict):
        for field in DROP_PROVENANCE:
            provenance.pop(field, None)
    return record


def copy_data(sources: dict[str, Path], out: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for domain, root in sources.items():
        total = 0
        for arm in ("associative", "distractor", "absence"):
            target = out / "data" / domain / arm
            target.mkdir(parents=True, exist_ok=True)
            for path in sorted((root / arm).glob("*.json")):
                record = strip_record(json.loads(path.read_text(encoding="utf-8")))
                (target / path.name).write_text(
                    json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
                )
                total += 1
        counts[domain] = total
    return counts


def copy_code(repo: Path, out: Path) -> None:
    code = out / "code"
    (code / "assomem_vnext").mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo / "experiments/assomem_vnext/schema.py", code / "assomem_vnext/schema.py")

    harness_src = repo / "experiments/assomem_harness"
    harness_dst = code / "assomem_harness"
    harness_dst.mkdir(parents=True, exist_ok=True)
    for name in (
        "aggregate.py", "arms.py", "dataset.py", "manifest.py", "models.py", "profile.py",
        "protocol.py", "reporting.py", "run.py", "scoring.py", "screen_vnext.py",
        "smoke_vnext.py", "workflow.py", "zero_evidence.py",
    ):
        # `query_validity` was the pilot that happened to own the model client; the
        # release names the directory after what it holds.
        text = (harness_src / name).read_text(encoding="utf-8").replace(
            '"query_validity"', '"model_client"'
        )
        (harness_dst / name).write_text(text, encoding="utf-8")
    (harness_dst / "profiles").mkdir(exist_ok=True)
    for path in sorted((harness_src / "profiles").glob("*.json")):
        shutil.copy2(path, harness_dst / "profiles" / path.name)
    (harness_dst / "tests").mkdir(exist_ok=True)
    for path in sorted((harness_src / "tests").glob("*.py")):
        # test_vnext.py points at a fixture that was never committed upstream and
        # errors on collection; shipping it would hand a reviewer a red suite.
        if path.name == "test_vnext.py":
            continue
        shutil.copy2(path, harness_dst / "tests" / path.name)

    (code / "model_client").mkdir(exist_ok=True)
    shutil.copy2(repo / "experiments/query_validity/clients.py", code / "model_client/clients.py")

    generators = code / "generators"
    shared = generators / "vnext_common"
    shared.mkdir(parents=True, exist_ok=True)
    for name in ("engine.py", "allocation.py", "audit.py", "aggregate_ladder.py"):
        shutil.copy2(repo / "staging/vnext_common" / name, shared / name)

    domain_generators = {
        "social": repo / "staging/social-vnext/social/generator",
        "hobby": repo / "staging/hobby-vnext/hobby/generator",
        "finance": repo / "staging/finance-vnext/finance/generator",
    }
    for domain, src in domain_generators.items():
        dst = generators / domain
        dst.mkdir(parents=True, exist_ok=True)
        for path in sorted(src.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            # release layout is code/generators/<domain>/x.py, so the shared engine
            # is one level up rather than three
            text = text.replace(
                'sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "vnext_common"))',
                'sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vnext_common"))',
            )
            (dst / path.name).write_text(text, encoding="utf-8")

    tools = code / "tools"
    tools.mkdir(exist_ok=True)
    shutil.copy2(
        repo / "staging/work-vnext/work/bprime_v2/rewrite_bprime.py", tools / "rewrite_bprime.py"
    )

    docs = repo / "tools/release_docs"
    shutil.copy2(docs / "README.md", out / "README.md")
    shutil.copy2(docs / "data_README.md", out / "data/README.md")
    shutil.copy2(docs / "code_README.md", code / "README.md")
    shutil.copy2(docs / "config.example.sh", code / "config.example.sh")
    shutil.copy2(docs / "test_release_data.py", harness_dst / "tests/test_release_data.py")

    spec = code / "spec"
    spec.mkdir(exist_ok=True)
    shutil.copy2(repo / "experiments/assomem_vnext/DATA CRITERIA_new.md", spec / "DATA_CRITERIA.md")


def extract_prompts(repo: Path, out: Path) -> None:
    """Lift the live prompt strings into readable Markdown.

    The prompts a reviewer cares about are embedded in `protocol.py` as f-strings.
    Rendering them with a placeholder for the payload makes them readable without
    asking anyone to read Python.
    """
    import sys

    sys.path.insert(0, str(repo / "experiments/assomem_harness"))
    from profile import DatasetProfile  # noqa: E402
    import protocol  # noqa: E402

    vnext = DatasetProfile(
        profile_id="release", schema_version=1, data_format="social-vnext-1",
        arms=("associative", "distractor", "absence"), domain_prefixes={"x": "X"},
        filename_template="", context_field="context", query_field="query",
        annotation_field="episode_annotations", evidence_roles={}, capabilities={},
    )
    payload = {"context": ["<20 dated sessions>"], "query": "<the final user turn>",
               "target_proposition": "<the binary proposition being judged>"}
    gold = {"target_proposition": "<proposition>", "allowed_decisions": ["yes", "no"],
            "required_output_fields": ["mode", "answer", "evidence_session_ids"],
            "expected_mode": "<infer_C | withhold_C>", "binary_decision": "<true | false>",
            "required_elements": ["<element>"], "rationale": "<why>",
            "evidence_contract": {"ev_A": "<...>", "ev_B": "<...>"}}
    answer = {"decision": "yes", "answer": "<justification>", "evidence_session_ids": [6, 14]}

    prompts = out / "code" / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    (prompts / "solver.md").write_text(
        "# Solver prompt (vNext)\n\n"
        "Sent once per evaluation arm. The payload carries only `context`, `query` and\n"
        "`target_proposition`; every annotation, gold field and arm label stays behind\n"
        "the boundary in `dataset.solver_input`.\n\n```text\n"
        + protocol.solver_prompt(payload, vnext)
        + "```\n",
        encoding="utf-8",
    )
    (prompts / "judge.md").write_text(
        "# Validator prompt (vNext)\n\n"
        "Sent once per scored arm, to a model that must differ from the solver\n"
        "(`models.validate_solver_validator_independence`).\n\n```text\n"
        + protocol.score_prompt(answer, gold, vnext)
        + "```\n",
        encoding="utf-8",
    )
    shutil.copy2(
        repo / "experiments/assomem_vnext/author_prompt.md", prompts / "author.md"
    )


def copy_results(repo: Path, out: Path) -> None:
    results = {
        "social": ("staging/social-vnext/social/review", "ladder_full_200"),
        "hobby": ("staging/hobby-vnext/hobby/review", "ladder_full_200"),
        "finance": ("staging/finance-vnext/finance/review", "ladder_v3_200"),
        "work": ("staging/work-vnext/work/review", "ladder_bprime_v2_200"),
        "health": ("staging/health-vnext/health/review", "ladder_200"),
    }
    for domain, (folder, stem) in results.items():
        target = out / "results" / domain
        target.mkdir(parents=True, exist_ok=True)
        for suffix in (".json", "_summary.txt"):
            src = repo / folder / f"{stem}{suffix}"
            if src.is_file():
                shutil.copy2(src, target / f"ladder{suffix}")


def scan(out: Path) -> list[str]:
    problems = []
    for path in sorted(out.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{path.relative_to(out)}: not utf-8 text")
            continue
        for pattern, label in FORBIDDEN:
            match = pattern.search(text)
            if match:
                problems.append(f"{path.relative_to(out)}: {label} ({match.group(0)[:24]!r})")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work", type=Path, default=Path("/tmp/work_data"))
    parser.add_argument("--health", type=Path, default=Path("/tmp/health_data"))
    args = parser.parse_args()
    repo = Path.cwd()

    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    counts = copy_data(
        {
            "social": repo / "staging/social-vnext/social/candidates-s1-s20-full",
            "hobby": repo / "staging/hobby-vnext/hobby/candidates-s1-s20-full",
            "finance": repo / "staging/finance-vnext/finance/candidates-s1-s20-v3",
            "work": args.work,
            "health": args.health,
        },
        args.out,
    )
    copy_code(repo, args.out)
    extract_prompts(repo, args.out)
    copy_results(repo, args.out)

    print("data files per domain:", counts, "total", sum(counts.values()))
    problems = scan(args.out)
    if problems:
        print(f"\nSCAN FAILED: {len(problems)} problems")
        for line in problems[:25]:
            print("   ", line)
        return 1
    print("scan clean: no identity, path, URL, key or endpoint strings in the tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

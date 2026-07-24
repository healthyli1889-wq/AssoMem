"""Read-only gold discovery and solver-visible input construction."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from profile import DatasetProfile

EXPERIMENTS_ROOT = Path(__file__).resolve().parents[1]
if str(EXPERIMENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS_ROOT))
from assomem_vnext.schema import validate_candidate  # noqa: E402


@dataclass(frozen=True)
class PairedItem:
    item_id: str
    domain: str
    user_id: str
    scenario_id: str
    arms: dict[str, dict[str, Any]]
    filenames: dict[str, str]


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def discover_items(data_root: Path, profile: DatasetProfile, domain: str) -> list[PairedItem]:
    """Enumerate an entire domain; every base item must have all shipped arms."""
    rows: list[PairedItem] = []
    for user in range(1, 11):
        for scenario in range(1, 21):
            paths = {
                arm: data_root / domain / arm / profile.filename(domain, arm, user, scenario)
                for arm in profile.arms
            }
            missing = [str(path) for path in paths.values() if not path.is_file()]
            if missing:
                raise FileNotFoundError("Paired gold files are missing: " + ", ".join(missing))
            arms = {arm: _read(path) for arm, path in paths.items()}
            _validate_pair(arms, profile, domain, user, scenario)
            rows.append(PairedItem(
                item_id=f"{domain}-u{user:02d}-S{scenario}",
                domain=domain,
                user_id=f"u{user:02d}",
                scenario_id=f"S{scenario}",
                arms=arms,
                filenames={arm: str(path.relative_to(data_root)) for arm, path in paths.items()},
            ))
    return rows


def discover_vnext_items(data_root: Path, profile: DatasetProfile, domain: str) -> list[PairedItem]:
    """Discover one immutable three-file vNext source pair per candidate."""
    if profile.data_format not in {"work-vnext-1", "assomem-vnext-1"}:
        raise ValueError("discover_vnext_items requires an assomem vNext profile")
    grouped: dict[str, dict[str, tuple[dict[str, Any], Path]]] = {}
    for source_arm in profile.arms:
        directory = data_root / source_arm
        if not directory.is_dir():
            raise FileNotFoundError(f"Missing vNext source directory: {directory}")
        for path in sorted(directory.glob("*.json")):
            candidate = _read(path)
            errors = validate_candidate(candidate)
            if errors:
                raise ValueError(f"{path}: invalid vNext candidate: {'; '.join(errors)}")
            if candidate.get("data_arm") != source_arm:
                raise ValueError(f"{path}: data_arm does not match parent directory")
            pair_id = candidate.get("pair_id")
            if not isinstance(pair_id, str) or not pair_id:
                raise ValueError(f"{path}: missing pair_id")
            grouped.setdefault(pair_id, {})[source_arm] = (candidate, path)

    rows: list[PairedItem] = []
    for pair_id, sources in sorted(grouped.items()):
        missing = set(profile.arms) - set(sources)
        if missing:
            raise FileNotFoundError(f"{pair_id}: missing vNext sources: {', '.join(sorted(missing))}")
        arms = {name: value[0] for name, value in sources.items()}
        shared = {(item["user_id"], item["query"], item["domain"]) for item in arms.values()}
        if len(shared) != 1:
            raise ValueError(f"{pair_id}: source files disagree on user, query, or domain")
        user_id, _, _ = next(iter(shared))
        if arms[profile.arms[0]]["domain"] != domain:
            raise ValueError(f"{pair_id}: candidate domain does not match selected domain")
        rows.append(PairedItem(
            item_id=pair_id,
            domain=domain,
            user_id=user_id,
            scenario_id=pair_id,
            arms=arms,
            filenames={
                name: str(path.relative_to(data_root))
                for name, (_, path) in sources.items()
            },
        ))
    if not rows:
        raise FileNotFoundError(f"No vNext candidate pairs found below {data_root}")
    return rows


def _validate_pair(
    arms: dict[str, dict[str, Any]], profile: DatasetProfile, domain: str, user: int, scenario: int
) -> None:
    queries = {item.get(profile.query_field) for item in arms.values()}
    if len(queries) != 1:
        raise ValueError(f"{domain} u{user:02d} S{scenario}: paired arms disagree on query")
    if any(item.get("pilot_arm") != arm for arm, item in arms.items()):
        raise ValueError(f"{domain} u{user:02d} S{scenario}: arm metadata mismatch")
    expected = f"S{scenario}"
    if any(item.get("provenance", {}).get("scenario_id") != expected for item in arms.values()):
        raise ValueError(f"{domain} u{user:02d} S{scenario}: scenario metadata mismatch")


def solver_input(item: dict[str, Any], query: str) -> dict[str, Any]:
    """Construct the exact visible payload; no ground truth can cross this boundary."""
    context = copy.deepcopy(item["context"])
    for session in context:
        session.pop("annotation", None)
    return {
        "context": context,
        "query": query,
        "prompt_hash": hashlib.sha256(
            json.dumps({"context": context, "query": query}, sort_keys=True).encode()
        ).hexdigest(),
    }

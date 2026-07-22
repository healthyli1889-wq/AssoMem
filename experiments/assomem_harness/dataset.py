"""Read-only gold discovery and solver-visible input construction."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from profile import DatasetProfile


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

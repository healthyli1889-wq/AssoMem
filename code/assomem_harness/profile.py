"""Versioned, data-only dataset profiles for the experiment harness."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Dataset profiles that ship the three-file vNext source layout and are driven by
# the vNext prompt contract, arm vocabulary and gold shape. The construct is
# domain-independent, so covering a new domain means adding a profile here rather
# than editing the harness.
VNEXT_DATA_FORMATS = frozenset({"work-vnext-1", "social-vnext-1"})


@dataclass(frozen=True)
class DatasetProfile:
    profile_id: str
    schema_version: int
    data_format: str
    arms: tuple[str, ...]
    domain_prefixes: dict[str, str]
    filename_template: str
    context_field: str
    query_field: str
    annotation_field: str
    evidence_roles: dict[str, str]
    capabilities: dict[str, bool]

    def is_vnext(self) -> bool:
        return self.data_format in VNEXT_DATA_FORMATS

    def filename(self, domain: str, arm: str, user: int, scenario: int) -> str:
        try:
            prefix = self.domain_prefixes[domain]
        except KeyError as exc:
            raise ValueError(f"{domain!r} is not supported by profile {self.profile_id}") from exc
        return self.filename_template.format(
            prefix=prefix, arm=arm, user=user, scenario=scenario
        )


def load_profile(path: Path) -> DatasetProfile:
    raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    required = (
        "profile_id", "schema_version", "arms", "domain_prefixes",
        "filename_template", "context_field", "query_field",
        "annotation_field", "evidence_roles", "capabilities",
    )
    missing = [name for name in required if name not in raw]
    if missing:
        raise ValueError(f"Profile missing fields: {', '.join(missing)}")
    if set(raw["arms"]) != {"associative", "distractor", "absence"}:
        raise ValueError("This harness requires associative/distractor/absence arms")
    return DatasetProfile(
        profile_id=raw["profile_id"],
        schema_version=int(raw["schema_version"]),
        data_format=str(raw.get("data_format", "assomem-v1")),
        arms=tuple(raw["arms"]),
        domain_prefixes=dict(raw["domain_prefixes"]),
        filename_template=raw["filename_template"],
        context_field=raw["context_field"],
        query_field=raw["query_field"],
        annotation_field=raw["annotation_field"],
        evidence_roles=dict(raw["evidence_roles"]),
        capabilities={key: bool(value) for key, value in raw["capabilities"].items()},
    )

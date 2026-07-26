"""Frozen, reviewable item manifests for reproducible pilot selection."""

from __future__ import annotations

import hashlib
import random
from pathlib import Path

from dataset import PairedItem
from profile import DatasetProfile


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _difficulty(item: PairedItem, profile: DatasetProfile) -> dict[str, int | float]:
    base = item.arms["associative"]
    target_sessions = [
        int(session_id)
        for session_id, annotation in base[profile.annotation_field].items()
        if annotation.get("role_setup") == profile.evidence_roles["target"]
    ]
    context_chars = sum(
        len(turn["content"])
        for session in base["context"]
        for turn in session["dialogue"]
    )
    metrics = item.arms["distractor"].get("validity_metrics", {})
    return {
        "context_chars": context_chars,
        "target_session_gap": abs(target_sessions[1] - target_sessions[0]),
        "distractor_similarity": metrics.get("distractor_cosine_query", 0.0),
    }


def build_stratified_manifest(
    items: list[PairedItem], profile: DatasetProfile, data_root: Path, *, count: int, seed: int
) -> dict:
    if count > 20 or count < 1:
        raise ValueError("Pilot manifest count must be between 1 and 20")
    if profile.data_format == "work-vnext-1":
        ordered = sorted(items, key=lambda item: item.item_id)
        if len(ordered) < count:
            raise ValueError(f"Only {len(ordered)} vNext pairs are available")
        # Even stride over the sorted pair list so a small pilot spans all
        # scenario families instead of exhausting S01 first.
        stride = len(ordered) / count
        selected_items = [ordered[int(index * stride)] for index in range(count)]
        selected = [{
            "item_id": item.item_id,
            "user_id": item.user_id,
            "scenario_id": item.scenario_id,
            "arms": item.filenames,
            "source_hashes": {
                arm: _hash_file(data_root / filename)
                for arm, filename in item.filenames.items()
            },
            "difficulty": {
                "context_chars": sum(
                    len(turn["content"])
                    for session in item.arms["associative"]["context"]
                    for turn in session["dialogue"]
                ),
                "relation_specificity": item.arms["associative"].get("relation_specificity", 0),
            },
        } for item in selected_items]
        return {
            "manifest_version": 1,
            "selection_method": "pair_id_even_stride",
            "selection_seed": seed,
            "profile_id": profile.profile_id,
            "domain": "work",
            "items": selected,
        }
    by_key = {(item.user_id, item.scenario_id): item for item in items}
    users = sorted({item.user_id for item in items})
    rng = random.Random(seed)
    rng.shuffle(users)
    selected = []
    for scenario_number in range(1, count + 1):
        scenario_id = f"S{scenario_number}"
        user_id = users[(scenario_number - 1) % len(users)]
        item = by_key[(user_id, scenario_id)]
        selected.append({
            "item_id": item.item_id,
            "user_id": item.user_id,
            "scenario_id": item.scenario_id,
            "arms": item.filenames,
            "source_hashes": {
                arm: _hash_file(data_root / filename)
                for arm, filename in item.filenames.items()
            },
            "difficulty": _difficulty(item, profile),
        })
    return {
        "manifest_version": 1,
        "selection_method": "scenario_complete_user_balanced",
        "selection_seed": seed,
        "profile_id": profile.profile_id,
        "domain": selected[0]["item_id"].split("-")[0],
        "items": selected,
    }


def select_manifest_items(
    items: list[PairedItem], manifest: dict, data_root: Path
) -> list[PairedItem]:
    by_id = {item.item_id: item for item in items}
    selected = []
    for entry in manifest["items"]:
        item = by_id.get(entry["item_id"])
        if item is None:
            raise ValueError(f"Manifest item no longer exists: {entry['item_id']}")
        for arm, expected_hash in entry["source_hashes"].items():
            actual_hash = _hash_file(data_root / item.filenames[arm])
            if actual_hash != expected_hash:
                raise ValueError(f"Gold data changed for {entry['item_id']}:{arm}")
        selected.append(item)
    return selected

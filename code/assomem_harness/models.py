"""Role configuration for one evaluated solver and one independent validator."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "model_client"))
from clients import ModelConfig, config_from_env  # noqa: E402


def load_roles() -> dict[str, ModelConfig]:
    roles = {
        "solver": config_from_env("ASSOMEM_SOLVER"),
        "validator": config_from_env("ASSOMEM_VALIDATOR"),
    }
    if roles["solver"].model == roles["validator"].model:
        raise ValueError("solver and validator models must be distinct")
    return roles


def validate_solver_validator_independence(roles: dict[str, ModelConfig]) -> None:
    if roles["validator"].model.lower() == roles["solver"].model.lower():
        raise ValueError(f"validator cannot score itself ({roles['solver'].model})")

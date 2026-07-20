"""Role configuration for author, validator, and three evaluated solvers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "query_validity"))
from clients import ModelConfig, config_from_env  # noqa: E402


def load_roles() -> dict[str, ModelConfig]:
    roles = {
        "author": config_from_env("ASSOMEM_AUTHOR"),
        "validator": config_from_env("ASSOMEM_VALIDATOR"),
        "solver_a": config_from_env("ASSOMEM_SOLVER_A"),
        "solver_b": config_from_env("ASSOMEM_SOLVER_B"),
        "solver_c": config_from_env("ASSOMEM_SOLVER_C"),
    }
    names = [config.model for config in roles.values()]
    if len(set(names)) != len(names):
        raise ValueError("author, validator, and solver models must be distinct")
    return roles


def validate_solver_validator_independence(roles: dict[str, ModelConfig]) -> None:
    validator = roles["validator"].model.lower()
    for key in ("solver_a", "solver_b", "solver_c"):
        solver = roles[key].model.lower()
        if validator == solver:
            raise ValueError(f"validator cannot score itself ({solver})")

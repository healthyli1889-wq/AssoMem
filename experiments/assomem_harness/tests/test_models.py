import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "assomem_harness"))

from models import load_roles  # noqa: E402


class ModelRoleTests(unittest.TestCase):
    def test_loads_only_solver_and_validator_roles(self):
        environment = {
            "ASSOMEM_SOLVER_PROVIDER": "openai-chat",
            "ASSOMEM_SOLVER_MODEL": "solver-model",
            "ASSOMEM_SOLVER_API_KEY": "solver-key",
            "ASSOMEM_SOLVER_BASE_URL": "https://example.test/v1",
            "ASSOMEM_VALIDATOR_PROVIDER": "openai-chat",
            "ASSOMEM_VALIDATOR_MODEL": "judge-model",
            "ASSOMEM_VALIDATOR_API_KEY": "validator-key",
            "ASSOMEM_VALIDATOR_BASE_URL": "https://example.test/v1",
        }
        with patch.dict(os.environ, environment, clear=True):
            roles = load_roles()
        self.assertEqual(set(roles), {"solver", "validator"})
        self.assertEqual(roles["solver"].model, "solver-model")


if __name__ == "__main__":
    unittest.main()

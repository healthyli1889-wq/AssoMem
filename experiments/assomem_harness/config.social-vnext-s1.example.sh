# Copy to untracked my_config.sh and source from the repository root.
export ASSOMEM_DATA_ROOT="$PWD/staging/social-vnext/v1/s1/candidates"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/social-vnext-1.json"
export ASSOMEM_DOMAIN=social
export ASSOMEM_RUN_ID=social-vnext-s1-pilot-20260724
export ASSOMEM_LOG_ROOT="$PWD/experiments/assomem_harness/runs-vnext"

# Solver and validator must be independent. Keep all values local.
export ASSOMEM_SOLVER_PROVIDER=
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=
export ASSOMEM_VALIDATOR_PROVIDER=
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=

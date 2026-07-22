# Source this file from the repository root after copying it to my_config.sh.
# Keep API keys only in the untracked my_config.sh file.
export ASSOMEM_DATA_ROOT="$PWD/assomem/staging/work-vnext/v1/s1/candidates"
export ASSOMEM_PROFILE="$PWD/assomem/experiments/assomem_harness/profiles/work-vnext-1.json"
export ASSOMEM_DOMAIN=work
export ASSOMEM_RUN_ID=work-vnext-s1-pilot-20260722
# This is deliberately a new log root; legacy experiment logs are never reused.
export ASSOMEM_LOG_ROOT="$PWD/assomem/experiments/assomem_harness/runs-vnext"

# Solver: query-only zero-evidence and visible-memory answers.
export ASSOMEM_SOLVER_PROVIDER=openai-chat
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=

# Validator: independent from the solver and used only after E1 and zero-evidence pass.
export ASSOMEM_VALIDATOR_PROVIDER=openai-chat
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=

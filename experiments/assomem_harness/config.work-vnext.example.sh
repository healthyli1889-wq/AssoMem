# Example work-vNext harness config. Copy to my_config.sh locally.
# Do not put real API keys in any committed file.

export ASSOMEM_DATA_ROOT="$PWD/staging/work-vnext/work/harness-root-s16-s20-v2"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/work-vnext-1.json"
export ASSOMEM_DOMAIN=work
export ASSOMEM_RUN_ID=work-vnext-s16-s20-pilot-v2-YYYYMMDD
export ASSOMEM_LOG_ROOT="$PWD/experiments/assomem_harness/runs-vnext"

# Solver (openai-compatible)
export ASSOMEM_SOLVER_PROVIDER=openai-chat
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=
export ASSOMEM_SOLVER_TIMEOUT=300
export ASSOMEM_SOLVER_MAX_RETRIES=5
export ASSOMEM_SOLVER_MAX_TOKENS=4096

# Validator must differ from solver model string
export ASSOMEM_VALIDATOR_PROVIDER=openai-chat
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=
export ASSOMEM_VALIDATOR_TIMEOUT=300
export ASSOMEM_VALIDATOR_MAX_RETRIES=5
export ASSOMEM_VALIDATOR_MAX_TOKENS=8192

# For S11–S15 pilots, switch data root + run id, e.g.:
# export ASSOMEM_DATA_ROOT="$PWD/staging/work-vnext/work/harness-root-s11-s15-v2"
# export ASSOMEM_RUN_ID=work-vnext-s11-s15-pilot-v2-YYYYMMDD
# See staging/work-vnext/work/WORK_DATA_AND_HARNESS.md

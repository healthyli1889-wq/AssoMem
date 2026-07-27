# Copy to my_config.sh (untracked) and fill in the blanks, then `source my_config.sh`.
# Never commit a filled-in copy: keys belong only in the untracked file.
export ASSOMEM_DATA_ROOT="$PWD/staging/social-vnext/social/candidates-s1-s10-full"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/social-vnext-1.json"
export ASSOMEM_DOMAIN=social
export ASSOMEM_RUN_ID=social-vnext-s1-s10-pilot
# Deliberately a separate log root; legacy experiment logs are never reused.
export ASSOMEM_LOG_ROOT="$PWD/experiments/assomem_harness/runs-vnext"

# Solver: query-only zero-evidence screen and visible-memory answers.
export ASSOMEM_SOLVER_PROVIDER=openai-chat
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=
export ASSOMEM_SOLVER_MAX_TOKENS=1024

# Validator: must be a different model from the solver; used only after E1 and
# the zero-evidence screen pass.
export ASSOMEM_VALIDATOR_PROVIDER=openai-chat
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=
# Reasoning validators spend most of their budget on hidden thinking before the
# JSON appears. Too low a cap returns an empty `content` with finish_reason=length,
# which the harness records as invalid_response rather than a judgment.
export ASSOMEM_VALIDATOR_MAX_TOKENS=4096

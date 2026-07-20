# Read-only data and run identity.
export ASSOMEM_DATA_ROOT="$PWD/src/data"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/assomem-v1.json"
export ASSOMEM_DOMAIN=work
export ASSOMEM_RUN_ID=work-smoke-20260720
export ASSOMEM_LOG_ROOT="$PWD/logs"

# Query author: creates candidate query/GT records.
export ASSOMEM_AUTHOR_PROVIDER=openai-chat
export ASSOMEM_AUTHOR_MODEL=
export ASSOMEM_AUTHOR_API_KEY=
export ASSOMEM_AUTHOR_BASE_URL=https://api.openai.com/v1

# Independent validator: validates query/GT and scores solver answers.
export ASSOMEM_VALIDATOR_PROVIDER=anthropic
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=https://api.anthropic.com/v1

# Three solvers. Set each provider/model/key/base URL independently.
export ASSOMEM_SOLVER_A_PROVIDER=openai-chat
export ASSOMEM_SOLVER_A_MODEL=GPT-oss-20b
export ASSOMEM_SOLVER_A_API_KEY=
export ASSOMEM_SOLVER_A_BASE_URL=
export ASSOMEM_SOLVER_B_PROVIDER=openai-chat
export ASSOMEM_SOLVER_B_MODEL=Gemma-4-31b
export ASSOMEM_SOLVER_B_API_KEY=
export ASSOMEM_SOLVER_B_BASE_URL=
export ASSOMEM_SOLVER_C_PROVIDER=openai-chat
export ASSOMEM_SOLVER_C_MODEL=Qwen-3.6-35b
export ASSOMEM_SOLVER_C_API_KEY=
export ASSOMEM_SOLVER_C_BASE_URL=

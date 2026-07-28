# Copy to my_config.sh and fill in. Never commit a filled-in copy.
#
# The solver and the validator must be different models; models.py refuses
# otherwise, and aggregate.py refuses a run scored by more than one validator.

export ASSOMEM_DOMAIN=social                     # social | hobby | finance | work | health
export ASSOMEM_DATA_ROOT="$PWD/../data/$ASSOMEM_DOMAIN"
export ASSOMEM_PROFILE="$PWD/assomem_harness/profiles/social-vnext-1.json"
export ASSOMEM_RUN_ID=ladder-1
export ASSOMEM_LOG_ROOT="$PWD/runs"

# Some Python builds ship no CA bundle wired into OpenSSL, which makes urllib fail
# TLS verification where curl succeeds. Uncomment if you hit that.
# export SSL_CERT_FILE="$(python3 -c 'import certifi; print(certifi.where())')"

# Solver: the evaluated model.
export ASSOMEM_SOLVER_PROVIDER=openai-chat        # openai-chat | openai-responses | anthropic
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=
export ASSOMEM_SOLVER_MAX_TOKENS=1024
export ASSOMEM_SOLVER_TIMEOUT=180

# Validator: independent judge. Reasoning models spend most of their budget on
# hidden thinking before the JSON appears, so a cap sized for the answer alone
# returns empty content with finish_reason=length.
export ASSOMEM_VALIDATOR_PROVIDER=openai-chat
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=
export ASSOMEM_VALIDATOR_MAX_TOKENS=4096
export ASSOMEM_VALIDATOR_TIMEOUT=300

# Read-only data and run identity.
export ASSOMEM_DATA_ROOT="$PWD/src/data"
export ASSOMEM_PROFILE="$PWD/experiments/assomem_harness/profiles/assomem-v1.json"
export ASSOMEM_DOMAIN=work
export ASSOMEM_RUN_ID=work-smoke-20260720
export ASSOMEM_LOG_ROOT="$PWD/logs"
# Optional on hosts whose system certificate store is incomplete:
# export SSL_CERT_FILE="$(python3 -c 'import certifi; print(certifi.where())')"

# Solver: sees only frozen query + visible dialogue and writes an answer.
export ASSOMEM_SOLVER_PROVIDER=
export ASSOMEM_SOLVER_MODEL=
export ASSOMEM_SOLVER_API_KEY=
export ASSOMEM_SOLVER_BASE_URL=

# Independent validator: sees solver answer plus hidden gold and scores it.
export ASSOMEM_VALIDATOR_PROVIDER=
export ASSOMEM_VALIDATOR_MODEL=
export ASSOMEM_VALIDATOR_API_KEY=
export ASSOMEM_VALIDATOR_BASE_URL=


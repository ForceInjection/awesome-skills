#!/usr/bin/env bash
set -euo pipefail

PROMPT=${1:-"Use the $setup-demo-app skill to create the project in this directory."}
OUT=${2:-"./evals/artifacts/test-01.jsonl"}
ATTACH=${3:-}
CMD=${AGENT_CMD:-}

if [[ -z "${CMD}" ]]; then
  echo "error: AGENT_CMD is not set, please export AGENT_CMD to your agent CLI (e.g., 'opencode run --format json --print-logs')" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUT}")"
if [[ -n "${ATTACH}" ]]; then
  ${CMD} -f "${ATTACH}" -- "${PROMPT}" 2>&1 | tee "${OUT}" >/dev/null
else
  ${CMD} -- "${PROMPT}" 2>&1 | tee "${OUT}" >/dev/null
fi
echo "${OUT}"

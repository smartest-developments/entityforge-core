#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$ROOT_DIR/MVP/dashboard/streamlit_app"

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"

cd "$APP_DIR"

# Safe in Domino startup context; keeps the app self-contained.
if [[ -f requirements.txt ]]; then
  python3 -m pip install -r requirements.txt
fi

BASE_ARGS=(
  run app.py
  --server.address "$HOST"
  --server.port "$PORT"
  --server.headless true
  --browser.gatherUsageStats false
)

# Domino reverse-proxy path support when available.
if [[ -n "${DOMINO_RUN_HOST_PATH:-}" ]]; then
  BASE_PATH="${DOMINO_RUN_HOST_PATH#/}"
  BASE_ARGS+=(--server.baseUrlPath "$BASE_PATH")
fi

exec python3 -m streamlit "${BASE_ARGS[@]}"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$ROOT_DIR/MVP/dashboard/streamlit_app"

PORT="${PORT:-${DOMINO_PORT:-8000}}"
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
  --server.enableCORS false
  --server.enableXsrfProtection false
)

# Optional explicit base path (disabled by default; can cause white screen if wrong).
if [[ -n "${STREAMLIT_BASE_URL_PATH:-}" ]]; then
  BASE_ARGS+=(--server.baseUrlPath "${STREAMLIT_BASE_URL_PATH#/}")
fi

echo "[app.sh] Starting Streamlit"
echo "[app.sh] ROOT_DIR=$ROOT_DIR"
echo "[app.sh] APP_DIR=$APP_DIR"
echo "[app.sh] HOST=$HOST PORT=$PORT"
echo "[app.sh] DOMINO_RUN_HOST_PATH=${DOMINO_RUN_HOST_PATH:-}"
echo "[app.sh] DOMINO_BASE_PATH=${DOMINO_BASE_PATH:-}"
echo "[app.sh] DOMINO_PORT=${DOMINO_PORT:-}"
echo "[app.sh] STREAMLIT_BASE_URL_PATH=${STREAMLIT_BASE_URL_PATH:-}"
echo "[app.sh] Final args: ${BASE_ARGS[*]}"

if command -v streamlit >/dev/null 2>&1; then
  exec streamlit "${BASE_ARGS[@]}"
fi

exec python3 -m streamlit "${BASE_ARGS[@]}"

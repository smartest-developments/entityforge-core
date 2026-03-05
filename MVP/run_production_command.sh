#!/usr/bin/env bash
set -euo pipefail

# Production one-command run (pipeline + auto recovery + diagnostics on failure)
# Stable profile for current production environment:
# - single-thread load
# - proactive batching (1k records per file)
# - continue past failed split files (up to max-failed-files)
# - per-file timeout to avoid long stalls
# - ultra-small chunk fallback (100)
# - core dumps disabled for cleaner operations
ulimit -c 0 || true

LOAD_FILE_TIMEOUT_SECONDS="${LOAD_FILE_TIMEOUT_SECONDS:-180}"

python3 run_mvp_with_auto_diagnosis.py \
  --input-json /mnt/Senzing-Ready.json \
  --senzing-env /opt/senzing/er/resources/templates/setupEnv \
  --runtime-dir /mnt/mvp_runtime \
  --load-batch-size 1000 \
  --continue-on-failed-file \
  --max-failed-files 50 \
  --load-file-timeout-seconds "$LOAD_FILE_TIMEOUT_SECONDS" \
  --load-chunk-size 100

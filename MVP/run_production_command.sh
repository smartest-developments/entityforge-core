#!/usr/bin/env bash
set -euo pipefail

# Production one-command run (pipeline + auto recovery + diagnostics on failure)
# Stable profile for current production environment:
# - single-thread load
# - proactive batching (100k records per batch)
# - continue past failed split files (up to max-failed-files)
# - ultra-small chunk fallback (100)
# - keep chunk files for post-failure pinpoint analysis
# - core dumps disabled for cleaner operations
ulimit -c 0 || true

python3 run_mvp_with_auto_diagnosis.py \
  --input-json /mnt/Senzing-Ready.json \
  --senzing-env /opt/senzing/er/resources/templates/setupEnv \
  --runtime-dir /mnt/mvp_runtime \
  --load-threads 1 \
  --load-fallback-threads 1 \
  --load-batch-size 100000 \
  --keep-load-batch-files \
  --continue-on-failed-file \
  --max-failed-files 50 \
  --load-chunk-size 100 \
  --keep-load-chunk-files

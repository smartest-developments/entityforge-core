#!/usr/bin/env bash
set -euo pipefail

# Production one-command run (pipeline + auto recovery + diagnostics on failure)
python3 run_mvp_with_auto_diagnosis.py \
  --input-json /mnt/Senzing-Ready.json \
  --senzing-env /opt/senzing/er/resources/templates/setupEnv \
  --runtime-dir /mnt/mvp_runtime

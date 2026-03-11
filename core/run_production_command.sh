#!/usr/bin/env bash
set -euo pipefail

# Production one-command run (pipeline + auto recovery + diagnostics on failure)
# Stable profile for current production environment:
# - configurable load thread count with adaptive thread backoff on failed batches
# - proactive batching (1k records per file) with smaller chunk fallback
# - continue past failed split files (up to max-failed-files)
# - per-file timeout to avoid long stalls
# - ultra-small chunk fallback (100)
# - post-run audit package generation from the same mapped_output.jsonl
# - core dumps disabled for cleaner operations
ulimit -c 0 || true
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INPUT_JSON="${INPUT_JSON:-$ROOT_DIR/Senzing-Ready.json}"
if [[ ! -f "$INPUT_JSON" && -f /mnt/Senzing-Ready.json ]]; then
  INPUT_JSON="/mnt/Senzing-Ready.json"
fi
INPUT_RECORD_LIMIT="${INPUT_RECORD_LIMIT:-0}"
INPUT_ARRAY_KEY="${INPUT_ARRAY_KEY:-}"
SENZING_ENV="${SENZING_ENV:-/opt/senzing/er/resources/templates/setupEnv}"
EXECUTION_MODE="${EXECUTION_MODE:-local}"
LOAD_FILE_TIMEOUT_SECONDS="${LOAD_FILE_TIMEOUT_SECONDS:-180}"
STEP_TIMEOUT_SECONDS="${STEP_TIMEOUT_SECONDS:-28800}"
LOAD_THREADS="${LOAD_THREADS:-3}"
LOAD_FALLBACK_THREADS="${LOAD_FALLBACK_THREADS:-1}"
LOAD_SHUFFLE_PRIMARY="${LOAD_SHUFFLE_PRIMARY:-1}"
LOAD_BATCH_SIZE="${LOAD_BATCH_SIZE:-1000}"
LOAD_CHUNK_SIZE="${LOAD_CHUNK_SIZE:-100}"
KEEP_LOAD_BATCH_FILES="${KEEP_LOAD_BATCH_FILES:-1}"
MAX_FAILED_FILES="${MAX_FAILED_FILES:-50}"
SNAPSHOT_THREADS="${SNAPSHOT_THREADS:-1}"
AUDIT_OUTPUT_SUBDIR="${AUDIT_OUTPUT_SUBDIR:-senzing_audit}"
NON_MATCH_WHY_OUTPUT_SUBDIR="${NON_MATCH_WHY_OUTPUT_SUBDIR:-non_match_why}"
NON_MATCH_WHY_PAIR_LIMIT="${NON_MATCH_WHY_PAIR_LIMIT:-500}"
RUN_STAMP="$(date '+%Y%m%d_%H%M%S')"
OUTPUT_LABEL="${OUTPUT_LABEL:-production_${RUN_STAMP}}"
RUNTIME_DIR="${RUNTIME_DIR:-/mnt/runtime}"
STAGING_ROOT="${STAGING_ROOT:-$RUNTIME_DIR/_staging/$OUTPUT_LABEL}"
OUTPUT_ROOT="${OUTPUT_ROOT:-$STAGING_ROOT/output_root}"
DIAGNOSTIC_OUTPUT_DIR="${DIAGNOSTIC_OUTPUT_DIR:-$STAGING_ROOT/diagnostics}"

if [[ ! -f "$INPUT_JSON" ]]; then
  echo "ERROR: input JSON not found: $INPUT_JSON" >&2
  exit 2
fi

PIPELINE_INPUT_JSON="$INPUT_JSON"
if [[ "$INPUT_RECORD_LIMIT" =~ ^[0-9]+$ ]] && [[ "$INPUT_RECORD_LIMIT" -gt 0 ]]; then
  export STAGING_ROOT OUTPUT_LABEL INPUT_RECORD_LIMIT
  LIMITED_INPUT_JSON="$(
    python3 - <<'PY'
import os
from pathlib import Path

staging_root = Path(os.environ["STAGING_ROOT"]).resolve()
label = os.environ["OUTPUT_LABEL"]
limit = os.environ["INPUT_RECORD_LIMIT"]
target = staging_root / "_limited_inputs" / f"{label}__first_{limit}.jsonl"
target.parent.mkdir(parents=True, exist_ok=True)
print(target)
PY
  )"

  LIMIT_CMD=(
    python3 "$ROOT_DIR/app/create_limited_input.py"
    "$INPUT_JSON"
    "$LIMITED_INPUT_JSON"
    --limit "$INPUT_RECORD_LIMIT"
  )
  if [[ -n "$INPUT_ARRAY_KEY" ]]; then
    LIMIT_CMD+=(--array-key "$INPUT_ARRAY_KEY")
  fi

  echo "Creating limited input for smoke/full-flow validation..."
  printf ' %q' "${LIMIT_CMD[@]}"
  printf '\n'
  "${LIMIT_CMD[@]}"
  PIPELINE_INPUT_JSON="$LIMITED_INPUT_JSON"
fi

PIPELINE_CMD=(
  python3 "$ROOT_DIR/app/run_mvp_with_auto_diagnosis.py"
  --input-json "$PIPELINE_INPUT_JSON"
  --execution-mode "$EXECUTION_MODE"
  --senzing-env "$SENZING_ENV"
  --runtime-dir "$RUNTIME_DIR"
  --output-root "$OUTPUT_ROOT"
  --diagnostic-output-dir "$DIAGNOSTIC_OUTPUT_DIR"
  --output-label "$OUTPUT_LABEL"
  --step-timeout-seconds "$STEP_TIMEOUT_SECONDS"
  --load-threads "$LOAD_THREADS"
  --load-fallback-threads "$LOAD_FALLBACK_THREADS"
  --load-batch-size "$LOAD_BATCH_SIZE"
  --continue-on-failed-file
  --max-failed-files "$MAX_FAILED_FILES"
  --load-file-timeout-seconds "$LOAD_FILE_TIMEOUT_SECONDS"
  --load-chunk-size "$LOAD_CHUNK_SIZE"
  --snapshot-threads "$SNAPSHOT_THREADS"
  --with-snapshot
)

if [[ "$LOAD_SHUFFLE_PRIMARY" == "1" ]]; then
  PIPELINE_CMD+=(--load-shuffle-primary)
fi
if [[ "$KEEP_LOAD_BATCH_FILES" == "1" ]]; then
  PIPELINE_CMD+=(--keep-load-batch-files)
fi

echo "Running full production pipeline..."
printf ' %q' "${PIPELINE_CMD[@]}"
printf '\n'
"${PIPELINE_CMD[@]}"

export ROOT_DIR OUTPUT_ROOT OUTPUT_LABEL AUDIT_OUTPUT_SUBDIR RUNTIME_DIR
RUN_OUTPUT_DIR="$(
  python3 - <<'PY'
import os
from pathlib import Path

root_dir = Path(os.environ["ROOT_DIR"]).resolve()
output_root = Path(os.environ["OUTPUT_ROOT"])
if not output_root.is_absolute():
    output_root = (root_dir / output_root).resolve()
runs_root = Path(os.environ["RUNTIME_DIR"]).resolve() / "runs"

candidates = sorted(
    [
        path / "output_bundle"
        for path in runs_root.glob("run_mvp_*")
        if path.is_dir() and (path / "output_bundle").is_dir()
    ],
    key=lambda path: path.stat().st_mtime,
    reverse=True,
)
if candidates:
    print(candidates[0])
    raise SystemExit(0)

label = os.environ["OUTPUT_LABEL"]
legacy = sorted(
    [path for path in output_root.glob(f"*__{label}") if path.is_dir()],
    key=lambda path: path.stat().st_mtime,
    reverse=True,
)
if not legacy:
    raise SystemExit(1)
print(legacy[0])
PY
)"

RUN_SUMMARY_JSON="$RUN_OUTPUT_DIR/technical output/run_summary.json"
MAPPED_OUTPUT_JSONL="$RUN_OUTPUT_DIR/technical output/mapped_output.jsonl"
if [[ ! -f "$RUN_SUMMARY_JSON" ]]; then
  echo "ERROR: run summary not found: $RUN_SUMMARY_JSON" >&2
  exit 2
fi
if [[ ! -f "$MAPPED_OUTPUT_JSONL" ]]; then
  echo "ERROR: mapped output not found: $MAPPED_OUTPUT_JSONL" >&2
  exit 2
fi

export RUN_SUMMARY_JSON
PROJECT_DIR="$(
  python3 - <<'PY'
import json
import os
from pathlib import Path

summary_path = Path(os.environ["RUN_SUMMARY_JSON"])
payload = json.loads(summary_path.read_text(encoding="utf-8"))
project_dir = str(payload.get("project_dir") or "").strip()
if not project_dir:
    raise SystemExit(1)
print(project_dir)
PY
)"

if [[ "$PROJECT_DIR" == /runtime/* ]]; then
  PROJECT_DIR="$RUNTIME_DIR/${PROJECT_DIR#/runtime/}"
fi

AUDIT_OUTPUT_DIR="$RUN_OUTPUT_DIR/$AUDIT_OUTPUT_SUBDIR"
NON_MATCH_WHY_OUTPUT_DIR="$RUN_OUTPUT_DIR/$NON_MATCH_WHY_OUTPUT_SUBDIR"
RUN_DIAGNOSTICS_DIR="$RUN_OUTPUT_DIR/diagnostics"
RUN_LIMITED_INPUTS_DIR="$RUN_OUTPUT_DIR/limited_inputs"

if [[ -n "${LIMITED_INPUT_JSON:-}" && -f "$LIMITED_INPUT_JSON" ]]; then
  mkdir -p "$RUN_LIMITED_INPUTS_DIR"
  FINAL_LIMITED_INPUT_JSON="$RUN_LIMITED_INPUTS_DIR/$(basename "$LIMITED_INPUT_JSON")"
  mv "$LIMITED_INPUT_JSON" "$FINAL_LIMITED_INPUT_JSON"
  PIPELINE_INPUT_JSON="$FINAL_LIMITED_INPUT_JSON"
fi

if [[ -d "$DIAGNOSTIC_OUTPUT_DIR" ]]; then
  mkdir -p "$RUN_DIAGNOSTICS_DIR"
  while IFS= read -r item; do
    mv "$item" "$RUN_DIAGNOSTICS_DIR/"
  done < <(find "$DIAGNOSTIC_OUTPUT_DIR" -mindepth 1 -maxdepth 1)
fi

echo "Running audit package generation..."
AUDIT_CMD=(
  python3 "$ROOT_DIR/app/prepare_senzing_audit_inputs.py"
  "$MAPPED_OUTPUT_JSONL"
  --project-dir "$PROJECT_DIR"
  --output-dir "$AUDIT_OUTPUT_DIR"
  --data-source PARTNERS
  --snapshot-threads "$SNAPSHOT_THREADS"
)
printf ' %q' "${AUDIT_CMD[@]}"
printf '\n'
EXECUTION_MODE="$EXECUTION_MODE" "${AUDIT_CMD[@]}"

echo "Running non-match WHY report generation..."
NON_MATCH_WHY_CMD=(
  python3 "$ROOT_DIR/app/build_non_match_why_report.py"
  --run-output-dir "$RUN_OUTPUT_DIR"
  --project-dir "$PROJECT_DIR"
  --output-dir "$NON_MATCH_WHY_OUTPUT_DIR"
  --data-source PARTNERS
  --why-pair-limit "$NON_MATCH_WHY_PAIR_LIMIT"
)
printf ' %q' "${NON_MATCH_WHY_CMD[@]}"
printf '\n'
"${NON_MATCH_WHY_CMD[@]}"

rm -rf "$STAGING_ROOT"
if [[ -d "$(dirname "$STAGING_ROOT")" ]]; then
  rmdir "$(dirname "$STAGING_ROOT")" 2>/dev/null || true
fi

echo
echo "Production pipeline + audit completed."
echo "Run output directory: $RUN_OUTPUT_DIR"
echo "Source input JSON: $INPUT_JSON"
echo "Pipeline input JSON: $PIPELINE_INPUT_JSON"
echo "Mapped output JSONL: $MAPPED_OUTPUT_JSONL"
echo "Project directory: $PROJECT_DIR"
echo "Audit output directory: $AUDIT_OUTPUT_DIR"
echo "Non-match WHY directory: $NON_MATCH_WHY_OUTPUT_DIR"

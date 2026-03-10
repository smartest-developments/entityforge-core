#!/usr/bin/env bash
set -euo pipefail

# One-command production audit package generation without re-running load.
#
# Choose one mode:
# - PROJECT_DIR: existing Senzing project with setupEnv, bin/sz_snapshot, bin/sz_audit
# - SNAPSHOT_CSV + AUDIT_BIN: reuse an existing sz_snapshot -A CSV and run only sz_audit
#
# INPUT_JSON is optional when PROJECT_DIR is provided and the script can auto-discover
# a matching run input or mapped JSONL from run metadata.
#
# Optional:
# - OUTPUT_DIR: target folder for generated artifacts
# - DATA_SOURCE: mapper DATA_SOURCE value (default: PARTNERS)
# - SNAPSHOT_THREADS: threads for sz_snapshot (default: 1)
# - SKIP_EMPTY_CLUSTER_ID: 1 to omit rows with empty IPG ID
# - ARRAY_KEY, FUZZY_CUTOFF, SCAN_RECORDS

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INPUT_JSON="${INPUT_JSON:-}"
PROJECT_DIR="${PROJECT_DIR:-}"
SNAPSHOT_CSV="${SNAPSHOT_CSV:-}"
AUDIT_BIN="${AUDIT_BIN:-}"
OUTPUT_DIR="${OUTPUT_DIR:-}"
DATA_SOURCE="${DATA_SOURCE:-PARTNERS}"
SNAPSHOT_THREADS="${SNAPSHOT_THREADS:-1}"
SKIP_EMPTY_CLUSTER_ID="${SKIP_EMPTY_CLUSTER_ID:-0}"
ARRAY_KEY="${ARRAY_KEY:-}"
FUZZY_CUTOFF="${FUZZY_CUTOFF:-0.90}"
SCAN_RECORDS="${SCAN_RECORDS:-500}"

if [[ -z "$PROJECT_DIR" && -z "$SNAPSHOT_CSV" ]]; then
  echo "ERROR: set PROJECT_DIR or SNAPSHOT_CSV." >&2
  exit 2
fi

if [[ -z "$INPUT_JSON" && -z "$PROJECT_DIR" ]]; then
  echo "ERROR: INPUT_JSON is required unless PROJECT_DIR is set for auto-discovery." >&2
  exit 2
fi

if [[ -n "$SNAPSHOT_CSV" && -z "$PROJECT_DIR" && -z "$AUDIT_BIN" ]]; then
  echo "ERROR: when using SNAPSHOT_CSV without PROJECT_DIR, set AUDIT_BIN too." >&2
  exit 2
fi

CMD=(
  python3
  "$ROOT_DIR/app/prepare_senzing_audit_inputs.py"
  --data-source "$DATA_SOURCE"
  --fuzzy-cutoff "$FUZZY_CUTOFF"
  --scan-records "$SCAN_RECORDS"
  --snapshot-threads "$SNAPSHOT_THREADS"
)

if [[ -n "$INPUT_JSON" ]]; then
  CMD=(
    python3
    "$ROOT_DIR/app/prepare_senzing_audit_inputs.py"
    "$INPUT_JSON"
    --data-source "$DATA_SOURCE"
    --fuzzy-cutoff "$FUZZY_CUTOFF"
    --scan-records "$SCAN_RECORDS"
    --snapshot-threads "$SNAPSHOT_THREADS"
  )
fi

if [[ -n "$OUTPUT_DIR" ]]; then
  CMD+=(--output-dir "$OUTPUT_DIR")
fi

if [[ -n "$ARRAY_KEY" ]]; then
  CMD+=(--array-key "$ARRAY_KEY")
fi

if [[ "$SKIP_EMPTY_CLUSTER_ID" == "1" ]]; then
  CMD+=(--skip-empty-cluster-id)
fi

if [[ -n "$PROJECT_DIR" ]]; then
  CMD+=(--project-dir "$PROJECT_DIR")
fi

if [[ -n "$SNAPSHOT_CSV" ]]; then
  CMD+=(--snapshot-csv "$SNAPSHOT_CSV")
fi

if [[ -n "$AUDIT_BIN" ]]; then
  CMD+=(--audit-bin "$AUDIT_BIN")
fi

echo "Running production audit package generation..."
printf ' %q' "${CMD[@]}"
printf '\n'

"${CMD[@]}"

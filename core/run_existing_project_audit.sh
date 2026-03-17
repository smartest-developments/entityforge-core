#!/usr/bin/env bash
set -euo pipefail

# One-command production audit package generation without re-running load.
#
# Choose one mode:
# - PROJECT_DIR: existing Senzing project with setupEnv, bin/sz_snapshot, bin/sz_audit
# - SNAPSHOT_CSV + AUDIT_BIN: reuse an existing sz_snapshot -A CSV and run only sz_audit
#
# INPUT_JSON is optional:
# - if omitted and ./Senzing-Ready.json exists, that file is used
# - otherwise, when PROJECT_DIR is provided, the script can auto-discover
#   a matching run input or mapped JSONL from run metadata.
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
RUNTIME_DIR="${RUNTIME_DIR:-/mnt/runtime}"

if [[ -z "$INPUT_JSON" && -f "$ROOT_DIR/Senzing-Ready.json" ]]; then
  INPUT_JSON="$ROOT_DIR/Senzing-Ready.json"
fi

if [[ -z "$INPUT_JSON" && -z "$PROJECT_DIR" && -z "$SNAPSHOT_CSV" ]]; then
  export ROOT_DIR RUNTIME_DIR
  AUTOFILL="$(
    python3 - <<'PY'
import json
import os
from pathlib import Path

root_dir = Path(os.environ["ROOT_DIR"]).resolve()
runtime_dir = Path(os.environ["RUNTIME_DIR"]).expanduser()
if not runtime_dir.is_absolute():
    runtime_dir = (root_dir / runtime_dir).resolve()
else:
    runtime_dir = runtime_dir.resolve()

candidate_runs_roots = [runtime_dir / "runs", root_dir / "runtime" / "runs"]
output_bundles = []
seen = set()
for runs_root in candidate_runs_roots:
    if not runs_root.exists():
        continue
    for bundle in runs_root.glob("run_mvp_*/output_bundle"):
        if not bundle.is_dir():
            continue
        key = str(bundle.resolve())
        if key in seen:
            continue
        seen.add(key)
        output_bundles.append(bundle.resolve())

if not output_bundles:
    raise SystemExit(2)

latest_bundle = sorted(output_bundles, key=lambda p: p.stat().st_mtime, reverse=True)[0]
run_summary = latest_bundle / "technical output" / "run_summary.json"
mapped_output = latest_bundle / "technical output" / "mapped_output.jsonl"
if not run_summary.exists() or not mapped_output.exists():
    raise SystemExit(3)

payload = json.loads(run_summary.read_text(encoding="utf-8"))
project_dir_raw = str(payload.get("project_dir") or "").strip()
if not project_dir_raw:
    raise SystemExit(4)

if project_dir_raw.startswith("/runtime/"):
    project_dir = runtime_dir / project_dir_raw.removeprefix("/runtime/")
else:
    project_dir = Path(project_dir_raw).expanduser().resolve()

print(f"INPUT_JSON={mapped_output}")
print(f"PROJECT_DIR={project_dir}")
print(f"OUTPUT_DIR={latest_bundle / 'senzing_audit'}")
PY
  )" || {
    echo "ERROR: unable to auto-discover latest run. Set INPUT_JSON and PROJECT_DIR explicitly." >&2
    exit 2
  }

  while IFS= read -r line; do
    case "$line" in
      INPUT_JSON=*) INPUT_JSON="${line#INPUT_JSON=}" ;;
      PROJECT_DIR=*) PROJECT_DIR="${line#PROJECT_DIR=}" ;;
      OUTPUT_DIR=*) OUTPUT_DIR="${line#OUTPUT_DIR=}" ;;
    esac
  done <<< "$AUTOFILL"

  echo "Auto-discovered latest run inputs:"
  echo "  INPUT_JSON=$INPUT_JSON"
  echo "  PROJECT_DIR=$PROJECT_DIR"
  echo "  OUTPUT_DIR=$OUTPUT_DIR"
fi

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

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "[validate] missing required file: $path" >&2
    exit 2
  fi
}

require_file "core/run_production_command.sh"
require_file "core/run_existing_project_audit.sh"
require_file "core/testing/run_dashboard_tests.py"
require_file "core/app/verify_dashboard_metrics.py"

echo "[validate] shell syntax"
bash -n core/run_production_command.sh
bash -n core/run_existing_project_audit.sh

echo "[validate] python compile"
python3 - <<'PY'
import py_compile
from pathlib import Path

for root in [Path("core/app"), Path("core/testing")]:
    for path in sorted(root.rglob("*.py")):
        py_compile.compile(str(path), doraise=True)
PY

LATEST_OUTPUT_BUNDLE="$(find "${ROOT_DIR}/core" -path '*/output_bundle' -type d | sort | tail -n 1 || true)"

if [[ -n "${LATEST_OUTPUT_BUNDLE}" ]]; then
  DASHBOARD_DATA_PATH="${LATEST_OUTPUT_BUNDLE}/dashboard_web/management_dashboard_data.js"
  if [[ ! -f "${DASHBOARD_DATA_PATH}" ]]; then
    echo "[validate] latest output bundle has no dashboard data; skipping dashboard runtime validation"
    echo "[validate] done"
    exit 0
  fi

  RUN_ID="$(
    python3 - <<'PY' "${DASHBOARD_DATA_PATH}"
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding="utf-8")
prefix = "window.MVP_DASHBOARD_DATA = "
if not raw.startswith(prefix):
    raise SystemExit(1)
payload = raw[len(prefix):].strip()
if payload.endswith(";"):
    payload = payload[:-1]
data = json.loads(payload)
runs = data.get("runs") if isinstance(data, dict) else None
if not isinstance(runs, list) or not runs:
    raise SystemExit(1)
run_id = str(runs[0].get("run_id") or "").strip()
if not run_id:
    raise SystemExit(1)
print(run_id)
PY
  )"

  TEMP_OUTPUT_ROOT="$(mktemp -d)"
  trap 'rm -rf "${TEMP_OUTPUT_ROOT}"' EXIT
  ln -s "${LATEST_OUTPUT_BUNDLE}" "${TEMP_OUTPUT_ROOT}/${RUN_ID}"

  echo "[validate] dashboard tests against latest output bundle: ${LATEST_OUTPUT_BUNDLE}"
  python3 core/testing/run_dashboard_tests.py \
    --output-root "${TEMP_OUTPUT_ROOT}" \
    --dashboard-data "${DASHBOARD_DATA_PATH}" \
    --report-json "${LATEST_OUTPUT_BUNDLE}/dashboard_web/dashboard_test_suite_report.json" \
    --report-md "${LATEST_OUTPUT_BUNDLE}/dashboard_web/dashboard_test_suite_report.md"

  echo "[validate] dashboard metric audit against latest output bundle"
  python3 core/app/verify_dashboard_metrics.py \
    --output-root "${TEMP_OUTPUT_ROOT}" \
    --dashboard-data "${DASHBOARD_DATA_PATH}" \
    --report-json "${LATEST_OUTPUT_BUNDLE}/dashboard_web/dashboard_data_audit_report.json" \
    --report-md "${LATEST_OUTPUT_BUNDLE}/dashboard_web/dashboard_data_audit_report.md"
else
  echo "[validate] no output bundle found under core/; skipping dashboard runtime validation"
fi

echo "[validate] done"

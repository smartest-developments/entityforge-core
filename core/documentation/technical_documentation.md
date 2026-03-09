# Technical Documentation

## 1) Purpose
This document explains, in operational detail, how the core pipeline runs end-to-end, how it is executed in production, why the resilience settings were introduced, and how dashboard numbers are generated and validated.

## 2) Repository Structure (Core Scope)
Main folder:
- `core/`

Key runtime and reporting areas:
- `core/run_production_command.sh`: one-command production execution profile
- `core/app/run_mvp_with_auto_diagnosis.py`: wrapper (pipeline + automatic diagnostics)
- `core/app/run_mvp_pipeline.py`: orchestrator (map -> E2E -> artifacts -> dashboard rebuild)
- `core/app/run_senzing_end_to_end.py`: Senzing engine execution and load strategy
- `core/app/diagnose_senzing_runtime.py`: failure investigation report generator
- `core/app/build_management_dashboard.py`: dashboard data rebuild + tests + metric audit
- `core/app/verify_dashboard_metrics.py`: metric cross-check against technical artifacts
- `core/testing/`: dashboard test suite
- `core/dashboard/`: static dashboard bundle + streamlit app subfolder
- `core/output/`: timestamped run outputs
- `core/documentation/`: business and technical documents

## 3) Supported Inputs and Parsing Behavior
Input accepted by pipeline:
- JSON array
- JSON object containing array (auto-detect keys such as `records`, `data`, `items`)
- JSONL

Parsing behavior:
- Encoding fallback is implemented in the pipeline (UTF-8, UTF-16 variants, UTF-32 variants, CP1252, Latin-1).
- For JSONL validation, the pipeline checks sample lines before full processing.
- If parsing fails, a clear error is returned with attempted encodings.

## 4) License Resolution Logic
License is loaded in this order:
1. `--license-base64-file <path>`
2. environment variable `SENZING_LICENSE_BASE64_FILE`
3. `core/.secrets/g2.lic_base64`
4. `core/license/g2.lic_base64`

If found, the value is injected as:
- `SENZING_LICENSE_STRING_BASE64`

If not found:
- engine may run in evaluation mode (500-record limit).

## 5) One-Command Production Run (Recommended)
Production run is designed to be launched via shell script:

```bash
cd core
bash run_production_command.sh
```

Current production profile in `run_production_command.sh`:
- `--load-batch-size 1000`
- `--load-chunk-size 100`
- `--continue-on-failed-file`
- `--max-failed-files 50`
- `--load-file-timeout-seconds ${LOAD_FILE_TIMEOUT_SECONDS:-180}`
- `ulimit -c 0` to avoid core dump clutter

Custom timeout example:
```bash
cd core
LOAD_FILE_TIMEOUT_SECONDS=240 bash run_production_command.sh
```

## 6) Why This Profile Exists (Operational Rationale)
During large runs, we observed:
- native loader pressure (`flatbuffer allocation failure / BufferFullError`)
- resolved-entity lock contention (`SENZ0010` locklist timeout)
- stalls on specific data segments

To stabilize execution:
- load thread is kept to 1 in production wrapper
- input is physically split into files of 1,000 records
- failed batches can be retried with chunk fallback at 100 records
- per-file timeout prevents long indefinite stalls
- failed files can be quarantined and tracked by row range

Trade-off:
- higher completion reliability
- longer total runtime

## 7) End-to-End Execution Flow
1. Input ingestion and preflight:
- source file existence check
- runtime/output directories creation
- disk preflight for large runs

2. Mapping:
- `partner_json_to_senzing.py` maps source records to `mapped_output.jsonl`
- field map and mapping summary are saved under technical output

3. Senzing execution:
- `run_senzing_end_to_end.py` receives mapped JSONL
- can run in local mode or docker mode
- by default, snapshot and explain are skipped unless explicitly enabled
- stream export is enabled for large runs to reduce output pressure

4. Load strategy:
- primary load attempt
- fallback load attempt
- optional chunk fallback when enabled
- optional proactive split-file loading (`--load-batch-size`)

5. Artifacts collection:
- technical files copied to `core/output/<timestamp>__<label>/technical output/`
- includes run summary, management summary, quality files, entity/match csv files

6. Dashboard refresh:
- `build_management_dashboard.py` is called automatically at the end
- this step also runs tests/audit unless explicitly skipped

## 8) Large-Run Auto-Tuning in `run_mvp_pipeline.py`
When input records are above threshold (default 300,000) and tuning is enabled:
- timeout is raised (floor)
- load/snapshot threads are reduced
- no-shuffle primary load is enabled
- stream export is enabled
- chunk fallback is enabled
- proactive load batch size is set if not already provided

This auto-tuning is designed for safer completion on heavy datasets.

## 9) Split-File and Chunk Behavior Details
With `--load-batch-size`:
- input JSONL is split into sequential files (`load_batch_00001.jsonl`, etc.)
- logs include:
  - `[LOAD] Starting file X/Y (...)`
  - `[LOAD] Loaded file X/Y successfully (...) in N seconds`
  - `[LOAD] FAILED at file X/Y (...)`

If a file fails:
- file can be copied to quarantine directory:
  - `.../failed_files/failed_file_<index>_rows_<start>_<end>.jsonl`
- processing can continue (`--continue-on-failed-file`)
- hard stop can be configured by `--max-failed-files`

With chunk fallback:
- failed load can be retried in smaller JSONL chunks
- chunk attempts are logged as separate steps

## 10) Diagnostics and Failure Escalation
Wrapper script:
- `run_mvp_with_auto_diagnosis.py`

Behavior:
- always runs pipeline command first
- runs diagnostics on failure (or on success unless skipped)
- prints compact `COPY THIS BLOCK` summary for escalation

Diagnostics output:
- `core/output/diagnostics/runtime_diagnostic_<timestamp>.json`
- `core/output/diagnostics/runtime_diagnostic_<timestamp>.md`
- `core/output/diagnostics/runtime_diagnostic_<timestamp>.txt`

## 11) Dashboard Build and Data Selection Logic
Dashboard script:
- `core/app/build_management_dashboard.py`

Current behavior:
- default: uses only latest run chronologically
- optional history mode: `--all-runs`
- writes:
  - `management_dashboard_data.js`
  - `management_dashboard_data.json`
  - flat CSV exports for runs/summary/top-keys/entity-distribution

Validation steps executed by default:
- `testing/run_dashboard_tests.py`
- `verify_dashboard_metrics.py`

## 12) Dashboard and Streamlit Alignment
During dashboard rebuild, the same generated data is synced to:
- `core/dashboard/management_dashboard_data.js`
- `core/dashboard/streamlit_app/assets/management_dashboard_data.js`

This ensures HTML dashboard and Streamlit app show the same latest numbers.

## 13) Streamlit Application Startup
Primary startup script:
- `/app.sh` (repo root)

What it does:
- changes directory to `core/dashboard/streamlit_app`
- installs requirements if needed
- runs Streamlit with host/port and Domino-safe flags
- supports optional base path via `STREAMLIT_BASE_URL_PATH`

Commands:
```bash
cd /Users/simones/Developer/entity-forge
bash app.sh
```

Direct mode:
```bash
cd core/dashboard/streamlit_app
streamlit run app.py --server.address 0.0.0.0 --server.port 8000
```

## 14) Output Artifacts You Should Expect
Per run folder:
- `core/output/<timestamp>__<label>/`

Important files:
- `management_summary.md`
- `ground_truth_match_quality.md`
- `technical output/mapped_output.jsonl`
- `technical output/run_summary.json`
- `technical output/management_summary.json`
- `technical output/ground_truth_match_quality.json`
- `technical output/matched_pairs.csv`
- `technical output/entity_records.csv`
- `technical output/match_stats.csv`

Dashboard folder:
- `core/dashboard/index.html`
- `core/dashboard/management_dashboard_data.js`

## 15) Cleanup Procedure
Cleanup script:
- `core/app/cleanup_working_directory.py`

Purpose:
- removes generated runtime/output clutter
- preserves source JSON inputs

Example:
```bash
cd core
python3 app/cleanup_working_directory.py --runtime-dir /mnt/mvp_runtime
```

Dry run:
```bash
cd core
python3 app/cleanup_working_directory.py --runtime-dir /mnt/mvp_runtime --dry-run
```

## 16) Recommended Daily Operational Sequence
1. Set license env var (or ensure license file is present).
2. Run one-command production script:
   - `bash run_production_command.sh`
3. Check pipeline completion status.
4. Review diagnostics report if generated.
5. Open dashboard:
   - `core/dashboard/index.html`
6. If needed, rerun only dashboard build:
   - `python3 app/build_management_dashboard.py`

## 17) Known Limitations
- Runtime for ~1M records can still be long in constrained environments.
- Throughput varies by data shape and contention hot spots.
- Conservative settings prioritize stability over speed.

## 18) Change Control Note
For production reliability, prefer changing one parameter at a time:
- `LOAD_FILE_TIMEOUT_SECONDS`
- `--load-batch-size`
- `--load-chunk-size`
- `--max-failed-files`

Record each change in run notes together with resulting runtime and failure profile.

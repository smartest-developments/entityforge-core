# Core Pipeline

`core/` is the production-facing area of the repository. It contains:

- executable pipeline scripts
- dashboard templates
- validation tests
- runbooks and context docs
- generated runtime artifacts under `runtime/`

## Core files

- `app/generate_sample_inputs.py`: generates `sample_input/one_million_stress.jsonl`
- `app/run_mvp_pipeline.py`: source -> mapped JSONL -> Senzing E2E -> management outputs
- `app/build_management_dashboard.py`: rebuilds static dashboard data + automated checks
- `app/verify_dashboard_metrics.py`: cross-checks dashboard KPIs vs technical artifacts
- `app/record_cluster_exports.py`: single CLI for `record_id,cluster_id` and truthset key CSV exports
- `testing/`: full automated KPI validation suite
- `dashboard/`: versioned dashboard template/assets only
- `run_production_command.sh`: one-command production wrapper
- `run_existing_project_audit.sh`: manual audit helper for already-loaded projects

## App layout

Top-level `app/` should stay focused on active production logic and a small set of
operator-facing utilities.

Current active areas:

- pipeline orchestration: `run_mvp_pipeline.py`, `run_mvp_with_auto_diagnosis.py`, `run_senzing_end_to_end.py`
- mapping/input prep: `partner_json_to_senzing.py`, `create_limited_input.py`, `record_cluster_exports.py`
- reporting: `build_management_dashboard.py`, `verify_dashboard_metrics.py`
- audit/non-match analysis: `prepare_senzing_audit_inputs.py`, `build_non_match_why_report.py`, `run_non_match_why_helper.py`
- diagnostics/utilities: `diagnose_senzing_runtime.py`, `cleanup_working_directory.py`, `generate_sample_inputs.py`

Lower-priority or historical utilities live under:

- `app/legacy/`

For a fast operational overview, also read:

- `documentation/CORE_CONTEXT_SPEC.md`
- `documentation/PRODUCTION_RUNBOOK.md`

## Production command

```bash
cd core
./run_production_command.sh
```

Optional first-record cap for smoke/full-flow validation:

```bash
cd core
INPUT_RECORD_LIMIT=10000 ./run_production_command.sh
```

## Runtime output location

Final outputs for a specific execution live under:

```text
core/runtime/runs/<run_id>/output_bundle/
```

Typical contents:

- `technical output/`
- `dashboard_web/`
- `dashboard_streamlit_app/`
- `senzing_audit/`
- `non_match_why/`
- `diagnostics/`
- `limited_inputs/` when a capped run was used

The repository-level `dashboard/` directory is not the canonical destination for run outputs.

## Optional Streamlit dashboard

Each run now includes its own ready-to-open Streamlit bundle under:

- `runtime/runs/<run_id>/output_bundle/dashboard_streamlit_app/`

Template source remains in:

- `dashboard/streamlit_app/app.py`

Run:

```bash
python3 -m pip install -r dashboard/streamlit_app/requirements.txt
streamlit run dashboard/streamlit_app/app.py
```

## Generate the 1M stress sample

```bash
cd core
python3 app/generate_sample_inputs.py --records 1000000 --clean-legacy-samples
```

Generated local files (not committed):
- `sample_input/one_million_stress.jsonl`
- `sample_input/one_million_stress.metadata.json`

The dataset includes:
- `SOURCE_TRUE_GROUP_ID` (ground truth)
- noisy/partial `IPG ID` labels (to create baseline FP/FN pressure)
- mixed PERSON/ORGANIZATION
- sparse/noisy/duplicate-style scenarios

## Run pipeline on the sample

```bash
cd core
python3 app/run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --execution-mode auto
```

Large-run safety defaults are now automatic when input size is large (>= 300k rows):
- extended step timeout
- lower thread pressure
- `sz_file_loader` primary run with `--no-shuffle` to reduce temporary disk churn
- `sz_export` streaming mode (avoids writing a large standalone export CSV)
- preflight disk visibility in runtime metadata

Useful flags:

```bash
# fail fast if free disk is below recommendation
python3 app/run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --strict-preflight

# override large-run tuning defaults
python3 app/run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --disable-large-run-tuning \
  --step-timeout-seconds 7200 \
  --load-threads 2
```

If runs above ~500k fail intermittently, the common causes are:
- Docker amd64 emulation on ARM hosts (significant slowdown)
- timeout too short for `sz_file_loader`/`sz_snapshot`
- low free disk on the mounted runtime/output filesystem

## Senzing license (local, never committed)

Put your license only in local secret paths, for example:
- `core/.secrets/g2.lic_base64`

The repository ignores `*.lic`, `*.lic_base64`, `.secrets/`, and `license/` paths.

Pipeline auto-detection order:
1. `--license-base64-file <path>`
2. env `SENZING_LICENSE_BASE64_FILE`

## Production audit inputs for Senzing

When you need to compare your production clustering against a Senzing snapshot audit flow:

```bash
cd core
python3 app/prepare_senzing_audit_inputs.py \
  /path/to/production_input.jsonl \
  --data-source PARTNERS \
  --output-dir /path/to/audit_package \
  --project-dir /path/to/senzing_project
```

This creates:
- `record_id_cluster_id.csv`
- `truthset_key.csv`
- `truthset_snapshot.csv` and `truthset_snapshot.json` via `sz_snapshot -A`
- `truthset_audit.csv` and `truthset_audit.json` via `sz_audit`

Shell wrapper version:

```bash
cd core
PROJECT_DIR=/path/to/senzing_project \
OUTPUT_DIR=/path/to/audit_package \
./run_existing_project_audit.sh
```

If run metadata is available, `INPUT_JSON` can be auto-discovered from `PROJECT_DIR`.
Otherwise pass it explicitly:

```bash
cd core
INPUT_JSON=/path/to/production_input.jsonl \
PROJECT_DIR=/path/to/senzing_project \
OUTPUT_DIR=/path/to/audit_package \
./run_existing_project_audit.sh
```

If the snapshot already exists, reuse it:

```bash
python3 app/prepare_senzing_audit_inputs.py \
  /path/to/production_input.jsonl \
  --data-source PARTNERS \
  --output-dir /path/to/audit_package \
  --snapshot-csv /path/to/truthset_snapshot.csv \
  --audit-bin /path/to/sz_audit
```

Shell wrapper with existing snapshot:

```bash
cd core
INPUT_JSON=/path/to/production_input.jsonl \
SNAPSHOT_CSV=/path/to/truthset_snapshot.csv \
AUDIT_BIN=/path/to/sz_audit \
OUTPUT_DIR=/path/to/audit_package \
./run_existing_project_audit.sh
```
3. `core/.secrets/g2.lic_base64`
4. `core/license/g2.lic_base64`

The runtime injects this value as `LICENSESTRINGBASE64` in Senzing engine config.

## Dashboard and validation

After each production run, the pipeline builds a run-local dashboard bundle and validates it automatically.

It also produces:

- `senzing_audit/` for truth-set comparison against Senzing
- `non_match_why/` for readable analysis of records expected to match but split by Senzing

Manual dashboard rebuilds are still possible for development, but the production path should go through `run_production_command.sh`.

## Test commands

```bash
cd core
python3 testing/run_dashboard_tests.py
python3 app/verify_dashboard_metrics.py
```

Enable strict snapshot regression checks:

```bash
cd core
MVP_ENFORCE_REGRESSION_SNAPSHOT=1 python3 testing/run_dashboard_tests.py
```

## Runtime failure diagnostics (production-safe)

When `run_mvp_pipeline.py` fails (for example at `load_records`), run:

```bash
cd core
python3 app/diagnose_senzing_runtime.py --runtime-dir /mnt/runtime --search-dirs /mnt,/tmp,.
```

This generates diagnostics intended to be kept with the run under `runtime/runs/<run_id>/output_bundle/diagnostics/`.

The `.txt` file contains a compact copy/paste block for engineering/support escalation.

### One-command production run + diagnostics

Use this wrapper when operators must avoid manual troubleshooting steps:

```bash
cd core
python3 app/run_mvp_with_auto_diagnosis.py \
  --input-json /mnt/Senzing-Ready.json \
  --senzing-env /opt/senzing/er/resources/templates/setupEnv \
  --runtime-dir /mnt/runtime
```

This command:
1. Runs `run_mvp_pipeline.py` with conservative load settings.
2. If standard load retries fail, automatically enables sequential chunked load fallback (no record removal).
3. If the run still fails, automatically runs `diagnose_senzing_runtime.py`.
4. Prints a compact `COPY THIS BLOCK` summary for escalation.

By default it does **not** remove or filter records.

## Guardrails

- do not commit generated run outputs
- do not commit dashboard runtime payloads
- do not commit local license files
- keep production run deliverables together under the run-local `output_bundle/`

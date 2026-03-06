# MVP Pipeline (One-Million Mode)

This MVP is now focused on a **single high-volume stress dataset**:
- one sample
- default size: **1,000,000 rows**
- objective: challenge both our baseline and the Senzing engine under heavy, noisy conditions.

## Core files

- `generate_sample_inputs.py`: generates `sample_input/one_million_stress.jsonl`
- `run_mvp_pipeline.py`: source -> mapped JSONL -> Senzing E2E -> management outputs
- `build_management_dashboard.py`: rebuilds static dashboard data + automated checks
- `verify_dashboard_metrics.py`: cross-checks dashboard KPIs vs technical artifacts
- `testing/`: full automated KPI validation suite
- `presentation/`: minimal offline bundle for business presentation (`index.html`)

## Final results (offline, no server)

If you only need to present final numbers/graphs, use:

- `presentation/index.html` (double-click to open)

The `presentation/` folder is intentionally self-contained:
- dashboard HTML/CSS/JS
- UI libraries
- embedded final data (`management_dashboard_data.js`)

## Generate the 1M stress sample

```bash
cd MVP
python3 generate_sample_inputs.py --records 1000000 --clean-legacy-samples
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
cd MVP
python3 run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --execution-mode auto
```

Large-run safety defaults are now automatic when input size is large (>= 300k rows):
- extended step timeout
- lower thread pressure
- `sz_file_loader` primary run with `--no-shuffle` to reduce temporary disk churn
- `sz_export` streaming mode (avoids writing a large standalone export CSV)
- preflight disk visibility in runtime metadata

Default lightweight mode now skips:
- snapshot
- explain/why

Enable snapshot only when needed:

```bash
python3 run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --with-snapshot
```

Useful flags:

```bash
# fail fast if free disk is below recommendation
python3 run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --strict-preflight

# override large-run tuning defaults
python3 run_mvp_pipeline.py \
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
- `MVP/.secrets/g2.lic_base64`

The repository ignores `*.lic`, `*.lic_base64`, `.secrets/`, and `license/` paths.

Pipeline auto-detection order:
1. `--license-base64-file <path>`
2. env `SENZING_LICENSE_BASE64_FILE`
3. `MVP/.secrets/g2.lic_base64`
4. `MVP/license/g2.lic_base64`

The runtime injects this value as `LICENSESTRINGBASE64` in Senzing engine config.

## Dashboard and validation

After each pipeline run, dashboard rebuild runs automatically and enforces:
1. `testing/run_dashboard_tests.py`
2. `verify_dashboard_metrics.py`

If any check fails, the process exits with non-zero status.

Manual run:

```bash
cd MVP
python3 build_management_dashboard.py
```

Skip checks only for debug:

```bash
python3 build_management_dashboard.py --skip-tests --skip-audit
```

## Test commands

```bash
cd MVP
python3 testing/run_dashboard_tests.py
python3 verify_dashboard_metrics.py
```

Enable strict snapshot regression checks:

```bash
cd MVP
MVP_ENFORCE_REGRESSION_SNAPSHOT=1 python3 testing/run_dashboard_tests.py
```

## Runtime failure diagnostics (production-safe)

When `run_mvp_pipeline.py` fails (for example at `load_records`), run:

```bash
cd MVP
python3 diagnose_senzing_runtime.py --runtime-dir /mnt/mvp_runtime --search-dirs /mnt,/tmp,.
```

This generates:
- `output/diagnostics/runtime_diagnostic_<timestamp>.json`
- `output/diagnostics/runtime_diagnostic_<timestamp>.md`
- `output/diagnostics/runtime_diagnostic_<timestamp>.txt`

The `.txt` file contains a compact copy/paste block for engineering/support escalation.

### One-command production run + diagnostics

Use this wrapper when operators must avoid manual troubleshooting steps:

```bash
cd MVP
python3 run_mvp_with_auto_diagnosis.py \
  --input-json /mnt/Senzing-Ready.json \
  --senzing-env /opt/senzing/er/resources/templates/setupEnv \
  --runtime-dir /mnt/mvp_runtime
```

This command:
1. Runs `run_mvp_pipeline.py` with conservative load settings.
2. If standard load retries fail, automatically enables sequential chunked load fallback (no record removal).
3. If the run still fails, automatically runs `diagnose_senzing_runtime.py`.
4. Prints a compact `COPY THIS BLOCK` summary for escalation.

By default it does **not** remove or filter records.

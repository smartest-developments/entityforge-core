# Production Runbook

## Scope

This runbook covers the current one-command production flow in `core/`.

## Primary Command

From `core/`:

```bash
./run_production_command.sh
```

Optional smoke/full-flow validation on the first records of the real production file:

```bash
INPUT_RECORD_LIMIT=10000 ./run_production_command.sh
```

## Current Execution Profile

The production wrapper currently aims for resilient completion, not fragile peak speed:

- primary load threads: `3`
- automatic fallback threads: `2`, then `1`
- shuffle: enabled
- proactive load file size: `1000`
- fallback chunk size: `100`
- per-load-file timeout: `180` seconds
- snapshot enabled
- audit generation enabled at the end of the run

## Runtime Layout

Generated run deliverables live under:

```text
core/runtime/runs/<run_id>/output_bundle/
```

Expected subfolders:

- `technical output/`
- `dashboard_web/`
- `dashboard_streamlit_app/`
- `senzing_audit/`
- `diagnostics/` when diagnostics were generated
- `limited_inputs/` when `INPUT_RECORD_LIMIT` was used

## What The Production Wrapper Does

`run_production_command.sh` performs:

1. optional creation of a reduced input file
2. full pipeline execution through `app/run_mvp_with_auto_diagnosis.py`
3. automatic run discovery inside `runtime/runs/`
4. automatic audit package generation from the same `mapped_output.jsonl`
5. cleanup of temporary staging folders

## Audit Package Contents

Inside `senzing_audit/` expect:

- `record_id_cluster_id.csv`
- `truthset_key.csv`
- `truthset_snapshot.csv`
- `truthset_snapshot.json`
- `truthset_audit.csv`
- `truthset_audit.json`
- `audit_manifest.json`
- `README.md`

## Dashboard Outputs

Each run has its own dashboard bundle:

- static web bundle in `dashboard_web/`
- Streamlit-ready bundle in `dashboard_streamlit_app/`

The repository-level `core/dashboard/` folder is template/source material, not the final destination of run-specific dashboard payloads.

## Local Secrets

Keep the Senzing license local only, for example:

- `core/.secrets/g2.lic_base64`

Do not commit the license file.

## Troubleshooting

If the core pipeline completes but the audit package is incomplete:

- inspect `technical output/run_summary.json`
- verify `project_dir` points to the expected runtime project
- verify the run-local `bin/sz_snapshot` works with the project `setupEnv`

If a run is intentionally capped with `INPUT_RECORD_LIMIT`, the reduced input should be preserved in:

- `output_bundle/limited_inputs/`

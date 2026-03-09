# Entity Forge

Entity Forge is a Python-based evaluation and reporting stack for large-scale entity resolution workflows built around Senzing.

## Current focus

The repository is currently organized around the production-facing `core/` workflow:

- generate or ingest large partner-style datasets
- map source records into Senzing-ready JSONL
- run end-to-end Senzing processing with large-run safeguards
- build an offline management dashboard
- validate dashboard KPIs against raw technical artifacts

Start here:

- `core/README.md`

## Repository layout

- `core/`: main pipeline, dashboard, tests, technical/business documentation
- `S3Z/`: reusable Senzing tools, workflows, prompts, and references
- `project_meta/`: project metadata, changelog, contribution docs, and legacy docs

## Common entry points

Generate the default one-million-row stress sample:

```bash
cd core
python3 app/generate_sample_inputs.py --records 1000000 --clean-legacy-samples
```

Run the main pipeline:

```bash
cd core
python3 app/run_mvp_pipeline.py \
  --input-json sample_input/one_million_stress.jsonl \
  --execution-mode auto
```

Rebuild the dashboard:

```bash
cd core
python3 app/build_management_dashboard.py
```

Run dashboard validation:

```bash
cd core
python3 testing/run_dashboard_tests.py
python3 app/verify_dashboard_metrics.py
```

## Notes

- Local Senzing license files and secrets are intentionally ignored and never committed.
- The repository name has been updated to `entity-forge`, while some historical artifacts may still reference earlier internal naming.

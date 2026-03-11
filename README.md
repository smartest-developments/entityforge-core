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
- `project_meta/REPOSITORY_CONTEXT_SPEC.md`
- `project_meta/REPOSITORY_GUARDRAILS.md`

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
./run_production_command.sh
```

Run only the first 10,000 records of the production file:

```bash
cd core
INPUT_RECORD_LIMIT=10000 ./run_production_command.sh
```

## Runtime layout

Run-specific generated artifacts are intended to live under:

- `core/runtime/runs/<run_id>/output_bundle/`

This bundle contains technical output, dashboards, diagnostics, and Senzing audit files for that run.

Repository-global generated outputs should not be committed.

## Validation and diagnostics

Manual dashboard validation:

```bash
cd core
python3 testing/run_dashboard_tests.py
python3 app/verify_dashboard_metrics.py
```

## Notes

- Local Senzing license files and secrets are intentionally ignored and never committed.
- The repository name has been updated to `entity-forge`, while some historical artifacts may still reference earlier internal naming.
- For fast repository orientation, see `project_meta/REPOSITORY_CONTEXT_SPEC.md`, `project_meta/REPOSITORY_GUARDRAILS.md`, `core/documentation/CORE_CONTEXT_SPEC.md`, and `S3Z/reference/S3Z_CONTEXT_SPEC.md`.

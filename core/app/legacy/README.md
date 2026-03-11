Legacy utilities that are not part of the main production flow.

Files here are kept for reference or occasional operator use, but they are not
the primary entrypoints for:

- production runs
- audit generation
- dashboard validation
- non-match WHY analysis

Current legacy contents:

- `dashboard_single_csv_tool.py`: pack/unpack dashboard CSV bundles for manual sharing/rebuild scenarios
- `run_samples_batch.py`: batch runner for multiple local sample inputs

If a legacy script becomes operationally important again, move it back into the
top-level `core/app/` area and document it in `core/README.md`.

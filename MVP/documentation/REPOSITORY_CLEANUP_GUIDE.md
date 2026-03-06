# Repository Cleanup Guide

## Objective

Keep the repository practical for day-to-day usage while preserving the ability to present final results immediately.

Primary target:
- open `MVP/presentation/index.html` directly (double-click)
- view final dashboard with data and styling

## What Must Stay For Final Presentation

Required folder:
- `MVP/presentation/`

Required files inside:
- `index.html`
- `management_dashboard.html`
- `management_dashboard.css`
- `management_dashboard.js`
- `management_dashboard_data.js`
- `tabler.min.css`
- `tabler.min.js`
- `chart.umd.js`

## What Is Runtime/Engineering Scope (Not Needed To Just View Final Results)

Inside `MVP`:
- pipeline scripts (`run_mvp_pipeline.py`, `run_senzing_end_to_end.py`, ...)
- mapping/diagnostic scripts
- `output/` generated artifacts
- `testing/` validation suite

Outside `MVP`:
- top-level `docs/` and `senzing/` are support/reference assets for development
- governance/project files (`LICENSE`, `CONTRIBUTING.md`, `.github/*`, etc.) are repository standard metadata

## Current Organization Decision

- Business-facing artifacts are consolidated under `MVP/documentation/`.
- Final offline dashboard is consolidated under `MVP/presentation/`.
- Production/runtime generated files should not be committed.

## Recommended Cleanup Routine (Local)

From `MVP`:

```bash
python3 cleanup_working_directory.py --runtime-dir /mnt/mvp_runtime
```

This removes generated clutter and preserves source scripts + input JSON.

## Validation Before Sharing

Run:

```bash
cd MVP
python3 testing/run_dashboard_tests.py
python3 verify_dashboard_metrics.py
```

Then verify final bundle manually:
- open `MVP/presentation/index.html`
- check metrics cards, both entity charts, and top match keys

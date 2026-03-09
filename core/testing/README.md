# Core Dashboard Testing

This folder contains the automated Python test suite that validates dashboard KPI correctness against raw technical artifacts.

## What is validated

- Counts from files (`input_normalized.jsonl`, `matched_pairs.csv`, `entity_records.csv`)
- Confusion matrix metrics (`true_positive`, `false_positive`, `false_negative`, `predicted_pairs_labeled`)
- KPI formulas (`Match Found`, `False Positive %`, `Miss-Matched`-related calculations)
- Baseline metrics (`our_true_positive`, `our_false_positive`, `our_false_negative`, coverage)
- Extra discovery metrics (`extra_true_matches_found`, `extra_false_matches_found`, `extra_gain_vs_known_pct`)
- Entity size distribution integrity and consistency with entity totals
- Dashboard global summary consistency
- Synthetic sample coverage (presence of FP/FN cases in generated stress samples)
- Aggregate and contract checks (payload schema, distributions, paths, summary invariants)
- Cross-tool consistency (`testing` suite vs `verify_dashboard_metrics.py`)
- Failure-mode robustness tests for parser/helpers (invalid JS/JSON, missing files, bad distributions)
- Optional regression snapshot checks on latest run per source

## Run manually

```bash
cd core
python3 testing/run_dashboard_tests.py
```

Optional paths:

```bash
python3 testing/run_dashboard_tests.py \
  --output-root output \
  --dashboard-data dashboard/management_dashboard_data.js
```

Generate/update regression snapshot baseline:

```bash
python3 testing/generate_dashboard_snapshot.py
```

Enable strict snapshot regression checks:

```bash
MVP_ENFORCE_REGRESSION_SNAPSHOT=1 python3 testing/run_dashboard_tests.py
```

## Reports generated

- `dashboard/dashboard_test_suite_report.json`
- `dashboard/dashboard_test_suite_report.md`
- `testing/snapshots/dashboard_regression_snapshot.json` (generated baseline for optional regression lock)

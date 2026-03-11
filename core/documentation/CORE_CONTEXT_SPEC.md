# Core Context Spec

## What `core/` Is

`core/` is the operational pipeline used to evaluate Senzing on large, noisy partner-style datasets and publish validated management metrics.

It is optimized for:

- large input sizes,
- unstable or constrained runtimes,
- traceable outputs,
- dashboard correctness.

## Core Workflow

The normal flow is:

1. generate or ingest source input,
2. map source records to Senzing-ready JSONL,
3. run Senzing end-to-end,
4. build comparison artifacts,
5. rebuild dashboard data,
6. run dashboard tests,
7. audit KPI values against technical files.

## Main Entry Points

### Dataset generation

- `app/generate_sample_inputs.py`

Generates the default stress dataset, usually around one million rows, with:

- `SOURCE_TRUE_GROUP_ID` for hidden truth,
- partial/noisy `IPG ID`,
- mixed person/organization records,
- sparse and noisy matching scenarios.

### Main orchestrator

- `app/run_mvp_pipeline.py`

This is the primary source-to-output pipeline.

It is responsible for:

- input parsing with encoding fallback,
- mapper execution,
- large-run auto-tuning,
- runtime/output bundle management,
- per-run dashboard generation after the run,
- artifact copying into final `output/`.

### Senzing engine runner

- `app/run_senzing_end_to_end.py`

This is the heaviest runtime component.

It handles:

- isolated project creation,
- data source configuration,
- load attempts and retries,
- split-file loading,
- chunk fallback,
- timeout handling,
- snapshot/export,
- explain calls through SDK,
- comparison file generation,
- ground-truth quality reports,
- run registry updates.

### Production wrapper

- `app/run_mvp_with_auto_diagnosis.py`

Use this when the operator should have one command with automatic diagnostics on failure.

### Diagnostics

- `app/diagnose_senzing_runtime.py`

Used after failure to inspect logs, loader errors, core dumps, mapped JSONL shape, and likely root causes.

### Dashboard build and checks

- `app/build_management_dashboard.py`
- `app/verify_dashboard_metrics.py`
- `testing/run_dashboard_tests.py`

These are release gates for reporting correctness.

## Metric Semantics

Dashboard metrics compare two views:

- `Our`: baseline/internal grouping inferred from source labels, mainly `SOURCE_IPG_ID`
- `Their`: Senzing resolved output

Important derived values include:

- matched pairs,
- entity counts,
- pair precision/recall,
- false positive and false negative counts,
- entity size distributions,
- extra true matches found beyond known labels.

## Source Of Truth Inside `core/`

Prefer this order when understanding behavior:

1. `app/run_mvp_pipeline.py`
2. `app/run_senzing_end_to_end.py`
3. `app/build_management_dashboard.py`
4. `testing/dashboard_assertions.py`
5. `README.md`
6. `documentation/*.md`

## Non-Obvious Design Decisions

### Large runs are the default design target

The code assumes that 300k+ and 1M-row workloads are normal, not edge cases.

### Reliability is preferred over raw speed

The pipeline includes:

- lower thread fallbacks,
- no-shuffle load mode,
- chunked retry,
- proactive file splitting,
- per-file timeout,
- continue-on-failure options,
- auto-diagnostics.

### Reporting must be defendable

Dashboard output is not trusted by default.
It is rebuilt and then checked against:

- raw CSV counts,
- JSON summaries,
- recomputed formulas,
- regression snapshots when enabled.

## Folder Roles

### `app/`

Execution scripts and operational utilities.

### `dashboard/`

Versioned dashboard templates and static assets used to build per-run dashboard bundles.

### `testing/`

Automated correctness checks and helper assertions.

### `documentation/`

Operational and business-facing documents for the active `core` workflow.

### `runtime/`

Generated run artifacts only. The canonical final location is:

- `runtime/runs/<run_id>/output_bundle/`

## Read This Before Editing

If a change affects any of the following, review both implementation and validation:

- record counting,
- entity counting,
- match quality formulas,
- dashboard payload shape,
- run folder artifact names,
- stream export mode,
- split-file load behavior.

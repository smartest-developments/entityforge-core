# Repository Context Spec

## Purpose

This repository is a Python-based evaluation and reporting stack for entity resolution workflows built around Senzing.

The current practical goal is not generic product development. It is:

1. prepare or generate partner-style source datasets,
2. map them into Senzing-ready JSONL,
3. run Senzing end-to-end with operational safeguards,
4. produce technical and management-facing artifacts,
5. validate that dashboard KPIs match raw run outputs.

## Repository Areas

### `core/`

This is the active, production-facing area of the repository.

Use this folder first when the task is about:

- the main pipeline,
- runtime stability,
- output artifacts,
- dashboard generation,
- KPI verification,
- production execution.

Primary entry points:

- `core/app/run_mvp_pipeline.py`
- `core/app/run_mvp_with_auto_diagnosis.py`
- `core/app/build_management_dashboard.py`
- `core/app/verify_dashboard_metrics.py`

### `S3Z/`

This contains reusable Senzing tooling, references, prompts, and older workflow wrappers.

Use this area when the task is about:

- standalone mapping utilities,
- Senzing helper tools,
- workshop/reference material,
- reusable workflow components outside the main `core/` path.

Important note:

- parts of `S3Z/` still reflect earlier repository layouts and wrapper conventions;
- for current production behavior, `core/` is the source of truth.

### `project_meta/`

This folder contains metadata and supporting project documentation:

- changelog,
- contribution docs,
- security/license files,
- legacy docs moved out of the main execution path.

## Source Of Truth

When documentation or wrapper behavior appears duplicated, prefer this order:

1. `core/app/*.py`
2. `core/README.md`
3. `core/documentation/*.md`
4. `S3Z/` tools and workflow wrappers
5. `project_meta/docs_legacy/`

## Actual Runtime Flow

The active pipeline is:

1. source JSON or JSONL input,
2. mapping to Senzing-ready JSONL,
3. Senzing project creation and load,
4. export/comparison artifact generation,
5. management dashboard rebuild,
6. automated dashboard test suite,
7. metric audit against raw artifacts.

## Main Outputs

Primary generated outputs live under:

- `core/runtime/runs/<run_id>/output_bundle/`
- `core/runtime/runs/<run_id>/output_bundle/dashboard_web/`
- `core/runtime/runs/<run_id>/output_bundle/dashboard_streamlit_app/`
- `core/runtime/runs/<run_id>/output_bundle/senzing_audit/`

Typical per-run artifacts:

- copied source input,
- mapped JSONL,
- run summary,
- management summary,
- ground truth match quality report,
- `matched_pairs.csv`,
- `entity_records.csv`,
- per-run diagnostics when generated.

## Working Guidance

When changing behavior:

- treat `core/` as canonical,
- preserve dashboard/tests/audit alignment,
- assume high-volume runs are a first-class requirement,
- do not remove resilience features unless the change explicitly replaces them.

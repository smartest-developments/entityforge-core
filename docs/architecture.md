# Architecture

## High-level structure

- `core/`
  - active pipeline, runtime wrappers, dashboard templates, tests, documentation
- `S3Z/`
  - reusable Senzing tools and older workflow material
- `project_meta/`
  - repository-level metadata, context, and legacy docs

## Core execution path

```text
input JSON/JSONL
  -> partner_json_to_senzing.py
  -> mapped_output.jsonl
  -> run_senzing_end_to_end.py
  -> technical artifacts
  -> build_management_dashboard.py
  -> prepare_senzing_audit_inputs.py
  -> build_non_match_why_report.py
```

## Runtime model

- `core/run_production_command.sh` is the operator entrypoint.
- It stages optional limited input data.
- It delegates to `core/app/run_mvp_with_auto_diagnosis.py`.
- The pipeline writes final deliverables under `<RUNTIME_DIR>/runs/<run_id>/output_bundle/`.
- In production, `RUNTIME_DIR` defaults to `/mnt/runtime`.
- Repository-local `core/runtime_smoke*` and `core/runtime_demo_*` directories are example/smoke artifacts, not the production default.

## Validation model

- `core/testing/run_dashboard_tests.py`
- `core/app/verify_dashboard_metrics.py`
- `scripts/validate.sh` for repository-level checks

## Design constraints

- per-run outputs must stay co-located
- generated runtime artifacts are not source files
- Docker and local runtime modes both exist; scripts must not assume one mode blindly
- Senzing-specific behavior belongs in `core/app/`
- repository validation must not assume a package manager or root virtualenv that the repo does not define

## Architectural risks

- historical path drift between legacy docs and current runtime layout
- environment-sensitive behavior for Senzing SDK and CLI tools
- generated dashboard payloads can be mistaken for source if not ignored

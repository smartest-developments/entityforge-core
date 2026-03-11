# Repository Guardrails

## Purpose

This file defines the minimum maintenance rules for this repository so that it stays understandable and safe to operate even after large AI-assisted changes.

## Canonical Repository Shape

At the root level, the repository should remain simple:

- `core/`: active production-facing pipeline
- `S3Z/`: reusable Senzing tools and older workflow material
- `project_meta/`: repository-level context, guardrails, and legacy/meta docs

Inside `core/`, the stable areas are:

- `app/`: executable scripts and pipeline logic
- `dashboard/`: versioned dashboard templates and static assets only
- `documentation/`: operational specs and runbooks
- `testing/`: validation suite
- `runtime/`: generated run artifacts only, never committed
- shell entrypoints such as `run_production_command.sh`

## Never Commit These

- Senzing license files
- `.secrets/` content
- generated run outputs
- generated dashboard payloads
- diagnostics produced by a specific execution
- temporary loader files

Even in a private repository, secrets stay local.

## Source Of Truth Order

When code and docs disagree, use this order:

1. `core/app/*.py`
2. `core/run_production_command.sh`
3. `core/README.md`
4. `core/documentation/*.md`
5. repository-level context in `project_meta/`

## Run Output Rules

Generated artifacts for one execution must stay together under the runtime run folder:

- `core/runtime/runs/<run_id>/output_bundle/technical output/`
- `core/runtime/runs/<run_id>/output_bundle/dashboard_web/`
- `core/runtime/runs/<run_id>/output_bundle/dashboard_streamlit_app/`
- `core/runtime/runs/<run_id>/output_bundle/senzing_audit/`
- `core/runtime/runs/<run_id>/output_bundle/diagnostics/`
- `core/runtime/runs/<run_id>/output_bundle/limited_inputs/` when a capped input was used

Do not write final run deliverables to repository-global folders.

## Documentation Minimum Set

The repository should always retain:

- a root `README.md`
- a `core/README.md`
- repository context spec
- core context spec
- at least one production runbook
- at least one guardrail document

## Change Discipline

When changing runtime behavior, update in the same change set:

- operator-facing README instructions
- output location documentation
- any new environment variables or defaults
- any assumptions about secrets, paths, or generated artifacts

## Review Checklist

Before considering a structural change complete, verify:

- generated artifacts are ignored by Git
- docs point to the current runtime layout
- dashboards are generated per run, not globally
- audit output location is documented
- production commands are still one-command usable

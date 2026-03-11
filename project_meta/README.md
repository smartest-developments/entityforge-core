# Entity Forge

Repository for Senzing mapping and core evaluation workflows.

## Current operating model

Primary execution target is now:
- `core/` in **one-million-row mode**
- single stress sample input
- dashboard + automated KPI validation gates

Start from:
- `core/README.md`
- `project_meta/REPOSITORY_CONTEXT_SPEC.md`
- `project_meta/REPOSITORY_GUARDRAILS.md`

## Repository areas

- `core/`: production-facing pipeline, dashboard, tests
- `S3Z/`: reusable Senzing tools/workflows/reference material
- `project_meta/docs_legacy/`: legacy documentation moved from previous root layout

## Notes

Local license/secrets are never committed. Paths like `.secrets/`, `license/`, `*.lic`, `*.lic_base64` are ignored.

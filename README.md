# mapper-ai-main

Repository for Senzing mapping and MVP evaluation workflows.

## Current operating model

Primary execution target is now:
- `MVP/` in **one-million-row mode**
- single stress sample input
- dashboard + automated KPI validation gates

Start from:
- `MVP/README.md`

## Repository areas

- `MVP/`: production-facing pipeline, dashboard, tests
- `senzing/`: reusable Senzing tools/workflows/reference material
- `docs/`: project documentation

## Notes

Local license/secrets are never committed. Paths like `.secrets/`, `license/`, `*.lic`, `*.lic_base64` are ignored.

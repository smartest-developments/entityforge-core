# Architecture Rules

- Treat `core/` as the implementation source of truth.
- Keep final run outputs under `<RUNTIME_DIR>/runs/<run_id>/output_bundle/`, not under ad-hoc repository-global folders.
- Do not reintroduce repository-global final output locations for per-run deliverables.
- Keep dashboard generation run-local for production flows.
- Keep audit and non-match analysis tied to the same run that produced the mapped input and project.
- Do not move logic from `core/app/` into ad-hoc shell scripts unless there is a clear operational need.
- If touching legacy areas such as `S3Z/`, state whether the change affects active production behavior or only reference tooling.

# AGENTS.md

Mandatory entry point for Codex work in this repository.

## Required reading order

Before making changes, read in this order:

1. `core/README.md`
2. `core/documentation/CORE_CONTEXT_SPEC.md`
3. `core/documentation/PRODUCTION_RUNBOOK.md`
4. `project_meta/REPOSITORY_CONTEXT_SPEC.md`
5. `project_meta/REPOSITORY_GUARDRAILS.md`
6. `docs/specifications.md`
7. `docs/requirements.md`
8. `docs/architecture.md`
9. `guardrails/*.md`

Do not skip the `core/` documentation. It is the source of truth for runtime behavior.

If documentation conflicts with executable code under `core/app/` or `core/*.sh`, treat the current code as authoritative and update the documentation in the same change.

## Working rules

- Keep changes minimal, scoped, and reversible.
- Do not make unrelated edits while touching a file.
- Prefer `core/` as the canonical implementation area.
- Treat generated outputs under configured runtime roots such as `core/runtime*`, `/mnt/runtime`, `core/output/`, `core/dashboard/*.json`, and similar artifacts as non-source material unless the task is explicitly about them.
- Do not commit secrets, licenses, `.secrets/`, or generated runtime data.
- If a path, command, or behavior is uncertain, mark it as an assumption or TODO instead of inventing certainty.
- Do not edit generated dashboards, runtime bundles, or smoke outputs to “fix” a bug in source code. Fix the generator instead.
- Before changing any shell wrapper, check the Python entrypoint it delegates to. Keep orchestration logic thin.

## Validation

Before completion, run:

```bash
./scripts/validate.sh
```

Do not claim completion if validation fails. If a validation step is skipped because prerequisites are missing, report that explicitly.

## Completion format

Every Codex completion must report:

- changed files
- commands run
- command outcomes
- assumptions
- unresolved gaps

If validation wrote reports into a run bundle, mention the exact output paths.

## Related governance files

- `docs/specifications.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `guardrails/coding-rules.md`
- `guardrails/architecture-rules.md`
- `guardrails/security-rules.md`
- `guardrails/forbidden-actions.md`
- `scripts/validate.sh`

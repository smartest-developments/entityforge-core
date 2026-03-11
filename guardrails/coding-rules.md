# Coding Rules

- Prefer small, scoped edits over broad refactors.
- Do not change behavior and documentation separately; update both when behavior changes.
- Reuse existing scripts in `core/app/` instead of duplicating logic in new wrappers.
- Keep new files ASCII unless the existing file clearly uses another encoding.
- Preserve current naming and file layout unless there is a concrete repository-level reason to change them.
- Avoid introducing new dependencies unless the repository already supports them or the task requires them.
- Mark assumptions and TODOs explicitly when behavior is not fully verified.

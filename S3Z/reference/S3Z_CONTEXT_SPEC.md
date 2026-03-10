# S3Z Context Spec

## What `S3Z/` Is

`S3Z/` is the reusable Senzing toolkit area of the repository.

It contains:

- helper tools,
- workflow wrappers,
- prompts,
- references and crosswalks,
- older end-to-end utility paths.

It is useful for experimentation, workshops, reusable scripts, and lower-level Senzing support work.

## What `S3Z/` Is Not

`S3Z/` is not the current production source of truth for the repository-wide pipeline.

For the active operational flow, prefer `core/`.

## Main Subfolders

### `tools/`

Reusable utilities such as:

- `partner_json_to_senzing.py`
- `lint_senzing_json.py`
- `sz_json_analyzer.py`
- `sz_schema_generator.py`
- `run_partner_mapping_pipeline.py`
- `run_sample_to_management.py`

These are useful when a task is about:

- mapper development,
- JSON validation,
- data analysis before loading,
- standalone report generation.

### `workflows/`

Organized wrappers by responsibility:

- `mapper/`
- `e2e_runner/`
- `testing/`

These wrap lower-level tools into a staged flow, but some wrappers still reflect older repository paths.

### `reference/`

Reference files, examples, and crosswalk material.

This is the right place for static specification-style context documents for `S3Z/`.

### `all_in_one/`

Older all-in-one execution scripts that influenced later `core/app` implementations.

## Relationship To `core/`

Conceptually:

- `S3Z/` is the toolkit and reference layer,
- `core/` is the active productized workflow layer.

Practically:

- some logic exists in both places,
- `core/app` versions are the ones to trust first for current behavior.

## When To Use `S3Z/`

Use `S3Z/` first when the task is:

- creating or adjusting mapping support tools,
- working on generic Senzing helper scripts,
- consulting examples or reference docs,
- running lightweight or workshop-oriented flows outside `core/`.

Use `core/` first when the task is:

- changing production pipeline behavior,
- changing dashboard outputs,
- changing test/audit behavior,
- debugging run outputs under `core/output/`.

## Known Caveat

Some wrappers in `S3Z/workflows` reference older `senzing/...` paths.
Treat those wrappers as convenience or legacy surfaces unless they are explicitly being repaired.

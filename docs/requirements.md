# Requirements

## Functional requirements

- A single production wrapper must be able to run the full pipeline from source input to run-local output bundle.
- Dashboard assets must be generated per run, not only globally.
- Senzing audit files must be generated from the same run inputs used for load.
- Non-match analysis must be generated from audit and snapshot outputs and placed inside the same run bundle.
- Validation tooling must exist for dashboard correctness.

## Operational requirements

- Large runs must prefer resilience over unsafe throughput.
- Load fallback must support thread degradation and chunk fallback.
- Diagnostics must be preservable with the corresponding run.
- Optional limited-input smoke runs must preserve the exact reduced input used.

## Repository requirements

- Secrets and licenses must remain local and uncommitted.
- Generated runtime outputs must stay out of version control.
- Repository guidance must point contributors to `core/` documentation first.
- Governance files must stay concise and reflect actual repository behavior.

## Validation requirements

At minimum, repository validation should check:

- shell syntax for primary scripts
- Python syntax/compilation for active application code
- dashboard validation commands when a run bundle is available anywhere under `core/`

## TODO / uncertainty

- There is no single repository-wide package manager entrypoint at the root. Validation therefore uses direct shell and Python commands already present in the repo.
- Some legacy documentation still references historical layouts; these should be treated as historical unless explicitly refreshed or matched by current code.

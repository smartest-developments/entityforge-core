# Local Senzing License Setup (Not Committed)

This repository must never store real Senzing license payloads in git.

## Recommended local path

Place your local license file in:

- `MVP/.secrets/g2.lic_base64`

Alternative local paths (also ignored):
- `MVP/license/`
- any `*.lic` or `*.lic_base64` under repository paths

## Rules

- Never commit license content.
- Never paste license content into tracked files.
- Keep license files only on local machine / secure secret stores.

## Runtime behavior

`run_mvp_pipeline.py` auto-loads the license string from:
1. `--license-base64-file`
2. env `SENZING_LICENSE_BASE64_FILE`
3. `MVP/.secrets/g2.lic_base64`
4. `MVP/license/g2.lic_base64`

Then it injects the value into Senzing config as `LICENSESTRINGBASE64`.

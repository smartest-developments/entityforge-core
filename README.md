# mapper toolkit

Toolkit for mapping source data to Senzing entity-resolution JSON format.

> Note: this toolkit is intended for development and validation workflows.

## What's Included

```text
senzing/
├── prompts/
│   └── senzing_mapping_assistant.md
├── reference/
│   ├── senzing_entity_specification.md
│   ├── senzing_mapping_examples.md
│   ├── identifier_crosswalk.json
│   └── usage_type_crosswalk.json
├── tools/
│   ├── sz_schema_generator.py
│   ├── lint_senzing_json.py
│   ├── sz_json_analyzer.py
│   ├── partner_json_to_senzing.py
│   ├── generate_realistic_partner_dataset.py
│   ├── run_sample_to_management.py
│   └── run_partner_mapping_pipeline.py
└── workflows/
    ├── mapper/
    ├── e2e_runner/
    └── testing/

sample/
└── partner_input_realistic_<records>_<timestamp>.json

output/
├── partner_output_senzing_<records>_<timestamp>.jsonl
├── field_map_<records>_<timestamp>.json
├── generation_summary_<records>_<timestamp>.json
└── run_registry.csv
```

## Main Workflows

1. Build Senzing-ready JSONL from source data:

```bash
python3 senzing/workflows/mapper/run_mapper_jsonl.py \
  /path/to/input.json \
  /path/to/output.jsonl \
  --data-source PARTNERS
```

2. Run Senzing end-to-end (project creation, load, export, explain, comparison):

```bash
python3 senzing/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/output.jsonl
```

For large runs (e.g. 500k), use performance mode:

```bash
python3 senzing/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/output.jsonl \
  --fast-mode \
  --use-input-jsonl-directly \
  --data-sources PARTNERS
```

3. Run automated management test cases on one run folder:

```bash
python3 senzing/workflows/testing/run_management_tests.py \
  /path/to/senzing_run_folder
```

4. Run one unified pipeline (map -> e2e -> management outputs):

```bash
python3 senzing/tools/run_sample_to_management.py --input-json /path/to/input.json
```

If you do not pass `--input-json`, it auto-generates a realistic sample:

```bash
python3 senzing/tools/run_sample_to_management.py --records 500
```

By default this command now cleans `--projects-root` at the end of each run to prevent disk growth.
If you need to inspect project internals for debugging, add `--keep-projects-root`.

If the input root is an object containing the array (example key: `records`):

```bash
python3 senzing/tools/run_sample_to_management.py \
  --input-json /path/to/input.json \
  --input-array-key records
```

5. Generate realistic source sample and map it to Senzing JSONL (500k default):

```bash
python3 senzing/tools/generate_realistic_partner_dataset.py --records 500000
```

This command writes:
- source-style input JSON to `sample/`
- mapped Senzing JSONL + field map + summary to `output/`
- timestamped filenames for every run

Each E2E run also appends one row to `output/run_registry.csv` with:
- run folder
- exact input JSONL used
- linked generation summary/base input (when available)
- key management output file paths

Generation defaults:
- `70%` PERSON, `30%` ORGANIZATION
- `IPG ID` present on `35%` of records
- always present source IDs:
  - `externalPartnerKeyDirExternalID`
  - `partnerKeyDirBusRelExternalID`

## Documentation

- `senzing/senzing_tools_reference.md`
- `docs/partner_json_to_senzing.md`
- `docs/management_reporting.md`
- `senzing/workflows/README.md`
- `MVP/README.md` (portable execution package for production handoff)

## Environment Setup

- Python 3.10+
- Access to Senzing CLI tools for load/export steps
- Git + SSH configuration for repository sync

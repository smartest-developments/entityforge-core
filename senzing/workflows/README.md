# Senzing Workflows (Organized)

This folder contains the three operational scripts separated by responsibility.

## Folders

- `mapper/`: Convert production JSON data into Senzing-ready JSONL.
- `e2e_runner/`: Create isolated Senzing project, load data, export, explain, comparison outputs.
- `testing/`: Run automated management test cases (10 tests) on one run directory.

## Typical End-to-End Usage

1. Build Senzing-ready JSONL:

```bash
python3 senzing/workflows/mapper/run_mapper_jsonl.py \
  /path/to/production_input.json \
  /path/to/production_output.jsonl \
  --data-source PARTNERS
```

2. Run Senzing project + export + comparison:

```bash
python3 senzing/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/production_output.jsonl
```

For large datasets (500k+), run performance mode:

```bash
python3 senzing/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/production_output.jsonl \
  --fast-mode \
  --use-input-jsonl-directly \
  --data-sources PARTNERS
```

3. Run management tests on that run folder:

```bash
python3 senzing/workflows/testing/run_management_tests.py \
  /path/to/senzing_run_folder
```

Each subfolder has its own README with details.

## Unified Command

To run mapping + E2E + management outputs in one step from a real source JSON:

```bash
python3 senzing/tools/run_sample_to_management.py --input-json /path/to/input.json
```

If no `--input-json` is provided, the command generates a realistic sample first:

```bash
python3 senzing/tools/run_sample_to_management.py --records 500
```

Default behavior: cleanup of `--projects-root` at the end of the run to avoid accumulating multi-GB project folders.
Use `--keep-projects-root` only when you need project internals for troubleshooting.

# Management Reporting Guide

## Goal

Keep each execution traceable: from input sample to management-facing results.

## Where Inputs Are Stored

- Base source-style input files: `sample/`
- Senzing JSONL mapped inputs: `output/`
- Generation linkage metadata: `output/generation_summary_*.json`

## Where Run Results Are Stored

Each execution gets its own run folder under:

- `.senzing_runs_test/<run_prefix>_<timestamp>/`

Inside each run folder, management files are in:

- `comparison/management_summary.md`
- `comparison/ground_truth_match_quality.md`
- `comparison/ground_truth_match_quality.json`

## Run Registry

The file below is updated automatically after each successful E2E run:

- `output/run_registry.csv`

Each row includes:

- run folder (`run_directory`, `run_name`)
- exact input used (`input_file`, `load_input_jsonl`)
- generation linkage (`generation_summary_json`, `base_input_json`, `mapped_output_jsonl`)
- key reports (`management_summary_md`, `ground_truth_match_quality_md`, `ground_truth_match_quality_json`)

This is the primary index to retrieve old executions.

## Unified Command

Run the full pipeline in one command:

```bash
python3 senzing/tools/run_sample_to_management.py --input-json /path/to/input.json
```

Default behavior:

- maps source JSON input to Senzing JSONL
- runs full E2E in Docker
- generates management reports
- updates `output/run_registry.csv`
- removes loader temp shuffle files (`*_sz_shuff_*`) unless `--keep-loader-temp-files` is set
- cleans `--projects-root` at the end of each run (default) to avoid disk growth

Use `--keep-projects-root` only for debugging sessions where project internals must be inspected.

If `--input-json` is omitted, it generates a realistic sample first (`--records` controls size).

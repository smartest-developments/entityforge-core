# Senzing E2E Runner

## Purpose

Run Senzing from A to Z for one JSONL input:

- create isolated project,
- configure data source,
- load records,
- snapshot,
- export (`sz_export`),
- explain on matched records,
- comparison artifacts for analytics.

## Script

- `run_senzing_e2e.py` (wrapper)
- Delegates to: `S3Z/all_in_one/run_senzing_end_to_end.py`

## Command

```bash
python3 S3Z/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/input_senzing_ready.jsonl
```

## Fast Command (Large Files)

For large loads (e.g. 500k), use the performance preset:

```bash
python3 S3Z/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/input_senzing_ready.jsonl \
  --fast-mode \
  --use-input-jsonl-directly \
  --data-sources PARTNERS
```

What this does:
- skips snapshot/export/explain/comparison
- disables retry passes
- avoids JSONL normalization copy
- keeps run logs and summary for load verification

To run full explain without cap:

```bash
python3 S3Z/workflows/e2e_runner/run_senzing_e2e.py \
  /path/to/input_senzing_ready.jsonl \
  --max-explain-records 0 \
  --max-explain-pairs 0
```

By default, temporary loader shuffle files (`*_sz_shuff_*`) are removed after load.
Use `--keep-loader-temp-files` if you want to keep them for troubleshooting.

## Main Artifacts

Inside the generated run folder:

- `entity_export.csv`
- `explain/why_entity_by_record.jsonl`
- `explain/why_records_pairs.jsonl`
- `comparison/entity_records.csv`
- `comparison/matched_pairs.csv`
- `comparison/management_summary.md`
- `comparison/ground_truth_match_quality.md`
- `comparison/ground_truth_match_quality.json`
- `run_summary.json`

## Run Registry

Each successful run appends one row to:

- `output/run_registry.csv`

This index links run folder, input JSONL, generation summary, and management report files.

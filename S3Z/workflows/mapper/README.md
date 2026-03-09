# Mapper Script

## Purpose

Convert production source JSON (array of records) into Senzing-ready JSONL.

## Script

- `run_mapper_jsonl.py` (wrapper)
- Delegates to: `S3Z/tools/partner_json_to_senzing.py`

## Command

```bash
python3 S3Z/workflows/mapper/run_mapper_jsonl.py \
  /path/to/input.json \
  /path/to/output.jsonl \
  --data-source PARTNERS
```

## Current Mapping Rules (key points)

- `SOURCE_IPG_ID` stays in payload only.
- Internal partner and business relation IDs are emitted as matching features (`OTHER_ID_*`).
- `RECORD_ID` is generated as increasing sequence (`1`, `2`, `3`, ...).

# MVP Sample Input (One-Million Mode)

This folder now targets a **single high-volume stress sample** instead of many small samples.

## Canonical sample

- `one_million_stress.jsonl` (generated locally, not committed)
- `one_million_stress.metadata.json` (generated locally, not committed)

## Generate sample

```bash
cd MVP
python3 generate_sample_inputs.py --records 1000000 --clean-legacy-samples
```

## Run pipeline on the sample

```bash
cd MVP
python3 run_mvp_pipeline.py --input-json sample_input/one_million_stress.jsonl --execution-mode auto
```

The generated JSONL includes `SOURCE_TRUE_GROUP_ID` and noisy `IPG ID` labels to stress both:
- our baseline behavior
- Senzing matching behavior

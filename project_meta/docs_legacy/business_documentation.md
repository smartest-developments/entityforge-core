# Business Documentation

## Scope
This PoC evaluates Senzing for entity resolution on partner data, with a direct comparison against our internal baseline matching logic.

## What Management Gets
- One consolidated dashboard (`core/dashboard/index.html`)
- A Streamlit app for interactive review (`core/dashboard/streamlit_app/app.py`)
- Traceable technical outputs per run in `core/output/<run_id>/technical output/`
- Validation artifacts (tests + metric audit) to support number reliability

## How Runs Are Executed
Operational execution is standardized via:
- `core/run_production_command.sh`

This wrapper runs the full pipeline with stability-first settings:
- single load thread
- file split into 1,000-record batches
- fallback chunking at 100 records when needed
- per-file timeout and diagnostics support

## Latest Run Snapshot (Dashboard)
Source run:
- `run_id`: `20260305_123333__Senzing-Ready`

Headline numbers:
- Input records (loaded): `1,031,617`
- Execution time: `462.25 minutes` (~`7.7 hours`)
- Our match found (%): `33.58%`
- Their match found (%): `26.80%`
- Our entities formed: `785,140`
- Their entities formed: `834,249`
- Their match gain/loss: `-6.78%`
- Their pair precision: `87.37%`
- Their pair recall: `5.36%`
- Their false positive rate: `12.63%`

## Business Interpretation
- Senzing is producing high precision on detected pairs, but low recall on known labeled truth in this dataset.
- Our baseline currently groups more records (higher match found %), while Senzing creates more entities (higher fragmentation in this run).
- For production decisioning, the key axis is not only precision but also recall and operational throughput.

## Decision-Oriented Recommendation
- Keep Senzing as a candidate engine.
- Continue with controlled production pilot runs and strict KPI acceptance thresholds.
- Use dashboard + audit reports as mandatory governance evidence before rollout.

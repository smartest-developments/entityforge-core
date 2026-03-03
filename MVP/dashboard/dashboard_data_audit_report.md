# Dashboard Data Audit Report

- Generated at: 2026-03-03T22:45:54
- Output root: `/Users/simones/Developer/mapper-ai-main/MVP/output`
- Dashboard data: `/Users/simones/Developer/mapper-ai-main/MVP/dashboard/management_dashboard_data.js`
- Runs audited: 10
- Runs PASS: 5
- Runs FAIL: 0
- Runs SKIP: 5

## Run Summary

| Run ID | Source Input | Status |
|---|---|---|
| `20260303_221424__one-million-partial-616k` | `one_million_stress.jsonl` | **PASS** |
| `20260303_174641__one-million-final-stream-debug` | `one_million_stress.jsonl` | **SKIP** |
| `20260303_174451__one-million-final-stream` | `one_million_stress.jsonl` | **SKIP** |
| `20260303_174400__stream-smoke-30c` | `stream_smoke_30.jsonl` | **PASS** |
| `20260303_174221__stream-smoke-30b` | `stream_smoke_30.jsonl` | **SKIP** |
| `20260303_173857__stream-smoke-30` | `stream_smoke_30.jsonl` | **SKIP** |
| `20260303_171324__one-million-final` | `one_million_stress.jsonl` | **SKIP** |
| `20260303_171153__path-smoke-50` | `path_smoke_50.jsonl` | **PASS** |
| `20260303_155125__metric-smoke-200-safe-tuned` | `metric_smoke_200.jsonl` | **PASS** |
| `20260303_153108__metric-smoke-200` | `mvp_metric_smoke_200.jsonl` | **PASS** |

## Failed Checks

No failed checks.

## Re-run

```bash
cd MVP
python3 verify_dashboard_metrics.py
```

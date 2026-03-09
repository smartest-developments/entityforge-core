# Summary Report: Senzing Core

## 1) Purpose
This project evaluates entity resolution quality and operational feasibility using Senzing on large partner datasets.

The business goal is simple:
- measure matching quality,
- compare our baseline logic vs Senzing,
- provide auditable outputs for management,
- prepare a production-ready runbook.

## 2) What We Built
We implemented an end-to-end pipeline that:
1. accepts a source JSON file,
2. maps it to Senzing-ready JSONL,
3. runs Senzing load + export + KPI generation,
4. builds a static dashboard,
5. validates dashboard numbers with automated tests.

## 3) How Senzing Is Used
We use Senzing both via CLI tools and SDK-oriented logic.

Operationally, the flow is:
1. create project,
2. configure data source,
3. load records (`sz_file_loader`),
4. export resolved results (`sz_export`),
5. compute comparison metrics and management KPIs.

Important note:
- `RECORD_ID` is passed for each input row,
- final entity assignment is evaluated from canonical/final views,
- raw export rows can repeat the same record key because they are relationship-oriented.

## 4) Key Business Metrics
The dashboard/reporting focuses on:
- records loaded,
- entities formed,
- match found percentage,
- top matching keys,
- entity size distribution.

These metrics are cross-checked by automated tests before publishing dashboard output.

## 5) Main Challenges We Faced
During high-volume runs, we observed known operational limits:
- memory/buffer pressure in native loading steps,
- lock contention on heavy clusters,
- long stalls on specific file portions,
- high runtime variability depending on data shape.

This is why a single 1M "one-shot" load can be unstable in constrained environments.

## 6) Mitigations Implemented
To keep runs reliable, we added progressive safeguards:

1. Split-file loading (ordered):
- one large input is split into sequential physical files at runtime.
- example: 1,036,882 rows -> 1,037 files of 1,000 rows each.

2. Per-file retries and fallback:
- primary load,
- fallback single-thread retry,
- optional chunk fallback (100 records) if needed.

3. Per-file timeout:
- configurable timeout per split file (default in current script: 180 seconds).

4. Continue-on-failure mode:
- if a file fails, pipeline can continue with next files,
- failed files are quarantined for replay and investigation.

5. Auto-diagnostics:
- after failure, diagnostics report is generated automatically.

6. Workspace cleanup utility:
- cleanup script resets runtime/output clutter while keeping essential inputs.

## 7) Practical Example
Example run behavior:
- File 1/1037 loaded in 10.5s
- File 2/1037 loaded in 20.1s
- File 10/1037 exceeded 180s and failed
- failed file saved to quarantine

Meaning for business:
- process does not lose traceability,
- we know exactly which row range failed,
- we can rerun only the failed portion later,
- reporting can flag partial vs full completion.

## 8) Current Operational Recommendation
For constrained environments:
- use small split size (for stability),
- keep per-file timeout enabled,
- keep continue-on-failure enabled,
- keep automated diagnostics enabled,
- track partial runs explicitly in governance discussions.

For stronger production environments:
- increase split size gradually to reduce total runtime,
- tune timeout based on observed percentile durations.

## 9) Test and Control Coverage
The project includes Python test suites that validate:
- metric formulas,
- cross-file consistency,
- aggregate contracts,
- dashboard payload correctness,
- regression snapshots (optional strict mode).

This gives a defensible control layer over results correctness.

# Senzing Gaps and Issues Observed

## Objective
Summarize practical limitations and issues encountered during this PoC, based on real runs.

## Issues Encountered
1. Loader instability on high-volume runs
- Intermittent failures in load phase on large files.
- Long stalls on specific segments.

2. Runtime contention and variability
- Performance is highly sensitive to data distribution.
- Some segments complete quickly; others trigger retries/timeouts.

3. Memory/buffer pressure symptoms
- Large runs can hit native-level pressure and fail without careful throttling.

4. Long total execution time in constrained environments
- End-to-end runtime can be several hours when stability settings are conservative.

5. Operational complexity
- Stable execution requires tuning (batch size, chunk size, timeout, fallback policy).
- This increases operational overhead for non-technical users.

## Functional Gaps (from a management perspective)
1. Out-of-the-box behavior is not always "one-click stable" at high scale in constrained environments.
2. Additional wrapper logic is required for robust production execution (retry/fallback/diagnostics).
3. KPI interpretation still needs domain framing (precision vs recall trade-off).

## Mitigations Implemented in This Project
- Split load into ordered files
- Per-file timeout
- Fallback load paths
- Continue-on-failure mode with quarantine
- Automatic diagnostics output
- Automated KPI verification and dashboard audit

## Residual Risks
- Runtime remains data-shape dependent.
- Throughput may degrade significantly under contention-heavy distributions.
- Need production pilot with real infra to validate final SLAs.

## Recommendation
- Treat Senzing as viable but not plug-and-play for our workload.
- Keep resilience wrapper and metric audit as mandatory controls.
- Approve production adoption only after pilot evidence on real infrastructure.

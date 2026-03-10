# Dashboard Test Suite Report

- Generated at: 2026-03-10T13:47:15+00:00
- Dashboard data: `/Users/simonesalvo/Developer/entityforge-core/core/core/output/sample_20260310_135805/sdk_probe/smoke_dashboard_test/management_dashboard_data.js`
- Output root: `/Users/simonesalvo/Developer/entityforge-core/core/core/output/sample_20260310_135805/sdk_probe/smoke_output`
- Tests run: 76
- Failures: 0
- Errors: 0
- Skipped: 36
- Status: **PASS**

## Skipped

- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_aggregate_coverage_formula_is_valid`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_aggregate_false_positive_rate_formula_is_valid`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_aggregate_match_gain_formula_is_valid`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_aggregate_precision_formula_is_valid`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_aggregate_total_input_matches_success_runs`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_all_success_runs_have_mandatory_flags`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_distribution_fields_are_non_negative_ints`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_explain_coverage_shape`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_mapping_info_shape`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_aggregate_contracts.DashboardAggregateContractsTestCase.test_new_metric_fields_shape`: No successful runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_baseline_relations`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_confusion_matrix_counts_match_ground_truth`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_confusion_matrix_non_negative`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_entity_distribution_total_matches_resolved_entities`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_entity_size_distribution_is_consistent`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_execution_minutes_matches_run_summary_steps`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_extra_gain_relation`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_extra_metrics_match_discovery_fields`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_file_counts_match_dashboard_values`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_gain_loss_percentage_ranges`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_ground_truth_count_relations`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_kpi_percentages_match_formulas`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_match_and_entity_comparison_metrics`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_our_baseline_metrics_match_discovery_logic`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_our_entity_distribution_total_matches_our_entities_formed`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_our_entity_size_distribution_is_consistent`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_payload_contains_runs`: Dashboard payload has no runs yet
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_percentage_ranges`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_quality_available_flag_consistency`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_success_run_artifacts_exist`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_success_runs_have_quality_data`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_synthetic_noise_coverage_exists`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_top_match_keys_format`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_validation_block_shape`: No successful dashboard runs available yet; generate outputs first.
- `testing.test_dashboard_metrics.DashboardMetricsTestCase.test_validation_checks_have_no_failures`: No successful dashboard runs available yet; generate outputs first.
- `setUpClass (testing.test_dashboard_regression_snapshot.DashboardRegressionSnapshotTestCase)`: Regression snapshot checks disabled (set MVP_ENFORCE_REGRESSION_SNAPSHOT=1 to enable)

## Re-run

```bash
cd core
python3 testing/run_dashboard_tests.py
```

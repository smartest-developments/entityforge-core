"""End-to-end assertions for dashboard KPIs against raw run artifacts."""

from __future__ import annotations

import datetime as dt
import os
import re
import unittest
from pathlib import Path
from typing import Any

from testing.dashboard_assertions import (
    as_int,
    compute_expected_run_metrics,
    compute_summary_from_runs,
    normalize_distribution,
    parse_dashboard_data_js,
)

TOLERANCE = 0.01
RUN_ID_RE = re.compile(r"^\d{8}_\d{6}(?:__.+)?$")


class DashboardMetricsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mvp_root = Path(__file__).resolve().parents[1]

        dashboard_data_env = os.environ.get("MVP_DASHBOARD_DATA_PATH", "").strip()
        if dashboard_data_env:
            dashboard_data_path = Path(dashboard_data_env).expanduser()
            if not dashboard_data_path.is_absolute():
                dashboard_data_path = cls.mvp_root / dashboard_data_path
        else:
            dashboard_data_path = cls.mvp_root / "dashboard" / "management_dashboard_data.js"
        cls.dashboard_data_path = dashboard_data_path.resolve()

        cls.payload = parse_dashboard_data_js(cls.dashboard_data_path)
        runs = cls.payload.get("runs") if isinstance(cls.payload.get("runs"), list) else []
        cls.runs = [run for run in runs if isinstance(run, dict)]
        cls.success_runs = [run for run in cls.runs if run.get("run_status") == "success"]

        output_root_env = os.environ.get("MVP_OUTPUT_ROOT", "").strip()
        if output_root_env:
            output_root = Path(output_root_env).expanduser()
            if not output_root.is_absolute():
                output_root = cls.mvp_root / output_root
        else:
            output_root = Path(str(cls.payload.get("output_root") or "")).expanduser()
            if not output_root.is_absolute():
                output_root = cls.mvp_root / "output"
        cls.output_root = output_root.resolve()

        cls.expected_by_run: dict[str, dict[str, Any]] = {
            str(run.get("run_id")): compute_expected_run_metrics(run, cls.output_root)
            for run in cls.success_runs
        }

    def as_float_or_none(self, value: Any) -> float | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def assert_metric(self, run_id: str, metric_name: str, dashboard_value: Any, expected_value: Any, tolerance: float = TOLERANCE) -> None:
        context = f"run_id={run_id} metric={metric_name}"
        if expected_value is None:
            self.assertIsNone(dashboard_value, msg=f"Expected None ({context}) but got {dashboard_value!r}")
            return
        if isinstance(expected_value, (int, float)):
            self.assertIsInstance(
                dashboard_value,
                (int, float),
                msg=f"Expected numeric value for {context}, got {type(dashboard_value).__name__}",
            )
            delta = abs(float(dashboard_value) - float(expected_value))
            self.assertLessEqual(
                delta,
                tolerance,
                msg=f"Value mismatch for {context}: dashboard={dashboard_value} expected={expected_value} delta={delta}",
            )
            return
        self.assertEqual(dashboard_value, expected_value, msg=f"Value mismatch for {context}")

    def test_payload_contains_runs(self) -> None:
        self.assertTrue(self.dashboard_data_path.exists(), "Dashboard data file does not exist")
        self.assertGreater(len(self.runs), 0, "Dashboard payload has no runs")

    def test_success_run_artifacts_exist(self) -> None:
        self.assertGreater(len(self.success_runs), 0, "No successful runs found in dashboard payload")
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]
            with self.subTest(run_id=run_id):
                paths = expected["paths"]
                self.assertTrue(paths["run_dir"].exists(), f"Missing run directory: {paths['run_dir']}")
                self.assertTrue(paths["technical_dir"].exists(), f"Missing technical output directory: {paths['technical_dir']}")
                self.assertTrue(paths["management_summary_json"].exists(), f"Missing management_summary.json for {run_id}")
                self.assertTrue(paths["ground_truth_json"].exists(), f"Missing ground_truth_match_quality.json for {run_id}")
                self.assertTrue(paths["entity_records_csv"].exists(), f"Missing entity_records.csv for {run_id}")
                self.assertTrue(paths["matched_pairs_csv"].exists(), f"Missing matched_pairs.csv for {run_id}")
                self.assertTrue(paths["input_source_json"].exists(), f"Missing input_source.json for {run_id}")

    def test_file_counts_match_dashboard_values(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]["from_files"]
            with self.subTest(run_id=run_id):
                self.assert_metric(run_id, "records_input", run.get("records_input"), expected.get("records_input"), tolerance=0.0)
                self.assert_metric(run_id, "matched_pairs", run.get("matched_pairs"), expected.get("matched_pairs"), tolerance=0.0)
                self.assert_metric(run_id, "resolved_entities", run.get("resolved_entities"), expected.get("resolved_entities"), tolerance=0.0)
                self.assert_metric(
                    run_id,
                    "our_resolved_entities",
                    run.get("our_resolved_entities"),
                    expected.get("our_resolved_entities"),
                    tolerance=0.0,
                )

    def test_confusion_matrix_counts_match_ground_truth(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]["from_ground_truth"]
            with self.subTest(run_id=run_id):
                self.assert_metric(run_id, "true_positive", run.get("true_positive"), expected.get("true_positive"), tolerance=0.0)
                self.assert_metric(run_id, "false_positive", run.get("false_positive"), expected.get("false_positive"), tolerance=0.0)
                self.assert_metric(run_id, "false_negative", run.get("false_negative"), expected.get("false_negative"), tolerance=0.0)
                self.assert_metric(
                    run_id,
                    "predicted_pairs_labeled",
                    run.get("predicted_pairs_labeled"),
                    expected.get("predicted_pairs_labeled"),
                    tolerance=0.0,
                )

    def test_kpi_percentages_match_formulas(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]["from_ground_truth"]
            with self.subTest(run_id=run_id):
                self.assert_metric(
                    run_id,
                    "pair_precision_pct",
                    run.get("pair_precision_pct"),
                    expected.get("pair_precision_pct"),
                )
                self.assert_metric(
                    run_id,
                    "pair_recall_pct",
                    run.get("pair_recall_pct"),
                    expected.get("pair_recall_pct"),
                )
                self.assert_metric(
                    run_id,
                    "overall_false_positive_pct",
                    run.get("overall_false_positive_pct"),
                    expected.get("overall_false_positive_pct"),
                )
                self.assert_metric(
                    run_id,
                    "pair_precision_pct_from_counts",
                    run.get("pair_precision_pct"),
                    expected.get("pair_precision_pct_from_counts"),
                )
                self.assert_metric(
                    run_id,
                    "pair_recall_pct_from_counts",
                    run.get("pair_recall_pct"),
                    expected.get("pair_recall_pct_from_counts"),
                )

    def test_our_baseline_metrics_match_discovery_logic(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]["from_discovery"]
            with self.subTest(run_id=run_id):
                self.assert_metric(run_id, "our_true_positive", run.get("our_true_positive"), expected.get("our_true_positive"), tolerance=0.0)
                self.assert_metric(
                    run_id,
                    "our_true_pairs_total",
                    run.get("our_true_pairs_total"),
                    expected.get("our_true_pairs_total"),
                    tolerance=0.0,
                )
                self.assert_metric(
                    run_id,
                    "our_false_positive",
                    run.get("our_false_positive"),
                    expected.get("our_false_positive"),
                    tolerance=0.0,
                )
                self.assert_metric(
                    run_id,
                    "our_false_negative",
                    run.get("our_false_negative"),
                    expected.get("our_false_negative"),
                    tolerance=0.0,
                )
                self.assert_metric(
                    run_id,
                    "our_match_coverage_pct",
                    run.get("our_match_coverage_pct"),
                    expected.get("our_match_coverage_pct"),
                )

    def test_extra_metrics_match_discovery_fields(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected = self.expected_by_run[run_id]["from_discovery"]
            with self.subTest(run_id=run_id):
                self.assert_metric(
                    run_id,
                    "extra_true_matches_found",
                    run.get("extra_true_matches_found"),
                    expected.get("extra_true_matches_found"),
                    tolerance=0.0,
                )
                self.assert_metric(
                    run_id,
                    "extra_false_matches_found",
                    run.get("extra_false_matches_found"),
                    expected.get("extra_false_matches_found"),
                    tolerance=0.0,
                )
                self.assert_metric(
                    run_id,
                    "extra_gain_vs_known_pct",
                    run.get("extra_gain_vs_known_pct"),
                    expected.get("extra_gain_vs_known_pct"),
                )

    def test_entity_size_distribution_is_consistent(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            expected_dist = self.expected_by_run[run_id]["from_files"].get("entity_size_distribution")
            dashboard_dist = normalize_distribution(run.get("entity_size_distribution"))
            with self.subTest(run_id=run_id):
                self.assertIsNotNone(dashboard_dist, f"Invalid entity_size_distribution type for {run_id}")
                self.assertEqual(dashboard_dist, expected_dist, f"Distribution mismatch for {run_id}")
                dist_total = sum(int(value) for value in (dashboard_dist or {}).values())
                self.assertEqual(
                    dist_total,
                    as_int(run.get("resolved_entities")),
                    f"Distribution total must match resolved_entities for {run_id}",
                )

    def test_summary_block_matches_recomputed_values(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        expected_summary = compute_summary_from_runs(self.runs)

        for key in (
            "runs_total",
            "quality_runs_total",
            "successful_runs",
            "failed_runs",
            "incomplete_runs",
            "latest_run_id",
            "records_input_total",
            "matched_pairs_total",
        ):
            with self.subTest(summary_key=key):
                self.assertEqual(summary.get(key), expected_summary.get(key), f"Summary mismatch for {key}")

        for key in ("avg_pair_precision_pct", "avg_pair_recall_pct"):
            with self.subTest(summary_key=key):
                expected_value = expected_summary.get(key)
                dashboard_value = summary.get(key)
                if expected_value is None:
                    self.assertIsNone(dashboard_value, f"Expected None for summary.{key}")
                else:
                    self.assertIsInstance(dashboard_value, (int, float), f"Expected numeric summary.{key}")
                    self.assertLessEqual(
                        abs(float(dashboard_value) - float(expected_value)),
                        TOLERANCE,
                        f"Summary mismatch for {key}: dashboard={dashboard_value} expected={expected_value}",
                    )

    def test_validation_checks_have_no_failures(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id"))
            validation = run.get("validation") if isinstance(run.get("validation"), dict) else {}
            with self.subTest(run_id=run_id):
                self.assertNotEqual(validation.get("status"), "FAIL", f"Validation status FAIL in dashboard payload for {run_id}")
                checks = validation.get("checks") if isinstance(validation.get("checks"), list) else []
                for check in checks:
                    if not isinstance(check, dict):
                        continue
                    self.assertNotEqual(
                        check.get("status"),
                        "FAIL",
                        f"Validation check failed in payload for {run_id}: {check.get('name')}",
                    )

    def test_synthetic_noise_coverage_exists(self) -> None:
        sample_runs = [
            run
            for run in self.success_runs
            if "sample_" in str(run.get("source_input_name") or "")
            or "sample_" in str(run.get("run_label") or "")
        ]
        if len(sample_runs) < 5:
            self.skipTest("Synthetic sample runs not detected; skipping synthetic-noise coverage checks")

        self.assertTrue(
            any((as_int(run.get("our_false_positive")) or 0) > 0 for run in sample_runs),
            "Expected at least one sample run with Our False Positive > 0",
        )
        self.assertTrue(
            any((as_int(run.get("our_false_negative")) or 0) > 0 for run in sample_runs),
            "Expected at least one sample run with Our False Negative > 0",
        )
        self.assertTrue(
            any((as_int(run.get("false_positive")) or 0) > 0 for run in sample_runs),
            "Expected at least one sample run with Their False Positive > 0",
        )
        self.assertTrue(
            any((as_int(run.get("false_negative")) or 0) > 0 for run in sample_runs),
            "Expected at least one sample run with Their False Negative > 0",
        )

    def test_top_level_payload_schema(self) -> None:
        for key in ("generated_at", "output_root", "runs", "summary"):
            self.assertIn(key, self.payload, f"Missing top-level field: {key}")

    def test_run_ids_are_unique_and_sorted_desc(self) -> None:
        run_ids = [str(run.get("run_id") or "") for run in self.runs]
        self.assertEqual(len(run_ids), len(set(run_ids)), "Duplicate run_id found in payload")
        sorted_ids = sorted(run_ids, reverse=True)
        self.assertEqual(run_ids, sorted_ids, "Runs are expected to be sorted descending by run_id")

    def test_runs_have_required_identity_fields(self) -> None:
        required = (
            "run_id",
            "run_status",
            "source_input_name",
            "records_input",
            "matched_pairs",
            "resolved_entities",
            "our_resolved_entities",
            "validation",
        )
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for key in required:
                    self.assertIn(key, run, f"Missing required run field '{key}' in {run_id}")

    def test_success_runs_have_quality_data(self) -> None:
        quality_runs = [run for run in self.success_runs if bool(run.get("quality_available"))]
        self.assertGreaterEqual(len(quality_runs), 1, "No quality-enabled successful runs found")

    def test_percentage_ranges(self) -> None:
        pct_fields = (
            "pair_precision_pct",
            "pair_recall_pct",
            "overall_false_positive_pct",
            "our_match_coverage_pct",
            "extra_gain_vs_known_pct",
        )
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for field in pct_fields:
                    value = self.as_float_or_none(run.get(field))
                    if value is None:
                        continue
                    lower_bound = 0.0
                    upper_bound = 100.0 if field != "extra_gain_vs_known_pct" else 100000.0
                    self.assertGreaterEqual(value, lower_bound, f"{field} below 0 in {run_id}")
                    self.assertLessEqual(value, upper_bound, f"{field} above expected bound in {run_id}")

    def test_ground_truth_count_relations(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            tp = as_int(run.get("true_positive"))
            fp = as_int(run.get("false_positive"))
            fn = as_int(run.get("false_negative"))
            predicted = as_int(run.get("predicted_pairs_labeled"))
            labeled_true = as_int(run.get("ground_truth_pairs_labeled"))
            with self.subTest(run_id=run_id):
                if tp is not None and fp is not None and predicted is not None:
                    self.assertEqual(tp + fp, predicted, f"Expected TP+FP==predicted_pairs_labeled in {run_id}")
                if tp is not None and fn is not None and labeled_true is not None:
                    self.assertEqual(tp + fn, labeled_true, f"Expected TP+FN==ground_truth_pairs_labeled in {run_id}")

    def test_confusion_matrix_non_negative(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for field in (
                    "true_positive",
                    "false_positive",
                    "false_negative",
                    "our_true_positive",
                    "our_false_positive",
                    "our_false_negative",
                ):
                    value = as_int(run.get(field))
                    if value is None:
                        continue
                    self.assertGreaterEqual(value, 0, f"{field} must be >= 0 in {run_id}")

    def test_baseline_relations(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            our_tp = as_int(run.get("our_true_positive"))
            our_total = as_int(run.get("our_true_pairs_total"))
            our_fn = as_int(run.get("our_false_negative"))
            with self.subTest(run_id=run_id):
                if our_tp is not None and our_total is not None:
                    self.assertLessEqual(our_tp, our_total, f"Our TP cannot exceed Our total true pairs in {run_id}")
                if our_tp is not None and our_total is not None and our_fn is not None:
                    self.assertEqual(our_tp + our_fn, our_total, f"Our TP+FN must equal Our total true pairs in {run_id}")

    def test_extra_gain_relation(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            extra_pairs = as_int(run.get("extra_true_matches_found"))
            known_pairs = as_int(run.get("known_pairs_ipg"))
            gain_pct = self.as_float_or_none(run.get("extra_gain_vs_known_pct"))
            with self.subTest(run_id=run_id):
                if extra_pairs is None or known_pairs is None or gain_pct is None or known_pairs <= 0:
                    continue
                recomputed = round((extra_pairs / known_pairs) * 100.0, 2)
                self.assertLessEqual(
                    abs(gain_pct - recomputed),
                    TOLERANCE,
                    f"extra_gain_vs_known_pct mismatch in {run_id}: dashboard={gain_pct} recomputed={recomputed}",
                )

    def test_entity_distribution_total_matches_resolved_entities(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            distribution = run.get("entity_size_distribution")
            resolved_entities = as_int(run.get("resolved_entities"))
            with self.subTest(run_id=run_id):
                self.assertIsInstance(distribution, dict, f"entity_size_distribution must be object in {run_id}")
                if not isinstance(distribution, dict) or resolved_entities is None:
                    continue
                total = 0
                for value in distribution.values():
                    self.assertIsInstance(value, int, f"Distribution values must be int in {run_id}")
                    total += int(value)
                self.assertEqual(total, resolved_entities, f"Distribution total mismatch in {run_id}")

    def test_top_match_keys_format(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            top_keys = run.get("top_match_keys")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(top_keys, list, f"top_match_keys must be a list in {run_id}")
                if not isinstance(top_keys, list):
                    continue
                self.assertLessEqual(len(top_keys), 10, f"top_match_keys should contain max 10 entries in {run_id}")
                for item in top_keys:
                    self.assertIsInstance(item, list, f"Each top_match_keys item must be a list in {run_id}")
                    if not isinstance(item, list):
                        continue
                    self.assertEqual(len(item), 2, f"Each top_match_keys item must have 2 elements in {run_id}")
                    self.assertIsInstance(item[0], str, f"Match key label must be string in {run_id}")
                    self.assertIsInstance(item[1], int, f"Match key count must be int in {run_id}")
                    self.assertGreaterEqual(item[1], 0, f"Match key count must be non-negative in {run_id}")

    def test_validation_block_shape(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            validation = run.get("validation")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(validation, dict, f"Validation must be object in {run_id}")
                if not isinstance(validation, dict):
                    continue
                self.assertIn(validation.get("status"), {"PASS", "FAIL", "SKIP"}, f"Unexpected validation status in {run_id}")
                checks = validation.get("checks")
                self.assertIsInstance(checks, list, f"Validation checks must be list in {run_id}")
                if not isinstance(checks, list):
                    continue
                for check in checks:
                    self.assertIsInstance(check, dict, f"Validation check must be object in {run_id}")
                    if not isinstance(check, dict):
                        continue
                    self.assertIn("name", check, f"Validation check missing name in {run_id}")
                    self.assertIn("status", check, f"Validation check missing status in {run_id}")
                    self.assertIn(check.get("status"), {"PASS", "FAIL", "SKIP"}, f"Unexpected check status in {run_id}")

    def test_quality_available_flag_consistency(self) -> None:
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            quality = bool(run.get("quality_available"))
            with self.subTest(run_id=run_id):
                if not quality:
                    continue
                for field in ("pair_precision_pct", "pair_recall_pct", "true_positive", "false_positive", "false_negative"):
                    self.assertIsNotNone(run.get(field), f"quality_available=True but missing {field} in {run_id}")

    def test_run_status_values_allowed(self) -> None:
        allowed = {"success", "failed", "incomplete"}
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            status = run.get("run_status")
            with self.subTest(run_id=run_id):
                self.assertIn(status, allowed, f"Unexpected run_status '{status}' in {run_id}")

    def test_run_id_format(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                self.assertRegex(run_id, RUN_ID_RE, f"Invalid run_id format: {run_id}")

    def test_run_datetime_is_iso(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            value = run.get("run_datetime")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(value, str, f"run_datetime must be string in {run_id}")
                if isinstance(value, str):
                    try:
                        dt.datetime.fromisoformat(value)
                    except ValueError as exc:
                        self.fail(f"Invalid run_datetime '{value}' in {run_id}: {exc}")

    def test_source_input_name_is_json(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            value = run.get("source_input_name")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(value, str, f"source_input_name must be string in {run_id}")
                if isinstance(value, str):
                    self.assertTrue(value.endswith(".json"), f"source_input_name must end with .json in {run_id}")

    def test_artifacts_metadata_shape(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            artifacts = run.get("artifacts")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(artifacts, list, f"artifacts must be list in {run_id}")
                if not isinstance(artifacts, list):
                    continue
                self.assertGreater(len(artifacts), 0, f"artifacts list should not be empty in {run_id}")
                for item in artifacts:
                    self.assertIsInstance(item, dict, f"artifact entry must be object in {run_id}")
                    if not isinstance(item, dict):
                        continue
                    self.assertIsInstance(item.get("relative_path"), str, f"artifact.relative_path must be string in {run_id}")
                    self.assertIsInstance(item.get("display_name"), str, f"artifact.display_name must be string in {run_id}")
                    self.assertIsInstance(item.get("size_bytes"), int, f"artifact.size_bytes must be int in {run_id}")
                    if isinstance(item.get("size_bytes"), int):
                        self.assertGreaterEqual(item["size_bytes"], 0, f"artifact.size_bytes must be >= 0 in {run_id}")

    def test_artifact_paths_exist_on_disk(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            artifacts = run.get("artifacts") if isinstance(run.get("artifacts"), list) else []
            with self.subTest(run_id=run_id):
                for item in artifacts:
                    if not isinstance(item, dict):
                        continue
                    relative_path = item.get("relative_path")
                    if not isinstance(relative_path, str):
                        continue
                    file_path = self.output_root / relative_path
                    self.assertTrue(file_path.exists(), f"Missing artifact file for {run_id}: {relative_path}")
                    self.assertTrue(file_path.is_file(), f"Artifact path is not a file for {run_id}: {relative_path}")

    def test_validation_check_names_unique_per_run(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            validation = run.get("validation") if isinstance(run.get("validation"), dict) else {}
            checks = validation.get("checks") if isinstance(validation.get("checks"), list) else []
            with self.subTest(run_id=run_id):
                names = [check.get("name") for check in checks if isinstance(check, dict)]
                self.assertEqual(len(names), len(set(names)), f"Duplicate validation check names in {run_id}")

    def test_summary_latest_run_id_is_present(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        latest = summary.get("latest_run_id")
        run_ids = {run.get("run_id") for run in self.runs}
        self.assertIn(latest, run_ids, "summary.latest_run_id is not present in runs list")

    def test_summary_quality_runs_matches_flags(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        expected = sum(1 for run in self.runs if bool(run.get("quality_available")))
        self.assertEqual(
            summary.get("quality_runs_total"),
            expected,
            "summary.quality_runs_total does not match count of runs with quality_available=True",
        )

    def test_records_export_relationships(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            records_input = as_int(run.get("records_input"))
            records_exported = as_int(run.get("records_exported"))
            matched_records = as_int(run.get("matched_records"))
            with self.subTest(run_id=run_id):
                if records_input is not None and records_exported is not None:
                    self.assertGreaterEqual(
                        records_exported,
                        records_input,
                        f"records_exported should be >= records_input in {run_id}",
                    )
                if matched_records is not None and records_exported is not None:
                    self.assertLessEqual(
                        matched_records,
                        records_exported,
                        f"matched_records should be <= records_exported in {run_id}",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)

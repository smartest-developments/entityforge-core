"""Aggregate and contract tests for dashboard payload integrity."""

from __future__ import annotations

import datetime as dt
import os
import unittest
from pathlib import Path
from typing import Any

from testing.dashboard_assertions import as_int, parse_dashboard_data_js

TOLERANCE = 0.01


class DashboardAggregateContractsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mvp_root = Path(__file__).resolve().parents[1]
        dashboard_data_env = os.environ.get("MVP_DASHBOARD_DATA_PATH", "").strip()
        dashboard_data_path = (
            Path(dashboard_data_env).expanduser()
            if dashboard_data_env
            else cls.mvp_root / "dashboard" / "management_dashboard_data.js"
        )
        if not dashboard_data_path.is_absolute():
            dashboard_data_path = cls.mvp_root / dashboard_data_path
        cls.dashboard_data_path = dashboard_data_path.resolve()
        cls.payload = parse_dashboard_data_js(cls.dashboard_data_path)
        cls.runs = [run for run in (cls.payload.get("runs") or []) if isinstance(run, dict)]
        cls.success_runs = [run for run in cls.runs if run.get("run_status") == "success"]
        cls.has_success_runs = len(cls.success_runs) > 0

    def require_success_runs(self) -> None:
        if not self.has_success_runs:
            self.skipTest("No successful runs available yet; generate outputs first.")

    def as_float(self, value: Any) -> float | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def assert_close(self, left: float, right: float, msg: str) -> None:
        self.assertLessEqual(abs(left - right), TOLERANCE, msg)

    def test_payload_generated_at_is_iso(self) -> None:
        generated_at = self.payload.get("generated_at")
        self.assertIsInstance(generated_at, str)
        if isinstance(generated_at, str):
            dt.datetime.fromisoformat(generated_at)

    def test_all_success_runs_have_mandatory_flags(self) -> None:
        self.require_success_runs()
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for key in ("has_management_summary", "has_ground_truth_summary", "has_run_summary", "quality_available"):
                    self.assertIsInstance(run.get(key), bool, f"{key} must be bool in {run_id}")

    def test_mapping_info_shape(self) -> None:
        self.require_success_runs()
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            info = run.get("mapping_info")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(info, dict, f"mapping_info must be object in {run_id}")
                if not isinstance(info, dict):
                    continue
                for key in ("data_source", "tax_id_type", "execution_mode"):
                    self.assertIn(key, info, f"mapping_info missing {key} in {run_id}")

    def test_explain_coverage_shape(self) -> None:
        self.require_success_runs()
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            coverage = run.get("explain_coverage")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(coverage, dict, f"explain_coverage must be object in {run_id}")
                if not isinstance(coverage, dict):
                    continue
                for key in ("why_entity_total", "why_entity_ok", "why_records_total", "why_records_ok"):
                    self.assertIn(key, coverage, f"explain_coverage missing {key} in {run_id}")
                    value = as_int(coverage.get(key))
                    self.assertIsNotNone(value, f"explain_coverage.{key} must be int in {run_id}")
                    if value is not None:
                        self.assertGreaterEqual(value, 0, f"explain_coverage.{key} must be >= 0 in {run_id}")

    def test_runtime_warnings_is_list(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            warnings = run.get("runtime_warnings")
            with self.subTest(run_id=run_id):
                self.assertIsInstance(warnings, list, f"runtime_warnings must be list in {run_id}")

    def test_distribution_fields_are_non_negative_ints(self) -> None:
        self.require_success_runs()
        dist_fields = (
            "our_entity_size_distribution",
            "entity_size_distribution",
            "entity_pairings_distribution",
            "record_pairing_degree_distribution",
            "match_level_distribution",
        )
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for field in dist_fields:
                    distribution = run.get(field)
                    self.assertIsInstance(distribution, dict, f"{field} must be object in {run_id}")
                    if not isinstance(distribution, dict):
                        continue
                    for key, value in distribution.items():
                        self.assertIsInstance(key, str, f"{field} keys must be strings in {run_id}")
                        self.assertIsInstance(value, int, f"{field} values must be ints in {run_id}")
                        if isinstance(value, int):
                            self.assertGreaterEqual(value, 0, f"{field} values must be >= 0 in {run_id}")

    def test_new_metric_fields_shape(self) -> None:
        self.require_success_runs()
        int_fields = (
            "our_entities_formed",
            "their_entities_formed",
            "our_grouped_members",
            "their_grouped_members",
        )
        pct_fields = (
            "our_match_pct",
            "their_match_pct",
            "our_match_gain_loss_pct",
            "their_match_gain_loss_pct",
            "our_entity_gain_loss_pct",
            "their_entity_gain_loss_pct",
        )
        for run in self.success_runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for field in int_fields:
                    value = run.get(field)
                    self.assertTrue(value is None or isinstance(value, int), f"{field} must be int|None in {run_id}")
                for field in pct_fields:
                    value = run.get(field)
                    self.assertTrue(
                        value is None or isinstance(value, (int, float)),
                        f"{field} must be number|None in {run_id}",
                    )

    def test_artifact_relative_paths_unique_per_run(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            artifacts = run.get("artifacts") if isinstance(run.get("artifacts"), list) else []
            with self.subTest(run_id=run_id):
                rel_paths = [item.get("relative_path") for item in artifacts if isinstance(item, dict)]
                rel_paths = [path for path in rel_paths if isinstance(path, str)]
                self.assertEqual(len(rel_paths), len(set(rel_paths)), f"Duplicate artifact relative_path in {run_id}")

    def test_paths_reference_run_id(self) -> None:
        for run in self.runs:
            run_id = str(run.get("run_id") or "")
            with self.subTest(run_id=run_id):
                for key in ("input_source_path", "management_summary_path", "ground_truth_summary_path", "technical_path"):
                    value = run.get(key)
                    self.assertIsInstance(value, str, f"{key} must be string in {run_id}")
                    if isinstance(value, str):
                        self.assertIn(run_id, value, f"{key} must include run_id in {run_id}")

    def test_aggregate_total_input_matches_success_runs(self) -> None:
        self.require_success_runs()
        total_input = sum(int(run.get("records_input")) for run in self.success_runs if as_int(run.get("records_input")) is not None)
        self.assertGreater(total_input, 0)

    def test_aggregate_precision_formula_is_valid(self) -> None:
        self.require_success_runs()
        tp = sum(int(run.get("true_positive")) for run in self.success_runs if as_int(run.get("true_positive")) is not None)
        fp = sum(int(run.get("false_positive")) for run in self.success_runs if as_int(run.get("false_positive")) is not None)
        denominator = tp + fp
        self.assertGreater(denominator, 0)
        precision = (tp / denominator) * 100.0
        self.assertGreaterEqual(precision, 0.0)
        self.assertLessEqual(precision, 100.0)

    def test_aggregate_coverage_formula_is_valid(self) -> None:
        self.require_success_runs()
        our_tp = sum(int(run.get("our_true_positive")) for run in self.success_runs if as_int(run.get("our_true_positive")) is not None)
        our_total = sum(int(run.get("our_true_pairs_total")) for run in self.success_runs if as_int(run.get("our_true_pairs_total")) is not None)
        self.assertGreater(our_total, 0)
        coverage = (our_tp / our_total) * 100.0
        self.assertGreaterEqual(coverage, 0.0)
        self.assertLessEqual(coverage, 100.0)

    def test_aggregate_false_positive_rate_formula_is_valid(self) -> None:
        self.require_success_runs()
        fp = sum(int(run.get("false_positive")) for run in self.success_runs if as_int(run.get("false_positive")) is not None)
        predicted = sum(
            int(run.get("predicted_pairs_labeled"))
            for run in self.success_runs
            if as_int(run.get("predicted_pairs_labeled")) is not None
        )
        self.assertGreater(predicted, 0)
        fp_rate = (fp / predicted) * 100.0
        self.assertGreaterEqual(fp_rate, 0.0)
        self.assertLessEqual(fp_rate, 100.0)

    def test_aggregate_match_gain_formula_is_valid(self) -> None:
        self.require_success_runs()
        extra = sum(
            int(run.get("extra_true_matches_found"))
            for run in self.success_runs
            if as_int(run.get("extra_true_matches_found")) is not None
        )
        known = sum(int(run.get("known_pairs_ipg")) for run in self.success_runs if as_int(run.get("known_pairs_ipg")) is not None)
        self.assertGreater(known, 0)
        gain = (extra / known) * 100.0
        self.assertGreaterEqual(gain, 0.0)

    def test_summary_run_counts_consistency(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        runs_total = as_int(summary.get("runs_total"))
        successful = as_int(summary.get("successful_runs"))
        failed = as_int(summary.get("failed_runs"))
        incomplete = as_int(summary.get("incomplete_runs"))
        self.assertIsNotNone(runs_total)
        self.assertIsNotNone(successful)
        self.assertIsNotNone(failed)
        self.assertIsNotNone(incomplete)
        if None not in (runs_total, successful, failed, incomplete):
            self.assertEqual(runs_total, successful + failed + incomplete)

    def test_summary_numeric_fields_non_negative(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        for key in ("runs_total", "quality_runs_total", "successful_runs", "failed_runs", "incomplete_runs", "records_input_total", "matched_pairs_total"):
            value = as_int(summary.get(key))
            with self.subTest(summary_key=key):
                self.assertIsNotNone(value, f"summary.{key} must be int")
                if value is not None:
                    self.assertGreaterEqual(value, 0, f"summary.{key} must be >= 0")

    def test_summary_average_percentages_in_range(self) -> None:
        summary = self.payload.get("summary") if isinstance(self.payload.get("summary"), dict) else {}
        for key in ("avg_pair_precision_pct", "avg_pair_recall_pct"):
            value = self.as_float(summary.get(key))
            with self.subTest(summary_key=key):
                if value is None:
                    continue
                self.assertGreaterEqual(value, 0.0, f"summary.{key} must be >= 0")
                self.assertLessEqual(value, 100.0, f"summary.{key} must be <= 100")


if __name__ == "__main__":
    unittest.main(verbosity=2)

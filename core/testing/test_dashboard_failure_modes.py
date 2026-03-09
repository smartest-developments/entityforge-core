"""Failure-mode tests for dashboard test helpers and parsing logic."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from testing.dashboard_assertions import (
    build_entity_size_distribution,
    compute_expected_run_metrics,
    count_input_source_records,
    count_unique_source_ipg_groups,
    normalize_distribution,
    parse_dashboard_data_js,
    read_json,
    to_pct_from_counts,
)


class DashboardFailureModesTestCase(unittest.TestCase):
    def test_parse_dashboard_data_js_invalid_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "management_dashboard_data.js"
            path.write_text("const BAD = {};\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_dashboard_data_js(path)

    def test_parse_dashboard_data_js_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "management_dashboard_data.js"
            path.write_text("window.MVP_DASHBOARD_DATA = {invalid};\n", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                parse_dashboard_data_js(path)

    def test_read_json_missing_returns_empty_dict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.json"
            self.assertEqual(read_json(path), {})

    def test_read_json_invalid_returns_empty_dict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{invalid json", encoding="utf-8")
            self.assertEqual(read_json(path), {})

    def test_to_pct_from_counts_handles_zero_denominator(self) -> None:
        self.assertIsNone(to_pct_from_counts(10, 0))

    def test_to_pct_from_counts_valid_case(self) -> None:
        self.assertEqual(to_pct_from_counts(1, 4), 25.0)

    def test_normalize_distribution_rejects_non_int_values(self) -> None:
        self.assertIsNone(normalize_distribution({"1": 1.5}))

    def test_normalize_distribution_accepts_numeric_string_keys(self) -> None:
        self.assertEqual(normalize_distribution({"2": 1, "1": 3}), {"1": 3, "2": 1})

    def test_count_input_source_records_handles_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input_source.json"
            path.write_text(json.dumps([{"a": 1}, {"a": 2}, "x"]), encoding="utf-8")
            self.assertEqual(count_input_source_records(path), 2)

    def test_count_input_source_records_handles_nested_records_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input_source.json"
            path.write_text(json.dumps({"records": [{"a": 1}, {"a": 2}, None]}), encoding="utf-8")
            self.assertEqual(count_input_source_records(path), 2)

    def test_count_unique_source_ipg_groups_empty_when_no_ipg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input_source.json"
            path.write_text(json.dumps([{"name": "a"}, {"name": "b"}]), encoding="utf-8")
            self.assertEqual(count_unique_source_ipg_groups(path), 2)

    def test_build_entity_size_distribution_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.csv"
            self.assertEqual(build_entity_size_distribution(path), {})

    def test_compute_expected_run_metrics_missing_run_dir_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run = {"run_id": "20990101_000000__missing_run"}
            expected = compute_expected_run_metrics(run, Path(tmp))
            self.assertIn("from_files", expected)
            self.assertIn("from_ground_truth", expected)
            self.assertIn("from_discovery", expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Optional regression snapshot checks for dashboard KPIs.

Enable with env var: MVP_ENFORCE_REGRESSION_SNAPSHOT=1
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from typing import Any

from testing.dashboard_assertions import parse_dashboard_data_js

TOLERANCE = 0.01


def latest_by_source(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for run in runs:
        source = str(run.get("source_input_name") or "").strip()
        run_id = str(run.get("run_id") or "").strip()
        if not source or not run_id:
            continue
        current = latest.get(source)
        if current is None or str(current.get("run_id") or "") < run_id:
            latest[source] = run
    return latest


class DashboardRegressionSnapshotTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        enforce = os.environ.get("MVP_ENFORCE_REGRESSION_SNAPSHOT", "0").strip()
        if enforce not in {"1", "true", "TRUE", "yes", "YES"}:
            raise unittest.SkipTest("Regression snapshot checks disabled (set MVP_ENFORCE_REGRESSION_SNAPSHOT=1 to enable)")

        cls.mvp_root = Path(__file__).resolve().parents[1]
        snapshot_path = cls.mvp_root / "testing" / "snapshots" / "dashboard_regression_snapshot.json"
        if not snapshot_path.exists():
            raise unittest.SkipTest(f"Snapshot file not found: {snapshot_path}")

        dashboard_data_env = os.environ.get("MVP_DASHBOARD_DATA_PATH", "").strip()
        dashboard_data_path = (
            Path(dashboard_data_env).expanduser()
            if dashboard_data_env
            else cls.mvp_root / "dashboard" / "management_dashboard_data.js"
        )
        if not dashboard_data_path.is_absolute():
            dashboard_data_path = cls.mvp_root / dashboard_data_path

        cls.snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        cls.payload = parse_dashboard_data_js(dashboard_data_path.resolve())

        runs = [run for run in (cls.payload.get("runs") or []) if isinstance(run, dict)]
        cls.latest_source_runs = latest_by_source(runs)

    def assert_numeric_close(self, source: str, key: str, current: Any, expected: Any) -> None:
        if expected is None:
            self.assertIsNone(current, f"{source}: expected None for {key}, got {current}")
            return
        self.assertIsInstance(current, (int, float), f"{source}: expected numeric current value for {key}")
        delta = abs(float(current) - float(expected))
        self.assertLessEqual(delta, TOLERANCE, f"{source}: mismatch for {key} current={current} expected={expected}")

    def test_snapshot_sources_present_in_current_payload(self) -> None:
        snapshot_sources = self.snapshot.get("sources") if isinstance(self.snapshot.get("sources"), dict) else {}
        for source_name in snapshot_sources.keys():
            with self.subTest(source=source_name):
                self.assertIn(source_name, self.latest_source_runs, f"Source missing from current payload: {source_name}")

    def test_snapshot_metric_values_match(self) -> None:
        snapshot_sources = self.snapshot.get("sources") if isinstance(self.snapshot.get("sources"), dict) else {}
        metric_keys = (
            "records_input",
            "our_resolved_entities",
            "resolved_entities",
            "matched_pairs",
            "pair_precision_pct",
            "pair_recall_pct",
            "true_positive",
            "false_positive",
            "false_negative",
            "our_true_positive",
            "our_false_positive",
            "our_false_negative",
            "our_match_coverage_pct",
            "extra_true_matches_found",
            "extra_false_matches_found",
            "extra_gain_vs_known_pct",
        )
        for source_name, expected in snapshot_sources.items():
            if source_name not in self.latest_source_runs:
                continue
            current = self.latest_source_runs[source_name]
            with self.subTest(source=source_name):
                for key in metric_keys:
                    expected_value = expected.get(key)
                    current_value = current.get(key)
                    if isinstance(expected_value, (int, float)):
                        self.assert_numeric_close(source_name, key, current_value, expected_value)
                    else:
                        self.assertEqual(
                            current_value,
                            expected_value,
                            f"{source_name}: mismatch for {key} current={current_value} expected={expected_value}",
                        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

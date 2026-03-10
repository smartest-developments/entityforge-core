"""Cross-check consistency between unittest suite inputs and verify_dashboard_metrics output."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from testing.dashboard_assertions import parse_dashboard_data_js


class DashboardCrossToolConsistencyTestCase(unittest.TestCase):
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

        output_root_env = os.environ.get("MVP_OUTPUT_ROOT", "").strip()
        if output_root_env:
            output_root = Path(output_root_env).expanduser()
            if not output_root.is_absolute():
                output_root = cls.mvp_root / output_root
        else:
            output_root = cls.mvp_root / "output"
        cls.output_root = output_root.resolve()

        cls.payload = parse_dashboard_data_js(cls.dashboard_data_path)
        cls.dashboard_runs = [run for run in (cls.payload.get("runs") or []) if isinstance(run, dict)]
        cls.success_run_ids = [str(run.get("run_id") or "") for run in cls.dashboard_runs if run.get("run_status") == "success"]

        cls.tmpdir = tempfile.TemporaryDirectory()
        tmp_root = Path(cls.tmpdir.name)
        cls.audit_json_path = tmp_root / "audit_report.json"
        cls.audit_md_path = tmp_root / "audit_report.md"

        cmd = [
            sys.executable,
            str(cls.mvp_root / "app" / "verify_dashboard_metrics.py"),
            "--output-root",
            str(cls.output_root),
            "--dashboard-data",
            str(cls.dashboard_data_path),
            "--report-json",
            str(cls.audit_json_path),
            "--report-md",
            str(cls.audit_md_path),
        ]
        proc = subprocess.run(cmd, cwd=str(cls.mvp_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        cls.audit_returncode = proc.returncode
        cls.audit_stdout = proc.stdout
        cls.audit_stderr = proc.stderr
        cls.audit_payload = json.loads(cls.audit_json_path.read_text(encoding="utf-8")) if cls.audit_json_path.exists() else {}

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmpdir.cleanup()

    def test_verify_dashboard_metrics_exit_code_is_zero(self) -> None:
        self.assertEqual(
            self.audit_returncode,
            0,
            f"verify_dashboard_metrics.py failed with exit code {self.audit_returncode}\nSTDOUT:\n{self.audit_stdout}\nSTDERR:\n{self.audit_stderr}",
        )

    def test_verify_report_summary_has_no_failures(self) -> None:
        summary = self.audit_payload.get("summary") if isinstance(self.audit_payload.get("summary"), dict) else {}
        self.assertEqual(summary.get("runs_fail"), 0, "Audit summary reports failing runs")

    def test_verify_report_run_count_matches_dashboard_runs(self) -> None:
        audited_runs = self.audit_payload.get("runs") if isinstance(self.audit_payload.get("runs"), list) else []
        self.assertEqual(len(audited_runs), len(self.dashboard_runs), "Audit run count differs from dashboard run count")

    def test_verify_report_run_ids_match_dashboard_run_ids(self) -> None:
        audited_runs = self.audit_payload.get("runs") if isinstance(self.audit_payload.get("runs"), list) else []
        audited_ids = [str(run.get("run_id") or "") for run in audited_runs if isinstance(run, dict)]
        dashboard_ids = [str(run.get("run_id") or "") for run in self.dashboard_runs]
        self.assertEqual(sorted(audited_ids), sorted(dashboard_ids), "Audit run IDs differ from dashboard run IDs")

    def test_verify_checks_have_no_fail_status(self) -> None:
        audited_runs = self.audit_payload.get("runs") if isinstance(self.audit_payload.get("runs"), list) else []
        failures: list[str] = []
        for run in audited_runs:
            if not isinstance(run, dict):
                continue
            run_id = str(run.get("run_id") or "")
            for check in run.get("checks") or []:
                if not isinstance(check, dict):
                    continue
                if check.get("status") == "FAIL":
                    failures.append(f"{run_id}: {check.get('name')}")
        self.assertEqual(failures, [], f"Audit contains failing checks: {failures}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

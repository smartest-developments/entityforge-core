#!/usr/bin/env python3
"""Run MVP dashboard validation suite and emit machine/human reports."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import unittest
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run automated tests for MVP dashboard metric correctness")
    parser.add_argument("--output-root", default="output", help="MVP output root directory (default: output)")
    parser.add_argument(
        "--dashboard-data",
        default="dashboard/management_dashboard_data.js",
        help="Path to dashboard data JS (default: dashboard/management_dashboard_data.js)",
    )
    parser.add_argument(
        "--report-json",
        default="dashboard/dashboard_test_suite_report.json",
        help="Output JSON report path",
    )
    parser.add_argument(
        "--report-md",
        default="dashboard/dashboard_test_suite_report.md",
        help="Output Markdown report path",
    )
    parser.add_argument("--verbosity", type=int, default=2, help="unittest verbosity (default: 2)")
    return parser.parse_args()


def to_abs_path(mvp_root: Path, raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (mvp_root / path).resolve()


def serialize_result(result: unittest.result.TestResult) -> dict[str, Any]:
    return {
        "tests_run": result.testsRun,
        "failures": [
            {
                "test": test.id(),
                "traceback": traceback_text,
            }
            for test, traceback_text in result.failures
        ],
        "errors": [
            {
                "test": test.id(),
                "traceback": traceback_text,
            }
            for test, traceback_text in result.errors
        ],
        "skipped": [
            {
                "test": test.id(),
                "reason": reason,
            }
            for test, reason in result.skipped
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines: list[str] = []
    lines.append("# Dashboard Test Suite Report")
    lines.append("")
    lines.append(f"- Generated at: {report['generated_at']}")
    lines.append(f"- Dashboard data: `{report['dashboard_data']}`")
    lines.append(f"- Output root: `{report['output_root']}`")
    lines.append(f"- Tests run: {summary['tests_run']}")
    lines.append(f"- Failures: {summary['failures']}")
    lines.append(f"- Errors: {summary['errors']}")
    lines.append(f"- Skipped: {summary['skipped']}")
    lines.append(f"- Status: **{summary['status']}**")
    lines.append("")

    if report["failures"]:
        lines.append("## Failures")
        lines.append("")
        for item in report["failures"]:
            lines.append(f"### {item['test']}")
            lines.append("")
            lines.append("```text")
            lines.append(item["traceback"].rstrip())
            lines.append("```")
            lines.append("")

    if report["errors"]:
        lines.append("## Errors")
        lines.append("")
        for item in report["errors"]:
            lines.append(f"### {item['test']}")
            lines.append("")
            lines.append("```text")
            lines.append(item["traceback"].rstrip())
            lines.append("```")
            lines.append("")

    if report["skipped"]:
        lines.append("## Skipped")
        lines.append("")
        for item in report["skipped"]:
            lines.append(f"- `{item['test']}`: {item['reason']}")
        lines.append("")

    lines.append("## Re-run")
    lines.append("")
    lines.append("```bash")
    lines.append("cd MVP")
    lines.append("python3 testing/run_dashboard_tests.py")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parents[1]

    output_root = to_abs_path(mvp_root, args.output_root)
    dashboard_data = to_abs_path(mvp_root, args.dashboard_data)
    report_json = to_abs_path(mvp_root, args.report_json)
    report_md = to_abs_path(mvp_root, args.report_md)

    os.environ["MVP_OUTPUT_ROOT"] = str(output_root)
    os.environ["MVP_DASHBOARD_DATA_PATH"] = str(dashboard_data)

    sys.path.insert(0, str(mvp_root))

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(mvp_root / "testing"), pattern="test_*.py", top_level_dir=str(mvp_root))
    runner = unittest.TextTestRunner(verbosity=args.verbosity)
    result = runner.run(suite)

    serialized = serialize_result(result)
    status = "PASS" if result.wasSuccessful() else "FAIL"
    report: dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "output_root": str(output_root),
        "dashboard_data": str(dashboard_data),
        "summary": {
            "tests_run": serialized["tests_run"],
            "failures": len(serialized["failures"]),
            "errors": len(serialized["errors"]),
            "skipped": len(serialized["skipped"]),
            "status": status,
        },
        "failures": serialized["failures"],
        "errors": serialized["errors"],
        "skipped": serialized["skipped"],
    }

    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_md.write_text(render_markdown(report), encoding="utf-8")

    print(f"Dashboard test JSON report: {report_json}")
    print(f"Dashboard test Markdown report: {report_md}")
    print(
        "Tests run: "
        f"{report['summary']['tests_run']} | "
        f"Failures: {report['summary']['failures']} | "
        f"Errors: {report['summary']['errors']} | "
        f"Skipped: {report['summary']['skipped']}"
    )

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

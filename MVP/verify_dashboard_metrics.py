#!/usr/bin/env python3
"""Audit dashboard metrics against raw technical artifacts."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify dashboard KPI values against MVP output artifacts.")
    parser.add_argument("--output-root", default="output", help="MVP output root directory (default: output)")
    parser.add_argument(
        "--dashboard-data",
        default="dashboard/management_dashboard_data.js",
        help="Path to management_dashboard_data.js",
    )
    parser.add_argument(
        "--report-json",
        default="dashboard/dashboard_data_audit_report.json",
        help="Output JSON report path",
    )
    parser.add_argument(
        "--report-md",
        default="dashboard/dashboard_data_audit_report.md",
        help="Output Markdown report path",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.01,
        help="Numeric tolerance for float comparisons in percentage points (default: 0.01)",
    )
    return parser.parse_args()


def is_close(a: float, b: float, tolerance: float) -> bool:
    return abs(a - b) <= tolerance


def pct(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return round((numerator / denominator) * 100.0, 2)


def parse_dashboard_data_js(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    prefix = "window.MVP_DASHBOARD_DATA = "
    if not raw.startswith(prefix):
        raise ValueError(f"Unexpected dashboard data format in {path}")
    payload = raw[len(prefix) :].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise TypeError("Dashboard payload is not an object")
    return data


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def count_jsonl_rows(path: Path) -> int | None:
    if not path.exists():
        return None
    count = 0
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                count += 1
    return count


def count_csv_rows(path: Path) -> int | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.reader(infile)
        next(reader, None)
        return sum(1 for _ in reader)


def count_unique_resolved_entities(path: Path) -> int | None:
    if not path.exists():
        return None
    values: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            value = str(row.get("resolved_entity_id") or "").strip()
            if value:
                values.add(value)
    return len(values)


def count_entity_size_distribution_total(path: Path) -> int | None:
    if not path.exists():
        return None
    values: dict[str, int] = {}
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            entity_id = str(row.get("resolved_entity_id") or "").strip()
            if not entity_id:
                continue
            values[entity_id] = values.get(entity_id, 0) + 1
    # Number of entities represented by the distribution equals number of unique entity IDs.
    return len(values)


def dashboard_distribution_total(distribution: Any) -> int | None:
    if not isinstance(distribution, dict):
        return None
    total = 0
    for value in distribution.values():
        if isinstance(value, (int, float)):
            total += int(value)
        else:
            return None
    return total


def evaluate_check(
    name: str,
    dashboard_value: Any,
    recomputed_value: Any,
    source: str,
    tolerance: float,
) -> dict[str, Any]:
    if dashboard_value is None or recomputed_value is None:
        status = "SKIP"
        passed = None
    elif isinstance(dashboard_value, (int, float)) and isinstance(recomputed_value, (int, float)):
        passed = is_close(float(dashboard_value), float(recomputed_value), tolerance)
        status = "PASS" if passed else "FAIL"
    else:
        passed = dashboard_value == recomputed_value
        status = "PASS" if passed else "FAIL"
    return {
        "name": name,
        "dashboard": dashboard_value,
        "recomputed": recomputed_value,
        "status": status,
        "source": source,
    }


def audit_run(run: dict[str, Any], output_root: Path, tolerance: float) -> dict[str, Any]:
    run_id = str(run.get("run_id") or "").strip()
    run_dir = output_root / run_id
    technical_dir = run_dir / "technical output"

    management_summary = read_json(technical_dir / "management_summary.json")
    ground_truth = read_json(technical_dir / "ground_truth_match_quality.json")
    pair_metrics = ground_truth.get("pair_metrics") if isinstance(ground_truth.get("pair_metrics"), dict) else {}
    discovery_metrics = (
        management_summary.get("discovery_metrics") if isinstance(management_summary.get("discovery_metrics"), dict) else {}
    )

    tp = pair_metrics.get("true_positive") if isinstance(pair_metrics.get("true_positive"), int) else None
    fp = pair_metrics.get("false_positive") if isinstance(pair_metrics.get("false_positive"), int) else None
    fn = pair_metrics.get("false_negative") if isinstance(pair_metrics.get("false_negative"), int) else None
    predicted = pair_metrics.get("predicted_pairs_labeled") if isinstance(pair_metrics.get("predicted_pairs_labeled"), int) else None
    matched_pairs = management_summary.get("matched_pairs") if isinstance(management_summary.get("matched_pairs"), int) else None
    resolved_entities = management_summary.get("resolved_entities") if isinstance(management_summary.get("resolved_entities"), int) else None
    records_input = management_summary.get("records_input") if isinstance(management_summary.get("records_input"), int) else None
    our_tp = discovery_metrics.get("known_pairs_ipg") if isinstance(discovery_metrics.get("known_pairs_ipg"), int) else None
    our_total = discovery_metrics.get("true_pairs_total") if isinstance(discovery_metrics.get("true_pairs_total"), int) else None

    recomputed = {
        "records_input": count_jsonl_rows(technical_dir / "input_normalized.jsonl"),
        "matched_pairs": count_csv_rows(technical_dir / "matched_pairs.csv"),
        "resolved_entities": count_unique_resolved_entities(technical_dir / "entity_records.csv"),
        "entity_size_distribution_total": count_entity_size_distribution_total(technical_dir / "entity_records.csv"),
        "pair_precision_pct": pct(tp, (tp or 0) + (fp or 0)) if tp is not None and fp is not None else None,
        "overall_false_positive_pct": pct(fp, predicted),
        "pair_recall_pct": pct(tp, (tp or 0) + (fn or 0)) if tp is not None and fn is not None else None,
        "our_match_coverage_pct": pct(our_tp, our_total),
        "our_true_positive": our_tp,
        "our_true_pairs_total": our_total,
        "false_positive": fp,
        "false_negative": fn,
        "true_positive": tp,
        "predicted_pairs_labeled": predicted,
        "management_records_input": records_input,
        "management_matched_pairs": matched_pairs,
        "management_resolved_entities": resolved_entities,
    }

    checks = [
        evaluate_check(
            "Input Records",
            run.get("records_input"),
            recomputed["records_input"],
            "technical output/input_normalized.jsonl",
            tolerance,
        ),
        evaluate_check(
            "Matched Pairs",
            run.get("matched_pairs"),
            recomputed["matched_pairs"],
            "technical output/matched_pairs.csv",
            tolerance,
        ),
        evaluate_check(
            "Resolved Entities",
            run.get("resolved_entities"),
            recomputed["resolved_entities"],
            "technical output/entity_records.csv",
            tolerance,
        ),
        evaluate_check(
            "Entity Size Distribution Total",
            dashboard_distribution_total(run.get("entity_size_distribution")),
            recomputed["entity_size_distribution_total"],
            "technical output/entity_records.csv",
            tolerance,
        ),
        evaluate_check(
            "Their Match Found (%)",
            run.get("pair_precision_pct"),
            recomputed["pair_precision_pct"],
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Their False Positive (%)",
            run.get("overall_false_positive_pct"),
            recomputed["overall_false_positive_pct"],
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Their Match Missed (%)",
            None if run.get("pair_recall_pct") is None else round(100.0 - float(run.get("pair_recall_pct")), 2),
            None if recomputed["pair_recall_pct"] is None else round(100.0 - float(recomputed["pair_recall_pct"]), 2),
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Our Match Found (%)",
            run.get("our_match_coverage_pct"),
            recomputed["our_match_coverage_pct"],
            "technical output/management_summary.json (discovery_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Our Matched Pairs",
            run.get("our_true_positive"),
            recomputed["our_true_positive"],
            "technical output/management_summary.json (discovery_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Their True Positive",
            run.get("true_positive"),
            recomputed["true_positive"],
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Their False Positive",
            run.get("false_positive"),
            recomputed["false_positive"],
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
        evaluate_check(
            "Their False Negative",
            run.get("false_negative"),
            recomputed["false_negative"],
            "technical output/ground_truth_match_quality.json (pair_metrics)",
            tolerance,
        ),
    ]

    has_fail = any(item["status"] == "FAIL" for item in checks)
    all_skip = all(item["status"] == "SKIP" for item in checks)
    overall_status = "SKIP" if all_skip else ("FAIL" if has_fail else "PASS")

    return {
        "run_id": run_id,
        "run_label": run.get("run_label"),
        "source_input_name": run.get("source_input_name"),
        "run_status": run.get("run_status"),
        "overall_status": overall_status,
        "checks": checks,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Dashboard Data Audit Report")
    lines.append("")
    lines.append(f"- Generated at: {report['generated_at']}")
    lines.append(f"- Output root: `{report['output_root']}`")
    lines.append(f"- Dashboard data: `{report['dashboard_data']}`")
    lines.append(f"- Runs audited: {report['summary']['runs_total']}")
    lines.append(f"- Runs PASS: {report['summary']['runs_pass']}")
    lines.append(f"- Runs FAIL: {report['summary']['runs_fail']}")
    lines.append(f"- Runs SKIP: {report['summary']['runs_skip']}")
    lines.append("")
    lines.append("## Run Summary")
    lines.append("")
    lines.append("| Run ID | Source Input | Status |")
    lines.append("|---|---|---|")
    for run in report["runs"]:
        lines.append(
            f"| `{run['run_id']}` | `{run.get('source_input_name') or ''}` | **{run['overall_status']}** |"
        )
    lines.append("")
    lines.append("## Failed Checks")
    lines.append("")
    failed = []
    for run in report["runs"]:
        for check in run["checks"]:
            if check["status"] == "FAIL":
                failed.append((run["run_id"], check))

    if not failed:
        lines.append("No failed checks.")
    else:
        lines.append("| Run ID | Check | Dashboard | Recomputed | Source |")
        lines.append("|---|---|---:|---:|---|")
        for run_id, check in failed:
            lines.append(
                f"| `{run_id}` | {check['name']} | {check['dashboard']} | {check['recomputed']} | `{check['source']}` |"
            )
    lines.append("")
    lines.append("## Re-run")
    lines.append("")
    lines.append("```bash")
    lines.append("cd MVP")
    lines.append("python3 verify_dashboard_metrics.py")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parent
    output_root = (mvp_root / args.output_root).resolve()
    dashboard_data_path = (mvp_root / args.dashboard_data).resolve()
    report_json_path = (mvp_root / args.report_json).resolve()
    report_md_path = (mvp_root / args.report_md).resolve()

    payload = parse_dashboard_data_js(dashboard_data_path)
    runs = payload.get("runs") if isinstance(payload.get("runs"), list) else []

    audited_runs = [audit_run(run, output_root, args.tolerance) for run in runs if isinstance(run, dict)]
    runs_pass = sum(1 for run in audited_runs if run["overall_status"] == "PASS")
    runs_fail = sum(1 for run in audited_runs if run["overall_status"] == "FAIL")
    runs_skip = sum(1 for run in audited_runs if run["overall_status"] == "SKIP")

    report = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "output_root": str(output_root),
        "dashboard_data": str(dashboard_data_path),
        "summary": {
            "runs_total": len(audited_runs),
            "runs_pass": runs_pass,
            "runs_fail": runs_fail,
            "runs_skip": runs_skip,
        },
        "runs": audited_runs,
    }

    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_md_path.parent.mkdir(parents=True, exist_ok=True)
    report_json_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_md_path.write_text(render_markdown(report), encoding="utf-8")

    print(f"Audit JSON: {report_json_path}")
    print(f"Audit Markdown: {report_md_path}")
    print(
        f"Runs audited: {len(audited_runs)} | PASS: {runs_pass} | FAIL: {runs_fail} | SKIP: {runs_skip}"
    )
    return 1 if runs_fail > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())

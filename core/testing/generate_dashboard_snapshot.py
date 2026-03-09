#!/usr/bin/env python3
"""Generate a regression snapshot from dashboard data (latest run per source)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

PREFIX = "window.MVP_DASHBOARD_DATA = "


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate dashboard regression snapshot")
    parser.add_argument("--dashboard-data", default="dashboard/management_dashboard_data.js")
    parser.add_argument("--snapshot-path", default="testing/snapshots/dashboard_regression_snapshot.json")
    return parser.parse_args()


def parse_dashboard_data(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith(PREFIX):
        raise ValueError(f"Unexpected dashboard data format: {path}")
    payload = raw[len(PREFIX) :].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise TypeError("Dashboard data payload must be an object")
    return data


def latest_by_source(runs: list[dict]) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for run in runs:
        source = str(run.get("source_input_name") or "").strip()
        run_id = str(run.get("run_id") or "").strip()
        if not source or not run_id:
            continue
        current = latest.get(source)
        if current is None or str(current.get("run_id") or "") < run_id:
            latest[source] = run
    return latest


def build_snapshot(data: dict) -> dict:
    runs = [run for run in (data.get("runs") or []) if isinstance(run, dict)]
    per_source = latest_by_source(runs)

    snapshot_sources: dict[str, dict] = {}
    keep_fields = (
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

    for source, run in sorted(per_source.items()):
        item = {"run_id": run.get("run_id")}
        for key in keep_fields:
            item[key] = run.get(key)
        snapshot_sources[source] = item

    summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "sources_count": len(snapshot_sources),
        "sources": snapshot_sources,
        "summary": {
            "runs_total": summary.get("runs_total"),
            "quality_runs_total": summary.get("quality_runs_total"),
            "records_input_total": summary.get("records_input_total"),
            "matched_pairs_total": summary.get("matched_pairs_total"),
            "avg_pair_precision_pct": summary.get("avg_pair_precision_pct"),
            "avg_pair_recall_pct": summary.get("avg_pair_recall_pct"),
        },
    }


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parents[1]
    dashboard_data = (mvp_root / args.dashboard_data).resolve()
    snapshot_path = (mvp_root / args.snapshot_path).resolve()

    data = parse_dashboard_data(dashboard_data)
    snapshot = build_snapshot(data)

    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Snapshot generated: {snapshot_path}")
    print(f"Sources included: {snapshot['sources_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

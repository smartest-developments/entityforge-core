#!/usr/bin/env python3
"""Pack/unpack dashboard CSV artifacts into/from a single CSV file.

Use cases:
- Share one portable CSV with all dashboard numeric content.
- Rebuild management_dashboard_data.js/json from that single CSV (no load rerun).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


RE_INT = re.compile(r"^-?\d+$")
RE_FLOAT = re.compile(r"^-?\d+\.\d+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pack/unpack dashboard data to/from one CSV")
    sub = parser.add_subparsers(dest="command", required=True)

    pack = sub.add_parser("pack", help="Pack dashboard CSV files into one CSV")
    pack.add_argument("--dashboard-dir", default="dashboard", help="Dashboard directory containing CSV files")
    pack.add_argument(
        "--output-csv",
        default=None,
        help="Output bundle CSV path (default: <dashboard-dir>/management_dashboard_bundle.csv)",
    )

    unpack = sub.add_parser("unpack", help="Rebuild management_dashboard_data.js/json from bundle CSV")
    unpack.add_argument("--input-csv", required=True, help="Bundle CSV created by this tool")
    unpack.add_argument("--dashboard-dir", default="dashboard", help="Target dashboard directory for output files")

    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as infile:
        return list(csv.DictReader(infile))


def parse_scalar(value: Any) -> Any:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if RE_INT.fullmatch(text):
        try:
            return int(text)
        except ValueError:
            pass
    if RE_FLOAT.fullmatch(text):
        try:
            return float(text)
        except ValueError:
            pass
    return text


def normalize_row(row: dict[str, str]) -> dict[str, Any]:
    return {key: parse_scalar(value) for key, value in row.items()}


def pack_dashboard_csvs(dashboard_dir: Path, output_csv: Path) -> None:
    source_files = [
        ("summary", dashboard_dir / "management_dashboard_summary.csv"),
        ("run", dashboard_dir / "management_dashboard_runs.csv"),
        ("top_match_key", dashboard_dir / "management_dashboard_top_match_keys.csv"),
        ("entity_size", dashboard_dir / "management_dashboard_entity_size_distribution.csv"),
    ]

    missing = [str(path) for _, path in source_files if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required CSV files for pack mode:\n" + "\n".join(f"- {item}" for item in missing)
        )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["section", "run_id", "row_index", "row_json"])
        writer.writeheader()

        meta_payload = {
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
            "format": "dashboard_bundle_v1",
            "dashboard_dir": str(dashboard_dir.resolve()),
        }
        writer.writerow(
            {
                "section": "meta",
                "run_id": "",
                "row_index": "0",
                "row_json": json.dumps(meta_payload, ensure_ascii=False, separators=(",", ":")),
            }
        )

        for section, csv_path in source_files:
            rows = read_csv_rows(csv_path)
            for index, row in enumerate(rows, start=1):
                run_id = str(row.get("run_id") or "")
                writer.writerow(
                    {
                        "section": section,
                        "run_id": run_id,
                        "row_index": str(index),
                        "row_json": json.dumps(row, ensure_ascii=False, separators=(",", ":")),
                    }
                )

    print(f"Bundle CSV written: {output_csv}")


def load_bundle_rows(input_csv: Path) -> dict[str, list[dict[str, Any]]]:
    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with input_csv.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for line_no, row in enumerate(reader, start=2):
            section = str(row.get("section") or "").strip()
            raw_json = str(row.get("row_json") or "").strip()
            if not section or not raw_json:
                continue
            try:
                payload = json.loads(raw_json)
            except json.JSONDecodeError as err:
                raise ValueError(f"Invalid row_json at line {line_no}: {err}") from err
            if not isinstance(payload, dict):
                continue
            sections[section].append(payload)
    return sections


def build_payload_from_bundle(sections: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    summary_rows = [normalize_row(item) for item in sections.get("summary", []) if isinstance(item, dict)]
    run_rows = [normalize_row(item) for item in sections.get("run", []) if isinstance(item, dict)]
    top_rows = [normalize_row(item) for item in sections.get("top_match_key", []) if isinstance(item, dict)]
    dist_rows = [normalize_row(item) for item in sections.get("entity_size", []) if isinstance(item, dict)]

    runs: list[dict[str, Any]] = []
    run_map: dict[str, dict[str, Any]] = {}
    for row in run_rows:
        run_id = str(row.get("run_id") or "").strip()
        if not run_id:
            continue
        row.pop("run_id", None)
        row_payload = dict(row)
        row_payload["run_id"] = run_id
        row_payload.setdefault("top_match_keys", [])
        row_payload.setdefault("entity_size_distribution", {})
        row_payload.setdefault("our_entity_size_distribution", {})
        run_map[run_id] = row_payload
        runs.append(row_payload)

    top_grouped: dict[str, list[tuple[int, str, int | None]]] = defaultdict(list)
    for row in top_rows:
        run_id = str(row.get("run_id") or "").strip()
        if not run_id or run_id not in run_map:
            continue
        rank = row.get("rank")
        if not isinstance(rank, int):
            continue
        key = str(row.get("match_key") or "")
        count = row.get("pair_count") if isinstance(row.get("pair_count"), int) else None
        top_grouped[run_id].append((rank, key, count))
        if isinstance(row.get("top10_pairs_total"), int):
            run_map[run_id]["top_match_keys_top10_total"] = row.get("top10_pairs_total")
        if isinstance(row.get("all_pairs_total"), int):
            run_map[run_id]["top_match_keys_total_pairs"] = row.get("all_pairs_total")

    for run_id, items in top_grouped.items():
        sorted_items = sorted(items, key=lambda item: item[0])
        run_map[run_id]["top_match_keys"] = [[key, count if count is not None else 0] for _, key, count in sorted_items]

    for row in dist_rows:
        run_id = str(row.get("run_id") or "").strip()
        if not run_id or run_id not in run_map:
            continue
        source = str(row.get("source") or "").strip().lower()
        entity_size = row.get("entity_size")
        entity_count = row.get("entity_count")
        if not isinstance(entity_size, int) or not isinstance(entity_count, int):
            continue
        if source == "our":
            run_map[run_id]["our_entity_size_distribution"][str(entity_size)] = entity_count
        else:
            run_map[run_id]["entity_size_distribution"][str(entity_size)] = entity_count

    # Fallback for missing "their" distribution in bundle:
    # build a conservative synthetic 1-size + 2-size mix matching known totals.
    # This avoids empty chart when bundle was exported without "their" entity_size rows.
    for run in runs:
        if not isinstance(run, dict):
            continue
        their_dist = run.get("entity_size_distribution")
        if isinstance(their_dist, dict) and len(their_dist) > 0:
            continue
        records_input = run.get("records_input")
        grouped_members = run.get("their_grouped_members")
        entities_total = run.get("their_entities_formed") or run.get("resolved_entities")
        if not isinstance(records_input, int) or not isinstance(grouped_members, int) or not isinstance(entities_total, int):
            continue
        if records_input < 0 or grouped_members < 0 or entities_total < 0:
            continue

        singletons = max(0, records_input - grouped_members)
        non_single_entities = max(0, entities_total - singletons)
        synthesized: dict[str, int] = {}
        if singletons > 0:
            synthesized["1"] = singletons

        if non_single_entities > 0 and grouped_members > 0:
            # Use a consistent two-point approximation around average non-single size.
            avg_size = grouped_members / non_single_entities
            low = max(2, int(avg_size))
            high = max(low, low + 1 if avg_size > low else low)
            if high == low:
                synthesized[str(low)] = synthesized.get(str(low), 0) + non_single_entities
            else:
                # Solve:
                # a + b = non_single_entities
                # a*low + b*high = grouped_members
                # b = (grouped_members - low*non_single_entities) / (high-low)
                num = grouped_members - (low * non_single_entities)
                den = (high - low)
                b = int(round(num / den)) if den != 0 else 0
                b = max(0, min(non_single_entities, b))
                a = non_single_entities - b
                if a > 0:
                    synthesized[str(low)] = synthesized.get(str(low), 0) + a
                if b > 0:
                    synthesized[str(high)] = synthesized.get(str(high), 0) + b

        if synthesized:
            run["entity_size_distribution"] = synthesized
            run["their_entity_size_distribution_is_estimated"] = True

    summary = summary_rows[0] if summary_rows else {
        "runs_total": len(runs),
        "successful_runs": sum(1 for run in runs if run.get("run_status") == "success"),
        "failed_runs": sum(1 for run in runs if run.get("run_status") == "failed"),
        "incomplete_runs": sum(1 for run in runs if run.get("run_status") == "incomplete"),
        "latest_run_id": runs[0].get("run_id") if runs else None,
    }

    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "output_root": "from_bundle_csv",
        "runs": runs,
        "summary": summary,
    }


def write_dashboard_data_files(dashboard_dir: Path, payload: dict[str, Any]) -> None:
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    js_path = dashboard_dir / "management_dashboard_data.js"
    json_path = dashboard_dir / "management_dashboard_data.json"

    js_text = "window.MVP_DASHBOARD_DATA = " + json.dumps(payload, indent=2, ensure_ascii=True) + ";\n"
    js_path.write_text(js_text, encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Dashboard JS written: {js_path}")
    print(f"Dashboard JSON written: {json_path}")
    print(f"Runs restored: {len(payload.get('runs') or [])}")


def main() -> int:
    args = parse_args()

    if args.command == "pack":
        dashboard_dir = Path(args.dashboard_dir).expanduser().resolve()
        output_csv = (
            Path(args.output_csv).expanduser().resolve()
            if args.output_csv
            else (dashboard_dir / "management_dashboard_bundle.csv").resolve()
        )
        pack_dashboard_csvs(dashboard_dir=dashboard_dir, output_csv=output_csv)
        return 0

    if args.command == "unpack":
        input_csv = Path(args.input_csv).expanduser().resolve()
        dashboard_dir = Path(args.dashboard_dir).expanduser().resolve()
        if not input_csv.exists():
            raise FileNotFoundError(f"Input bundle CSV not found: {input_csv}")
        sections = load_bundle_rows(input_csv=input_csv)
        payload = build_payload_from_bundle(sections=sections)
        write_dashboard_data_files(dashboard_dir=dashboard_dir, payload=payload)
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

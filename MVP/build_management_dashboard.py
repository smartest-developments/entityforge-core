#!/usr/bin/env python3
"""Build a static, local-first dashboard data file from MVP output runs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import csv
import subprocess
import sys
import functools
from pathlib import Path

RUN_DIR_RE = re.compile(r"^(?P<ts>\d{8}_\d{6})(?:__(?P<label>[A-Za-z0-9._-]+))?$")
STATIC_DASHBOARD_FILES = (
    "management_dashboard.html",
    "management_dashboard.css",
    "management_dashboard.js",
    "metrics_validation_guide.html",
    "tabler.min.css",
    "tabler.min.js",
    "chart.umd.js",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build management dashboard data from MVP outputs")
    parser.add_argument("--output-root", default="output", help="Output root containing timestamped run folders")
    parser.add_argument(
        "--dashboard-dir",
        default="dashboard",
        help="Dashboard directory under MVP root (self-contained, ready to open)",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip automated dashboard metric test suite after rebuild",
    )
    parser.add_argument(
        "--skip-audit",
        action="store_true",
        help="Skip verify_dashboard_metrics cross-check after rebuild",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def parse_run_datetime(run_id: str) -> str | None:
    match = RUN_DIR_RE.match(run_id)
    timestamp = match.group("ts") if match else run_id
    try:
        return dt.datetime.strptime(timestamp, "%Y%m%d_%H%M%S").isoformat(timespec="seconds")
    except ValueError:
        return None


def to_num(value: object) -> float | int | None:
    if isinstance(value, (int, float)):
        return value
    return None


def pct(value: object) -> float | None:
    number = to_num(value)
    if number is None:
        return None
    return round(float(number) * 100.0, 2)


def safe_ratio(num: int | float | None, den: int | float | None) -> float | None:
    if not isinstance(num, (int, float)) or not isinstance(den, (int, float)) or den <= 0:
        return None
    return float(num) / float(den)


def is_close(a: float | int | None, b: float | int | None, tol: float = 0.01) -> bool:
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return False
    return abs(float(a) - float(b)) <= tol


def count_jsonl_rows(path: Path) -> int | None:
    if not path.exists():
        return None
    rows = 0
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                rows += 1
    return rows


def count_csv_rows(path: Path) -> int | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as infile:
        return sum(1 for _ in csv.DictReader(infile))


@functools.lru_cache(maxsize=256)
def load_entity_record_profile(path: Path) -> dict[str, Any]:
    """Build deduplicated entity/record profile from entity_records.csv."""
    empty_profile = {
        "records_total": None,
        "entities_total": None,
        "grouped_members": None,
        "entity_size_distribution": {},
        "entity_pairings_distribution": {},
        "record_pairing_degree_distribution": {},
        "record_ids": set(),
    }
    if not path.exists():
        return empty_profile

    # Deduplicate by (DATA_SOURCE, RECORD_ID) to avoid inflated counts when export emits repeated rows.
    record_to_entity: dict[str, tuple[int, str]] = {}
    record_ids: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as infile:
        for row in csv.DictReader(infile):
            entity_id = str(row.get("resolved_entity_id") or "").strip()
            data_source = str(row.get("data_source") or "").strip()
            record_id = str(row.get("record_id") or "").strip()
            match_level_raw = str(row.get("match_level") or "").strip()
            try:
                match_level = int(match_level_raw)
            except ValueError:
                match_level = 999999
            if not entity_id or not record_id:
                continue
            record_key = f"{data_source}::{record_id}" if data_source else record_id
            existing = record_to_entity.get(record_key)
            if existing is None or match_level < existing[0]:
                record_to_entity[record_key] = (match_level, entity_id)
            record_ids.add(record_id)

    if not record_to_entity:
        return {
            "records_total": 0,
            "entities_total": 0,
            "grouped_members": 0,
            "entity_size_distribution": {},
            "entity_pairings_distribution": {},
            "record_pairing_degree_distribution": {},
            "record_ids": set(),
        }

    per_entity_records: dict[str, int] = {}
    for _, entity_id in record_to_entity.values():
        per_entity_records[entity_id] = per_entity_records.get(entity_id, 0) + 1

    size_distribution: dict[int, int] = {}
    pairings_distribution: dict[int, int] = {}
    degree_distribution: dict[int, int] = {}
    grouped_members = 0
    for size in per_entity_records.values():
        size_distribution[size] = size_distribution.get(size, 0) + 1
        pairings = size * (size - 1) // 2 if size > 1 else 0
        pairings_distribution[pairings] = pairings_distribution.get(pairings, 0) + 1
        degree = max(0, size - 1)
        degree_distribution[degree] = degree_distribution.get(degree, 0) + size
        if size > 1:
            grouped_members += size

    return {
        "records_total": len(record_to_entity),
        "entities_total": len(per_entity_records),
        "grouped_members": grouped_members,
        "entity_size_distribution": {str(k): v for k, v in sorted(size_distribution.items())},
        "entity_pairings_distribution": {str(k): v for k, v in sorted(pairings_distribution.items())},
        "record_pairing_degree_distribution": {str(k): v for k, v in sorted(degree_distribution.items())},
        "record_ids": record_ids,
    }


def count_unique_resolved_entities(path: Path) -> int | None:
    profile = load_entity_record_profile(path)
    value = profile.get("entities_total")
    return value if isinstance(value, int) else None


def count_unique_entity_records(path: Path) -> int | None:
    profile = load_entity_record_profile(path)
    value = profile.get("records_total")
    return value if isinstance(value, int) else None


def build_entity_distributions(path: Path) -> dict[str, dict[str, int]]:
    profile = load_entity_record_profile(path)
    return {
        "entity_size_distribution": profile.get("entity_size_distribution", {}) or {},
        "entity_pairings_distribution": profile.get("entity_pairings_distribution", {}) or {},
        "record_pairing_degree_distribution": profile.get("record_pairing_degree_distribution", {}) or {},
    }


def iter_input_source_records(path: Path):
    if not path.exists():
        return
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as infile:
            for line in infile:
                text = line.strip()
                if not text:
                    continue
                try:
                    item = json.loads(text)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    yield item
        return

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return

    if isinstance(payload, dict):
        for key in ("records", "data", "items"):
            records = payload.get(key)
            if isinstance(records, list):
                for item in records:
                    if isinstance(item, dict):
                        yield item
                return


def summarize_source_ipg_groups(input_source_json: Path, record_ids_filter: set[str] | None = None) -> dict[str, int | None]:
    if not input_source_json.exists():
        return {"records_total": None, "entities_total": None, "grouped_members": None, "entity_size_distribution": {}}

    candidates = ("IPG ID", "IPG_ID", "ipg_id", "SOURCE_IPG_ID", "source_ipg_id")
    records_total = 0
    ipg_sizes: dict[str, int] = {}

    for index, record in enumerate(iter_input_source_records(input_source_json), start=1):
        if record_ids_filter is not None and str(index) not in record_ids_filter:
            continue
        records_total += 1
        for key in candidates:
            value = record.get(key)
            if value is None:
                continue
            text = str(value).strip()
            if text:
                ipg_sizes[text] = ipg_sizes.get(text, 0) + 1
                break

    if records_total == 0:
        return {"records_total": 0, "entities_total": None, "grouped_members": None, "entity_size_distribution": {}}

    grouped_members = sum(size for size in ipg_sizes.values() if size > 1)
    size_distribution: dict[int, int] = {}
    for size in ipg_sizes.values():
        size_distribution[size] = size_distribution.get(size, 0) + 1
    return {
        "records_total": records_total,
        "entities_total": len(ipg_sizes),
        "grouped_members": grouped_members,
        "entity_size_distribution": {str(k): v for k, v in sorted(size_distribution.items())},
    }


def summarize_resolved_entity_groups(entity_records_csv: Path) -> dict[str, int | None]:
    profile = load_entity_record_profile(entity_records_csv)
    return {
        "records_total": profile.get("records_total"),
        "entities_total": profile.get("entities_total"),
        "grouped_members": profile.get("grouped_members"),
    }


def count_unique_source_ipg_groups(input_source_json: Path) -> int | None:
    summary = summarize_source_ipg_groups(input_source_json)
    return summary.get("entities_total")


def find_input_source_file(run_dir: Path) -> Path:
    json_path = run_dir / "input_source.json"
    if json_path.exists():
        return json_path
    jsonl_path = run_dir / "input_source.jsonl"
    if jsonl_path.exists():
        return jsonl_path
    return json_path


def compute_execution_seconds(run_summary: dict) -> float | None:
    if not isinstance(run_summary, dict):
        return None
    steps = run_summary.get("steps")
    if not isinstance(steps, list) or not steps:
        return None
    total = 0.0
    found = False
    for step in steps:
        if not isinstance(step, dict):
            continue
        duration = step.get("duration_seconds")
        if isinstance(duration, (int, float)):
            total += float(duration)
            found = True
    if not found:
        return None
    return round(total, 3)


def build_validation_summary(
    run_dir: Path,
    technical_dir: Path,
    records_input: int | None,
    resolved_entities: int | None,
    matched_pairs: int | None,
    pair_precision_pct: float | None,
    pair_recall_pct: float | None,
    our_match_coverage_pct: float | None,
    our_true_positive: int | None,
    our_true_pairs_total: int | None,
    false_positive_pct: float | None,
    true_positive: int | None,
    false_positive: int | None,
    false_negative: int | None,
    predicted_pairs_labeled: int | None,
) -> dict[str, object]:
    checks: list[dict[str, object]] = []
    input_source_file = find_input_source_file(run_dir)

    def add_check(name: str, expected: object, actual: object, source: str) -> None:
        if expected is None or actual is None:
            status = "SKIP"
            passed = None
        elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            passed = is_close(expected, actual)
            status = "PASS" if passed else "FAIL"
        else:
            passed = expected == actual
            status = "PASS" if passed else "FAIL"
        checks.append(
            {
                "name": name,
                "expected": expected,
                "actual": actual,
                "status": status,
                "source": source,
            }
        )

    loaded_entity_rows = count_unique_entity_records(technical_dir / "entity_records.csv")
    input_jsonl_rows = count_jsonl_rows(technical_dir / "input_normalized.jsonl")
    selected_input_actual = loaded_entity_rows if isinstance(loaded_entity_rows, int) else input_jsonl_rows
    selected_input_source = (
        "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
        if isinstance(loaded_entity_rows, int)
        else "technical output/input_normalized.jsonl"
    )
    add_check(
        "Selected Input Records",
        records_input,
        selected_input_actual,
        selected_input_source,
    )

    matched_pairs_rows = count_csv_rows(technical_dir / "matched_pairs.csv")
    add_check(
        "Matched Pairs",
        matched_pairs,
        matched_pairs_rows,
        "technical output/matched_pairs.csv",
    )

    resolved_entities_rows = count_unique_resolved_entities(technical_dir / "entity_records.csv")
    add_check(
        "Selected Resolved Entities",
        resolved_entities,
        resolved_entities_rows,
        "technical output/entity_records.csv",
    )

    precision_from_counts = pct(safe_ratio(true_positive, (true_positive or 0) + (false_positive or 0)))
    add_check(
        "Match Correctness (%)",
        pair_precision_pct,
        precision_from_counts,
        "technical output/ground_truth_match_quality.json (pair_metrics)",
    )

    coverage_from_recall = pct(safe_ratio(our_true_positive, our_true_pairs_total))
    add_check(
        "Our Match Coverage (%)",
        our_match_coverage_pct,
        coverage_from_recall,
        "technical output/management_summary.json (discovery baseline)",
    )

    false_positive_rate_from_counts = pct(safe_ratio(false_positive, predicted_pairs_labeled))
    add_check(
        "False Positive (%)",
        false_positive_pct,
        false_positive_rate_from_counts,
        "technical output/ground_truth_match_quality.json (pair_metrics)",
    )

    missed_from_recall = None if pair_recall_pct is None else round(100.0 - pair_recall_pct, 2)
    missed_from_counts = pct(safe_ratio(false_negative, (true_positive or 0) + (false_negative or 0)))
    add_check(
        "Match Missed (%)",
        missed_from_recall,
        missed_from_counts,
        "technical output/ground_truth_match_quality.json (pair_metrics)",
    )

    has_failure = any(item.get("status") == "FAIL" for item in checks)
    all_skipped = all(item.get("status") == "SKIP" for item in checks)
    overall_status = "SKIP" if all_skipped else ("FAIL" if has_failure else "PASS")

    return {
        "status": overall_status,
        "checks": checks,
        "run_path": str(run_dir),
        "input_source_path": str(input_source_file),
        "management_summary_path": str(technical_dir / "management_summary.json"),
        "ground_truth_path": str(technical_dir / "ground_truth_match_quality.json"),
        "matched_pairs_path": str(technical_dir / "matched_pairs.csv"),
        "entity_records_path": str(technical_dir / "entity_records.csv"),
        "input_jsonl_path": str(technical_dir / "input_normalized.jsonl"),
    }


def collect_run_record(output_root: Path, run_dir: Path) -> dict:
    run_id = run_dir.name
    match = RUN_DIR_RE.match(run_id)
    run_timestamp = match.group("ts") if match else run_id
    run_folder_label = match.group("label") if match else None
    technical_dir = run_dir / "technical output"

    management_summary = read_json(technical_dir / "management_summary.json")
    ground_truth = read_json(technical_dir / "ground_truth_match_quality.json")
    run_summary = read_json(technical_dir / "run_summary.json")
    mapping_summary = read_json(technical_dir / "mapping_summary.json")
    discovery_metrics = (
        management_summary.get("discovery_metrics") if isinstance(management_summary.get("discovery_metrics"), dict) else {}
    )

    pair_metrics = ground_truth.get("pair_metrics") if isinstance(ground_truth.get("pair_metrics"), dict) else {}
    distribution_metrics = (
        ground_truth.get("distribution_metrics") if isinstance(ground_truth.get("distribution_metrics"), dict) else {}
    )
    entity_records_csv = technical_dir / "entity_records.csv"
    entity_profile = load_entity_record_profile(entity_records_csv)
    entity_distributions = {
        "entity_size_distribution": entity_profile.get("entity_size_distribution", {}) or {},
        "entity_pairings_distribution": entity_profile.get("entity_pairings_distribution", {}) or {},
        "record_pairing_degree_distribution": entity_profile.get("record_pairing_degree_distribution", {}) or {},
    }
    baseline_match_coverage_raw = discovery_metrics.get("baseline_match_coverage")
    if not isinstance(baseline_match_coverage_raw, (int, float)):
        known_pairs = discovery_metrics.get("known_pairs_ipg")
        true_pairs = discovery_metrics.get("true_pairs_total")
        if isinstance(known_pairs, int) and isinstance(true_pairs, int) and true_pairs > 0:
            baseline_match_coverage_raw = known_pairs / true_pairs

    senzing_true_coverage_raw = discovery_metrics.get("senzing_true_coverage")
    if not isinstance(senzing_true_coverage_raw, (int, float)):
        true_found = discovery_metrics.get("overall_true_pairs_found")
        true_pairs = discovery_metrics.get("true_pairs_total")
        if isinstance(true_found, int) and isinstance(true_pairs, int) and true_pairs > 0:
            senzing_true_coverage_raw = true_found / true_pairs

    pair_precision_raw = to_num(pair_metrics.get("pair_precision"))
    pair_recall_raw = to_num(pair_metrics.get("pair_recall"))
    true_positive = pair_metrics.get("true_positive") if isinstance(pair_metrics.get("true_positive"), int) else None
    false_positive = pair_metrics.get("false_positive") if isinstance(pair_metrics.get("false_positive"), int) else None
    false_negative = pair_metrics.get("false_negative") if isinstance(pair_metrics.get("false_negative"), int) else None
    predicted_pairs_labeled = (
        pair_metrics.get("predicted_pairs_labeled")
        if isinstance(pair_metrics.get("predicted_pairs_labeled"), int)
        else None
    )
    ground_truth_pairs_labeled = (
        pair_metrics.get("ground_truth_pairs_labeled")
        if isinstance(pair_metrics.get("ground_truth_pairs_labeled"), int)
        else None
    )

    false_positive_rate_raw = to_num(discovery_metrics.get("overall_false_positive_rate"))
    false_positive_rate_ground_truth = safe_ratio(
        false_positive,
        predicted_pairs_labeled if isinstance(predicted_pairs_labeled, int) and predicted_pairs_labeled > 0 else None,
    )

    our_true_positive = (
        discovery_metrics.get("baseline_true_positive")
        if isinstance(discovery_metrics.get("baseline_true_positive"), int)
        else (
            discovery_metrics.get("known_pairs_ipg")
            if isinstance(discovery_metrics.get("known_pairs_ipg"), int)
            else ground_truth_pairs_labeled
        )
    )
    if not isinstance(our_true_positive, int):
        our_true_positive = 0

    our_true_pairs_total = (
        discovery_metrics.get("true_pairs_total")
        if isinstance(discovery_metrics.get("true_pairs_total"), int)
        else our_true_positive
    )
    if not isinstance(our_true_pairs_total, int):
        our_true_pairs_total = our_true_positive

    our_false_positive = (
        discovery_metrics.get("baseline_false_positive")
        if isinstance(discovery_metrics.get("baseline_false_positive"), int)
        else 0
    )
    our_false_negative = (
        discovery_metrics.get("baseline_false_negative")
        if isinstance(discovery_metrics.get("baseline_false_negative"), int)
        else max(0, our_true_pairs_total - our_true_positive)
    )
    our_match_coverage_raw = safe_ratio(our_true_positive, our_true_pairs_total)
    if our_match_coverage_raw is None:
        our_match_coverage_raw = 0.0

    mapping_input = str(mapping_summary.get("input_json") or "").strip()
    source_input_name = Path(mapping_input).name if mapping_input else None
    output_label = str(mapping_summary.get("output_label") or "").strip() or run_folder_label
    input_source_json = find_input_source_file(run_dir)
    loaded_record_ids = entity_profile.get("record_ids")
    source_ipg_summary = summarize_source_ipg_groups(
        input_source_json,
        record_ids_filter=loaded_record_ids if isinstance(loaded_record_ids, set) and loaded_record_ids else None,
    )
    our_resolved_entities = source_ipg_summary.get("entities_total")
    our_entity_size_distribution = (
        source_ipg_summary.get("entity_size_distribution")
        if isinstance(source_ipg_summary.get("entity_size_distribution"), dict)
        else {}
    )
    execution_seconds = compute_execution_seconds(run_summary)
    execution_minutes = round(execution_seconds / 60.0, 2) if isinstance(execution_seconds, (int, float)) else None

    their_entity_summary = summarize_resolved_entity_groups(entity_records_csv)

    records_input_reported = (
        management_summary.get("records_input") if isinstance(management_summary.get("records_input"), int) else None
    )
    records_input_loaded = (
        their_entity_summary.get("records_total") if isinstance(their_entity_summary.get("records_total"), int) else None
    )
    records_input = records_input_loaded
    if records_input is None:
        records_input = source_ipg_summary.get("records_total")
    if records_input is None:
        records_input = records_input_reported
    if records_input is None:
        records_input = count_jsonl_rows(technical_dir / "input_normalized.jsonl")

    resolved_entities = (
        their_entity_summary.get("entities_total")
        if isinstance(their_entity_summary.get("entities_total"), int)
        else (
            management_summary.get("resolved_entities")
            if isinstance(management_summary.get("resolved_entities"), int)
            else None
        )
    )
    their_grouped_members = their_entity_summary.get("grouped_members")
    our_grouped_members = source_ipg_summary.get("grouped_members")

    our_match_pct = pct(safe_ratio(our_grouped_members, records_input))
    their_match_pct = pct(safe_ratio(their_grouped_members, records_input))

    match_members_delta = None
    if isinstance(our_grouped_members, int) and isinstance(their_grouped_members, int):
        match_members_delta = our_grouped_members - their_grouped_members

    entity_count_delta = None
    if isinstance(our_resolved_entities, int) and isinstance(resolved_entities, int):
        entity_count_delta = our_resolved_entities - resolved_entities

    our_match_gain_loss_pct = pct(safe_ratio(match_members_delta, records_input))
    their_match_gain_loss_pct = pct(safe_ratio(-match_members_delta, records_input)) if match_members_delta is not None else None
    our_entity_gain_loss_pct = pct(safe_ratio(entity_count_delta, records_input))
    their_entity_gain_loss_pct = pct(safe_ratio(-entity_count_delta, records_input)) if entity_count_delta is not None else None

    artifact_entries: list[dict[str, object]] = []
    for file_path in sorted(path for path in run_dir.rglob("*") if path.is_file()):
        if any(part.startswith(".") for part in file_path.relative_to(run_dir).parts):
            continue
        rel = file_path.relative_to(output_root)
        artifact_entries.append(
            {
                "relative_path": rel.as_posix(),
                "display_name": str(file_path.relative_to(run_dir)).replace("\\", "/"),
                "size_bytes": file_path.stat().st_size,
            }
        )

    has_management_summary = bool(management_summary)
    has_ground_truth = bool(ground_truth)
    has_run_summary = bool(run_summary)
    overall_ok = run_summary.get("overall_ok") if isinstance(run_summary.get("overall_ok"), bool) else None
    quality_available = (
        isinstance(pair_metrics.get("pair_precision"), (int, float))
        and isinstance(pair_metrics.get("pair_recall"), (int, float))
        and isinstance(pair_metrics.get("true_positive"), int)
        and isinstance(pair_metrics.get("false_positive"), int)
        and isinstance(pair_metrics.get("false_negative"), int)
    )
    if has_run_summary and overall_ok is False:
        run_status = "failed"
    elif has_management_summary and has_ground_truth:
        run_status = "success"
    else:
        run_status = "incomplete"

    return {
        "run_id": run_id,
        "run_timestamp": run_timestamp,
        "run_datetime": parse_run_datetime(run_id),
        "run_label": output_label,
        "source_input_name": source_input_name,
        "run_status": run_status,
        "has_management_summary": has_management_summary,
        "has_ground_truth_summary": has_ground_truth,
        "has_run_summary": has_run_summary,
        "overall_ok": overall_ok,
        "quality_available": quality_available,
        "generated_at": management_summary.get("generated_at")
        or ground_truth.get("generated_at")
        or run_summary.get("generated_at"),
        "execution_seconds": execution_seconds,
        "execution_minutes": execution_minutes,
        "execution_minutes_estimated": None,
        "execution_minutes_is_estimate": False,
        "records_input": records_input,
        "records_input_loaded": records_input_loaded,
        "records_input_reported": records_input_reported,
        "records_exported": management_summary.get("records_exported"),
        "our_entities_formed": our_resolved_entities,
        "their_entities_formed": resolved_entities,
        "our_grouped_members": our_grouped_members,
        "their_grouped_members": their_grouped_members,
        "our_match_pct": our_match_pct,
        "their_match_pct": their_match_pct,
        "our_match_gain_loss_pct": our_match_gain_loss_pct,
        "their_match_gain_loss_pct": their_match_gain_loss_pct,
        "our_entity_gain_loss_pct": our_entity_gain_loss_pct,
        "their_entity_gain_loss_pct": their_entity_gain_loss_pct,
        "our_resolved_entities": our_resolved_entities,
        "resolved_entities": resolved_entities,
        "matched_records": management_summary.get("matched_records"),
        "matched_pairs": management_summary.get("matched_pairs"),
        "pair_precision_pct": pct(pair_precision_raw),
        "pair_recall_pct": pct(pair_recall_raw),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "discovery_available": bool(discovery_metrics.get("available")),
        "extra_true_matches_found": discovery_metrics.get("extra_true_matches_found"),
        "extra_false_matches_found": discovery_metrics.get("extra_false_matches_found"),
        "extra_match_precision_pct": pct(discovery_metrics.get("extra_match_precision")),
        "extra_match_recall_pct": pct(discovery_metrics.get("extra_match_recall")),
        "extra_gain_vs_known_pct": pct(discovery_metrics.get("extra_gain_vs_known")),
        "known_pairs_ipg": our_true_positive,
        "discoverable_true_pairs": discovery_metrics.get("discoverable_true_pairs"),
        "predicted_pairs_beyond_known": discovery_metrics.get("predicted_pairs_beyond_known"),
        "net_extra_matches": discovery_metrics.get("net_extra_matches"),
        "overall_false_positive_pct": pct(false_positive_rate_ground_truth),
        "overall_false_positive_discovery_pct": pct(false_positive_rate_raw),
        "overall_match_correctness_pct": pct(discovery_metrics.get("overall_match_correctness")),
        "our_true_positive": our_true_positive,
        "our_true_pairs_total": our_true_pairs_total,
        "our_false_positive": our_false_positive,
        "our_false_negative": our_false_negative,
        "our_match_coverage_pct": pct(our_match_coverage_raw),
        "baseline_match_coverage_pct": pct(baseline_match_coverage_raw),
        "senzing_true_coverage_pct": pct(senzing_true_coverage_raw),
        "predicted_pairs_labeled": predicted_pairs_labeled,
        "ground_truth_pairs_labeled": ground_truth_pairs_labeled,
        "match_level_distribution": management_summary.get("match_level_distribution", {}),
        "top_match_keys": sorted(
            (
                (
                    str(key),
                    int(value),
                )
                for key, value in (management_summary.get("match_key_distribution") or {}).items()
                if isinstance(key, str) and isinstance(value, int)
            ),
            key=lambda item: item[1],
            reverse=True,
        )[:10],
        "entity_size_distribution": entity_distributions.get("entity_size_distribution")
        or distribution_metrics.get("entity_size_distribution", {}),
        "our_entity_size_distribution": our_entity_size_distribution,
        "entity_pairings_distribution": entity_distributions.get("entity_pairings_distribution")
        or distribution_metrics.get("entity_pairings_distribution", {}),
        "record_pairing_degree_distribution": entity_distributions.get("record_pairing_degree_distribution")
        or distribution_metrics.get("record_pairing_degree_distribution", {}),
        "explain_coverage": management_summary.get("explain_coverage", {}),
        "runtime_warnings": run_summary.get("runtime_warnings", []),
        "input_source_path": f"{run_id}/{input_source_json.name}",
        "management_summary_path": f"{run_id}/management_summary.md",
        "ground_truth_summary_path": f"{run_id}/ground_truth_match_quality.md",
        "technical_path": f"{run_id}/technical output",
        "mapping_info": {
            "data_source": mapping_summary.get("data_source"),
            "tax_id_type": mapping_summary.get("tax_id_type"),
            "execution_mode": mapping_summary.get("execution_mode"),
        },
        "artifacts": artifact_entries,
        "validation": build_validation_summary(
            run_dir=run_dir,
            technical_dir=technical_dir,
            records_input=records_input if isinstance(records_input, int) else None,
            resolved_entities=resolved_entities if isinstance(resolved_entities, int) else None,
            matched_pairs=management_summary.get("matched_pairs")
            if isinstance(management_summary.get("matched_pairs"), int)
            else None,
            pair_precision_pct=pct(pair_precision_raw),
            pair_recall_pct=pct(pair_recall_raw),
            our_match_coverage_pct=pct(our_match_coverage_raw),
            our_true_positive=our_true_positive,
            our_true_pairs_total=our_true_pairs_total,
            false_positive_pct=pct(false_positive_rate_ground_truth),
            true_positive=true_positive,
            false_positive=false_positive,
            false_negative=false_negative,
            predicted_pairs_labeled=predicted_pairs_labeled,
        ),
    }


def apply_execution_estimates(runs: list[dict]) -> None:
    measured = [
        run
        for run in runs
        if isinstance(run.get("execution_minutes"), (int, float))
        and isinstance(run.get("records_input"), int)
        and int(run.get("records_input") or 0) > 0
    ]
    if not measured:
        return

    # Use the largest measured run as baseline throughput to estimate missing durations.
    anchor = max(measured, key=lambda item: int(item.get("records_input") or 0))
    anchor_minutes = float(anchor.get("execution_minutes") or 0.0)
    anchor_records = int(anchor.get("records_input") or 0)
    if anchor_minutes <= 0 or anchor_records <= 0:
        return
    minutes_per_record = anchor_minutes / anchor_records

    for run in runs:
        if isinstance(run.get("execution_minutes"), (int, float)):
            run["execution_minutes_estimated"] = run.get("execution_minutes")
            run["execution_minutes_is_estimate"] = False
            continue
        records_input = run.get("records_input")
        if isinstance(records_input, int) and records_input > 0:
            run["execution_minutes_estimated"] = round(records_input * minutes_per_record, 2)
            run["execution_minutes_is_estimate"] = True


def collect_runs(output_root: Path) -> list[dict]:
    run_dirs = [path for path in output_root.iterdir() if path.is_dir() and RUN_DIR_RE.match(path.name)]
    run_dirs.sort(key=lambda path: path.name, reverse=True)
    runs = [collect_run_record(output_root, run_dir) for run_dir in run_dirs]
    apply_execution_estimates(runs)
    return runs


def aggregate(runs: list[dict]) -> dict:
    def mean(values: list[float]) -> float | None:
        if not values:
            return None
        return round(sum(values) / len(values), 2)

    quality_runs = [run for run in runs if bool(run.get("quality_available"))]
    precision_values = [float(run["pair_precision_pct"]) for run in quality_runs if isinstance(run.get("pair_precision_pct"), (int, float))]
    recall_values = [float(run["pair_recall_pct"]) for run in quality_runs if isinstance(run.get("pair_recall_pct"), (int, float))]

    total_input = sum(int(run.get("records_input")) for run in quality_runs if isinstance(run.get("records_input"), int))
    total_pairs = sum(int(run.get("matched_pairs")) for run in quality_runs if isinstance(run.get("matched_pairs"), int))
    successful_runs = sum(1 for run in runs if run.get("run_status") == "success")
    failed_runs = sum(1 for run in runs if run.get("run_status") == "failed")
    incomplete_runs = sum(1 for run in runs if run.get("run_status") == "incomplete")

    return {
        "runs_total": len(runs),
        "quality_runs_total": len(quality_runs),
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "incomplete_runs": incomplete_runs,
        "latest_run_id": runs[0]["run_id"] if runs else None,
        "avg_pair_precision_pct": mean(precision_values),
        "avg_pair_recall_pct": mean(recall_values),
        "records_input_total": total_input,
        "matched_pairs_total": total_pairs,
    }


def write_data_js(path: Path, payload: dict) -> None:
    js = "window.MVP_DASHBOARD_DATA = " + json.dumps(payload, indent=2, ensure_ascii=True) + ";\n"
    path.write_text(js, encoding="utf-8")


def sync_dashboard_assets(template_dir: Path, target_dir: Path) -> None:
    if template_dir.resolve() == target_dir.resolve():
        return
    for filename in STATIC_DASHBOARD_FILES:
        source = template_dir / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing dashboard template asset: {source}")
        shutil.copy2(source, target_dir / filename)


def write_index_html(target_dir: Path) -> None:
    index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=./management_dashboard.html">
    <title>Dashboard</title>
  </head>
  <body>
    <p>Open <a href="./management_dashboard.html">management_dashboard.html</a>.</p>
  </body>
</html>
"""
    (target_dir / "index.html").write_text(index_html, encoding="utf-8")


def run_dashboard_test_suite(mvp_root: Path, output_root: Path, dashboard_dir: Path) -> None:
    test_runner = mvp_root / "testing" / "run_dashboard_tests.py"
    if not test_runner.exists():
        raise FileNotFoundError(f"Missing test runner: {test_runner}")

    command = [
        sys.executable,
        str(test_runner),
        "--output-root",
        str(output_root),
        "--dashboard-data",
        str(dashboard_dir / "management_dashboard_data.js"),
        "--report-json",
        str(dashboard_dir / "dashboard_test_suite_report.json"),
        "--report-md",
        str(dashboard_dir / "dashboard_test_suite_report.md"),
    ]
    subprocess.run(command, cwd=str(mvp_root), check=True)


def run_dashboard_metric_audit(mvp_root: Path, output_root: Path, dashboard_dir: Path) -> None:
    verifier = mvp_root / "verify_dashboard_metrics.py"
    if not verifier.exists():
        raise FileNotFoundError(f"Missing dashboard verifier: {verifier}")

    command = [
        sys.executable,
        str(verifier),
        "--output-root",
        str(output_root),
        "--dashboard-data",
        str(dashboard_dir / "management_dashboard_data.js"),
        "--report-json",
        str(dashboard_dir / "dashboard_data_audit_report.json"),
        "--report-md",
        str(dashboard_dir / "dashboard_data_audit_report.md"),
    ]
    subprocess.run(command, cwd=str(mvp_root), check=True)


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parent
    output_root = (mvp_root / args.output_root).resolve()
    dashboard_template_dir = (mvp_root / "dashboard").resolve()
    dashboard_dir = (mvp_root / args.dashboard_dir).resolve()
    data_js_path = dashboard_dir / "management_dashboard_data.js"

    if not output_root.exists():
        output_root.mkdir(parents=True, exist_ok=True)
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    sync_dashboard_assets(dashboard_template_dir, dashboard_dir)
    write_index_html(dashboard_dir)

    runs = collect_runs(output_root)
    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "output_root": str(output_root),
        "runs": runs,
        "summary": aggregate(runs),
    }

    write_data_js(data_js_path, payload)
    print(f"Dashboard data generated: {data_js_path}")
    print(f"Runs indexed: {len(runs)}")
    print(f"Dashboard directory: {dashboard_dir}")

    if not args.skip_tests:
        try:
            run_dashboard_test_suite(mvp_root=mvp_root, output_root=output_root, dashboard_dir=dashboard_dir)
            print("Dashboard test suite: PASS")
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        except subprocess.CalledProcessError as exc:
            print(
                f"ERROR: dashboard test suite failed (exit code {exc.returncode}). "
                "Check dashboard_test_suite_report.md for details.",
                file=sys.stderr,
            )
            return exc.returncode or 1
    if not args.skip_audit:
        try:
            run_dashboard_metric_audit(mvp_root=mvp_root, output_root=output_root, dashboard_dir=dashboard_dir)
            print("Dashboard metric audit: PASS")
        except FileNotFoundError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        except subprocess.CalledProcessError as exc:
            print(
                f"ERROR: dashboard metric audit failed (exit code {exc.returncode}). "
                "Check dashboard_data_audit_report.md for details.",
                file=sys.stderr,
            )
            return exc.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

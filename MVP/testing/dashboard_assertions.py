"""Shared helpers for dashboard metric validation tests."""

from __future__ import annotations

import csv
import json
import math
import functools
from pathlib import Path
from typing import Any

DASHBOARD_JS_PREFIX = "window.MVP_DASHBOARD_DATA = "
IPG_ID_CANDIDATE_KEYS = ("IPG ID", "IPG_ID", "ipg_id", "SOURCE_IPG_ID", "source_ipg_id")


def parse_dashboard_data_js(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith(DASHBOARD_JS_PREFIX):
        raise ValueError(f"Unexpected dashboard data format: {path}")
    payload = raw[len(DASHBOARD_JS_PREFIX) :].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise TypeError("Dashboard payload must be a JSON object")
    return data


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return False


def as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def as_float(value: Any) -> float | None:
    if not is_number(value):
        return None
    return float(value)


def to_pct_from_ratio(ratio: Any) -> float | None:
    value = as_float(ratio)
    if value is None:
        return None
    return round(value * 100.0, 2)


def to_pct_from_counts(numerator: Any, denominator: Any) -> float | None:
    num = as_float(numerator)
    den = as_float(denominator)
    if num is None or den is None or den <= 0:
        return None
    return round((num / den) * 100.0, 2)


def count_non_empty_jsonl(path: Path) -> int | None:
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
        reader = csv.DictReader(infile)
        return sum(1 for _ in reader)


def count_unique_csv_values(path: Path, column_name: str) -> int | None:
    if not path.exists():
        return None
    values: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            value = str(row.get(column_name) or "").strip()
            if value:
                values.add(value)
    return len(values)


@functools.lru_cache(maxsize=256)
def load_entity_record_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "records_total": None,
            "entities_total": None,
            "grouped_members": None,
            "entity_size_distribution": {},
            "record_ids": set(),
        }

    record_to_entity: dict[str, tuple[int, str]] = {}
    record_ids: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
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
            "record_ids": set(),
        }

    per_entity: dict[str, int] = {}
    for _, entity_id in record_to_entity.values():
        per_entity[entity_id] = per_entity.get(entity_id, 0) + 1

    distribution: dict[int, int] = {}
    grouped_members = 0
    for size in per_entity.values():
        distribution[size] = distribution.get(size, 0) + 1
        if size > 1:
            grouped_members += size

    return {
        "records_total": len(record_to_entity),
        "entities_total": len(per_entity),
        "grouped_members": grouped_members,
        "entity_size_distribution": {str(key): value for key, value in sorted(distribution.items(), key=lambda item: item[0])},
        "record_ids": record_ids,
    }


def build_entity_size_distribution(path: Path) -> dict[str, int]:
    profile = load_entity_record_profile(path)
    distribution = profile.get("entity_size_distribution")
    return distribution if isinstance(distribution, dict) else {}


def iter_input_source_records(input_source_json: Path):
    if not input_source_json.exists():
        return
    if input_source_json.suffix.lower() == ".jsonl":
        with input_source_json.open("r", encoding="utf-8") as infile:
            for line in infile:
                text = line.strip()
                if not text:
                    continue
                try:
                    record = json.loads(text)
                except json.JSONDecodeError:
                    continue
                if isinstance(record, dict):
                    yield record
        return
    try:
        payload = json.loads(input_source_json.read_text(encoding="utf-8"))
    except Exception:
        return
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return
    if isinstance(payload, dict):
        for key in ("records", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item
                return


def summarize_source_ipg_groups(input_source_json: Path, record_ids_filter: set[str] | None = None) -> dict[str, int | None]:
    if not input_source_json.exists():
        return {"records_total": None, "entities_total": None, "grouped_members": None, "entity_size_distribution": {}}

    ipg_sizes: dict[str, int] = {}
    records_total = 0
    missing_ipg_singletons = 0
    for index, record in enumerate(iter_input_source_records(input_source_json), start=1):
        if record_ids_filter is not None and str(index) not in record_ids_filter:
            continue
        records_total += 1
        found_ipg = False
        for key in IPG_ID_CANDIDATE_KEYS:
            raw_value = record.get(key)
            if raw_value is None:
                continue
            text = str(raw_value).strip()
            if text:
                ipg_sizes[text] = ipg_sizes.get(text, 0) + 1
                found_ipg = True
                break
        if not found_ipg:
            missing_ipg_singletons += 1
    if records_total == 0:
        return {"records_total": 0, "entities_total": None, "grouped_members": None, "entity_size_distribution": {}}
    grouped_members = sum(size for size in ipg_sizes.values() if size > 1)
    size_distribution: dict[int, int] = {}
    for size in ipg_sizes.values():
        size_distribution[size] = size_distribution.get(size, 0) + 1
    if missing_ipg_singletons > 0:
        size_distribution[1] = size_distribution.get(1, 0) + missing_ipg_singletons
    return {
        "records_total": records_total,
        "entities_total": len(ipg_sizes) + missing_ipg_singletons,
        "grouped_members": grouped_members,
        "entity_size_distribution": {str(k): v for k, v in sorted(size_distribution.items())},
    }


def count_unique_source_ipg_groups(input_source_json: Path) -> int | None:
    return summarize_source_ipg_groups(input_source_json).get("entities_total")


def find_input_source_file(run_dir: Path) -> Path:
    json_path = run_dir / "input_source.json"
    if json_path.exists():
        return json_path
    jsonl_path = run_dir / "input_source.jsonl"
    if jsonl_path.exists():
        return jsonl_path
    return json_path


def count_input_source_records(input_source_json: Path) -> int | None:
    if not input_source_json.exists():
        return None
    if input_source_json.suffix.lower() == ".jsonl":
        count = 0
        with input_source_json.open("r", encoding="utf-8") as infile:
            for line in infile:
                text = line.strip()
                if not text:
                    continue
                try:
                    item = json.loads(text)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    count += 1
        return count
    try:
        payload = json.loads(input_source_json.read_text(encoding="utf-8"))
    except Exception:
        return None

    if isinstance(payload, list):
        return sum(1 for item in payload if isinstance(item, dict))

    if isinstance(payload, dict):
        for key in ("records", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return sum(1 for item in value if isinstance(item, dict))
    return None


def summarize_resolved_entity_groups(entity_records_csv: Path) -> dict[str, int | None]:
    profile = load_entity_record_profile(entity_records_csv)
    return {
        "records_total": profile.get("records_total"),
        "entities_total": profile.get("entities_total"),
        "grouped_members": profile.get("grouped_members"),
    }


def normalize_distribution(raw_distribution: Any) -> dict[str, int] | None:
    if not isinstance(raw_distribution, dict):
        return None
    normalized: dict[str, int] = {}
    for key, value in raw_distribution.items():
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(value, int):
            return None
        normalized[key] = value
    return dict(sorted(normalized.items(), key=lambda item: int(item[0]) if item[0].isdigit() else item[0]))


def compute_execution_minutes_from_run_summary(run_summary_json: Path) -> float | None:
    payload = read_json(run_summary_json)
    steps = payload.get("steps")
    if not isinstance(steps, list) or not steps:
        return None
    total_seconds = 0.0
    found = False
    for step in steps:
        if not isinstance(step, dict):
            continue
        duration = step.get("duration_seconds")
        if isinstance(duration, (int, float)):
            total_seconds += float(duration)
            found = True
    if not found:
        return None
    return round(total_seconds / 60.0, 2)


def compute_expected_run_metrics(run: dict[str, Any], output_root: Path) -> dict[str, Any]:
    run_id = str(run.get("run_id") or "").strip()
    run_dir = output_root / run_id
    technical_dir = run_dir / "technical output"

    management_summary = read_json(technical_dir / "management_summary.json")
    ground_truth = read_json(technical_dir / "ground_truth_match_quality.json")

    pair_metrics = ground_truth.get("pair_metrics") if isinstance(ground_truth.get("pair_metrics"), dict) else {}
    discovery = management_summary.get("discovery_metrics") if isinstance(management_summary.get("discovery_metrics"), dict) else {}

    true_positive = as_int(pair_metrics.get("true_positive"))
    false_positive = as_int(pair_metrics.get("false_positive"))
    false_negative = as_int(pair_metrics.get("false_negative"))
    predicted_pairs_labeled = as_int(pair_metrics.get("predicted_pairs_labeled"))
    ground_truth_pairs_labeled = as_int(pair_metrics.get("ground_truth_pairs_labeled"))

    baseline_true_positive = as_int(discovery.get("baseline_true_positive"))
    known_pairs_ipg = as_int(discovery.get("known_pairs_ipg"))
    if baseline_true_positive is not None:
        our_true_positive = baseline_true_positive
    elif known_pairs_ipg is not None:
        our_true_positive = known_pairs_ipg
    elif ground_truth_pairs_labeled is not None:
        our_true_positive = ground_truth_pairs_labeled
    else:
        our_true_positive = 0

    true_pairs_total = as_int(discovery.get("true_pairs_total"))
    our_true_pairs_total = true_pairs_total if true_pairs_total is not None else our_true_positive

    baseline_false_positive = as_int(discovery.get("baseline_false_positive"))
    our_false_positive = baseline_false_positive if baseline_false_positive is not None else 0

    baseline_false_negative = as_int(discovery.get("baseline_false_negative"))
    our_false_negative = baseline_false_negative if baseline_false_negative is not None else max(0, our_true_pairs_total - our_true_positive)

    input_jsonl = technical_dir / "input_normalized.jsonl"
    matched_pairs_csv = technical_dir / "matched_pairs.csv"
    entity_records_csv = technical_dir / "entity_records.csv"
    input_source_json = find_input_source_file(run_dir)
    entity_profile = load_entity_record_profile(entity_records_csv)
    source_ipg_summary = summarize_source_ipg_groups(
        input_source_json,
        record_ids_filter=entity_profile.get("record_ids") if isinstance(entity_profile.get("record_ids"), set) else None,
    )
    their_entity_summary = summarize_resolved_entity_groups(entity_records_csv)

    entity_size_distribution = build_entity_size_distribution(entity_records_csv)
    our_entity_size_distribution = source_ipg_summary.get("entity_size_distribution")

    extra_true = as_int(discovery.get("extra_true_matches_found"))
    extra_false = as_int(discovery.get("extra_false_matches_found"))
    extra_gain_ratio = as_float(discovery.get("extra_gain_vs_known"))

    records_input = (
        entity_profile.get("records_total")
        or source_ipg_summary.get("records_total")
        or count_non_empty_jsonl(input_jsonl)
        or count_input_source_records(input_source_json)
    )
    our_entities_formed = source_ipg_summary.get("entities_total")
    their_entities_formed = entity_profile.get("entities_total")
    our_grouped_members = source_ipg_summary.get("grouped_members")
    their_grouped_members = their_entity_summary.get("grouped_members")

    our_match_pct = to_pct_from_counts(our_grouped_members, records_input)
    their_match_pct = to_pct_from_counts(their_grouped_members, records_input)
    match_members_delta = (
        our_grouped_members - their_grouped_members
        if isinstance(our_grouped_members, int) and isinstance(their_grouped_members, int)
        else None
    )
    entity_delta = (
        our_entities_formed - their_entities_formed
        if isinstance(our_entities_formed, int) and isinstance(their_entities_formed, int)
        else None
    )

    return {
        "paths": {
            "run_dir": run_dir,
            "technical_dir": technical_dir,
            "input_jsonl": input_jsonl,
            "matched_pairs_csv": matched_pairs_csv,
            "entity_records_csv": entity_records_csv,
            "input_source_json": input_source_json,
            "management_summary_json": technical_dir / "management_summary.json",
            "ground_truth_json": technical_dir / "ground_truth_match_quality.json",
            "run_summary_json": technical_dir / "run_summary.json",
        },
        "from_files": {
            "records_input": records_input,
            "matched_pairs": count_csv_rows(matched_pairs_csv),
            "resolved_entities": count_unique_csv_values(entity_records_csv, "resolved_entity_id"),
            "our_resolved_entities": count_unique_source_ipg_groups(input_source_json),
            "our_entities_formed": our_entities_formed,
            "their_entities_formed": their_entities_formed,
            "our_grouped_members": our_grouped_members,
            "their_grouped_members": their_grouped_members,
            "our_match_pct": our_match_pct,
            "their_match_pct": their_match_pct,
            "our_match_gain_loss_pct": to_pct_from_counts(match_members_delta, records_input),
            "their_match_gain_loss_pct": to_pct_from_counts(
                -match_members_delta if isinstance(match_members_delta, int) else None,
                records_input,
            ),
            "our_entity_gain_loss_pct": to_pct_from_counts(entity_delta, records_input),
            "their_entity_gain_loss_pct": to_pct_from_counts(
                -entity_delta if isinstance(entity_delta, int) else None,
                records_input,
            ),
            "our_entity_size_distribution": normalize_distribution(our_entity_size_distribution),
            "entity_size_distribution": entity_size_distribution,
        },
        "from_ground_truth": {
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "predicted_pairs_labeled": predicted_pairs_labeled,
            "pair_precision_pct": to_pct_from_ratio(pair_metrics.get("pair_precision")),
            "pair_recall_pct": to_pct_from_ratio(pair_metrics.get("pair_recall")),
            "pair_precision_pct_from_counts": to_pct_from_counts(
                true_positive,
                (true_positive or 0) + (false_positive or 0),
            )
            if true_positive is not None and false_positive is not None
            else None,
            "pair_recall_pct_from_counts": to_pct_from_counts(
                true_positive,
                (true_positive or 0) + (false_negative or 0),
            )
            if true_positive is not None and false_negative is not None
            else None,
            "overall_false_positive_pct": to_pct_from_counts(false_positive, predicted_pairs_labeled),
        },
        "from_discovery": {
            "our_true_positive": our_true_positive,
            "our_true_pairs_total": our_true_pairs_total,
            "our_false_positive": our_false_positive,
            "our_false_negative": our_false_negative,
            "our_match_coverage_pct": to_pct_from_counts(our_true_positive, our_true_pairs_total),
            "known_pairs_ipg": known_pairs_ipg,
            "extra_true_matches_found": extra_true,
            "extra_false_matches_found": extra_false,
            "extra_gain_vs_known_pct": to_pct_from_ratio(extra_gain_ratio)
            if extra_gain_ratio is not None
            else to_pct_from_counts(extra_true, known_pairs_ipg),
        },
        "from_runtime": {
            "execution_minutes": compute_execution_minutes_from_run_summary(technical_dir / "run_summary.json"),
        },
    }


def compute_summary_from_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    def mean(values: list[float]) -> float | None:
        if not values:
            return None
        return round(sum(values) / len(values), 2)

    quality_runs = [run for run in runs if bool(run.get("quality_available"))]

    precision_values = [
        float(run["pair_precision_pct"])
        for run in quality_runs
        if is_number(run.get("pair_precision_pct"))
    ]
    recall_values = [
        float(run["pair_recall_pct"])
        for run in quality_runs
        if is_number(run.get("pair_recall_pct"))
    ]

    total_input = sum(int(run.get("records_input")) for run in quality_runs if as_int(run.get("records_input")) is not None)
    total_pairs = sum(int(run.get("matched_pairs")) for run in quality_runs if as_int(run.get("matched_pairs")) is not None)

    successful_runs = sum(1 for run in runs if run.get("run_status") == "success")
    failed_runs = sum(1 for run in runs if run.get("run_status") == "failed")
    incomplete_runs = sum(1 for run in runs if run.get("run_status") == "incomplete")

    return {
        "runs_total": len(runs),
        "quality_runs_total": len(quality_runs),
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "incomplete_runs": incomplete_runs,
        "latest_run_id": runs[0].get("run_id") if runs else None,
        "avg_pair_precision_pct": mean(precision_values),
        "avg_pair_recall_pct": mean(recall_values),
        "records_input_total": total_input,
        "matched_pairs_total": total_pairs,
    }

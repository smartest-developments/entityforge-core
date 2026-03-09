#!/usr/bin/env python3
"""Automated management test suite for Senzing vs internal EPG grouping.

Expected run directory input (produced by run_senzing_e2e):
- input_normalized.jsonl
- comparison/entity_records.csv
- comparison/matched_pairs.csv
- comparison/match_key_stats.csv (optional for this script)

Outputs:
- testing/management_test_results.json
- testing/management_test_results.csv
- testing/management_test_summary.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CASE_METADATA: dict[str, dict[str, str]] = {
    "TC-01": {
        "management_question": "How many Senzing entities are pure vs mixed by EPG ID?",
        "metric_name": "Entity_EPG_Purity_Rate",
        "threshold": ">= 95%",
    },
    "TC-02": {
        "management_question": "How often are records from same EPG split into multiple Senzing entities?",
        "metric_name": "EPG_Split_Rate",
        "threshold": "<= 10%",
    },
    "TC-03": {
        "management_question": "How often does Senzing merge different EPG groups?",
        "metric_name": "Cross_EPG_Merge_Rate",
        "threshold": "<= 5%",
    },
    "TC-04": {
        "management_question": "Among same EPG records, what percentage was correctly linked by Senzing?",
        "metric_name": "Same_EPG_Link_Recall_Proxy",
        "threshold": ">= 90%",
    },
    "TC-05": {
        "management_question": "Can we explain why each matched pair was linked?",
        "metric_name": "WhyRecords_Coverage",
        "threshold": ">= 95%",
    },
    "TC-06": {
        "management_question": "Can we explain entity assignment for each matched record?",
        "metric_name": "WhyEntity_Coverage",
        "threshold": ">= 95%",
    },
    "TC-07": {
        "management_question": "Are match reasons concentrated in expected keys?",
        "metric_name": "Top_Match_Key_Concentration",
        "threshold": ">= 70%",
    },
    "TC-08": {
        "management_question": "Is record lineage complete from input to Senzing output?",
        "metric_name": "Lineage_Integrity_Rate",
        "threshold": "= 100%",
    },
    "TC-09": {
        "management_question": "Are high-confidence cross-EPG merges within accepted policy?",
        "metric_name": "High_Confidence_Cross_EPG_Merge_Rate",
        "threshold": "<= configurable (default 1%)",
    },
    "TC-10": {
        "management_question": "Is Senzing better than current engine on approved KPI?",
        "metric_name": "Delta_vs_Current_Engine",
        "threshold": ">= 0",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run automated management test cases on one Senzing run folder.")
    parser.add_argument("run_dir", help="Path to one Senzing run directory")
    parser.add_argument(
        "--epg-field-candidates",
        default="SOURCE_IPG_ID,IPG ID,IPG_ID,EPGID,EPG_ID",
        help="Comma-separated EPG field candidates to search in input_normalized.jsonl",
    )
    parser.add_argument(
        "--high-confidence-level",
        type=int,
        default=2,
        help="Match level considered high confidence for TC-09 (default: 2)",
    )
    parser.add_argument(
        "--high-confidence-cross-epg-threshold",
        type=float,
        default=0.01,
        help="Max accepted rate for TC-09 (default: 0.01 = 1%%)",
    )
    parser.add_argument(
        "--baseline-metric",
        default="Entity_EPG_Purity_Rate",
        help="Metric name used for TC-10 baseline comparison",
    )
    parser.add_argument(
        "--baseline-value",
        type=float,
        default=None,
        help="Explicit baseline value for --baseline-metric",
    )
    parser.add_argument(
        "--baseline-json",
        default=None,
        help="Optional JSON file with baseline metrics",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for test reports (default: <run_dir>/testing)",
    )
    return parser.parse_args()


def parse_int(value: Any, default: int = 0) -> int:
    text = "" if value is None else str(value).strip()
    if not text:
        return default
    try:
        return int(float(text))
    except ValueError:
        return default


def parse_float(value: Any, default: float | None = None) -> float | None:
    text = "" if value is None else str(value).strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = "" if value is None else str(value).strip().lower()
    return text in {"1", "true", "yes", "y", "ok", "pass"}


def comb2(n: int) -> int:
    return 0 if n < 2 else n * (n - 1) // 2


def safe_rate(num: int, den: int) -> float | None:
    if den <= 0:
        return None
    return num / den


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as infile:
        for line_no, line in enumerate(infile, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"Invalid JSONL object at line {line_no}")
            rows.append(obj)
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                normalized[key.strip()] = "" if value is None else str(value).strip()
            rows.append(normalized)
        return rows


def key_of(data_source: Any, record_id: Any) -> tuple[str, str] | None:
    ds = "" if data_source is None else str(data_source).strip()
    rid = "" if record_id is None else str(record_id).strip()
    if not ds or not rid:
        return None
    return ds, rid


def detect_epg(row: dict[str, Any], candidates: list[str]) -> str | None:
    for candidate in candidates:
        value = row.get(candidate)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def evaluate_threshold(value: float | None, op: str, threshold: float) -> tuple[str, bool | None]:
    if value is None:
        return "NOT_EVALUATED", None

    if op == ">=":
        passed = value >= threshold
    elif op == "<=":
        passed = value <= threshold
    elif op == "=":
        passed = math.isclose(value, threshold, rel_tol=1e-9, abs_tol=1e-9)
    else:
        return "NOT_EVALUATED", None

    return ("PASS" if passed else "FAIL"), passed


def load_baseline_value(args: argparse.Namespace) -> float | None:
    if args.baseline_value is not None:
        return args.baseline_value

    if not args.baseline_json:
        return None

    baseline_path = Path(args.baseline_json).expanduser().resolve()
    if not baseline_path.exists():
        return None

    try:
        payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    if isinstance(payload, dict):
        direct = parse_float(payload.get(args.baseline_metric))
        if direct is not None:
            return direct
        metrics_obj = payload.get("metrics")
        if isinstance(metrics_obj, dict):
            nested = parse_float(metrics_obj.get(args.baseline_metric))
            if nested is not None:
                return nested

    return None


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir).expanduser().resolve()

    input_jsonl = run_dir / "input_normalized.jsonl"
    entity_records_csv = run_dir / "comparison" / "entity_records.csv"
    matched_pairs_csv = run_dir / "comparison" / "matched_pairs.csv"

    required = [input_jsonl, entity_records_csv, matched_pairs_csv]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("ERROR: Missing required files:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (run_dir / "testing")
    output_dir.mkdir(parents=True, exist_ok=True)

    epg_candidates = [item.strip() for item in args.epg_field_candidates.split(",") if item.strip()]

    input_rows = read_jsonl(input_jsonl)
    entity_rows = read_csv_rows(entity_records_csv)
    pair_rows = read_csv_rows(matched_pairs_csv)

    input_keys: set[tuple[str, str]] = set()
    record_to_epg: dict[tuple[str, str], str] = {}
    record_to_epg_conflicts = 0

    for row in input_rows:
        key = key_of(row.get("DATA_SOURCE"), row.get("RECORD_ID"))
        if key is None:
            continue
        input_keys.add(key)
        epg = detect_epg(row, epg_candidates)
        if epg is None:
            continue
        existing = record_to_epg.get(key)
        if existing is not None and existing != epg:
            record_to_epg_conflicts += 1
            continue
        record_to_epg[key] = epg

    entity_entries: list[dict[str, Any]] = []
    entity_keys: set[tuple[str, str]] = set()
    for row in entity_rows:
        key = key_of(row.get("data_source"), row.get("record_id"))
        if key is None:
            continue
        entity_keys.add(key)
        entity_entries.append(
            {
                "key": key,
                "resolved_entity_id": row.get("resolved_entity_id", ""),
                "match_level": parse_int(row.get("match_level"), default=0),
                "match_key": row.get("match_key", ""),
                "why_entity_ok": is_truthy(row.get("why_entity_ok")),
                "epg": record_to_epg.get(key),
            }
        )

    pair_entries: list[dict[str, Any]] = []
    for row in pair_rows:
        anchor_key = key_of(row.get("anchor_data_source"), row.get("anchor_record_id"))
        matched_key = key_of(row.get("matched_data_source"), row.get("matched_record_id"))
        if anchor_key is None or matched_key is None:
            continue
        pair_entries.append(
            {
                "anchor_key": anchor_key,
                "matched_key": matched_key,
                "match_level": parse_int(row.get("match_level"), default=0),
                "match_key": row.get("match_key", ""),
                "why_records_ok": is_truthy(row.get("why_records_ok")),
                "anchor_epg": record_to_epg.get(anchor_key),
                "matched_epg": record_to_epg.get(matched_key),
            }
        )

    metrics: dict[str, float | None] = {}
    details: dict[str, dict[str, Any]] = {}

    # TC-01 Entity purity
    entity_to_epgs: dict[str, set[str]] = defaultdict(set)
    for entry in entity_entries:
        entity_id = entry["resolved_entity_id"]
        epg = entry["epg"]
        if entity_id and epg:
            entity_to_epgs[entity_id].add(epg)
    pure_entities = sum(1 for epg_set in entity_to_epgs.values() if len(epg_set) == 1)
    total_entities_with_epg = len(entity_to_epgs)
    metrics["Entity_EPG_Purity_Rate"] = safe_rate(pure_entities, total_entities_with_epg)
    details["Entity_EPG_Purity_Rate"] = {
        "pure_entities": pure_entities,
        "total_entities_with_epg": total_entities_with_epg,
    }

    # TC-02 EPG split rate
    epg_to_entities: dict[str, set[str]] = defaultdict(set)
    for entry in entity_entries:
        epg = entry["epg"]
        entity_id = entry["resolved_entity_id"]
        if epg and entity_id:
            epg_to_entities[epg].add(entity_id)
    split_epg = sum(1 for entities in epg_to_entities.values() if len(entities) > 1)
    total_epg = len(epg_to_entities)
    metrics["EPG_Split_Rate"] = safe_rate(split_epg, total_epg)
    details["EPG_Split_Rate"] = {
        "split_epg": split_epg,
        "total_epg": total_epg,
    }

    # TC-03 Cross-EPG merge rate
    considered_pairs = 0
    cross_epg_pairs = 0
    for pair in pair_entries:
        if not pair["anchor_epg"] or not pair["matched_epg"]:
            continue
        considered_pairs += 1
        if pair["anchor_epg"] != pair["matched_epg"]:
            cross_epg_pairs += 1
    metrics["Cross_EPG_Merge_Rate"] = safe_rate(cross_epg_pairs, considered_pairs)
    details["Cross_EPG_Merge_Rate"] = {
        "cross_epg_pairs": cross_epg_pairs,
        "considered_pairs": considered_pairs,
    }

    # TC-04 Same EPG link recall proxy
    epg_entity_counter: dict[str, Counter[str]] = defaultdict(Counter)
    for entry in entity_entries:
        epg = entry["epg"]
        entity_id = entry["resolved_entity_id"]
        if epg and entity_id:
            epg_entity_counter[epg][entity_id] += 1
    total_same_epg_pairs = 0
    linked_same_epg_pairs = 0
    for entity_counter in epg_entity_counter.values():
        n = sum(entity_counter.values())
        total_same_epg_pairs += comb2(n)
        linked_same_epg_pairs += sum(comb2(count) for count in entity_counter.values())
    metrics["Same_EPG_Link_Recall_Proxy"] = safe_rate(linked_same_epg_pairs, total_same_epg_pairs)
    details["Same_EPG_Link_Recall_Proxy"] = {
        "linked_same_epg_pairs": linked_same_epg_pairs,
        "total_same_epg_pairs": total_same_epg_pairs,
    }

    # TC-05 WhyRecords coverage
    total_pairs_all = len(pair_entries)
    why_records_ok = sum(1 for pair in pair_entries if pair["why_records_ok"])
    metrics["WhyRecords_Coverage"] = safe_rate(why_records_ok, total_pairs_all)
    details["WhyRecords_Coverage"] = {
        "why_records_ok": why_records_ok,
        "total_matched_pairs": total_pairs_all,
    }

    # TC-06 WhyEntity coverage
    matched_entity_entries = [entry for entry in entity_entries if entry["match_level"] > 0]
    total_matched_records = len(matched_entity_entries)
    why_entity_ok = sum(1 for entry in matched_entity_entries if entry["why_entity_ok"])
    metrics["WhyEntity_Coverage"] = safe_rate(why_entity_ok, total_matched_records)
    details["WhyEntity_Coverage"] = {
        "why_entity_ok": why_entity_ok,
        "total_matched_records": total_matched_records,
    }

    # TC-07 Top match key concentration
    match_key_counts = Counter(pair["match_key"] for pair in pair_entries if pair["match_key"])
    total_match_key = sum(match_key_counts.values())
    top3_share = sum(count for _, count in match_key_counts.most_common(3))
    metrics["Top_Match_Key_Concentration"] = safe_rate(top3_share, total_match_key)
    details["Top_Match_Key_Concentration"] = {
        "top3_count": top3_share,
        "total_with_match_key": total_match_key,
        "top_keys": dict(match_key_counts.most_common(5)),
    }

    # TC-08 Lineage integrity
    lineage_matched = len(input_keys & entity_keys)
    metrics["Lineage_Integrity_Rate"] = safe_rate(lineage_matched, len(input_keys))
    details["Lineage_Integrity_Rate"] = {
        "lineage_matched": lineage_matched,
        "input_keys": len(input_keys),
        "entity_keys": len(entity_keys),
    }

    # TC-09 High-confidence cross-EPG merge rate
    high_conf_cross = 0
    for pair in pair_entries:
        if not pair["anchor_epg"] or not pair["matched_epg"]:
            continue
        if pair["anchor_epg"] == pair["matched_epg"]:
            continue
        if pair["match_level"] >= args.high_confidence_level:
            high_conf_cross += 1
    metrics["High_Confidence_Cross_EPG_Merge_Rate"] = safe_rate(high_conf_cross, considered_pairs)
    details["High_Confidence_Cross_EPG_Merge_Rate"] = {
        "high_conf_cross_epg_pairs": high_conf_cross,
        "considered_pairs": considered_pairs,
        "high_confidence_level": args.high_confidence_level,
    }

    # TC-10 Delta vs baseline
    baseline_value = load_baseline_value(args)
    selected_metric_value = metrics.get(args.baseline_metric)
    delta_vs_baseline = None
    if selected_metric_value is not None and baseline_value is not None:
        delta_vs_baseline = selected_metric_value - baseline_value
    metrics["Delta_vs_Current_Engine"] = delta_vs_baseline
    details["Delta_vs_Current_Engine"] = {
        "baseline_metric": args.baseline_metric,
        "baseline_value": baseline_value,
        "senzing_value": selected_metric_value,
    }

    results: list[dict[str, Any]] = []

    def add_result(case_id: str, value: float | None, op: str, threshold: float) -> None:
        status, passed = evaluate_threshold(value, op, threshold)
        meta = CASE_METADATA[case_id]
        results.append(
            {
                "test_case_id": case_id,
                "management_question": meta["management_question"],
                "metric_name": meta["metric_name"],
                "value": value,
                "value_percent": format_percent(value) if case_id != "TC-10" else ("N/A" if value is None else f"{value:.6f}"),
                "threshold": meta["threshold"],
                "status": status,
                "passed": passed,
                "details": details.get(meta["metric_name"], {}),
            }
        )

    add_result("TC-01", metrics["Entity_EPG_Purity_Rate"], ">=", 0.95)
    add_result("TC-02", metrics["EPG_Split_Rate"], "<=", 0.10)
    add_result("TC-03", metrics["Cross_EPG_Merge_Rate"], "<=", 0.05)
    add_result("TC-04", metrics["Same_EPG_Link_Recall_Proxy"], ">=", 0.90)
    add_result("TC-05", metrics["WhyRecords_Coverage"], ">=", 0.95)
    add_result("TC-06", metrics["WhyEntity_Coverage"], ">=", 0.95)
    add_result("TC-07", metrics["Top_Match_Key_Concentration"], ">=", 0.70)
    add_result("TC-08", metrics["Lineage_Integrity_Rate"], "=", 1.00)
    add_result("TC-09", metrics["High_Confidence_Cross_EPG_Merge_Rate"], "<=", args.high_confidence_cross_epg_threshold)

    tc10_status = "NOT_EVALUATED"
    tc10_passed = None
    if delta_vs_baseline is not None:
        tc10_status, tc10_passed = evaluate_threshold(delta_vs_baseline, ">=", 0.0)
    results.append(
        {
            "test_case_id": "TC-10",
            "management_question": CASE_METADATA["TC-10"]["management_question"],
            "metric_name": CASE_METADATA["TC-10"]["metric_name"],
            "value": delta_vs_baseline,
            "value_percent": "N/A" if delta_vs_baseline is None else f"{delta_vs_baseline:.6f}",
            "threshold": CASE_METADATA["TC-10"]["threshold"],
            "status": tc10_status,
            "passed": tc10_passed,
            "details": details["Delta_vs_Current_Engine"],
        }
    )

    pass_count = sum(1 for item in results if item["status"] == "PASS")
    fail_count = sum(1 for item in results if item["status"] == "FAIL")
    not_eval_count = sum(1 for item in results if item["status"] == "NOT_EVALUATED")

    json_out = output_dir / "management_test_results.json"
    csv_out = output_dir / "management_test_results.csv"
    md_out = output_dir / "management_test_summary.md"

    payload = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "run_dir": str(run_dir),
        "input_files": {
            "input_normalized_jsonl": str(input_jsonl),
            "entity_records_csv": str(entity_records_csv),
            "matched_pairs_csv": str(matched_pairs_csv),
        },
        "config": {
            "epg_field_candidates": epg_candidates,
            "high_confidence_level": args.high_confidence_level,
            "high_confidence_cross_epg_threshold": args.high_confidence_cross_epg_threshold,
            "baseline_metric": args.baseline_metric,
            "baseline_value": baseline_value,
        },
        "data_quality": {
            "input_records": len(input_rows),
            "input_keys": len(input_keys),
            "records_with_epg": len(record_to_epg),
            "record_to_epg_conflicts": record_to_epg_conflicts,
            "entity_rows": len(entity_entries),
            "pair_rows": len(pair_entries),
        },
        "summary": {
            "pass": pass_count,
            "fail": fail_count,
            "not_evaluated": not_eval_count,
            "total": len(results),
        },
        "results": results,
    }

    json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with csv_out.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=[
                "test_case_id",
                "metric_name",
                "status",
                "value",
                "value_percent",
                "threshold",
                "management_question",
            ],
        )
        writer.writeheader()
        for item in results:
            writer.writerow(
                {
                    "test_case_id": item["test_case_id"],
                    "metric_name": item["metric_name"],
                    "status": item["status"],
                    "value": "" if item["value"] is None else f"{item['value']:.10f}",
                    "value_percent": item["value_percent"],
                    "threshold": item["threshold"],
                    "management_question": item["management_question"],
                }
            )

    lines: list[str] = []
    lines.append("# Management Test Summary")
    lines.append("")
    lines.append(f"- Run directory: `{run_dir}`")
    lines.append(f"- Generated at: `{payload['generated_at']}`")
    lines.append(f"- PASS: {pass_count}")
    lines.append(f"- FAIL: {fail_count}")
    lines.append(f"- NOT_EVALUATED: {not_eval_count}")
    lines.append("")
    lines.append("| Test Case | Metric | Status | Value | Threshold |")
    lines.append("| --- | --- | --- | --- | --- |")
    for item in results:
        value_text = item["value_percent"]
        lines.append(
            f"| {item['test_case_id']} | {item['metric_name']} | {item['status']} | {value_text} | {item['threshold']} |"
        )

    md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Management tests completed.")
    print(f"  - JSON: {json_out}")
    print(f"  - CSV:  {csv_out}")
    print(f"  - MD:   {md_out}")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

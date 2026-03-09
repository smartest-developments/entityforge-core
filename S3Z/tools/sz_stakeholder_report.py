#!/usr/bin/env python3
"""Generate a stakeholder-friendly summary from Senzing JSONL output.

This script is intentionally simpler than sz_json_analyzer output and is meant
for business stakeholders who need clear, high-level results.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


NAME_KEYS = {"NAME_FULL", "NAME_FIRST", "NAME_LAST", "NAME_ORG"}
ADDRESS_KEYS = {"ADDR_FULL", "ADDR_LINE1", "ADDR_CITY", "ADDR_POSTAL_CODE", "ADDR_COUNTRY"}
TAX_ID_KEYS = {"TAX_ID_NUMBER"}
OTHER_ID_KEYS = {"OTHER_ID_NUMBER"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read JSONL records."""
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as infile:
        for line_number, line in enumerate(infile, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                item = json.loads(text)
            except json.JSONDecodeError as err:
                raise ValueError(f"Invalid JSON on line {line_number}: {err}") from err
            if not isinstance(item, dict):
                raise ValueError(f"Line {line_number} is not a JSON object.")
            records.append(item)
    return records


def parse_analyzer_markdown(path: Path) -> tuple[list[str], list[str]]:
    """Extract compact critical error and warning rows from analyzer markdown."""
    critical_rows: list[str] = []
    warning_rows: list[str] = []
    if not path.exists():
        return critical_rows, warning_rows

    section = ""
    with path.open("r", encoding="utf-8") as infile:
        for raw_line in infile:
            line = raw_line.strip()
            if line.startswith("## ❌ Critical Errors"):
                section = "critical"
                continue
            if line.startswith("## ⚠️ Warnings"):
                section = "warnings"
                continue
            if line.startswith("## "):
                section = ""
                continue
            if section and line.startswith("|") and not line.startswith("|---"):
                columns = [cell.strip() for cell in line.strip("|").split("|")]
                if not columns or columns[0] == "Attribute":
                    continue
                summary = f"{columns[0]} (records: {columns[1]})" if len(columns) > 1 else columns[0]
                if section == "critical":
                    critical_rows.append(summary)
                elif section == "warnings":
                    warning_rows.append(summary)
    return critical_rows, warning_rows


def feature_presence(record: dict[str, Any]) -> dict[str, bool]:
    """Evaluate core feature presence for one record."""
    features = record.get("FEATURES", [])
    has_name = False
    has_address = False
    has_tax_id = False
    has_other_id = False
    has_partner_id = False
    has_business_relation_id = False
    has_other_id_country = True
    has_addr_full = False
    has_addr_line1 = False

    if not isinstance(features, list):
        features = []

    for feature_obj in features:
        if not isinstance(feature_obj, dict):
            continue
        keys = set(feature_obj.keys())
        if keys & NAME_KEYS:
            has_name = True
        if keys & ADDRESS_KEYS:
            has_address = True
        if "ADDR_FULL" in keys:
            has_addr_full = True
        if "ADDR_LINE1" in keys:
            has_addr_line1 = True
        if keys & TAX_ID_KEYS:
            has_tax_id = True
        if keys & OTHER_ID_KEYS:
            has_other_id = True
            id_type = str(feature_obj.get("OTHER_ID_TYPE", "")).upper()
            if id_type == "PARTNER_ID":
                has_partner_id = True
            if id_type == "BUSINESS_RELATION_ID":
                has_business_relation_id = True
            if "OTHER_ID_COUNTRY" not in feature_obj:
                has_other_id_country = False

    return {
        "has_name": has_name,
        "has_address": has_address,
        "has_tax_id": has_tax_id,
        "has_other_id": has_other_id,
        "has_partner_id": has_partner_id,
        "has_business_relation_id": has_business_relation_id,
        "has_other_id_country": has_other_id_country,
        "has_addr_full": has_addr_full,
        "has_addr_line1": has_addr_line1,
    }


def record_type_value(record: dict[str, Any]) -> str:
    """Return RECORD_TYPE if present."""
    features = record.get("FEATURES", [])
    if not isinstance(features, list):
        return "UNKNOWN"
    for feature_obj in features:
        if isinstance(feature_obj, dict) and "RECORD_TYPE" in feature_obj:
            value = str(feature_obj["RECORD_TYPE"]).strip().upper()
            return value or "UNKNOWN"
    return "UNKNOWN"


def percentage(part: int, total: int) -> str:
    """Format percentage."""
    if total == 0:
        return "0.0%"
    return f"{(part / total) * 100:.1f}%"


def build_report(
    records: list[dict[str, Any]],
    input_path: Path,
    analyzer_critical: list[str],
    analyzer_warnings: list[str],
) -> str:
    """Build stakeholder markdown report."""
    total = len(records)
    record_type_counts = Counter(record_type_value(record) for record in records)
    data_source_counts = Counter(str(r.get("DATA_SOURCE", "MISSING")) for r in records)

    missing_record_id = 0
    missing_name = 0
    missing_address = 0
    missing_tax_id = 0
    with_partner_id = 0
    with_business_relation_id = 0
    other_id_country_complete = 0
    address_with_full = 0
    address_with_line1 = 0

    for record in records:
        if not record.get("RECORD_ID"):
            missing_record_id += 1

        presence = feature_presence(record)
        if not presence["has_name"]:
            missing_name += 1
        if not presence["has_address"]:
            missing_address += 1
        if not presence["has_tax_id"]:
            missing_tax_id += 1
        if presence["has_partner_id"]:
            with_partner_id += 1
        if presence["has_business_relation_id"]:
            with_business_relation_id += 1
        if presence["has_other_id_country"]:
            other_id_country_complete += 1
        if presence["has_addr_full"]:
            address_with_full += 1
        if presence["has_addr_line1"]:
            address_with_line1 += 1

    lines: list[str] = []
    lines.append(f"# Stakeholder Summary - {input_path.name}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Records processed | {total} |")
    lines.append(f"| Data sources in output | {', '.join(f'{k} ({v})' for k, v in sorted(data_source_counts.items()))} |")
    lines.append(f"| Records with Partner ID for matching | {with_partner_id} ({percentage(with_partner_id, total)}) |")
    lines.append(
        f"| Records with Business Relation ID for matching | {with_business_relation_id} ({percentage(with_business_relation_id, total)}) |"
    )
    lines.append(f"| Records missing RECORD_ID | {missing_record_id} ({percentage(missing_record_id, total)}) |")
    lines.append("")

    lines.append("## Entity Mix")
    lines.append("")
    lines.append("| Record Type | Count | Percent |")
    lines.append("|---|---|---|")
    for rtype, count in sorted(record_type_counts.items()):
        lines.append(f"| {rtype} | {count} | {percentage(count, total)} |")
    lines.append("")

    lines.append("## Matching Signal Coverage")
    lines.append("")
    lines.append("| Signal | Coverage |")
    lines.append("|---|---|")
    lines.append(f"| Name | {total - missing_name}/{total} ({percentage(total - missing_name, total)}) |")
    lines.append(f"| Address | {total - missing_address}/{total} ({percentage(total - missing_address, total)}) |")
    lines.append(f"| Tax ID | {total - missing_tax_id}/{total} ({percentage(total - missing_tax_id, total)}) |")
    lines.append(f"| Partner ID | {with_partner_id}/{total} ({percentage(with_partner_id, total)}) |")
    lines.append(
        f"| Business Relation ID | {with_business_relation_id}/{total} ({percentage(with_business_relation_id, total)}) |"
    )
    lines.append("")

    lines.append("## Data Quality Snapshot")
    lines.append("")
    lines.append("| Check | Result |")
    lines.append("|---|---|")
    lines.append(f"| Other ID includes country | {other_id_country_complete}/{total} records complete |")
    lines.append(f"| Address mapped as ADDR_FULL | {address_with_full}/{total} records |")
    lines.append(f"| Address mapped with ADDR_LINE1 | {address_with_line1}/{total} records |")
    lines.append("")

    lines.append("## Analyzer Findings (Simplified)")
    lines.append("")
    if analyzer_critical:
        lines.append("Critical issues:")
        for row in analyzer_critical:
            lines.append(f"- {row}")
    else:
        lines.append("Critical issues: none found.")
    lines.append("")
    if analyzer_warnings:
        lines.append("Warnings:")
        for row in analyzer_warnings:
            lines.append(f"- {row}")
    else:
        lines.append("Warnings: none found.")
    lines.append("")

    lines.append("## Business Interpretation")
    lines.append("")
    lines.append(
        "The dataset is consistently mapped with person/organization typing and includes both Partner ID and Business Relation ID as matching signals."
    )
    lines.append(
        "Before loading into Senzing, ensure the DATA_SOURCE value is registered in Senzing configuration."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate stakeholder-friendly markdown summary from Senzing JSONL.")
    parser.add_argument("input_jsonl", help="Input Senzing JSONL path")
    parser.add_argument("output_md", help="Output markdown report path")
    parser.add_argument(
        "--analyzer-md",
        default=None,
        help="Optional sz_json_analyzer markdown report to include findings",
    )
    args = parser.parse_args()

    input_path = Path(args.input_jsonl)
    output_path = Path(args.output_md)

    if not input_path.exists():
        print(f"ERROR: Input JSONL not found: {input_path}")
        return 2

    try:
        records = read_jsonl(input_path)
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: {err}")
        return 2

    analyzer_critical: list[str] = []
    analyzer_warnings: list[str] = []
    if args.analyzer_md:
        analyzer_path = Path(args.analyzer_md)
        analyzer_critical, analyzer_warnings = parse_analyzer_markdown(analyzer_path)

    report_text = build_report(records, input_path, analyzer_critical, analyzer_warnings)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")

    print(f"Stakeholder report written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

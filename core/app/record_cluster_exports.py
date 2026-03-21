#!/usr/bin/env python3
"""Shared helpers and CLI for record/cluster export artifacts."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from partner_json_to_senzing import infer_field_map, iter_input_records, resolve_value


@dataclass(frozen=True)
class RecordClusterRow:
    record_id: str
    cluster_id: str | None
    data_source: str


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def to_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def effective_cluster_id(row: RecordClusterRow) -> str:
    """Return the cluster identifier to export for audit/report files.

    When source cluster id is missing, keep the row traceable by assigning
    a deterministic placeholder based on the generated record id.
    """
    if row.cluster_id:
        return row.cluster_id
    return f"non-match-{row.record_id}"


def infer_mapper_field_map(
    input_path: Path,
    array_key: str | None,
    fuzzy_cutoff: float,
    scan_records: int,
) -> tuple[dict[str, str], str | None]:
    sample_records: list[dict] = []
    for record in iter_input_records(input_path, array_key):
        sample_records.append(record)
        if len(sample_records) >= scan_records:
            break
    if not sample_records:
        raise ValueError("Input contains no records.")
    field_map = infer_field_map(sample_records, fuzzy_cutoff)
    return field_map, field_map.get("ipg_id")


def detect_input_mode(input_path: Path, array_key: str | None) -> tuple[str, dict[str, str]]:
    sample_iter = iter_input_records(input_path, array_key)
    try:
        first_record = next(sample_iter)
    except StopIteration as err:
        raise ValueError("Input contains no records.") from err

    sample_records = [first_record]
    for _, record in zip(range(24), sample_iter):
        sample_records.append(record)

    normalized_lookup: dict[str, str] = {}
    for record in sample_records:
        for key in record.keys():
            normalized_lookup.setdefault(normalize_key(key), key)
    if "recordid" in normalized_lookup and ("sourceipgid" in normalized_lookup or "ipgid" in normalized_lookup):
        resolved = {
            "record_id": normalized_lookup["recordid"],
            "cluster_id": normalized_lookup.get("sourceipgid") or normalized_lookup.get("ipgid"),
            "data_source": normalized_lookup.get("datasource", ""),
        }
        return "mapped", resolved
    return "source", {}


def iter_record_cluster_rows(
    input_path: Path,
    array_key: str | None,
    fuzzy_cutoff: float,
    scan_records: int,
    data_source: str,
) -> tuple[Iterator[RecordClusterRow], str | None]:
    input_mode, mapped_fields = detect_input_mode(input_path, array_key)
    if input_mode == "mapped":
        cluster_source_key = mapped_fields["cluster_id"]
        record_id_key = mapped_fields["record_id"]
        data_source_key = mapped_fields.get("data_source")

        def mapped_row_iterator() -> Iterator[RecordClusterRow]:
            for record in iter_input_records(input_path, array_key):
                current_data_source = to_text(record.get(data_source_key)) if data_source_key else None
                yield RecordClusterRow(
                    record_id=to_text(record.get(record_id_key)) or "",
                    cluster_id=to_text(record.get(cluster_source_key)),
                    data_source=current_data_source or data_source,
                )

        return mapped_row_iterator(), cluster_source_key

    field_map, ipg_source_key = infer_mapper_field_map(
        input_path=input_path,
        array_key=array_key,
        fuzzy_cutoff=fuzzy_cutoff,
        scan_records=scan_records,
    )

    def row_iterator() -> Iterator[RecordClusterRow]:
        for index, record in enumerate(iter_input_records(input_path, array_key), start=1):
            cluster_id, _ = resolve_value(record, field_map, "ipg_id", fuzzy_cutoff)
            yield RecordClusterRow(
                record_id=str(index),
                cluster_id=cluster_id,
                data_source=data_source,
            )

    return row_iterator(), ipg_source_key


def write_record_id_cluster_csv(
    output_path: Path,
    row_iter: Iterator[RecordClusterRow],
    skip_empty_cluster_id: bool,
) -> tuple[int, int]:
    written_rows = 0
    skipped_rows = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["record_id", "cluster_id"])
        for row in row_iter:
            if skip_empty_cluster_id and not row.cluster_id:
                skipped_rows += 1
                continue
            writer.writerow([row.record_id, effective_cluster_id(row)])
            written_rows += 1
    return written_rows, skipped_rows


def write_truthset_key_csv(
    output_path: Path,
    row_iter: Iterator[RecordClusterRow],
    skip_empty_cluster_id: bool,
) -> tuple[int, int]:
    written_rows = 0
    skipped_rows = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["DATA_SOURCE", "RECORD_ID", "CLUSTER_ID"])
        for row in row_iter:
            if skip_empty_cluster_id and not row.cluster_id:
                skipped_rows += 1
                continue
            writer.writerow([row.data_source, row.record_id, effective_cluster_id(row)])
            written_rows += 1
    return written_rows, skipped_rows


def default_output_path(input_path: Path, export_type: str) -> Path:
    suffix_map = {
        "record-id-cluster": "__cluster_record_ids.csv",
        "truthset-key": "__truthset_key.csv",
    }
    try:
        suffix = suffix_map[export_type]
    except KeyError as err:
        raise ValueError(f"Unsupported export type: {export_type}") from err
    return input_path.with_name(f"{input_path.stem}{suffix}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export record/cluster CSV artifacts using the same RECORD_ID logic as the mapper."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    common_options: list[tuple[tuple[str, ...], dict[str, object]]] = [
        (("input_json",), {"help": "Input JSON/JSONL file path"}),
        (
            ("output_csv",),
            {
                "nargs": "?",
                "default": None,
                "help": "Optional output CSV path. Defaults depend on the selected command.",
            },
        ),
        (("--data-source",), {"default": "PARTNERS", "help": "DATA_SOURCE value used by the mapper (default: PARTNERS)"}),
        (("--array-key",), {"default": None, "help": "Optional key if input root is an object containing an array"}),
        (
            ("--fuzzy-cutoff",),
            {"type": float, "default": 0.90, "help": "Fuzzy key match threshold between 0 and 1 (default: 0.90)"},
        ),
        (
            ("--scan-records",),
            {"type": int, "default": 500, "help": "Max number of input records used for field-map inference (default: 500)"},
        ),
        (
            ("--skip-empty-cluster-id",),
            {"action": "store_true", "help": "Skip rows where IPG ID is missing or empty"},
        ),
    ]

    for command, help_text in [
        ("record-id-cluster", "Export a simple record_id,cluster_id CSV"),
        ("truthset-key", "Export a Senzing audit-ready DATA_SOURCE,RECORD_ID,CLUSTER_ID CSV"),
    ]:
        subparser = subparsers.add_parser(command, help=help_text)
        for args, kwargs in common_options:
            subparser.add_argument(*args, **kwargs)

    return parser


def run_cli() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_path = Path(args.input_json).expanduser().resolve()
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2
    if not 0.0 <= args.fuzzy_cutoff <= 1.0:
        print("ERROR: --fuzzy-cutoff must be between 0 and 1", file=sys.stderr)
        return 2

    output_path = (
        Path(args.output_csv).expanduser().resolve()
        if args.output_csv
        else default_output_path(input_path, args.command).resolve()
    )

    try:
        row_iter, ipg_source_key = iter_record_cluster_rows(
            input_path=input_path,
            array_key=args.array_key,
            fuzzy_cutoff=args.fuzzy_cutoff,
            scan_records=args.scan_records,
            data_source=args.data_source,
        )
        if args.command == "record-id-cluster":
            written_rows, skipped_rows = write_record_id_cluster_csv(
                output_path=output_path,
                row_iter=row_iter,
                skip_empty_cluster_id=args.skip_empty_cluster_id,
            )
        else:
            written_rows, skipped_rows = write_truthset_key_csv(
                output_path=output_path,
                row_iter=row_iter,
                skip_empty_cluster_id=args.skip_empty_cluster_id,
            )
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Unable to export CSV: {err}", file=sys.stderr)
        return 2

    print(f"Command: {args.command}")
    print(f"Input file: {input_path}")
    print(f"Output CSV: {output_path}")
    print(f"Inferred IPG source key: {ipg_source_key or '<NOT_FOUND>'}")
    print(f"Written rows: {written_rows}")
    print(f"Skipped rows: {skipped_rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())

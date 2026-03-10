#!/usr/bin/env python3
"""Export a Senzing audit-ready truthset key CSV from source input records."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from record_cluster_exports import iter_record_cluster_rows


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export DATA_SOURCE/RECORD_ID/CLUSTER_ID CSV for sz_audit prior file."
    )
    parser.add_argument("input_json", help="Input JSON/JSONL file path")
    parser.add_argument(
        "output_csv",
        nargs="?",
        default=None,
        help="Optional output CSV path. Default: <input_stem>__truthset_key.csv",
    )
    parser.add_argument(
        "--data-source",
        default="PARTNERS",
        help="DATA_SOURCE value used by the mapper (default: PARTNERS)",
    )
    parser.add_argument(
        "--array-key",
        default=None,
        help="Optional key if input root is an object containing an array",
    )
    parser.add_argument(
        "--fuzzy-cutoff",
        type=float,
        default=0.90,
        help="Fuzzy key match threshold between 0 and 1 (default: 0.90)",
    )
    parser.add_argument(
        "--scan-records",
        type=int,
        default=500,
        help="Max number of input records used for field-map inference (default: 500)",
    )
    parser.add_argument(
        "--skip-empty-cluster-id",
        action="store_true",
        help="Skip rows where IPG ID is missing or empty",
    )
    return parser


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}__truthset_key.csv")


def main() -> int:
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
        else default_output_path(input_path).resolve()
    )

    written_rows = 0
    skipped_rows = 0

    try:
        row_iter, ipg_source_key = iter_record_cluster_rows(
            input_path=input_path,
            array_key=args.array_key,
            fuzzy_cutoff=args.fuzzy_cutoff,
            scan_records=args.scan_records,
            data_source=args.data_source,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["DATA_SOURCE", "RECORD_ID", "CLUSTER_ID"])
            for row in row_iter:
                if args.skip_empty_cluster_id and not row.cluster_id:
                    skipped_rows += 1
                    continue
                writer.writerow([row.data_source, row.record_id, row.cluster_id or ""])
                written_rows += 1
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Unable to export CSV: {err}", file=sys.stderr)
        return 2

    print(f"Input file: {input_path}")
    print(f"Output CSV: {output_path}")
    print(f"Inferred IPG source key: {ipg_source_key or '<NOT_FOUND>'}")
    print(f"Written rows: {written_rows}")
    print(f"Skipped rows: {skipped_rows}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

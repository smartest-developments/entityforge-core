#!/usr/bin/env python3
"""Write the first N records from a source JSON/JSONL file to JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from partner_json_to_senzing import iter_input_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a JSONL file containing the first N input records.")
    parser.add_argument("input_json", help="Source JSON or JSONL input file")
    parser.add_argument("output_jsonl", help="Target JSONL path")
    parser.add_argument("--limit", type=int, required=True, help="Number of records to keep")
    parser.add_argument("--array-key", default=None, help="Optional array key when the root JSON is an object")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit <= 0:
        raise SystemExit("--limit must be greater than zero")

    input_path = Path(args.input_json).expanduser().resolve()
    output_path = Path(args.output_jsonl).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    with output_path.open("w", encoding="utf-8") as outfile:
        for written, record in enumerate(iter_input_records(input_path, args.array_key), start=1):
            outfile.write(json.dumps(record, ensure_ascii=False))
            outfile.write("\n")
            if written >= args.limit:
                break

    print(f"Input file: {input_path}")
    print(f"Output JSONL: {output_path}")
    print(f"Requested limit: {args.limit}")
    print(f"Written records: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

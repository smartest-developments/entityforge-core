#!/usr/bin/env python3
"""Run whyRecords for selected pairs inside a compatible runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_senzing_end_to_end import extract_reason_summary, init_g2_engine, run_sdk_why_records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute whyRecords for a list of record pairs.")
    parser.add_argument("--project-dir", required=True, help="Senzing project directory")
    parser.add_argument("--pairs-json", required=True, help="Input JSON file with requested pairs")
    parser.add_argument("--output-jsonl", required=True, help="Output JSONL path")
    parser.add_argument("--data-source", default="PARTNERS", help="Default DATA_SOURCE")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    pairs_json = Path(args.pairs_json).expanduser().resolve()
    output_jsonl = Path(args.output_jsonl).expanduser().resolve()

    project_setup_env = project_dir / "setupEnv"
    requests = json.loads(pairs_json.read_text(encoding="utf-8"))
    if not isinstance(requests, list):
        raise ValueError("pairs-json must contain a JSON list")

    g2 = None
    factory = None
    try:
        g2, factory, engine_details = init_g2_engine(project_dir, project_setup_env)
        if not g2:
            raise RuntimeError(str(engine_details.get("error") or "Unable to initialize SDK engine"))
        output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with output_jsonl.open("w", encoding="utf-8") as outfile:
            for item in requests:
                if not isinstance(item, dict):
                    continue
                cluster_id = str(item.get("cluster_id") or "").strip()
                left_record_id = str(item.get("left_record_id") or "").strip()
                right_record_id = str(item.get("right_record_id") or "").strip()
                left_data_source = str(item.get("left_data_source") or args.data_source).strip() or args.data_source
                right_data_source = str(item.get("right_data_source") or args.data_source).strip() or args.data_source
                result = run_sdk_why_records(g2, left_data_source, left_record_id, right_data_source, right_record_id)
                enriched = {
                    "cluster_id": cluster_id,
                    "left_record_id": left_record_id,
                    "right_record_id": right_record_id,
                    "ok": bool(result.get("ok")),
                    "method": result.get("method"),
                    "reason_summary": extract_reason_summary(result.get("output_json"), result.get("output_text")),
                    "error": result.get("error"),
                    "output_json": result.get("output_json"),
                    "output_text": result.get("output_text"),
                }
                outfile.write(json.dumps(enriched, ensure_ascii=False) + "\n")
    finally:
        try:
            if g2 and hasattr(g2, "destroy"):
                g2.destroy()
        except Exception:
            pass
        try:
            if factory and hasattr(factory, "destroy"):
                factory.destroy()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

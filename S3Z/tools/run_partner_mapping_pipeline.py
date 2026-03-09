#!/usr/bin/env python3
"""Master wrapper for the full partner-to-Senzing pipeline.

This script runs all steps in sequence:
1. Convert source JSON array to Senzing JSONL
2. Lint generated JSONL
3. Run Senzing JSON analyzer
4. Generate stakeholder-friendly summary

The wrapper is intentionally lightweight and uses standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_DATA_SOURCE = "PARTNERS"


def run_step(step_name: str, command: list[str], log_file: Path) -> dict[str, Any]:
    """Execute one pipeline step and capture logs."""
    start = time.time()
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration_seconds = round(time.time() - start, 3)

    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("w", encoding="utf-8") as outfile:
        outfile.write(f"STEP: {step_name}\n")
        outfile.write(f"COMMAND: {' '.join(command)}\n")
        outfile.write(f"EXIT_CODE: {result.returncode}\n")
        outfile.write(f"DURATION_SECONDS: {duration_seconds}\n")
        outfile.write("\n--- STDOUT ---\n")
        outfile.write(result.stdout or "")
        outfile.write("\n--- STDERR ---\n")
        outfile.write(result.stderr or "")

    return {
        "step": step_name,
        "exit_code": result.returncode,
        "duration_seconds": duration_seconds,
        "log_file": str(log_file),
        "stdout_tail": (result.stdout or "")[-1200:],
        "stderr_tail": (result.stderr or "")[-1200:],
        "ok": result.returncode == 0,
    }


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser."""
    parser = argparse.ArgumentParser(description="Run full partner mapping pipeline (convert + lint + analyze + stakeholder report).")
    parser.add_argument("input_json", help="Input JSON file (array of records)")
    parser.add_argument("--output-root", default="mapper_runs", help="Root folder for timestamped pipeline runs")
    parser.add_argument("--run-name-prefix", default="partner_pipeline", help="Run folder prefix (default: partner_pipeline)")
    parser.add_argument(
        "--include-unmapped-source-fields",
        action="store_true",
        help="Include non-mapped source fields in payload as SRC_* keys",
    )
    parser.add_argument(
        "--tax-id-type",
        default="TIN",
        help="TAX_ID_TYPE value (default: TIN)",
    )
    parser.add_argument("--python-bin", default=sys.executable, help="Python executable for child scripts")
    return parser


def main() -> int:
    """Entry point."""
    args = build_parser().parse_args()

    input_path = Path(args.input_json)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    tools_dir = Path(__file__).resolve().parent
    mapper_script = tools_dir / "partner_json_to_senzing.py"
    linter_script = tools_dir / "lint_senzing_json.py"
    analyzer_script = tools_dir / "sz_json_analyzer.py"
    stakeholder_script = tools_dir / "sz_stakeholder_report.py"

    required_scripts = [mapper_script, linter_script, analyzer_script, stakeholder_script]
    missing = [str(path) for path in required_scripts if not path.exists()]
    if missing:
        print("ERROR: Required scripts are missing:", file=sys.stderr)
        for item in missing:
            print(f"  - {item}", file=sys.stderr)
        return 2

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.output_root) / f"{args.run_name_prefix}_{timestamp}"
    logs_dir = run_dir / "logs"
    run_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    output_jsonl = run_dir / "output.jsonl"
    field_map_json = run_dir / "field_map.json"
    analyzer_md = run_dir / "analysis.md"
    stakeholder_md = run_dir / "stakeholder_summary.md"
    summary_json = run_dir / "pipeline_summary.json"

    print(f"Run directory: {run_dir}")
    print(f"DATA_SOURCE: {DEFAULT_DATA_SOURCE}")
    print("Starting pipeline...")

    steps: list[dict[str, Any]] = []

    mapper_command = [
        args.python_bin,
        str(mapper_script),
        str(input_path),
        str(output_jsonl),
        "--data-source",
        DEFAULT_DATA_SOURCE,
        "--tax-id-type",
        args.tax_id_type,
        "--write-field-map",
        str(field_map_json),
    ]
    if args.include_unmapped_source_fields:
        mapper_command.append("--include-unmapped-source-fields")
    mapper_result = run_step("convert", mapper_command, logs_dir / "01_convert.log")
    steps.append(mapper_result)
    if not mapper_result["ok"]:
        print("FAILED at step: convert")
        return_code = 1
    else:
        lint_command = [args.python_bin, str(linter_script), str(output_jsonl)]
        lint_result = run_step("lint", lint_command, logs_dir / "02_lint.log")
        steps.append(lint_result)
        if not lint_result["ok"]:
            print("FAILED at step: lint")
            return_code = 1
        else:
            analyzer_command = [args.python_bin, str(analyzer_script), str(output_jsonl), "-o", str(analyzer_md)]
            analyzer_result = run_step("analyze", analyzer_command, logs_dir / "03_analyze.log")
            steps.append(analyzer_result)
            if not analyzer_result["ok"]:
                print("FAILED at step: analyze")
                return_code = 1
            else:
                stakeholder_command = [
                    args.python_bin,
                    str(stakeholder_script),
                    str(output_jsonl),
                    str(stakeholder_md),
                    "--analyzer-md",
                    str(analyzer_md),
                ]
                stakeholder_result = run_step("stakeholder_report", stakeholder_command, logs_dir / "04_stakeholder.log")
                steps.append(stakeholder_result)
                return_code = 0 if stakeholder_result["ok"] else 1

    overall_ok = return_code == 0
    summary = {
        "overall_ok": overall_ok,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_file": str(input_path),
        "data_source": DEFAULT_DATA_SOURCE,
        "run_directory": str(run_dir),
        "artifacts": {
            "output_jsonl": str(output_jsonl),
            "field_map_json": str(field_map_json),
            "analysis_md": str(analyzer_md),
            "stakeholder_summary_md": str(stakeholder_md),
            "logs_dir": str(logs_dir),
        },
        "steps": steps,
    }
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Pipeline complete. Success={overall_ok}")
    print(f"Artifacts: {run_dir}")
    print(f"Summary: {summary_json}")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())

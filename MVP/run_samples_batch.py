#!/usr/bin/env python3
"""Run MVP pipeline for one or more sample inputs in a directory."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MVP pipeline for sample JSON/JSONL inputs")
    parser.add_argument("--sample-dir", default="sample_input", help="Directory with input JSON samples")
    parser.add_argument("--execution-mode", choices=["auto", "docker", "local"], default="auto")
    parser.add_argument("--senzing-env", default=None, help="Optional setupEnv path for local mode")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop at first error")
    return parser.parse_args()


def now_timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def classify_input(sample_path: Path) -> tuple[bool, str | None]:
    if sample_path.suffix.lower() == ".jsonl":
        return True, None
    try:
        payload = json.loads(sample_path.read_text(encoding="utf-8"))
    except Exception:
        return False, None

    if isinstance(payload, list):
        return True, None
    if isinstance(payload, dict):
        for candidate in ["records", "data", "items"]:
            if isinstance(payload.get(candidate), list):
                return True, candidate
    return False, None


def run_one(
    mvp_root: Path,
    sample_path: Path,
    execution_mode: str,
    senzing_env: str | None,
    input_array_key: str | None,
) -> tuple[int, list[str]]:
    command = [
        sys.executable,
        str(mvp_root / "run_mvp_pipeline.py"),
        "--input-json",
        str(sample_path),
        "--execution-mode",
        execution_mode,
    ]
    if input_array_key:
        command.extend(["--input-array-key", input_array_key])
    if senzing_env:
        command.extend(["--senzing-env", senzing_env])
    proc = subprocess.run(command, cwd=str(mvp_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = (proc.stdout + "\n" + proc.stderr).strip().splitlines()[-20:]
    return proc.returncode, tail


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parent
    sample_dir = (mvp_root / args.sample_dir).resolve()

    if not sample_dir.exists() or not sample_dir.is_dir():
        print(f"ERROR: sample dir not found: {sample_dir}", file=sys.stderr)
        return 2

    discovered = sorted(
        path
        for pattern in ("*.json", "*.jsonl")
        for path in sample_dir.glob(pattern)
        if path.is_file()
    )
    sample_entries: list[tuple[Path, str | None]] = []
    for sample_path in discovered:
        supported, array_key = classify_input(sample_path)
        if supported:
            sample_entries.append((sample_path, array_key))
        else:
            print(f"Skipping unsupported file: {sample_path.name}")

    if not sample_entries:
        print(f"ERROR: no .json/.jsonl files found in {sample_dir}", file=sys.stderr)
        return 2

    started_at = dt.datetime.now().isoformat(timespec="seconds")
    results: list[dict[str, object]] = []

    for sample, input_array_key in sample_entries:
        print(f"Running: {sample.name}")
        exit_code, tail = run_one(mvp_root, sample, args.execution_mode, args.senzing_env, input_array_key)
        status = "ok" if exit_code == 0 else "failed"
        print(f"  -> {status} (exit {exit_code})")
        if input_array_key:
            print(f"  -> input-array-key: {input_array_key}")
        results.append(
            {
                "sample": sample.name,
                "sample_path": str(sample),
                "input_array_key": input_array_key,
                "status": status,
                "exit_code": exit_code,
                "log_tail": tail,
            }
        )
        if exit_code != 0 and args.stop_on_error:
            break

    summary = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "started_at": started_at,
        "sample_dir": str(sample_dir),
        "execution_mode": args.execution_mode,
        "senzing_env": args.senzing_env,
        "total": len(results),
        "ok": sum(1 for item in results if item.get("status") == "ok"),
        "failed": sum(1 for item in results if item.get("status") == "failed"),
        "results": results,
    }

    output_dir = (mvp_root / "output").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / f"batch_run_summary_{now_timestamp()}.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"\nBatch summary: {summary_path}")
    print(f"OK: {summary['ok']}  FAILED: {summary['failed']}")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

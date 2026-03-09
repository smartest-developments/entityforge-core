#!/usr/bin/env python3
"""Run Senzing end-to-end with the same command flow used manually.

This script intentionally uses Senzing CLI tools in shell order:
1. Create project (`sz_create_project` / `G2CreateProject.py`)
2. source <project>/setupEnv
3. Configure DATA_SOURCE (`sz_configtool`)
4. Load input JSONL (`sz_file_loader`)
5. Snapshot (`sz_snapshot`)
6. Export (`sz_export -o <file>`)
7. Extract matched records from export
8. Run explain for matched records using Python SDK (`G2Engine`)

Input must already be Senzing-ready JSON objects (JSONL or JSON array).
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import csv
import datetime as dt
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def now_timestamp() -> str:
    """Return timestamp suitable for directory naming."""
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def read_records(input_path: Path) -> list[dict[str, Any]]:
    """Read Senzing-ready records from JSONL or JSON array."""
    if input_path.suffix.lower() == ".jsonl":
        records: list[dict[str, Any]] = []
        with input_path.open("r", encoding="utf-8") as infile:
            for line_no, line in enumerate(infile, start=1):
                text = line.strip()
                if not text:
                    continue
                obj = json.loads(text)
                if not isinstance(obj, dict):
                    raise ValueError(f"Line {line_no} is not a JSON object")
                records.append(obj)
        return records

    with input_path.open("r", encoding="utf-8") as infile:
        data = json.load(infile)
    if not isinstance(data, list):
        raise ValueError("JSON input must be an array of objects")
    records = []
    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Record {idx} is not a JSON object")
        records.append(item)
    return records


def parse_csv_items(value: str | None) -> list[str]:
    """Parse comma-separated CLI values into a stable de-duplicated list."""
    if value is None:
        return []
    seen: set[str] = set()
    items: list[str] = []
    for raw in value.split(","):
        token = raw.strip()
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        items.append(token)
    return items


def count_non_empty_lines(path: Path) -> int:
    """Count non-empty lines in a text file."""
    total = 0
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                total += 1
    return total


def normalize_input_to_jsonl(
    input_path: Path,
    normalized_jsonl_path: Path,
    provided_data_sources: list[str],
    use_input_jsonl_directly: bool,
) -> tuple[int, list[str], Path]:
    """Normalize supported input formats to JSONL and extract metadata."""
    if use_input_jsonl_directly:
        if input_path.suffix.lower() != ".jsonl":
            raise ValueError("--use-input-jsonl-directly requires .jsonl input")
        if not provided_data_sources:
            raise ValueError("--use-input-jsonl-directly requires --data-sources")
        record_count = count_non_empty_lines(input_path)
        if record_count <= 0:
            raise ValueError("Input contains no records.")
        return record_count, provided_data_sources, input_path

    data_sources_found: set[str] = set()
    record_count = 0

    if input_path.suffix.lower() == ".jsonl":
        with input_path.open("r", encoding="utf-8") as infile, normalized_jsonl_path.open("w", encoding="utf-8") as outfile:
            for line_no, line in enumerate(infile, start=1):
                text = line.strip()
                if not text:
                    continue
                obj = json.loads(text)
                if not isinstance(obj, dict):
                    raise ValueError(f"Line {line_no} is not a JSON object")
                data_source = str(obj.get("DATA_SOURCE", "")).strip()
                if data_source:
                    data_sources_found.add(data_source)
                outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
                record_count += 1
    else:
        with input_path.open("r", encoding="utf-8") as infile:
            data = json.load(infile)
        if not isinstance(data, list):
            raise ValueError("JSON input must be an array of objects")

        with normalized_jsonl_path.open("w", encoding="utf-8") as outfile:
            for idx, item in enumerate(data, start=1):
                if not isinstance(item, dict):
                    raise ValueError(f"Record {idx} is not a JSON object")
                data_source = str(item.get("DATA_SOURCE", "")).strip()
                if data_source:
                    data_sources_found.add(data_source)
                outfile.write(json.dumps(item, ensure_ascii=False) + "\n")
                record_count += 1

    if record_count <= 0:
        raise ValueError("Input contains no records.")

    data_sources = provided_data_sources or sorted(data_sources_found)
    if not data_sources:
        raise ValueError("No DATA_SOURCE found in input records.")

    return record_count, data_sources, normalized_jsonl_path


def run_shell_step(
    step_name: str,
    shell_command: str,
    log_path: Path,
    timeout_seconds: int | None = None,
) -> dict[str, Any]:
    """Run one shell command and store stdout/stderr into log file."""
    start = time.time()
    timed_out = False
    try:
        result = subprocess.run(
            ["bash", "-lc", shell_command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout_seconds,
        )
        exit_code = result.returncode
        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""
    except subprocess.TimeoutExpired as err:
        timed_out = True
        exit_code = 124
        if isinstance(err.stdout, bytes):
            stdout_text = err.stdout.decode("utf-8", errors="replace")
        else:
            stdout_text = err.stdout or ""
        if isinstance(err.stderr, bytes):
            stderr_text = err.stderr.decode("utf-8", errors="replace")
        else:
            stderr_text = err.stderr or ""
        timeout_msg = f"Command timed out after {timeout_seconds} seconds."
        stderr_text = f"{stderr_text}\n{timeout_msg}" if stderr_text else timeout_msg

    elapsed = round(time.time() - start, 3)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as outfile:
        outfile.write(f"STEP: {step_name}\n")
        outfile.write(f"COMMAND: {shell_command}\n")
        outfile.write(f"EXIT_CODE: {exit_code}\n")
        outfile.write(f"TIMED_OUT: {timed_out}\n")
        outfile.write(f"TIMEOUT_SECONDS: {timeout_seconds if timeout_seconds is not None else 'none'}\n")
        outfile.write(f"DURATION_SECONDS: {elapsed}\n")
        outfile.write("\n--- STDOUT ---\n")
        outfile.write(stdout_text)
        outfile.write("\n--- STDERR ---\n")
        outfile.write(stderr_text)

    return {
        "step": step_name,
        "ok": exit_code == 0,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_seconds": elapsed,
        "log_file": str(log_path),
        "stdout_tail": stdout_text[-1200:],
        "stderr_tail": stderr_text[-1200:],
    }


def build_load_command(
    project_setup_env: Path,
    input_jsonl: Path,
    num_threads: int,
    no_shuffle: bool = False,
) -> str:
    """Build sz_file_loader shell command."""
    cmd = (
        f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1 && "
        f"sz_file_loader -f {shlex.quote(str(input_jsonl))}"
    )
    if num_threads > 0:
        cmd += f" -nt {num_threads}"
    if no_shuffle:
        cmd += " --no-shuffle"
    return cmd


def build_snapshot_command(
    project_setup_env: Path,
    snapshot_prefix: Path,
    thread_count: int,
    force_sdk: bool = False,
) -> str:
    """Build sz_snapshot shell command."""
    cmd = (
        f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1 && "
        f"sz_snapshot -o {shlex.quote(str(snapshot_prefix))} -Q"
    )
    if thread_count > 0:
        cmd += f" -t {thread_count}"
    if force_sdk:
        cmd += " -F"
    return cmd


def load_setup_env(project_setup_env: Path) -> dict[str, str]:
    """Load environment variables by sourcing setupEnv in a subshell."""
    cmd = f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1 && env -0"
    result = subprocess.run(
        ["bash", "-lc", cmd],
        capture_output=True,
        text=False,
        check=False,
    )
    if result.returncode != 0:
        return {}

    env_map: dict[str, str] = {}
    for item in result.stdout.split(b"\x00"):
        if not item or b"=" not in item:
            continue
        key, value = item.split(b"=", 1)
        env_map[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return env_map


def build_engine_config_json(project_dir: Path) -> str:
    """Build a fallback G2Engine config JSON based on project directory layout."""
    payload = {
        "PIPELINE": {
            "CONFIGPATH": str(project_dir / "etc"),
            "SUPPORTPATH": str(project_dir / "data"),
            "RESOURCEPATH": str(project_dir / "resources"),
        },
        "SQL": {
            "CONNECTION": f"sqlite3://na:na@/{project_dir / 'var' / 'sqlite' / 'G2C.db'}",
        },
    }
    return json.dumps(payload)


def preload_senzing_library(project_dir: Path) -> dict[str, Any]:
    """Preload native SDK libraries so in-process SDK init works in Docker/Linux."""
    details: dict[str, Any] = {
        "ok": False,
        "strategy": None,
        "initial_error": None,
        "final_error": None,
        "libs_seen": 0,
        "libs_loaded": 0,
        "libs_pending": 0,
    }

    lib_dir = project_dir / "lib"
    if not lib_dir.exists():
        details["final_error"] = f"Library directory not found: {lib_dir}"
        return details

    all_libs = sorted([p for p in lib_dir.iterdir() if p.is_file() and p.suffix in (".so", ".dylib")])
    details["libs_seen"] = len(all_libs)
    if not all_libs:
        details["final_error"] = f"No shared libraries found under: {lib_dir}"
        return details

    primary = next((p for p in all_libs if p.name in {"libSz.so", "libSz.dylib"}), all_libs[0])
    rtld_global = getattr(ctypes, "RTLD_GLOBAL", 0)

    def load_library(path: Path) -> None:
        if rtld_global:
            ctypes.CDLL(str(path), mode=rtld_global)
        else:
            ctypes.CDLL(str(path))

    # Fast path: if main library resolves immediately, no bulk preload needed.
    try:
        load_library(primary)
        details["ok"] = True
        details["strategy"] = "primary_only"
        details["libs_loaded"] = 1
        return details
    except Exception as err:  # pylint: disable=broad-exception-caught
        details["initial_error"] = str(err)

    # Fallback: preload all libs with retries to satisfy cross-library dependencies.
    pending = list(all_libs)
    loaded: set[str] = set()
    for _ in range(6):
        next_pending: list[Path] = []
        progressed = 0
        for lib_path in pending:
            try:
                load_library(lib_path)
                loaded.add(str(lib_path))
                progressed += 1
            except Exception:  # pylint: disable=broad-exception-caught
                next_pending.append(lib_path)
        pending = next_pending
        if not pending or progressed == 0:
            break

    details["libs_loaded"] = len(loaded)
    details["libs_pending"] = len(pending)

    try:
        load_library(primary)
        details["ok"] = True
        details["strategy"] = "bulk_preload"
        return details
    except Exception as err:  # pylint: disable=broad-exception-caught
        details["final_error"] = str(err)
        return details


def init_g2_engine(project_dir: Path, project_setup_env: Path) -> tuple[Any | None, Any | None, dict[str, Any]]:
    """Initialize SDK engine for explain calls (supports legacy and modern SDK APIs)."""
    details: dict[str, Any] = {
        "ok": False,
        "sdk_api": None,
        "config_source": None,
        "library_preload": None,
        "error": None,
    }

    loaded_env = load_setup_env(project_setup_env)
    if loaded_env:
        os.environ.update(loaded_env)
        py_path = loaded_env.get("PYTHONPATH", "")
        for part in py_path.split(":"):
            if part and part not in sys.path:
                sys.path.insert(0, part)
    preload_details = preload_senzing_library(project_dir)
    details["library_preload"] = preload_details

    config_json = os.environ.get("SENZING_ENGINE_CONFIGURATION_JSON", "").strip()
    if config_json:
        details["config_source"] = "setupEnv:SENZING_ENGINE_CONFIGURATION_JSON"
    else:
        config_json = build_engine_config_json(project_dir)
        details["config_source"] = "generated_from_project_paths"

    # Legacy API path (G2Engine).
    try:
        from senzing import G2Engine  # type: ignore

        g2 = G2Engine()
        g2.init("mapper_e2e", config_json)
        details["sdk_api"] = "G2Engine"
        details["ok"] = True
        return g2, g2, details
    except Exception as err:  # pylint: disable=broad-exception-caught
        details["legacy_error"] = f"G2Engine init failed: {err}"

    # Modern API path (SzEngine via SzAbstractFactoryCore).
    try:
        from senzing_core import SzAbstractFactoryCore  # type: ignore

        factory = SzAbstractFactoryCore("mapper_e2e", config_json)
        engine = factory.create_engine()
        details["sdk_api"] = "SzEngine"
        details["ok"] = True
        return engine, factory, details
    except Exception as err:  # pylint: disable=broad-exception-caught
        preload_error = preload_details.get("final_error") if isinstance(preload_details, dict) else None
        details["error"] = (
            f"Unable to initialize SDK (G2Engine/SzEngine): {err}"
            + (f" | preload: {preload_error}" if preload_error else "")
        )
        return None, None, details


def try_sdk_call(method: Any, args: list[str]) -> tuple[bool, bytearray | None, str | None]:
    """Call SDK method with common signatures and capture response buffer."""
    response = bytearray()
    try:
        method(*args, response)
        return True, response, None
    except TypeError:
        try:
            method(*args, response, 0)
            return True, response, None
        except Exception as err:  # pylint: disable=broad-exception-caught
            return False, None, str(err)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return False, None, str(err)


def run_sdk_why_entity(g2: Any, data_source: str, record_id: str) -> dict[str, Any]:
    """Run why-entity explain via SDK methods."""
    for method_name in ("whyEntityByRecordID", "whyRecordInEntity"):
        if not hasattr(g2, method_name):
            continue
        ok, response, error = try_sdk_call(getattr(g2, method_name), [data_source, record_id])
        if ok and response is not None:
            output_text = response.decode("utf-8", errors="replace").strip()
            return {
                "ok": True,
                "method": method_name,
                "output_text": output_text,
                "output_json": try_parse_json(output_text),
                "error": None,
            }

    for method_name in ("why_record_in_entity",):
        if not hasattr(g2, method_name):
            continue
        try:
            output_text = str(getattr(g2, method_name)(data_source, record_id)).strip()
            return {
                "ok": True,
                "method": method_name,
                "output_text": output_text,
                "output_json": try_parse_json(output_text),
                "error": None,
            }
        except Exception as err:  # pylint: disable=broad-exception-caught
            return {
                "ok": False,
                "method": method_name,
                "output_text": "",
                "output_json": None,
                "error": str(err),
            }
    return {
        "ok": False,
        "method": None,
        "output_text": "",
        "output_json": None,
        "error": "No supported SDK method available for why entity by record.",
    }


def run_sdk_why_records(
    g2: Any,
    data_source_1: str,
    record_id_1: str,
    data_source_2: str,
    record_id_2: str,
) -> dict[str, Any]:
    """Run why-records explain via SDK methods."""
    if hasattr(g2, "whyRecords"):
        ok, response, error = try_sdk_call(
            getattr(g2, "whyRecords"),
            [data_source_1, record_id_1, data_source_2, record_id_2],
        )
        if ok and response is not None:
            output_text = response.decode("utf-8", errors="replace").strip()
            return {
                "ok": True,
                "method": "whyRecords",
                "output_text": output_text,
                "output_json": try_parse_json(output_text),
                "error": None,
            }
        return {
            "ok": False,
            "method": "whyRecords",
            "output_text": "",
            "output_json": None,
            "error": error or "whyRecords failed.",
        }

    if hasattr(g2, "why_records"):
        try:
            output_text = str(g2.why_records(data_source_1, record_id_1, data_source_2, record_id_2)).strip()
            return {
                "ok": True,
                "method": "why_records",
                "output_text": output_text,
                "output_json": try_parse_json(output_text),
                "error": None,
            }
        except Exception as err:  # pylint: disable=broad-exception-caught
            return {
                "ok": False,
                "method": "why_records",
                "output_text": "",
                "output_json": None,
                "error": str(err),
            }

    return {
        "ok": False,
        "method": None,
        "output_text": "",
        "output_json": None,
        "error": "SDK method whyRecords not available.",
    }


def write_sdk_log(
    log_path: Path,
    step_name: str,
    input_payload: dict[str, Any],
    sdk_result: dict[str, Any],
    duration_seconds: float,
) -> None:
    """Write one explain SDK invocation log file."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "step": step_name,
        "duration_seconds": duration_seconds,
        "input": input_payload,
        "ok": sdk_result.get("ok"),
        "method": sdk_result.get("method"),
        "error": sdk_result.get("error"),
        "output_json": sdk_result.get("output_json"),
        "output_text": sdk_result.get("output_text"),
    }
    log_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def create_project(project_dir: Path, base_setup_env: Path | None, log_path: Path) -> dict[str, Any]:
    """Create an isolated project, trying preferred Senzing commands first."""
    project_dir.parent.mkdir(parents=True, exist_ok=True)
    quoted_project = shlex.quote(str(project_dir))
    base_source = (
        f"source {shlex.quote(str(base_setup_env))} >/dev/null 2>&1 && "
        if base_setup_env is not None
        else ""
    )
    attempts = [
        f"{base_source}/opt/senzing/er/bin/sz_create_project {quoted_project}",
        f"{base_source}sz_create_project {quoted_project}",
        f"{base_source}G2CreateProject.py {quoted_project}",
        f"{base_source}g2createproject.py {quoted_project}",
    ]

    combined_log = {
        "step": "create_project",
        "ok": False,
        "exit_code": 1,
        "duration_seconds": 0.0,
        "log_file": str(log_path),
        "stdout_tail": "",
        "stderr_tail": "",
    }
    start = time.time()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as log:
        log.write("STEP: create_project\n")
        log.write(f"PROJECT_DIR: {project_dir}\n")
        log.write(f"BASE_SETUP_ENV: {base_setup_env if base_setup_env else '<none>'}\n")
        for idx, command in enumerate(attempts, start=1):
            result = subprocess.run(
                ["bash", "-lc", command],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            log.write(f"\n--- ATTEMPT {idx} ---\n")
            log.write(f"COMMAND: {command}\n")
            log.write(f"EXIT_CODE: {result.returncode}\n")
            log.write("\nSTDOUT:\n")
            log.write(result.stdout or "")
            log.write("\nSTDERR:\n")
            log.write(result.stderr or "")

            setup_env = project_dir / "setupEnv"
            if result.returncode == 0 and setup_env.exists():
                combined_log["ok"] = True
                combined_log["exit_code"] = 0
                combined_log["stdout_tail"] = (result.stdout or "")[-1200:]
                combined_log["stderr_tail"] = (result.stderr or "")[-1200:]
                break

            combined_log["stdout_tail"] = (result.stdout or "")[-1200:]
            combined_log["stderr_tail"] = (result.stderr or "")[-1200:]

    combined_log["duration_seconds"] = round(time.time() - start, 3)
    return combined_log


def parse_args() -> argparse.Namespace:
    """Build CLI parser and return parsed args."""
    parser = argparse.ArgumentParser(description="Manual-style Senzing all-in-one runner.")
    parser.add_argument("input_file", help="Senzing-ready input (.jsonl or .json array)")
    parser.add_argument("--output-root", default="senzing_runs", help="Run artifacts root folder")
    parser.add_argument("--run-name-prefix", default="senzing_e2e", help="Run folder prefix")
    parser.add_argument(
        "--project-parent-dir",
        default="/mnt",
        help="Parent directory for isolated project (default: /mnt)",
    )
    parser.add_argument(
        "--project-name-prefix",
        default="Senzing_PoC",
        help="Isolated project name prefix (default: Senzing_PoC)",
    )
    parser.add_argument(
        "--senzing-env",
        default=None,
        help="Optional base setupEnv path. Used only to bootstrap create-project command.",
    )
    parser.add_argument("--skip-snapshot", action="store_true", help="Skip snapshot step")
    parser.add_argument("--skip-export", action="store_true", help="Skip sz_export step")
    parser.add_argument(
        "--skip-comparison",
        action="store_true",
        help="Skip comparison artifact generation from export rows",
    )
    parser.add_argument(
        "--skip-explain",
        action="store_true",
        help="Skip explain phase (whyEntityByRecordID / whyRecords)",
    )
    parser.add_argument(
        "--data-sources",
        default=None,
        help="Optional comma-separated DATA_SOURCE list (e.g. PARTNERS,CRM)",
    )
    parser.add_argument(
        "--use-input-jsonl-directly",
        action="store_true",
        help="Use input .jsonl directly without normalization copy (requires --data-sources)",
    )
    parser.add_argument(
        "--fast-mode",
        action="store_true",
        help=(
            "Performance preset for large loads: skip snapshot/export/explain/comparison "
            "and disable stability retries"
        ),
    )
    parser.add_argument(
        "--max-explain-records",
        type=int,
        default=200,
        help="Maximum matched records to explain (default: 200, 0 = no limit)",
    )
    parser.add_argument(
        "--max-explain-pairs",
        type=int,
        default=200,
        help="Maximum matched pairs to explain (default: 200, 0 = no limit)",
    )
    parser.add_argument(
        "--export-output-name",
        default="entity_export.csv",
        help="Export filename inside run directory (default: entity_export.csv)",
    )
    parser.add_argument(
        "--step-timeout-seconds",
        type=int,
        default=1800,
        help="Timeout for load/snapshot/export/configure shell steps (default: 1800)",
    )
    parser.add_argument(
        "--load-threads",
        type=int,
        default=4,
        help="Worker threads for sz_file_loader primary attempt (default: 4)",
    )
    parser.add_argument(
        "--load-fallback-threads",
        type=int,
        default=1,
        help="Worker threads for sz_file_loader fallback attempt (default: 1)",
    )
    parser.add_argument(
        "--snapshot-threads",
        type=int,
        default=4,
        help="Worker threads for sz_snapshot primary attempt (default: 4)",
    )
    parser.add_argument(
        "--snapshot-fallback-threads",
        type=int,
        default=1,
        help="Worker threads for sz_snapshot fallback attempt (default: 1)",
    )
    parser.add_argument(
        "--disable-stability-retries",
        action="store_true",
        help="Disable automatic fallback retry for load/snapshot.",
    )
    parser.add_argument(
        "--keep-loader-temp-files",
        action="store_true",
        help="Keep temporary shuffled files created by sz_file_loader",
    )
    return parser.parse_args()


def parse_int(value: Any, fallback: int = 0) -> int:
    """Parse integer values from export CSV safely."""
    if value is None:
        return fallback
    text = str(value).strip()
    if not text:
        return fallback
    try:
        return int(text)
    except ValueError:
        return fallback


def parse_export_rows(export_file: Path) -> list[dict[str, str]]:
    """Read sz_export CSV and normalize keys and values."""
    if not export_file.exists():
        return []

    with export_file.open("r", encoding="utf-8", newline="") as infile:
        sample = infile.read(4096)
        infile.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(infile, dialect=dialect)
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                norm_key = key.strip().strip('"').strip().upper()
                norm_value = (value or "").strip().strip('"').strip()
                normalized[norm_key] = norm_value
            if normalized:
                rows.append(normalized)
    return rows


def build_match_inputs(export_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Extract matched records and matched pairs from sz_export rows."""
    first_record_by_entity: dict[str, tuple[str, str]] = {}
    anchor_by_entity: dict[str, tuple[str, str]] = {}
    matched_records: dict[tuple[str, str], dict[str, str]] = {}
    matched_pairs: dict[tuple[str, str, str, str], dict[str, str]] = {}

    for row in export_rows:
        entity_id = row.get("RESOLVED_ENTITY_ID", "")
        data_source = row.get("DATA_SOURCE", "")
        record_id = row.get("RECORD_ID", "")
        match_level = parse_int(row.get("MATCH_LEVEL", "0"), fallback=0)
        match_key = row.get("MATCH_KEY", "")

        if not entity_id or not data_source or not record_id:
            continue

        first_record_by_entity.setdefault(entity_id, (data_source, record_id))
        if match_level == 0:
            anchor_by_entity.setdefault(entity_id, (data_source, record_id))

        if match_level <= 0:
            continue

        matched_records[(data_source, record_id)] = {
            "resolved_entity_id": entity_id,
            "data_source": data_source,
            "record_id": record_id,
            "match_level": str(match_level),
            "match_key": match_key,
        }

        anchor = anchor_by_entity.get(entity_id) or first_record_by_entity.get(entity_id)
        if not anchor:
            continue
        anchor_ds, anchor_rid = anchor
        if anchor_ds == data_source and anchor_rid == record_id:
            continue

        pair_key = (anchor_ds, anchor_rid, data_source, record_id)
        matched_pairs[pair_key] = {
            "resolved_entity_id": entity_id,
            "anchor_data_source": anchor_ds,
            "anchor_record_id": anchor_rid,
            "matched_data_source": data_source,
            "matched_record_id": record_id,
            "match_level": str(match_level),
            "match_key": match_key,
        }

    return list(matched_records.values()), list(matched_pairs.values())


def try_parse_json(text: str) -> Any:
    """Parse text as JSON when possible, else return None."""
    cleaned = text.strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def extract_reason_summary(output_json: Any, output_text: str | None, max_items: int = 4) -> str:
    """Create a short human-readable reason summary from explain output."""
    candidates: list[str] = []
    seen: set[str] = set()

    def push(value: str) -> None:
        cleaned = " ".join(value.split())
        if not cleaned:
            return
        if len(cleaned) > 240:
            cleaned = cleaned[:237] + "..."
        if cleaned in seen:
            return
        seen.add(cleaned)
        candidates.append(cleaned)

    signal_tokens = ("MATCH", "REASON", "RULE", "FEATURE", "PRINCIPLE", "ATTRIBUTE", "WHY", "EVIDENCE")

    def walk(node: Any, key_hint: str = "") -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                key_text = str(key)
                key_upper = key_text.upper()
                if isinstance(value, (str, int, float, bool)) and any(token in key_upper for token in signal_tokens):
                    push(f"{key_text}={value}")
                walk(value, key_text)
            return
        if isinstance(node, list):
            for item in node:
                walk(item, key_hint)
            return
        if isinstance(node, (str, int, float, bool)):
            hint_upper = key_hint.upper()
            if any(token in hint_upper for token in signal_tokens):
                push(f"{key_hint}={node}")

    if output_json is not None:
        walk(output_json)

    if not candidates and output_text:
        lines = [line.strip() for line in output_text.splitlines() if line.strip()]
        for line in lines[:max_items]:
            push(line)

    if not candidates:
        return ""
    return " | ".join(candidates[:max_items])


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    """Write rows to CSV with a stable schema."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            normalized = {name: row.get(name, "") for name in fieldnames}
            writer.writerow(normalized)


def comb2(value: int) -> int:
    """Return number of unordered pairs from a set size."""
    if value < 2:
        return 0
    return value * (value - 1) // 2


def safe_ratio(numerator: int, denominator: int) -> float | None:
    """Return a safe ratio or None when denominator is zero."""
    if denominator <= 0:
        return None
    return numerator / denominator


def parse_record_key(data_source: Any, record_id: Any) -> tuple[str, str] | None:
    """Normalize record key (DATA_SOURCE, RECORD_ID)."""
    ds = str(data_source or "").strip()
    rid = str(record_id or "").strip()
    if not ds or not rid:
        return None
    return ds, rid


def cleanup_loader_shuffle_files(load_input_jsonl: Path) -> list[str]:
    """Remove temporary shuffled files created by sz_file_loader."""
    removed: list[str] = []
    pattern = f"{load_input_jsonl.name}_sz_shuff_*"
    for file_path in sorted(load_input_jsonl.parent.glob(pattern)):
        if not file_path.is_file():
            continue
        try:
            file_path.unlink()
            removed.append(str(file_path))
        except OSError:
            continue
    return removed


def format_percent(value: float | None) -> str:
    """Render percentage text from a 0..1 ratio."""
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def load_source_ipg_labels(input_jsonl_path: Path) -> dict[str, Any]:
    """Load SOURCE_IPG_ID labels keyed by (DATA_SOURCE, RECORD_ID)."""
    labels: dict[tuple[str, str], str] = {}
    total_rows = 0
    rows_with_record_key = 0
    rows_with_source_ipg_id = 0
    duplicate_conflicts = 0

    with input_jsonl_path.open("r", encoding="utf-8") as infile:
        for line_no, line in enumerate(infile, start=1):
            text = line.strip()
            if not text:
                continue
            total_rows += 1
            obj = json.loads(text)
            if not isinstance(obj, dict):
                raise ValueError(f"Invalid JSON object in input JSONL at line {line_no}")
            key = parse_record_key(obj.get("DATA_SOURCE"), obj.get("RECORD_ID"))
            if key is None:
                continue
            rows_with_record_key += 1
            source_ipg_id = str(obj.get("SOURCE_IPG_ID") or "").strip()
            if not source_ipg_id:
                continue
            rows_with_source_ipg_id += 1
            existing = labels.get(key)
            if existing is not None and existing != source_ipg_id:
                duplicate_conflicts += 1
                continue
            labels[key] = source_ipg_id

    return {
        "labels": labels,
        "total_rows": total_rows,
        "rows_with_record_key": rows_with_record_key,
        "rows_with_source_ipg_id": rows_with_source_ipg_id,
        "duplicate_conflicts": duplicate_conflicts,
    }


def build_ground_truth_match_quality(
    input_jsonl_path: Path,
    entity_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute match quality metrics against SOURCE_IPG_ID ground truth."""
    source_info = load_source_ipg_labels(input_jsonl_path)
    labels: dict[tuple[str, str], str] = source_info["labels"]

    record_to_entity: dict[tuple[str, str], str] = {}
    for row in entity_rows:
        key = parse_record_key(row.get("data_source"), row.get("record_id"))
        entity_id = str(row.get("resolved_entity_id") or "").strip()
        if key is None or not entity_id:
            continue
        record_to_entity[key] = entity_id

    ipg_counts: Counter[str] = Counter()
    entity_ipg_counts: dict[str, Counter[str]] = defaultdict(Counter)
    labeled_records_in_export = 0

    for key, source_ipg_id in labels.items():
        entity_id = record_to_entity.get(key)
        if not entity_id:
            continue
        labeled_records_in_export += 1
        ipg_counts[source_ipg_id] += 1
        entity_ipg_counts[entity_id][source_ipg_id] += 1

    true_pairs = sum(comb2(count) for count in ipg_counts.values())
    predicted_pairs = sum(comb2(sum(counter.values())) for counter in entity_ipg_counts.values())
    true_positive = sum(comb2(count) for counter in entity_ipg_counts.values() for count in counter.values())
    false_positive = max(0, predicted_pairs - true_positive)
    false_negative = max(0, true_pairs - true_positive)

    pair_precision = safe_ratio(true_positive, true_positive + false_positive)
    pair_recall = safe_ratio(true_positive, true_positive + false_negative)
    pair_f1 = None
    if pair_precision is not None and pair_recall is not None and (pair_precision + pair_recall) > 0:
        pair_f1 = 2 * pair_precision * pair_recall / (pair_precision + pair_recall)

    entities_with_labels = len(entity_ipg_counts)
    pure_entities = sum(1 for counter in entity_ipg_counts.values() if len(counter) == 1)
    mixed_entities = entities_with_labels - pure_entities
    entity_purity = safe_ratio(pure_entities, entities_with_labels)

    ipg_to_entities: dict[str, set[str]] = defaultdict(set)
    for entity_id, counter in entity_ipg_counts.items():
        for source_ipg_id in counter.keys():
            ipg_to_entities[source_ipg_id].add(entity_id)

    ipg_groups_size_ge_2 = sum(1 for count in ipg_counts.values() if count >= 2)
    ipg_groups_single_entity = sum(
        1
        for source_ipg_id, count in ipg_counts.items()
        if count >= 2 and len(ipg_to_entities.get(source_ipg_id, set())) == 1
    )
    ipg_groups_split = ipg_groups_size_ge_2 - ipg_groups_single_entity
    ipg_group_concentration = safe_ratio(ipg_groups_single_entity, ipg_groups_size_ge_2)

    mixed_entity_examples: list[dict[str, Any]] = []
    for entity_id, counter in sorted(
        entity_ipg_counts.items(),
        key=lambda item: (-sum(item[1].values()), item[0]),
    ):
        if len(counter) <= 1:
            continue
        mixed_entity_examples.append(
            {
                "resolved_entity_id": entity_id,
                "labeled_records": sum(counter.values()),
                "source_ipg_id_counts": dict(counter),
            }
        )
        if len(mixed_entity_examples) >= 10:
            break

    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_jsonl": str(input_jsonl_path),
        "data_quality": {
            "input_rows_total": source_info["total_rows"],
            "rows_with_record_key": source_info["rows_with_record_key"],
            "rows_with_source_ipg_id": source_info["rows_with_source_ipg_id"],
            "source_ipg_duplicate_conflicts": source_info["duplicate_conflicts"],
            "labeled_records_in_export": labeled_records_in_export,
        },
        "pair_metrics": {
            "pair_precision": pair_precision,
            "pair_recall": pair_recall,
            "pair_f1": pair_f1,
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "predicted_pairs_labeled": predicted_pairs,
            "ground_truth_pairs_labeled": true_pairs,
        },
        "entity_metrics": {
            "entities_with_labeled_records": entities_with_labels,
            "pure_entities": pure_entities,
            "mixed_entities": mixed_entities,
            "entity_purity": entity_purity,
        },
        "group_metrics": {
            "ipg_groups_size_ge_2": ipg_groups_size_ge_2,
            "ipg_groups_single_entity": ipg_groups_single_entity,
            "ipg_groups_split": ipg_groups_split,
            "ipg_group_concentration": ipg_group_concentration,
        },
        "mixed_entity_examples": mixed_entity_examples,
    }


def write_ground_truth_match_quality_reports(
    comparison_dir: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path]:
    """Write management-facing ground truth quality reports."""
    quality_json = comparison_dir / "ground_truth_match_quality.json"
    quality_md = comparison_dir / "ground_truth_match_quality.md"

    quality_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pair_metrics = payload.get("pair_metrics", {})
    entity_metrics = payload.get("entity_metrics", {})
    group_metrics = payload.get("group_metrics", {})
    data_quality = payload.get("data_quality", {})

    lines: list[str] = []
    lines.append("# Match Quality vs SOURCE_IPG_ID")
    lines.append("")
    lines.append(f"- Generated at: {payload.get('generated_at')}")
    lines.append(f"- Input JSONL: {payload.get('input_jsonl')}")
    lines.append("")
    lines.append("## Pair Quality")
    lines.append("")
    lines.append(f"- Pair precision: {format_percent(pair_metrics.get('pair_precision'))}")
    lines.append(f"- Pair recall: {format_percent(pair_metrics.get('pair_recall'))}")
    lines.append(f"- Pair F1: {format_percent(pair_metrics.get('pair_f1'))}")
    lines.append(f"- True positive: {pair_metrics.get('true_positive', 0)}")
    lines.append(f"- False positive: {pair_metrics.get('false_positive', 0)}")
    lines.append(f"- False negative: {pair_metrics.get('false_negative', 0)}")
    lines.append("")
    lines.append("## Extra Metrics")
    lines.append("")
    lines.append(f"- Predicted pairs (labeled): {pair_metrics.get('predicted_pairs_labeled', 0)}")
    lines.append(f"- Ground-truth pairs (labeled): {pair_metrics.get('ground_truth_pairs_labeled', 0)}")
    lines.append(f"- Labeled records in export: {data_quality.get('labeled_records_in_export', 0)}")
    lines.append(f"- Rows with SOURCE_IPG_ID in input: {data_quality.get('rows_with_source_ipg_id', 0)}")
    lines.append(f"- Entity purity (labeled): {format_percent(entity_metrics.get('entity_purity'))}")
    lines.append(f"- Pure entities (labeled): {entity_metrics.get('pure_entities', 0)}")
    lines.append(f"- Mixed entities (labeled): {entity_metrics.get('mixed_entities', 0)}")
    lines.append(
        "- IPG group concentration (size>=2): "
        f"{format_percent(group_metrics.get('ipg_group_concentration'))}"
    )
    lines.append(
        f"- Split IPG groups (size>=2): {group_metrics.get('ipg_groups_split', 0)}"
        f"/{group_metrics.get('ipg_groups_size_ge_2', 0)}"
    )

    mixed_examples = payload.get("mixed_entity_examples", [])
    if mixed_examples:
        lines.append("")
        lines.append("## Mixed Entity Examples")
        lines.append("")
        lines.append("| Entity | Labeled Records | SOURCE_IPG_ID Counts |")
        lines.append("| --- | ---: | --- |")
        for item in mixed_examples:
            lines.append(
                f"| {item.get('resolved_entity_id')} | {item.get('labeled_records', 0)} | "
                f"{json.dumps(item.get('source_ipg_id_counts', {}), ensure_ascii=False)} |"
            )

    quality_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return quality_json, quality_md


def resolve_generation_summary_for_input(
    repo_root: Path,
    input_jsonl_path: Path,
) -> dict[str, str | None]:
    """Resolve generation summary metadata matching the run input JSONL."""
    output_dir = repo_root / "output"
    if not output_dir.exists():
        return {
            "generation_summary_json": None,
            "base_input_json": None,
            "mapped_output_jsonl": None,
        }

    input_path_text = str(input_jsonl_path)
    input_name = input_jsonl_path.name

    for summary_path in sorted(output_dir.glob("generation_summary_*.json"), reverse=True):
        try:
            payload = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        mapped_output = str(payload.get("mapped_output_jsonl") or "").strip()
        if not mapped_output:
            continue
        mapped_name = Path(mapped_output).name
        if mapped_output == input_path_text or mapped_name == input_name:
            return {
                "generation_summary_json": str(summary_path.resolve()),
                "base_input_json": str(payload.get("base_input_json") or "") or None,
                "mapped_output_jsonl": mapped_output or None,
            }

    return {
        "generation_summary_json": None,
        "base_input_json": None,
        "mapped_output_jsonl": None,
    }


def append_run_registry_entry(
    repo_root: Path,
    summary: dict[str, Any],
    load_input_jsonl: Path,
) -> Path | None:
    """Append one execution row to output/run_registry.csv."""
    registry_dir = repo_root / "output"
    if not registry_dir.exists():
        return None

    registry_path = registry_dir / "run_registry.csv"
    artifacts = summary.get("artifacts", {}) if isinstance(summary.get("artifacts"), dict) else {}
    generation_meta = {
        "generation_summary_json": None,
        "base_input_json": None,
        "mapped_output_jsonl": None,
    }
    candidate_inputs: list[Path] = []
    input_file_text = str(summary.get("input_file") or "").strip()
    if input_file_text:
        candidate_inputs.append(Path(input_file_text))
    candidate_inputs.append(load_input_jsonl)
    for candidate in candidate_inputs:
        try:
            current_meta = resolve_generation_summary_for_input(repo_root, candidate)
        except Exception:  # pylint: disable=broad-exception-caught
            continue
        if current_meta.get("generation_summary_json"):
            generation_meta = current_meta
            break
    run_dir = str(summary.get("run_directory") or "")

    row = {
        "generated_at": str(summary.get("generated_at") or ""),
        "run_directory": run_dir,
        "run_name": Path(run_dir).name if run_dir else "",
        "overall_ok": str(summary.get("overall_ok") or False),
        "records_input": str(summary.get("records_input") or ""),
        "data_sources": ",".join(summary.get("data_sources", [])),
        "input_file": str(summary.get("input_file") or ""),
        "load_input_jsonl": str(artifacts.get("load_input_jsonl") or ""),
        "project_dir": str(summary.get("project_dir") or ""),
        "fast_mode": str((summary.get("runtime_options") or {}).get("fast_mode") if isinstance(summary.get("runtime_options"), dict) else ""),
        "comparison_dir": str(artifacts.get("comparison_dir") or ""),
        "management_summary_md": str(artifacts.get("management_summary_md") or ""),
        "ground_truth_match_quality_md": str(artifacts.get("ground_truth_match_quality_md") or ""),
        "ground_truth_match_quality_json": str(artifacts.get("ground_truth_match_quality_json") or ""),
        "generation_summary_json": str(generation_meta.get("generation_summary_json") or ""),
        "base_input_json": str(generation_meta.get("base_input_json") or ""),
        "mapped_output_jsonl": str(generation_meta.get("mapped_output_jsonl") or ""),
    }

    fieldnames = [
        "generated_at",
        "run_directory",
        "run_name",
        "overall_ok",
        "records_input",
        "data_sources",
        "input_file",
        "load_input_jsonl",
        "project_dir",
        "fast_mode",
        "comparison_dir",
        "management_summary_md",
        "ground_truth_match_quality_md",
        "ground_truth_match_quality_json",
        "generation_summary_json",
        "base_input_json",
        "mapped_output_jsonl",
    ]

    write_header = not registry_path.exists() or registry_path.stat().st_size == 0
    with registry_path.open("a", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return registry_path


def make_comparison_outputs(
    run_dir: Path,
    input_jsonl_path: Path,
    export_rows: list[dict[str, str]],
    matched_records: list[dict[str, str]],
    matched_pairs: list[dict[str, str]],
    why_entity_results: list[dict[str, Any]],
    why_records_results: list[dict[str, Any]],
    records_input_count: int,
) -> dict[str, Any]:
    """Create comparison-ready artifacts for downstream testing and management."""
    comparison_dir = run_dir / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)

    entity_records_csv = comparison_dir / "entity_records.csv"
    matched_pairs_csv = comparison_dir / "matched_pairs.csv"
    match_stats_csv = comparison_dir / "match_key_stats.csv"
    management_json = comparison_dir / "management_summary.json"
    management_md = comparison_dir / "management_summary.md"

    why_entity_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for item in why_entity_results:
        rec = item.get("input", {})
        key = (str(rec.get("data_source", "")), str(rec.get("record_id", "")))
        why_entity_by_key[key] = item

    why_records_by_key: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for item in why_records_results:
        rec = item.get("input", {})
        key = (
            str(rec.get("anchor_data_source", "")),
            str(rec.get("anchor_record_id", "")),
            str(rec.get("matched_data_source", "")),
            str(rec.get("matched_record_id", "")),
        )
        why_records_by_key[key] = item

    entity_rows: list[dict[str, Any]] = []
    entity_ids: set[str] = set()
    for row in export_rows:
        resolved_entity_id = row.get("RESOLVED_ENTITY_ID", "")
        data_source = row.get("DATA_SOURCE", "")
        record_id = row.get("RECORD_ID", "")
        match_level = parse_int(row.get("MATCH_LEVEL", "0"), fallback=0)
        match_key = row.get("MATCH_KEY", "")
        if resolved_entity_id:
            entity_ids.add(resolved_entity_id)

        why_info = why_entity_by_key.get((data_source, record_id), {})
        reason = extract_reason_summary(
            why_info.get("output_json"),
            why_info.get("output_text"),
        )
        entity_rows.append(
            {
                "resolved_entity_id": resolved_entity_id,
                "data_source": data_source,
                "record_id": record_id,
                "match_level": match_level,
                "match_key": match_key,
                "is_anchor": 1 if match_level == 0 else 0,
                "why_entity_ok": 1 if why_info.get("ok") else 0,
                "why_entity_reason_summary": reason,
            }
        )

    pair_rows: list[dict[str, Any]] = []
    for pair in matched_pairs:
        key = (
            pair["anchor_data_source"],
            pair["anchor_record_id"],
            pair["matched_data_source"],
            pair["matched_record_id"],
        )
        why_info = why_records_by_key.get(key, {})
        reason = extract_reason_summary(
            why_info.get("output_json"),
            why_info.get("output_text"),
        )
        pair_rows.append(
            {
                "resolved_entity_id": pair["resolved_entity_id"],
                "anchor_data_source": pair["anchor_data_source"],
                "anchor_record_id": pair["anchor_record_id"],
                "matched_data_source": pair["matched_data_source"],
                "matched_record_id": pair["matched_record_id"],
                "match_level": parse_int(pair.get("match_level", "0"), fallback=0),
                "match_key": pair.get("match_key", ""),
                "why_records_ok": 1 if why_info.get("ok") else 0,
                "why_records_reason_summary": reason,
            }
        )

    match_key_counts = Counter([p.get("match_key", "") for p in matched_pairs if p.get("match_key", "")])
    match_level_counts = Counter([parse_int(p.get("match_level", "0"), fallback=0) for p in matched_pairs])

    stats_rows = [
        {"metric": "records_input", "value": records_input_count},
        {"metric": "records_exported", "value": len(export_rows)},
        {"metric": "resolved_entities", "value": len(entity_ids)},
        {"metric": "matched_records", "value": len(matched_records)},
        {"metric": "matched_pairs", "value": len(matched_pairs)},
    ]
    for level, count in sorted(match_level_counts.items()):
        stats_rows.append({"metric": f"match_level_{level}", "value": count})
    for key, count in sorted(match_key_counts.items(), key=lambda x: (-x[1], x[0])):
        stats_rows.append({"metric": f"match_key::{key}", "value": count})

    write_csv(
        entity_records_csv,
        [
            "resolved_entity_id",
            "data_source",
            "record_id",
            "match_level",
            "match_key",
            "is_anchor",
            "why_entity_ok",
            "why_entity_reason_summary",
        ],
        entity_rows,
    )
    write_csv(
        matched_pairs_csv,
        [
            "resolved_entity_id",
            "anchor_data_source",
            "anchor_record_id",
            "matched_data_source",
            "matched_record_id",
            "match_level",
            "match_key",
            "why_records_ok",
            "why_records_reason_summary",
        ],
        pair_rows,
    )
    write_csv(match_stats_csv, ["metric", "value"], stats_rows)

    ground_truth_payload = build_ground_truth_match_quality(
        input_jsonl_path=input_jsonl_path,
        entity_rows=entity_rows,
    )
    ground_truth_json, ground_truth_md = write_ground_truth_match_quality_reports(
        comparison_dir=comparison_dir,
        payload=ground_truth_payload,
    )

    summary_obj = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "records_input": records_input_count,
        "records_exported": len(export_rows),
        "resolved_entities": len(entity_ids),
        "matched_records": len(matched_records),
        "matched_pairs": len(matched_pairs),
        "match_level_distribution": {str(k): v for k, v in sorted(match_level_counts.items())},
        "match_key_distribution": dict(sorted(match_key_counts.items(), key=lambda x: (-x[1], x[0]))),
        "explain_coverage": {
            "why_entity_total": len(why_entity_results),
            "why_entity_ok": sum(1 for item in why_entity_results if item.get("ok")),
            "why_records_total": len(why_records_results),
            "why_records_ok": sum(1 for item in why_records_results if item.get("ok")),
        },
        "artifacts": {
            "entity_records_csv": str(entity_records_csv),
            "matched_pairs_csv": str(matched_pairs_csv),
            "match_stats_csv": str(match_stats_csv),
            "management_summary_md": str(management_md),
            "ground_truth_match_quality_json": str(ground_truth_json),
            "ground_truth_match_quality_md": str(ground_truth_md),
        },
        "ground_truth_match_quality": ground_truth_payload,
    }
    management_json.write_text(json.dumps(summary_obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# Senzing Matching Summary")
    lines.append("")
    lines.append(f"- Generated at: {summary_obj['generated_at']}")
    lines.append(f"- Records input: {records_input_count}")
    lines.append(f"- Records exported: {len(export_rows)}")
    lines.append(f"- Resolved entities: {len(entity_ids)}")
    lines.append(f"- Matched records: {len(matched_records)}")
    lines.append(f"- Matched pairs: {len(matched_pairs)}")
    lines.append(
        "- Explain coverage: "
        f"whyEntity {summary_obj['explain_coverage']['why_entity_ok']}/{summary_obj['explain_coverage']['why_entity_total']}, "
        f"whyRecords {summary_obj['explain_coverage']['why_records_ok']}/{summary_obj['explain_coverage']['why_records_total']}"
    )
    lines.append("")
    lines.append("## Top Match Keys")
    lines.append("")
    lines.append("| Match Key | Count |")
    lines.append("| --- | ---: |")
    if match_key_counts:
        for key, count in sorted(match_key_counts.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"| {key} | {count} |")
    else:
        lines.append("| (none) | 0 |")

    lines.append("")
    lines.append("## Match Level Distribution")
    lines.append("")
    lines.append("| Match Level | Count |")
    lines.append("| --- | ---: |")
    if match_level_counts:
        for level, count in sorted(match_level_counts.items()):
            lines.append(f"| {level} | {count} |")
    else:
        lines.append("| 0 | 0 |")

    lines.append("")
    lines.append("## First 20 Matched Pairs")
    lines.append("")
    lines.append("| Entity | Anchor | Matched | Match Key | Level | Explain |")
    lines.append("| --- | --- | --- | --- | ---: | --- |")
    for row in pair_rows[:20]:
        anchor = f"{row['anchor_data_source']}:{row['anchor_record_id']}"
        matched = f"{row['matched_data_source']}:{row['matched_record_id']}"
        explain_text = str(row["why_records_reason_summary"] or "").replace("\n", " ")
        lines.append(
            f"| {row['resolved_entity_id']} | {anchor} | {matched} | "
            f"{row['match_key']} | {row['match_level']} | {explain_text} |"
        )
    if not pair_rows:
        lines.append("| - | - | - | - | - | No matched pairs detected |")

    management_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "comparison_dir": str(comparison_dir),
        "entity_records_csv": str(entity_records_csv),
        "matched_pairs_csv": str(matched_pairs_csv),
        "match_stats_csv": str(match_stats_csv),
        "management_summary_json": str(management_json),
        "management_summary_md": str(management_md),
        "ground_truth_match_quality_json": str(ground_truth_json),
        "ground_truth_match_quality_md": str(ground_truth_md),
        "matched_pairs_count": len(matched_pairs),
    }


def main() -> int:
    """Entry point."""
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    if args.fast_mode:
        args.skip_snapshot = True
        args.skip_export = True
        args.skip_explain = True
        args.skip_comparison = True
        args.disable_stability_retries = True
        if args.load_threads == 4:
            cpu_guess = os.cpu_count() or 4
            args.load_threads = max(4, min(12, cpu_guess))

    if args.step_timeout_seconds <= 0:
        print("ERROR: --step-timeout-seconds must be > 0", file=sys.stderr)
        return 2
    if args.max_explain_records < 0 or args.max_explain_pairs < 0:
        print("ERROR: --max-explain-records and --max-explain-pairs must be >= 0", file=sys.stderr)
        return 2
    if args.load_threads <= 0 or args.load_fallback_threads <= 0:
        print("ERROR: --load-threads and --load-fallback-threads must be > 0", file=sys.stderr)
        return 2
    if args.snapshot_threads <= 0 or args.snapshot_fallback_threads <= 0:
        print("ERROR: --snapshot-threads and --snapshot-fallback-threads must be > 0", file=sys.stderr)
        return 2

    input_path = Path(args.input_file).expanduser().resolve()
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    data_sources_override = parse_csv_items(args.data_sources)
    if (
        args.fast_mode
        and input_path.suffix.lower() == ".jsonl"
        and data_sources_override
        and not args.use_input_jsonl_directly
    ):
        args.use_input_jsonl_directly = True
    if args.use_input_jsonl_directly:
        if input_path.suffix.lower() != ".jsonl":
            print("ERROR: --use-input-jsonl-directly requires .jsonl input", file=sys.stderr)
            return 2
        if not data_sources_override:
            print("ERROR: --use-input-jsonl-directly requires --data-sources", file=sys.stderr)
            return 2

    base_setup_env = Path(args.senzing_env).expanduser().resolve() if args.senzing_env else None
    if base_setup_env and not base_setup_env.exists():
        print(f"ERROR: --senzing-env not found: {base_setup_env}", file=sys.stderr)
        return 2

    run_dir = Path(args.output_root).expanduser().resolve() / f"{args.run_name_prefix}_{now_timestamp()}"
    logs_dir = run_dir / "logs"
    run_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    project_dir = Path(args.project_parent_dir).expanduser() / f"{args.project_name_prefix}_{now_timestamp()}"
    project_setup_env = project_dir / "setupEnv"

    normalized_jsonl = run_dir / "input_normalized.jsonl"
    config_scripts_dir = run_dir / "config_scripts"
    snapshot_prefix = run_dir / "snapshot"
    snapshot_json = run_dir / "snapshot.json"
    export_file = run_dir / args.export_output_name
    explain_dir = run_dir / "explain"
    explain_logs_dir = explain_dir / "logs"
    match_inputs_file = explain_dir / "match_inputs.json"
    why_entity_file = explain_dir / "why_entity_by_record.jsonl"
    why_records_file = explain_dir / "why_records_pairs.jsonl"
    summary_file = run_dir / "run_summary.json"
    comparison_artifacts: dict[str, str | int | dict[str, int] | None] = {}
    loader_temp_files_removed: list[str] = []
    run_registry_path: Path | None = None

    print(f"Run directory: {run_dir}")
    print(f"Input file: {input_path}")
    print(f"Project dir: {project_dir}")
    if args.fast_mode:
        print("Fast mode: enabled")

    try:
        records_input_count, data_sources, load_input_jsonl = normalize_input_to_jsonl(
            input_path=input_path,
            normalized_jsonl_path=normalized_jsonl,
            provided_data_sources=data_sources_override,
            use_input_jsonl_directly=args.use_input_jsonl_directly,
        )
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Unable to normalize input: {err}", file=sys.stderr)
        return 2
    print(f"Load input JSONL: {load_input_jsonl}")
    print(f"Records detected: {records_input_count}")
    print(f"Data sources: {', '.join(data_sources)}")

    config_scripts_dir.mkdir(parents=True, exist_ok=True)
    steps: list[dict[str, Any]] = []
    runtime_warnings: list[str] = []

    step = create_project(project_dir, base_setup_env, logs_dir / "00_create_project.log")
    steps.append(step)
    if not step["ok"] or not project_setup_env.exists():
        summary = {
            "overall_ok": False,
            "error": "create_project failed",
            "run_directory": str(run_dir),
            "project_dir": str(project_dir),
            "runtime_warnings": runtime_warnings,
            "steps": steps,
        }
        summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("FAILED at create_project", file=sys.stderr)
        return 1

    for index, data_source in enumerate(data_sources, start=1):
        cfg_file = config_scripts_dir / f"add_{data_source}.g2c"
        cfg_file.write_text(f"addDataSource {data_source}\nsave\n", encoding="utf-8")
        command = (
            f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1 && "
            f"sz_configtool -f {shlex.quote(str(cfg_file))}"
        )
        step = run_shell_step(
            f"configure_data_source_{data_source}",
            command,
            logs_dir / f"01_configure_{index:02d}_{data_source}.log",
            timeout_seconds=args.step_timeout_seconds,
        )
        steps.append(step)
        if not step["ok"]:
            stdout = (step.get("stdout_tail") or "").lower()
            stderr = (step.get("stderr_tail") or "").lower()
            already_exists = "already" in stdout or "already" in stderr or "exist" in stdout or "exist" in stderr
            if not already_exists:
                summary = {
                    "overall_ok": False,
                    "error": f"configure_data_source failed for {data_source}",
                    "run_directory": str(run_dir),
                    "project_dir": str(project_dir),
                    "runtime_warnings": runtime_warnings,
                    "steps": steps,
                }
                summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"FAILED at configure_data_source_{data_source}", file=sys.stderr)
                return 1

    load_attempts: list[tuple[str, str, Path]] = [
        (
            "primary",
            build_load_command(project_setup_env, load_input_jsonl, args.load_threads, no_shuffle=False),
            logs_dir / "02_load.log",
        )
    ]
    if not args.disable_stability_retries:
        load_attempts.append(
            (
                "fallback_single_thread",
                build_load_command(
                    project_setup_env,
                    load_input_jsonl,
                    args.load_fallback_threads,
                    no_shuffle=True,
                ),
                logs_dir / "02_load_retry_1.log",
            )
        )

    load_ok = False
    for attempt_index, (attempt_mode, load_cmd, load_log_path) in enumerate(load_attempts):
        step_name = "load_records" if attempt_index == 0 else f"load_records_retry_{attempt_index}"
        step = run_shell_step(
            step_name,
            load_cmd,
            load_log_path,
            timeout_seconds=args.step_timeout_seconds,
        )
        step["attempt_mode"] = attempt_mode
        steps.append(step)
        if step["ok"]:
            if attempt_index > 0:
                runtime_warnings.append(
                    f"load_records primary attempt failed; fallback '{attempt_mode}' succeeded."
                )
            load_ok = True
            break

    if not load_ok:
        summary = {
            "overall_ok": False,
            "error": "load_records failed after retries",
            "run_directory": str(run_dir),
            "project_dir": str(project_dir),
            "runtime_warnings": runtime_warnings,
            "steps": steps,
        }
        summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("FAILED at load_records", file=sys.stderr)
        return 1

    if not args.keep_loader_temp_files:
        loader_temp_files_removed = cleanup_loader_shuffle_files(load_input_jsonl)
        if loader_temp_files_removed:
            runtime_warnings.append(
                f"Removed {len(loader_temp_files_removed)} loader temp file(s)."
            )

    if not args.skip_snapshot:
        snapshot_attempts: list[tuple[str, str, Path]] = [
            (
                "primary",
                build_snapshot_command(project_setup_env, snapshot_prefix, args.snapshot_threads, force_sdk=False),
                logs_dir / "03_snapshot.log",
            )
        ]
        if not args.disable_stability_retries:
            snapshot_attempts.append(
                (
                    "fallback_single_thread_force_sdk",
                    build_snapshot_command(
                        project_setup_env,
                        snapshot_prefix,
                        args.snapshot_fallback_threads,
                        force_sdk=True,
                    ),
                    logs_dir / "03_snapshot_retry_1.log",
                )
            )

        snapshot_ok = False
        for attempt_index, (attempt_mode, snapshot_cmd, snapshot_log_path) in enumerate(snapshot_attempts):
            step_name = "snapshot" if attempt_index == 0 else f"snapshot_retry_{attempt_index}"
            step = run_shell_step(
                step_name,
                snapshot_cmd,
                snapshot_log_path,
                timeout_seconds=args.step_timeout_seconds,
            )
            step["attempt_mode"] = attempt_mode
            steps.append(step)
            if step["ok"]:
                if attempt_index > 0:
                    runtime_warnings.append(
                        f"snapshot primary attempt failed; fallback '{attempt_mode}' succeeded."
                    )
                snapshot_ok = True
                break

        if not snapshot_ok:
            summary = {
                "overall_ok": False,
                "error": "snapshot failed after retries",
                "run_directory": str(run_dir),
                "project_dir": str(project_dir),
                "runtime_warnings": runtime_warnings,
                "steps": steps,
            }
            summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("FAILED at snapshot", file=sys.stderr)
            return 1

        candidates = sorted(run_dir.glob("snapshot*.json"))
        if candidates:
            candidates[0].replace(snapshot_json)

    if not args.skip_export:
        export_cmd = (
            f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1 && "
            f"sz_export -o {shlex.quote(str(export_file))}"
        )
        step = run_shell_step(
            "export",
            export_cmd,
            logs_dir / "04_export.log",
            timeout_seconds=args.step_timeout_seconds,
        )
        steps.append(step)
        if not step["ok"]:
            summary = {
                "overall_ok": False,
                "error": "export failed",
                "run_directory": str(run_dir),
                "project_dir": str(project_dir),
                "runtime_warnings": runtime_warnings,
                "steps": steps,
            }
            summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("FAILED at export", file=sys.stderr)
            return 1

    need_export_rows = export_file.exists() and (not args.skip_explain or not args.skip_comparison)
    export_rows: list[dict[str, str]] = parse_export_rows(export_file) if need_export_rows else []
    matched_records: list[dict[str, str]] = []
    matched_pairs: list[dict[str, str]] = []
    if export_rows:
        matched_records, matched_pairs = build_match_inputs(export_rows)

    why_entity_results: list[dict[str, Any]] = []
    why_records_results: list[dict[str, Any]] = []

    explain_summary: dict[str, Any] = {
        "enabled": not args.skip_explain,
        "status": "skipped" if args.skip_explain else "not_started",
        "matched_records_detected": len(matched_records),
        "matched_pairs_detected": len(matched_pairs),
        "why_entity_attempted": 0,
        "why_entity_ok": 0,
        "why_records_attempted": 0,
        "why_records_ok": 0,
        "warnings": [],
    }

    if not args.skip_explain:
        if args.skip_export or not export_file.exists():
            explain_summary["status"] = "skipped_no_export"
            explain_summary["warnings"].append(
                "Explain skipped because export file is missing (export skipped or failed)."
            )
        else:
            explain_dir.mkdir(parents=True, exist_ok=True)
            explain_logs_dir.mkdir(parents=True, exist_ok=True)

            match_inputs_file.write_text(
                json.dumps(
                    {
                        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                        "matched_records_detected": len(matched_records),
                        "matched_pairs_detected": len(matched_pairs),
                        "matched_records": matched_records,
                        "matched_pairs": matched_pairs,
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            explain_summary["status"] = "done"
            if args.max_explain_records > 0 and len(matched_records) > args.max_explain_records:
                explain_summary["warnings"].append(
                    f"Matched records limited from {len(matched_records)} to {args.max_explain_records}."
                )
                matched_records = matched_records[: args.max_explain_records]
            if args.max_explain_pairs > 0 and len(matched_pairs) > args.max_explain_pairs:
                explain_summary["warnings"].append(
                    f"Matched pairs limited from {len(matched_pairs)} to {args.max_explain_pairs}."
                )
                matched_pairs = matched_pairs[: args.max_explain_pairs]

            g2, engine_cleanup_target, engine_details = init_g2_engine(project_dir, project_setup_env)
            explain_summary["engine_mode"] = "python_sdk"
            explain_summary["engine_init_ok"] = bool(g2)
            explain_summary["engine_config_source"] = engine_details.get("config_source")
            explain_summary["engine_sdk_api"] = engine_details.get("sdk_api")
            if not g2:
                explain_summary["status"] = "skipped_sdk_init_failed"
                explain_summary["warnings"].append(
                    str(engine_details.get("error") or "Unable to initialize SDK engine for explain phase.")
                )
            else:
                try:
                    with why_entity_file.open("w", encoding="utf-8") as outfile:
                        for index, rec in enumerate(matched_records, start=1):
                            ds = rec["data_source"]
                            rid = rec["record_id"]
                            started = time.time()
                            sdk_result = run_sdk_why_entity(g2, ds, rid)
                            duration = round(time.time() - started, 3)
                            log_path = explain_logs_dir / f"why_entity_{index:04d}.log"
                            write_sdk_log(
                                log_path=log_path,
                                step_name=f"why_entity_by_record_{index:04d}",
                                input_payload=rec,
                                sdk_result=sdk_result,
                                duration_seconds=duration,
                            )

                            explain_summary["why_entity_attempted"] += 1
                            if sdk_result.get("ok"):
                                explain_summary["why_entity_ok"] += 1

                            item = {
                                "index": index,
                                "input": rec,
                                "ok": bool(sdk_result.get("ok")),
                                "command_used": f"sdk:{sdk_result.get('method')}" if sdk_result.get("method") else "sdk:unavailable",
                                "log_file": str(log_path),
                                "output_json": sdk_result.get("output_json"),
                                "output_text": None if sdk_result.get("output_json") is not None else str(sdk_result.get("output_text", "")).strip(),
                                "stderr": sdk_result.get("error"),
                            }
                            why_entity_results.append(item)
                            outfile.write(json.dumps(item, ensure_ascii=False) + "\n")

                            steps.append(
                                {
                                    "step": f"why_entity_by_record_{index:04d}",
                                    "ok": item["ok"],
                                    "exit_code": 0 if item["ok"] else 1,
                                    "duration_seconds": duration,
                                    "command_used": item["command_used"],
                                    "log_file": str(log_path),
                                    "stdout_tail": str(item.get("output_text") or "")[-1200:],
                                    "stderr_tail": str(item.get("stderr") or "")[-1200:],
                                }
                            )

                    with why_records_file.open("w", encoding="utf-8") as outfile:
                        for index, pair in enumerate(matched_pairs, start=1):
                            ds1 = pair["anchor_data_source"]
                            rid1 = pair["anchor_record_id"]
                            ds2 = pair["matched_data_source"]
                            rid2 = pair["matched_record_id"]
                            started = time.time()
                            sdk_result = run_sdk_why_records(g2, ds1, rid1, ds2, rid2)
                            duration = round(time.time() - started, 3)
                            log_path = explain_logs_dir / f"why_records_{index:04d}.log"
                            write_sdk_log(
                                log_path=log_path,
                                step_name=f"why_records_{index:04d}",
                                input_payload=pair,
                                sdk_result=sdk_result,
                                duration_seconds=duration,
                            )

                            explain_summary["why_records_attempted"] += 1
                            if sdk_result.get("ok"):
                                explain_summary["why_records_ok"] += 1

                            item = {
                                "index": index,
                                "input": pair,
                                "ok": bool(sdk_result.get("ok")),
                                "command_used": f"sdk:{sdk_result.get('method')}" if sdk_result.get("method") else "sdk:unavailable",
                                "log_file": str(log_path),
                                "output_json": sdk_result.get("output_json"),
                                "output_text": None if sdk_result.get("output_json") is not None else str(sdk_result.get("output_text", "")).strip(),
                                "stderr": sdk_result.get("error"),
                            }
                            why_records_results.append(item)
                            outfile.write(json.dumps(item, ensure_ascii=False) + "\n")

                            steps.append(
                                {
                                    "step": f"why_records_{index:04d}",
                                    "ok": item["ok"],
                                    "exit_code": 0 if item["ok"] else 1,
                                    "duration_seconds": duration,
                                    "command_used": item["command_used"],
                                    "log_file": str(log_path),
                                    "stdout_tail": str(item.get("output_text") or "")[-1200:],
                                    "stderr_tail": str(item.get("stderr") or "")[-1200:],
                                }
                            )
                finally:
                    try:
                        if engine_cleanup_target is not None and hasattr(engine_cleanup_target, "destroy"):
                            engine_cleanup_target.destroy()
                    except Exception:
                        pass

                if explain_summary["why_entity_attempted"] > 0 and explain_summary["why_entity_ok"] == 0:
                    explain_summary["warnings"].append(
                        "No why-entity call succeeded in SDK mode."
                    )
                if explain_summary["why_records_attempted"] > 0 and explain_summary["why_records_ok"] == 0:
                    explain_summary["warnings"].append(
                        "No why-records call succeeded in SDK mode."
                    )

    if export_rows and not args.skip_comparison:
        comparison_artifacts = make_comparison_outputs(
            run_dir=run_dir,
            input_jsonl_path=load_input_jsonl,
            export_rows=export_rows,
            matched_records=matched_records,
            matched_pairs=matched_pairs,
            why_entity_results=why_entity_results,
            why_records_results=why_records_results,
            records_input_count=records_input_count,
        )

    summary = {
        "overall_ok": True,
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_file": str(input_path),
        "project_dir": str(project_dir),
        "project_setup_env": str(project_setup_env),
        "run_directory": str(run_dir),
        "records_input": records_input_count,
        "data_sources": data_sources,
        "runtime_options": {
            "step_timeout_seconds": args.step_timeout_seconds,
            "load_threads": args.load_threads,
            "load_fallback_threads": args.load_fallback_threads,
            "snapshot_threads": args.snapshot_threads,
            "snapshot_fallback_threads": args.snapshot_fallback_threads,
            "fast_mode": args.fast_mode,
            "skip_comparison": args.skip_comparison,
            "use_input_jsonl_directly": args.use_input_jsonl_directly,
            "data_sources_override": data_sources_override,
            "keep_loader_temp_files": args.keep_loader_temp_files,
            "stability_retries_enabled": not args.disable_stability_retries,
        },
        "runtime_warnings": runtime_warnings,
        "artifacts": {
            "normalized_jsonl": str(normalized_jsonl) if normalized_jsonl.exists() else None,
            "load_input_jsonl": str(load_input_jsonl),
            "loader_temp_files_removed": loader_temp_files_removed,
            "config_scripts_dir": str(config_scripts_dir),
            "snapshot_json": str(snapshot_json) if snapshot_json.exists() else None,
            "export_file": str(export_file) if export_file.exists() else None,
            "explain_dir": str(explain_dir) if explain_dir.exists() else None,
            "match_inputs_file": str(match_inputs_file) if match_inputs_file.exists() else None,
            "why_entity_file": str(why_entity_file) if why_entity_file.exists() else None,
            "why_records_file": str(why_records_file) if why_records_file.exists() else None,
            "comparison_dir": comparison_artifacts.get("comparison_dir"),
            "entity_records_csv": comparison_artifacts.get("entity_records_csv"),
            "matched_pairs_csv": comparison_artifacts.get("matched_pairs_csv"),
            "match_stats_csv": comparison_artifacts.get("match_stats_csv"),
            "management_summary_json": comparison_artifacts.get("management_summary_json"),
            "management_summary_md": comparison_artifacts.get("management_summary_md"),
            "ground_truth_match_quality_json": comparison_artifacts.get("ground_truth_match_quality_json"),
            "ground_truth_match_quality_md": comparison_artifacts.get("ground_truth_match_quality_md"),
            "logs_dir": str(logs_dir),
        },
        "explain": explain_summary,
        "comparison": comparison_artifacts,
        "steps": steps,
    }
    try:
        run_registry_path = append_run_registry_entry(
            repo_root=repo_root,
            summary=summary,
            load_input_jsonl=load_input_jsonl,
        )
    except Exception as err:  # pylint: disable=broad-exception-caught
        runtime_warnings.append(f"Unable to append run registry entry: {err}")
        run_registry_path = None

    summary["artifacts"]["run_registry_csv"] = str(run_registry_path) if run_registry_path else None

    summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Pipeline complete. Success=True")
    print(f"Summary: {summary_file}")
    if run_registry_path:
        print(f"Run registry: {run_registry_path}")
    print(f"Project: {project_dir}")
    print(f"Artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

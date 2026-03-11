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
import itertools
import json
import os
import shutil
import shlex
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

LICENSE_STRING_ENV = "SENZING_LICENSE_STRING_BASE64"
MODERN_SCHEMA_SQL_PATH = Path("/opt/senzing/er/resources/schema/szcore-schema-sqlite-create.sql")
MODERN_TEMPLATE_CONFIG_PATH = Path("/opt/senzing/er/resources/templates/g2config.json")
MODERN_LIB_DIR = Path("/opt/senzing/g2/lib")
MODERN_RESOURCE_DIR = Path("/opt/senzing/g2/resources")
MODERN_DATA_DIR = Path("/opt/senzing/data")
MODERN_ETC_DIR = Path("/etc/opt/senzing")


def now_timestamp() -> str:
    """Return timestamp suitable for directory naming."""
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def detect_repo_root(script_path: Path) -> Path:
    """Resolve repository root for both legacy and current core layouts."""
    resolved = script_path.resolve()
    # Legacy layout: <root>/senzing/all_in_one/run_senzing_end_to_end.py
    # Current layout: <root>/S3Z/all_in_one/run_senzing_end_to_end.py
    if resolved.parent.name == "all_in_one" and resolved.parent.parent.name in {"senzing", "S3Z"}:
        return resolved.parents[2]
    # Current app layout: <root>/core/app/run_senzing_end_to_end.py
    if resolved.parent.name == "app":
        return resolved.parent.parent
    # Flat layout: <root>/run_senzing_end_to_end.py
    return resolved.parent


def resolve_registry_dir(repo_root: Path) -> Path:
    """Resolve directory used for run registry / generation summaries."""
    output_dir = repo_root / "output"
    if output_dir.exists():
        return output_dir
    return repo_root


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


def read_license_string_file(path: Path) -> str | None:
    """Read and normalize base64 license content from file."""
    if not path.exists() or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="ignore")
    compact = "".join(text.split())
    return compact if compact else None


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
    env_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Run one shell command and store stdout/stderr into log file."""
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
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
            env=env,
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


def build_shell_prefix(
    project_setup_env: Path,
    engine_config_json: str | None = None,
    license_string: str | None = None,
) -> str:
    """Build shell prefix that sources setupEnv and applies optional runtime overrides."""
    parts = [f"source {shlex.quote(str(project_setup_env))} >/dev/null 2>&1"]
    if engine_config_json:
        parts.append(f"export SENZING_ENGINE_CONFIGURATION_JSON={shlex.quote(engine_config_json)}")
    return " && ".join(parts) + " && "


def build_load_command(
    project_setup_env: Path,
    input_jsonl: Path,
    num_threads: int,
    no_shuffle: bool = False,
    engine_config_json: str | None = None,
    license_string: str | None = None,
) -> str:
    """Build sz_file_loader shell command."""
    cmd = (
        build_shell_prefix(project_setup_env, engine_config_json=engine_config_json, license_string=license_string)
        + f"sz_file_loader -f {shlex.quote(str(input_jsonl))}"
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
    engine_config_json: str | None = None,
    license_string: str | None = None,
) -> str:
    """Build sz_snapshot shell command."""
    cmd = (
        build_shell_prefix(project_setup_env, engine_config_json=engine_config_json, license_string=license_string)
        + f"sz_snapshot -o {shlex.quote(str(snapshot_prefix))} -Q"
    )
    if thread_count > 0:
        cmd += f" -t {thread_count}"
    if force_sdk:
        cmd += " -F"
    return cmd


def merge_license_into_engine_config(config_json: str, license_string: str) -> str:
    """Merge LICENSESTRINGBASE64 into engine configuration JSON."""
    try:
        payload = json.loads(config_json)
    except Exception:
        return config_json
    if not isinstance(payload, dict):
        return config_json
    pipeline = payload.get("PIPELINE")
    if not isinstance(pipeline, dict):
        pipeline = {}
        payload["PIPELINE"] = pipeline
    pipeline["LICENSESTRINGBASE64"] = license_string
    return json.dumps(payload, separators=(",", ":"))


def load_setup_env(project_setup_env: Path, license_string: str | None = None) -> dict[str, str]:
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

    if license_string:
        env_map[LICENSE_STRING_ENV] = license_string
    return env_map


def sqlite_connection_url(db_path: Path) -> str:
    """Build SQLite connection URL accepted by Senzing."""
    absolute = str(db_path.resolve())
    return f"sqlite3://na:na@{absolute}"


def build_engine_config_json(project_dir: Path) -> str:
    """Build a fallback G2Engine config JSON based on project directory layout."""
    payload = {
        "PIPELINE": {
            "CONFIGPATH": str(project_dir / "etc"),
            "SUPPORTPATH": str(project_dir / "data"),
            "RESOURCEPATH": str(project_dir / "resources"),
        },
        "SQL": {
            "CONNECTION": sqlite_connection_url(project_dir / "var" / "sqlite" / "G2C.db"),
        },
    }
    return json.dumps(payload)


def build_modern_engine_config_json(project_dir: Path, license_string: str | None = None) -> str:
    """Build engine settings for modern SDK containers using shared runtime paths."""
    payload = {
        "PIPELINE": {
            "CONFIGPATH": str(MODERN_ETC_DIR),
            "SUPPORTPATH": str(MODERN_DATA_DIR),
            "RESOURCEPATH": str(MODERN_RESOURCE_DIR),
        },
        "SQL": {
            "CONNECTION": sqlite_connection_url(project_dir / "var" / "sqlite" / "G2C.db"),
        },
    }
    if license_string:
        payload["PIPELINE"]["LICENSESTRINGBASE64"] = license_string
    return json.dumps(payload, separators=(",", ":"))


def ensure_link(target: Path, link_path: Path) -> str:
    """Create or refresh a symlink for project compatibility paths."""
    if link_path.exists() or link_path.is_symlink():
        try:
            current = link_path.resolve()
            if current == target.resolve():
                return "existing"
        except OSError:
            pass
        if link_path.is_dir() and not link_path.is_symlink():
            shutil.rmtree(link_path)
        else:
            link_path.unlink()
    link_path.parent.mkdir(parents=True, exist_ok=True)
    link_path.symlink_to(target, target_is_directory=target.is_dir())
    return "created"


def write_modern_setup_env(project_dir: Path, engine_config_json: str) -> Path:
    """Write setupEnv compatible with shell-based steps and SDK explain."""
    setup_env = project_dir / "setupEnv"
    content = f"""#!/usr/bin/env bash
export SENZING_ROOT=/opt/senzing
export SENZING_ETC_PATH={shlex.quote(str(MODERN_ETC_DIR))}
export SENZING_DATA_DIR={shlex.quote(str(MODERN_DATA_DIR))}
export SENZING_G2_DIR=/opt/senzing/g2
export PATH=/opt/senzing/er/bin:$PATH
export PYTHONPATH=/opt/senzing/er/sdk/python:/opt/senzing/g2/sdk/python:/opt/senzing/g2/python${{PYTHONPATH:+:$PYTHONPATH}}
export LD_LIBRARY_PATH={shlex.quote(str(MODERN_LIB_DIR))}${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}
export SENZING_PROJECT_FLAVOR=modern_sdk
export SENZING_ENGINE_CONFIGURATION_JSON={shlex.quote(engine_config_json)}
"""
    setup_env.write_text(content, encoding="utf-8")
    setup_env.chmod(0o755)
    return setup_env


def embed_license_in_setup_env(project_setup_env: Path, project_dir: Path, license_string: str) -> None:
    """Persist license into setupEnv so Senzing CLI tools can pick it up without logging the secret."""
    marker_start = "# BEGIN CODex SENZING LICENSE BLOCK"
    marker_end = "# END CODex SENZING LICENSE BLOCK"
    existing = project_setup_env.read_text(encoding="utf-8") if project_setup_env.exists() else "#!/usr/bin/env bash\n"
    if marker_start in existing and marker_end in existing:
        prefix, remainder = existing.split(marker_start, 1)
        _, suffix = remainder.split(marker_end, 1)
        existing = prefix.rstrip() + "\n" + suffix.lstrip("\n")
    engine_config_json = merge_license_into_engine_config(build_engine_config_json(project_dir), license_string)
    block = (
        f"{marker_start}\n"
        f"export {LICENSE_STRING_ENV}={shlex.quote(license_string)}\n"
        f"export SENZING_ENGINE_CONFIGURATION_JSON={shlex.quote(engine_config_json)}\n"
        f"{marker_end}\n"
    )
    updated = existing.rstrip() + "\n" + block
    project_setup_env.write_text(updated, encoding="utf-8")
    project_setup_env.chmod(0o700)


def initialize_modern_sqlite_schema(db_path: Path) -> None:
    """Initialize SQLite schema used by modern SDK runtime."""
    if not MODERN_SCHEMA_SQL_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {MODERN_SCHEMA_SQL_PATH}")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    sql_text = MODERN_SCHEMA_SQL_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql_text)
        conn.commit()
    finally:
        conn.close()


def create_modern_factory(settings_json: str) -> Any:
    """Create modern SDK abstract factory."""
    from senzing_core import SzAbstractFactoryCore  # type: ignore

    return SzAbstractFactoryCore("mapper_e2e", settings_json)


def datasource_codes_from_registry(registry_json: str) -> set[str]:
    """Extract datasource codes from registry JSON string."""
    try:
        payload = json.loads(registry_json)
    except Exception:
        return set()
    items = payload.get("DATA_SOURCES") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        return set()
    output: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        code = str(item.get("DSRC_CODE") or "").strip()
        if code:
            output.add(code)
    return output


def command_missing(step: dict[str, Any]) -> bool:
    """Return True when a shell step failed because the command was unavailable."""
    stderr = str(step.get("stderr_tail") or "").lower()
    stdout = str(step.get("stdout_tail") or "").lower()
    combined = f"{stdout}\n{stderr}"
    return step.get("exit_code") == 127 or "command not found" in combined or "no such file or directory" in combined


def create_project_modern(project_dir: Path, log_path: Path, license_string: str | None = None) -> dict[str, Any]:
    """Bootstrap a modern SDK-backed project when legacy CLI create-project is unavailable."""
    start = time.time()
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "var" / "sqlite").mkdir(parents=True, exist_ok=True)
    engine_config_json = build_modern_engine_config_json(project_dir, license_string=license_string)

    link_results = {
        "lib": ensure_link(MODERN_LIB_DIR, project_dir / "lib"),
        "resources": ensure_link(MODERN_RESOURCE_DIR, project_dir / "resources"),
        "data": ensure_link(MODERN_DATA_DIR, project_dir / "data"),
        "etc": ensure_link(MODERN_ETC_DIR, project_dir / "etc"),
    }
    db_path = project_dir / "var" / "sqlite" / "G2C.db"
    initialize_modern_sqlite_schema(db_path)
    write_modern_setup_env(project_dir, engine_config_json)

    template_json = MODERN_TEMPLATE_CONFIG_PATH.read_text(encoding="utf-8")
    factory = create_modern_factory(engine_config_json)
    try:
        config_manager = factory.create_configmanager()
        config = config_manager.create_config_from_string(template_json)
        config_id = config_manager.register_config(config.export(), "bootstrap modern sdk project")
        config_manager.set_default_config_id(config_id)
    finally:
        factory.destroy()

    duration = round(time.time() - start, 3)
    log_lines = [
        "STEP: create_project",
        f"MODE: modern_sdk",
        f"PROJECT_DIR: {project_dir}",
        f"DB_PATH: {db_path}",
        f"SETUP_ENV: {project_dir / 'setupEnv'}",
        f"DURATION_SECONDS: {duration}",
        "",
        "--- LINK RESULTS ---",
        json.dumps(link_results, indent=2, ensure_ascii=False),
        "",
        "--- ENGINE CONFIG ---",
        engine_config_json,
    ]
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return {
        "step": "create_project",
        "ok": True,
        "exit_code": 0,
        "duration_seconds": duration,
        "log_file": str(log_path),
        "stdout_tail": "modern_sdk bootstrap completed",
        "stderr_tail": "",
        "mode": "modern_sdk",
    }


def configure_data_source_modern(
    project_dir: Path,
    data_source: str,
    log_path: Path,
    license_string: str | None = None,
) -> dict[str, Any]:
    """Configure a datasource through the modern SDK config manager."""
    start = time.time()
    engine_config_json = build_modern_engine_config_json(project_dir, license_string=license_string)
    template_json = MODERN_TEMPLATE_CONFIG_PATH.read_text(encoding="utf-8")
    factory = create_modern_factory(engine_config_json)
    created = False
    existing_codes: set[str] = set()
    config_id = None
    try:
        config_manager = factory.create_configmanager()
        try:
            default_config_id = config_manager.get_default_config_id()
        except Exception:
            default_config_id = 0
        if default_config_id:
            config = config_manager.create_config_from_config_id(default_config_id)
        else:
            config = config_manager.create_config_from_string(template_json)
        existing_codes = datasource_codes_from_registry(config.get_data_source_registry())
        if data_source not in existing_codes:
            config.register_data_source(data_source)
            config_id = config_manager.register_config(config.export(), f"add datasource {data_source}")
            config_manager.set_default_config_id(config_id)
            created = True
    finally:
        factory.destroy()

    duration = round(time.time() - start, 3)
    log_payload = {
        "step": f"configure_data_source_{data_source}",
        "mode": "modern_sdk",
        "data_source": data_source,
        "created": created,
        "config_id": config_id,
        "existing_data_sources": sorted(existing_codes),
        "duration_seconds": duration,
    }
    log_path.write_text(json.dumps(log_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "step": f"configure_data_source_{data_source}",
        "ok": True,
        "exit_code": 0,
        "duration_seconds": duration,
        "log_file": str(log_path),
        "stdout_tail": "created" if created else "already_exists",
        "stderr_tail": "",
        "mode": "modern_sdk",
    }


def export_csv_modern(
    project_dir: Path,
    export_file: Path,
    log_path: Path,
    license_string: str | None = None,
) -> dict[str, Any]:
    """Export entity report to CSV through the modern SDK."""
    start = time.time()
    from senzing import SzEngineFlags  # type: ignore

    engine_config_json = build_modern_engine_config_json(project_dir, license_string=license_string)
    factory = create_modern_factory(engine_config_json)
    rows_written = 0
    try:
        engine = factory.create_engine()
        flags = int(
            SzEngineFlags.SZ_EXPORT_INCLUDE_SINGLE_RECORD_ENTITIES
            | SzEngineFlags.SZ_EXPORT_INCLUDE_MULTI_RECORD_ENTITIES
            | SzEngineFlags.SZ_EXPORT_INCLUDE_POSSIBLY_SAME
            | SzEngineFlags.SZ_EXPORT_INCLUDE_POSSIBLY_RELATED
            | SzEngineFlags.SZ_EXPORT_INCLUDE_NAME_ONLY
            | SzEngineFlags.SZ_EXPORT_INCLUDE_DISCLOSED
        )
        handle = engine.export_csv_entity_report(
            "RESOLVED_ENTITY_ID,DATA_SOURCE,RECORD_ID,MATCH_LEVEL,MATCH_KEY",
            flags,
        )
        export_file.parent.mkdir(parents=True, exist_ok=True)
        with export_file.open("w", encoding="utf-8", newline="") as outfile:
            while True:
                row = engine.fetch_next(handle)
                if not row:
                    break
                outfile.write(row.rstrip("\n") + "\n")
                rows_written += 1
        engine.close_export_report(handle)
    finally:
        factory.destroy()

    duration = round(time.time() - start, 3)
    log_payload = {
        "step": "export",
        "mode": "modern_sdk",
        "export_file": str(export_file),
        "rows_written": rows_written,
        "duration_seconds": duration,
    }
    log_path.write_text(json.dumps(log_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "step": "export",
        "ok": export_file.exists() and rows_written > 0,
        "exit_code": 0,
        "duration_seconds": duration,
        "log_file": str(log_path),
        "stdout_tail": f"rows_written={rows_written}",
        "stderr_tail": "",
        "mode": "modern_sdk",
    }


def snapshot_modern(
    project_dir: Path,
    snapshot_json: Path,
    log_path: Path,
    license_string: str | None = None,
) -> dict[str, Any]:
    """Generate a JSON entity snapshot through the modern SDK."""
    start = time.time()
    from senzing import SzEngineFlags  # type: ignore

    engine_config_json = build_modern_engine_config_json(project_dir, license_string=license_string)
    factory = create_modern_factory(engine_config_json)
    rows_written = 0
    try:
        engine = factory.create_engine()
        flags = int(
            SzEngineFlags.SZ_EXPORT_INCLUDE_SINGLE_RECORD_ENTITIES
            | SzEngineFlags.SZ_EXPORT_INCLUDE_MULTI_RECORD_ENTITIES
            | SzEngineFlags.SZ_EXPORT_INCLUDE_POSSIBLY_SAME
            | SzEngineFlags.SZ_EXPORT_INCLUDE_POSSIBLY_RELATED
            | SzEngineFlags.SZ_EXPORT_INCLUDE_NAME_ONLY
            | SzEngineFlags.SZ_EXPORT_INCLUDE_DISCLOSED
        )
        handle = engine.export_json_entity_report(flags)
        snapshot_json.parent.mkdir(parents=True, exist_ok=True)
        with snapshot_json.open("w", encoding="utf-8") as outfile:
            while True:
                row = engine.fetch_next(handle)
                if not row:
                    break
                outfile.write(row.rstrip("\n") + "\n")
                rows_written += 1
        engine.close_export_report(handle)
    finally:
        factory.destroy()

    duration = round(time.time() - start, 3)
    log_payload = {
        "step": "snapshot",
        "mode": "modern_sdk",
        "snapshot_json": str(snapshot_json),
        "rows_written": rows_written,
        "duration_seconds": duration,
    }
    log_path.write_text(json.dumps(log_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "step": "snapshot",
        "ok": snapshot_json.exists() and rows_written > 0,
        "exit_code": 0,
        "duration_seconds": duration,
        "log_file": str(log_path),
        "stdout_tail": f"rows_written={rows_written}",
        "stderr_tail": "",
        "mode": "modern_sdk",
    }


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

    loaded_env = load_setup_env(
        project_setup_env,
        license_string=os.environ.get(LICENSE_STRING_ENV, "").strip() or None,
    )
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


def create_project(
    project_dir: Path,
    base_setup_env: Path | None,
    log_path: Path,
    license_string: str | None = None,
) -> dict[str, Any]:
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

    if not combined_log["ok"]:
        modern_ready = MODERN_SCHEMA_SQL_PATH.exists() and MODERN_TEMPLATE_CONFIG_PATH.exists()
        if modern_ready:
            with log_path.open("a", encoding="utf-8") as log:
                log.write("\n--- FALLBACK modern_sdk ---\n")
            try:
                modern_step = create_project_modern(project_dir, log_path, license_string=license_string)
                modern_step["duration_seconds"] = round(time.time() - start, 3)
                return modern_step
            except Exception as err:  # pylint: disable=broad-exception-caught
                with log_path.open("a", encoding="utf-8") as log:
                    log.write(f"MODERN_FALLBACK_ERROR: {err}\n")
                combined_log["stderr_tail"] = f"{combined_log['stderr_tail']}\nmodern_fallback: {err}".strip()[-1200:]

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
        "--stream-export",
        action="store_true",
        help=(
            "Stream sz_export output directly into comparison artifacts (no large export CSV on disk). "
            "Requires --skip-explain and comparison enabled."
        ),
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
        "--load-no-shuffle-primary",
        action="store_true",
        help="Disable shuffle on primary sz_file_loader attempt (reduces temp disk pressure on large loads).",
    )
    parser.add_argument(
        "--enable-load-chunk-fallback",
        action="store_true",
        help=(
            "If standard load attempts fail, retry load in sequential single-thread JSONL chunks "
            "(keeps all records; slower but more stable)."
        ),
    )
    parser.add_argument(
        "--load-chunk-size",
        type=int,
        default=0,
        help="Records per chunk for chunked load fallback (default: 0 = disabled).",
    )
    parser.add_argument(
        "--keep-load-chunk-files",
        action="store_true",
        help="Keep temporary chunk JSONL files generated by chunked load fallback.",
    )
    parser.add_argument(
        "--load-batch-size",
        type=int,
        default=0,
        help=(
            "Optional proactive load batching size (records per batch). "
            "When > 0, input JSONL is split into sequential batches and loaded one batch at a time."
        ),
    )
    parser.add_argument(
        "--keep-load-batch-files",
        action="store_true",
        help="Keep temporary JSONL files generated for proactive load batches.",
    )
    parser.add_argument(
        "--continue-on-failed-file",
        action="store_true",
        help=(
            "When proactive file split is enabled, continue loading next files even if one file fails. "
            "Failed files are quarantined for later replay."
        ),
    )
    parser.add_argument(
        "--max-failed-files",
        type=int,
        default=0,
        help=(
            "Maximum number of failed split files allowed before aborting the run "
            "(default: 0 = unlimited when --continue-on-failed-file is enabled)."
        ),
    )
    parser.add_argument(
        "--load-file-timeout-seconds",
        type=int,
        default=0,
        help=(
            "Maximum wall-clock seconds allowed for loading one split file "
            "(0 = disabled, uses normal step timeout behavior)."
        ),
    )
    parser.add_argument(
        "--failed-files-output-dir",
        default="failed_files",
        help="Run-relative directory where failed split files are copied (default: failed_files).",
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
    parser.add_argument(
        "--license-base64-file",
        default=None,
        help="Optional path to file containing LICENSESTRINGBASE64. Overrides env SENZING_LICENSE_STRING_BASE64.",
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
            normalized = normalize_export_row(row)
            if normalized:
                rows.append(normalized)
    return rows


def normalize_export_row(row: dict[str, Any]) -> dict[str, str]:
    """Normalize sz_export row keys and values."""
    normalized: dict[str, str] = {}
    for key, value in row.items():
        if key is None:
            continue
        norm_key = str(key).strip().strip('"').strip().upper()
        norm_value = str(value or "").strip().strip('"').strip()
        normalized[norm_key] = norm_value
    return normalized


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


def describe_load_failure(step: dict[str, Any]) -> str:
    """Summarize a load attempt failure for adaptive retry warnings."""
    if step.get("timed_out"):
        return "timeout"
    combined = (
        f"{step.get('stderr_tail') or ''}\n{step.get('stdout_tail') or ''}"
    ).lower()
    if "locked" in combined or "lock" in combined or "sqlite_busy" in combined or "busy" in combined:
        return "probable lock/contention"
    return f"exit_code={step.get('exit_code')}"


def build_load_attempt_specs(
    load_threads: int,
    load_fallback_threads: int,
    load_no_shuffle_primary: bool,
    disable_stability_retries: bool,
) -> list[dict[str, Any]]:
    """Build adaptive load attempt plan.

    Strategy:
    - first attempt uses the requested primary profile
    - thread fallback attempts preserve the same shuffle mode
    - progressively reduce thread count down to the fallback floor
    """
    attempts: list[dict[str, Any]] = [
        {
            "attempt_mode": "primary",
            "threads": load_threads,
            "no_shuffle": load_no_shuffle_primary,
        }
    ]
    if disable_stability_retries:
        return attempts

    seen: set[tuple[int, bool]] = {(load_threads, load_no_shuffle_primary)}

    def add_attempt(mode: str, threads: int, no_shuffle: bool) -> None:
        key = (threads, no_shuffle)
        if threads <= 0 or key in seen:
            return
        attempts.append(
            {
                "attempt_mode": mode,
                "threads": threads,
                "no_shuffle": no_shuffle,
            }
        )
        seen.add(key)

    fallback_floor = min(load_threads, max(1, load_fallback_threads))
    for threads in range(load_threads - 1, fallback_floor - 1, -1):
        add_attempt(f"retry_threads_{threads}", threads, load_no_shuffle_primary)

    add_attempt("fallback_floor", fallback_floor, load_no_shuffle_primary)
    return attempts


def run_chunked_load_fallback(
    project_setup_env: Path,
    load_input_jsonl: Path,
    chunk_dir: Path,
    logs_dir: Path,
    chunk_size: int,
    timeout_seconds: int | None,
    file_deadline_ts: float | None = None,
    engine_config_json: str | None = None,
    license_string: str | None = None,
    keep_chunk_files: bool = False,
    keep_loader_temp_files: bool = False,
) -> tuple[bool, list[dict[str, Any]], list[str], int, int]:
    """Load input in sequential single-thread chunks.

    Returns:
    - ok
    - chunk step list
    - runtime warnings
    - chunks attempted
    - records attempted
    """
    if chunk_size <= 0:
        return False, [], ["Chunk fallback requested with invalid chunk size."], 0, 0

    chunk_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    steps: list[dict[str, Any]] = []
    chunk_index = 0
    step_attempts = 0
    failed_single_record_ids: list[str] = []
    total_records = 0

    def extract_record_id_from_line(raw_line: str) -> str | None:
        try:
            obj = json.loads(raw_line)
        except Exception:
            return None
        if not isinstance(obj, dict):
            return None
        rid = str(obj.get("RECORD_ID") or "").strip()
        return rid or None

    def execute_chunk(chunk_lines: list[str], idx: int, split_level: int = 0, split_tag: str = "") -> bool:
        nonlocal step_attempts
        file_suffix = f"{idx:05d}"
        if split_tag:
            file_suffix = f"{file_suffix}_{split_tag}"
        chunk_file = chunk_dir / f"load_chunk_{file_suffix}.jsonl"
        chunk_file.write_text("\n".join(chunk_lines) + "\n", encoding="utf-8")
        chunk_cmd = build_load_command(
            project_setup_env=project_setup_env,
            input_jsonl=chunk_file,
            num_threads=1,
            no_shuffle=True,
            engine_config_json=engine_config_json,
            license_string=license_string,
        )
        effective_timeout = timeout_seconds
        if file_deadline_ts is not None:
            remaining = int(file_deadline_ts - time.time())
            if remaining <= 0:
                warnings.append(
                    f"Chunk {file_suffix} skipped: load-file timeout exceeded before chunk execution."
                )
                return False
            if effective_timeout is None:
                effective_timeout = remaining
            else:
                effective_timeout = max(1, min(effective_timeout, remaining))
        step = run_shell_step(
            step_name=f"load_records_chunk_{file_suffix}",
            shell_command=chunk_cmd,
            log_path=logs_dir / f"02_load_chunk_{file_suffix}.log",
            timeout_seconds=effective_timeout,
        )
        step_attempts += 1
        step["attempt_mode"] = "chunked_single_thread"
        step["chunk_index"] = idx
        step["chunk_records"] = len(chunk_lines)
        step["chunk_file"] = str(chunk_file)
        step["chunk_split_level"] = split_level
        step["chunk_split_tag"] = split_tag
        steps.append(step)

        if step["ok"] and (not keep_loader_temp_files):
            removed = cleanup_loader_shuffle_files(chunk_file)
            if removed:
                warnings.append(
                    f"Removed {len(removed)} loader temp file(s) after chunk {file_suffix}."
                )
        if step["ok"] and (not keep_chunk_files) and chunk_file.exists():
            try:
                chunk_file.unlink()
            except OSError:
                warnings.append(f"Unable to delete chunk file: {chunk_file}")
        if step["ok"]:
            return True

        # Adaptive split: if a chunk fails, split and retry smaller chunks.
        if len(chunk_lines) <= 1:
            rid = extract_record_id_from_line(chunk_lines[0]) if chunk_lines else None
            if rid:
                failed_single_record_ids.append(rid)
            warnings.append(
                f"Chunk {file_suffix} failed at single-record granularity; "
                f"RECORD_ID={rid or '<unknown>'}. See {step.get('log_file')}."
            )
            return False

        mid = len(chunk_lines) // 2
        left = chunk_lines[:mid]
        right = chunk_lines[mid:]
        warnings.append(
            f"Chunk {file_suffix} failed (size={len(chunk_lines)}); "
            f"splitting into {len(left)} + {len(right)}."
        )
        left_ok = execute_chunk(left, idx, split_level + 1, f"{split_tag}a")
        right_ok = execute_chunk(right, idx, split_level + 1, f"{split_tag}b")
        return left_ok and right_ok

    current_chunk: list[str] = []
    with load_input_jsonl.open("r", encoding="utf-8", errors="replace") as infile:
        for line in infile:
            text = line.strip()
            if not text:
                continue
            current_chunk.append(text)
            total_records += 1
            if len(current_chunk) >= chunk_size:
                chunk_index += 1
                if not execute_chunk(current_chunk, chunk_index):
                    failed_ids_path = chunk_dir / "failed_single_record_ids.txt"
                    if failed_single_record_ids:
                        failed_ids_path.write_text(
                            "\n".join(sorted(set(failed_single_record_ids))) + "\n",
                            encoding="utf-8",
                        )
                        warnings.append(f"Failed single-record IDs written to: {failed_ids_path}")
                    return False, steps, warnings, step_attempts, total_records
                current_chunk = []

    if current_chunk:
        chunk_index += 1
        if not execute_chunk(current_chunk, chunk_index):
            failed_ids_path = chunk_dir / "failed_single_record_ids.txt"
            if failed_single_record_ids:
                failed_ids_path.write_text(
                    "\n".join(sorted(set(failed_single_record_ids))) + "\n",
                    encoding="utf-8",
                )
                warnings.append(f"Failed single-record IDs written to: {failed_ids_path}")
            return False, steps, warnings, step_attempts, total_records

    if failed_single_record_ids:
        failed_ids_path = chunk_dir / "failed_single_record_ids.txt"
        failed_ids_path.write_text(
            "\n".join(sorted(set(failed_single_record_ids))) + "\n",
            encoding="utf-8",
        )
        warnings.append(f"Failed single-record IDs written to: {failed_ids_path}")
    return True, steps, warnings, step_attempts, total_records


def run_load_attempts_for_file(
    project_setup_env: Path,
    load_input_jsonl: Path,
    logs_dir: Path,
    step_timeout_seconds: int | None,
    load_threads: int,
    load_fallback_threads: int,
    load_no_shuffle_primary: bool,
    disable_stability_retries: bool,
    enable_load_chunk_fallback: bool,
    load_chunk_size: int,
    chunk_dir: Path,
    engine_config_json: str | None = None,
    license_string: str | None = None,
    keep_load_chunk_files: bool = False,
    keep_loader_temp_files: bool = False,
    load_file_timeout_seconds: int | None = None,
    step_name_prefix: str = "load_records",
    log_name_prefix: str = "02_load",
) -> tuple[bool, list[dict[str, Any]], list[str], list[str]]:
    """Run load attempts for one JSONL file with retries and optional chunk fallback."""
    steps: list[dict[str, Any]] = []
    runtime_warnings: list[str] = []
    loader_temp_files_removed: list[str] = []
    file_started_at = time.time()
    file_deadline_ts = None
    if load_file_timeout_seconds is not None and load_file_timeout_seconds > 0:
        file_deadline_ts = file_started_at + load_file_timeout_seconds

    def resolve_timeout_for_step() -> int | None:
        if file_deadline_ts is None:
            return step_timeout_seconds
        remaining = int(file_deadline_ts - time.time())
        if remaining <= 0:
            return 0
        if step_timeout_seconds is None:
            return remaining
        return max(1, min(step_timeout_seconds, remaining))

    load_attempt_specs = build_load_attempt_specs(
        load_threads=load_threads,
        load_fallback_threads=load_fallback_threads,
        load_no_shuffle_primary=load_no_shuffle_primary,
        disable_stability_retries=disable_stability_retries,
    )

    load_ok = False
    for attempt_index, attempt_spec in enumerate(load_attempt_specs):
        attempt_mode = str(attempt_spec["attempt_mode"])
        attempt_threads = int(attempt_spec["threads"])
        attempt_no_shuffle = bool(attempt_spec["no_shuffle"])
        load_cmd = build_load_command(
            project_setup_env=project_setup_env,
            input_jsonl=load_input_jsonl,
            num_threads=attempt_threads,
            no_shuffle=attempt_no_shuffle,
            engine_config_json=engine_config_json,
            license_string=license_string,
        )
        load_log_path = logs_dir / (
            f"{log_name_prefix}.log" if attempt_index == 0 else f"{log_name_prefix}_retry_{attempt_index}.log"
        )
        step_name = step_name_prefix if attempt_index == 0 else f"{step_name_prefix}_retry_{attempt_index}"
        timeout_for_step = resolve_timeout_for_step()
        if timeout_for_step == 0:
            runtime_warnings.append(
                f"{step_name_prefix} skipped remaining attempts: load-file timeout exceeded."
            )
            break
        step = run_shell_step(
            step_name=step_name,
            shell_command=load_cmd,
            log_path=load_log_path,
            timeout_seconds=timeout_for_step,
        )
        step["attempt_mode"] = attempt_mode
        step["attempt_threads"] = attempt_threads
        step["attempt_no_shuffle"] = attempt_no_shuffle
        step["load_input_jsonl"] = str(load_input_jsonl)
        steps.append(step)
        if step["ok"]:
            if attempt_index > 0:
                runtime_warnings.append(
                    f"{step_name_prefix} previous attempts failed; retry '{attempt_mode}' "
                    f"succeeded with {attempt_threads} thread(s)"
                    f"{' and no-shuffle' if attempt_no_shuffle else ''}."
                )
            load_ok = True
            break
        if attempt_index + 1 < len(load_attempt_specs):
            next_attempt = load_attempt_specs[attempt_index + 1]
            runtime_warnings.append(
                f"{step_name_prefix} attempt '{attempt_mode}' failed ({describe_load_failure(step)}); "
                f"retrying with {int(next_attempt['threads'])} thread(s)"
                f"{' and no-shuffle' if bool(next_attempt['no_shuffle']) else ''}."
            )

    if not load_ok and enable_load_chunk_fallback and load_chunk_size > 0:
        timeout_for_chunks = resolve_timeout_for_step()
        if timeout_for_chunks == 0:
            runtime_warnings.append(
                f"{step_name_prefix} chunk fallback skipped: load-file timeout exceeded."
            )
            return False, steps, runtime_warnings, loader_temp_files_removed
        runtime_warnings.append(
            f"{step_name_prefix} standard retries failed; trying chunked fallback (chunk_size={load_chunk_size})."
        )
        chunk_ok, chunk_steps, chunk_warnings, chunks_attempted, records_attempted = run_chunked_load_fallback(
            project_setup_env=project_setup_env,
            load_input_jsonl=load_input_jsonl,
            chunk_dir=chunk_dir,
            logs_dir=logs_dir,
            chunk_size=load_chunk_size,
            timeout_seconds=timeout_for_chunks,
            file_deadline_ts=file_deadline_ts,
            engine_config_json=engine_config_json,
            license_string=license_string,
            keep_chunk_files=keep_load_chunk_files,
            keep_loader_temp_files=keep_loader_temp_files,
        )
        steps.extend(chunk_steps)
        runtime_warnings.extend(chunk_warnings)
        if chunk_ok:
            load_ok = True
            runtime_warnings.append(
                f"{step_name_prefix} chunked load fallback succeeded "
                f"({chunks_attempted} chunks, {records_attempted} records)."
            )
        else:
            runtime_warnings.append(
                f"{step_name_prefix} chunked load fallback failed after {chunks_attempted} chunks."
            )

    if load_ok and (not keep_loader_temp_files):
        removed = cleanup_loader_shuffle_files(load_input_jsonl)
        if removed:
            runtime_warnings.append(
                f"Removed {len(removed)} loader temp file(s) for {load_input_jsonl.name}."
            )
            loader_temp_files_removed.extend(removed)

    return load_ok, steps, runtime_warnings, loader_temp_files_removed


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


def build_ground_truth_match_quality_from_record_to_entity(
    input_jsonl_path: Path,
    record_to_entity: dict[tuple[str, str], str],
) -> dict[str, Any]:
    """Compute match quality metrics against SOURCE_IPG_ID ground truth."""
    source_info = load_source_ipg_labels(input_jsonl_path)
    labels: dict[tuple[str, str], str] = source_info["labels"]

    ipg_counts: Counter[str] = Counter()
    entity_ipg_counts: dict[str, Counter[str]] = defaultdict(Counter)
    entity_record_counts: Counter[str] = Counter()
    labeled_records_in_export = 0

    for key, source_ipg_id in labels.items():
        entity_id = record_to_entity.get(key)
        if not entity_id:
            continue
        labeled_records_in_export += 1
        ipg_counts[source_ipg_id] += 1
        entity_ipg_counts[entity_id][source_ipg_id] += 1
        entity_record_counts[entity_id] += 1

    true_pairs = sum(comb2(count) for count in ipg_counts.values())
    predicted_pairs = sum(comb2(sum(counter.values())) for counter in entity_ipg_counts.values())
    true_positive = sum(comb2(count) for counter in entity_ipg_counts.values() for count in counter.values())
    false_positive = max(0, predicted_pairs - true_positive)
    false_negative = max(0, true_pairs - true_positive)

    pair_precision = safe_ratio(true_positive, true_positive + false_positive)
    pair_recall = safe_ratio(true_positive, true_positive + false_negative)
    entity_size_distribution: Counter[int] = Counter(entity_record_counts.values())
    entity_pairings_distribution: Counter[int] = Counter()
    record_pairing_degree_distribution: Counter[int] = Counter()
    for size, entities_count in entity_size_distribution.items():
        entity_pairings_distribution[comb2(size)] += entities_count
        record_pairing_degree_distribution[max(0, size - 1)] += size * entities_count

    entities_with_labeled_records = sum(entity_size_distribution.values())
    largest_labeled_entity_size = max(entity_size_distribution.keys(), default=0)

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
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "predicted_pairs_labeled": predicted_pairs,
            "ground_truth_pairs_labeled": true_pairs,
        },
        "distribution_metrics": {
            "entities_with_labeled_records": entities_with_labeled_records,
            "largest_labeled_entity_size": largest_labeled_entity_size,
            "entity_size_distribution": {str(k): v for k, v in sorted(entity_size_distribution.items())},
            "entity_pairings_distribution": {str(k): v for k, v in sorted(entity_pairings_distribution.items())},
            "record_pairing_degree_distribution": {str(k): v for k, v in sorted(record_pairing_degree_distribution.items())},
        },
    }


def build_ground_truth_match_quality(
    input_jsonl_path: Path,
    entity_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute match quality metrics against SOURCE_IPG_ID ground truth."""
    record_to_entity: dict[tuple[str, str], str] = {}
    for row in entity_rows:
        key = parse_record_key(row.get("data_source"), row.get("record_id"))
        entity_id = str(row.get("resolved_entity_id") or "").strip()
        if key is None or not entity_id:
            continue
        record_to_entity[key] = entity_id
    return build_ground_truth_match_quality_from_record_to_entity(
        input_jsonl_path=input_jsonl_path,
        record_to_entity=record_to_entity,
    )


def build_ground_truth_match_quality_from_entity_csv(
    input_jsonl_path: Path,
    entity_records_csv: Path,
) -> dict[str, Any]:
    """Compute ground truth metrics by reading entity_records CSV incrementally."""
    record_to_entity: dict[tuple[str, str], str] = {}
    if entity_records_csv.exists():
        with entity_records_csv.open("r", encoding="utf-8", newline="") as infile:
            for row in csv.DictReader(infile):
                key = parse_record_key(row.get("data_source"), row.get("record_id"))
                entity_id = str(row.get("resolved_entity_id") or "").strip()
                if key is None or not entity_id:
                    continue
                record_to_entity[key] = entity_id
    return build_ground_truth_match_quality_from_record_to_entity(
        input_jsonl_path=input_jsonl_path,
        record_to_entity=record_to_entity,
    )


def write_ground_truth_match_quality_reports(
    comparison_dir: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path]:
    """Write management-facing ground truth quality reports."""
    quality_json = comparison_dir / "ground_truth_match_quality.json"
    quality_md = comparison_dir / "ground_truth_match_quality.md"

    quality_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pair_metrics = payload.get("pair_metrics", {})
    distribution_metrics = payload.get("distribution_metrics", {})
    data_quality = payload.get("data_quality", {})

    lines: list[str] = []
    lines.append("# Match Quality vs SOURCE_IPG_ID")
    lines.append("")
    lines.append(f"- Generated at: {payload.get('generated_at')}")
    lines.append(f"- Input JSONL: {payload.get('input_jsonl')}")
    lines.append("")
    lines.append("## Pair Quality")
    lines.append("")
    lines.append(f"- Pair precision: {format_percent(pair_metrics.get('pair_precision'))} (Out of all predicted matches, how many are correct.)")
    lines.append(f"- Pair recall: {format_percent(pair_metrics.get('pair_recall'))} (Out of all real matches, how many were found.)")
    lines.append(f"- True positive: {pair_metrics.get('true_positive', 0)} (Predicted match and truly a match.)")
    lines.append(f"- False positive: {pair_metrics.get('false_positive', 0)} (Predicted match but actually wrong.)")
    lines.append(f"- False negative: {pair_metrics.get('false_negative', 0)} (Real match that was missed.)")
    lines.append("")
    lines.append("## Supporting Counts")
    lines.append("")
    lines.append(f"- Predicted pairs (labeled): {pair_metrics.get('predicted_pairs_labeled', 0)} (Pairs marked as matches by Senzing.)")
    lines.append(f"- Ground-truth pairs (labeled): {pair_metrics.get('ground_truth_pairs_labeled', 0)} (Pairs that are truly correct in sample labels.)")
    lines.append(f"- Labeled records in export: {data_quality.get('labeled_records_in_export', 0)} (Exported records that include `SOURCE_IPG_ID`.)")
    lines.append(f"- Rows with SOURCE_IPG_ID in input: {data_quality.get('rows_with_source_ipg_id', 0)} (Input rows usable for labeled-quality evaluation.)")
    lines.append("")
    lines.append("## Cluster Size Distribution (Labeled Records)")
    lines.append("")
    lines.append("Shows how many resolved entities were built with 1, 2, 3, 4... labeled records.")
    lines.append("")
    lines.append(f"- Entities with labeled records: {distribution_metrics.get('entities_with_labeled_records', 0)}")
    lines.append(f"- Largest labeled entity size: {distribution_metrics.get('largest_labeled_entity_size', 0)}")
    lines.append("")
    lines.append("| Entity Size (records) | Entities Count |")
    lines.append("| ---: | ---: |")
    size_dist = distribution_metrics.get("entity_size_distribution", {}) or {}
    if size_dist:
        for size, count in sorted(size_dist.items(), key=lambda item: int(item[0])):
            lines.append(f"| {size} | {count} |")
    else:
        lines.append("| 0 | 0 |")

    lines.append("")
    lines.append("## Pairings Distribution by Entity")
    lines.append("")
    lines.append("Shows how many entities generated 1 pairing (size 2), 3 pairings (size 3), 6 pairings (size 4), etc.")
    lines.append("")
    lines.append("| Pairings Inside Entity | Entities Count |")
    lines.append("| ---: | ---: |")
    pairings_dist = distribution_metrics.get("entity_pairings_distribution", {}) or {}
    if pairings_dist:
        for pairings, count in sorted(pairings_dist.items(), key=lambda item: int(item[0])):
            lines.append(f"| {pairings} | {count} |")
    else:
        lines.append("| 0 | 0 |")

    lines.append("")
    lines.append("## Per-Record Pairing Degree Distribution")
    lines.append("")
    lines.append("For each record, degree means how many other records it is grouped with in the same resolved entity.")
    lines.append("")
    lines.append("| Pairings Per Record | Records Count |")
    lines.append("| ---: | ---: |")
    degree_dist = distribution_metrics.get("record_pairing_degree_distribution", {}) or {}
    if degree_dist:
        for degree, count in sorted(degree_dist.items(), key=lambda item: int(item[0])):
            lines.append(f"| {degree} | {count} |")
    else:
        lines.append("| 0 | 0 |")

    quality_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return quality_json, quality_md


def resolve_generation_summary_for_input(
    repo_root: Path,
    input_jsonl_path: Path,
) -> dict[str, str | None]:
    """Resolve generation summary metadata matching the run input JSONL."""
    registry_dir = resolve_registry_dir(repo_root)
    if not registry_dir.exists():
        return {
            "generation_summary_json": None,
            "base_input_json": None,
            "mapped_output_jsonl": None,
        }

    input_path_text = str(input_jsonl_path)
    input_name = input_jsonl_path.name

    for summary_path in sorted(registry_dir.glob("generation_summary_*.json"), reverse=True):
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
    registry_dir = resolve_registry_dir(repo_root)
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
    lines.append(f"- Generated at: {summary_obj['generated_at']} (report generation time).")
    lines.append(f"- Records input: {records_input_count} (records read from input file).")
    lines.append(
        f"- Records exported: {len(export_rows)} "
        "(rows produced by `sz_export`; can be higher than input due to export row structure)."
    )
    lines.append(f"- Resolved entities: {len(entity_ids)} (final entities resolved by Senzing).")
    lines.append(f"- Matched records: {len(matched_records)} (records that have at least one match).")
    lines.append(f"- Matched pairs: {len(matched_pairs)} (matched record pairs).")
    lines.append(
        "- Explain coverage: "
        f"whyEntity {summary_obj['explain_coverage']['why_entity_ok']}/{summary_obj['explain_coverage']['why_entity_total']}, "
        f"whyRecords {summary_obj['explain_coverage']['why_records_ok']}/{summary_obj['explain_coverage']['why_records_total']} "
        "(how many explain requests succeeded)."
    )
    lines.append("")
    lines.append("## Top Match Keys")
    lines.append("")
    lines.append("Shows which signal combinations (for example `NAME+DOB`) generated the most matches.")
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
    lines.append("Distribution of numeric match levels produced by Senzing.")
    lines.append("")
    lines.append("| Match Level | Count |")
    lines.append("| --- | ---: |")
    if match_level_counts:
        for level, count in sorted(match_level_counts.items()):
            lines.append(f"| {level} | {count} |")
    else:
        lines.append("| 0 | 0 |")

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


def stream_export_to_comparison_outputs(
    run_dir: Path,
    logs_dir: Path,
    project_setup_env: Path,
    input_jsonl_path: Path,
    records_input_count: int,
    timeout_seconds: int | None,
    engine_config_json: str | None = None,
    license_string: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Stream sz_export directly into comparison artifacts, avoiding large export CSV files."""
    comparison_dir = run_dir / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)
    entity_records_csv = comparison_dir / "entity_records.csv"
    matched_pairs_csv = comparison_dir / "matched_pairs.csv"
    match_stats_csv = comparison_dir / "match_key_stats.csv"
    management_json = comparison_dir / "management_summary.json"
    management_md = comparison_dir / "management_summary.md"
    export_log_path = logs_dir / "04_export.log"

    export_cmd = (
        build_shell_prefix(
            project_setup_env,
            engine_config_json=engine_config_json,
            license_string=license_string,
        )
        + "sz_export -o /dev/stdout"
    )

    started = time.time()
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        ["bash", "-lc", export_cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    records_exported = 0
    resolved_entities = 0
    matched_records = 0
    matched_pairs = 0
    match_key_counts: Counter[str] = Counter()
    match_level_counts: Counter[int] = Counter()
    first_record_by_entity: dict[str, tuple[str, str]] = {}
    anchor_by_entity: dict[str, tuple[str, str]] = {}

    timed_out = False
    parse_error: str | None = None
    stderr_text = ""

    try:
        if process.stdout is None:
            raise RuntimeError("sz_export stdout stream is not available.")

        sample_lines: list[str] = []
        sample_bytes = 0
        while len(sample_lines) < 32 and sample_bytes < 16384:
            line = process.stdout.readline()
            if line == "":
                break
            sample_lines.append(line)
            sample_bytes += len(line)
            if len(sample_lines) >= 2 and sample_bytes >= 2048:
                break
            if timeout_seconds is not None and (time.time() - started) > timeout_seconds:
                timed_out = True
                break

        if not timed_out and not sample_lines:
            parse_error = "sz_export produced no output rows."
        else:
            sniff_sample = "".join(sample_lines)
            try:
                dialect = csv.Sniffer().sniff(sniff_sample, delimiters=",;\t|")
            except csv.Error:
                dialect = csv.excel

            line_iter = itertools.chain(sample_lines, process.stdout)
            reader = csv.DictReader(line_iter, dialect=dialect)
            with entity_records_csv.open("w", encoding="utf-8", newline="") as entity_out, matched_pairs_csv.open(
                "w", encoding="utf-8", newline=""
            ) as pairs_out:
                entity_writer = csv.DictWriter(
                    entity_out,
                    fieldnames=[
                        "resolved_entity_id",
                        "data_source",
                        "record_id",
                        "match_level",
                        "match_key",
                        "is_anchor",
                        "why_entity_ok",
                        "why_entity_reason_summary",
                    ],
                )
                pair_writer = csv.DictWriter(
                    pairs_out,
                    fieldnames=[
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
                )
                entity_writer.writeheader()
                pair_writer.writeheader()

                for raw_row in reader:
                    if timeout_seconds is not None and (time.time() - started) > timeout_seconds:
                        timed_out = True
                        break
                    row = normalize_export_row(raw_row)
                    if not row:
                        continue
                    entity_id = row.get("RESOLVED_ENTITY_ID", "")
                    data_source = row.get("DATA_SOURCE", "")
                    record_id = row.get("RECORD_ID", "")
                    match_level = parse_int(row.get("MATCH_LEVEL", "0"), fallback=0)
                    match_key = row.get("MATCH_KEY", "")

                    if not entity_id or not data_source or not record_id:
                        continue

                    records_exported += 1
                    if entity_id not in first_record_by_entity:
                        first_record_by_entity[entity_id] = (data_source, record_id)
                        resolved_entities += 1
                    if match_level == 0 and entity_id not in anchor_by_entity:
                        anchor_by_entity[entity_id] = (data_source, record_id)

                    entity_writer.writerow(
                        {
                            "resolved_entity_id": entity_id,
                            "data_source": data_source,
                            "record_id": record_id,
                            "match_level": match_level,
                            "match_key": match_key,
                            "is_anchor": 1 if match_level == 0 else 0,
                            "why_entity_ok": 0,
                            "why_entity_reason_summary": "",
                        }
                    )

                    if match_level <= 0:
                        continue

                    matched_records += 1
                    anchor = anchor_by_entity.get(entity_id) or first_record_by_entity.get(entity_id)
                    if not anchor:
                        continue
                    anchor_ds, anchor_rid = anchor
                    if anchor_ds == data_source and anchor_rid == record_id:
                        continue

                    matched_pairs += 1
                    pair_writer.writerow(
                        {
                            "resolved_entity_id": entity_id,
                            "anchor_data_source": anchor_ds,
                            "anchor_record_id": anchor_rid,
                            "matched_data_source": data_source,
                            "matched_record_id": record_id,
                            "match_level": match_level,
                            "match_key": match_key,
                            "why_records_ok": 0,
                            "why_records_reason_summary": "",
                        }
                    )
                    if match_key:
                        match_key_counts[match_key] += 1
                    match_level_counts[match_level] += 1
    finally:
        try:
            if timed_out and process.poll() is None:
                process.kill()
        except Exception:
            pass
        if process.stderr is not None:
            stderr_text = process.stderr.read()

    if not timed_out:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            timed_out = True

    exit_code = process.returncode if process.returncode is not None else 1
    duration = round(time.time() - started, 3)

    log_lines = [
        "STEP: export",
        f"COMMAND: {export_cmd}",
        f"EXIT_CODE: {exit_code}",
        f"TIMED_OUT: {timed_out}",
        f"TIMEOUT_SECONDS: {timeout_seconds if timeout_seconds is not None else 'none'}",
        f"DURATION_SECONDS: {duration}",
        "",
        "--- STREAM COUNTS ---",
        f"records_exported={records_exported}",
        f"resolved_entities={resolved_entities}",
        f"matched_records={matched_records}",
        f"matched_pairs={matched_pairs}",
        "",
        "--- STDERR ---",
        stderr_text,
    ]
    if parse_error:
        log_lines.extend(["", f"PARSE_ERROR: {parse_error}"])
    export_log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    step = {
        "step": "export",
        "ok": (exit_code == 0) and (not timed_out) and parse_error is None,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "log_file": str(export_log_path),
        "stdout_tail": (
            f"records_exported={records_exported}, resolved_entities={resolved_entities}, "
            f"matched_records={matched_records}, matched_pairs={matched_pairs}"
        )[-1200:],
        "stderr_tail": stderr_text[-1200:],
        "mode": "stream",
    }
    if not step["ok"]:
        if parse_error:
            step["stderr_tail"] = f"{step['stderr_tail']}\n{parse_error}".strip()[-1200:]
        return step, {}

    stats_rows = [
        {"metric": "records_input", "value": records_input_count},
        {"metric": "records_exported", "value": records_exported},
        {"metric": "resolved_entities", "value": resolved_entities},
        {"metric": "matched_records", "value": matched_records},
        {"metric": "matched_pairs", "value": matched_pairs},
    ]
    for level, count in sorted(match_level_counts.items()):
        stats_rows.append({"metric": f"match_level_{level}", "value": count})
    for key, count in sorted(match_key_counts.items(), key=lambda x: (-x[1], x[0])):
        stats_rows.append({"metric": f"match_key::{key}", "value": count})
    write_csv(match_stats_csv, ["metric", "value"], stats_rows)

    ground_truth_payload = build_ground_truth_match_quality_from_entity_csv(
        input_jsonl_path=input_jsonl_path,
        entity_records_csv=entity_records_csv,
    )
    ground_truth_json, ground_truth_md = write_ground_truth_match_quality_reports(
        comparison_dir=comparison_dir,
        payload=ground_truth_payload,
    )

    summary_obj = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "records_input": records_input_count,
        "records_exported": records_exported,
        "resolved_entities": resolved_entities,
        "matched_records": matched_records,
        "matched_pairs": matched_pairs,
        "match_level_distribution": {str(k): v for k, v in sorted(match_level_counts.items())},
        "match_key_distribution": dict(sorted(match_key_counts.items(), key=lambda x: (-x[1], x[0]))),
        "explain_coverage": {
            "why_entity_total": 0,
            "why_entity_ok": 0,
            "why_records_total": 0,
            "why_records_ok": 0,
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
    lines.append(f"- Generated at: {summary_obj['generated_at']} (report generation time).")
    lines.append(f"- Records input: {records_input_count} (records read from input file).")
    lines.append(
        f"- Records exported: {records_exported} "
        "(rows produced by `sz_export`; can be higher than input due to export row structure)."
    )
    lines.append(f"- Resolved entities: {resolved_entities} (final entities resolved by Senzing).")
    lines.append(f"- Matched records: {matched_records} (records that have at least one match).")
    lines.append(f"- Matched pairs: {matched_pairs} (matched record pairs).")
    lines.append(
        "- Explain coverage: "
        "whyEntity 0/0, whyRecords 0/0 (explain not executed in stream-export mode)."
    )
    lines.append("")
    lines.append("## Top Match Keys")
    lines.append("")
    lines.append("Shows which signal combinations (for example `NAME+DOB`) generated the most matches.")
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
    lines.append("Distribution of numeric match levels produced by Senzing.")
    lines.append("")
    lines.append("| Match Level | Count |")
    lines.append("| --- | ---: |")
    if match_level_counts:
        for level, count in sorted(match_level_counts.items()):
            lines.append(f"| {level} | {count} |")
    else:
        lines.append("| 0 | 0 |")
    management_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return step, {
        "comparison_dir": str(comparison_dir),
        "entity_records_csv": str(entity_records_csv),
        "matched_pairs_csv": str(matched_pairs_csv),
        "match_stats_csv": str(match_stats_csv),
        "management_summary_json": str(management_json),
        "management_summary_md": str(management_md),
        "ground_truth_match_quality_json": str(ground_truth_json),
        "ground_truth_match_quality_md": str(ground_truth_md),
        "resolved_entities": resolved_entities,
        "matched_records_count": matched_records,
        "matched_pairs_count": matched_pairs,
        "records_exported": records_exported,
    }


def main() -> int:
    """Entry point."""
    args = parse_args()
    repo_root = detect_repo_root(Path(__file__))
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
    if args.load_chunk_size < 0:
        print("ERROR: --load-chunk-size must be >= 0", file=sys.stderr)
        return 2
    if args.load_batch_size < 0:
        print("ERROR: --load-batch-size must be >= 0", file=sys.stderr)
        return 2
    if args.max_failed_files < 0:
        print("ERROR: --max-failed-files must be >= 0", file=sys.stderr)
        return 2
    if args.load_file_timeout_seconds < 0:
        print("ERROR: --load-file-timeout-seconds must be >= 0", file=sys.stderr)
        return 2
    if args.snapshot_threads <= 0 or args.snapshot_fallback_threads <= 0:
        print("ERROR: --snapshot-threads and --snapshot-fallback-threads must be > 0", file=sys.stderr)
        return 2
    if args.enable_load_chunk_fallback and args.load_chunk_size == 0:
        args.load_chunk_size = 50_000

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

    license_source = None
    license_string = os.environ.get(LICENSE_STRING_ENV, "").strip() or None
    if args.license_base64_file:
        license_path = Path(args.license_base64_file).expanduser().resolve()
        license_string = read_license_string_file(license_path)
        if not license_string:
            print(f"ERROR: --license-base64-file not found or empty: {license_path}", file=sys.stderr)
            return 2
        license_source = str(license_path)
    elif license_string:
        license_source = f"env:{LICENSE_STRING_ENV}"

    if license_string:
        os.environ[LICENSE_STRING_ENV] = license_string

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
    if license_source:
        print(f"License source: {license_source}")

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

    step = create_project(project_dir, base_setup_env, logs_dir / "00_create_project.log", license_string=license_string)
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

    if license_string:
        try:
            embed_license_in_setup_env(project_setup_env, project_dir, license_string)
        except Exception as err:  # pylint: disable=broad-exception-caught
            summary = {
                "overall_ok": False,
                "error": f"unable to persist license into setupEnv: {err}",
                "run_directory": str(run_dir),
                "project_dir": str(project_dir),
                "runtime_warnings": runtime_warnings,
                "steps": steps,
            }
            summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("FAILED updating setupEnv with license", file=sys.stderr)
            return 1

    project_env = load_setup_env(project_setup_env, license_string=license_string)
    if not project_env:
        summary = {
            "overall_ok": False,
            "error": "unable to load project setup environment",
            "run_directory": str(run_dir),
            "project_dir": str(project_dir),
            "runtime_warnings": runtime_warnings,
            "steps": steps,
        }
        summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("FAILED loading setupEnv", file=sys.stderr)
        return 1
    if not license_string:
        runtime_warnings.append("No Senzing license string detected (evaluation limits may apply).")
    runtime_engine_config = None
    project_runtime_flavor = project_env.get("SENZING_PROJECT_FLAVOR", "").strip() or "legacy_cli"

    for index, data_source in enumerate(data_sources, start=1):
        cfg_file = config_scripts_dir / f"add_{data_source}.g2c"
        cfg_file.write_text(f"addDataSource {data_source}\nsave\n", encoding="utf-8")
        command = (
            build_shell_prefix(
                project_setup_env,
                engine_config_json=runtime_engine_config,
                license_string=license_string,
            )
            + f"sz_configtool -f {shlex.quote(str(cfg_file))}"
        )
        step = run_shell_step(
            f"configure_data_source_{data_source}",
            command,
            logs_dir / f"01_configure_{index:02d}_{data_source}.log",
            timeout_seconds=args.step_timeout_seconds,
        )
        if not step["ok"] and command_missing(step):
            step = configure_data_source_modern(
                project_dir=project_dir,
                data_source=data_source,
                log_path=logs_dir / f"01_configure_{index:02d}_{data_source}.log",
                license_string=license_string,
            )
            project_runtime_flavor = "modern_sdk"
            runtime_warnings.append(
                f"configure_data_source_{data_source} used modern SDK fallback."
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

    load_ok = False
    load_batch_count = 0
    load_batch_records_total = 0
    load_batch_success_count = 0
    load_batch_failure_count = 0
    load_batches_dir = run_dir / "load_batches"
    failed_files_dir = run_dir / args.failed_files_output_dir
    failed_files_summary_json = run_dir / "failed_files_summary.json"
    failed_file_entries: list[dict[str, Any]] = []

    if args.load_batch_size > 0:
        expected_files = (records_input_count + args.load_batch_size - 1) // args.load_batch_size
        load_batches_dir.mkdir(parents=True, exist_ok=True)
        print(
            f"File split enabled: {args.load_batch_size} records per file "
            f"(expected files: {expected_files})"
        )

        batch_file: Path | None = None
        batch_writer = None
        batch_records = 0
        batch_index = 0
        batch_failed = False
        abort_due_to_failed_limit = False
        next_row_index = 1

        def process_batch_file(
            current_batch_file: Path,
            current_batch_index: int,
            current_batch_records: int,
            row_start: int,
            row_end: int,
        ) -> bool:
            nonlocal load_batch_count, load_batch_success_count, load_batch_failure_count, abort_due_to_failed_limit
            print(
                f"[LOAD] Starting file {current_batch_index}/{expected_files} "
                f"(rows {row_start:,}-{row_end:,}, {current_batch_records} records): {current_batch_file.name}"
            )
            started_at = time.time()
            batch_ok, batch_steps, batch_warnings, removed = run_load_attempts_for_file(
                project_setup_env=project_setup_env,
                load_input_jsonl=current_batch_file,
                logs_dir=logs_dir,
                step_timeout_seconds=args.step_timeout_seconds,
                load_file_timeout_seconds=(args.load_file_timeout_seconds or None),
                load_threads=args.load_threads,
                load_fallback_threads=args.load_fallback_threads,
                load_no_shuffle_primary=args.load_no_shuffle_primary,
                disable_stability_retries=args.disable_stability_retries,
                enable_load_chunk_fallback=args.enable_load_chunk_fallback,
                load_chunk_size=args.load_chunk_size,
                chunk_dir=run_dir / "load_chunks" / f"batch_{current_batch_index:05d}",
                engine_config_json=runtime_engine_config,
                license_string=license_string,
                keep_load_chunk_files=args.keep_load_chunk_files,
                keep_loader_temp_files=args.keep_loader_temp_files,
                step_name_prefix=f"load_records_batch_{current_batch_index:05d}",
                log_name_prefix=f"02_load_batch_{current_batch_index:05d}",
            )
            steps.extend(batch_steps)
            runtime_warnings.extend(batch_warnings)
            loader_temp_files_removed.extend(removed)
            elapsed_seconds = round(time.time() - started_at, 1)
            load_batch_count += 1

            if batch_ok:
                load_batch_success_count += 1
                print(
                    f"[LOAD] Loaded file {current_batch_index}/{expected_files} successfully "
                    f"(rows {row_start:,}-{row_end:,}) in {elapsed_seconds:.1f} seconds"
                )
                if (not args.keep_load_batch_files) and current_batch_file.exists():
                    try:
                        current_batch_file.unlink()
                    except OSError:
                        runtime_warnings.append(f"Unable to delete batch file: {current_batch_file}")
                return True

            load_batch_failure_count += 1
            failed_step = next((item for item in reversed(batch_steps) if not item.get("ok")), None)
            failure_tail = ""
            if failed_step:
                failure_tail = str(
                    failed_step.get("stderr_tail") or failed_step.get("stdout_tail") or ""
                ).strip()
            if len(failure_tail) > 400:
                failure_tail = failure_tail[:397] + "..."

            quarantine_path = None
            try:
                failed_files_dir.mkdir(parents=True, exist_ok=True)
                quarantine_path = (
                    failed_files_dir
                    / f"failed_file_{current_batch_index:05d}_rows_{row_start}_{row_end}.jsonl"
                )
                if current_batch_file.exists():
                    shutil.copy2(current_batch_file, quarantine_path)
            except OSError as err:
                runtime_warnings.append(
                    f"Unable to copy failed file {current_batch_file} to quarantine ({err})."
                )
                quarantine_path = None

            failed_entry = {
                "file_index": current_batch_index,
                "expected_files": expected_files,
                "rows_start": row_start,
                "rows_end": row_end,
                "records": current_batch_records,
                "source_file": str(current_batch_file),
                "quarantine_file": str(quarantine_path) if quarantine_path else None,
                "elapsed_seconds": elapsed_seconds,
                "failure_tail": failure_tail,
            }
            failed_file_entries.append(failed_entry)

            print(
                f"[LOAD] FAILED at file {current_batch_index}/{expected_files} "
                f"(rows {row_start:,}-{row_end:,}) after {elapsed_seconds:.1f} seconds"
            )
            if quarantine_path:
                print(f"[LOAD] Failed file quarantined at: {quarantine_path}")

            if args.continue_on_failed_file:
                runtime_warnings.append(
                    f"Continuing after failed file {current_batch_index}/{expected_files} "
                    f"(rows {row_start:,}-{row_end:,})."
                )
                if args.max_failed_files > 0 and load_batch_failure_count >= args.max_failed_files:
                    abort_due_to_failed_limit = True
                    runtime_warnings.append(
                        f"Max failed files limit reached ({args.max_failed_files}); aborting remaining files."
                    )
            return False

        try:
            with load_input_jsonl.open("r", encoding="utf-8", errors="replace") as infile:
                for line in infile:
                    text = line.strip()
                    if not text:
                        continue
                    if batch_writer is None:
                        batch_index += 1
                        batch_file = load_batches_dir / f"load_batch_{batch_index:05d}.jsonl"
                        batch_writer = batch_file.open("w", encoding="utf-8")
                        batch_records = 0

                    batch_writer.write(text + "\n")
                    batch_records += 1
                    load_batch_records_total += 1

                    if batch_records >= args.load_batch_size:
                        batch_writer.close()
                        batch_writer = None

                        row_start = next_row_index
                        row_end = next_row_index + batch_records - 1
                        next_row_index = row_end + 1

                        if not process_batch_file(batch_file, batch_index, batch_records, row_start, row_end):
                            if args.continue_on_failed_file and not abort_due_to_failed_limit:
                                continue
                            batch_failed = True
                            break

                if batch_writer is not None and batch_file is not None:
                    batch_writer.close()
                    batch_writer = None
                    row_start = next_row_index
                    row_end = next_row_index + batch_records - 1
                    next_row_index = row_end + 1
                    if not process_batch_file(batch_file, batch_index, batch_records, row_start, row_end):
                        if not (args.continue_on_failed_file and not abort_due_to_failed_limit):
                            batch_failed = True
        finally:
            if batch_writer is not None:
                batch_writer.close()

        if failed_file_entries:
            failed_payload = {
                "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                "continue_on_failed_file": args.continue_on_failed_file,
                "max_failed_files": args.max_failed_files,
                "failed_file_count": len(failed_file_entries),
                "failed_files": failed_file_entries,
            }
            failed_files_summary_json.write_text(
                json.dumps(failed_payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        if args.continue_on_failed_file:
            load_ok = (not batch_failed) and load_batch_success_count > 0
        else:
            load_ok = (not batch_failed) and load_batch_failure_count == 0 and load_batch_success_count > 0

        if load_ok:
            runtime_warnings.append(
                "Split-file load completed: "
                f"processed={load_batch_count}, success={load_batch_success_count}, "
                f"failed={load_batch_failure_count}, records_seen={load_batch_records_total}."
            )
            if load_batch_failure_count > 0:
                runtime_warnings.append(
                    "Run completed with partial load due to failed files. "
                    f"Review: {failed_files_summary_json}"
                )
    else:
        if args.continue_on_failed_file:
            runtime_warnings.append(
                "--continue-on-failed-file ignored because --load-batch-size is disabled."
            )
        load_ok, load_steps, load_warnings, removed = run_load_attempts_for_file(
            project_setup_env=project_setup_env,
            load_input_jsonl=load_input_jsonl,
            logs_dir=logs_dir,
            step_timeout_seconds=args.step_timeout_seconds,
            load_file_timeout_seconds=(args.load_file_timeout_seconds or None),
            load_threads=args.load_threads,
            load_fallback_threads=args.load_fallback_threads,
            load_no_shuffle_primary=args.load_no_shuffle_primary,
            disable_stability_retries=args.disable_stability_retries,
            enable_load_chunk_fallback=args.enable_load_chunk_fallback,
            load_chunk_size=args.load_chunk_size,
            chunk_dir=run_dir / "load_chunks",
            engine_config_json=runtime_engine_config,
            license_string=license_string,
            keep_load_chunk_files=args.keep_load_chunk_files,
            keep_loader_temp_files=args.keep_loader_temp_files,
            step_name_prefix="load_records",
            log_name_prefix="02_load",
        )
        steps.extend(load_steps)
        runtime_warnings.extend(load_warnings)
        loader_temp_files_removed.extend(removed)

    if not load_ok:
        summary = {
            "overall_ok": False,
            "error": "load_records failed after retries",
            "run_directory": str(run_dir),
            "project_dir": str(project_dir),
            "runtime_warnings": runtime_warnings,
            "failed_files": failed_file_entries,
            "failed_files_summary_json": str(failed_files_summary_json) if failed_files_summary_json.exists() else None,
            "steps": steps,
        }
        summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("FAILED at load_records", file=sys.stderr)
        return 1

    if args.load_batch_size > 0:
        runtime_warnings.append(
            f"Input was split into sequential files for load (file_size={args.load_batch_size})."
        )

    if not args.skip_snapshot:
        snapshot_attempts: list[tuple[str, str, Path]] = [
            (
                "primary",
                build_snapshot_command(
                    project_setup_env,
                    snapshot_prefix,
                    args.snapshot_threads,
                    force_sdk=False,
                    engine_config_json=runtime_engine_config,
                    license_string=license_string,
                ),
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
                        engine_config_json=runtime_engine_config,
                        license_string=license_string,
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
            if command_missing(step):
                step = snapshot_modern(
                    project_dir=project_dir,
                    snapshot_json=snapshot_json,
                    log_path=logs_dir / "03_snapshot.log",
                    license_string=license_string,
                )
                project_runtime_flavor = "modern_sdk"
                runtime_warnings.append("snapshot used modern SDK fallback.")
                steps.append(step)
                snapshot_ok = step["ok"]
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

        if not snapshot_json.exists():
            candidates = sorted(run_dir.glob("snapshot*.json"))
            if candidates:
                candidates[0].replace(snapshot_json)

    use_stream_export = (
        args.stream_export and (not args.skip_export) and args.skip_explain and (not args.skip_comparison)
    )
    if args.stream_export and not use_stream_export:
        runtime_warnings.append(
            "--stream-export requested but requirements not met (needs --skip-explain and comparison enabled); "
            "falling back to file export."
        )
    elif use_stream_export and project_runtime_flavor == "modern_sdk":
        runtime_warnings.append(
            "--stream-export requested under modern SDK runtime; falling back to file export."
        )
        use_stream_export = False

    if use_stream_export:
        step, stream_artifacts = stream_export_to_comparison_outputs(
            run_dir=run_dir,
            logs_dir=logs_dir,
            project_setup_env=project_setup_env,
            input_jsonl_path=load_input_jsonl,
            records_input_count=records_input_count,
            timeout_seconds=args.step_timeout_seconds,
            engine_config_json=runtime_engine_config,
            license_string=license_string,
        )
        steps.append(step)
        if not step["ok"]:
            summary = {
                "overall_ok": False,
                "error": "export failed (stream mode)",
                "run_directory": str(run_dir),
                "project_dir": str(project_dir),
                "runtime_warnings": runtime_warnings,
                "steps": steps,
            }
            summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("FAILED at export (stream mode)", file=sys.stderr)
            return 1
        comparison_artifacts = stream_artifacts
        runtime_warnings.append("Export executed in stream mode (no standalone export CSV written).")
    elif not args.skip_export:
        export_cmd = (
            build_shell_prefix(
                project_setup_env,
                engine_config_json=runtime_engine_config,
                license_string=license_string,
            )
            + f"sz_export -o {shlex.quote(str(export_file))}"
        )
        step = run_shell_step(
            "export",
            export_cmd,
            logs_dir / "04_export.log",
            timeout_seconds=args.step_timeout_seconds,
        )
        if not step["ok"] and command_missing(step):
            step = export_csv_modern(
                project_dir=project_dir,
                export_file=export_file,
                log_path=logs_dir / "04_export.log",
                license_string=license_string,
            )
            project_runtime_flavor = "modern_sdk"
            runtime_warnings.append("export used modern SDK fallback.")
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

    need_export_rows = (not use_stream_export) and export_file.exists() and (not args.skip_explain or not args.skip_comparison)
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
    if use_stream_export:
        explain_summary["matched_records_detected"] = int(comparison_artifacts.get("matched_records_count") or 0)
        explain_summary["matched_pairs_detected"] = int(comparison_artifacts.get("matched_pairs_count") or 0)

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

    if (not use_stream_export) and export_rows and not args.skip_comparison:
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
            "load_no_shuffle_primary": args.load_no_shuffle_primary,
            "enable_load_chunk_fallback": args.enable_load_chunk_fallback,
            "load_chunk_size": args.load_chunk_size,
            "keep_load_chunk_files": args.keep_load_chunk_files,
            "load_batch_size": args.load_batch_size,
            "keep_load_batch_files": args.keep_load_batch_files,
            "continue_on_failed_file": args.continue_on_failed_file,
            "max_failed_files": args.max_failed_files,
            "load_file_timeout_seconds": args.load_file_timeout_seconds,
            "load_batch_count": load_batch_count,
            "load_batch_success_count": load_batch_success_count,
            "load_batch_failure_count": load_batch_failure_count,
            "load_batch_records_total": load_batch_records_total,
            "snapshot_threads": args.snapshot_threads,
            "snapshot_fallback_threads": args.snapshot_fallback_threads,
            "fast_mode": args.fast_mode,
            "skip_comparison": args.skip_comparison,
            "stream_export_requested": args.stream_export,
            "stream_export_used": use_stream_export,
            "use_input_jsonl_directly": args.use_input_jsonl_directly,
            "data_sources_override": data_sources_override,
            "keep_loader_temp_files": args.keep_loader_temp_files,
            "stability_retries_enabled": not args.disable_stability_retries,
            "license_string_present": bool(license_string),
            "license_source": license_source,
            "project_runtime_flavor": project_runtime_flavor,
        },
        "runtime_warnings": runtime_warnings,
        "artifacts": {
            "normalized_jsonl": str(normalized_jsonl) if normalized_jsonl.exists() else None,
            "load_input_jsonl": str(load_input_jsonl),
            "loader_temp_files_removed": loader_temp_files_removed,
            "load_batches_dir": str(load_batches_dir) if load_batches_dir.exists() else None,
            "failed_files_dir": str(failed_files_dir) if failed_files_dir.exists() else None,
            "failed_files_summary_json": (
                str(failed_files_summary_json) if failed_files_summary_json.exists() else None
            ),
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
        "failed_files": failed_file_entries,
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

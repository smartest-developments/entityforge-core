#!/usr/bin/env python3
"""Diagnose Senzing pipeline/runtime failures without external tooling.

This script is designed for production environments where AI/interactive support
is unavailable. It inspects latest runtime artifacts and emits:
- a JSON diagnostic payload
- a Markdown report
- a compact TXT summary that can be pasted to support/engineering
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import resource
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

RUN_DIR_RE = re.compile(r"^run_mvp_\d{8}_\d{6}$")
SENZ_CODE_RE = re.compile(r"\b(SENZ\d{4})\b")
RECORD_ID_RE = re.compile(r'"RECORD_ID"\s*:\s*"([^"]+)"')
LOAD_FILE_RE = re.compile(r"sz_file_loader\s+-f\s+('([^']+)'|\"([^\"]+)\"|(\S+))")


def now_timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose core/Senzing runtime failures")
    parser.add_argument(
        "--runtime-dir",
        default=None,
        help="Runtime directory used by pipeline (e.g. /mnt/mvp_runtime). If omitted, auto-detected.",
    )
    parser.add_argument(
        "--run-dir",
        default=None,
        help="Explicit run directory (e.g. /mnt/mvp_runtime/runs/run_mvp_20260304_104022).",
    )
    parser.add_argument(
        "--search-dirs",
        default="/mnt,/tmp,.",
        help="Comma-separated roots to search loader error files and core dumps (default: /mnt,/tmp,.)",
    )
    parser.add_argument(
        "--output-dir",
        default="output/diagnostics",
        help="Output directory for reports (default: output/diagnostics under core root).",
    )
    parser.add_argument(
        "--max-tail-lines",
        type=int,
        default=120,
        help="Tail lines captured per runtime log (default: 120).",
    )
    parser.add_argument(
        "--max-loader-error-files",
        type=int,
        default=8,
        help="Max loader error files to analyze (default: 8).",
    )
    parser.add_argument(
        "--max-sample-records",
        type=int,
        default=200000,
        help="Max JSONL records to sample for distribution diagnostics (default: 200000).",
    )
    parser.add_argument(
        "--max-error-record-samples",
        type=int,
        default=15,
        help="Max failing RECORD_ID samples to include (default: 15).",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def split_paths(raw: str) -> list[Path]:
    values: list[Path] = []
    for token in raw.split(","):
        path = token.strip()
        if not path:
            continue
        values.append(Path(path).expanduser().resolve())
    return values


def latest_by_mtime(paths: list[Path]) -> Path | None:
    existing = [p for p in paths if p.exists()]
    if not existing:
        return None
    existing.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return existing[0]


def detect_runtime_dir(explicit_runtime: str | None) -> Path | None:
    if explicit_runtime:
        path = Path(explicit_runtime).expanduser().resolve()
        return path if path.exists() else None

    candidates: list[Path] = []
    for base in [Path("/mnt"), Path("/tmp"), Path.cwd()]:
        if not base.exists():
            continue
        direct = base / "mvp_runtime"
        if direct.exists():
            candidates.append(direct.resolve())
        candidates.extend([p.resolve() for p in base.glob("mvp_runtime_*") if p.is_dir()])
    return latest_by_mtime(candidates)


def detect_run_dir(explicit_run: str | None, runtime_dir: Path | None) -> Path | None:
    if explicit_run:
        path = Path(explicit_run).expanduser().resolve()
        return path if path.exists() else None

    candidates: list[Path] = []
    if runtime_dir and runtime_dir.exists():
        runs_root = runtime_dir / "runs"
        if runs_root.exists():
            candidates.extend([p for p in runs_root.iterdir() if p.is_dir() and RUN_DIR_RE.match(p.name)])
    return latest_by_mtime(candidates)


def load_log_tail(path: Path, max_tail_lines: int) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) <= max_tail_lines:
        return lines
    return lines[-max_tail_lines:]


def parse_loader_error_files(search_dirs: list[Path], max_files: int) -> dict[str, Any]:
    files: list[Path] = []
    for root in search_dirs:
        if not root.exists():
            continue
        files.extend(root.glob("sz_file_loader_errors_*.log"))
    files = sorted({p.resolve() for p in files}, key=lambda p: p.stat().st_mtime, reverse=True)[:max_files]

    senz_codes: Counter[str] = Counter()
    unique_record_ids: set[str] = set()
    locklist_errors = 0
    flatbuffer_mentions = 0
    file_summaries: list[dict[str, Any]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        codes = SENZ_CODE_RE.findall(text)
        ids = RECORD_ID_RE.findall(text)
        lock_hits = sum(1 for line in lines if "locklist" in line.lower())
        flat_hits = sum(1 for line in lines if "flatbuffer" in line.lower() or "bufferfull" in line.lower())
        senz_codes.update(codes)
        unique_record_ids.update(ids)
        locklist_errors += lock_hits
        flatbuffer_mentions += flat_hits
        file_summaries.append(
            {
                "path": str(path),
                "mtime_iso": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                "size_bytes": path.stat().st_size,
                "lines": len(lines),
                "senz_codes": dict(Counter(codes)),
                "record_ids_found": len(set(ids)),
                "locklist_lines": lock_hits,
                "flatbuffer_lines": flat_hits,
            }
        )

    return {
        "files": [str(p) for p in files],
        "file_summaries": file_summaries,
        "senz_codes": dict(senz_codes),
        "record_ids_count": len(unique_record_ids),
        "record_ids_sample": sorted(unique_record_ids)[:200],
        "locklist_errors": locklist_errors,
        "flatbuffer_mentions": flatbuffer_mentions,
    }


def parse_core_dumps(search_dirs: list[Path]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for root in search_dirs:
        if not root.exists():
            continue
        for path in root.glob("core*"):
            if not path.is_file():
                continue
            name = path.name
            if not name.startswith("core"):
                continue
            items.append(
                {
                    "path": str(path.resolve()),
                    "size_bytes": path.stat().st_size,
                    "mtime_iso": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                }
            )
    items.sort(key=lambda item: item["mtime_iso"], reverse=True)
    return items


def detect_mapped_jsonl(run_summary: dict[str, Any], run_dir: Path, log_tails: dict[str, list[str]]) -> Path | None:
    artifacts = run_summary.get("artifacts")
    if isinstance(artifacts, dict):
        for key in ("load_input_jsonl", "mapped_output_jsonl", "normalized_jsonl"):
            value = str(artifacts.get(key) or "").strip()
            if value:
                path = Path(value).expanduser()
                if path.exists():
                    return path.resolve()
    for lines in log_tails.values():
        for line in lines:
            match = LOAD_FILE_RE.search(line)
            if not match:
                continue
            candidate = match.group(2) or match.group(3) or match.group(4) or ""
            if candidate:
                path = Path(candidate).expanduser()
                if path.exists():
                    return path.resolve()
    fallback = run_dir / "input_normalized.jsonl"
    if fallback.exists():
        return fallback.resolve()
    return None


def profile_mapped_jsonl(path: Path, max_records: int) -> dict[str, Any]:
    if not path.exists():
        return {}

    scanned = 0
    non_empty = 0
    total_bytes = 0
    max_line_bytes = 0
    parse_errors = 0
    missing_record_id = 0
    source_ipg_counter: Counter[str] = Counter()

    with path.open("rb") as infile:
        for raw_line in infile:
            scanned += 1
            if scanned > max_records:
                break
            line = raw_line.strip()
            if not line:
                continue
            non_empty += 1
            line_size = len(line)
            total_bytes += line_size
            max_line_bytes = max(max_line_bytes, line_size)
            try:
                obj = json.loads(line.decode("utf-8", errors="replace"))
            except Exception:
                parse_errors += 1
                continue
            if not isinstance(obj, dict):
                parse_errors += 1
                continue
            record_id = str(obj.get("RECORD_ID") or "").strip()
            if not record_id:
                missing_record_id += 1
            source_ipg = str(obj.get("SOURCE_IPG_ID") or "").strip()
            if source_ipg:
                source_ipg_counter[source_ipg] += 1

    avg_line_bytes = round(total_bytes / non_empty, 2) if non_empty else None
    top_ipg = source_ipg_counter.most_common(10)
    top1 = top_ipg[0][1] if top_ipg else 0
    top1_ratio = round((top1 / non_empty) * 100.0, 4) if non_empty else None

    return {
        "path": str(path),
        "scanned_records": scanned,
        "non_empty_records": non_empty,
        "avg_line_bytes": avg_line_bytes,
        "max_line_bytes": max_line_bytes,
        "parse_errors": parse_errors,
        "missing_record_id": missing_record_id,
        "source_ipg_distinct": len(source_ipg_counter),
        "source_ipg_top10": top_ipg,
        "source_ipg_top1_ratio_pct": top1_ratio,
        "sample_limited": scanned >= max_records,
    }


def collect_error_record_samples(
    mapped_jsonl_path: Path | None,
    failing_record_ids: list[str],
    max_samples: int,
) -> list[dict[str, Any]]:
    if mapped_jsonl_path is None or not mapped_jsonl_path.exists():
        return []
    if not failing_record_ids or max_samples <= 0:
        return []

    target_ids = set(failing_record_ids)
    samples: list[dict[str, Any]] = []
    seen: set[str] = set()
    with mapped_jsonl_path.open("r", encoding="utf-8", errors="replace") as infile:
        for line_no, line in enumerate(infile, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            record_id = str(obj.get("RECORD_ID") or "").strip()
            if not record_id or record_id not in target_ids or record_id in seen:
                continue
            seen.add(record_id)
            samples.append(
                {
                    "line_no": line_no,
                    "record_id": record_id,
                    "source_ipg_id": str(obj.get("SOURCE_IPG_ID") or "").strip() or None,
                    "feature_count": len(obj.get("FEATURES", [])) if isinstance(obj.get("FEATURES"), list) else None,
                    "record": obj,
                }
            )
            if len(samples) >= max_samples:
                break
    return samples


def system_snapshot(paths: list[Path]) -> dict[str, Any]:
    disk: dict[str, Any] = {}
    for path in paths:
        if not path.exists():
            continue
        usage = shutil.disk_usage(path)
        disk[str(path)] = {
            "total_gb": round(usage.total / (1024.0**3), 2),
            "used_gb": round(usage.used / (1024.0**3), 2),
            "free_gb": round(usage.free / (1024.0**3), 2),
        }

    mem: dict[str, Any] = {}
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        values: dict[str, int] = {}
        for line in meminfo.read_text(encoding="utf-8", errors="replace").splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            token = value.strip().split()
            if not token:
                continue
            try:
                values[key] = int(token[0])  # kB
            except ValueError:
                continue
        for key in ("MemTotal", "MemFree", "MemAvailable", "SwapTotal", "SwapFree"):
            if key in values:
                mem[key] = values[key]

    core_soft, core_hard = resource.getrlimit(resource.RLIMIT_CORE)
    return {
        "disk": disk,
        "memory_kb": mem,
        "rlimit_core": {
            "soft": core_soft,
            "hard": core_hard,
        },
    }


def classify_root_causes(payload: dict[str, Any]) -> list[str]:
    causes: list[str] = []
    loader = payload.get("loader_errors", {})
    run_summary = payload.get("run_summary", {})
    log_signatures = payload.get("log_signatures", {})
    mapped_profile = payload.get("mapped_profile", {})

    if loader.get("flatbuffer_mentions", 0) > 0 or log_signatures.get("flatbuffer", 0) > 0:
        causes.append("Memory/buffer pressure during sz_file_loader (flatbuffer allocation failure).")
    if loader.get("locklist_errors", 0) > 0 or log_signatures.get("locklist", 0) > 0:
        causes.append("Resolved-entity lock contention during load (SENZ0010 locklist retries exhausted).")
    if payload.get("core_dumps"):
        causes.append("Native process crash detected (core dump files present).")
    if isinstance(mapped_profile, dict):
        ratio = mapped_profile.get("source_ipg_top1_ratio_pct")
        if isinstance(ratio, (int, float)) and ratio >= 0.5:
            causes.append(
                "High concentration on single SOURCE_IPG_ID in sampled input may amplify load contention."
            )
    if run_summary and run_summary.get("error") == "load_records failed after retries":
        causes.append("Load step failed after primary + fallback attempts.")
    if not causes:
        causes.append("No dominant root-cause signature detected. Inspect load logs and failing RECORD_ID samples.")
    return causes


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# Core Runtime Diagnostic Report")
    lines.append("")
    lines.append(f"- Generated at: {payload['generated_at']}")
    lines.append(f"- Runtime dir: `{summary.get('runtime_dir') or 'N/A'}`")
    lines.append(f"- Run dir: `{summary.get('run_dir') or 'N/A'}`")
    lines.append(f"- Overall ok: `{summary.get('overall_ok')}`")
    lines.append(f"- Failure step: `{summary.get('failure_step') or 'N/A'}`")
    lines.append(f"- Run error: `{summary.get('run_error') or 'N/A'}`")
    lines.append("")
    lines.append("## Probable Root Causes")
    lines.append("")
    for item in payload.get("root_causes", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Loader Errors")
    lines.append("")
    loader = payload.get("loader_errors", {})
    lines.append(f"- Files analyzed: {len(loader.get('files', []))}")
    lines.append(f"- Senz codes: `{loader.get('senz_codes', {})}`")
    lines.append(f"- Locklist lines: {loader.get('locklist_errors', 0)}")
    lines.append(f"- Flatbuffer mentions: {loader.get('flatbuffer_mentions', 0)}")
    lines.append(f"- Unique failing RECORD_ID: {loader.get('record_ids_count', 0)}")
    lines.append("")
    lines.append("## Input Profile")
    lines.append("")
    profile = payload.get("mapped_profile", {})
    if profile:
        lines.append(f"- Input JSONL: `{profile.get('path')}`")
        lines.append(f"- Scanned records: {profile.get('scanned_records')}")
        lines.append(f"- Non-empty records: {profile.get('non_empty_records')}")
        lines.append(f"- Avg line bytes: {profile.get('avg_line_bytes')}")
        lines.append(f"- Max line bytes: {profile.get('max_line_bytes')}")
        lines.append(f"- Missing RECORD_ID: {profile.get('missing_record_id')}")
        lines.append(f"- Distinct SOURCE_IPG_ID: {profile.get('source_ipg_distinct')}")
        lines.append(f"- SOURCE_IPG_ID top1 ratio (%): {profile.get('source_ipg_top1_ratio_pct')}")
    else:
        lines.append("- Input profile unavailable.")
    lines.append("")
    lines.append("## Suggested Next Command")
    lines.append("")
    lines.append("```bash")
    lines.append(payload["suggested_retry_command"])
    lines.append("```")
    lines.append("")
    lines.append("## Copy/Paste Summary")
    lines.append("")
    lines.append("```text")
    lines.extend(payload["compact_summary_lines"])
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_suggested_retry_command(run_payload: dict[str, Any], mapped_jsonl_path: Path | None) -> str:
    input_path = None
    mapping_summary = run_payload.get("mapping_summary", {})
    if isinstance(mapping_summary, dict):
        raw_input = str(mapping_summary.get("input_json") or "").strip()
        if raw_input:
            input_path = raw_input

    if not input_path and mapped_jsonl_path:
        input_path = str(mapped_jsonl_path)

    if not input_path:
        input_path = "/mnt/Senzing-Ready.json"

    return (
        "python3 run_mvp_pipeline.py "
        f"--input-json {input_path} "
        "--execution-mode local "
        "--senzing-env /opt/senzing/er/resources/templates/setupEnv "
        "--runtime-dir /mnt/mvp_runtime "
        "--keep-runtime-dir "
        "--step-timeout-seconds 21600 "
        "--load-threads 1 "
        "--load-fallback-threads 1 "
        "--load-no-shuffle-primary "
        "--stream-export"
    )


def main() -> int:
    args = parse_args()
    mvp_root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir).expanduser()
    if not output_dir.is_absolute():
        output_dir = (mvp_root / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    runtime_dir = detect_runtime_dir(args.runtime_dir)
    run_dir = detect_run_dir(args.run_dir, runtime_dir)
    if run_dir is None:
        print("ERROR: no run directory found. Provide --run-dir or --runtime-dir.", flush=True)
        return 2

    run_summary_path = run_dir / "run_summary.json"
    run_summary = read_json(run_summary_path)
    steps = run_summary.get("steps") if isinstance(run_summary.get("steps"), list) else []

    failure_step = None
    if isinstance(steps, list):
        for item in steps:
            if not isinstance(item, dict):
                continue
            if item.get("ok") is False:
                failure_step = str(item.get("step") or "")
                break

    log_paths: dict[str, Path] = {
        "load_primary": run_dir / "logs" / "02_load.log",
        "load_fallback": run_dir / "logs" / "02_load_retry_1.log",
        "snapshot": run_dir / "logs" / "03_snapshot.log",
        "export": run_dir / "logs" / "04_export.log",
    }
    log_tails = {name: load_log_tail(path, args.max_tail_lines) for name, path in log_paths.items()}

    log_signatures = {
        "flatbuffer": 0,
        "locklist": 0,
        "senz0010": 0,
        "segfault": 0,
    }
    for lines in log_tails.values():
        for line in lines:
            text = line.lower()
            if "flatbuffer" in text or "bufferfull" in text:
                log_signatures["flatbuffer"] += 1
            if "locklist" in text:
                log_signatures["locklist"] += 1
            if "senz0010" in text:
                log_signatures["senz0010"] += 1
            if "segmentation fault" in text or "core dumped" in text:
                log_signatures["segfault"] += 1

    search_dirs = split_paths(args.search_dirs)
    loader_errors = parse_loader_error_files(search_dirs, args.max_loader_error_files)
    core_dumps = parse_core_dumps(search_dirs)

    mapped_jsonl = detect_mapped_jsonl(run_summary, run_dir, log_tails)
    mapped_profile = profile_mapped_jsonl(mapped_jsonl, args.max_sample_records) if mapped_jsonl else {}
    error_record_samples = collect_error_record_samples(
        mapped_jsonl_path=mapped_jsonl,
        failing_record_ids=loader_errors.get("record_ids_sample", []),
        max_samples=args.max_error_record_samples,
    )

    mapping_summary = {}
    if mapped_jsonl:
        for candidate in [mapped_jsonl.parent / "mapping_summary.json", run_dir / "mapping_summary.json"]:
            if candidate.exists():
                mapping_summary = read_json(candidate)
                if mapping_summary:
                    break

    sys_paths: list[Path] = [Path("/"), Path("/mnt"), Path("/tmp"), run_dir]
    if mapped_jsonl:
        sys_paths.append(mapped_jsonl.parent)
    snapshot = system_snapshot([p for p in sys_paths if p.exists()])

    generated_at = dt.datetime.now().isoformat(timespec="seconds")
    summary = {
        "runtime_dir": str(runtime_dir) if runtime_dir else None,
        "run_dir": str(run_dir),
        "run_summary_path": str(run_summary_path),
        "overall_ok": run_summary.get("overall_ok"),
        "failure_step": failure_step,
        "run_error": run_summary.get("error"),
        "mapped_jsonl": str(mapped_jsonl) if mapped_jsonl else None,
    }

    payload: dict[str, Any] = {
        "generated_at": generated_at,
        "summary": summary,
        "run_summary": run_summary,
        "mapping_summary": mapping_summary,
        "log_paths": {name: str(path) for name, path in log_paths.items()},
        "log_tails": log_tails,
        "log_signatures": log_signatures,
        "loader_errors": loader_errors,
        "core_dumps": core_dumps,
        "mapped_profile": mapped_profile,
        "error_record_samples": error_record_samples,
        "system_snapshot": snapshot,
    }

    payload["root_causes"] = classify_root_causes(payload)
    payload["suggested_retry_command"] = build_suggested_retry_command(payload, mapped_jsonl)

    compact_lines = [
        f"RUN_DIR={summary.get('run_dir')}",
        f"OVERALL_OK={summary.get('overall_ok')}",
        f"FAILURE_STEP={summary.get('failure_step')}",
        f"RUN_ERROR={summary.get('run_error')}",
        f"SENZ_CODES={loader_errors.get('senz_codes', {})}",
        f"LOCKLIST_LINES={loader_errors.get('locklist_errors', 0)}",
        f"FLATBUFFER_MENTIONS={loader_errors.get('flatbuffer_mentions', 0)}",
        f"FAILED_RECORD_IDS={loader_errors.get('record_ids_count', 0)}",
        f"FAILED_RECORD_SAMPLES={len(error_record_samples)}",
        f"CORE_DUMPS={len(core_dumps)}",
        f"MAPPED_JSONL={summary.get('mapped_jsonl')}",
        f"INPUT_TOP1_SOURCE_IPG_RATIO_PCT={mapped_profile.get('source_ipg_top1_ratio_pct') if mapped_profile else None}",
        "PROBABLE_CAUSES=" + " | ".join(payload["root_causes"]),
    ]
    payload["compact_summary_lines"] = compact_lines

    stamp = now_timestamp()
    json_path = output_dir / f"runtime_diagnostic_{stamp}.json"
    md_path = output_dir / f"runtime_diagnostic_{stamp}.md"
    txt_path = output_dir / f"runtime_diagnostic_{stamp}.txt"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    txt_path.write_text("\n".join(compact_lines) + "\n", encoding="utf-8")

    print(f"Diagnostic JSON: {json_path}")
    print(f"Diagnostic Markdown: {md_path}")
    print(f"Diagnostic compact TXT: {txt_path}")
    print("")
    print("COPY THIS BLOCK:")
    print("-----8<-----")
    print("\n".join(compact_lines))
    print("----->8-----")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

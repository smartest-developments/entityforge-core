#!/usr/bin/env python3
"""Cleanup utility for core working directories.

Removes generated runtime/output clutter while preserving source scripts and input JSON files.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEFAULT_OUTPUT_KEEP = {".gitkeep"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean generated core runtime/output artifacts.")
    parser.add_argument(
        "--mvp-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="core root directory (default: script directory)",
    )
    parser.add_argument(
        "--runtime-dir",
        default=None,
        help="Optional runtime dir to clean (for example /mnt/mvp_runtime)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without deleting files.",
    )
    return parser.parse_args()


def remove_path(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path, ignore_errors=True)
        return True
    try:
        path.unlink()
        return True
    except OSError:
        return False


def collect_generated_files(mvp_root: Path) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    dirs: list[Path] = []

    # 1) Output run folders and generated files (keep .gitkeep only).
    output_dir = mvp_root / "output"
    if output_dir.exists() and output_dir.is_dir():
        for child in output_dir.iterdir():
            if child.name in DEFAULT_OUTPUT_KEEP:
                continue
            if child.name == "dashboard" and child.is_dir():
                # Keep dashboard source folder; only clean generated dashboard_data if present.
                dashboard_data = child / "dashboard_data"
                if dashboard_data.exists() and dashboard_data.is_dir():
                    dirs.append(dashboard_data)
                continue
            if child.is_dir():
                dirs.append(child)
            else:
                files.append(child)

    # 2) Python cache directories.
    for cache_dir in mvp_root.rglob("__pycache__"):
        if ".git" in cache_dir.parts:
            continue
        dirs.append(cache_dir)

    # 3) Generated JSONL and loader/core artifacts.
    for pattern in [
        "**/*.jsonl",
        "**/sz_file_loader_errors_*.log",
        "**/core*",
        "**/.DS_Store",
    ]:
        for path in mvp_root.glob(pattern):
            if not path.exists() or path.is_dir():
                continue
            if ".git" in path.parts:
                continue
            files.append(path)

    # Deduplicate while keeping stable order.
    dedup_files = list(dict.fromkeys(files))
    dedup_dirs = list(dict.fromkeys(dirs))
    return dedup_files, dedup_dirs


def clean_runtime_dir(runtime_dir: Path, dry_run: bool) -> tuple[int, int]:
    removed_files = 0
    removed_dirs = 0
    if not runtime_dir.exists() or not runtime_dir.is_dir():
        return removed_files, removed_dirs

    for child in runtime_dir.iterdir():
        if child.is_dir():
            if remove_path(child, dry_run=dry_run):
                removed_dirs += 1
        else:
            if remove_path(child, dry_run=dry_run):
                removed_files += 1
    return removed_files, removed_dirs


def main() -> int:
    args = parse_args()
    mvp_root = Path(args.mvp_root).expanduser().resolve()
    if not mvp_root.exists() or not mvp_root.is_dir():
        print(f"ERROR: invalid --mvp-root: {mvp_root}")
        return 2

    files, dirs = collect_generated_files(mvp_root)

    removed_files = 0
    removed_dirs = 0

    # Remove files first, then directories.
    for file_path in files:
        if remove_path(file_path, dry_run=args.dry_run):
            removed_files += 1
    # Deepest dirs first.
    for dir_path in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        if remove_path(dir_path, dry_run=args.dry_run):
            removed_dirs += 1

    runtime_msg = "not requested"
    if args.runtime_dir:
        runtime_dir = Path(args.runtime_dir).expanduser().resolve()
        rt_files, rt_dirs = clean_runtime_dir(runtime_dir, dry_run=args.dry_run)
        removed_files += rt_files
        removed_dirs += rt_dirs
        runtime_msg = str(runtime_dir)

    mode = "DRY-RUN" if args.dry_run else "CLEANUP"
    print(f"[{mode}] core root: {mvp_root}")
    print(f"[{mode}] Runtime dir: {runtime_msg}")
    print(f"[{mode}] Removed files: {removed_files}")
    print(f"[{mode}] Removed directories: {removed_dirs}")
    print("[CLEANUP] Source JSON files are preserved. Generated JSONL files are removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

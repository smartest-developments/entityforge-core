#!/usr/bin/env python3
"""Wrapper for Senzing end-to-end run script.

This wrapper keeps the workflow organized while delegating implementation to the
canonical all-in-one script in senzing/all_in_one.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    target = repo_root / "senzing" / "all_in_one" / "run_senzing_end_to_end.py"

    if not target.exists():
        print(f"ERROR: Target e2e script not found: {target}", file=sys.stderr)
        return 2

    command = [sys.executable, str(target), *sys.argv[1:]]
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

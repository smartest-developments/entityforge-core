#!/usr/bin/env python3
"""Wrapper for production->Senzing JSONL mapping script.

This wrapper keeps the workflow organized while delegating implementation to the
canonical mapper script in senzing/tools.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    target = repo_root / "senzing" / "tools" / "partner_json_to_senzing.py"

    if not target.exists():
        print(f"ERROR: Target mapper script not found: {target}", file=sys.stderr)
        return 2

    command = [sys.executable, str(target), *sys.argv[1:]]
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate Senzing audit input files and optionally run snapshot+audit."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

from record_cluster_exports import iter_record_cluster_rows


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create both CSV inputs needed for production comparison and, when a "
            "Senzing project is supplied, run sz_snapshot -A plus sz_audit."
        )
    )
    parser.add_argument("input_json", help="Input JSON/JSONL file path")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Target directory for generated files. Default: <input_dir>/<input_stem>__senzing_audit",
    )
    parser.add_argument(
        "--data-source",
        default="PARTNERS",
        help="DATA_SOURCE value used by the mapper (default: PARTNERS)",
    )
    parser.add_argument(
        "--array-key",
        default=None,
        help="Optional key if input root is an object containing an array",
    )
    parser.add_argument(
        "--fuzzy-cutoff",
        type=float,
        default=0.90,
        help="Fuzzy key match threshold between 0 and 1 (default: 0.90)",
    )
    parser.add_argument(
        "--scan-records",
        type=int,
        default=500,
        help="Max number of input records used for field-map inference (default: 500)",
    )
    parser.add_argument(
        "--skip-empty-cluster-id",
        action="store_true",
        help="Skip rows where IPG ID is missing or empty",
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Existing Senzing project directory containing setupEnv and bin/sz_snapshot, bin/sz_audit",
    )
    parser.add_argument(
        "--audit-bin",
        default=None,
        help="Optional explicit path to sz_audit (used with --snapshot-csv if no --project-dir is supplied)",
    )
    parser.add_argument(
        "--snapshot-csv",
        default=None,
        help="Use an existing snapshot CSV instead of generating one from --project-dir",
    )
    parser.add_argument(
        "--snapshot-prefix",
        default="truthset_snapshot",
        help="Output file root for sz_snapshot inside --output-dir (default: truthset_snapshot)",
    )
    parser.add_argument(
        "--audit-output-root",
        default="truthset_audit",
        help="Output file root for sz_audit inside --output-dir (default: truthset_audit)",
    )
    parser.add_argument(
        "--snapshot-threads",
        type=int,
        default=1,
        help="Thread count passed to sz_snapshot (default: 1)",
    )
    return parser


def default_output_dir(input_path: Path) -> Path:
    return input_path.parent / f"{input_path.stem}__senzing_audit"


def load_setup_env(setup_env_path: Path) -> dict[str, str]:
    shell_command = f"source {shlex.quote(str(setup_env_path))} >/dev/null 2>&1; env -0"
    result = subprocess.run(
        ["/bin/zsh", "-c", shell_command],
        capture_output=True,
        text=False,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Unable to source setupEnv: {setup_env_path}")

    env_map = dict(os.environ)
    for item in result.stdout.split(b"\x00"):
        if not item or b"=" not in item:
            continue
        key, value = item.split(b"=", 1)
        env_map[key.decode("utf-8", errors="replace")] = value.decode("utf-8", errors="replace")
    return env_map


def run_command(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print("Running:", " ".join(shlex.quote(part) for part in cmd))
    result = subprocess.run(cmd, env=env, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_path = Path(args.input_json).expanduser().resolve()
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    if not 0.0 <= args.fuzzy_cutoff <= 1.0:
        print("ERROR: --fuzzy-cutoff must be between 0 and 1", file=sys.stderr)
        return 2

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else default_output_dir(input_path).resolve()
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    simple_csv = output_dir / "record_id_cluster_id.csv"
    truthset_key_csv = output_dir / "truthset_key.csv"

    written_simple = 0
    written_truth = 0
    skipped_rows = 0

    try:
        row_iter, ipg_source_key = iter_record_cluster_rows(
            input_path=input_path,
            array_key=args.array_key,
            fuzzy_cutoff=args.fuzzy_cutoff,
            scan_records=args.scan_records,
            data_source=args.data_source,
        )
        with simple_csv.open("w", encoding="utf-8", newline="") as simple_out, truthset_key_csv.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as truth_out:
            simple_writer = csv.writer(simple_out)
            truth_writer = csv.writer(truth_out)
            simple_writer.writerow(["record_id", "cluster_id"])
            truth_writer.writerow(["DATA_SOURCE", "RECORD_ID", "CLUSTER_ID"])

            for row in row_iter:
                if args.skip_empty_cluster_id and not row.cluster_id:
                    skipped_rows += 1
                    continue
                simple_writer.writerow([row.record_id, row.cluster_id or ""])
                truth_writer.writerow([row.data_source, row.record_id, row.cluster_id or ""])
                written_simple += 1
                written_truth += 1
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Unable to prepare audit inputs: {err}", file=sys.stderr)
        return 2

    project_dir = Path(args.project_dir).expanduser().resolve() if args.project_dir else None
    audit_bin = Path(args.audit_bin).expanduser().resolve() if args.audit_bin else None
    if audit_bin is None and project_dir is not None:
        audit_bin = project_dir / "bin" / "sz_audit"

    snapshot_csv: Path | None = None
    audit_csv: Path | None = None
    audit_json: Path | None = None

    try:
        if args.snapshot_csv:
            snapshot_csv = Path(args.snapshot_csv).expanduser().resolve()
            if not snapshot_csv.exists():
                raise FileNotFoundError(f"Snapshot CSV not found: {snapshot_csv}")
        elif project_dir:
            setup_env = project_dir / "setupEnv"
            snapshot_bin = project_dir / "bin" / "sz_snapshot"
            missing = [str(path) for path in (setup_env, snapshot_bin, audit_bin) if not path.exists()]
            if missing:
                raise FileNotFoundError("Missing required project files:\n" + "\n".join(f"- {item}" for item in missing))

            project_env = load_setup_env(setup_env)
            snapshot_root = output_dir / args.snapshot_prefix
            snapshot_csv = snapshot_root.with_suffix(".csv")
            run_command(
                [
                    str(snapshot_bin),
                    "-A",
                    "-Q",
                    "-o",
                    str(snapshot_root),
                    "-t",
                    str(args.snapshot_threads),
                ],
                env=project_env,
            )
            if not snapshot_csv.exists():
                raise FileNotFoundError(f"Expected snapshot CSV not found: {snapshot_csv}")

        if snapshot_csv and audit_bin:
            audit_root = output_dir / args.audit_output_root
            audit_csv = audit_root.with_suffix(".csv")
            audit_json = audit_root.with_suffix(".json")
            run_command(
                [
                    str(audit_bin),
                    "-n",
                    str(snapshot_csv),
                    "-p",
                    str(truthset_key_csv),
                    "-o",
                    str(audit_root),
                ]
            )
            missing_outputs = [str(path) for path in (audit_csv, audit_json) if not path.exists()]
            if missing_outputs:
                raise FileNotFoundError(
                    "sz_audit finished without producing expected files:\n" + "\n".join(f"- {item}" for item in missing_outputs)
                )
        elif snapshot_csv and not audit_bin and project_dir:
            raise RuntimeError("Unable to resolve sz_audit path from --project-dir")
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Snapshot/audit step failed: {err}", file=sys.stderr)
        return 1

    manifest = {
        "input_json": str(input_path),
        "output_dir": str(output_dir),
        "ipg_source_key": ipg_source_key or None,
        "record_cluster_csv": str(simple_csv),
        "truthset_key_csv": str(truthset_key_csv),
        "written_rows": written_simple,
        "skipped_rows": skipped_rows,
        "snapshot_csv": str(snapshot_csv) if snapshot_csv else None,
        "audit_csv": str(audit_csv) if audit_csv else None,
        "audit_json": str(audit_json) if audit_json else None,
    }
    manifest_path = output_dir / "audit_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Input file: {input_path}")
    print(f"Output directory: {output_dir}")
    print(f"Inferred IPG source key: {ipg_source_key or '<NOT_FOUND>'}")
    print(f"Simple CSV: {simple_csv}")
    print(f"Truthset key CSV: {truthset_key_csv}")
    if snapshot_csv:
        print(f"Snapshot CSV: {snapshot_csv}")
    if audit_csv:
        print(f"Audit CSV: {audit_csv}")
    if audit_json:
        print(f"Audit JSON: {audit_json}")
    print(f"Written rows: {written_simple}")
    print(f"Skipped rows: {skipped_rows}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

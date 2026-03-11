#!/usr/bin/env python3
"""Generate Senzing audit input files and optionally run snapshot+audit."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shlex
import shutil
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
    parser.add_argument("input_json", nargs="?", default=None, help="Input JSON/JSONL file path")
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


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def candidate_runtime_roots(project_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    for root in [project_dir.parent.parent, *project_dir.parents]:
        if root not in candidates:
            candidates.append(root)
    return candidates


def to_host_path(raw_path: str | Path, project_dir: Path) -> Path:
    raw = str(raw_path).strip()
    repo_root = resolve_repo_root()
    runtime_roots = candidate_runtime_roots(project_dir)
    runtime_root = runtime_roots[0] if runtime_roots else project_dir.parent.parent
    if raw.startswith("/runtime/"):
        return (runtime_root / raw.removeprefix("/runtime/")).resolve()
    if raw.startswith("/workspace/"):
        return (repo_root / raw.removeprefix("/workspace/")).resolve()
    return Path(raw).expanduser().resolve()


def discover_run_summary(project_dir: Path) -> tuple[Path | None, dict | None]:
    for runtime_root in candidate_runtime_roots(project_dir):
        runs_dir = runtime_root / "runs"
        if not runs_dir.exists():
            continue
        summaries = sorted(runs_dir.rglob("run_summary.json"), key=lambda item: item.stat().st_mtime, reverse=True)
        for summary_path in summaries:
            try:
                payload = json.loads(summary_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            payload_project_dir = str(payload.get("project_dir") or "").strip()
            if not payload_project_dir:
                continue
            if to_host_path(payload_project_dir, project_dir) == project_dir:
                return summary_path, payload
    return None, None


def discover_input_from_project(project_dir: Path) -> tuple[Path | None, str]:
    summary_path, payload = discover_run_summary(project_dir)
    candidate_paths: list[tuple[Path, str]] = []
    if payload:
        artifacts = payload.get("artifacts", {}) if isinstance(payload.get("artifacts"), dict) else {}
        for key, label in [
            ("input_file", "run_summary.input_file"),
            ("load_input_jsonl", "run_summary.artifacts.load_input_jsonl"),
            ("normalized_jsonl", "run_summary.artifacts.normalized_jsonl"),
        ]:
            raw = payload.get(key) if key == "input_file" else artifacts.get(key)
            if raw:
                candidate_paths.append((to_host_path(raw, project_dir), label))

        if summary_path:
            run_dir = summary_path.parent
            for rel_path, label in [
                ("input_normalized.jsonl", "run_dir/input_normalized.jsonl"),
            ]:
                candidate_paths.append((run_dir / rel_path, label))

    repo_root = resolve_repo_root()
    registry_path = repo_root / "output" / "run_registry.csv"
    if registry_path.exists():
        try:
            with registry_path.open("r", encoding="utf-8", newline="") as infile:
                reader = csv.DictReader(infile)
                rows = [
                    row
                    for row in reader
                    if str(row.get("project_dir") or "").strip()
                    and to_host_path(str(row.get("project_dir") or "").strip(), project_dir) == project_dir
                ]
            rows.reverse()
            for row in rows:
                for key, label in [
                    ("base_input_json", "run_registry.base_input_json"),
                    ("mapped_output_jsonl", "run_registry.mapped_output_jsonl"),
                    ("load_input_jsonl", "run_registry.load_input_jsonl"),
                    ("input_file", "run_registry.input_file"),
                ]:
                    raw = str(row.get(key) or "").strip()
                    if raw:
                        candidate_paths.append((to_host_path(raw, project_dir), label))
        except OSError:
            pass

    for path, label in candidate_paths:
        if path.exists():
            return path, label

    return None, "not found"


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


def resolve_snapshot_bin(project_dir: Path, project_env: dict[str, str]) -> Path:
    """Prefer host/system sz_snapshot when available, otherwise fall back to the project copy."""
    env_path = project_env.get("PATH", "")
    host_bin = shutil.which("sz_snapshot", path=env_path)
    if host_bin:
        return Path(host_bin).expanduser().resolve()
    return (project_dir / "bin" / "sz_snapshot").resolve()


def containerize_path(path: Path, repo_root: Path, runtime_root: Path, extra_mount: Path) -> tuple[str, list[tuple[Path, str]]]:
    resolved = path.resolve()
    mounts: list[tuple[Path, str]] = []
    try:
        return f"/runtime/{resolved.relative_to(runtime_root).as_posix()}", mounts
    except ValueError:
        pass
    try:
        return f"/workspace/{resolved.relative_to(repo_root).as_posix()}", mounts
    except ValueError:
        pass
    mounts.append((extra_mount, "/audit-output"))
    if resolved == extra_mount:
        return "/audit-output", mounts
    return f"/audit-output/{resolved.relative_to(extra_mount).as_posix()}", mounts


def run_snapshot_with_docker(
    *,
    project_dir: Path,
    snapshot_root: Path,
    snapshot_threads: int,
    repo_root: Path,
    runtime_root: Path,
) -> None:
    image = os.environ.get("SENZING_DOCKER_IMAGE", "senzing/sz-file-loader:latest")
    extra_mount = snapshot_root.parent
    project_container_path, project_mounts = containerize_path(project_dir, repo_root, runtime_root, extra_mount)
    snapshot_container_root, snapshot_mounts = containerize_path(snapshot_root, repo_root, runtime_root, extra_mount)

    mount_map: dict[str, str] = {
        str(repo_root.resolve()): "/workspace",
        str(runtime_root.resolve()): "/runtime",
    }
    for host_path, container_path in [*project_mounts, *snapshot_mounts]:
        mount_map[str(host_path.resolve())] = container_path

    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "--entrypoint",
        "/bin/bash",
        "-v",
        f"{repo_root.resolve()}:/workspace",
        "-v",
        f"{runtime_root.resolve()}:/runtime",
        "-w",
        "/workspace",
    ]
    for host_path, container_path in mount_map.items():
        if container_path in {"/workspace", "/runtime"}:
            continue
        docker_cmd.extend(["-v", f"{host_path}:{container_path}"])

    shell_command = (
        f"source {shlex.quote(project_container_path + '/setupEnv')} >/dev/null 2>&1 && "
        f"{shlex.quote(project_container_path + '/bin/sz_snapshot')} "
        f"-A -Q -o {shlex.quote(snapshot_container_root)} -t {snapshot_threads}"
    )
    docker_cmd.extend([image, "-lc", shell_command])
    run_command(docker_cmd)


def write_audit_readme(
    *,
    output_dir: Path,
    manifest_path: Path,
    simple_csv: Path,
    truthset_key_csv: Path,
    snapshot_csv: Path | None,
    snapshot_json: Path | None,
    audit_csv: Path | None,
    audit_json: Path | None,
) -> Path:
    """Write a README describing each generated audit artifact."""
    readme_path = output_dir / "README.md"
    descriptions: list[tuple[Path, str]] = [
        (
            simple_csv,
            "Simple reference file mapping each generated `record_id` to the corresponding source `cluster_id` (`IPG ID`) from the same input row.",
        ),
        (
            truthset_key_csv,
            "Truth-set key file used as the `prior` input for `sz_audit`; it contains `DATA_SOURCE`, `RECORD_ID`, and `CLUSTER_ID`.",
        ),
    ]
    if snapshot_csv is not None:
        descriptions.append(
            (
                snapshot_csv,
                "Audit-format snapshot exported from the loaded Senzing project with `sz_snapshot -A`; it represents how Senzing actually clustered the loaded records.",
            )
        )
    if snapshot_json is not None:
        descriptions.append(
            (
                snapshot_json,
                "Metadata sidecar written by `sz_snapshot`; useful for tracing snapshot execution details alongside the CSV payload.",
            )
        )
    if audit_csv is not None:
        descriptions.append(
            (
                audit_csv,
                "Detailed audit output from `sz_audit`, listing record-level differences between the truth-set clustering and the clustering produced by Senzing.",
            )
        )
    if audit_json is not None:
        descriptions.append(
            (
                audit_json,
                "Summary audit metrics from `sz_audit`, including aggregate precision, recall, F1, and merge/split counts.",
            )
        )
    descriptions.append(
        (
            manifest_path,
            "Machine-readable manifest describing the generated files, discovered input source, inferred IPG field, and row counts.",
        )
    )

    lines = [
        "# Senzing Audit Package",
        "",
        "This folder contains the files used to compare the source clustering (`IPG ID`) with the clustering produced by Senzing.",
        "",
        "## Files",
        "",
    ]
    for path, description in descriptions:
        if path.exists():
            lines.append(f"- `{path.name}`: {description}")
    lines.append("")
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return readme_path


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve() if args.project_dir else None
    audit_bin = Path(args.audit_bin).expanduser().resolve() if args.audit_bin else None
    if audit_bin is None and project_dir is not None:
        audit_bin = project_dir / "bin" / "sz_audit"

    input_discovery_source = "explicit"
    input_path: Path | None = None
    if args.input_json:
        input_path = Path(args.input_json).expanduser().resolve()
        if not input_path.exists():
            print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
            return 2
    elif project_dir:
        input_path, input_discovery_source = discover_input_from_project(project_dir)
        if input_path is None:
            print(
                "ERROR: unable to auto-discover input from PROJECT_DIR; set INPUT_JSON explicitly.",
                file=sys.stderr,
            )
            return 2
        print(f"Auto-discovered input: {input_path} ({input_discovery_source})")
    else:
        print("ERROR: input_json is required unless --project-dir is supplied for auto-discovery.", file=sys.stderr)
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
            project_snapshot_bin = project_dir / "bin" / "sz_snapshot"
            execution_mode = os.environ.get("EXECUTION_MODE", "").strip().lower()
            missing = [str(path) for path in (setup_env, project_snapshot_bin, audit_bin) if not path.exists()]
            if missing:
                raise FileNotFoundError("Missing required project files:\n" + "\n".join(f"- {item}" for item in missing))

            snapshot_root = output_dir / args.snapshot_prefix
            snapshot_csv = snapshot_root.with_suffix(".csv")
            try:
                project_env = load_setup_env(setup_env)
                snapshot_bin = resolve_snapshot_bin(project_dir, project_env)
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
            except Exception as host_err:  # pylint: disable=broad-exception-caught
                if execution_mode == "local":
                    raise RuntimeError(
                        "Host snapshot failed in local mode. "
                        "Local Senzing runtime is not configured correctly for sz_snapshot. "
                        f"Original error: {host_err}"
                    ) from host_err
                runtime_roots = candidate_runtime_roots(project_dir)
                runtime_root = runtime_roots[0] if runtime_roots else project_dir.parent.parent
                print(
                    "Host snapshot failed; retrying inside Docker. "
                    f"Original error: {host_err}",
                    file=sys.stderr,
                )
                run_snapshot_with_docker(
                    project_dir=project_dir,
                    snapshot_root=snapshot_root,
                    snapshot_threads=args.snapshot_threads,
                    repo_root=resolve_repo_root(),
                    runtime_root=runtime_root,
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
        "input_discovery_source": input_discovery_source,
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
    snapshot_json = snapshot_csv.with_suffix(".json") if snapshot_csv else None
    readme_path = write_audit_readme(
        output_dir=output_dir,
        manifest_path=manifest_path,
        simple_csv=simple_csv,
        truthset_key_csv=truthset_key_csv,
        snapshot_csv=snapshot_csv,
        snapshot_json=snapshot_json,
        audit_csv=audit_csv,
        audit_json=audit_json,
    )

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
    print(f"README: {readme_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

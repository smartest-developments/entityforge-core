#!/usr/bin/env python3
"""MVP pipeline: JSON -> Senzing JSONL -> Senzing E2E -> output/<timestamp> artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
import datetime as dt
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LARGE_RUN_THRESHOLD_DEFAULT = 300_000
LARGE_RUN_TIMEOUT_SECONDS_DEFAULT = 10_800
LARGE_RUN_PRECHECK_MIN_FREE_GB_DEFAULT = 20.0


def now_timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MVP pipeline from source JSON to timestamped output artifacts.")
    parser.add_argument("--input-json", required=True, help="Source JSON path (array of records)")
    parser.add_argument("--input-array-key", default=None, help="Optional key if JSON root is an object containing array")
    parser.add_argument("--data-source", default="PARTNERS", help="Senzing DATA_SOURCE (default: PARTNERS)")
    parser.add_argument("--tax-id-type", default="TIN", help="TAX_ID_TYPE for mapper (default: TIN)")
    parser.add_argument(
        "--include-unmapped-source-fields",
        action="store_true",
        help="Include non-mapped source fields as SRC_* payload fields",
    )
    parser.add_argument("--run-name-prefix", default="run_mvp", help="Run folder prefix")
    parser.add_argument("--project-name-prefix", default="Senzing_MVP", help="Project folder prefix")
    parser.add_argument(
        "--docker-image",
        default="mapper-senzing-poc:4.2.1",
        help="Docker image containing Senzing tools (default: mapper-senzing-poc:4.2.1)",
    )
    parser.add_argument("--docker-platform", default="linux/amd64", help="Docker platform (default: linux/amd64)")
    parser.add_argument("--step-timeout-seconds", type=int, default=1800, help="Timeout per E2E step")
    parser.add_argument("--load-threads", type=int, default=4, help="Primary sz_file_loader threads (default: 4)")
    parser.add_argument(
        "--load-fallback-threads",
        type=int,
        default=1,
        help="Fallback sz_file_loader threads on retry (default: 1)",
    )
    parser.add_argument("--snapshot-threads", type=int, default=4, help="Primary sz_snapshot threads (default: 4)")
    parser.add_argument(
        "--snapshot-fallback-threads",
        type=int,
        default=1,
        help="Fallback sz_snapshot threads on retry (default: 1)",
    )
    parser.add_argument(
        "--load-no-shuffle-primary",
        action="store_true",
        help="Disable shuffle in primary sz_file_loader attempt.",
    )
    parser.add_argument(
        "--disable-large-run-tuning",
        action="store_true",
        help="Disable automatic tuning for large inputs.",
    )
    parser.add_argument(
        "--large-run-threshold",
        type=int,
        default=LARGE_RUN_THRESHOLD_DEFAULT,
        help=f"Input size threshold for automatic tuning (default: {LARGE_RUN_THRESHOLD_DEFAULT}).",
    )
    parser.add_argument(
        "--large-run-timeout-seconds",
        type=int,
        default=LARGE_RUN_TIMEOUT_SECONDS_DEFAULT,
        help=f"Auto-timeout floor for large runs (default: {LARGE_RUN_TIMEOUT_SECONDS_DEFAULT}).",
    )
    parser.add_argument(
        "--large-run-min-free-gb",
        type=float,
        default=LARGE_RUN_PRECHECK_MIN_FREE_GB_DEFAULT,
        help=(
            "Minimum free disk GB required by preflight for large runs "
            f"(default: {LARGE_RUN_PRECHECK_MIN_FREE_GB_DEFAULT})."
        ),
    )
    parser.add_argument(
        "--strict-preflight",
        action="store_true",
        help="Fail fast when preflight disk checks are below recommended threshold.",
    )
    parser.add_argument(
        "--stream-export",
        action="store_true",
        help="Force stream-export mode in E2E (avoids writing standalone export CSV).",
    )
    parser.add_argument(
        "--with-snapshot",
        action="store_true",
        help="Enable snapshot extraction (disabled by default for faster/lighter runs)",
    )
    parser.add_argument(
        "--with-why",
        action="store_true",
        help="Enable explain/WHY extraction (disabled by default for faster large runs)",
    )
    parser.add_argument("--max-explain-records", type=int, default=200, help="Max explain records when --with-why is enabled")
    parser.add_argument("--max-explain-pairs", type=int, default=200, help="Max explain pairs when --with-why is enabled")
    parser.add_argument(
        "--keep-loader-temp-files",
        action="store_true",
        help="Keep sz_file_loader temporary shuffle files",
    )
    parser.add_argument(
        "--execution-mode",
        choices=["auto", "docker", "local"],
        default="auto",
        help="Execution mode for E2E runner (default: auto)",
    )
    parser.add_argument(
        "--senzing-env",
        default=None,
        help="Optional setupEnv path for local mode (passed to run_senzing_end_to_end.py)",
    )
    parser.add_argument(
        "--output-root",
        default="output",
        help="Root directory for final artifacts (default: output)",
    )
    parser.add_argument(
        "--runtime-dir",
        default=None,
        help="Optional runtime directory (default: temporary directory outside MVP)",
    )
    parser.add_argument(
        "--output-label",
        default=None,
        help="Optional friendly label appended to output folder name",
    )
    parser.add_argument(
        "--keep-runtime-dir",
        action="store_true",
        help="Do not delete runtime directory after completion",
    )
    parser.add_argument(
        "--license-base64-file",
        default=None,
        help=(
            "Optional path to Senzing LICENSESTRINGBASE64 file. "
            "If omitted, auto-detects MVP/.secrets/g2.lic_base64 and MVP/license/g2.lic_base64."
        ),
    )
    return parser.parse_args()


def run_command(command: list[str], cwd: Path, env_overrides: dict[str, str] | None = None) -> None:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    subprocess.run(command, cwd=str(cwd), check=True, env=env)


def sanitize_output_label(raw_label: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", raw_label).strip("._-")
    return safe[:48]


def check_docker_ready() -> tuple[bool, str]:
    """Return Docker availability and a short diagnostic string."""
    if shutil.which("docker") is None:
        return False, "docker command not found"
    probe = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if probe.returncode == 0:
        return True, "docker ready"
    detail = (probe.stderr or probe.stdout or "").strip().splitlines()
    return False, detail[-1] if detail else "docker not available"


def read_license_string(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="ignore")
    compact = "".join(text.split())
    return compact if compact else None


def resolve_license_string(mvp_root: Path, explicit_path: str | None) -> tuple[str | None, str | None]:
    candidates: list[Path] = []
    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())
    env_path = os.environ.get("SENZING_LICENSE_BASE64_FILE", "").strip()
    if env_path:
        candidates.append(Path(env_path).expanduser())
    candidates.extend(
        [
            mvp_root / ".secrets" / "g2.lic_base64",
            mvp_root / "license" / "g2.lic_base64",
        ]
    )

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        license_string = read_license_string(resolved)
        if license_string:
            return license_string, str(resolved)
    return None, None


def detect_input_array_key(input_json: Path) -> str | None:
    if input_json.suffix.lower() == ".jsonl":
        return None
    try:
        payload = json.loads(input_json.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(payload, list):
        return None
    if isinstance(payload, dict):
        for candidate in ["records", "data", "items"]:
            if isinstance(payload.get(candidate), list):
                return candidate
    return None


def count_non_empty_lines(path: Path) -> int:
    total = 0
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip():
                total += 1
    return total


def count_source_records(input_json: Path, input_array_key: str | None) -> int:
    if input_json.suffix.lower() == ".jsonl":
        return count_non_empty_lines(input_json)
    total = 0
    for _ in iter_source_records(input_json, input_array_key):
        total += 1
    return total


def bytes_to_gb(value: int) -> float:
    return value / (1024.0**3)


def estimate_large_run_required_gb(source_record_count: int, configured_min_gb: float) -> float:
    if source_record_count <= 0:
        return configured_min_gb
    # Conservative estimate for SQLite + export + temp files on high-volume runs.
    estimated = max(8.0, (source_record_count / 100_000.0) * 2.0)
    return max(configured_min_gb, estimated)


def collect_disk_space_snapshot(paths: list[Path]) -> dict[str, dict[str, float]]:
    snapshot: dict[str, dict[str, float]] = {}
    for path in paths:
        usage = shutil.disk_usage(path)
        snapshot[str(path)] = {
            "total_gb": round(bytes_to_gb(usage.total), 2),
            "used_gb": round(bytes_to_gb(usage.used), 2),
            "free_gb": round(bytes_to_gb(usage.free), 2),
        }
    return snapshot


def host_architecture_note(execution_mode: str, docker_platform: str) -> str | None:
    if execution_mode != "docker":
        return None
    host_machine = platform.machine().lower()
    requested = docker_platform.lower()
    if host_machine in {"arm64", "aarch64"} and "amd64" in requested:
        return (
            "Host is ARM64 but Docker platform is linux/amd64 (emulation). "
            "Large runs can be significantly slower and may require higher timeouts."
        )
    return None


def find_new_run_dir(runs_root: Path, prefix: str) -> Path:
    run_dirs = sorted(
        [path for path in runs_root.glob(f"{prefix}_*") if path.is_dir()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not run_dirs:
        raise FileNotFoundError(f"No run directory found under {runs_root} with prefix {prefix}")
    return run_dirs[0]


def comb2(value: int) -> int:
    return value * (value - 1) // 2 if value > 1 else 0


def safe_ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def text_from_keys(record: dict[str, object], keys: list[str]) -> str:
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def iter_source_records(input_json: Path, input_array_key: str | None):
    if input_json.suffix.lower() == ".jsonl":
        with input_json.open("r", encoding="utf-8") as infile:
            for line_no, line in enumerate(infile, start=1):
                text = line.strip()
                if not text:
                    continue
                try:
                    payload = json.loads(text)
                except json.JSONDecodeError as err:
                    raise ValueError(f"Invalid JSON on line {line_no} of {input_json}: {err}") from err
                if isinstance(payload, dict):
                    yield payload
        return

    payload = json.loads(input_json.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        candidate_key = input_array_key or detect_input_array_key(input_json) or "records"
        records = payload.get(candidate_key)
    else:
        raise TypeError("Unsupported source JSON root type")
    if not isinstance(records, list):
        raise TypeError("Source records array not found in input JSON")
    for item in records:
        if isinstance(item, dict):
            yield item


def compute_extra_match_metrics(
    source_input_json: Path,
    input_array_key: str | None,
    matched_pairs_csv: Path,
) -> dict[str, object] | None:
    if not matched_pairs_csv.exists():
        return None

    true_group_keys = [
        "SOURCE_TRUE_GROUP_ID",
        "source_true_group_id",
        "TRUE_GROUP_ID",
        "true_group_id",
        "TRUE_ENTITY_ID",
        "true_entity_id",
    ]
    ipg_keys = ["IPG ID", "IPG_ID", "ipg_id", "SOURCE_IPG_ID", "source_ipg_id"]

    record_truth: dict[str, tuple[str, str]] = {}
    true_group_counts: Counter[str] = Counter()
    ipg_true_group_counts: dict[str, Counter[str]] = defaultdict(Counter)
    records_with_true_group = 0
    records_with_ipg = 0

    records_total = 0
    for index, record in enumerate(iter_source_records(source_input_json, input_array_key), start=1):
        records_total += 1
        true_group = text_from_keys(record, true_group_keys)
        ipg_id = text_from_keys(record, ipg_keys)
        record_truth[str(index)] = (true_group, ipg_id)
        if true_group:
            records_with_true_group += 1
            true_group_counts[true_group] += 1
            if ipg_id:
                ipg_true_group_counts[ipg_id][true_group] += 1
        if ipg_id:
            records_with_ipg += 1

    if records_with_true_group <= 1:
        return None

    true_pairs_total = sum(comb2(count) for count in true_group_counts.values())
    baseline_predicted_pairs = sum(comb2(sum(counter.values())) for counter in ipg_true_group_counts.values())
    baseline_true_positive = sum(
        comb2(group_count) for counter in ipg_true_group_counts.values() for group_count in counter.values()
    )
    baseline_false_positive = max(0, baseline_predicted_pairs - baseline_true_positive)
    baseline_false_negative = max(0, true_pairs_total - baseline_true_positive)
    known_pairs_ipg = baseline_true_positive
    discoverable_true_pairs = max(0, true_pairs_total - baseline_true_positive)

    predicted_pairs_beyond_known = 0
    extra_true_matches_found = 0
    extra_false_matches_found = 0
    overall_predicted_pairs = 0
    overall_true_pairs_found = 0
    overall_false_pairs_found = 0

    with matched_pairs_csv.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            anchor_meta = record_truth.get(str(row.get("anchor_record_id") or "").strip())
            matched_meta = record_truth.get(str(row.get("matched_record_id") or "").strip())
            if not anchor_meta or not matched_meta:
                continue

            anchor_true_group, anchor_ipg = anchor_meta
            matched_true_group, matched_ipg = matched_meta

            is_true_pair = bool(anchor_true_group and matched_true_group and anchor_true_group == matched_true_group)
            is_known_pair = bool(anchor_ipg and matched_ipg and anchor_ipg == matched_ipg)

            overall_predicted_pairs += 1
            if is_true_pair:
                overall_true_pairs_found += 1
            else:
                overall_false_pairs_found += 1

            if is_known_pair:
                continue

            predicted_pairs_beyond_known += 1
            if is_true_pair:
                extra_true_matches_found += 1
            else:
                extra_false_matches_found += 1

    return {
        "available": True,
        "records_input": records_total,
        "records_with_true_group": records_with_true_group,
        "records_with_ipg": records_with_ipg,
        "true_pairs_total": true_pairs_total,
        "baseline_predicted_pairs": baseline_predicted_pairs,
        "baseline_true_positive": baseline_true_positive,
        "baseline_false_positive": baseline_false_positive,
        "baseline_false_negative": baseline_false_negative,
        "baseline_match_precision": safe_ratio(baseline_true_positive, baseline_predicted_pairs),
        "known_pairs_ipg": known_pairs_ipg,
        "baseline_match_coverage": safe_ratio(baseline_true_positive, true_pairs_total),
        "discoverable_true_pairs": discoverable_true_pairs,
        "predicted_pairs_beyond_known": predicted_pairs_beyond_known,
        "extra_true_matches_found": extra_true_matches_found,
        "extra_false_matches_found": extra_false_matches_found,
        "extra_match_precision": safe_ratio(extra_true_matches_found, predicted_pairs_beyond_known),
        "extra_match_recall": safe_ratio(extra_true_matches_found, discoverable_true_pairs),
        "extra_gain_vs_known": safe_ratio(extra_true_matches_found, known_pairs_ipg),
        "net_extra_matches": extra_true_matches_found - extra_false_matches_found,
        "overall_predicted_pairs": overall_predicted_pairs,
        "overall_true_pairs_found": overall_true_pairs_found,
        "overall_false_pairs_found": overall_false_pairs_found,
        "overall_false_positive_rate": safe_ratio(overall_false_pairs_found, overall_predicted_pairs),
        "overall_match_correctness": safe_ratio(overall_true_pairs_found, overall_predicted_pairs),
        "senzing_true_coverage": safe_ratio(overall_true_pairs_found, true_pairs_total),
    }


def enrich_management_summary_with_extra_metrics(
    source_input_json: Path,
    input_array_key: str | None,
    output_run_dir: Path,
) -> None:
    technical_dir = output_run_dir / "technical output"
    management_json = technical_dir / "management_summary.json"
    management_md = output_run_dir / "management_summary.md"
    matched_pairs_csv = technical_dir / "matched_pairs.csv"
    if not management_json.exists() or not management_md.exists() or not matched_pairs_csv.exists():
        return

    discovery_metrics = compute_extra_match_metrics(
        source_input_json=source_input_json,
        input_array_key=input_array_key,
        matched_pairs_csv=matched_pairs_csv,
    )
    if not discovery_metrics:
        return

    summary_payload = json.loads(management_json.read_text(encoding="utf-8"))
    if not isinstance(summary_payload, dict):
        return
    summary_payload["discovery_metrics"] = discovery_metrics
    management_json.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = management_md.read_text(encoding="utf-8").rstrip("\n")
    lines += "\n\n## Extra True Matches Beyond SOURCE_IPG_ID\n\n"
    lines += (
        f"- Our match coverage (without Senzing): {discovery_metrics['baseline_match_coverage'] * 100:.2f}% "
        "(Portion of true pairs that were already known from SOURCE_IPG_ID labels before Senzing.)\n"
    )
    lines += (
        f"- Our false positives (without Senzing): {discovery_metrics.get('baseline_false_positive', 0)} "
        "(Pairs implied by SOURCE_IPG_ID that are not true matches by SOURCE_TRUE_GROUP_ID.)\n"
    )
    lines += (
        f"- Our false negatives (without Senzing): {discovery_metrics.get('baseline_false_negative', 0)} "
        "(True pairs that SOURCE_IPG_ID labels do not capture.)\n"
    )
    lines += (
        f"- Extra true matches found: {discovery_metrics['extra_true_matches_found']} "
        "(True matches discovered by Senzing where SOURCE_IPG_ID did not already label the pair.)\n"
    )
    lines += (
        f"- Extra gain vs known pairs: {discovery_metrics['extra_gain_vs_known'] * 100:.2f}% "
        "(Extra true matches divided by pairs already known via SOURCE_IPG_ID.)\n"
    )
    lines += (
        f"- Extra match precision: {discovery_metrics['extra_match_precision'] * 100:.2f}% "
        "(Among predicted pairs beyond known labels, how many are truly correct.)\n"
    )
    lines += (
        f"- Extra match recall: {discovery_metrics['extra_match_recall'] * 100:.2f}% "
        "(Share of true-but-unlabeled pairs that Senzing successfully found.)\n"
    )
    lines += (
        f"- Discoverable true pairs (beyond known): {discovery_metrics['discoverable_true_pairs']} "
        "(Total true pairs present in hidden ground truth that are not in SOURCE_IPG_ID labels.)\n"
    )
    lines += (
        f"- False positive % (all predicted pairs): {discovery_metrics['overall_false_positive_rate'] * 100:.2f}% "
        "(Among all pairs predicted by Senzing, percentage that are not true matches by SOURCE_TRUE_GROUP_ID.)\n"
    )
    lines += (
        f"- Senzing true coverage: {discovery_metrics['senzing_true_coverage'] * 100:.2f}% "
        "(Portion of all true pairs in the sample that Senzing actually recovered.)\n"
    )
    management_md.write_text(lines + "\n", encoding="utf-8")


def copy_if_exists(source: Path, destination: Path) -> bool:
    if not source.exists():
        return False
    try:
        if source.resolve() == destination.resolve():
            return True
    except FileNotFoundError:
        pass
    shutil.copy2(source, destination)
    return True


def refresh_dashboard_data(mvp_root: Path, output_root: Path) -> None:
    dashboard_builder = mvp_root / "build_management_dashboard.py"
    if not dashboard_builder.exists():
        print(f"WARNING: dashboard builder not found: {dashboard_builder}")
        return
    command = [
        sys.executable,
        str(dashboard_builder),
        "--output-root",
        str(output_root),
        "--dashboard-dir",
        "dashboard",
    ]
    run_command(command, mvp_root)


def copy_artifacts_to_output(
    output_run_dir: Path,
    mvp_root: Path,
    runtime_dir: Path,
    source_input_json: Path,
    run_dir: Path,
    mapped_output_jsonl: Path,
    field_map_json: Path,
    mapping_summary_json: Path,
    run_summary_json: Path,
) -> dict[str, str]:
    copied: dict[str, str] = {}
    technical_dir = output_run_dir / "technical output"
    technical_dir.mkdir(parents=True, exist_ok=True)
    source_copy_name = "input_source.jsonl" if source_input_json.suffix.lower() == ".jsonl" else "input_source.json"

    def to_host_path(raw_path: Path) -> Path:
        raw = str(raw_path)
        if raw.startswith("/runtime/"):
            return runtime_dir / raw.removeprefix("/runtime/")
        if raw.startswith("/workspace/"):
            return mvp_root / raw.removeprefix("/workspace/")
        return raw_path

    targets = {
        source_input_json: output_run_dir / source_copy_name,
        mapped_output_jsonl: technical_dir / "mapped_output.jsonl",
        field_map_json: technical_dir / "field_map.json",
        mapping_summary_json: technical_dir / "mapping_summary.json",
        run_summary_json: technical_dir / "run_summary.json",
        run_dir / "input_normalized.jsonl": technical_dir / "input_normalized.jsonl",
    }
    run_summary_payload = json.loads(run_summary_json.read_text(encoding="utf-8"))
    artifacts = run_summary_payload.get("artifacts", {}) if isinstance(run_summary_payload.get("artifacts"), dict) else {}
    for key, destination in [
        ("management_summary_md", output_run_dir / "management_summary.md"),
        ("ground_truth_match_quality_md", output_run_dir / "ground_truth_match_quality.md"),
        ("management_summary_json", technical_dir / "management_summary.json"),
        ("ground_truth_match_quality_json", technical_dir / "ground_truth_match_quality.json"),
        ("matched_pairs_csv", technical_dir / "matched_pairs.csv"),
        ("match_stats_csv", technical_dir / "match_stats.csv"),
        ("entity_records_csv", technical_dir / "entity_records.csv"),
    ]:
        value = artifacts.get(key)
        if not value:
            continue
        targets[to_host_path(Path(str(value)))] = destination

    run_registry_candidate = mvp_root / "output" / "run_registry.csv"
    if run_registry_candidate.exists():
        targets[run_registry_candidate] = technical_dir / "run_registry.csv"

    for source, destination in targets.items():
        if copy_if_exists(source, destination):
            copied[destination.name] = str(destination.resolve())

    return copied


def main() -> int:
    args = parse_args()
    if args.step_timeout_seconds <= 0:
        print("ERROR: --step-timeout-seconds must be > 0", file=sys.stderr)
        return 2
    if args.load_threads <= 0 or args.load_fallback_threads <= 0:
        print("ERROR: --load-threads and --load-fallback-threads must be > 0", file=sys.stderr)
        return 2
    if args.snapshot_threads <= 0 or args.snapshot_fallback_threads <= 0:
        print("ERROR: --snapshot-threads and --snapshot-fallback-threads must be > 0", file=sys.stderr)
        return 2
    if args.large_run_threshold < 0:
        print("ERROR: --large-run-threshold must be >= 0", file=sys.stderr)
        return 2
    if args.large_run_timeout_seconds <= 0:
        print("ERROR: --large-run-timeout-seconds must be > 0", file=sys.stderr)
        return 2
    if args.large_run_min_free_gb <= 0:
        print("ERROR: --large-run-min-free-gb must be > 0", file=sys.stderr)
        return 2

    mvp_root = Path(__file__).resolve().parent
    input_json = Path(args.input_json).expanduser().resolve()

    if not input_json.exists():
        print(f"ERROR: input JSON not found: {input_json}", file=sys.stderr)
        return 2

    mapper_script = mvp_root / "partner_json_to_senzing.py"
    e2e_script = mvp_root / "run_senzing_end_to_end.py"
    missing_scripts = [str(path) for path in [mapper_script, e2e_script] if not path.exists()]
    if missing_scripts:
        print("ERROR: missing required scripts:", file=sys.stderr)
        for item in missing_scripts:
            print(f"  - {item}", file=sys.stderr)
        return 2

    ts = now_timestamp()
    derived_label = sanitize_output_label(args.output_label or input_json.stem)
    output_folder_name = f"{ts}__{derived_label}" if derived_label else ts
    output_root = (mvp_root / args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_run_dir = output_root / output_folder_name

    if args.runtime_dir:
        runtime_dir = Path(args.runtime_dir).expanduser().resolve()
        runtime_dir.mkdir(parents=True, exist_ok=True)
        runtime_created = False
    else:
        runtime_dir = Path(tempfile.mkdtemp(prefix="mvp_runtime_"))
        runtime_created = True

    runtime_runs = runtime_dir / "runs"
    runtime_projects = runtime_dir / "projects"
    runtime_runs.mkdir(parents=True, exist_ok=True)
    runtime_projects.mkdir(parents=True, exist_ok=True)
    technical_output_dir = output_run_dir / "technical output"
    technical_output_dir.mkdir(parents=True, exist_ok=True)

    mapped_output_jsonl = technical_output_dir / "mapped_output.jsonl"
    field_map_json = technical_output_dir / "field_map.json"
    mapping_summary_json = technical_output_dir / "mapping_summary.json"
    effective_input_array_key = args.input_array_key or detect_input_array_key(input_json)

    source_records_detected = count_source_records(input_json, effective_input_array_key)
    large_input_detected = source_records_detected >= args.large_run_threshold
    effective_step_timeout_seconds = args.step_timeout_seconds
    effective_load_threads = args.load_threads
    effective_load_fallback_threads = args.load_fallback_threads
    effective_snapshot_threads = args.snapshot_threads
    effective_snapshot_fallback_threads = args.snapshot_fallback_threads
    effective_load_no_shuffle_primary = bool(args.load_no_shuffle_primary)
    large_run_tuning_applied = False
    effective_stream_export = bool(args.stream_export)

    if large_input_detected and not args.disable_large_run_tuning:
        large_run_tuning_applied = True
        effective_step_timeout_seconds = max(args.step_timeout_seconds, args.large_run_timeout_seconds)
        effective_load_threads = min(effective_load_threads, 2)
        effective_load_fallback_threads = 1
        effective_snapshot_threads = min(effective_snapshot_threads, 2)
        effective_snapshot_fallback_threads = 1
        effective_load_no_shuffle_primary = True
        effective_stream_export = True

    disk_snapshot = collect_disk_space_snapshot([runtime_dir, output_root, output_run_dir, mvp_root])
    min_free_disk_gb = min(item["free_gb"] for item in disk_snapshot.values())
    required_free_disk_gb = estimate_large_run_required_gb(source_records_detected, args.large_run_min_free_gb)
    preflight_ok = (not large_input_detected) or (min_free_disk_gb >= required_free_disk_gb)
    if large_input_detected:
        print(
            "Preflight: "
            f"records={source_records_detected:,}, min_free={min_free_disk_gb:.2f}GB, "
            f"recommended_free={required_free_disk_gb:.2f}GB"
        )
    if not preflight_ok:
        message = (
            "Large-run preflight warning: free disk appears below recommended threshold "
            f"({min_free_disk_gb:.2f}GB < {required_free_disk_gb:.2f}GB)."
        )
        if args.strict_preflight:
            print(f"ERROR: {message}", file=sys.stderr)
            return 2
        print(f"WARNING: {message}")

    mapper_cmd = [
        sys.executable,
        str(mapper_script),
        str(input_json),
        str(mapped_output_jsonl),
        "--data-source",
        args.data_source,
        "--tax-id-type",
        args.tax_id_type,
        "--write-field-map",
        str(field_map_json),
    ]
    if effective_input_array_key:
        mapper_cmd.extend(["--array-key", effective_input_array_key])
    if args.include_unmapped_source_fields:
        mapper_cmd.append("--include-unmapped-source-fields")
    run_command(mapper_cmd, mvp_root)

    mapping_summary = {
        "mode": "input_json",
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "input_json": str(input_json),
        "source_input_name": input_json.name,
        "source_records_detected": source_records_detected,
        "mapped_output_jsonl": str(mapped_output_jsonl),
        "field_map_json": str(field_map_json),
        "data_source": args.data_source,
        "tax_id_type": args.tax_id_type,
        "input_array_key": effective_input_array_key,
        "output_folder_name": output_folder_name,
        "output_label": derived_label or None,
        "include_unmapped_source_fields": bool(args.include_unmapped_source_fields),
        "runtime_dir": str(runtime_dir),
        "large_input_detected": large_input_detected,
        "large_run_tuning_applied": large_run_tuning_applied,
        "effective_step_timeout_seconds": effective_step_timeout_seconds,
        "effective_load_threads": effective_load_threads,
        "effective_load_fallback_threads": effective_load_fallback_threads,
        "effective_snapshot_threads": effective_snapshot_threads,
        "effective_snapshot_fallback_threads": effective_snapshot_fallback_threads,
        "effective_load_no_shuffle_primary": effective_load_no_shuffle_primary,
        "effective_stream_export": effective_stream_export,
        "with_snapshot": bool(args.with_snapshot),
        "with_why": bool(args.with_why),
        "preflight": {
            "strict_preflight": bool(args.strict_preflight),
            "disk_snapshot_gb": disk_snapshot,
            "min_free_disk_gb": min_free_disk_gb,
            "recommended_free_disk_gb": required_free_disk_gb,
            "ok": preflight_ok,
        },
    }
    mapping_summary_json.write_text(json.dumps(mapping_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    docker_ready, docker_note = check_docker_ready()
    execution_mode = args.execution_mode
    if execution_mode == "docker" and not docker_ready:
        print(f"ERROR: --execution-mode docker requested but Docker is not available ({docker_note})", file=sys.stderr)
        return 2
    if execution_mode == "auto":
        execution_mode = "docker" if docker_ready else "local"
    arch_note = host_architecture_note(execution_mode=execution_mode, docker_platform=args.docker_platform)
    if arch_note:
        print(f"WARNING: {arch_note}")

    license_string, license_source_path = resolve_license_string(
        mvp_root=mvp_root,
        explicit_path=args.license_base64_file,
    )
    if license_string:
        print(f"Senzing license detected from: {license_source_path}")
    else:
        print("WARNING: no Senzing license file detected; engine may run in 500-record evaluation mode.")

    e2e_env: dict[str, str] = {}
    if license_string:
        e2e_env["SENZING_LICENSE_STRING_BASE64"] = license_string

    e2e_cmd: list[str]
    if execution_mode == "docker":
        container_mapped_input = f"/workspace/{mapped_output_jsonl.relative_to(mvp_root).as_posix()}"
        e2e_cmd = [
            "docker",
            "run",
            "--rm",
            "--platform",
            args.docker_platform,
            "-v",
            f"{mvp_root}:/workspace",
            "-v",
            f"{runtime_dir}:/runtime",
            "-w",
            "/workspace",
        ]
        if license_string:
            e2e_cmd.extend(
                [
                    "-e",
                    f"SENZING_LICENSE_STRING_BASE64={license_string}",
                ]
            )
        e2e_cmd.extend(
            [
            args.docker_image,
            "python3",
            "/workspace/run_senzing_end_to_end.py",
            container_mapped_input,
            "--output-root",
            "/runtime/runs",
            "--run-name-prefix",
            args.run_name_prefix,
            "--project-parent-dir",
            "/runtime/projects",
            "--project-name-prefix",
            args.project_name_prefix,
            "--use-input-jsonl-directly",
            "--data-sources",
            args.data_source,
            "--step-timeout-seconds",
            str(effective_step_timeout_seconds),
            "--load-threads",
            str(effective_load_threads),
            "--load-fallback-threads",
            str(effective_load_fallback_threads),
            "--snapshot-threads",
            str(effective_snapshot_threads),
            "--snapshot-fallback-threads",
            str(effective_snapshot_fallback_threads),
            ]
        )
    else:
        e2e_cmd = [
            sys.executable,
            str(e2e_script),
            str(mapped_output_jsonl),
            "--output-root",
            str(runtime_runs),
            "--run-name-prefix",
            args.run_name_prefix,
            "--project-parent-dir",
            str(runtime_projects),
            "--project-name-prefix",
            args.project_name_prefix,
            "--use-input-jsonl-directly",
            "--data-sources",
            args.data_source,
            "--step-timeout-seconds",
            str(effective_step_timeout_seconds),
            "--load-threads",
            str(effective_load_threads),
            "--load-fallback-threads",
            str(effective_load_fallback_threads),
            "--snapshot-threads",
            str(effective_snapshot_threads),
            "--snapshot-fallback-threads",
            str(effective_snapshot_fallback_threads),
        ]
        if args.senzing_env:
            e2e_cmd.extend(["--senzing-env", str(Path(args.senzing_env).expanduser().resolve())])

    if args.with_why:
        e2e_cmd.extend(["--max-explain-records", str(args.max_explain_records)])
        e2e_cmd.extend(["--max-explain-pairs", str(args.max_explain_pairs)])
    else:
        e2e_cmd.append("--skip-explain")
    if not args.with_snapshot:
        e2e_cmd.append("--skip-snapshot")
    if args.keep_loader_temp_files:
        e2e_cmd.append("--keep-loader-temp-files")
    if effective_load_no_shuffle_primary:
        e2e_cmd.append("--load-no-shuffle-primary")
    if effective_stream_export:
        e2e_cmd.append("--stream-export")

    mapping_summary["execution_mode"] = execution_mode
    mapping_summary["docker_probe"] = docker_note
    mapping_summary["architecture_note"] = arch_note
    mapping_summary["license_string_present"] = bool(license_string)
    mapping_summary["license_source_path"] = license_source_path
    mapping_summary_json.write_text(json.dumps(mapping_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"E2E execution mode: {execution_mode}")
    print(f"Input records detected: {source_records_detected:,}")
    print(f"Snapshot enabled: {bool(args.with_snapshot)}")
    if large_run_tuning_applied:
        print(
            "Large-run tuning: enabled "
            f"(timeout={effective_step_timeout_seconds}s, load_threads={effective_load_threads}, "
            f"snapshot_threads={effective_snapshot_threads}, load_no_shuffle_primary={effective_load_no_shuffle_primary})"
        )
    print(f"Stream export enabled: {effective_stream_export}")
    if execution_mode == "local" and docker_note != "docker ready":
        print(f"Docker note: {docker_note}")

    keep_runtime = args.keep_runtime_dir or not runtime_created
    try:
        run_command(e2e_cmd, mvp_root, env_overrides=e2e_env if e2e_env else None)

        run_dir = find_new_run_dir(runtime_runs, args.run_name_prefix)
        run_summary_json = run_dir / "run_summary.json"
        if not run_summary_json.exists():
            print(f"ERROR: run summary not found: {run_summary_json}", file=sys.stderr)
            return 2

        output_run_dir.mkdir(parents=True, exist_ok=True)
        copied = copy_artifacts_to_output(
            output_run_dir=output_run_dir,
            mvp_root=mvp_root,
            runtime_dir=runtime_dir,
            source_input_json=input_json,
            run_dir=run_dir,
            mapped_output_jsonl=mapped_output_jsonl,
            field_map_json=field_map_json,
            mapping_summary_json=mapping_summary_json,
            run_summary_json=run_summary_json,
        )
        try:
            enrich_management_summary_with_extra_metrics(
                source_input_json=input_json,
                input_array_key=effective_input_array_key,
                output_run_dir=output_run_dir,
            )
        except Exception as exc:
            print(f"WARNING: unable to compute extra match metrics ({exc})")
        try:
            refresh_dashboard_data(mvp_root=mvp_root, output_root=output_root)
        except subprocess.CalledProcessError as exc:
            print(
                f"ERROR: dashboard refresh/test suite failed (exit code {exc.returncode}).",
                file=sys.stderr,
            )
            return exc.returncode or 1

        print("\nMVP pipeline completed.")
        print(f"Input JSON: {input_json}")
        print(f"Output directory: {output_run_dir}")
        print(f"Technical directory: {output_run_dir / 'technical output'}")
        print(f"Artifacts copied: {len(copied)}")
        print(f"Mapped JSONL: {copied.get('mapped_output.jsonl')}")
        print(f"Management summary (md): {copied.get('management_summary.md')}")
        print(f"Ground truth quality (md): {copied.get('ground_truth_match_quality.md')}")
        print(f"Run summary (technical): {copied.get('run_summary.json')}")
        print(f"Run registry CSV: {copied.get('run_registry.csv')}")
        if keep_runtime:
            print(f"Runtime directory kept: {runtime_dir}")
        return 0
    finally:
        if not keep_runtime:
            shutil.rmtree(runtime_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate concrete mismatch tuning points from snapshot+audit JSON."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ConcretePoint:
    side: str
    priority: int
    issue: str
    pattern: str
    count: int
    share_pct: float
    action: str
    expected_effect: str
    risk: str
    sample_audit_ids: str
    sample_record_ids: str
    sample_newer_scores: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build concrete tuning/data-improvement points from truthset_snapshot + truthset_audit."
        )
    )
    parser.add_argument("--snapshot", required=True, help="Path to truthset_snapshot.json/kjson")
    parser.add_argument("--audit", required=True, help="Path to truthset_audit.json")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--top-n", type=int, default=12, help="Top patterns per side (default: 12)")
    parser.add_argument("--samples-per-point", type=int, default=10, help="Max sample ids per point")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise ValueError(f"Unable to parse JSON from {path}: {err}") from err


def safe_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(round(value))
    try:
        return int(str(value).strip())
    except Exception:
        return 0


def safe_float(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except Exception:
        return 0.0


def pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return (count / total) * 100.0


def get_category(audit_payload: dict[str, Any], category: str) -> dict[str, Any]:
    block = audit_payload.get("AUDIT", {})
    if not isinstance(block, dict):
        return {}
    value = block.get(category, {})
    return value if isinstance(value, dict) else {}


def flatten_rows(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "AUDIT_ID" in value or "RECORD_ID" in value or "NEWER_SCORE" in value:
            rows.append(value)
        for item in value.values():
            rows.extend(flatten_rows(item))
    elif isinstance(value, list):
        for item in value:
            rows.extend(flatten_rows(item))
    return rows


def subcategory_rows(category_payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sub = category_payload.get("SUB_CATEGORY", {})
    if not isinstance(sub, dict):
        return {}
    out: dict[str, list[dict[str, Any]]] = {}
    for name, payload in sub.items():
        if isinstance(payload, dict):
            samples = payload.get("SAMPLE", [])
            rows = flatten_rows(samples)
            out[str(name)] = rows
    return out


def top_snapshot_principles(snapshot_payload: dict[str, Any], limit: int = 8) -> list[tuple[str, int]]:
    principles = snapshot_payload.get("TOTALS", {}).get("MATCH", {}).get("PRINCIPLES", {})
    if not isinstance(principles, dict):
        return []
    pairs: list[tuple[str, int]] = []
    for key, value in principles.items():
        if isinstance(value, dict):
            pairs.append((str(key), safe_int(value.get("COUNT", 0))))
    pairs.sort(key=lambda item: item[1], reverse=True)
    return pairs[:limit]


def sample_values(rows: list[dict[str, Any]], key: str, limit: int) -> str:
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        value = str(row.get(key, "")).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
        if len(out) >= limit:
            break
    return ",".join(out)


def classify_their_pattern(pattern: str) -> tuple[int, str, str, str, str]:
    lower = pattern.lower()
    if lower.startswith("related on:"):
        return (
            1,
            "Near-match blocked (related-on)",
            "Tune matching to promote selected related-on paths to merge when 2+ strong corroborators exist.",
            "Increase recall on missed true matches.",
            "Can lower precision if applied globally.",
        )
    if "multiple" in lower:
        return (
            2,
            "Mixed split behavior",
            "Build a calibration set for this pattern and tune subgroup-specific thresholds.",
            "More controlled recall gain with lower collateral risk.",
            "Requires calibration cycle.",
        )
    if "-tax_id" in pattern:
        return (
            3,
            "Tax-ID conflict blocking merge",
            "Reduce tax-id conflict penalty when NAME+DOB+OTHER_ID evidence is strong.",
            "Recover valid matches with tax-id noise.",
            "May add false positives on truly distinct entities.",
        )
    if "ambiguous" in lower:
        return (
            4,
            "Ambiguity-driven split",
            "In ambiguity cases require one extra corroborating attribute before split.",
            "Recover borderline true matches.",
            "Moderate precision risk if corroborator quality is weak.",
        )
    return (
        5,
        "Other split pattern",
        "Review sample IDs and define a scoped tuning rule for this exact pattern.",
        "Potential recall gain on uncovered pattern.",
        "Unknown until calibrated.",
    )


def classify_our_pattern(pattern: str) -> tuple[int, str, str, str, str]:
    lower = pattern.lower()
    if "multiple" in lower:
        return (
            1,
            "Baseline fragmentation from mixed source quality",
            "Add upstream normalization + quality gate for names/addresses/ids for this pattern family.",
            "Fewer baseline false negatives and cleaner truthset.",
            "Data engineering effort required.",
        )
    if "+tax_id" in pattern:
        return (
            2,
            "Baseline misses despite strong TAX_ID evidence",
            "Standardize TAX_ID/NAME/DOB formatting and missing-value handling before cluster assignment.",
            "Higher baseline consistency and fewer split source clusters.",
            "Potential upstream schema/process changes.",
        )
    if "non-match" in lower:
        return (
            3,
            "Missing source cluster IDs",
            "Increase SOURCE cluster completeness; reduce placeholder non-match assignments.",
            "Lower artificial mismatch noise.",
            "Depends on upstream data owners.",
        )
    return (
        4,
        "Other baseline mismatch pattern",
        "Review sample records and define deterministic source clustering rules for this pattern.",
        "Reduced baseline instability.",
        "Requires rules governance.",
    )


def build_their_points(
    audit_payload: dict[str, Any],
    top_n: int,
    samples_per_point: int,
) -> list[ConcretePoint]:
    split_block = get_category(audit_payload, "SPLIT")
    split_total = safe_int(split_block.get("COUNT", 0))
    rows_by_pattern = subcategory_rows(split_block)

    counts: list[tuple[str, int, list[dict[str, Any]]]] = []
    sub = split_block.get("SUB_CATEGORY", {})
    if isinstance(sub, dict):
        for pattern, payload in sub.items():
            if isinstance(payload, dict):
                count = safe_int(payload.get("COUNT", 0))
                counts.append((str(pattern), count, rows_by_pattern.get(str(pattern), [])))
    counts.sort(key=lambda item: item[1], reverse=True)
    counts = counts[: max(1, top_n)]

    out: list[ConcretePoint] = []
    for pattern, count, rows in counts:
        prio, issue, action, effect, risk = classify_their_pattern(pattern)
        out.append(
            ConcretePoint(
                side="their",
                priority=prio,
                issue=issue,
                pattern=pattern,
                count=count,
                share_pct=pct(count, split_total),
                action=action,
                expected_effect=effect,
                risk=risk,
                sample_audit_ids=sample_values(rows, "AUDIT_ID", samples_per_point),
                sample_record_ids=sample_values(rows, "RECORD_ID", samples_per_point),
                sample_newer_scores=sample_values(rows, "NEWER_SCORE", samples_per_point),
            )
        )
    out.sort(key=lambda item: (item.priority, -item.count))
    return out


def build_our_points(
    audit_payload: dict[str, Any],
    top_n: int,
    samples_per_point: int,
) -> list[ConcretePoint]:
    merge_block = get_category(audit_payload, "MERGE")
    merge_total = safe_int(merge_block.get("COUNT", 0))
    rows_by_pattern = subcategory_rows(merge_block)

    counts: list[tuple[str, int, list[dict[str, Any]]]] = []
    sub = merge_block.get("SUB_CATEGORY", {})
    if isinstance(sub, dict):
        for pattern, payload in sub.items():
            if isinstance(payload, dict):
                count = safe_int(payload.get("COUNT", 0))
                counts.append((str(pattern), count, rows_by_pattern.get(str(pattern), [])))
    counts.sort(key=lambda item: item[1], reverse=True)
    counts = counts[: max(1, top_n)]

    out: list[ConcretePoint] = []
    for pattern, count, rows in counts:
        prio, issue, action, effect, risk = classify_our_pattern(pattern)
        out.append(
            ConcretePoint(
                side="our",
                priority=prio,
                issue=issue,
                pattern=pattern,
                count=count,
                share_pct=pct(count, merge_total),
                action=action,
                expected_effect=effect,
                risk=risk,
                sample_audit_ids=sample_values(rows, "AUDIT_ID", samples_per_point),
                sample_record_ids=sample_values(rows, "RECORD_ID", samples_per_point),
                sample_newer_scores=sample_values(rows, "NEWER_SCORE", samples_per_point),
            )
        )
    out.sort(key=lambda item: (item.priority, -item.count))
    return out


def write_points_csv(path: Path, points: list[ConcretePoint]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(
            [
                "side",
                "priority",
                "issue",
                "pattern",
                "count",
                "share_pct",
                "action",
                "expected_effect",
                "risk",
                "sample_audit_ids",
                "sample_record_ids",
                "sample_newer_scores",
            ]
        )
        for point in points:
            writer.writerow(
                [
                    point.side,
                    point.priority,
                    point.issue,
                    point.pattern,
                    point.count,
                    f"{point.share_pct:.2f}",
                    point.action,
                    point.expected_effect,
                    point.risk,
                    point.sample_audit_ids,
                    point.sample_record_ids,
                    point.sample_newer_scores,
                ]
            )


def write_text_report(
    path: Path,
    title: str,
    points: list[ConcretePoint],
    audit_payload: dict[str, Any],
    snapshot_payload: dict[str, Any],
) -> None:
    pairs = audit_payload.get("PAIRS", {})
    new_positive = safe_int(pairs.get("NEW_POSITIVE", 0)) if isinstance(pairs, dict) else 0
    new_negative = safe_int(pairs.get("NEW_NEGATIVE", 0)) if isinstance(pairs, dict) else 0
    precision = safe_float(pairs.get("PRECISION", 0.0)) if isinstance(pairs, dict) else 0.0
    recall = safe_float(pairs.get("RECALL", 0.0)) if isinstance(pairs, dict) else 0.0

    lines: list[str] = []
    lines.append(title)
    lines.append("=" * len(title))
    lines.append("")
    lines.append("Audit context")
    lines.append(f"- NEW_POSITIVE: {new_positive}")
    lines.append(f"- NEW_NEGATIVE: {new_negative}")
    lines.append(f"- Pair precision: {precision:.5f}")
    lines.append(f"- Pair recall: {recall:.5f}")
    lines.append("")

    top_principles = top_snapshot_principles(snapshot_payload)
    if top_principles:
        lines.append("Top snapshot match principles")
        for key, count in top_principles:
            lines.append(f"- {key} -> {count}")
        lines.append("")

    lines.append("Concrete tuning/improvement points")
    for idx, point in enumerate(points, start=1):
        lines.append(f"{idx}. Priority P{point.priority} | {point.issue}")
        lines.append(f"   Pattern: {point.pattern}")
        lines.append(f"   Evidence: {point.count} cases ({point.share_pct:.2f}% of side-relevant mismatch bucket)")
        lines.append(f"   Action: {point.action}")
        lines.append(f"   Expected effect: {point.expected_effect}")
        lines.append(f"   Risk: {point.risk}")
        lines.append(f"   Sample AUDIT_ID: {point.sample_audit_ids or 'n/a'}")
        lines.append(f"   Sample RECORD_ID: {point.sample_record_ids or 'n/a'}")
        lines.append(f"   Sample NEWER_SCORE: {point.sample_newer_scores or 'n/a'}")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    snapshot_path = Path(args.snapshot).expanduser().resolve()
    audit_path = Path(args.audit).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not snapshot_path.exists():
        raise SystemExit(f"ERROR: snapshot file not found: {snapshot_path}")
    if not audit_path.exists():
        raise SystemExit(f"ERROR: audit file not found: {audit_path}")

    snapshot_payload = load_json(snapshot_path)
    audit_payload = load_json(audit_path)

    their_points = build_their_points(
        audit_payload=audit_payload,
        top_n=args.top_n,
        samples_per_point=args.samples_per_point,
    )
    our_points = build_our_points(
        audit_payload=audit_payload,
        top_n=args.top_n,
        samples_per_point=args.samples_per_point,
    )

    their_txt = output_dir / "their_tuning_recommendations.txt"
    our_txt = output_dir / "our_data_improvement_recommendations.txt"
    their_csv = output_dir / "their_concrete_tuning_points.csv"
    our_csv = output_dir / "our_concrete_improvement_points.csv"

    write_text_report(
        path=their_txt,
        title="Their Mismatch Tuning Recommendations",
        points=their_points,
        audit_payload=audit_payload,
        snapshot_payload=snapshot_payload,
    )
    write_text_report(
        path=our_txt,
        title="Our Mismatch Data Improvement Recommendations",
        points=our_points,
        audit_payload=audit_payload,
        snapshot_payload=snapshot_payload,
    )
    write_points_csv(their_csv, their_points)
    write_points_csv(our_csv, our_points)

    print(f"Snapshot input: {snapshot_path}")
    print(f"Audit input: {audit_path}")
    print(f"Their recommendations txt: {their_txt}")
    print(f"Our recommendations txt: {our_txt}")
    print(f"Their concrete points csv: {their_csv}")
    print(f"Our concrete points csv: {our_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

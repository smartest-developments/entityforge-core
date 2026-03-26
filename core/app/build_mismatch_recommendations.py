#!/usr/bin/env python3
"""Generate action-oriented mismatch diagnostics and recommendations from snapshot+audit JSON."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LossSignal:
    name: str
    count: int
    share_pct: str
    meaning: str


@dataclass(frozen=True)
class Recommendation:
    issue: str
    evidence: str
    recommended_change: str
    expected_benefit: str
    risk: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build two files from snapshot+audit that explain why matches are lost "
            "and what to tune/improve for Their side and Our side."
        )
    )
    parser.add_argument("--snapshot", required=True, help="Path to truthset_snapshot JSON/KJSON")
    parser.add_argument("--audit", required=True, help="Path to truthset_audit JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory")
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


def pct(part: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{(part / total) * 100:.1f}%"


def get_audit_category(audit_payload: dict[str, Any], category: str) -> dict[str, Any]:
    block = audit_payload.get("AUDIT", {})
    if not isinstance(block, dict):
        return {}
    value = block.get(category, {})
    return value if isinstance(value, dict) else {}


def get_subcategory_counts(category_payload: dict[str, Any]) -> dict[str, int]:
    sub = category_payload.get("SUB_CATEGORY", {})
    if not isinstance(sub, dict):
        return {}
    out: dict[str, int] = {}
    for name, payload in sub.items():
        if isinstance(payload, dict):
            out[str(name)] = safe_int(payload.get("COUNT", 0))
    return out


def flatten_rows(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "RECORD_ID" in value or "PRIOR_ID" in value or "NEWER_ID" in value:
            rows.append(value)
        for item in value.values():
            rows.extend(flatten_rows(item))
    elif isinstance(value, list):
        for item in value:
            rows.extend(flatten_rows(item))
    return rows


def top_snapshot_principles(snapshot_payload: dict[str, Any], limit: int = 5) -> list[tuple[str, int]]:
    principles = snapshot_payload.get("TOTALS", {}).get("MATCH", {}).get("PRINCIPLES", {})
    if not isinstance(principles, dict):
        return []
    pairs: list[tuple[str, int]] = []
    for key, value in principles.items():
        if isinstance(value, dict):
            pairs.append((str(key), safe_int(value.get("COUNT", 0))))
    pairs.sort(key=lambda item: item[1], reverse=True)
    return pairs[:limit]


def rank_recommendations(recs: list[Recommendation]) -> list[Recommendation]:
    priority = {
        "Many misses occur in 'related on' scenarios (near-match, not full match).": 1,
        "Broad 'multiple' split patterns indicate mixed failure modes.": 2,
        "True matches are split when TAX_ID disagrees or is noisy.": 3,
        "Ambiguous linkage paths block some valid merges.": 4,
        "Our baseline clusters are fragmented where resolver evidence can join records.": 1,
        "A large share of our misses falls into broad 'multiple' merge patterns.": 2,
        "Many merged cases already share strong identity signals including TAX_ID.": 3,
        "A relevant share of sampled merged records came from non-match placeholders.": 4,
        "Conflicting cluster behavior exists (split+merge in same audit areas).": 5,
    }
    return sorted(recs, key=lambda rec: priority.get(rec.issue, 999))


def build_their_analysis(audit_payload: dict[str, Any]) -> tuple[list[LossSignal], list[Recommendation]]:
    split_block = get_audit_category(audit_payload, "SPLIT")
    split_total = safe_int(split_block.get("COUNT", 0))
    split_sub = get_subcategory_counts(split_block)

    related_on = sum(count for name, count in split_sub.items() if name.startswith("related on:"))
    multiple = split_sub.get("multiple", 0)
    taxid_conflict = sum(count for name, count in split_sub.items() if "-TAX_ID" in name)
    ambiguous = sum(count for name, count in split_sub.items() if "Ambiguous" in name)

    signals = [
        LossSignal(
            name="Related-on split pressure",
            count=related_on,
            share_pct=pct(related_on, split_total),
            meaning="Many near-match cases are not crossing merge thresholds.",
        ),
        LossSignal(
            name="Mixed-pattern split pressure (multiple)",
            count=multiple,
            share_pct=pct(multiple, split_total),
            meaning="Split errors come from heterogeneous patterns, not one single rule.",
        ),
        LossSignal(
            name="Tax-ID conflict split pressure",
            count=taxid_conflict,
            share_pct=pct(taxid_conflict, split_total),
            meaning="Tax-id disagreement can block otherwise plausible merges.",
        ),
        LossSignal(
            name="Ambiguity split pressure",
            count=ambiguous,
            share_pct=pct(ambiguous, split_total),
            meaning="Ambiguous neighborhoods push conservative split outcomes.",
        ),
    ]

    if split_total <= 0:
        return (
            [LossSignal("SPLIT mismatch pressure", 0, "0.0%", "No major split mismatch detected.")],
            [
                Recommendation(
                    issue="No major SPLIT mismatches detected.",
                    evidence="SPLIT count: 0",
                    recommended_change="No immediate tuning change needed.",
                    expected_benefit="Keeps precision stable.",
                    risk="Low",
                )
            ],
        )

    recs: list[Recommendation] = []
    if related_on > 0:
        recs.append(
            Recommendation(
                issue="Many misses occur in 'related on' scenarios (near-match, not full match).",
                evidence=f"SPLIT 'related on': {related_on} ({pct(related_on, split_total)} of SPLIT).",
                recommended_change=(
                    "Increase tolerance for near-match evidence in targeted domains "
                    "(name variants, partial address, sparse email), not globally."
                ),
                expected_benefit="Higher recall on noisy real-world identities.",
                risk="Can reduce precision if applied too broadly.",
            )
        )
    if multiple > 0:
        recs.append(
            Recommendation(
                issue="Broad 'multiple' split patterns indicate mixed failure modes.",
                evidence=f"SPLIT 'multiple': {multiple} ({pct(multiple, split_total)} of SPLIT).",
                recommended_change="Create a calibration set from top 'multiple' cases and tune by subgroup.",
                expected_benefit="More reliable gain than one global threshold change.",
                risk="Needs a short calibration cycle.",
            )
        )
    if taxid_conflict > 0:
        recs.append(
            Recommendation(
                issue="True matches are split when TAX_ID disagrees or is noisy.",
                evidence=f"SPLIT with '-TAX_ID': {taxid_conflict} ({pct(taxid_conflict, split_total)} of SPLIT).",
                recommended_change="Reduce hard penalty on TAX_ID conflict when NAME+DOB+other IDs are strong.",
                expected_benefit="Recovers true matches blocked by tax-id quality issues.",
                risk="May introduce extra false positives.",
            )
        )
    if ambiguous > 0:
        recs.append(
            Recommendation(
                issue="Ambiguous linkage paths block some valid merges.",
                evidence=f"SPLIT marked 'Ambiguous': {ambiguous} ({pct(ambiguous, split_total)} of SPLIT).",
                recommended_change="Require one extra corroborating signal before final split in ambiguous cases.",
                expected_benefit="Recovers matches currently blocked by conservative ambiguity handling.",
                risk="Moderate if corroborating attributes are weak/noisy.",
            )
        )
    return signals, rank_recommendations(recs)


def build_our_analysis(audit_payload: dict[str, Any]) -> tuple[list[LossSignal], list[Recommendation]]:
    merge_block = get_audit_category(audit_payload, "MERGE")
    split_merge_block = get_audit_category(audit_payload, "SPLIT+MERGE")
    merge_total = safe_int(merge_block.get("COUNT", 0))
    split_merge_total = safe_int(split_merge_block.get("COUNT", 0))
    merge_sub = get_subcategory_counts(merge_block)

    merge_multiple = merge_sub.get("multiple", 0)
    merge_with_taxid = sum(count for name, count in merge_sub.items() if "+TAX_ID" in name)
    sample_rows = flatten_rows(merge_block.get("SUB_CATEGORY", {}))
    sample_total = len(sample_rows)
    sample_non_match_prior = sum(
        1 for row in sample_rows if str(row.get("PRIOR_ID", "")).startswith("non-match-")
    )

    signals = [
        LossSignal(
            name="Baseline fragmentation (MERGE)",
            count=merge_total,
            share_pct="n/a",
            meaning="Our source clusters are split where resolver can merge.",
        ),
        LossSignal(
            name="Mixed merge-pattern pressure (multiple)",
            count=merge_multiple,
            share_pct=pct(merge_multiple, merge_total) if merge_total > 0 else "0.0%",
            meaning="Data quality heterogeneity likely weakens baseline cluster consistency.",
        ),
        LossSignal(
            name="TAX_ID-linked merge opportunities",
            count=merge_with_taxid,
            share_pct=pct(merge_with_taxid, merge_total) if merge_total > 0 else "0.0%",
            meaning="Normalization/completeness gaps on key identifiers are likely present.",
        ),
        LossSignal(
            name="Conflicting cluster behavior (SPLIT+MERGE)",
            count=split_merge_total,
            share_pct="n/a",
            meaning="Cluster assignment logic may be inconsistent across similar records.",
        ),
    ]

    if merge_total <= 0 and split_merge_total <= 0:
        return (
            [LossSignal("MERGE/SPLIT+MERGE pressure", 0, "0.0%", "No major baseline mismatch detected.")],
            [
                Recommendation(
                    issue="No major MERGE or SPLIT+MERGE mismatches detected.",
                    evidence="MERGE count: 0, SPLIT+MERGE count: 0",
                    recommended_change="No immediate baseline/data change needed.",
                    expected_benefit="Stable baseline behavior.",
                    risk="Low",
                )
            ],
        )

    recs: list[Recommendation] = []
    if merge_total > 0:
        recs.append(
            Recommendation(
                issue="Our baseline clusters are fragmented where resolver evidence can join records.",
                evidence=f"MERGE mismatches: {merge_total}",
                recommended_change="Improve upstream cluster assignment logic (IPG/source grouping).",
                expected_benefit="Fewer false negatives in our baseline.",
                risk="Over-consolidation could add baseline false positives.",
            )
        )
    if merge_multiple > 0:
        recs.append(
            Recommendation(
                issue="A large share of our misses falls into broad 'multiple' merge patterns.",
                evidence=f"MERGE 'multiple': {merge_multiple} ({pct(merge_multiple, merge_total)} of MERGE).",
                recommended_change="Add pre-load data quality gate for names, addresses, and identifiers.",
                expected_benefit="Reduces heterogeneous baseline errors before resolution.",
                risk="Implementation effort and stricter input quality requirements.",
            )
        )
    if merge_with_taxid > 0:
        recs.append(
            Recommendation(
                issue="Many merged cases already share strong identity signals including TAX_ID.",
                evidence=f"MERGE with '+TAX_ID': {merge_with_taxid} ({pct(merge_with_taxid, merge_total)} of MERGE).",
                recommended_change="Strengthen TAX_ID/NAME/DOB normalization and completeness checks pre-load.",
                expected_benefit="More consistent baseline clusters and cleaner comparison.",
                risk="Needs strict normalization governance.",
            )
        )
    if sample_total > 0 and sample_non_match_prior > 0:
        recs.append(
            Recommendation(
                issue="A relevant share of sampled merged records came from non-match placeholders.",
                evidence=(
                    f"Sample MERGE rows with PRIOR_ID='non-match-*': {sample_non_match_prior}/{sample_total} "
                    f"({pct(sample_non_match_prior, sample_total)})."
                ),
                recommended_change="Increase completeness of source cluster IDs to reduce placeholder usage.",
                expected_benefit="Improves baseline comparability and reduces artificial mismatch noise.",
                risk="May require upstream source-system changes.",
            )
        )
    if split_merge_total > 0:
        recs.append(
            Recommendation(
                issue="Conflicting cluster behavior exists (split+merge in same audit areas).",
                evidence=f"SPLIT+MERGE mismatches: {split_merge_total}",
                recommended_change="Enforce deterministic clustering rules across similar records.",
                expected_benefit="Less contradictory baseline clustering behavior.",
                risk="Requires coordinated rule cleanup.",
            )
        )
    return signals, rank_recommendations(recs)


def render_report(
    title: str,
    audit_payload: dict[str, Any],
    snapshot_payload: dict[str, Any],
    signals: list[LossSignal],
    recommendations: list[Recommendation],
) -> str:
    pairs = audit_payload.get("PAIRS", {})
    pairs_new_positive = safe_int(pairs.get("NEW_POSITIVE", 0)) if isinstance(pairs, dict) else 0
    pairs_new_negative = safe_int(pairs.get("NEW_NEGATIVE", 0)) if isinstance(pairs, dict) else 0
    pairs_precision = pairs.get("PRECISION", "n/a") if isinstance(pairs, dict) else "n/a"
    pairs_recall = pairs.get("RECALL", "n/a") if isinstance(pairs, dict) else "n/a"

    lines: list[str] = []
    lines.append(title)
    lines.append("=" * len(title))
    lines.append("")
    lines.append("Audit context")
    lines.append(f"- NEW_POSITIVE: {pairs_new_positive}")
    lines.append(f"- NEW_NEGATIVE: {pairs_new_negative}")
    lines.append(f"- Pair precision: {pairs_precision}")
    lines.append(f"- Pair recall: {pairs_recall}")
    lines.append("")

    lines.append("Why matches are being lost")
    for signal in sorted(signals, key=lambda item: item.count, reverse=True):
        lines.append(f"- {signal.name}: {signal.count} ({signal.share_pct})")
        lines.append(f"  Meaning: {signal.meaning}")
    lines.append("")

    top_principles = top_snapshot_principles(snapshot_payload)
    if top_principles:
        lines.append("Top snapshot match principles (context)")
        for key, count in top_principles:
            lines.append(f"- {key} -> {count}")
        lines.append("")

    lines.append("What to change to improve matching")
    for idx, rec in enumerate(recommendations, start=1):
        lines.append(f"{idx}. Issue: {rec.issue}")
        lines.append(f"   Evidence: {rec.evidence}")
        lines.append(f"   Recommended change: {rec.recommended_change}")
        lines.append(f"   Expected benefit: {rec.expected_benefit}")
        lines.append(f"   Risk: {rec.risk}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


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

    their_signals, their_recs = build_their_analysis(audit_payload)
    our_signals, our_recs = build_our_analysis(audit_payload)

    their_path = output_dir / "their_tuning_recommendations.txt"
    our_path = output_dir / "our_data_improvement_recommendations.txt"

    their_path.write_text(
        render_report(
            title="Their Mismatch Tuning Recommendations",
            audit_payload=audit_payload,
            snapshot_payload=snapshot_payload,
            signals=their_signals,
            recommendations=their_recs,
        ),
        encoding="utf-8",
    )
    our_path.write_text(
        render_report(
            title="Our Mismatch Data Improvement Recommendations",
            audit_payload=audit_payload,
            snapshot_payload=snapshot_payload,
            signals=our_signals,
            recommendations=our_recs,
        ),
        encoding="utf-8",
    )

    print(f"Snapshot input: {snapshot_path}")
    print(f"Audit input: {audit_path}")
    print(f"Their recommendations: {their_path}")
    print(f"Our recommendations: {our_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

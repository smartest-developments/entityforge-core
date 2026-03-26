#!/usr/bin/env python3
"""Generate simple action-oriented mismatch recommendations from snapshot+audit JSON."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
            "Build two simple recommendation files from Senzing snapshot/audit outputs: "
            "1) Their tuning recommendations, 2) Our data-improvement recommendations."
        )
    )
    parser.add_argument(
        "--snapshot",
        required=True,
        help="Path to truthset snapshot JSON/KJSON (for context on top matching principles).",
    )
    parser.add_argument(
        "--audit",
        required=True,
        help="Path to truthset audit JSON output (from sz_audit).",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where recommendation files will be written.",
    )
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


def get_category(audit_payload: dict[str, Any], category: str) -> dict[str, Any]:
    audit_block = audit_payload.get("AUDIT", {})
    if not isinstance(audit_block, dict):
        return {}
    value = audit_block.get(category, {})
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


def flatten_dict_rows(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "RECORD_ID" in value or "PRIOR_ID" in value or "NEWER_ID" in value:
            rows.append(value)
        for item in value.values():
            rows.extend(flatten_dict_rows(item))
    elif isinstance(value, list):
        for item in value:
            rows.extend(flatten_dict_rows(item))
    return rows


def top_snapshot_principles(snapshot_payload: dict[str, Any], limit: int = 5) -> list[tuple[str, int]]:
    principles = (
        snapshot_payload.get("TOTALS", {})
        .get("MATCH", {})
        .get("PRINCIPLES", {})
    )
    if not isinstance(principles, dict):
        return []
    ranked: list[tuple[str, int]] = []
    for key, value in principles.items():
        if not isinstance(value, dict):
            continue
        ranked.append((str(key), safe_int(value.get("COUNT", 0))))
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:limit]


def pct(part: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{(part / total) * 100:.1f}%"


def build_their_recommendations(audit_payload: dict[str, Any]) -> list[Recommendation]:
    split_block = get_category(audit_payload, "SPLIT")
    split_total = safe_int(split_block.get("COUNT", 0))
    split_sub = get_subcategory_counts(split_block)

    taxid_conflict = sum(count for name, count in split_sub.items() if "-TAX_ID" in name)
    ambiguous = sum(count for name, count in split_sub.items() if "Ambiguous" in name)
    related_on = sum(count for name, count in split_sub.items() if name.startswith("related on:"))
    multiple = split_sub.get("multiple", 0)

    recs: list[Recommendation] = []
    if split_total <= 0:
        recs.append(
            Recommendation(
                issue="No major SPLIT mismatches detected in audit.",
                evidence="SPLIT count: 0",
                recommended_change="Keep current matching strictness; optimize only after new evidence.",
                expected_benefit="Stable precision with no unnecessary retuning.",
                risk="Low",
            )
        )
        return recs

    if taxid_conflict > 0:
        recs.append(
            Recommendation(
                issue="True matches are split when TAX_ID disagrees or is noisy.",
                evidence=f"SPLIT cases with '-TAX_ID': {taxid_conflict} ({pct(taxid_conflict, split_total)} of SPLIT).",
                recommended_change=(
                    "Tune to reduce hard penalty on TAX_ID conflicts for records with strong corroboration "
                    "(e.g., NAME+DOB+other stable identifiers)."
                ),
                expected_benefit="Higher recall on typo/noisy tax-id populations.",
                risk="May increase false positives if over-relaxed.",
            )
        )

    if ambiguous > 0:
        recs.append(
            Recommendation(
                issue="Ambiguous linkage paths block some valid merges.",
                evidence=f"SPLIT cases marked 'Ambiguous': {ambiguous} ({pct(ambiguous, split_total)} of SPLIT).",
                recommended_change=(
                    "Tune ambiguity handling by requiring one additional corroborating attribute "
                    "(address/email/other-id) before final split."
                ),
                expected_benefit="Recover missed matches currently blocked by conservative ambiguity rules.",
                risk="Moderate if weak corroborators are low quality.",
            )
        )

    if related_on > 0:
        recs.append(
            Recommendation(
                issue="Many misses occur in 'related on' scenarios (near-match, not full match).",
                evidence=f"SPLIT 'related on' subcategories: {related_on} ({pct(related_on, split_total)} of SPLIT).",
                recommended_change=(
                    "Increase tolerance for near-match patterns in targeted domains "
                    "(e.g., name variants, partial address, sparse email)."
                ),
                expected_benefit="Better recall for real-world noisy identity variations.",
                risk="Could reduce precision if applied globally; prefer scoped tuning.",
            )
        )

    if multiple > 0:
        recs.append(
            Recommendation(
                issue="Broad 'multiple' split patterns indicate mixed failure modes.",
                evidence=f"SPLIT subcategory 'multiple': {multiple} ({pct(multiple, split_total)} of SPLIT).",
                recommended_change=(
                    "Run a focused calibration set on top 'multiple' examples to separate strictness issues "
                    "from data quality issues before changing global thresholds."
                ),
                expected_benefit="Safer, data-driven tuning changes.",
                risk="Requires short calibration cycle before rollout.",
            )
        )

    return recs


def build_our_recommendations(audit_payload: dict[str, Any]) -> list[Recommendation]:
    merge_block = get_category(audit_payload, "MERGE")
    split_merge_block = get_category(audit_payload, "SPLIT+MERGE")
    merge_total = safe_int(merge_block.get("COUNT", 0))
    split_merge_total = safe_int(split_merge_block.get("COUNT", 0))
    merge_sub = get_subcategory_counts(merge_block)

    merge_multiple = merge_sub.get("multiple", 0)
    merge_with_taxid = sum(count for name, count in merge_sub.items() if "+TAX_ID" in name)

    # Sample-driven indicator: how often PRIOR_ID looks like our placeholder non-match.
    sample_rows = flatten_dict_rows(merge_block.get("SUB_CATEGORY", {}))
    sample_total = len(sample_rows)
    sample_non_match_prior = sum(
        1
        for row in sample_rows
        if str(row.get("PRIOR_ID", "")).startswith("non-match-")
    )

    recs: list[Recommendation] = []
    if merge_total <= 0 and split_merge_total <= 0:
        recs.append(
            Recommendation(
                issue="No major MERGE or SPLIT+MERGE mismatches detected.",
                evidence="MERGE count: 0, SPLIT+MERGE count: 0",
                recommended_change="No immediate baseline/data change required.",
                expected_benefit="Keeps current behavior stable.",
                risk="Low",
            )
        )
        return recs

    if merge_total > 0:
        recs.append(
            Recommendation(
                issue="Our baseline clusters are fragmented where Senzing finds clear joins.",
                evidence=f"MERGE mismatches: {merge_total}",
                recommended_change=(
                    "Improve upstream cluster assignment logic (IPG/source grouping), "
                    "especially where duplicate records should share one cluster id."
                ),
                expected_benefit="Fewer false negatives in our baseline and better truthset consistency.",
                risk="If over-consolidated, baseline may add false positives.",
            )
        )

    if merge_with_taxid > 0:
        recs.append(
            Recommendation(
                issue="Many merged cases already share strong identity signals including TAX_ID.",
                evidence=f"MERGE subcategories containing '+TAX_ID': {merge_with_taxid} ({pct(merge_with_taxid, merge_total)} of MERGE).",
                recommended_change=(
                    "Strengthen pre-load normalization on TAX_ID/NAME/DOB formatting and ensure these fields are consistently populated."
                ),
                expected_benefit="More stable baseline clusters and easier alignment with Senzing output.",
                risk="Needs strict data cleaning governance to avoid accidental rewrites.",
            )
        )

    if merge_multiple > 0:
        recs.append(
            Recommendation(
                issue="A large share of our misses falls into broad 'multiple' merge patterns.",
                evidence=f"MERGE subcategory 'multiple': {merge_multiple} ({pct(merge_multiple, merge_total)} of MERGE).",
                recommended_change=(
                    "Create a pre-load data quality gate for top noisy dimensions "
                    "(name variants, address standardization, inconsistent IDs)."
                ),
                expected_benefit="Reduces heterogeneous baseline errors before entity resolution.",
                risk="Initial implementation effort and potential stricter rejection of low-quality rows.",
            )
        )

    if sample_total > 0 and sample_non_match_prior > 0:
        recs.append(
            Recommendation(
                issue="A relevant share of sampled merged records came from non-match placeholders.",
                evidence=(
                    f"Sampled rows with PRIOR_ID='non-match-*': {sample_non_match_prior}/{sample_total} "
                    f"({pct(sample_non_match_prior, sample_total)} in sampled MERGE rows)."
                ),
                recommended_change=(
                    "Increase completeness of source cluster IDs in input (reduce missing cluster assignments)."
                ),
                expected_benefit="Improves baseline comparability and reduces artificial mismatch noise.",
                risk="May require upstream source-system changes.",
            )
        )

    if split_merge_total > 0:
        recs.append(
            Recommendation(
                issue="Conflicting cluster behavior exists (split+merge in same audit areas).",
                evidence=f"SPLIT+MERGE mismatches: {split_merge_total}",
                recommended_change=(
                    "Review inconsistent cluster labels for the same logical population "
                    "and enforce deterministic clustering rules before load."
                ),
                expected_benefit="Less contradictory baseline behavior across similar records.",
                risk="Requires coordinated rule cleanup across teams.",
            )
        )

    return recs


def render_recommendations(
    title: str,
    audit_payload: dict[str, Any],
    snapshot_payload: dict[str, Any],
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

    top_principles = top_snapshot_principles(snapshot_payload)
    if top_principles:
        lines.append("Top snapshot match principles (context)")
        for key, count in top_principles:
            lines.append(f"- {key} -> {count}")
        lines.append("")

    lines.append("Recommended actions")
    for index, rec in enumerate(recommendations, start=1):
        lines.append(f"{index}. Issue: {rec.issue}")
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

    their_recs = build_their_recommendations(audit_payload)
    our_recs = build_our_recommendations(audit_payload)

    their_path = output_dir / "their_tuning_recommendations.txt"
    our_path = output_dir / "our_data_improvement_recommendations.txt"

    their_text = render_recommendations(
        title="Their Mismatch Tuning Recommendations",
        audit_payload=audit_payload,
        snapshot_payload=snapshot_payload,
        recommendations=their_recs,
    )
    our_text = render_recommendations(
        title="Our Mismatch Data Improvement Recommendations",
        audit_payload=audit_payload,
        snapshot_payload=snapshot_payload,
        recommendations=our_recs,
    )

    their_path.write_text(their_text, encoding="utf-8")
    our_path.write_text(our_text, encoding="utf-8")

    print(f"Snapshot input: {snapshot_path}")
    print(f"Audit input: {audit_path}")
    print(f"Their recommendations: {their_path}")
    print(f"Our recommendations: {our_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

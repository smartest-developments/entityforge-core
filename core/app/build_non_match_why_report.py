#!/usr/bin/env python3
"""Build a run-local non-match analysis bundle from audit, snapshot, and explain."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from run_senzing_end_to_end import extract_reason_summary, init_g2_engine, run_sdk_why_records


@dataclass(frozen=True)
class SnapshotRecord:
    resolved_entity_id: str
    match_level: str
    match_key: str


@dataclass(frozen=True)
class PairKey:
    cluster_id: str
    left_record_id: str
    right_record_id: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a run-local non-match analysis report.")
    parser.add_argument("--run-output-dir", required=True, help="Run output bundle directory")
    parser.add_argument("--project-dir", default=None, help="Senzing project directory for whyRecords")
    parser.add_argument("--output-dir", default=None, help="Target directory (default: <run-output-dir>/non_match_why)")
    parser.add_argument("--why-pair-limit", type=int, default=500, help="Maximum non-match pairs to explain with whyRecords (default: 500, 0 = skip)")
    parser.add_argument("--data-source", default="PARTNERS", help="Expected DATA_SOURCE value (default: PARTNERS)")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as infile:
        return list(csv.DictReader(infile))


def flatten_features(record: dict[str, Any]) -> dict[str, str]:
    features = record.get("FEATURES")
    flattened: dict[str, str] = {
        "record_id": str(record.get("RECORD_ID") or "").strip(),
        "data_source": str(record.get("DATA_SOURCE") or "").strip(),
        "source_ipg_id": str(record.get("SOURCE_IPG_ID") or "").strip(),
        "record_type": "",
        "name_full": "",
        "name_first": "",
        "name_last": "",
        "date_of_birth": "",
        "nationality": "",
        "addr_line1": "",
        "addr_city": "",
        "addr_postal_code": "",
        "addr_country": "",
        "tax_id_number": "",
        "lei_number": "",
        "website_address": "",
        "email_address": "",
        "other_ids": "",
    }
    other_ids: list[str] = []
    if not isinstance(features, list):
        flattened["raw_record_json"] = json.dumps(record, ensure_ascii=False)
        return flattened

    for item in features:
        if not isinstance(item, dict):
            continue
        if item.get("RECORD_TYPE") and not flattened["record_type"]:
            flattened["record_type"] = str(item.get("RECORD_TYPE"))
        if item.get("NAME_FULL") and not flattened["name_full"]:
            flattened["name_full"] = str(item.get("NAME_FULL"))
        if item.get("NAME_FIRST") and not flattened["name_first"]:
            flattened["name_first"] = str(item.get("NAME_FIRST"))
        if item.get("NAME_LAST") and not flattened["name_last"]:
            flattened["name_last"] = str(item.get("NAME_LAST"))
        if item.get("DATE_OF_BIRTH") and not flattened["date_of_birth"]:
            flattened["date_of_birth"] = str(item.get("DATE_OF_BIRTH"))
        if item.get("NATIONALITY") and not flattened["nationality"]:
            flattened["nationality"] = str(item.get("NATIONALITY"))
        if item.get("ADDR_LINE1") and not flattened["addr_line1"]:
            flattened["addr_line1"] = str(item.get("ADDR_LINE1"))
        if item.get("ADDR_CITY") and not flattened["addr_city"]:
            flattened["addr_city"] = str(item.get("ADDR_CITY"))
        if item.get("ADDR_POSTAL_CODE") and not flattened["addr_postal_code"]:
            flattened["addr_postal_code"] = str(item.get("ADDR_POSTAL_CODE"))
        if item.get("ADDR_COUNTRY") and not flattened["addr_country"]:
            flattened["addr_country"] = str(item.get("ADDR_COUNTRY"))
        if item.get("TAX_ID_NUMBER") and not flattened["tax_id_number"]:
            flattened["tax_id_number"] = str(item.get("TAX_ID_NUMBER"))
        if item.get("LEI_NUMBER") and not flattened["lei_number"]:
            flattened["lei_number"] = str(item.get("LEI_NUMBER"))
        if item.get("WEBSITE_ADDRESS") and not flattened["website_address"]:
            flattened["website_address"] = str(item.get("WEBSITE_ADDRESS"))
        if item.get("EMAIL_ADDRESS") and not flattened["email_address"]:
            flattened["email_address"] = str(item.get("EMAIL_ADDRESS"))
        other_id_type = str(item.get("OTHER_ID_TYPE") or "").strip()
        other_id_number = str(item.get("OTHER_ID_NUMBER") or "").strip()
        if other_id_type and other_id_number:
            other_ids.append(f"{other_id_type}:{other_id_number}")
    flattened["other_ids"] = " | ".join(other_ids)
    return flattened


def load_mapped_records(path: Path) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as infile:
        for line in infile:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            record_id = str(payload.get("RECORD_ID") or "").strip()
            if not record_id:
                continue
            records[record_id] = flatten_features(payload)
    return records


def load_snapshot_map(path: Path) -> dict[str, SnapshotRecord]:
    snapshot: dict[str, SnapshotRecord] = {}
    for row in load_csv_rows(path):
        record_id = str(row.get("RECORD_ID") or "").strip()
        if not record_id or record_id in snapshot:
            continue
        snapshot[record_id] = SnapshotRecord(
            resolved_entity_id=str(row.get("RESOLVED_ENTITY_ID") or "").strip(),
            match_level=str(row.get("MATCH_LEVEL") or "").strip(),
            match_key=str(row.get("MATCH_KEY") or "").strip(),
        )
    return snapshot


def load_truthset_key(path: Path) -> dict[str, list[str]]:
    clusters: dict[str, list[str]] = defaultdict(list)
    for row in load_csv_rows(path):
        cluster_id = str(row.get("CLUSTER_ID") or "").strip()
        record_id = str(row.get("RECORD_ID") or "").strip()
        if not cluster_id or not record_id:
            continue
        clusters[cluster_id].append(record_id)
    return dict(clusters)


def load_audit_by_record(path: Path) -> dict[str, dict[str, set[str]]]:
    by_record: dict[str, dict[str, set[str]]] = {}
    for row in load_csv_rows(path):
        record_id = str(row.get("RECORD_ID") or "").strip()
        if not record_id:
            continue
        current = by_record.setdefault(
            record_id,
            {
                "audit_ids": set(),
                "audit_categories": set(),
                "audit_results": set(),
                "prior_ids": set(),
                "newer_ids": set(),
                "newer_scores": set(),
            },
        )
        for key, source in [
            ("audit_ids", "AUDIT_ID"),
            ("audit_categories", "AUDIT_CATEGORY"),
            ("audit_results", "AUDIT_RESULT"),
            ("prior_ids", "PRIOR_ID"),
            ("newer_ids", "NEWER_ID"),
            ("newer_scores", "NEWER_SCORE"),
        ]:
            value = str(row.get(source) or "").strip()
            if value:
                current[key].add(value)
    return by_record


def compute_cluster_cases(
    expected_clusters: dict[str, list[str]],
    snapshot_by_record: dict[str, SnapshotRecord],
    audit_by_record: dict[str, dict[str, set[str]]],
    mapped_by_record: dict[str, dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[PairKey]]:
    cluster_rows: list[dict[str, Any]] = []
    record_rows: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    why_targets: list[PairKey] = []

    for cluster_id, record_ids in sorted(expected_clusters.items()):
        if len(record_ids) < 2:
            continue
        entities: dict[str, list[str]] = defaultdict(list)
        for record_id in record_ids:
            snapshot = snapshot_by_record.get(record_id)
            resolved_entity_id = snapshot.resolved_entity_id if snapshot else ""
            entities[resolved_entity_id].append(record_id)
        non_empty_entities = {entity_id: ids for entity_id, ids in entities.items() if entity_id}
        if len(non_empty_entities) <= 1:
            continue

        sorted_entities = sorted(non_empty_entities.items(), key=lambda item: (item[0], item[1]))
        non_match_pair_count = 0
        first_pair: PairKey | None = None
        for index, (_, left_ids) in enumerate(sorted_entities):
            for _, right_ids in sorted_entities[index + 1 :]:
                non_match_pair_count += len(left_ids) * len(right_ids)
                for left_id in left_ids:
                    for right_id in right_ids:
                        left_info = mapped_by_record.get(left_id, {})
                        right_info = mapped_by_record.get(right_id, {})
                        left_snapshot = snapshot_by_record.get(left_id)
                        right_snapshot = snapshot_by_record.get(right_id)
                        pair = PairKey(cluster_id=cluster_id, left_record_id=left_id, right_record_id=right_id)
                        if first_pair is None:
                            first_pair = pair
                        pair_rows.append(
                            {
                                "cluster_id": cluster_id,
                                "left_record_id": left_id,
                                "right_record_id": right_id,
                                "left_resolved_entity_id": left_snapshot.resolved_entity_id if left_snapshot else "",
                                "right_resolved_entity_id": right_snapshot.resolved_entity_id if right_snapshot else "",
                                "left_match_level": left_snapshot.match_level if left_snapshot else "",
                                "right_match_level": right_snapshot.match_level if right_snapshot else "",
                                "left_match_key": left_snapshot.match_key if left_snapshot else "",
                                "right_match_key": right_snapshot.match_key if right_snapshot else "",
                                "left_name_full": left_info.get("name_full", ""),
                                "right_name_full": right_info.get("name_full", ""),
                                "left_tax_id_number": left_info.get("tax_id_number", ""),
                                "right_tax_id_number": right_info.get("tax_id_number", ""),
                                "left_source_ipg_id": left_info.get("source_ipg_id", ""),
                                "right_source_ipg_id": right_info.get("source_ipg_id", ""),
                                "why_records_attempted": 0,
                                "why_records_ok": 0,
                                "why_records_method": "",
                                "why_records_reason_summary": "",
                                "why_records_error": "",
                            }
                        )

        if first_pair is not None:
            why_targets.append(first_pair)

        audit_categories: set[str] = set()
        audit_results: set[str] = set()
        for record_id in record_ids:
            audit_info = audit_by_record.get(record_id, {})
            audit_categories.update(audit_info.get("audit_categories", set()))
            audit_results.update(audit_info.get("audit_results", set()))
            record_info = mapped_by_record.get(record_id, {})
            snapshot = snapshot_by_record.get(record_id)
            record_rows.append(
                {
                    "cluster_id": cluster_id,
                    "record_id": record_id,
                    "resolved_entity_id": snapshot.resolved_entity_id if snapshot else "",
                    "match_level": snapshot.match_level if snapshot else "",
                    "match_key": snapshot.match_key if snapshot else "",
                    "audit_categories": " | ".join(sorted(audit_info.get("audit_categories", set()))),
                    "audit_results": " | ".join(sorted(audit_info.get("audit_results", set()))),
                    "audit_ids": " | ".join(sorted(audit_info.get("audit_ids", set()))),
                    "source_ipg_id": record_info.get("source_ipg_id", ""),
                    "record_type": record_info.get("record_type", ""),
                    "name_full": record_info.get("name_full", ""),
                    "name_first": record_info.get("name_first", ""),
                    "name_last": record_info.get("name_last", ""),
                    "date_of_birth": record_info.get("date_of_birth", ""),
                    "nationality": record_info.get("nationality", ""),
                    "addr_line1": record_info.get("addr_line1", ""),
                    "addr_city": record_info.get("addr_city", ""),
                    "addr_postal_code": record_info.get("addr_postal_code", ""),
                    "addr_country": record_info.get("addr_country", ""),
                    "tax_id_number": record_info.get("tax_id_number", ""),
                    "lei_number": record_info.get("lei_number", ""),
                    "website_address": record_info.get("website_address", ""),
                    "email_address": record_info.get("email_address", ""),
                    "other_ids": record_info.get("other_ids", ""),
                }
            )

        cluster_rows.append(
            {
                "cluster_id": cluster_id,
                "expected_record_count": len(record_ids),
                "senzing_entity_count": len(non_empty_entities),
                "non_match_pair_count": non_match_pair_count,
                "record_ids": " | ".join(record_ids),
                "resolved_entity_ids": " | ".join(entity_id for entity_id, _ in sorted_entities),
                "audit_categories": " | ".join(sorted(audit_categories)),
                "audit_results": " | ".join(sorted(audit_results)),
            }
        )

    cluster_rows.sort(key=lambda row: (-int(row["non_match_pair_count"]), str(row["cluster_id"])))
    pair_rows.sort(key=lambda row: (str(row["cluster_id"]), str(row["left_record_id"]), str(row["right_record_id"])))
    record_rows.sort(key=lambda row: (str(row["cluster_id"]), str(row["record_id"])))
    return cluster_rows, record_rows, pair_rows, why_targets


def extend_why_targets(why_targets: list[PairKey], pair_rows: list[dict[str, Any]], limit: int) -> list[PairKey]:
    if limit <= 0:
        return []
    selected: list[PairKey] = []
    seen: set[tuple[str, str, str]] = set()
    for pair in why_targets:
        key = (pair.cluster_id, pair.left_record_id, pair.right_record_id)
        if key in seen:
            continue
        selected.append(pair)
        seen.add(key)
        if len(selected) >= limit:
            return selected
    for row in pair_rows:
        key = (str(row["cluster_id"]), str(row["left_record_id"]), str(row["right_record_id"]))
        if key in seen:
            continue
        selected.append(PairKey(cluster_id=key[0], left_record_id=key[1], right_record_id=key[2]))
        seen.add(key)
        if len(selected) >= limit:
            break
    return selected


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def build_html(output_dir: Path, cluster_rows: list[dict[str, Any]], record_rows: list[dict[str, Any]], explained_pair_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    html_path = output_dir / "index.html"
    payload = {
        "summary": summary,
        "clusters": cluster_rows,
        "records": record_rows,
        "explained_pairs": explained_pair_rows,
    }
    html_path.write_text(
        """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Non-Match WHY Report</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #10233a; }
      main { max-width: 1440px; margin: 0 auto; padding: 20px; }
      h1, h2 { margin: 0 0 12px; }
      .panel { background: #fff; border: 1px solid #d6deea; border-radius: 10px; padding: 16px; margin-bottom: 16px; }
      .meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin-top: 12px; }
      .metric { background: #f8fbff; border: 1px solid #e0e8f2; border-radius: 8px; padding: 10px; }
      .metric .k { font-size: 12px; color: #5a6f8a; display: block; }
      .metric .v { font-size: 20px; font-weight: 700; display: block; margin-top: 4px; }
      .toolbar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }
      input { min-width: 260px; padding: 8px 10px; border-radius: 8px; border: 1px solid #b9c7d8; }
      table { width: 100%; border-collapse: collapse; font-size: 13px; }
      th, td { text-align: left; padding: 8px; border-bottom: 1px solid #e7edf5; vertical-align: top; }
      th { background: #f3f7fc; position: sticky; top: 0; }
      .table-wrap { max-height: 420px; overflow: auto; border: 1px solid #dde6f0; border-radius: 8px; }
      .note { color: #5a6f8a; font-size: 13px; }
      a { color: #0b5cab; }
    </style>
  </head>
  <body>
    <main>
      <section class="panel">
        <h1>Non-Match WHY Report</h1>
        <p class="note">This bundle focuses on records expected to match under the input clustering but split by Senzing in the audit snapshot.</p>
        <div id="summary" class="meta"></div>
      </section>
      <section class="panel">
        <h2>Split Clusters</h2>
        <div class="toolbar">
          <input id="clusterFilter" placeholder="Filter clusters, audit categories, entity ids">
        </div>
        <div class="table-wrap"><table id="clusterTable"></table></div>
      </section>
      <section class="panel">
        <h2>Records Involved</h2>
        <div class="toolbar">
          <input id="recordFilter" placeholder="Filter by cluster, record id, name, tax id, match key">
        </div>
        <div class="table-wrap"><table id="recordTable"></table></div>
      </section>
      <section class="panel">
        <h2>Explained Non-Match Pairs</h2>
        <p class="note">The full pair list remains in CSV. This table shows the pairs where whyRecords was executed.</p>
        <div class="toolbar">
          <input id="pairFilter" placeholder="Filter by cluster, record ids, reason summary, errors">
        </div>
        <div class="table-wrap"><table id="pairTable"></table></div>
      </section>
      <section class="panel">
        <h2>Files</h2>
        <ul>
          <li><a href="./summary.md">summary.md</a></li>
          <li><a href="./cluster_summary.csv">cluster_summary.csv</a></li>
          <li><a href="./record_membership.csv">record_membership.csv</a></li>
          <li><a href="./non_match_pairs.csv">non_match_pairs.csv</a></li>
          <li><a href="./explained_non_match_pairs.csv">explained_non_match_pairs.csv</a></li>
          <li><a href="./why_results.jsonl">why_results.jsonl</a></li>
        </ul>
      </section>
    </main>
    <script>
      const DATA = """
        + json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        + """;

      function renderSummary(summary) {
        const container = document.getElementById("summary");
        const items = [
          ["Clusters split by Senzing", summary.split_cluster_count],
          ["Records involved", summary.record_count],
          ["Non-match pairs", summary.non_match_pair_count],
          ["whyRecords attempted", summary.why_pairs_attempted],
          ["whyRecords succeeded", summary.why_pairs_ok],
          ["why coverage", summary.why_coverage_pct + "%"]
        ];
        container.innerHTML = items.map(([k, v]) => `<div class="metric"><span class="k">${k}</span><span class="v">${v}</span></div>`).join("");
      }

      function filterRows(rows, query) {
        if (!query) return rows;
        const q = query.toLowerCase();
        return rows.filter((row) => Object.values(row).some((value) => String(value || "").toLowerCase().includes(q)));
      }

      function renderTable(tableId, rows, columns) {
        const table = document.getElementById(tableId);
        const head = "<thead><tr>" + columns.map((col) => `<th>${col}</th>`).join("") + "</tr></thead>";
        const body = "<tbody>" + rows.map((row) => "<tr>" + columns.map((col) => `<td>${String(row[col] ?? "")}</td>`).join("") + "</tr>").join("") + "</tbody>";
        table.innerHTML = head + body;
      }

      function setupFilter(inputId, tableId, rows, columns) {
        const input = document.getElementById(inputId);
        const rerender = () => renderTable(tableId, filterRows(rows, input.value), columns);
        input.addEventListener("input", rerender);
        rerender();
      }

      renderSummary(DATA.summary);
      setupFilter("clusterFilter", "clusterTable", DATA.clusters, ["cluster_id", "expected_record_count", "senzing_entity_count", "non_match_pair_count", "resolved_entity_ids", "audit_categories", "audit_results"]);
      setupFilter("recordFilter", "recordTable", DATA.records, ["cluster_id", "record_id", "resolved_entity_id", "match_key", "name_full", "tax_id_number", "audit_categories", "audit_results"]);
      setupFilter("pairFilter", "pairTable", DATA.explained_pairs, ["cluster_id", "left_record_id", "right_record_id", "left_resolved_entity_id", "right_resolved_entity_id", "why_records_ok", "why_records_method", "why_records_reason_summary", "why_records_error"]);
    </script>
  </body>
</html>
""",
        encoding="utf-8",
    )


def write_summary_md(path: Path, summary: dict[str, Any], audit_json: dict[str, Any], why_engine_status: str) -> None:
    entity = audit_json.get("ENTITY", {}) if isinstance(audit_json.get("ENTITY"), dict) else {}
    pairs = audit_json.get("PAIRS", {}) if isinstance(audit_json.get("PAIRS"), dict) else {}
    audit = audit_json.get("AUDIT", {}) if isinstance(audit_json.get("AUDIT"), dict) else {}
    lines = [
        "# Non-Match WHY Report",
        "",
        "## Summary",
        "",
        f"- Split clusters detected: {summary['split_cluster_count']}",
        f"- Records involved in split clusters: {summary['record_count']}",
        f"- Non-match pairs (expected same cluster, different Senzing entity): {summary['non_match_pair_count']}",
        f"- whyRecords attempted: {summary['why_pairs_attempted']}",
        f"- whyRecords succeeded: {summary['why_pairs_ok']}",
        f"- why coverage: {summary['why_coverage_pct']}%",
        f"- why engine status: {why_engine_status}",
        "",
        "## Audit Totals",
        "",
        f"- Pair precision: {pairs.get('PRECISION', 'N/A')}",
        f"- Pair recall: {pairs.get('RECALL', 'N/A')}",
        f"- Pair F1: {pairs.get('F1-SCORE', 'N/A')}",
        f"- Same positives: {pairs.get('SAME_POSITIVE', 'N/A')}",
        f"- New positives: {pairs.get('NEW_POSITIVE', 'N/A')}",
        f"- New negatives: {pairs.get('NEW_NEGATIVE', 'N/A')}",
        f"- Prior entities: {entity.get('PRIOR_COUNT', 'N/A')}",
        f"- New entities: {entity.get('NEWER_COUNT', 'N/A')}",
        f"- Audit split count: {audit.get('SPLIT', {}).get('COUNT', 'N/A') if isinstance(audit.get('SPLIT'), dict) else 'N/A'}",
        f"- Audit merge count: {audit.get('MERGE', {}).get('COUNT', 'N/A') if isinstance(audit.get('MERGE'), dict) else 'N/A'}",
        "",
        "## Files",
        "",
        "- `cluster_summary.csv`: one row per expected cluster split by Senzing",
        "- `record_membership.csv`: all records involved in those split clusters",
        "- `non_match_pairs.csv`: exhaustive pair-level false negatives",
        "- `explained_non_match_pairs.csv`: pair rows where whyRecords was executed",
        "- `why_results.jsonl`: raw whyRecords payloads",
        "- `index.html`: filtered local report",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    run_output_dir = Path(args.run_output_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else run_output_dir / "non_match_why"
    technical_dir = run_output_dir / "technical output"
    audit_dir = run_output_dir / "senzing_audit"
    run_summary_json = technical_dir / "run_summary.json"
    mapped_output_jsonl = technical_dir / "mapped_output.jsonl"
    truthset_key_csv = audit_dir / "truthset_key.csv"
    truthset_snapshot_csv = audit_dir / "truthset_snapshot.csv"
    truthset_audit_csv = audit_dir / "truthset_audit.csv"
    truthset_audit_json = audit_dir / "truthset_audit.json"

    for required in [run_summary_json, mapped_output_jsonl, truthset_key_csv, truthset_snapshot_csv, truthset_audit_csv]:
        if not required.exists():
            raise FileNotFoundError(f"Required input not found: {required}")

    output_dir.mkdir(parents=True, exist_ok=True)

    run_summary = read_json(run_summary_json)
    project_dir = (
        Path(args.project_dir).expanduser().resolve()
        if args.project_dir
        else Path(str(run_summary.get("project_dir") or "")).expanduser()
    )
    if str(project_dir).startswith("/runtime/"):
        project_dir = (run_output_dir.parent.parent.parent / str(project_dir).removeprefix("/runtime/")).resolve()
    mapped_by_record = load_mapped_records(mapped_output_jsonl)
    snapshot_by_record = load_snapshot_map(truthset_snapshot_csv)
    expected_clusters = load_truthset_key(truthset_key_csv)
    audit_by_record = load_audit_by_record(truthset_audit_csv)
    cluster_rows, record_rows, pair_rows, seed_why_targets = compute_cluster_cases(
        expected_clusters=expected_clusters,
        snapshot_by_record=snapshot_by_record,
        audit_by_record=audit_by_record,
        mapped_by_record=mapped_by_record,
    )

    pair_index = {
        (str(row["cluster_id"]), str(row["left_record_id"]), str(row["right_record_id"])): row for row in pair_rows
    }
    selected_why_targets = extend_why_targets(seed_why_targets, pair_rows, args.why_pair_limit)
    why_results: list[dict[str, Any]] = []
    why_engine_status = "skipped"

    if selected_why_targets and project_dir.exists():
        project_setup_env = Path(str(run_summary.get("project_setup_env") or "")).expanduser()
        if not project_setup_env.exists():
            project_setup_env = project_dir / "setupEnv"
        g2 = None
        factory = None
        try:
            g2, factory, engine_details = init_g2_engine(project_dir, project_setup_env)
            why_engine_status = "ok" if g2 else f"init_failed: {engine_details.get('error') or 'unknown'}"
            if g2:
                for pair in selected_why_targets:
                    result = run_sdk_why_records(g2, args.data_source, pair.left_record_id, args.data_source, pair.right_record_id)
                    enriched = {
                        "cluster_id": pair.cluster_id,
                        "left_record_id": pair.left_record_id,
                        "right_record_id": pair.right_record_id,
                        "ok": bool(result.get("ok")),
                        "method": result.get("method"),
                        "reason_summary": extract_reason_summary(result.get("output_json"), result.get("output_text")),
                        "error": result.get("error"),
                        "output_json": result.get("output_json"),
                        "output_text": result.get("output_text"),
                    }
                    why_results.append(enriched)
                    row = pair_index.get((pair.cluster_id, pair.left_record_id, pair.right_record_id))
                    if row is not None:
                        row["why_records_attempted"] = 1
                        row["why_records_ok"] = 1 if enriched["ok"] else 0
                        row["why_records_method"] = str(enriched.get("method") or "")
                        row["why_records_reason_summary"] = str(enriched.get("reason_summary") or "")
                        row["why_records_error"] = str(enriched.get("error") or "")
        finally:
            try:
                if g2 and hasattr(g2, "destroy"):
                    g2.destroy()
            except Exception:
                pass
            try:
                if factory and hasattr(factory, "destroy"):
                    factory.destroy()
            except Exception:
                pass

    explained_pair_rows = [row for row in pair_rows if int(row.get("why_records_attempted", 0)) > 0]
    summary = {
        "run_id": run_output_dir.parent.name,
        "split_cluster_count": len(cluster_rows),
        "record_count": len(record_rows),
        "non_match_pair_count": len(pair_rows),
        "why_pairs_attempted": len(explained_pair_rows),
        "why_pairs_ok": sum(int(row.get("why_records_ok", 0)) for row in explained_pair_rows),
        "why_coverage_pct": round((len(explained_pair_rows) / len(pair_rows) * 100.0), 2) if pair_rows else 0.0,
    }

    write_csv(
        output_dir / "cluster_summary.csv",
        ["cluster_id", "expected_record_count", "senzing_entity_count", "non_match_pair_count", "resolved_entity_ids", "audit_categories", "audit_results", "record_ids"],
        cluster_rows,
    )
    write_csv(
        output_dir / "record_membership.csv",
        [
            "cluster_id",
            "record_id",
            "resolved_entity_id",
            "match_level",
            "match_key",
            "audit_categories",
            "audit_results",
            "audit_ids",
            "source_ipg_id",
            "record_type",
            "name_full",
            "name_first",
            "name_last",
            "date_of_birth",
            "nationality",
            "addr_line1",
            "addr_city",
            "addr_postal_code",
            "addr_country",
            "tax_id_number",
            "lei_number",
            "website_address",
            "email_address",
            "other_ids",
        ],
        record_rows,
    )
    write_csv(
        output_dir / "non_match_pairs.csv",
        [
            "cluster_id",
            "left_record_id",
            "right_record_id",
            "left_resolved_entity_id",
            "right_resolved_entity_id",
            "left_match_level",
            "right_match_level",
            "left_match_key",
            "right_match_key",
            "left_name_full",
            "right_name_full",
            "left_tax_id_number",
            "right_tax_id_number",
            "left_source_ipg_id",
            "right_source_ipg_id",
            "why_records_attempted",
            "why_records_ok",
            "why_records_method",
            "why_records_reason_summary",
            "why_records_error",
        ],
        pair_rows,
    )
    write_csv(
        output_dir / "explained_non_match_pairs.csv",
        [
            "cluster_id",
            "left_record_id",
            "right_record_id",
            "left_resolved_entity_id",
            "right_resolved_entity_id",
            "left_match_key",
            "right_match_key",
            "why_records_ok",
            "why_records_method",
            "why_records_reason_summary",
            "why_records_error",
        ],
        explained_pair_rows,
    )

    why_results_path = output_dir / "why_results.jsonl"
    with why_results_path.open("w", encoding="utf-8") as outfile:
        for item in why_results:
            outfile.write(json.dumps(item, ensure_ascii=False) + "\n")

    audit_json = read_json(truthset_audit_json)
    summary_json_path = output_dir / "summary.json"
    summary_json_path.write_text(
        json.dumps(
            {
                "summary": summary,
                "why_engine_status": why_engine_status,
                "audit_summary": audit_json,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    write_summary_md(output_dir / "summary.md", summary, audit_json, why_engine_status)
    write_summary_md(output_dir / "README.md", summary, audit_json, why_engine_status)
    build_html(output_dir, cluster_rows, record_rows, explained_pair_rows, summary)

    print(f"Run output dir: {run_output_dir}")
    print(f"Project dir: {project_dir}")
    print(f"Output dir: {output_dir}")
    print(f"Split clusters: {summary['split_cluster_count']}")
    print(f"Non-match pairs: {summary['non_match_pair_count']}")
    print(f"whyRecords attempted: {summary['why_pairs_attempted']}")
    print(f"whyRecords ok: {summary['why_pairs_ok']}")
    print(f"why engine status: {why_engine_status}")
    print(f"HTML report: {output_dir / 'index.html'}")
    print(f"Summary Markdown: {output_dir / 'summary.md'}")
    print(f"Pair CSV: {output_dir / 'non_match_pairs.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

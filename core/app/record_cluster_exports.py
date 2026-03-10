#!/usr/bin/env python3
"""Shared helpers for record/cluster export artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from partner_json_to_senzing import infer_field_map, iter_input_records, resolve_value


@dataclass(frozen=True)
class RecordClusterRow:
    record_id: str
    cluster_id: str | None
    data_source: str


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def to_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def infer_mapper_field_map(
    input_path: Path,
    array_key: str | None,
    fuzzy_cutoff: float,
    scan_records: int,
) -> tuple[dict[str, str], str | None]:
    sample_records: list[dict] = []
    for record in iter_input_records(input_path, array_key):
        sample_records.append(record)
        if len(sample_records) >= scan_records:
            break
    if not sample_records:
        raise ValueError("Input contains no records.")
    field_map = infer_field_map(sample_records, fuzzy_cutoff)
    return field_map, field_map.get("ipg_id")


def detect_input_mode(input_path: Path, array_key: str | None) -> tuple[str, dict[str, str]]:
    sample_iter = iter_input_records(input_path, array_key)
    try:
        first_record = next(sample_iter)
    except StopIteration as err:
        raise ValueError("Input contains no records.") from err

    sample_records = [first_record]
    for _, record in zip(range(24), sample_iter):
        sample_records.append(record)

    normalized_lookup: dict[str, str] = {}
    for record in sample_records:
        for key in record.keys():
            normalized_lookup.setdefault(normalize_key(key), key)
    if "recordid" in normalized_lookup and ("sourceipgid" in normalized_lookup or "ipgid" in normalized_lookup):
        resolved = {
            "record_id": normalized_lookup["recordid"],
            "cluster_id": normalized_lookup.get("sourceipgid") or normalized_lookup.get("ipgid"),
            "data_source": normalized_lookup.get("datasource", ""),
        }
        return "mapped", resolved
    return "source", {}


def iter_record_cluster_rows(
    input_path: Path,
    array_key: str | None,
    fuzzy_cutoff: float,
    scan_records: int,
    data_source: str,
) -> tuple[Iterator[RecordClusterRow], str | None]:
    input_mode, mapped_fields = detect_input_mode(input_path, array_key)
    if input_mode == "mapped":
        cluster_source_key = mapped_fields["cluster_id"]
        record_id_key = mapped_fields["record_id"]
        data_source_key = mapped_fields.get("data_source")

        def mapped_row_iterator() -> Iterator[RecordClusterRow]:
            for record in iter_input_records(input_path, array_key):
                current_data_source = to_text(record.get(data_source_key)) if data_source_key else None
                yield RecordClusterRow(
                    record_id=to_text(record.get(record_id_key)) or "",
                    cluster_id=to_text(record.get(cluster_source_key)),
                    data_source=current_data_source or data_source,
                )

        return mapped_row_iterator(), cluster_source_key

    field_map, ipg_source_key = infer_mapper_field_map(
        input_path=input_path,
        array_key=array_key,
        fuzzy_cutoff=fuzzy_cutoff,
        scan_records=scan_records,
    )

    def row_iterator() -> Iterator[RecordClusterRow]:
        for index, record in enumerate(iter_input_records(input_path, array_key), start=1):
            cluster_id, _ = resolve_value(record, field_map, "ipg_id", fuzzy_cutoff)
            yield RecordClusterRow(
                record_id=str(index),
                cluster_id=cluster_id,
                data_source=data_source,
            )

    return row_iterator(), ipg_source_key

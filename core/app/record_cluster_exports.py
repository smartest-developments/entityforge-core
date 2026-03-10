#!/usr/bin/env python3
"""Shared helpers for record/cluster export artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from partner_json_to_senzing import infer_field_map, iter_input_records, resolve_value


@dataclass(frozen=True)
class RecordClusterRow:
    record_id: str
    cluster_id: str | None
    data_source: str


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


def iter_record_cluster_rows(
    input_path: Path,
    array_key: str | None,
    fuzzy_cutoff: float,
    scan_records: int,
    data_source: str,
) -> tuple[Iterator[RecordClusterRow], str | None]:
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

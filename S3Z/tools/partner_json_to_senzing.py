#!/usr/bin/env python3
"""Convert partner JSON arrays into Senzing-ready JSONL records.

Input format:
- A JSON file containing an array of objects.
- Each object represents one source record.

Output format:
- JSONL file (one Senzing record per line), with:
  - DATA_SOURCE
  - RECORD_ID
  - FEATURES (Senzing feature objects)
  - Optional payload attributes (root-level scalars)

This mapper is designed for source schemas that contain fields similar to:
- record ID
- external partner/business-relation keys
- partner class code (I/C/S)
- partner/person/org name fields
- birth or foundation date
- domicile/nationality country
- street/residence/postal/city address fields
- tax and other identifiers (LEI, LEM ID, CRN, document ID, IPG ID)
- electronic address (email/website)

The script infers actual source keys by using normalized aliases and a fuzzy
fallback, so it can handle naming variations (spaces, underscores, camelCase).
"""

from __future__ import annotations

import argparse
import difflib
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


CANONICAL_FIELDS: dict[str, list[str]] = {
    "external_partner_key_dir_external_id": [
        "externalpartnerkeydirexternalid",
        "external partner key dir external id",
        "external_partner_key_dir_external_id",
        "external_partner_id",
        "partner_id",
        "partner id",
        "partnerid",
    ],
    "partner_key_dir_bus_rel_external_id": [
        "partnerkeydirbusrelexternalid",
        "partner key dir bus rel external id",
        "partner_key_dir_bus_rel_external_id",
        "business_relation_id",
        "business relation id",
        "businessrelationid",
        "busrelid",
        "bus_rel_id",
        "bus rel id",
        "busrelationid",
        "boost_rlid",
        "boost rlid",
        "boostrlid",
        "rlid",
    ],
    "partner_class_code": [
        "partner_class_code",
        "partner class code",
        "partnerclasscode",
        "partner_class",
        "class_code",
        "class code",
    ],
    "partner_name": [
        "partner_name",
        "partner name",
        "partnername",
        "name",
        "legal_name",
    ],
    "legal_first_name": [
        "legal_first_name",
        "legal first name",
        "legalfirstname",
        "first_name",
        "firstname",
    ],
    "additional_name": [
        "additional_name",
        "additional name",
        "additionalname",
        "middle_name",
        "middlename",
        "last_name",
        "lastname",
        "surname",
    ],
    "birth_or_foundation_date": [
        "birth_or_foundation_date",
        "birth or foundation date",
        "birth of foundation date",
        "birthoffoundationdate",
        "date_of_birth",
        "birth_date",
        "foundation_date",
        "registration_date",
    ],
    "domicile_country_code": [
        "domicile_country_code",
        "domicile country code",
        "domicilecountrycode",
        "country_code",
        "country",
    ],
    "prime_nationality_country_code": [
        "prime_nationality_country_code",
        "prime nationality country code",
        "primenationalitycountrycode",
        "nationality_country_code",
        "nationality",
    ],
    "address_postal_code": [
        "address_postal_code",
        "address postal code",
        "addresspostalcode",
        "postal_code",
        "postcode",
        "zip_code",
    ],
    "address_postal_city_name": [
        "address_postal_city_name",
        "address postal city name",
        "addresspostalcityname",
        "postal_city",
        "city",
        "city_name",
    ],
    "address_street_name": [
        "address_street_name",
        "address street name",
        "addressstreetname",
        "street_name",
        "street",
    ],
    "address_residence_identifier": [
        "address_residence_identifier",
        "address residence identifier",
        "addressresidenceidentifier",
        "street_number",
        "house_number",
        "residence_identifier",
    ],
    "lei": [
        "lei",
    ],
    "lem_id": [
        "lem_id",
        "lem id",
        "lemid",
    ],
    "crn": [
        "crn",
        "company_registration_number",
        "company registration number",
    ],
    "tax_id": [
        "tax_id",
        "tax id",
        "taxid",
        "tin",
        "vat",
        "fiscal_code",
    ],
    "id_document_number": [
        "iddocumentnumber",
        "id_document_number",
        "id document number",
        "document_number",
        "document id",
    ],
    "electronic_address": [
        "electronicaddress",
        "electronic_address",
        "electronic address",
        "email",
        "email_address",
        "mail",
        "website",
        "url",
    ],
    "ipg_id": [
        "ipg_id",
        "ipg id",
        "ipgid",
    ],
}


CLASS_CODE_TO_RECORD_TYPE = {
    "I": "PERSON",
    "C": "ORGANIZATION",
    "S": "ORGANIZATION",
}


def normalize_key(text: str) -> str:
    """Normalize key names for robust matching."""
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def to_text(value: Any) -> str | None:
    """Convert values to stripped text; return None for empty/null values."""
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def safe_payload_key(raw_key: str) -> str:
    """Generate a safe root payload key that cannot collide with Senzing feature keys."""
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", raw_key).strip("_").upper()
    if not normalized:
        normalized = "UNNAMED_FIELD"
    if normalized[0].isdigit():
        normalized = f"F_{normalized}"
    return f"SRC_{normalized}"


def infer_field_map(records: list[dict[str, Any]], fuzzy_cutoff: float) -> dict[str, str]:
    """Infer canonical->source key mapping using aliases and fuzzy fallback."""
    source_keys: list[str] = []
    seen: set[str] = set()

    for record in records:
        for key in record.keys():
            if key not in seen:
                seen.add(key)
                source_keys.append(key)

    normalized_to_source: dict[str, str] = {}
    for key in source_keys:
        normalized = normalize_key(key)
        normalized_to_source.setdefault(normalized, key)

    inferred: dict[str, str] = {}
    used_source_keys: set[str] = set()

    for canonical, aliases in CANONICAL_FIELDS.items():
        normalized_aliases = [normalize_key(alias) for alias in aliases]

        # 1) Exact normalized alias match.
        exact_matches: list[tuple[str, str]] = []
        for alias in normalized_aliases:
            if alias in normalized_to_source:
                source_key = normalized_to_source[alias]
                exact_matches.append((alias, source_key))
        for _, source_key in exact_matches:
            if source_key not in used_source_keys:
                inferred[canonical] = source_key
                used_source_keys.add(source_key)
                break
        if canonical in inferred:
            continue

        # 2) Fuzzy fallback.
        best_key: str | None = None
        best_score = 0.0
        normalized_source_items = [(normalize_key(k), k) for k in source_keys if k not in used_source_keys]
        for source_norm, source_key in normalized_source_items:
            source_score = 0.0
            for alias in normalized_aliases:
                score = difflib.SequenceMatcher(a=alias, b=source_norm).ratio()
                if score > source_score:
                    source_score = score
            if source_score > best_score:
                best_score = source_score
                best_key = source_key
        if best_key and best_score >= fuzzy_cutoff:
            inferred[canonical] = best_key
            used_source_keys.add(best_key)

    return inferred


def resolve_value(
    record: dict[str, Any],
    field_map: dict[str, str],
    canonical_field: str,
    fuzzy_cutoff: float,
) -> tuple[str | None, str | None]:
    """Resolve canonical field value from one record with alias and fuzzy fallback.

    Returns:
    - value (as text or None)
    - source key used (or None if not resolved)
    """
    # 1) Prefer dataset-level inferred mapping when present.
    preferred_source_key = field_map.get(canonical_field)
    if preferred_source_key in record:
        return to_text(record.get(preferred_source_key)), preferred_source_key

    # 2) Exact alias match within this record.
    normalized_to_source: dict[str, str] = {}
    for source_key in record.keys():
        normalized_to_source.setdefault(normalize_key(source_key), source_key)

    normalized_aliases = [normalize_key(alias) for alias in CANONICAL_FIELDS[canonical_field]]
    for alias in normalized_aliases:
        if alias in normalized_to_source:
            source_key = normalized_to_source[alias]
            return to_text(record.get(source_key)), source_key

    # 3) Fuzzy fallback within this record.
    best_key: str | None = None
    best_score = 0.0
    for source_key in record.keys():
        source_norm = normalize_key(source_key)
        source_score = 0.0
        for alias in normalized_aliases:
            score = difflib.SequenceMatcher(a=alias, b=source_norm).ratio()
            if score > source_score:
                source_score = score
        if source_score > best_score:
            best_score = source_score
            best_key = source_key
    if best_key and best_score >= fuzzy_cutoff:
        return to_text(record.get(best_key)), best_key

    return None, None


def build_name(record_type: str | None, partner_name: str | None, legal_first_name: str | None, additional_name: str | None) -> dict[str, str] | None:
    """Build NAME feature according to record type and available source values."""
    fallback_full_name = " ".join(part for part in [legal_first_name, additional_name] if part).strip() or None

    if record_type == "ORGANIZATION":
        org_name = partner_name or fallback_full_name
        return {"NAME_ORG": org_name} if org_name else None

    person_name = partner_name or fallback_full_name
    return {"NAME_FULL": person_name} if person_name else None


def looks_like_email(value: str) -> bool:
    """Return True when text resembles an email address."""
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value))


def looks_like_website(value: str) -> bool:
    """Return True when text resembles a URL or domain."""
    if re.fullmatch(r"https?://\S+", value):
        return True
    return bool(re.fullmatch(r"[A-Za-z0-9-]+\.[A-Za-z]{2,}(\S*)?", value))


def append_other_id_feature(
    features: list[dict[str, str]],
    identifier_value: str | None,
    id_type: str,
    country_code: str | None,
) -> None:
    """Append OTHER_ID feature when identifier_value is present."""
    if not identifier_value:
        return
    feature: dict[str, str] = {"OTHER_ID_TYPE": id_type, "OTHER_ID_NUMBER": identifier_value}
    if country_code:
        feature["OTHER_ID_COUNTRY"] = country_code
    features.append(feature)


def convert_record(
    record: dict[str, Any],
    field_map: dict[str, str],
    args: argparse.Namespace,
    record_index: int,
) -> tuple[dict[str, Any] | None, str | None]:
    """Convert one source record to one Senzing record."""
    resolved_source_keys: set[str] = set()

    def read(canonical_field: str) -> str | None:
        value, source_key = resolve_value(record, field_map, canonical_field, args.fuzzy_cutoff)
        if source_key:
            resolved_source_keys.add(source_key)
        return value

    external_partner_key_dir_external_id = read("external_partner_key_dir_external_id")
    partner_key_dir_bus_rel_external_id = read("partner_key_dir_bus_rel_external_id")

    # RECORD_ID is a simple monotonically increasing sequence per input file.
    record_id = str(record_index)

    partner_class_code = read("partner_class_code")
    partner_name = read("partner_name")
    legal_first_name = read("legal_first_name")
    additional_name = read("additional_name")
    birth_or_foundation_date = read("birth_or_foundation_date")
    domicile_country_code = read("domicile_country_code")
    prime_nationality_country_code = read("prime_nationality_country_code")
    address_street_name = read("address_street_name")
    address_residence_identifier = read("address_residence_identifier")
    address_postal_code = read("address_postal_code")
    address_postal_city_name = read("address_postal_city_name")
    lei = read("lei")
    lem_id = read("lem_id")
    crn = read("crn")
    tax_id = read("tax_id")
    id_document_number = read("id_document_number")
    electronic_address = read("electronic_address")
    ipg_id = read("ipg_id")

    normalized_class_code = (partner_class_code or "").upper()
    record_type = CLASS_CODE_TO_RECORD_TYPE.get(normalized_class_code)

    features: list[dict[str, str]] = []

    if record_type:
        features.append({"RECORD_TYPE": record_type})

    name_feature = build_name(record_type, partner_name, legal_first_name, additional_name)
    if name_feature:
        features.append(name_feature)
    if record_type != "ORGANIZATION" and any([legal_first_name, additional_name]):
        parsed_name_feature: dict[str, str] = {}
        if legal_first_name:
            parsed_name_feature["NAME_FIRST"] = legal_first_name
        if additional_name:
            parsed_name_feature["NAME_LAST"] = additional_name
        if parsed_name_feature:
            features.append(parsed_name_feature)

    if birth_or_foundation_date:
        if record_type == "ORGANIZATION":
            features.append({"REGISTRATION_DATE": birth_or_foundation_date})
        else:
            features.append({"DATE_OF_BIRTH": birth_or_foundation_date})

    if prime_nationality_country_code:
        features.append({"NATIONALITY": prime_nationality_country_code})

    if any([address_street_name, address_residence_identifier, address_postal_code, address_postal_city_name, domicile_country_code]):
        address_feature: dict[str, str] = {"ADDR_TYPE": "BUSINESS" if record_type == "ORGANIZATION" else "HOME"}
        line1_parts = [part for part in [address_street_name, address_residence_identifier] if part]
        if line1_parts:
            address_feature["ADDR_LINE1"] = " ".join(line1_parts)
        if address_postal_city_name:
            address_feature["ADDR_CITY"] = address_postal_city_name
        if address_postal_code:
            address_feature["ADDR_POSTAL_CODE"] = address_postal_code
        if domicile_country_code:
            address_feature["ADDR_COUNTRY"] = domicile_country_code
        features.append(address_feature)

    if tax_id:
        tax_feature: dict[str, str] = {
            "TAX_ID_TYPE": args.tax_id_type,
            "TAX_ID_NUMBER": tax_id,
        }
        if domicile_country_code:
            tax_feature["TAX_ID_COUNTRY"] = domicile_country_code
        features.append(tax_feature)

    if lei:
        features.append({"LEI_NUMBER": lei})

    append_other_id_feature(features, lem_id, "LEM_ID", domicile_country_code)
    append_other_id_feature(features, crn, "CRN", domicile_country_code)
    append_other_id_feature(features, id_document_number, "ID_DOCUMENT_NUMBER", domicile_country_code)

    # Internal source IDs are matching features, not payload.
    append_other_id_feature(
        features,
        external_partner_key_dir_external_id,
        args.partner_id_feature_type,
        domicile_country_code,
    )
    append_other_id_feature(
        features,
        partner_key_dir_bus_rel_external_id,
        args.business_relation_feature_type,
        domicile_country_code,
    )
    if electronic_address:
        if looks_like_email(electronic_address):
            features.append({"EMAIL_ADDRESS": electronic_address})
        elif looks_like_website(electronic_address):
            features.append({"WEBSITE_ADDRESS": electronic_address})
        else:
            append_other_id_feature(features, electronic_address, "ELECTRONIC_ADDRESS", domicile_country_code)

    output_record: dict[str, Any] = {
        "DATA_SOURCE": args.data_source,
        "RECORD_ID": record_id,
        "FEATURES": features,
    }

    # Keep only source-system operational ID IPG in payload.
    payload_fields = {
        "SOURCE_IPG_ID": ipg_id,
    }

    for payload_key, payload_value in payload_fields.items():
        if payload_value is not None:
            output_record[payload_key] = payload_value

    if args.include_unmapped_source_fields:
        for source_key, source_value in record.items():
            if source_key in resolved_source_keys:
                continue
            if source_value is None:
                continue
            output_record[safe_payload_key(source_key)] = (
                source_value if isinstance(source_value, (str, int, float, bool)) else json.dumps(source_value, ensure_ascii=False)
            )

    return output_record, None


def parse_input_records(input_path: Path, array_key: str | None) -> list[dict[str, Any]]:
    """Load and validate input records."""
    with input_path.open("r", encoding="utf-8") as infile:
        raw_data = json.load(infile)

    if isinstance(raw_data, list):
        records = raw_data
    elif isinstance(raw_data, dict) and array_key and isinstance(raw_data.get(array_key), list):
        records = raw_data[array_key]
    else:
        raise ValueError(
            "Input must be a JSON array, or a JSON object containing an array at --array-key."
        )

    validated: list[dict[str, Any]] = []
    for index, item in enumerate(records, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Record {index} is not a JSON object.")
        validated.append(item)

    return validated


def build_arg_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Map partner JSON records into Senzing-ready JSONL."
    )
    parser.add_argument("input_json", help="Input JSON file path")
    parser.add_argument(
        "output_jsonl",
        nargs="?",
        default=None,
        help=(
            "Optional output JSONL file path. If omitted, a timestamped run "
            "directory is created automatically under --run-output-root."
        ),
    )
    parser.add_argument(
        "--data-source",
        default="PARTNERS",
        help="Senzing DATA_SOURCE value (default: PARTNERS)",
    )
    parser.add_argument(
        "--array-key",
        default=None,
        help="Optional key if input root is an object containing an array",
    )
    parser.add_argument(
        "--internal-id-feature-mode",
        choices=["other_id", "account", "none"],
        default="other_id",
        help=(
            "Legacy option kept for backward compatibility (no effect in current mapping)"
        ),
    )
    parser.add_argument(
        "--partner-id-feature-type",
        default="PARTNER_ID",
        help="OTHER_ID_TYPE used for external partner key (default: PARTNER_ID)",
    )
    parser.add_argument(
        "--business-relation-feature-type",
        default="BUSINESS_RELATION_ID",
        help="OTHER_ID_TYPE used for business relation key (default: BUSINESS_RELATION_ID)",
    )
    parser.add_argument(
        "--tax-id-type",
        default="TIN",
        help="TAX_ID_TYPE value to emit when tax_id is present (default: TIN)",
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
        "--strict",
        action="store_true",
        help="Fail on the first conversion issue instead of skipping bad records",
    )
    parser.add_argument(
        "--include-unmapped-source-fields",
        action="store_true",
        help="Copy unknown source fields to payload (prefixed as SRC_*)",
    )
    parser.add_argument(
        "--write-field-map",
        default=None,
        help="Optional path to write inferred canonical->source field map as JSON",
    )
    parser.add_argument(
        "--run-output-root",
        default="mapper_runs",
        help=(
            "Root directory for auto-generated timestamped run folders "
            "(used only when output_jsonl is omitted). Default: mapper_runs"
        ),
    )
    parser.add_argument(
        "--run-name-prefix",
        default="partner_mapping",
        help=(
            "Prefix used for timestamped run folders (used only when "
            "output_jsonl is omitted). Default: partner_mapping"
        ),
    )
    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_arg_parser()
    args = parser.parse_args()

    input_path = Path(args.input_json)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    if not 0.0 <= args.fuzzy_cutoff <= 1.0:
        print("ERROR: --fuzzy-cutoff must be between 0 and 1", file=sys.stderr)
        return 2

    try:
        records = parse_input_records(input_path, args.array_key)
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"ERROR: Unable to parse input JSON: {err}", file=sys.stderr)
        return 2

    if not records:
        print("ERROR: Input JSON contains no records.", file=sys.stderr)
        return 2

    sample_records = records[: args.scan_records]
    field_map = infer_field_map(sample_records, args.fuzzy_cutoff)

    print("Inferred field map:")
    for canonical in sorted(CANONICAL_FIELDS.keys()):
        source_key = field_map.get(canonical, "<NOT_FOUND>")
        print(f"  - {canonical}: {source_key}")

    unresolved = [field for field in CANONICAL_FIELDS if field not in field_map]
    if unresolved:
        print("\nUnresolved canonical fields (no confident source match):")
        for field in unresolved:
            print(f"  - {field}")

    # Output strategy:
    # - If output_jsonl is provided: use it directly (backward compatible mode).
    # - If output_jsonl is omitted: create a timestamped run directory automatically.
    run_directory: Path | None = None
    if args.output_jsonl:
        output_path = Path(args.output_jsonl)
    else:
        timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_root = Path(args.run_output_root)
        run_directory = run_root / f"{args.run_name_prefix}_{timestamp}"
        run_directory.mkdir(parents=True, exist_ok=True)
        output_path = run_directory / "output.jsonl"
        if not args.write_field_map:
            args.write_field_map = str(run_directory / "field_map.json")

    converted = 0
    skipped = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as outfile:
        for index, record in enumerate(records, start=1):
            output_record, error = convert_record(record, field_map, args, index)
            if error:
                message = f"Record {index}: {error}"
                if args.strict:
                    print(f"ERROR: {message}", file=sys.stderr)
                    return 1
                print(f"WARN: {message}", file=sys.stderr)
                skipped += 1
                continue
            outfile.write(json.dumps(output_record, ensure_ascii=False) + "\n")
            converted += 1

    if args.write_field_map:
        mapping_output = {
            "canonical_to_source": field_map,
            "unresolved_canonical_fields": unresolved,
        }
        map_path = Path(args.write_field_map)
        map_path.parent.mkdir(parents=True, exist_ok=True)
        with map_path.open("w", encoding="utf-8") as map_out:
            json.dump(mapping_output, map_out, indent=2, ensure_ascii=False)

    if run_directory:
        run_info = {
            "run_directory": str(run_directory),
            "input_file": str(input_path),
            "output_jsonl": str(output_path),
            "field_map_file": args.write_field_map,
            "data_source": args.data_source,
            "records_input": len(records),
            "records_converted": converted,
            "records_skipped": skipped,
            "unresolved_canonical_fields": unresolved,
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        }
        run_info_path = run_directory / "run_info.json"
        run_info_path.write_text(json.dumps(run_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\nConversion complete.")
    print(f"  - Input records: {len(records)}")
    print(f"  - Converted: {converted}")
    print(f"  - Skipped: {skipped}")
    print(f"  - Output JSONL: {output_path}")
    if args.write_field_map:
        print(f"  - Field map: {args.write_field_map}")
    if run_directory:
        print(f"  - Run directory: {run_directory}")

    return 0 if converted > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

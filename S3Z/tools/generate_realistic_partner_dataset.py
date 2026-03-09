#!/usr/bin/env python3
"""Generate a realistic partner input sample and map it to Senzing JSONL.

This script creates:
1) A base input JSON array in `sample/` (internal/source-style schema).
2) A mapped Senzing JSONL file in `output/` using partner_json_to_senzing.py.

The generated base records always include:
- externalPartnerKeyDirExternalID
- partnerKeyDirBusRelExternalID

`IPG ID` is populated for a configurable share of records (default: 35%).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import string
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


COUNTRY_PROFILES: list[dict[str, Any]] = [
    {"code": "US", "cities": ["New York", "Chicago", "Austin", "Seattle"], "tld": "com"},
    {"code": "GB", "cities": ["London", "Manchester", "Leeds", "Bristol"], "tld": "co.uk"},
    {"code": "DE", "cities": ["Berlin", "Munich", "Hamburg", "Cologne"], "tld": "de"},
    {"code": "FR", "cities": ["Paris", "Lyon", "Toulouse", "Lille"], "tld": "fr"},
    {"code": "IT", "cities": ["Milan", "Rome", "Turin", "Bologna"], "tld": "it"},
    {"code": "ES", "cities": ["Madrid", "Barcelona", "Valencia", "Seville"], "tld": "es"},
    {"code": "NL", "cities": ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven"], "tld": "nl"},
    {"code": "CH", "cities": ["Zurich", "Geneva", "Basel", "Lugano"], "tld": "ch"},
    {"code": "AE", "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"], "tld": "ae"},
    {"code": "SG", "cities": ["Singapore"], "tld": "sg"},
    {"code": "AU", "cities": ["Sydney", "Melbourne", "Perth", "Brisbane"], "tld": "au"},
    {"code": "CA", "cities": ["Toronto", "Montreal", "Vancouver", "Calgary"], "tld": "ca"},
]

FIRST_NAMES = [
    "Luca", "Giulia", "Marco", "Sara", "Davide", "Elena", "Noah", "Emma", "Mia", "Liam",
    "Sofia", "Carlos", "Ana", "Miguel", "Julia", "Leon", "Marta", "Aisha", "Omar", "Nina",
    "Yuki", "Hiro", "Ari", "Leila", "Jonas", "Maya", "Ethan", "Olivia", "Samuel", "Camila",
]

LAST_NAMES = [
    "Rossi", "Bianchi", "Conti", "Ferri", "Vitale", "Neri", "Ricci", "Gallo", "Costa", "Moretti",
    "Smith", "Johnson", "Williams", "Brown", "Miller", "Taylor", "Anderson", "Thomas", "Lopez", "Martinez",
    "Schmidt", "Keller", "Dubois", "Lefevre", "Novak", "Kovacs", "Hassan", "Rahman", "Tanaka", "Sato",
]

ORG_PREFIX = [
    "Aurora", "Vertex", "Harbor", "Crescent", "Atlas", "Nimbus", "Summit", "Pioneer", "Lighthouse", "Northbridge",
    "Bluewave", "Artemis", "Global", "Prime", "Cobalt", "Sterling", "Orbit", "Terra", "Evergreen", "Helios",
]

ORG_CORE = [
    "Logistics", "Advisory", "Capital", "Technology", "Foods", "Healthcare", "Partners", "Manufacturing", "Holdings", "Analytics",
    "Trading", "Solutions", "Engineering", "Networks", "Retail", "Energy", "Pharma", "Media", "Maritime", "Consulting",
]

ORG_SUFFIX = ["Ltd", "LLC", "Inc", "Group", "GmbH", "SA", "BV", "AG", "Pte", "PLC"]

STREET_PARTS = [
    "Market", "King", "Maple", "River", "Hill", "Oak", "Harbor", "Garden", "Station", "Lake",
    "Cedar", "Sunset", "Bridge", "Central", "Forest", "Victoria", "Highland", "Park", "Elm", "Main",
]


def now_timestamp() -> str:
    """Timestamp for filenames."""
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def ascii_slug(text: str) -> str:
    """Build a lowercase ascii slug."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    return slug or "entity"


def maybe(rng: random.Random, probability: float) -> bool:
    """Probability helper."""
    return rng.random() < probability


def random_date(rng: random.Random, start_year: int, end_year: int) -> str:
    """Generate YYYY-MM-DD."""
    year = rng.randint(start_year, end_year)
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def random_postal_code(rng: random.Random, country_code: str) -> str:
    """Generate a simple country-aware postal code."""
    if country_code in {"US", "DE", "FR", "IT", "ES", "NL", "CH", "AU"}:
        return f"{rng.randint(10000, 99999)}"
    if country_code == "GB":
        return f"{rng.choice(string.ascii_uppercase)}{rng.randint(1,9)} {rng.randint(1,9)}{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}"
    if country_code == "CA":
        return f"{rng.choice(string.ascii_uppercase)}{rng.randint(0,9)}{rng.choice(string.ascii_uppercase)} {rng.randint(0,9)}{rng.choice(string.ascii_uppercase)}{rng.randint(0,9)}"
    if country_code in {"AE", "SG"}:
        return f"{rng.randint(100000, 999999)}"
    return f"{rng.randint(10000, 99999)}"


def random_tax_id(rng: random.Random, country_code: str, is_org: bool) -> str:
    """Create plausible alphanumeric tax id."""
    if is_org:
        return f"{country_code}{rng.randint(100000000, 999999999)}"
    return f"{country_code}{rng.randint(10, 99)}{rng.choice(string.ascii_uppercase)}{rng.randint(100000, 999999)}{rng.choice(string.ascii_uppercase)}"


def random_other_id(rng: random.Random, prefix: str, country_code: str) -> str:
    """Generic identifier generator."""
    return f"{prefix}-{country_code}-{rng.randint(100000, 999999)}"


def person_name_variant(rng: random.Random, first_name: str, last_name: str) -> str:
    """Return a realistic name variation."""
    variants = [
        f"{first_name} {last_name}",
        f"{last_name}, {first_name}",
        f"{first_name[0]}. {last_name}",
        f"{first_name} {last_name}".upper(),
        f"{first_name} {last_name[0]}.",
    ]
    return rng.choice(variants)


def org_name_variant(rng: random.Random, org_name: str) -> str:
    """Return a realistic organization name variation."""
    compact = re.sub(r"\s+", " ", org_name).strip()
    stripped = re.sub(r"[.,]", "", compact)
    parts = stripped.split()
    if len(parts) >= 2 and maybe(rng, 0.35):
        parts[-1] = parts[-1].replace("Group", "Grp").replace("Technology", "Tech").replace("Solutions", "Sol")
    short = " ".join(parts)
    variants = [compact, stripped, short, short.upper()]
    return rng.choice(variants)


def choose_record_type(rng: random.Random, person_ratio: float) -> str:
    """PERSON or ORGANIZATION."""
    return "PERSON" if rng.random() < person_ratio else "ORGANIZATION"


def build_profile(record_type: str, rng: random.Random) -> dict[str, Any]:
    """Build a canonical entity profile."""
    country = rng.choice(COUNTRY_PROFILES)
    country_code = country["code"]
    city = rng.choice(country["cities"])
    street = f"{rng.choice(STREET_PARTS)} {rng.choice(['Street', 'Avenue', 'Road', 'Lane', 'Boulevard'])}"
    house_number = str(rng.randint(1, 250))
    postal_code = random_postal_code(rng, country_code)
    tld = country["tld"]

    if record_type == "PERSON":
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        partner_name = f"{first_name} {last_name}"
        email = f"{ascii_slug(first_name)}.{ascii_slug(last_name)}@mail.{tld}"
        return {
            "record_type": record_type,
            "country_code": country_code,
            "partner_name": partner_name,
            "legal_first_name": first_name,
            "additional_name": last_name,
            "birth_or_foundation_date": random_date(rng, 1955, 2004),
            "prime_nationality_country_code": country_code,
            "address_street_name": street,
            "address_residence_identifier": house_number,
            "address_postal_code": postal_code,
            "address_postal_city_name": city,
            "lei": None,
            "lem_id": random_other_id(rng, "LEM", country_code) if maybe(rng, 0.30) else None,
            "crn": random_other_id(rng, "CRN", country_code) if maybe(rng, 0.06) else None,
            "tax_id": random_tax_id(rng, country_code, is_org=False),
            "id_document_number": random_other_id(rng, "DOC", country_code),
            "electronic_address": email,
        }

    org_name = f"{rng.choice(ORG_PREFIX)} {rng.choice(ORG_CORE)} {rng.choice(ORG_SUFFIX)}"
    website = f"https://www.{ascii_slug(org_name)}.{tld}"
    return {
        "record_type": record_type,
        "country_code": country_code,
        "partner_name": org_name,
        "legal_first_name": None,
        "additional_name": None,
        "birth_or_foundation_date": random_date(rng, 1970, 2024),
        "prime_nationality_country_code": country_code,
        "address_street_name": street,
        "address_residence_identifier": house_number,
        "address_postal_code": postal_code,
        "address_postal_city_name": city,
        "lei": random_other_id(rng, "LEI", country_code) if maybe(rng, 0.60) else None,
        "lem_id": random_other_id(rng, "LEM", country_code) if maybe(rng, 0.50) else None,
        "crn": random_other_id(rng, "CRN", country_code) if maybe(rng, 0.80) else None,
        "tax_id": random_tax_id(rng, country_code, is_org=True),
        "id_document_number": None,
        "electronic_address": website if maybe(rng, 0.75) else f"contact@{ascii_slug(org_name)}.{tld}",
    }


def apply_sparsity(record: dict[str, Any], record_type: str, rng: random.Random, clustered: bool) -> None:
    """Drop optional fields to simulate real sparse input."""
    if record_type == "PERSON":
        drop_prob = {
            "legal_first_name": 0.22,
            "additional_name": 0.28,
            "birth_or_foundation_date": 0.16,
            "prime_nationality_country_code": 0.33,
            "address_street_name": 0.45,
            "address_residence_identifier": 0.52,
            "address_postal_code": 0.40,
            "address_postal_city_name": 0.38,
            "lem_id": 0.72,
            "crn": 0.94,
            "tax_id": 0.42,
            "id_document_number": 0.56,
            "electronic_address": 0.55,
        }
    else:
        drop_prob = {
            "legal_first_name": 0.98,
            "additional_name": 0.98,
            "birth_or_foundation_date": 0.24,
            "prime_nationality_country_code": 0.45,
            "address_street_name": 0.30,
            "address_residence_identifier": 0.40,
            "address_postal_code": 0.24,
            "address_postal_city_name": 0.22,
            "lei": 0.62,
            "lem_id": 0.56,
            "crn": 0.38,
            "tax_id": 0.30,
            "id_document_number": 0.98,
            "electronic_address": 0.40,
        }

    for key, probability in drop_prob.items():
        if maybe(rng, probability):
            record[key] = None

    if maybe(rng, 0.08):
        record["address_residence_identifier"] = None
    if maybe(rng, 0.05):
        record["address_street_name"] = None

    # For clustered records we keep at least one strong matching signal.
    if clustered:
        strong_fields = ["tax_id", "id_document_number", "lei", "crn", "electronic_address", "partner_name"]
        if not any(record.get(field) for field in strong_fields):
            record["partner_name"] = " ".join(part for part in [record.get("legal_first_name"), record.get("additional_name")] if part) or "Known Entity"


def mutate_variant(record: dict[str, Any], rng: random.Random) -> None:
    """Introduce realistic variations for records in the same latent entity cluster."""
    if record["record_type"] == "PERSON":
        first_name = (record.get("legal_first_name") or "").strip()
        last_name = (record.get("additional_name") or "").strip()
        if first_name and last_name and maybe(rng, 0.70):
            record["partner_name"] = person_name_variant(rng, first_name, last_name)
    else:
        partner_name = (record.get("partner_name") or "").strip()
        if partner_name and maybe(rng, 0.75):
            record["partner_name"] = org_name_variant(rng, partner_name)

    if record.get("address_residence_identifier") and maybe(rng, 0.25):
        record["address_residence_identifier"] = str(record["address_residence_identifier"]).replace(" ", "")

    if record.get("electronic_address") and "@" in str(record["electronic_address"]) and maybe(rng, 0.20):
        local, _, domain = str(record["electronic_address"]).partition("@")
        record["electronic_address"] = f"{local.replace('.', '_')}@{domain}"


def to_input_record(
    profile: dict[str, Any],
    record_number: int,
    ipg_id: str | None,
    rng: random.Random,
) -> dict[str, Any]:
    """Convert profile into source/base record schema."""
    class_code = "I" if profile["record_type"] == "PERSON" else rng.choice(["C", "S"])

    return {
        "externalPartnerKeyDirExternalID": f"PTN-{record_number:09d}",
        "partnerKeyDirBusRelExternalID": f"BRL-{record_number:09d}",
        "PartnerClassCode": class_code,
        "PartnerName": profile.get("partner_name"),
        "LegalFirstName": profile.get("legal_first_name"),
        "AdditionalName": profile.get("additional_name"),
        "BirthOrFoundationDate": profile.get("birth_or_foundation_date"),
        "DomicileCountryCode": profile.get("country_code"),
        "PrimeNationalityCountryCode": profile.get("prime_nationality_country_code"),
        "AddressStreetName": profile.get("address_street_name"),
        "AddressResidenceIdentifier": profile.get("address_residence_identifier"),
        "AddressPostalCode": profile.get("address_postal_code"),
        "AddressPostalCityName": profile.get("address_postal_city_name"),
        "LEI": profile.get("lei"),
        "LEM ID": profile.get("lem_id"),
        "CRN": profile.get("crn"),
        "Tax ID": profile.get("tax_id"),
        "idDocumentNumber": profile.get("id_document_number"),
        "Electronic Address": profile.get("electronic_address"),
        "IPG ID": ipg_id,
    }


def cluster_sizes_for_records(total_cluster_records: int, rng: random.Random) -> list[int]:
    """Split cluster-target records into sizes 2..4."""
    sizes: list[int] = []
    remaining = total_cluster_records
    while remaining > 0:
        size = rng.choice([2, 2, 3, 3, 4])
        if size > remaining:
            size = remaining
        if remaining - size == 1:
            size += 1
        sizes.append(size)
        remaining -= size
    return sizes


def generate_dataset(
    records: int,
    person_ratio: float,
    ipg_rate: float,
    seed: int,
    output_path: Path,
) -> dict[str, Any]:
    """Generate dataset and write JSON array streaming to disk."""
    rng = random.Random(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ipg_target_records = int(round(records * ipg_rate))
    cluster_sizes = cluster_sizes_for_records(ipg_target_records, rng)

    stats = {
        "records_total": records,
        "records_with_ipg_id": 0,
        "person_records": 0,
        "organization_records": 0,
        "clusters_with_ipg_id": len(cluster_sizes),
    }

    record_number = 0
    ipg_counter = 0

    with output_path.open("w", encoding="utf-8") as out:
        out.write("[")

        def write_record(payload: dict[str, Any], is_first: bool) -> None:
            if not is_first:
                out.write(",\n")
            out.write(json.dumps(payload, ensure_ascii=False))

        first = True

        # 1) Records with IPG clusters (known internal matches).
        for size in cluster_sizes:
            ipg_counter += 1
            ipg_id = f"IPG-{ipg_counter:09d}"
            record_type = choose_record_type(rng, person_ratio)
            anchor_profile = build_profile(record_type, rng)

            for member_index in range(size):
                profile = dict(anchor_profile)
                if member_index > 0:
                    mutate_variant(profile, rng)
                apply_sparsity(profile, record_type, rng, clustered=True)

                record_number += 1
                payload = to_input_record(profile, record_number, ipg_id, rng)
                write_record(payload, first)
                first = False

                stats["records_with_ipg_id"] += 1
                if record_type == "PERSON":
                    stats["person_records"] += 1
                else:
                    stats["organization_records"] += 1

        # 2) Remaining singleton records without IPG.
        while record_number < records:
            record_type = choose_record_type(rng, person_ratio)
            profile = build_profile(record_type, rng)
            apply_sparsity(profile, record_type, rng, clustered=False)

            record_number += 1
            payload = to_input_record(profile, record_number, None, rng)
            write_record(payload, first)
            first = False

            if record_type == "PERSON":
                stats["person_records"] += 1
            else:
                stats["organization_records"] += 1

        out.write("\n]\n")

    return stats


def run_mapper(repo_root: Path, input_json: Path, output_jsonl: Path, field_map_path: Path) -> int:
    """Run existing mapper script."""
    mapper = repo_root / "senzing" / "tools" / "partner_json_to_senzing.py"
    command = [
        sys.executable,
        str(mapper),
        str(input_json),
        str(output_jsonl),
        "--data-source",
        "PARTNERS",
        "--tax-id-type",
        "TIN",
        "--write-field-map",
        str(field_map_path),
    ]
    result = subprocess.run(command, check=False)
    return result.returncode


def parse_args() -> argparse.Namespace:
    """CLI parser."""
    parser = argparse.ArgumentParser(description="Generate realistic partner sample and Senzing JSONL.")
    parser.add_argument("--records", type=int, default=500000, help="Number of records to generate (default: 500000)")
    parser.add_argument("--person-ratio", type=float, default=0.70, help="Share of person records in [0,1] (default: 0.70)")
    parser.add_argument("--ipg-rate", type=float, default=0.35, help="Share of records with IPG ID in [0,1] (default: 0.35)")
    parser.add_argument("--seed", type=int, default=20260226, help="Random seed for reproducibility")
    parser.add_argument("--sample-dir", default="sample", help="Directory for generated base input JSON files")
    parser.add_argument("--output-dir", default="output", help="Directory for mapped JSONL and metadata")
    parser.add_argument("--skip-mapper", action="store_true", help="Generate base sample only, skip mapper conversion")
    return parser.parse_args()


def main() -> int:
    """Entry point."""
    args = parse_args()
    if args.records <= 0:
        print("ERROR: --records must be > 0", file=sys.stderr)
        return 2
    if not 0.0 <= args.person_ratio <= 1.0:
        print("ERROR: --person-ratio must be in [0,1]", file=sys.stderr)
        return 2
    if not 0.0 <= args.ipg_rate <= 1.0:
        print("ERROR: --ipg-rate must be in [0,1]", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[2]
    sample_dir = (repo_root / args.sample_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    sample_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = now_timestamp()
    base_input_path = sample_dir / f"partner_input_realistic_{args.records}_{timestamp}.json"
    mapped_output_path = output_dir / f"partner_output_senzing_{args.records}_{timestamp}.jsonl"
    field_map_path = output_dir / f"field_map_{args.records}_{timestamp}.json"
    metadata_path = output_dir / f"generation_summary_{args.records}_{timestamp}.json"

    print(f"Generating base input: {base_input_path}")
    stats = generate_dataset(
        records=args.records,
        person_ratio=args.person_ratio,
        ipg_rate=args.ipg_rate,
        seed=args.seed,
        output_path=base_input_path,
    )

    metadata: dict[str, Any] = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "seed": args.seed,
        "records": args.records,
        "person_ratio_target": args.person_ratio,
        "ipg_rate_target": args.ipg_rate,
        "base_input_json": str(base_input_path),
        "mapped_output_jsonl": None if args.skip_mapper else str(mapped_output_path),
        "field_map_json": None if args.skip_mapper else str(field_map_path),
        "stats": stats,
        "mapper_exit_code": None,
    }

    if not args.skip_mapper:
        print(f"Mapping to Senzing JSONL: {mapped_output_path}")
        exit_code = run_mapper(repo_root, base_input_path, mapped_output_path, field_map_path)
        metadata["mapper_exit_code"] = exit_code
        if exit_code != 0:
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"ERROR: mapper failed with exit code {exit_code}", file=sys.stderr)
            print(f"Metadata: {metadata_path}", file=sys.stderr)
            return 1

    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Done.")
    print(f"Base sample: {base_input_path}")
    if not args.skip_mapper:
        print(f"Senzing JSONL: {mapped_output_path}")
        print(f"Field map: {field_map_path}")
    print(f"Summary: {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

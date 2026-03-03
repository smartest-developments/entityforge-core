#!/usr/bin/env python3
"""Generate one stress sample (default 1,000,000 rows) for MVP as source-style JSONL.

This generator is intentionally single-sample and high-volume.
It produces a mixed PERSON/ORGANIZATION dataset with:
- SOURCE_TRUE_GROUP_ID for ground-truth grouping
- noisy/partial IPG labels to challenge baseline precision/recall
- mixed data quality scenarios (sparse, name/address/id noise, duplicate pressure)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import string
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

SCENARIOS: list[tuple[str, float]] = [
    ("clean", 0.20),
    ("sparse", 0.18),
    ("name_noise", 0.14),
    ("address_noise", 0.12),
    ("id_noise", 0.12),
    ("duplicate_pressure", 0.10),
    ("mixed", 0.14),
]

IPG_MODES: list[tuple[str, float]] = [
    ("aligned", 0.52),
    ("split", 0.15),
    ("missing", 0.23),
    ("collision", 0.10),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one stress sample JSONL for MVP")
    parser.add_argument("--records", type=int, default=1_000_000, help="Rows to generate (default: 1000000)")
    parser.add_argument("--seed", type=int, default=20260303, help="Deterministic RNG seed")
    parser.add_argument("--person-ratio", type=float, default=0.68, help="Share of PERSON entities (default: 0.68)")
    parser.add_argument("--sample-dir", default="sample_input", help="Target sample directory under MVP")
    parser.add_argument("--output-file", default="one_million_stress.jsonl", help="Output JSONL filename")
    parser.add_argument(
        "--metadata-file",
        default="one_million_stress.metadata.json",
        help="Metadata summary filename",
    )
    parser.add_argument(
        "--clean-legacy-samples",
        action="store_true",
        help="Delete legacy sample_*.json/jsonl files in sample_dir before generation",
    )
    return parser.parse_args()


def weighted_choice(rng: random.Random, choices: list[tuple[str, float]]) -> str:
    labels = [item[0] for item in choices]
    weights = [item[1] for item in choices]
    return rng.choices(labels, weights=weights, k=1)[0]


def maybe(rng: random.Random, probability: float) -> bool:
    return rng.random() < probability


def random_date(rng: random.Random, start_year: int, end_year: int) -> str:
    year = rng.randint(start_year, end_year)
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def random_postal_code(rng: random.Random, country_code: str) -> str:
    if country_code in {"US", "DE", "FR", "IT", "ES", "NL", "CH"}:
        return f"{rng.randint(10000, 99999)}"
    if country_code == "GB":
        return (
            f"{rng.choice(string.ascii_uppercase)}{rng.randint(1,9)} "
            f"{rng.randint(1,9)}{rng.choice(string.ascii_uppercase)}{rng.choice(string.ascii_uppercase)}"
        )
    return f"{rng.randint(10000, 999999)}"


def random_tax_id(rng: random.Random, country_code: str, is_org: bool) -> str:
    if is_org:
        return f"{country_code}{rng.randint(100000000, 999999999)}"
    return (
        f"{country_code}{rng.randint(10, 99)}{rng.choice(string.ascii_uppercase)}"
        f"{rng.randint(100000, 999999)}{rng.choice(string.ascii_uppercase)}"
    )


def random_other_id(rng: random.Random, prefix: str, country_code: str) -> str:
    return f"{prefix}-{country_code}-{rng.randint(100000, 999999)}"


def ascii_slug(text: str) -> str:
    chars = []
    for ch in text.lower():
        if ch.isalnum():
            chars.append(ch)
        elif ch in {" ", "-", "_"}:
            chars.append("-")
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "entity"


def choose_record_type(rng: random.Random, person_ratio: float) -> str:
    return "PERSON" if rng.random() < person_ratio else "ORGANIZATION"


def build_profile(record_type: str, rng: random.Random) -> dict[str, Any]:
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
        return {
            "record_type": record_type,
            "country_code": country_code,
            "partner_name": partner_name,
            "legal_first_name": first_name,
            "additional_name": last_name,
            "birth_or_foundation_date": random_date(rng, 1950, 2005),
            "prime_nationality_country_code": country_code,
            "address_street_name": street,
            "address_residence_identifier": house_number,
            "address_postal_code": postal_code,
            "address_postal_city_name": city,
            "lei": None,
            "lem_id": random_other_id(rng, "LEM", country_code) if maybe(rng, 0.25) else None,
            "crn": random_other_id(rng, "CRN", country_code) if maybe(rng, 0.07) else None,
            "tax_id": random_tax_id(rng, country_code, is_org=False),
            "id_document_number": random_other_id(rng, "DOC", country_code),
            "electronic_address": f"{ascii_slug(first_name)}.{ascii_slug(last_name)}@mail.{tld}",
        }

    org_name = f"{rng.choice(ORG_PREFIX)} {rng.choice(ORG_CORE)} {rng.choice(ORG_SUFFIX)}"
    return {
        "record_type": record_type,
        "country_code": country_code,
        "partner_name": org_name,
        "legal_first_name": None,
        "additional_name": None,
        "birth_or_foundation_date": random_date(rng, 1970, 2025),
        "prime_nationality_country_code": country_code,
        "address_street_name": street,
        "address_residence_identifier": house_number,
        "address_postal_code": postal_code,
        "address_postal_city_name": city,
        "lei": random_other_id(rng, "LEI", country_code) if maybe(rng, 0.58) else None,
        "lem_id": random_other_id(rng, "LEM", country_code) if maybe(rng, 0.48) else None,
        "crn": random_other_id(rng, "CRN", country_code) if maybe(rng, 0.80) else None,
        "tax_id": random_tax_id(rng, country_code, is_org=True),
        "id_document_number": None,
        "electronic_address": f"https://www.{ascii_slug(org_name)}.{tld}",
    }


def apply_variant_noise(profile: dict[str, Any], scenario: str, rng: random.Random, member_index: int) -> None:
    if member_index > 0 and isinstance(profile.get("partner_name"), str):
        base_name = str(profile["partner_name"])
        profile["partner_name"] = rng.choice([
            base_name,
            base_name.upper(),
            base_name.lower(),
            base_name.replace(",", ""),
            f" {base_name} ",
        ])

    if scenario in {"sparse", "mixed", "duplicate_pressure"}:
        for key, prob in [
            ("legal_first_name", 0.24),
            ("additional_name", 0.24),
            ("address_street_name", 0.30),
            ("address_residence_identifier", 0.34),
            ("address_postal_code", 0.26),
            ("address_postal_city_name", 0.24),
            ("tax_id", 0.20),
            ("id_document_number", 0.30),
            ("electronic_address", 0.28),
        ]:
            if maybe(rng, prob):
                profile[key] = None

    if scenario in {"name_noise", "mixed", "duplicate_pressure"} and isinstance(profile.get("partner_name"), str):
        name = str(profile["partner_name"])
        profile["partner_name"] = rng.choice([
            name,
            name.upper(),
            name.lower(),
            name.replace(" ", "  "),
            name.replace(".", "").replace(",", ""),
        ])

    if scenario in {"address_noise", "mixed"}:
        if maybe(rng, 0.45):
            profile["address_street_name"] = None
        if maybe(rng, 0.35):
            profile["address_postal_city_name"] = None
        if maybe(rng, 0.30):
            profile["address_postal_code"] = None

    if scenario in {"id_noise", "mixed"}:
        if isinstance(profile.get("tax_id"), str) and maybe(rng, 0.40):
            profile["tax_id"] = str(profile["tax_id"]).replace("-", "")[:8]
        if isinstance(profile.get("id_document_number"), str) and maybe(rng, 0.32):
            profile["id_document_number"] = f"BAD-{rng.randint(100, 999)}"
        if maybe(rng, 0.10):
            profile["tax_id"] = None


def profile_to_record(
    profile: dict[str, Any],
    row_number: int,
    true_group_id: str,
    ipg_id: str | None,
) -> dict[str, Any]:
    record_type = str(profile["record_type"])
    class_code = "I" if record_type == "PERSON" else "O"
    return {
        "externalPartnerKeyDirExternalID": f"EXT-{row_number:012d}",
        "partnerKeyDirBusRelExternalID": f"BR-{row_number:012d}",
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
        "SOURCE_TRUE_GROUP_ID": true_group_id,
    }


def choose_group_size(rng: random.Random, remaining: int) -> int:
    if remaining <= 1:
        return 1
    size = rng.choices([1, 2, 3, 4, 5, 6], weights=[0.40, 0.26, 0.16, 0.10, 0.05, 0.03], k=1)[0]
    if size > remaining:
        size = remaining
    return max(1, size)


def assign_ipg(
    ipg_mode: str,
    group_id_num: int,
    member_index: int,
    group_size: int,
    rng: random.Random,
    collision_pool: list[str],
) -> str | None:
    if ipg_mode == "aligned":
        if member_index > 0 and maybe(rng, 0.06):
            return None
        return f"IPG-{group_id_num:09d}"

    if ipg_mode == "missing":
        return None

    if ipg_mode == "split":
        if group_size == 1:
            return None
        buckets = 2 if group_size < 5 else 3
        bucket = member_index % buckets
        if maybe(rng, 0.12):
            return None
        return f"IPG-{group_id_num:09d}-S{bucket+1}"

    # collision
    chosen = rng.choice(collision_pool)
    if maybe(rng, 0.10):
        return None
    return chosen


def clean_legacy_samples(sample_dir: Path, output_file: str, metadata_file: str) -> None:
    keep = {output_file, metadata_file, "README.md", ".gitkeep"}
    for path in sorted(sample_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name in keep:
            continue
        if path.suffix.lower() in {".json", ".jsonl", ".md"} and (
            path.name.startswith("sample_")
            or path.name.startswith("partner_input_realistic_")
            or path.name == "SAMPLE_CATALOG.md"
        ):
            path.unlink(missing_ok=True)


def generate_one_sample(
    output_jsonl_path: Path,
    metadata_path: Path,
    records: int,
    seed: int,
    person_ratio: float,
) -> dict[str, Any]:
    rng = random.Random(seed)
    output_jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    collision_pool = [f"IPG-COLL-{idx:05d}" for idx in range(1, 4001)]

    stats: dict[str, Any] = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "seed": seed,
        "records_total": records,
        "target_person_ratio": person_ratio,
        "output_file": str(output_jsonl_path),
        "rows_with_ipg": 0,
        "rows_without_ipg": 0,
        "person_rows": 0,
        "organization_rows": 0,
        "true_groups": 0,
        "ipg_mode_counts": {"aligned": 0, "split": 0, "missing": 0, "collision": 0},
        "scenario_counts": {name: 0 for name, _ in SCENARIOS},
    }

    written = 0
    group_id_num = 0

    with output_jsonl_path.open("w", encoding="utf-8") as outfile:
        while written < records:
            remaining = records - written
            group_size = choose_group_size(rng, remaining)
            group_id_num += 1
            true_group_id = f"TG-{group_id_num:09d}"

            record_type = choose_record_type(rng, person_ratio)
            scenario = weighted_choice(rng, SCENARIOS)
            ipg_mode = weighted_choice(rng, IPG_MODES)
            base_profile = build_profile(record_type, rng)

            stats["true_groups"] += 1
            stats["ipg_mode_counts"][ipg_mode] += 1
            stats["scenario_counts"][scenario] += 1

            for member_index in range(group_size):
                profile = dict(base_profile)
                apply_variant_noise(profile, scenario=scenario, rng=rng, member_index=member_index)
                ipg_id = assign_ipg(
                    ipg_mode=ipg_mode,
                    group_id_num=group_id_num,
                    member_index=member_index,
                    group_size=group_size,
                    rng=rng,
                    collision_pool=collision_pool,
                )

                row_number = written + 1
                record = profile_to_record(
                    profile=profile,
                    row_number=row_number,
                    true_group_id=true_group_id,
                    ipg_id=ipg_id,
                )
                outfile.write(json.dumps(record, ensure_ascii=False) + "\n")

                if ipg_id:
                    stats["rows_with_ipg"] += 1
                else:
                    stats["rows_without_ipg"] += 1

                if record_type == "PERSON":
                    stats["person_rows"] += 1
                else:
                    stats["organization_rows"] += 1

                written += 1
                if written % 100_000 == 0:
                    print(f"Generated {written:,}/{records:,} rows...")

    person_ratio_actual = (stats["person_rows"] / records) if records > 0 else 0.0
    stats["actual_person_ratio"] = round(person_ratio_actual, 4)
    stats["actual_ipg_rate"] = round((stats["rows_with_ipg"] / records) if records > 0 else 0.0, 4)
    stats["notes"] = [
        "Single high-volume stress sample for 1M+ runs.",
        "Includes SOURCE_TRUE_GROUP_ID and noisy IPG labeling to produce baseline FP/FN variability.",
        "Use with MVP/run_mvp_pipeline.py directly on JSONL input.",
    ]

    metadata_path.write_text(json.dumps(stats, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    args = parse_args()
    if args.records <= 0:
        print("ERROR: --records must be > 0")
        return 2
    if not 0.0 < args.person_ratio < 1.0:
        print("ERROR: --person-ratio must be between 0 and 1")
        return 2

    mvp_root = Path(__file__).resolve().parent
    sample_dir = (mvp_root / args.sample_dir).resolve()
    sample_dir.mkdir(parents=True, exist_ok=True)

    output_jsonl_path = sample_dir / args.output_file
    metadata_path = sample_dir / args.metadata_file

    if args.clean_legacy_samples:
        clean_legacy_samples(sample_dir=sample_dir, output_file=args.output_file, metadata_file=args.metadata_file)

    stats = generate_one_sample(
        output_jsonl_path=output_jsonl_path,
        metadata_path=metadata_path,
        records=args.records,
        seed=args.seed,
        person_ratio=args.person_ratio,
    )

    print("\nOne-million stress sample generation complete.")
    print(f"- Output JSONL: {output_jsonl_path}")
    print(f"- Metadata: {metadata_path}")
    print(f"- Rows: {stats['records_total']:,}")
    print(f"- True groups: {stats['true_groups']:,}")
    print(f"- IPG rate: {stats['actual_ipg_rate']:.4f}")
    print(f"- Person ratio: {stats['actual_person_ratio']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

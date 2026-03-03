#!/usr/bin/env python3
"""Generate curated MVP sample_input JSON files with top-level comment metadata."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PROFILES: list[dict[str, Any]] = [
    {
        "filename": "sample_01_legacy_baseline_500.json",
        "description": "Legacy baseline sample kept for continuity with previous MVP runs.",
        "features": [
            "original 500-record baseline",
            "mixed PERSON/ORGANIZATION",
            "default sparsity pattern",
            "includes hidden true matches without IPG labels",
        ],
        "source": "legacy",
    },
    {
        "filename": "sample_02_balanced_baseline_500.json",
        "description": "Balanced baseline with default realism and moderate IPG coverage.",
        "features": [
            "balanced person/org split",
            "moderate missing fields",
            "standard noise",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027101,
        "person_ratio": 0.70,
        "ipg_rate": 0.35,
        "mutations": [],
    },
    {
        "filename": "sample_03_sparse_fields_500.json",
        "description": "High sparsity scenario with many optional fields missing.",
        "features": [
            "aggressive null optional fields",
            "harder matching due to low completeness",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027102,
        "person_ratio": 0.70,
        "ipg_rate": 0.30,
        "mutations": ["sparse"],
    },
    {
        "filename": "sample_04_name_noise_500.json",
        "description": "Name formatting noise (case/punctuation/spacing variations).",
        "features": [
            "name normalization stress",
            "formatting inconsistencies",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027103,
        "person_ratio": 0.72,
        "ipg_rate": 0.35,
        "mutations": ["name_noise"],
    },
    {
        "filename": "sample_05_taxid_noise_500.json",
        "description": "Tax ID quality issues with malformed identifiers on a subset of records.",
        "features": [
            "identifier quality degradation",
            "weaker deterministic signals",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027104,
        "person_ratio": 0.68,
        "ipg_rate": 0.35,
        "mutations": ["tax_noise"],
    },
    {
        "filename": "sample_06_address_noise_500.json",
        "description": "Address inconsistencies and partial address drops.",
        "features": [
            "address quality stress",
            "missing residence/street/postal values",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027105,
        "person_ratio": 0.70,
        "ipg_rate": 0.35,
        "mutations": ["address_noise"],
    },
    {
        "filename": "sample_07_duplicate_pressure_500.json",
        "description": "Higher duplicate pressure by making subsets look near-identical.",
        "features": [
            "larger ambiguous clusters",
            "false positive/negative pressure",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027106,
        "person_ratio": 0.70,
        "ipg_rate": 0.35,
        "mutations": ["duplicate_pressure"],
    },
    {
        "filename": "sample_08_organization_heavy_500.json",
        "description": "Organization-heavy dataset with more corporate records than persons.",
        "features": [
            "organization-heavy",
            "different identifier mix",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027107,
        "person_ratio": 0.40,
        "ipg_rate": 0.32,
        "mutations": [],
    },
    {
        "filename": "sample_09_person_heavy_low_ipg_500.json",
        "description": "Person-heavy dataset with low SOURCE IPG labeling coverage.",
        "features": [
            "person-heavy",
            "low IPG labels",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027108,
        "person_ratio": 0.88,
        "ipg_rate": 0.15,
        "mutations": [],
    },
    {
        "filename": "sample_10_high_ipg_coverage_500.json",
        "description": "High SOURCE IPG coverage for comparison against lower-labeling scenarios.",
        "features": [
            "high IPG labels",
            "quality evaluation easier",
            "includes hidden true matches without IPG labels",
        ],
        "seed": 2027109,
        "person_ratio": 0.70,
        "ipg_rate": 0.65,
        "mutations": [],
    },
]

EXTRA_SCENARIO_TEMPLATES: list[dict[str, Any]] = [
    {
        "slug": "compound_noise",
        "description": "Compound noise on names and addresses with moderate sparsity.",
        "features": ["combined name/address noise", "moderate missing fields", "hidden true matches without IPG labels"],
        "person_ratio": 0.68,
        "ipg_rate": 0.30,
        "mutations": ["name_noise", "address_noise", "sparse"],
    },
    {
        "slug": "id_disruption",
        "description": "Identifier disruption with malformed tax IDs and duplicate pressure.",
        "features": ["identifier degradation", "duplicate pressure", "higher ambiguity on deterministic keys"],
        "person_ratio": 0.66,
        "ipg_rate": 0.32,
        "mutations": ["tax_noise", "duplicate_pressure"],
    },
    {
        "slug": "org_sparse_mix",
        "description": "Organization-heavy sparse mix with reduced field completeness.",
        "features": ["organization-heavy", "aggressive sparsity", "address inconsistency"],
        "person_ratio": 0.42,
        "ipg_rate": 0.28,
        "mutations": ["sparse", "address_noise"],
    },
    {
        "slug": "person_chaos_low_ipg",
        "description": "Person-heavy sample with low IPG labels and multi-signal noise.",
        "features": ["person-heavy", "low IPG coverage", "name+tax noise"],
        "person_ratio": 0.86,
        "ipg_rate": 0.14,
        "mutations": ["name_noise", "tax_noise"],
    },
    {
        "slug": "high_ipg_collision",
        "description": "High IPG label coverage with deliberate duplicate pressure stress.",
        "features": ["high IPG labels", "collision pressure", "match precision stress"],
        "person_ratio": 0.70,
        "ipg_rate": 0.68,
        "mutations": ["duplicate_pressure"],
    },
    {
        "slug": "full_stress_mix",
        "description": "Full stress profile combining sparse fields and multi-attribute noise.",
        "features": ["multi-noise profile", "high ambiguity", "hidden true clusters"],
        "person_ratio": 0.64,
        "ipg_rate": 0.27,
        "mutations": ["sparse", "name_noise", "tax_noise", "address_noise", "duplicate_pressure"],
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate curated sample_input files for MVP")
    parser.add_argument("--records", type=int, default=500, help="Records per sample (default: 500)")
    parser.add_argument("--samples", type=int, default=50, help="Number of curated samples to generate (default: 50)")
    parser.add_argument("--sample-dir", default="sample_input", help="Sample input directory under MVP")
    parser.add_argument("--output-dir", default="output", help="Output directory for generator metadata")
    return parser.parse_args()


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def filename_for_records(filename: str, records: int) -> str:
    marker = "_500.json"
    if filename.endswith(marker):
        return filename.removesuffix(marker) + f"_{records}.json"
    return filename


def build_profiles(samples: int, records: int) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    if samples <= 0:
        return profiles

    for idx, base in enumerate(PROFILES, start=1):
        if idx > samples:
            break
        clone = dict(base)
        clone["filename"] = filename_for_records(str(base["filename"]), records)
        profiles.append(clone)

    if samples <= len(PROFILES):
        return profiles

    extra_count = samples - len(PROFILES)
    for offset in range(extra_count):
        sample_idx = len(PROFILES) + offset + 1
        template = EXTRA_SCENARIO_TEMPLATES[offset % len(EXTRA_SCENARIO_TEMPLATES)]
        seed = 2028000 + sample_idx
        person_jitter = ((offset % 7) - 3) * 0.03
        ipg_jitter = ((offset % 5) - 2) * 0.035
        person_ratio = clamp(float(template["person_ratio"]) + person_jitter, 0.25, 0.92)
        ipg_rate = clamp(float(template["ipg_rate"]) + ipg_jitter, 0.08, 0.78)

        mutations = list(template["mutations"])
        if offset % 4 == 0 and "duplicate_pressure" not in mutations:
            mutations.append("duplicate_pressure")
        if offset % 6 == 0 and "sparse" not in mutations:
            mutations.append("sparse")
        if offset % 8 == 0 and "name_noise" not in mutations:
            mutations.append("name_noise")

        filename = f"sample_{sample_idx:02d}_{template['slug']}_{records}.json"
        description = (
            f"Extended stress scenario {sample_idx}: {template['description']} "
            f"(person_ratio={person_ratio:.2f}, ipg_rate={ipg_rate:.2f})."
        )
        features = list(template["features"]) + [
            "extended hard-case set for Senzing stress testing",
            f"seed={seed}",
        ]
        profiles.append(
            {
                "filename": filename,
                "description": description,
                "features": features,
                "seed": seed,
                "person_ratio": round(person_ratio, 4),
                "ipg_rate": round(ipg_rate, 4),
                "mutations": mutations,
            }
        )

    return profiles


def run_generator(repo_root: Path, sample_dir_arg: str, output_dir_arg: str, records: int, seed: int, person_ratio: float, ipg_rate: float) -> Path:
    cmd = [
        sys.executable,
        str(repo_root / "senzing/tools/generate_realistic_partner_dataset.py"),
        "--records",
        str(records),
        "--seed",
        str(seed),
        "--person-ratio",
        str(person_ratio),
        "--ipg-rate",
        str(ipg_rate),
        "--sample-dir",
        sample_dir_arg,
        "--output-dir",
        output_dir_arg,
        "--skip-mapper",
    ]
    before = {p for p in (repo_root / sample_dir_arg).glob(f"partner_input_realistic_{records}_*.json")}
    subprocess.run(cmd, cwd=str(repo_root), check=True)
    after = {p for p in (repo_root / sample_dir_arg).glob(f"partner_input_realistic_{records}_*.json")}
    created = sorted(after - before, key=lambda p: p.stat().st_mtime, reverse=True)
    if not created:
        # fallback: pick most recent matching file
        candidates = sorted(after, key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            raise FileNotFoundError("No generated sample file found")
        return candidates[0]
    return created[0]


def maybe(rng: random.Random, probability: float) -> bool:
    return rng.random() < probability


def class_code_to_type(class_code: str) -> str:
    code = str(class_code or "").strip().upper()
    return "PERSON" if code == "I" else "ORGANIZATION"


def mutate_hidden_name(anchor_name: str, rng: random.Random) -> str:
    if not anchor_name:
        return anchor_name
    variants = [
        anchor_name,
        anchor_name.upper(),
        anchor_name.lower(),
        anchor_name.replace(",", ""),
        anchor_name.replace("  ", " ").strip(),
    ]
    return rng.choice(variants)


def hide_part_of_email(value: str, rng: random.Random) -> str:
    if "@" not in value:
        return value
    local, at, domain = value.partition("@")
    if not local:
        return value
    if maybe(rng, 0.4):
        local = local.replace(".", "_")
    if maybe(rng, 0.3):
        local = local[: max(1, len(local) - 2)]
    return f"{local}{at}{domain}"


def impose_hidden_truth_clusters(records: list[dict[str, Any]], rng: random.Random) -> dict[str, int]:
    ipg_key = "IPG ID"
    true_key = "SOURCE_TRUE_GROUP_ID"

    ipg_group_map: dict[str, str] = {}
    hidden_group_counter = 0
    unlabeled_indices: list[int] = []

    for idx, record in enumerate(records):
        ipg_value = str(record.get(ipg_key) or "").strip()
        if ipg_value:
            group_id = ipg_group_map.setdefault(ipg_value, f"TG_IPG_{len(ipg_group_map)+1:05d}")
            record[true_key] = group_id
        else:
            unlabeled_indices.append(idx)
            record[true_key] = f"TG_SINGLE_{idx+1:05d}"

    if len(unlabeled_indices) < 6:
        return {"hidden_groups": 0, "hidden_records": 0}

    rng.shuffle(unlabeled_indices)
    hidden_target_records = max(20, min(len(unlabeled_indices) // 3, 150))
    consumed = 0
    cursor = 0

    while cursor + 1 < len(unlabeled_indices) and consumed < hidden_target_records:
        size = rng.choice([2, 2, 3, 3, 4])
        if cursor + size > len(unlabeled_indices):
            size = len(unlabeled_indices) - cursor
        if size < 2:
            break
        if consumed + size > hidden_target_records and hidden_group_counter >= 8:
            break

        group_indices = unlabeled_indices[cursor : cursor + size]
        cursor += size
        consumed += size
        hidden_group_counter += 1
        hidden_group_id = f"TG_HIDDEN_{hidden_group_counter:05d}"

        anchor = records[group_indices[0]]
        anchor_name = str(anchor.get("PartnerName") or "").strip()
        anchor_type = class_code_to_type(str(anchor.get("PartnerClassCode") or ""))

        for member_pos, idx in enumerate(group_indices):
            target = records[idx]
            target[true_key] = hidden_group_id
            if member_pos == 0:
                continue

            # Keep business IDs and IPG untouched, align identity signals to hidden anchor.
            target["PartnerClassCode"] = anchor.get("PartnerClassCode")
            for key in [
                "LegalFirstName",
                "AdditionalName",
                "BirthOrFoundationDate",
                "DomicileCountryCode",
                "PrimeNationalityCountryCode",
                "AddressStreetName",
                "AddressResidenceIdentifier",
                "AddressPostalCode",
                "AddressPostalCityName",
                "Tax ID",
                "idDocumentNumber",
                "LEI",
                "LEM ID",
                "CRN",
                "Electronic Address",
            ]:
                target[key] = anchor.get(key)

            if anchor_name:
                target["PartnerName"] = mutate_hidden_name(anchor_name, rng)
            if isinstance(target.get("Electronic Address"), str) and maybe(rng, 0.25):
                target["Electronic Address"] = hide_part_of_email(str(target["Electronic Address"]), rng)
            if anchor_type == "PERSON" and maybe(rng, 0.35):
                target["AddressResidenceIdentifier"] = None
            if anchor_type == "ORGANIZATION" and maybe(rng, 0.20):
                target["Tax ID"] = None

    return {"hidden_groups": hidden_group_counter, "hidden_records": consumed}


def apply_ipg_label_noise(
    records: list[dict[str, Any]],
    rng: random.Random,
    collision_rate: float,
    drop_rate: float,
) -> dict[str, int | float]:
    """Inject controlled IPG label noise to create baseline FP/FN variability."""
    ipg_key = "IPG ID"
    true_key = "SOURCE_TRUE_GROUP_ID"

    group_by_index: dict[int, str] = {}
    ipg_owner_group: dict[str, str] = {}
    for idx, record in enumerate(records):
        true_group = str(record.get(true_key) or "").strip()
        if not true_group:
            continue
        group_by_index[idx] = true_group
        ipg_id = str(record.get(ipg_key) or "").strip()
        if ipg_id and ipg_id not in ipg_owner_group:
            ipg_owner_group[ipg_id] = true_group

    if not group_by_index:
        return {
            "collision_rate": round(collision_rate, 4),
            "drop_rate": round(drop_rate, 4),
            "collisions_applied": 0,
            "drops_applied": 0,
        }

    ipg_candidates = list(ipg_owner_group.items())
    target_collisions = max(0, int(len(group_by_index) * collision_rate))
    target_drops = max(0, int(len(group_by_index) * drop_rate))

    collision_indices = list(group_by_index.keys())
    rng.shuffle(collision_indices)
    collisions_applied = 0
    for idx in collision_indices:
        if collisions_applied >= target_collisions:
            break
        true_group = group_by_index[idx]
        possible_ipg = [ipg for ipg, owner in ipg_candidates if owner != true_group]
        if not possible_ipg:
            continue
        new_ipg = rng.choice(possible_ipg)
        current_ipg = str(records[idx].get(ipg_key) or "").strip()
        if current_ipg == new_ipg:
            continue
        records[idx][ipg_key] = new_ipg
        collisions_applied += 1

    drop_indices = [idx for idx in group_by_index if str(records[idx].get(ipg_key) or "").strip()]
    rng.shuffle(drop_indices)
    drops_applied = 0
    for idx in drop_indices:
        if drops_applied >= target_drops:
            break
        records[idx][ipg_key] = None
        drops_applied += 1

    return {
        "collision_rate": round(collision_rate, 4),
        "drop_rate": round(drop_rate, 4),
        "collisions_applied": collisions_applied,
        "drops_applied": drops_applied,
    }


def apply_sparse(records: list[dict[str, Any]], rng: random.Random) -> None:
    optional_fields = [
        "LegalFirstName",
        "AdditionalName",
        "BirthOrFoundationDate",
        "PrimeNationalityCountryCode",
        "AddressStreetName",
        "AddressResidenceIdentifier",
        "AddressPostalCode",
        "AddressPostalCityName",
        "LEI",
        "LEM ID",
        "CRN",
        "Tax ID",
        "idDocumentNumber",
        "Electronic Address",
    ]
    for record in records:
        for key in optional_fields:
            if key in record and maybe(rng, 0.30):
                record[key] = None


def apply_name_noise(records: list[dict[str, Any]], rng: random.Random) -> None:
    for record in records:
        name = record.get("PartnerName")
        if not isinstance(name, str) or not name.strip() or not maybe(rng, 0.35):
            continue
        variant = rng.choice([
            name.upper(),
            name.lower(),
            f" {name} ",
            name.replace(" ", "  "),
            name.replace(",", "").replace(".", ""),
        ])
        record["PartnerName"] = variant


def apply_tax_noise(records: list[dict[str, Any]], rng: random.Random) -> None:
    for record in records:
        if not maybe(rng, 0.22):
            continue
        tax_id = record.get("Tax ID")
        if not tax_id:
            continue
        if maybe(rng, 0.50):
            record["Tax ID"] = str(tax_id).replace("-", "").replace(" ", "")[:6]
        else:
            record["Tax ID"] = f"BAD-{rng.randint(100,999)}"


def apply_address_noise(records: list[dict[str, Any]], rng: random.Random) -> None:
    for record in records:
        if maybe(rng, 0.30):
            record["AddressStreetName"] = None
        if maybe(rng, 0.28):
            record["AddressPostalCityName"] = None
        if maybe(rng, 0.24):
            record["AddressPostalCode"] = None
        if isinstance(record.get("AddressResidenceIdentifier"), str) and maybe(rng, 0.20):
            record["AddressResidenceIdentifier"] = f" {record['AddressResidenceIdentifier']} "


def apply_duplicate_pressure(records: list[dict[str, Any]], rng: random.Random) -> None:
    if len(records) < 60:
        return
    indices = list(range(len(records)))
    rng.shuffle(indices)
    targets = indices[:60]
    sources = indices[60:120]
    if len(sources) < len(targets):
        sources = (sources * ((len(targets) // max(1, len(sources))) + 1))[: len(targets)]
    for target_idx, source_idx in zip(targets, sources):
        source = records[source_idx]
        target = records[target_idx]
        # Keep business IDs untouched, overwrite match-relevant content.
        for key in [
            "PartnerName",
            "LegalFirstName",
            "AdditionalName",
            "BirthOrFoundationDate",
            "AddressStreetName",
            "AddressResidenceIdentifier",
            "AddressPostalCode",
            "AddressPostalCityName",
            "Tax ID",
            "idDocumentNumber",
            "Electronic Address",
            "PrimeNationalityCountryCode",
            "LEI",
            "LEM ID",
            "CRN",
        ]:
            target[key] = source.get(key)
        if isinstance(target.get("PartnerName"), str) and maybe(rng, 0.60):
            target["PartnerName"] = target["PartnerName"].replace("  ", " ").strip()


MUTATORS = {
    "sparse": apply_sparse,
    "name_noise": apply_name_noise,
    "tax_noise": apply_tax_noise,
    "address_noise": apply_address_noise,
    "duplicate_pressure": apply_duplicate_pressure,
}


def ensure_array(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise TypeError("Expected array JSON payload")
    if not all(isinstance(item, dict) for item in payload):
        raise TypeError("Expected array of object records")
    return payload


def load_existing_legacy_records(sample_dir: Path, legacy_filename: str, expected_count: int) -> list[dict[str, Any]] | None:
    legacy_path = sample_dir / legacy_filename
    if not legacy_path.exists():
        return None
    try:
        payload = json.loads(legacy_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if isinstance(payload, list):
        records = ensure_array(payload)
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = ensure_array(payload["records"])
    else:
        return None

    if len(records) != expected_count:
        return None
    return records


def wrap_sample(filename: str, description: str, features: list[str], records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "_sample_name": filename.removesuffix(".json"),
        "_sample_comment": description,
        "_sample_special_features": features,
        "_records_count": len(records),
        "_generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "records": records,
    }


def write_catalog(sample_dir: Path, profiles: list[dict[str, Any]], records: int) -> None:
    lines = [
        "# Sample Input Catalog",
        "",
        f"All files contain {records} records in JSON format with top-level metadata and `records` array.",
        "",
    ]
    for idx, profile in enumerate(profiles, start=1):
        lines.append(f"{idx}. `{profile['filename']}`")
        lines.append(f"   - {profile['description']}")
        lines.append(f"   - Features: {', '.join(profile['features'])}")
    (sample_dir / "SAMPLE_CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.records <= 0:
        print("ERROR: --records must be > 0", file=sys.stderr)
        return 2
    if args.samples <= 0:
        print("ERROR: --samples must be > 0", file=sys.stderr)
        return 2

    mvp_root = Path(__file__).resolve().parent
    repo_root = mvp_root.parent
    sample_dir = (mvp_root / args.sample_dir).resolve()
    sample_dir.mkdir(parents=True, exist_ok=True)

    profiles = build_profiles(samples=args.samples, records=args.records)
    if not profiles:
        print("ERROR: no profiles generated", file=sys.stderr)
        return 2

    legacy_filename = str(profiles[0]["filename"])
    legacy_records = load_existing_legacy_records(sample_dir, legacy_filename, args.records)

    # Keep only current curated artifacts in sample_input.
    for path in sorted(sample_dir.glob("*.json")):
        path.unlink(missing_ok=True)
    for archive_dir in sorted(sample_dir.glob("archive_raw_*")):
        if archive_dir.is_dir():
            shutil.rmtree(archive_dir)

    temp_sample_arg = f"{mvp_root.relative_to(repo_root)}/sample_input"
    output_arg = f"{mvp_root.relative_to(repo_root)}/{args.output_dir}"

    generated_files: list[Path] = []

    for profile in profiles:
        filename = profile["filename"]

        if profile.get("source") == "legacy":
            if legacy_records is None:
                print("WARNING: legacy baseline not found; generating fresh baseline for sample_01")
                generated = run_generator(
                    repo_root=repo_root,
                    sample_dir_arg=temp_sample_arg,
                    output_dir_arg=output_arg,
                    records=args.records,
                    seed=2027100,
                    person_ratio=0.70,
                    ipg_rate=0.35,
                )
                array_data = ensure_array(json.loads(generated.read_text(encoding="utf-8")))
            else:
                array_data = legacy_records
        else:
            generated = run_generator(
                repo_root=repo_root,
                sample_dir_arg=temp_sample_arg,
                output_dir_arg=output_arg,
                records=args.records,
                seed=int(profile["seed"]),
                person_ratio=float(profile["person_ratio"]),
                ipg_rate=float(profile["ipg_rate"]),
            )
            array_data = ensure_array(json.loads(generated.read_text(encoding="utf-8")))

        if len(array_data) != args.records:
            raise ValueError(f"Sample {filename} has {len(array_data)} records, expected {args.records}")

        rng = random.Random(int(profile.get("seed", 2027000)))
        for mutation_name in profile.get("mutations", []):
            mutator = MUTATORS.get(mutation_name)
            if mutator is None:
                raise KeyError(f"Unknown mutation: {mutation_name}")
            mutator(array_data, rng)

        hidden_truth_stats = impose_hidden_truth_clusters(array_data, rng)
        ipg_rate = float(profile.get("ipg_rate", 0.35))
        collision_rate = float(
            profile.get(
                "ipg_collision_rate",
                clamp(0.015 + (1.0 - ipg_rate) * 0.03, 0.01, 0.08),
            )
        )
        drop_rate = float(
            profile.get(
                "ipg_drop_rate",
                clamp(0.04 + (1.0 - ipg_rate) * 0.12, 0.03, 0.20),
            )
        )
        ipg_noise_stats = apply_ipg_label_noise(
            records=array_data,
            rng=rng,
            collision_rate=collision_rate,
            drop_rate=drop_rate,
        )

        wrapped = wrap_sample(
            filename=filename,
            description=profile["description"],
            features=profile["features"],
            records=array_data,
        )
        wrapped["_hidden_truth_groups"] = hidden_truth_stats["hidden_groups"]
        wrapped["_hidden_truth_records"] = hidden_truth_stats["hidden_records"]
        wrapped["_ipg_label_noise"] = ipg_noise_stats

        target = sample_dir / filename
        target.write_text(json.dumps(wrapped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        generated_files.append(target)

    write_catalog(sample_dir, profiles, args.records)

    # Remove raw temporary generator outputs.
    for raw_path in sorted(sample_dir.glob("partner_input_realistic_*.json")):
        raw_path.unlink(missing_ok=True)

    print(f"Generated curated samples: {len(generated_files)}")
    for path in generated_files:
        print(f"- {path}")
    print(f"Catalog: {sample_dir / 'SAMPLE_CATALOG.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

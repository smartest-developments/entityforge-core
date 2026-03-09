# Partner JSON to Senzing Mapper

## Purpose

This guide describes how to convert a simple JSON array of partner records into Senzing-ready JSONL using:

- `S3Z/tools/partner_json_to_senzing.py`

The output JSONL can be validated with the existing toolkit tools and then loaded into Senzing.

## Dependencies

This mapper uses **Python standard library only**:

- `argparse`
- `datetime`
- `difflib`
- `json`
- `pathlib`
- `re`
- `sys`
- `typing`

No third-party packages are required.

## Input Contract

Expected input is a JSON file containing an array:

```json
[
  {
    "externalPartnerKeyDirExternalID": "P001024500220214",
    "partnerKeyDirBusRelExternalID": "024500220214",
    "PartnerClassCode": "I",
    "PartnerName": "Majszczyk",
    "LegalFirstName": "Agnieszka",
    "AdditionalName": null,
    "BirthOrFoundationDate": "1979-05-23",
    "DomicileCountryCode": "CH",
    "PrimeNationalityCountryCode": "PL",
    "AddressStreetName": "chemin des Bossons",
    "AddressResidenceIdentifier": "55",
    "AddressPostalCode": "1018",
    "AddressPostalCityName": "Lausanne",
    "LEI": null,
    "LEM ID": null,
    "CRN": null,
    "Tax ID": null,
    "idDocumentNumber": null,
    "Electronic Address": null,
    "IPG ID": "uY9bRmyYyLBBR91w"
  }
]
```

The script handles naming variations (spaces, snake_case, camelCase, mixed casing) through alias + fuzzy matching.

## Mapping Rules

### Record Type

`partner class code` is mapped as:

- `I` -> `RECORD_TYPE=PERSON`
- `C` -> `RECORD_TYPE=ORGANIZATION`
- `S` -> `RECORD_TYPE=ORGANIZATION` (as requested)

If class code is unknown/missing, no `RECORD_TYPE` feature is emitted.

### Feature Mapping

| Source Canonical Field | Senzing Output | Rule |
|---|---|---|
| Record position in input array | `RECORD_ID` | `RECORD_ID` is assigned as a simple increasing sequence: `"1"`, `"2"`, `"3"`, ... |
| `partner_class_code` | `RECORD_TYPE` | `I -> PERSON`, `C/S -> ORGANIZATION`. |
| `partner_name` | `NAME_ORG` or `NAME_FULL` | ORG -> `NAME_ORG`; non-ORG -> `NAME_FULL`. |
| `legal_first_name` + `additional_name` | Parsed person name | For non-ORG records: `NAME_FIRST` and `NAME_LAST` when available. |
| `birth_or_foundation_date` | `DATE_OF_BIRTH` or `REGISTRATION_DATE` | ORG -> registration date; otherwise DOB. |
| `prime_nationality_country_code` | `NATIONALITY` | Added as matching feature when present. |
| `address_street_name` + `address_residence_identifier` | `ADDR_LINE1` | Combined into one parsed street line. |
| `address_postal_city_name` | `ADDR_CITY` | Added to parsed address feature. |
| `address_postal_code` | `ADDR_POSTAL_CODE` | Added to parsed address feature. |
| `domicile_country_code` | `ADDR_COUNTRY` + `TAX_ID_COUNTRY` + ID country | Used for address, tax ID, and OTHER_ID country context. |
| `partner_class_code` | `ADDR_TYPE` | `BUSINESS` for organizations, `HOME` otherwise. |
| `tax_id` | `TAX_ID_*` | Emits `TAX_ID_TYPE`, `TAX_ID_NUMBER`, optional `TAX_ID_COUNTRY`. |
| `lei` | `LEI_NUMBER` | Added as LEI feature. |
| `lem_id` | `OTHER_ID_*` | `OTHER_ID_TYPE=LEM_ID`. |
| `crn` | `OTHER_ID_*` | `OTHER_ID_TYPE=CRN`. |
| `id_document_number` | `OTHER_ID_*` | `OTHER_ID_TYPE=ID_DOCUMENT_NUMBER`. |
| `external_partner_key_dir_external_id` | `OTHER_ID_*` | `OTHER_ID_TYPE=PARTNER_ID` (configurable via `--partner-id-feature-type`). |
| `partner_key_dir_bus_rel_external_id` | `OTHER_ID_*` | `OTHER_ID_TYPE=BUSINESS_RELATION_ID` (configurable via `--business-relation-feature-type`). |
| `ipg_id` | Payload only | Stored as `SOURCE_IPG_ID`; not used for matching features. |
| `electronic_address` | `EMAIL_ADDRESS` or `WEBSITE_ADDRESS` or `OTHER_ID_*` | Email-like values -> `EMAIL_ADDRESS`; URL/domain-like -> `WEBSITE_ADDRESS`; otherwise `OTHER_ID_TYPE=ELECTRONIC_ADDRESS`. |

### Payload Fields

The script stores only this **payload-only** operational source ID at root:

- `SOURCE_IPG_ID`

The two internal IDs are emitted in `FEATURES` as `OTHER_ID_*` matching features.
All other mapped fields are emitted in `FEATURES`.

Optional: with `--include-unmapped-source-fields`, unknown source attributes are copied as `SRC_<UPPER_SNAKE_CASE_NAME>`.

## CLI Usage

### One-command master pipeline (recommended)

Use the wrapper to run all steps in sequence (convert + lint + analyzer + stakeholder report):

```bash
python3 S3Z/tools/run_partner_mapping_pipeline.py \
  /path/to/input_partners.json
```

Each run creates a timestamped folder containing:

- `output.jsonl`
- `field_map.json`
- `analysis.md`
- `stakeholder_summary.md`
- `pipeline_summary.json`
- `logs/` (one log per step)

### Simplest run (recommended for restricted environments)

Run with input only. The script creates a timestamped run folder automatically:

```bash
python3 S3Z/tools/partner_json_to_senzing.py \
  /path/to/input_partners.json
```

Default run root: `mapper_runs/`  
Generated run folder format: `partner_mapping_YYYYMMDD_HHMMSS/`

Generated files per run:

- `output.jsonl`
- `field_map.json`
- `run_info.json`

### Basic conversion

```bash
python3 S3Z/tools/partner_json_to_senzing.py \
  /path/to/input_partners.json \
  /path/to/output_partners.jsonl \
  --data-source PARTNERS
```

### Recommended conversion (keep extra unmapped attributes + export inferred map)

```bash
python3 S3Z/tools/partner_json_to_senzing.py \
  /path/to/input_partners.json \
  /path/to/output_partners.jsonl \
  --data-source PARTNERS \
  --include-unmapped-source-fields \
  --write-field-map /path/to/inferred_field_map.json
```

### Strict mode

```bash
python3 S3Z/tools/partner_json_to_senzing.py \
  /path/to/input_partners.json \
  /path/to/output_partners.jsonl \
  --data-source PARTNERS \
  --strict
```

## Validation Workflow

After conversion:

1. Validate structure:

```bash
python3 S3Z/tools/lint_senzing_json.py /path/to/output_partners.jsonl
```

2. Analyze mapping quality:

```bash
python3 S3Z/tools/sz_json_analyzer.py \
  /path/to/output_partners.jsonl \
  -o /path/to/output_partners_analysis.md
```

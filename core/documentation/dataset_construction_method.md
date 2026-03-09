# Dataset Construction Method (Original Production JSON)

## Scope
This document describes how the original dataset was constructed from production JSON for the SCV Senzing PoC.

## Target Volume
- Total records: ~1,000,000
- Records with `IPGID` (matched universe): ~300,000
- Records without `IPGID` (non-matched universe): ~700,000

## Pre-Filtering Rules (Applied Before Sampling IPGID-Based Entities)
From the production source, the following populations were excluded:
- high-risk clients
- clients from Monaco

After these exclusions, the IPGID-based sample was created.

## Matched Universe (`IPGID` Present)

### Entity Selection Logic
We selected **100,000 IPGIDs** (entities), split by entity cardinality:

1. **50,000 IPGIDs** with entity size = 2  
   - two records per entity

2. **35,000 IPGIDs** with entity size = 3 or 4  
   - medium-size entities

3. **15,000 IPGIDs** with entity size >= 5  
   - larger entities

### Resulting Record Volume
By extracting all records linked to those 100,000 IPGIDs, we obtained approximately:
- **~300,000 records with IPGID**

Note:
- The final count is approximate because entities in the >=5 bucket have variable size.
- The 3/4-member bucket also includes variable cardinality by design.

## Non-Matched Universe (`IPGID` Missing)
For records without `IPGID` (treated as non-matched population), the composition is:

- **60% Individuals**
- **30% Companies**
- **10% Simple Partnerships** (operationally treated as Companies)

This block contributes approximately:
- **~700,000 records without IPGID**

## Final Dataset Composition (PoC Input)
The final PoC dataset is therefore:
- matched segment (`IPGID` present): ~300k records
- non-matched segment (`IPGID` missing): ~700k records
- total: ~1M records

## Terminology Clarification
- `IPGID` identifies an entity/group in the matched universe.
- "Entity size" means the number of records associated to one `IPGID`.
- Records without `IPGID` are intentionally included as unmatched/background population.

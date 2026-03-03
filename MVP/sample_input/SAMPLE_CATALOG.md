# Sample Input Catalog

All files contain 500 records in JSON format with top-level metadata and `records` array.

1. `sample_01_legacy_baseline_500.json`
   - Legacy baseline sample kept for continuity with previous MVP runs.
   - Features: original 500-record baseline, mixed PERSON/ORGANIZATION, default sparsity pattern, includes hidden true matches without IPG labels
2. `sample_02_balanced_baseline_500.json`
   - Balanced baseline with default realism and moderate IPG coverage.
   - Features: balanced person/org split, moderate missing fields, standard noise, includes hidden true matches without IPG labels
3. `sample_03_sparse_fields_500.json`
   - High sparsity scenario with many optional fields missing.
   - Features: aggressive null optional fields, harder matching due to low completeness, includes hidden true matches without IPG labels
4. `sample_04_name_noise_500.json`
   - Name formatting noise (case/punctuation/spacing variations).
   - Features: name normalization stress, formatting inconsistencies, includes hidden true matches without IPG labels
5. `sample_05_taxid_noise_500.json`
   - Tax ID quality issues with malformed identifiers on a subset of records.
   - Features: identifier quality degradation, weaker deterministic signals, includes hidden true matches without IPG labels
6. `sample_06_address_noise_500.json`
   - Address inconsistencies and partial address drops.
   - Features: address quality stress, missing residence/street/postal values, includes hidden true matches without IPG labels
7. `sample_07_duplicate_pressure_500.json`
   - Higher duplicate pressure by making subsets look near-identical.
   - Features: larger ambiguous clusters, false positive/negative pressure, includes hidden true matches without IPG labels
8. `sample_08_organization_heavy_500.json`
   - Organization-heavy dataset with more corporate records than persons.
   - Features: organization-heavy, different identifier mix, includes hidden true matches without IPG labels
9. `sample_09_person_heavy_low_ipg_500.json`
   - Person-heavy dataset with low SOURCE IPG labeling coverage.
   - Features: person-heavy, low IPG labels, includes hidden true matches without IPG labels
10. `sample_10_high_ipg_coverage_500.json`
   - High SOURCE IPG coverage for comparison against lower-labeling scenarios.
   - Features: high IPG labels, quality evaluation easier, includes hidden true matches without IPG labels
11. `sample_11_compound_noise_500.json`
   - Extended stress scenario 11: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.59, ipg_rate=0.23).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028011
12. `sample_12_id_disruption_500.json`
   - Extended stress scenario 12: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.60, ipg_rate=0.29).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028012
13. `sample_13_org_sparse_mix_500.json`
   - Extended stress scenario 13: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.39, ipg_rate=0.28).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028013
14. `sample_14_person_chaos_low_ipg_500.json`
   - Extended stress scenario 14: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.86, ipg_rate=0.18).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028014
15. `sample_15_high_ipg_collision_500.json`
   - Extended stress scenario 15: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.73, ipg_rate=0.75).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028015
16. `sample_16_full_stress_mix_500.json`
   - Extended stress scenario 16: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.70, ipg_rate=0.20).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028016
17. `sample_17_compound_noise_500.json`
   - Extended stress scenario 17: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.77, ipg_rate=0.27).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028017
18. `sample_18_id_disruption_500.json`
   - Extended stress scenario 18: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.57, ipg_rate=0.32).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028018
19. `sample_19_org_sparse_mix_500.json`
   - Extended stress scenario 19: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.36, ipg_rate=0.32).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028019
20. `sample_20_person_chaos_low_ipg_500.json`
   - Extended stress scenario 20: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.83, ipg_rate=0.21).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028020
21. `sample_21_high_ipg_collision_500.json`
   - Extended stress scenario 21: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.70, ipg_rate=0.61).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028021
22. `sample_22_full_stress_mix_500.json`
   - Extended stress scenario 22: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.67, ipg_rate=0.24).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028022
23. `sample_23_compound_noise_500.json`
   - Extended stress scenario 23: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.74, ipg_rate=0.30).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028023
24. `sample_24_id_disruption_500.json`
   - Extended stress scenario 24: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.75, ipg_rate=0.35).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028024
25. `sample_25_org_sparse_mix_500.json`
   - Extended stress scenario 25: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.33, ipg_rate=0.35).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028025
26. `sample_26_person_chaos_low_ipg_500.json`
   - Extended stress scenario 26: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.80, ipg_rate=0.08).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028026
27. `sample_27_high_ipg_collision_500.json`
   - Extended stress scenario 27: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.67, ipg_rate=0.65).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028027
28. `sample_28_full_stress_mix_500.json`
   - Extended stress scenario 28: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.64, ipg_rate=0.27).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028028
29. `sample_29_compound_noise_500.json`
   - Extended stress scenario 29: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.71, ipg_rate=0.33).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028029
30. `sample_30_id_disruption_500.json`
   - Extended stress scenario 30: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.72, ipg_rate=0.39).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028030
31. `sample_31_org_sparse_mix_500.json`
   - Extended stress scenario 31: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.51, ipg_rate=0.21).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028031
32. `sample_32_person_chaos_low_ipg_500.json`
   - Extended stress scenario 32: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.77, ipg_rate=0.11).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028032
33. `sample_33_high_ipg_collision_500.json`
   - Extended stress scenario 33: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.64, ipg_rate=0.68).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028033
34. `sample_34_full_stress_mix_500.json`
   - Extended stress scenario 34: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.61, ipg_rate=0.31).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028034
35. `sample_35_compound_noise_500.json`
   - Extended stress scenario 35: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.68, ipg_rate=0.37).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028035
36. `sample_36_id_disruption_500.json`
   - Extended stress scenario 36: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.69, ipg_rate=0.25).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028036
37. `sample_37_org_sparse_mix_500.json`
   - Extended stress scenario 37: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.48, ipg_rate=0.25).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028037
38. `sample_38_person_chaos_low_ipg_500.json`
   - Extended stress scenario 38: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.92, ipg_rate=0.14).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028038
39. `sample_39_high_ipg_collision_500.json`
   - Extended stress scenario 39: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.61, ipg_rate=0.72).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028039
40. `sample_40_full_stress_mix_500.json`
   - Extended stress scenario 40: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.58, ipg_rate=0.34).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028040
41. `sample_41_compound_noise_500.json`
   - Extended stress scenario 41: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.65, ipg_rate=0.23).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028041
42. `sample_42_id_disruption_500.json`
   - Extended stress scenario 42: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.66, ipg_rate=0.29).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028042
43. `sample_43_org_sparse_mix_500.json`
   - Extended stress scenario 43: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.45, ipg_rate=0.28).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028043
44. `sample_44_person_chaos_low_ipg_500.json`
   - Extended stress scenario 44: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.92, ipg_rate=0.18).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028044
45. `sample_45_high_ipg_collision_500.json`
   - Extended stress scenario 45: High IPG label coverage with deliberate duplicate pressure stress. (person_ratio=0.79, ipg_rate=0.75).
   - Features: high IPG labels, collision pressure, match precision stress, extended hard-case set for Senzing stress testing, seed=2028045
46. `sample_46_full_stress_mix_500.json`
   - Extended stress scenario 46: Full stress profile combining sparse fields and multi-attribute noise. (person_ratio=0.55, ipg_rate=0.20).
   - Features: multi-noise profile, high ambiguity, hidden true clusters, extended hard-case set for Senzing stress testing, seed=2028046
47. `sample_47_compound_noise_500.json`
   - Extended stress scenario 47: Compound noise on names and addresses with moderate sparsity. (person_ratio=0.62, ipg_rate=0.27).
   - Features: combined name/address noise, moderate missing fields, hidden true matches without IPG labels, extended hard-case set for Senzing stress testing, seed=2028047
48. `sample_48_id_disruption_500.json`
   - Extended stress scenario 48: Identifier disruption with malformed tax IDs and duplicate pressure. (person_ratio=0.63, ipg_rate=0.32).
   - Features: identifier degradation, duplicate pressure, higher ambiguity on deterministic keys, extended hard-case set for Senzing stress testing, seed=2028048
49. `sample_49_org_sparse_mix_500.json`
   - Extended stress scenario 49: Organization-heavy sparse mix with reduced field completeness. (person_ratio=0.42, ipg_rate=0.32).
   - Features: organization-heavy, aggressive sparsity, address inconsistency, extended hard-case set for Senzing stress testing, seed=2028049
50. `sample_50_person_chaos_low_ipg_500.json`
   - Extended stress scenario 50: Person-heavy sample with low IPG labels and multi-signal noise. (person_ratio=0.89, ipg_rate=0.21).
   - Features: person-heavy, low IPG coverage, name+tax noise, extended hard-case set for Senzing stress testing, seed=2028050

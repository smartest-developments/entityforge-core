# Dashboard Data Audit Report

- Generated at: 2026-03-03T11:14:25
- Output root: `/Users/simones/Developer/mapper-ai-main/MVP/output`
- Dashboard data: `/Users/simones/Developer/mapper-ai-main/MVP/dashboard/management_dashboard_data.js`
- Runs audited: 30
- Runs PASS: 30
- Runs FAIL: 0
- Runs SKIP: 0

## Run Summary

| Run ID | Source Input | Status |
|---|---|---|
| `20260302_135931__sample_30_id_disruption_500` | `sample_30_id_disruption_500.json` | **PASS** |
| `20260302_135845__sample_29_compound_noise_500` | `sample_29_compound_noise_500.json` | **PASS** |
| `20260302_135820__sample_28_full_stress_mix_500` | `sample_28_full_stress_mix_500.json` | **PASS** |
| `20260302_135753__sample_27_high_ipg_collision_500` | `sample_27_high_ipg_collision_500.json` | **PASS** |
| `20260302_135728__sample_26_person_chaos_low_ipg_500` | `sample_26_person_chaos_low_ipg_500.json` | **PASS** |
| `20260302_135702__sample_25_org_sparse_mix_500` | `sample_25_org_sparse_mix_500.json` | **PASS** |
| `20260302_135636__sample_24_id_disruption_500` | `sample_24_id_disruption_500.json` | **PASS** |
| `20260302_135613__sample_23_compound_noise_500` | `sample_23_compound_noise_500.json` | **PASS** |
| `20260302_134653__sample_22_full_stress_mix_500` | `sample_22_full_stress_mix_500.json` | **PASS** |
| `20260302_134620__sample_21_high_ipg_collision_500` | `sample_21_high_ipg_collision_500.json` | **PASS** |
| `20260302_134554__sample_20_person_chaos_low_ipg_500` | `sample_20_person_chaos_low_ipg_500.json` | **PASS** |
| `20260302_134530__sample_19_org_sparse_mix_500` | `sample_19_org_sparse_mix_500.json` | **PASS** |
| `20260302_134503__sample_18_id_disruption_500` | `sample_18_id_disruption_500.json` | **PASS** |
| `20260302_134437__sample_17_compound_noise_500` | `sample_17_compound_noise_500.json` | **PASS** |
| `20260302_134413__sample_16_full_stress_mix_500` | `sample_16_full_stress_mix_500.json` | **PASS** |
| `20260302_134349__sample_15_high_ipg_collision_500` | `sample_15_high_ipg_collision_500.json` | **PASS** |
| `20260302_134325__sample_14_person_chaos_low_ipg_500` | `sample_14_person_chaos_low_ipg_500.json` | **PASS** |
| `20260302_134301__sample_13_org_sparse_mix_500` | `sample_13_org_sparse_mix_500.json` | **PASS** |
| `20260302_134234__sample_12_id_disruption_500` | `sample_12_id_disruption_500.json` | **PASS** |
| `20260302_133902__sample_11_compound_noise_500` | `sample_11_compound_noise_500.json` | **PASS** |
| `20260302_133835__sample_10_high_ipg_coverage_500` | `sample_10_high_ipg_coverage_500.json` | **PASS** |
| `20260302_133809__sample_09_person_heavy_low_ipg_500` | `sample_09_person_heavy_low_ipg_500.json` | **PASS** |
| `20260302_133745__sample_08_organization_heavy_500` | `sample_08_organization_heavy_500.json` | **PASS** |
| `20260302_133718__sample_07_duplicate_pressure_500` | `sample_07_duplicate_pressure_500.json` | **PASS** |
| `20260302_133651__sample_06_address_noise_500` | `sample_06_address_noise_500.json` | **PASS** |
| `20260302_133628__sample_05_taxid_noise_500` | `sample_05_taxid_noise_500.json` | **PASS** |
| `20260302_133605__sample_04_name_noise_500` | `sample_04_name_noise_500.json` | **PASS** |
| `20260302_133541__sample_03_sparse_fields_500` | `sample_03_sparse_fields_500.json` | **PASS** |
| `20260302_133518__sample_02_balanced_baseline_500` | `sample_02_balanced_baseline_500.json` | **PASS** |
| `20260302_133451__sample_01_legacy_baseline_500` | `sample_01_legacy_baseline_500.json` | **PASS** |

## Failed Checks

No failed checks.

## Re-run

```bash
cd MVP
python3 verify_dashboard_metrics.py
```

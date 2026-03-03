window.MVP_DASHBOARD_DATA = {
  "generated_at": "2026-03-02T15:32:30",
  "output_root": "/Users/simones/Developer/mapper-ai-main/MVP/output",
  "runs": [
    {
      "run_id": "20260302_135931__sample_30_id_disruption_500",
      "run_timestamp": "20260302_135931",
      "run_datetime": "2026-03-02T13:59:31",
      "run_label": "sample_30_id_disruption_500",
      "source_input_name": "sample_30_id_disruption_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T13:00:26",
      "records_input": 500,
      "records_exported": 774,
      "our_resolved_entities": 64,
      "resolved_entities": 344,
      "matched_records": 281,
      "matched_pairs": 430,
      "pair_precision_pct": 82.56,
      "pair_recall_pct": 59.17,
      "true_positive": 71,
      "false_positive": 15,
      "false_negative": 49,
      "discovery_available": true,
      "extra_true_matches_found": 166,
      "extra_false_matches_found": 191,
      "extra_match_precision_pct": 46.5,
      "extra_match_recall_pct": 79.05,
      "extra_gain_vs_known_pct": 174.74,
      "known_pairs_ipg": 95,
      "discoverable_true_pairs": 210,
      "predicted_pairs_beyond_known": 357,
      "net_extra_matches": -25,
      "overall_false_positive_pct": 17.44,
      "overall_false_positive_discovery_pct": 44.42,
      "overall_match_correctness_pct": 55.58,
      "our_true_positive": 95,
      "our_true_pairs_total": 305,
      "our_false_positive": 25,
      "our_false_negative": 210,
      "our_match_coverage_pct": 31.15,
      "baseline_match_coverage_pct": 31.15,
      "senzing_true_coverage_pct": 78.36,
      "predicted_pairs_labeled": 86,
      "ground_truth_pairs_labeled": 120,
      "match_level_distribution": {
        "1": 156,
        "2": 274
      },
      "top_match_keys": [
        [
          "NAME",
          106
        ],
        [
          "NAME+DOB",
          31
        ],
        [
          "NAME+NATIONALITY",
          25
        ],
        [
          "NAME+DOB-TAX_ID",
          15
        ],
        [
          "NAME+DOB+NATIONALITY",
          12
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          10
        ],
        [
          "NAME+DOB+NATIONALITY-TAX_ID",
          9
        ],
        [
          "NAME+ADDRESS+TAX_ID+WEBSITE-RECORD_TYPE",
          6
        ],
        [
          "NAME+ADDRESS+WEBSITE-RECORD_TYPE",
          6
        ],
        [
          "NAME+DOB+ADDRESS",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 163,
        "2": 54,
        "3": 58,
        "4": 41,
        "5": 17,
        "6": 4,
        "7": 4,
        "8": 1,
        "10": 2
      },
      "entity_pairings_distribution": {
        "0": 163,
        "1": 54,
        "3": 58,
        "6": 41,
        "10": 17,
        "15": 4,
        "21": 4,
        "28": 1,
        "45": 2
      },
      "record_pairing_degree_distribution": {
        "0": 163,
        "1": 108,
        "2": 174,
        "3": 164,
        "4": 85,
        "5": 24,
        "6": 28,
        "7": 8,
        "9": 20
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135931__sample_30_id_disruption_500/input_source.json",
      "management_summary_path": "20260302_135931__sample_30_id_disruption_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135931__sample_30_id_disruption_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135931__sample_30_id_disruption_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1633
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 391096
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 6316
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 29028
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1016
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7678
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 312976
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 5053
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 24894
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 17684
        },
        {
          "relative_path": "20260302_135931__sample_30_id_disruption_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7629
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 430,
            "actual": 430,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 344,
            "actual": 344,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 82.56,
            "actual": 82.56,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 31.15,
            "actual": 31.15,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 17.44,
            "actual": 17.44,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 40.83,
            "actual": 40.83,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135931__sample_30_id_disruption_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135845__sample_29_compound_noise_500",
      "run_timestamp": "20260302_135845",
      "run_datetime": "2026-03-02T13:58:45",
      "run_label": "sample_29_compound_noise_500",
      "source_input_name": "sample_29_compound_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:59:31",
      "records_input": 500,
      "records_exported": 814,
      "our_resolved_entities": 55,
      "resolved_entities": 354,
      "matched_records": 278,
      "matched_pairs": 460,
      "pair_precision_pct": 80.0,
      "pair_recall_pct": 70.33,
      "true_positive": 64,
      "false_positive": 16,
      "false_negative": 27,
      "discovery_available": true,
      "extra_true_matches_found": 158,
      "extra_false_matches_found": 234,
      "extra_match_precision_pct": 40.31,
      "extra_match_recall_pct": 74.88,
      "extra_gain_vs_known_pct": 219.44,
      "known_pairs_ipg": 72,
      "discoverable_true_pairs": 211,
      "predicted_pairs_beyond_known": 392,
      "net_extra_matches": -76,
      "overall_false_positive_pct": 20.0,
      "overall_false_positive_discovery_pct": 50.87,
      "overall_match_correctness_pct": 49.13,
      "our_true_positive": 72,
      "our_true_pairs_total": 283,
      "our_false_positive": 19,
      "our_false_negative": 211,
      "our_match_coverage_pct": 25.44,
      "baseline_match_coverage_pct": 25.44,
      "senzing_true_coverage_pct": 79.86,
      "predicted_pairs_labeled": 80,
      "ground_truth_pairs_labeled": 91,
      "match_level_distribution": {
        "1": 146,
        "2": 314
      },
      "top_match_keys": [
        [
          "NAME",
          269
        ],
        [
          "NAME+NATIONALITY",
          24
        ],
        [
          "NAME+DOB",
          17
        ],
        [
          "NAME+DOB+NATIONALITY",
          14
        ],
        [
          "NAME+TAX_ID",
          11
        ],
        [
          "NAME+OTHER_ID",
          9
        ],
        [
          "NAME+REGISTRATION_DATE",
          9
        ],
        [
          "NAME+DOB+OTHER_ID",
          7
        ],
        [
          "NAME+WEBSITE",
          7
        ],
        [
          "NAME+DOB+TAX_ID",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 173,
        "2": 62,
        "3": 49,
        "4": 36,
        "5": 12,
        "6": 9,
        "7": 4,
        "8": 3,
        "9": 4,
        "10": 1,
        "14": 1
      },
      "entity_pairings_distribution": {
        "0": 173,
        "1": 62,
        "3": 49,
        "6": 36,
        "10": 12,
        "15": 9,
        "21": 4,
        "28": 3,
        "36": 4,
        "45": 1,
        "91": 1
      },
      "record_pairing_degree_distribution": {
        "0": 173,
        "1": 124,
        "2": 147,
        "3": 144,
        "4": 60,
        "5": 54,
        "6": 28,
        "7": 24,
        "8": 36,
        "9": 10,
        "13": 14
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135845__sample_29_compound_noise_500/input_source.json",
      "management_summary_path": "20260302_135845__sample_29_compound_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135845__sample_29_compound_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135845__sample_29_compound_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1632
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384502
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3805
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 25867
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1000
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5043
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 274788
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2224
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 21780
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 17104
        },
        {
          "relative_path": "20260302_135845__sample_29_compound_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7628
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 460,
            "actual": 460,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 354,
            "actual": 354,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 80.0,
            "actual": 80.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 25.44,
            "actual": 25.44,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 20.0,
            "actual": 20.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 29.67,
            "actual": 29.67,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135845__sample_29_compound_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135820__sample_28_full_stress_mix_500",
      "run_timestamp": "20260302_135820",
      "run_datetime": "2026-03-02T13:58:20",
      "run_label": "sample_28_full_stress_mix_500",
      "source_input_name": "sample_28_full_stress_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:58:45",
      "records_input": 500,
      "records_exported": 922,
      "our_resolved_entities": 43,
      "resolved_entities": 375,
      "matched_records": 299,
      "matched_pairs": 547,
      "pair_precision_pct": 97.22,
      "pair_recall_pct": 59.32,
      "true_positive": 35,
      "false_positive": 1,
      "false_negative": 24,
      "discovery_available": true,
      "extra_true_matches_found": 160,
      "extra_false_matches_found": 345,
      "extra_match_precision_pct": 31.68,
      "extra_match_recall_pct": 80.81,
      "extra_gain_vs_known_pct": 340.43,
      "known_pairs_ipg": 47,
      "discoverable_true_pairs": 198,
      "predicted_pairs_beyond_known": 505,
      "net_extra_matches": -185,
      "overall_false_positive_pct": 2.78,
      "overall_false_positive_discovery_pct": 63.07,
      "overall_match_correctness_pct": 36.93,
      "our_true_positive": 47,
      "our_true_pairs_total": 245,
      "our_false_positive": 12,
      "our_false_negative": 198,
      "our_match_coverage_pct": 19.18,
      "baseline_match_coverage_pct": 19.18,
      "senzing_true_coverage_pct": 82.45,
      "predicted_pairs_labeled": 36,
      "ground_truth_pairs_labeled": 59,
      "match_level_distribution": {
        "1": 125,
        "2": 422
      },
      "top_match_keys": [
        [
          "NAME",
          334
        ],
        [
          "NAME+DOB",
          20
        ],
        [
          "NAME+NATIONALITY",
          20
        ],
        [
          "NAME+DOB+NATIONALITY",
          16
        ],
        [
          "NAME+ADDRESS-RECORD_TYPE",
          12
        ],
        [
          "NAME+OTHER_ID",
          9
        ],
        [
          "NAME+DOB+NATIONALITY-TAX_ID",
          7
        ],
        [
          "NAME+TAX_ID",
          7
        ],
        [
          "NAME+EMAIL+NATIONALITY-RECORD_TYPE",
          6
        ],
        [
          "NAME+ADDRESS",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 151,
        "2": 75,
        "3": 59,
        "4": 46,
        "5": 24,
        "6": 11,
        "7": 2,
        "8": 3,
        "9": 4
      },
      "entity_pairings_distribution": {
        "0": 151,
        "1": 75,
        "3": 59,
        "6": 46,
        "10": 24,
        "15": 11,
        "21": 2,
        "28": 3,
        "36": 4
      },
      "record_pairing_degree_distribution": {
        "0": 151,
        "1": 150,
        "2": 177,
        "3": 184,
        "4": 120,
        "5": 66,
        "6": 14,
        "7": 24,
        "8": 36
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135820__sample_28_full_stress_mix_500/input_source.json",
      "management_summary_path": "20260302_135820__sample_28_full_stress_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135820__sample_28_full_stress_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135820__sample_28_full_stress_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1626
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384400
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4489
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 29861
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1009
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5766
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 274170
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 950
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2992
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 26204
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 16524
        },
        {
          "relative_path": "20260302_135820__sample_28_full_stress_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 547,
            "actual": 547,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 375,
            "actual": 375,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 97.22,
            "actual": 97.22,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 19.18,
            "actual": 19.18,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 2.78,
            "actual": 2.78,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 40.68,
            "actual": 40.68,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135820__sample_28_full_stress_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135753__sample_27_high_ipg_collision_500",
      "run_timestamp": "20260302_135753",
      "run_datetime": "2026-03-02T13:57:53",
      "run_label": "sample_27_high_ipg_collision_500",
      "source_input_name": "sample_27_high_ipg_collision_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:58:19",
      "records_input": 500,
      "records_exported": 632,
      "our_resolved_entities": 112,
      "resolved_entities": 285,
      "matched_records": 291,
      "matched_pairs": 346,
      "pair_precision_pct": 78.54,
      "pair_recall_pct": 68.28,
      "true_positive": 183,
      "false_positive": 50,
      "false_negative": 85,
      "discovery_available": true,
      "extra_true_matches_found": 84,
      "extra_false_matches_found": 128,
      "extra_match_precision_pct": 39.62,
      "extra_match_recall_pct": 57.93,
      "extra_gain_vs_known_pct": 34.57,
      "known_pairs_ipg": 243,
      "discoverable_true_pairs": 145,
      "predicted_pairs_beyond_known": 212,
      "net_extra_matches": -44,
      "overall_false_positive_pct": 21.46,
      "overall_false_positive_discovery_pct": 36.99,
      "overall_match_correctness_pct": 63.01,
      "our_true_positive": 243,
      "our_true_pairs_total": 388,
      "our_false_positive": 25,
      "our_false_negative": 145,
      "our_match_coverage_pct": 62.63,
      "baseline_match_coverage_pct": 62.63,
      "senzing_true_coverage_pct": 56.19,
      "predicted_pairs_labeled": 233,
      "ground_truth_pairs_labeled": 268,
      "match_level_distribution": {
        "1": 214,
        "2": 132
      },
      "top_match_keys": [
        [
          "NAME",
          40
        ],
        [
          "NAME+ADDRESS+NATIONALITY-RECORD_TYPE",
          28
        ],
        [
          "NAME+DOB",
          16
        ],
        [
          "NAME+ADDRESS-RECORD_TYPE",
          10
        ],
        [
          "NAME+NATIONALITY",
          10
        ],
        [
          "NAME+TAX_ID",
          10
        ],
        [
          "NAME+DOB+ADDRESS",
          9
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+TAX_ID",
          9
        ],
        [
          "NAME+EMAIL+NATIONALITY-RECORD_TYPE",
          9
        ]
      ],
      "entity_size_distribution": {
        "1": 112,
        "2": 66,
        "3": 62,
        "4": 27,
        "5": 14,
        "6": 4
      },
      "entity_pairings_distribution": {
        "0": 112,
        "1": 66,
        "3": 62,
        "6": 27,
        "10": 14,
        "15": 4
      },
      "record_pairing_degree_distribution": {
        "0": 112,
        "1": 132,
        "2": 186,
        "3": 108,
        "4": 70,
        "5": 24
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135753__sample_27_high_ipg_collision_500/input_source.json",
      "management_summary_path": "20260302_135753__sample_27_high_ipg_collision_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135753__sample_27_high_ipg_collision_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1639
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393420
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5872
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 25023
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1022
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7222
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 323768
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 962
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4551
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 21503
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 15944
        },
        {
          "relative_path": "20260302_135753__sample_27_high_ipg_collision_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 346,
            "actual": 346,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 285,
            "actual": 285,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 78.54,
            "actual": 78.54,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 62.63,
            "actual": 62.63,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 21.46,
            "actual": 21.46,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 31.72,
            "actual": 31.72,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135753__sample_27_high_ipg_collision_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135728__sample_26_person_chaos_low_ipg_500",
      "run_timestamp": "20260302_135728",
      "run_datetime": "2026-03-02T13:57:28",
      "run_label": "sample_26_person_chaos_low_ipg_500",
      "source_input_name": "sample_26_person_chaos_low_ipg_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": false,
      "generated_at": "2026-03-02T12:57:53",
      "records_input": 500,
      "records_exported": 709,
      "our_resolved_entities": 0,
      "resolved_entities": 381,
      "matched_records": 207,
      "matched_pairs": 328,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": 0,
      "false_positive": 0,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 137,
      "extra_false_matches_found": 191,
      "extra_match_precision_pct": 41.77,
      "extra_match_recall_pct": 69.54,
      "extra_gain_vs_known_pct": 0.0,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": 197,
      "predicted_pairs_beyond_known": 328,
      "net_extra_matches": -54,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": 58.23,
      "overall_match_correctness_pct": 41.77,
      "our_true_positive": 0,
      "our_true_pairs_total": 197,
      "our_false_positive": 0,
      "our_false_negative": 197,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": 0.0,
      "senzing_true_coverage_pct": 69.54,
      "predicted_pairs_labeled": 0,
      "ground_truth_pairs_labeled": 0,
      "match_level_distribution": {
        "1": 119,
        "2": 209
      },
      "top_match_keys": [
        [
          "NAME",
          189
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          15
        ],
        [
          "NAME+DOB+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+NATIONALITY",
          6
        ],
        [
          "NAME+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          5
        ],
        [
          "NAME+DOB (Ambiguous)",
          4
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          4
        ],
        [
          "NAME+DOB+EMAIL+OTHER_ID",
          4
        ]
      ],
      "entity_size_distribution": {
        "1": 243,
        "2": 53,
        "3": 33,
        "4": 25,
        "5": 16,
        "6": 3,
        "7": 2,
        "8": 5,
        "9": 1
      },
      "entity_pairings_distribution": {
        "0": 243,
        "1": 53,
        "3": 33,
        "6": 25,
        "10": 16,
        "15": 3,
        "21": 2,
        "28": 5,
        "36": 1
      },
      "record_pairing_degree_distribution": {
        "0": 243,
        "1": 106,
        "2": 99,
        "3": 100,
        "4": 80,
        "5": 18,
        "6": 14,
        "7": 40,
        "8": 9
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/input_source.json",
      "management_summary_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1516
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 389907
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4325
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23336
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 787
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5280
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 313933
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 970
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2766
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 17157
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 15364
        },
        {
          "relative_path": "20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 328,
            "actual": 328,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 381,
            "actual": 381,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135728__sample_26_person_chaos_low_ipg_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135702__sample_25_org_sparse_mix_500",
      "run_timestamp": "20260302_135702",
      "run_datetime": "2026-03-02T13:57:02",
      "run_label": "sample_25_org_sparse_mix_500",
      "source_input_name": "sample_25_org_sparse_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:57:27",
      "records_input": 500,
      "records_exported": 698,
      "our_resolved_entities": 61,
      "resolved_entities": 359,
      "matched_records": 240,
      "matched_pairs": 339,
      "pair_precision_pct": 89.53,
      "pair_recall_pct": 77.78,
      "true_positive": 77,
      "false_positive": 9,
      "false_negative": 22,
      "discovery_available": true,
      "extra_true_matches_found": 147,
      "extra_false_matches_found": 98,
      "extra_match_precision_pct": 60.0,
      "extra_match_recall_pct": 78.61,
      "extra_gain_vs_known_pct": 179.27,
      "known_pairs_ipg": 82,
      "discoverable_true_pairs": 187,
      "predicted_pairs_beyond_known": 245,
      "net_extra_matches": 49,
      "overall_false_positive_pct": 10.47,
      "overall_false_positive_discovery_pct": 28.91,
      "overall_match_correctness_pct": 71.09,
      "our_true_positive": 82,
      "our_true_pairs_total": 269,
      "our_false_positive": 17,
      "our_false_negative": 187,
      "our_match_coverage_pct": 30.48,
      "baseline_match_coverage_pct": 30.48,
      "senzing_true_coverage_pct": 89.59,
      "predicted_pairs_labeled": 86,
      "ground_truth_pairs_labeled": 99,
      "match_level_distribution": {
        "1": 141,
        "2": 198
      },
      "top_match_keys": [
        [
          "NAME",
          150
        ],
        [
          "NAME+DOB",
          25
        ],
        [
          "NAME+NATIONALITY",
          21
        ],
        [
          "NAME+REGISTRATION_DATE",
          11
        ],
        [
          "NAME+DOB+NATIONALITY",
          9
        ],
        [
          "NAME+TAX_ID",
          7
        ],
        [
          "NAME+OTHER_ID",
          6
        ],
        [
          "NAME+TAX_ID+REGISTRATION_DATE",
          6
        ],
        [
          "NAME+WEBSITE",
          6
        ],
        [
          "NAME+OTHER_ID+REGISTRATION_DATE",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 197,
        "2": 62,
        "3": 53,
        "4": 31,
        "5": 8,
        "6": 4,
        "7": 2,
        "8": 2
      },
      "entity_pairings_distribution": {
        "0": 197,
        "1": 62,
        "3": 53,
        "6": 31,
        "10": 8,
        "15": 4,
        "21": 2,
        "28": 2
      },
      "record_pairing_degree_distribution": {
        "0": 197,
        "1": 124,
        "2": 159,
        "3": 124,
        "4": 40,
        "5": 24,
        "6": 14,
        "7": 16
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135702__sample_25_org_sparse_mix_500/input_source.json",
      "management_summary_path": "20260302_135702__sample_25_org_sparse_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135702__sample_25_org_sparse_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1631
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 387119
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4486
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 22695
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1014
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5745
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 280480
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2983
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 17172
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 14784
        },
        {
          "relative_path": "20260302_135702__sample_25_org_sparse_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 339,
            "actual": 339,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 359,
            "actual": 359,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 89.53,
            "actual": 89.53,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 30.48,
            "actual": 30.48,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 10.47,
            "actual": 10.47,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 22.22,
            "actual": 22.22,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135702__sample_25_org_sparse_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135636__sample_24_id_disruption_500",
      "run_timestamp": "20260302_135636",
      "run_datetime": "2026-03-02T13:56:36",
      "run_label": "sample_24_id_disruption_500",
      "source_input_name": "sample_24_id_disruption_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:57:01",
      "records_input": 500,
      "records_exported": 695,
      "our_resolved_entities": 60,
      "resolved_entities": 333,
      "matched_records": 263,
      "matched_pairs": 362,
      "pair_precision_pct": 78.75,
      "pair_recall_pct": 54.31,
      "true_positive": 63,
      "false_positive": 17,
      "false_negative": 53,
      "discovery_available": true,
      "extra_true_matches_found": 131,
      "extra_false_matches_found": 179,
      "extra_match_precision_pct": 42.26,
      "extra_match_recall_pct": 64.53,
      "extra_gain_vs_known_pct": 139.36,
      "known_pairs_ipg": 94,
      "discoverable_true_pairs": 203,
      "predicted_pairs_beyond_known": 310,
      "net_extra_matches": -48,
      "overall_false_positive_pct": 21.25,
      "overall_false_positive_discovery_pct": 49.45,
      "overall_match_correctness_pct": 50.55,
      "our_true_positive": 94,
      "our_true_pairs_total": 297,
      "our_false_positive": 22,
      "our_false_negative": 203,
      "our_match_coverage_pct": 31.65,
      "baseline_match_coverage_pct": 31.65,
      "senzing_true_coverage_pct": 61.62,
      "predicted_pairs_labeled": 80,
      "ground_truth_pairs_labeled": 116,
      "match_level_distribution": {
        "1": 167,
        "2": 192,
        "3": 3
      },
      "top_match_keys": [
        [
          "NAME",
          79
        ],
        [
          "NAME+DOB+NATIONALITY",
          18
        ],
        [
          "NAME+DOB",
          12
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY-TAX_ID",
          12
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          11
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          10
        ],
        [
          "NAME+DOB-TAX_ID",
          10
        ],
        [
          "NAME+DOB+NATIONALITY (Ambiguous)",
          8
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          8
        ],
        [
          "NAME+ADDRESS+NATIONALITY-RECORD_TYPE",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 164,
        "2": 69,
        "3": 44,
        "4": 36,
        "5": 12,
        "6": 3,
        "7": 1,
        "8": 4
      },
      "entity_pairings_distribution": {
        "0": 164,
        "1": 69,
        "3": 44,
        "6": 36,
        "10": 12,
        "15": 3,
        "21": 1,
        "28": 4
      },
      "record_pairing_degree_distribution": {
        "0": 164,
        "1": 138,
        "2": 132,
        "3": 144,
        "4": 60,
        "5": 18,
        "6": 7,
        "7": 32
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135636__sample_24_id_disruption_500/input_source.json",
      "management_summary_path": "20260302_135636__sample_24_id_disruption_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135636__sample_24_id_disruption_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135636__sample_24_id_disruption_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1633
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 390559
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5811
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 26526
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1004
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7131
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 313790
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4465
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 21934
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 14204
        },
        {
          "relative_path": "20260302_135636__sample_24_id_disruption_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7625
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 362,
            "actual": 362,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 333,
            "actual": 333,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 78.75,
            "actual": 78.75,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 31.65,
            "actual": 31.65,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 21.25,
            "actual": 21.25,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 45.69,
            "actual": 45.69,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135636__sample_24_id_disruption_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_135613__sample_23_compound_noise_500",
      "run_timestamp": "20260302_135613",
      "run_datetime": "2026-03-02T13:56:13",
      "run_label": "sample_23_compound_noise_500",
      "source_input_name": "sample_23_compound_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:56:36",
      "records_input": 500,
      "records_exported": 1056,
      "our_resolved_entities": 52,
      "resolved_entities": 358,
      "matched_records": 322,
      "matched_pairs": 698,
      "pair_precision_pct": 59.65,
      "pair_recall_pct": 52.31,
      "true_positive": 34,
      "false_positive": 23,
      "false_negative": 31,
      "discovery_available": true,
      "extra_true_matches_found": 149,
      "extra_false_matches_found": 513,
      "extra_match_precision_pct": 22.51,
      "extra_match_recall_pct": 69.3,
      "extra_gain_vs_known_pct": 317.02,
      "known_pairs_ipg": 47,
      "discoverable_true_pairs": 215,
      "predicted_pairs_beyond_known": 662,
      "net_extra_matches": -364,
      "overall_false_positive_pct": 40.35,
      "overall_false_positive_discovery_pct": 73.5,
      "overall_match_correctness_pct": 26.5,
      "our_true_positive": 47,
      "our_true_pairs_total": 262,
      "our_false_positive": 18,
      "our_false_negative": 215,
      "our_match_coverage_pct": 17.94,
      "baseline_match_coverage_pct": 17.94,
      "senzing_true_coverage_pct": 70.61,
      "predicted_pairs_labeled": 57,
      "ground_truth_pairs_labeled": 65,
      "match_level_distribution": {
        "1": 142,
        "2": 556
      },
      "top_match_keys": [
        [
          "NAME",
          482
        ],
        [
          "NAME+DOB+NATIONALITY",
          23
        ],
        [
          "NAME+NATIONALITY",
          23
        ],
        [
          "NAME+DOB",
          15
        ],
        [
          "NAME+DOB+ADDRESS",
          9
        ],
        [
          "NAME+WEBSITE-RECORD_TYPE",
          9
        ],
        [
          "NAME+ADDRESS (Ambiguous)",
          8
        ],
        [
          "NAME+TAX_ID",
          8
        ],
        [
          "NAME+DOB+OTHER_ID",
          6
        ],
        [
          "NAME+OTHER_ID+REGISTRATION_DATE",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 134,
        "2": 64,
        "3": 66,
        "4": 34,
        "5": 16,
        "6": 12,
        "7": 9,
        "8": 7,
        "9": 4,
        "10": 6,
        "11": 1,
        "12": 1,
        "17": 2,
        "18": 2
      },
      "entity_pairings_distribution": {
        "0": 134,
        "1": 64,
        "3": 66,
        "6": 34,
        "10": 16,
        "15": 12,
        "21": 9,
        "28": 7,
        "36": 4,
        "45": 6,
        "55": 1,
        "66": 1,
        "136": 2,
        "153": 2
      },
      "record_pairing_degree_distribution": {
        "0": 134,
        "1": 128,
        "2": 198,
        "3": 136,
        "4": 80,
        "5": 72,
        "6": 63,
        "7": 56,
        "8": 36,
        "9": 60,
        "10": 11,
        "11": 12,
        "16": 34,
        "17": 36
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_135613__sample_23_compound_noise_500/input_source.json",
      "management_summary_path": "20260302_135613__sample_23_compound_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_135613__sample_23_compound_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_135613__sample_23_compound_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1628
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384149
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4112
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 33816
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1011
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5381
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 273708
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2579
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 32223
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 13624
        },
        {
          "relative_path": "20260302_135613__sample_23_compound_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7629
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 698,
            "actual": 698,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 358,
            "actual": 358,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 59.65,
            "actual": 59.65,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 17.94,
            "actual": 17.94,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 40.35,
            "actual": 40.35,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 47.69,
            "actual": 47.69,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_135613__sample_23_compound_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134653__sample_22_full_stress_mix_500",
      "run_timestamp": "20260302_134653",
      "run_datetime": "2026-03-02T13:46:53",
      "run_label": "sample_22_full_stress_mix_500",
      "source_input_name": "sample_22_full_stress_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:47:25",
      "records_input": 500,
      "records_exported": 1001,
      "our_resolved_entities": 41,
      "resolved_entities": 370,
      "matched_records": 300,
      "matched_pairs": 631,
      "pair_precision_pct": 77.78,
      "pair_recall_pct": 73.39,
      "true_positive": 91,
      "false_positive": 26,
      "false_negative": 33,
      "discovery_available": true,
      "extra_true_matches_found": 103,
      "extra_false_matches_found": 426,
      "extra_match_precision_pct": 19.47,
      "extra_match_recall_pct": 84.43,
      "extra_gain_vs_known_pct": 83.06,
      "known_pairs_ipg": 124,
      "discoverable_true_pairs": 122,
      "predicted_pairs_beyond_known": 529,
      "net_extra_matches": -323,
      "overall_false_positive_pct": 22.22,
      "overall_false_positive_discovery_pct": 67.51,
      "overall_match_correctness_pct": 32.49,
      "our_true_positive": 124,
      "our_true_pairs_total": 246,
      "our_false_positive": 0,
      "our_false_negative": 122,
      "our_match_coverage_pct": 50.41,
      "baseline_match_coverage_pct": 50.41,
      "senzing_true_coverage_pct": 83.33,
      "predicted_pairs_labeled": 117,
      "ground_truth_pairs_labeled": 124,
      "match_level_distribution": {
        "1": 130,
        "2": 501
      },
      "top_match_keys": [
        [
          "NAME",
          423
        ],
        [
          "NAME+DOB+NATIONALITY",
          24
        ],
        [
          "NAME+NATIONALITY",
          21
        ],
        [
          "NAME+DOB",
          19
        ],
        [
          "NAME+TAX_ID",
          8
        ],
        [
          "NAME+ADDRESS+TAX_ID",
          6
        ],
        [
          "NAME+ADDRESS+TAX_ID+OTHER_ID",
          6
        ],
        [
          "NAME+ADDRESS-RECORD_TYPE",
          5
        ],
        [
          "NAME+EMAIL+NATIONALITY",
          5
        ],
        [
          "NAME+NATIONALITY+LEI_NUMBER-RECORD_TYPE",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 161,
        "2": 55,
        "3": 42,
        "4": 41,
        "5": 29,
        "6": 17,
        "7": 15,
        "8": 6,
        "9": 2,
        "10": 1,
        "12": 1
      },
      "entity_pairings_distribution": {
        "0": 161,
        "1": 55,
        "3": 42,
        "6": 41,
        "10": 29,
        "15": 17,
        "21": 15,
        "28": 6,
        "36": 2,
        "45": 1,
        "66": 1
      },
      "record_pairing_degree_distribution": {
        "0": 161,
        "1": 110,
        "2": 126,
        "3": 164,
        "4": 145,
        "5": 102,
        "6": 105,
        "7": 48,
        "8": 18,
        "9": 10,
        "11": 12
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134653__sample_22_full_stress_mix_500/input_source.json",
      "management_summary_path": "20260302_134653__sample_22_full_stress_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134653__sample_22_full_stress_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134653__sample_22_full_stress_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1666
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 383637
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4462
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 32109
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1061
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5844
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 274280
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 950
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 3224
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 29449
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 13044
        },
        {
          "relative_path": "20260302_134653__sample_22_full_stress_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7630
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 631,
            "actual": 631,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 370,
            "actual": 370,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 77.78,
            "actual": 77.78,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 50.41,
            "actual": 50.41,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 22.22,
            "actual": 22.22,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 26.61,
            "actual": 26.61,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134653__sample_22_full_stress_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134620__sample_21_high_ipg_collision_500",
      "run_timestamp": "20260302_134620",
      "run_datetime": "2026-03-02T13:46:20",
      "run_label": "sample_21_high_ipg_collision_500",
      "source_input_name": "sample_21_high_ipg_collision_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:46:52",
      "records_input": 500,
      "records_exported": 653,
      "our_resolved_entities": 107,
      "resolved_entities": 298,
      "matched_records": 289,
      "matched_pairs": 355,
      "pair_precision_pct": 81.1,
      "pair_recall_pct": 75.64,
      "true_positive": 236,
      "false_positive": 55,
      "false_negative": 76,
      "discovery_available": true,
      "extra_true_matches_found": 36,
      "extra_false_matches_found": 137,
      "extra_match_precision_pct": 20.81,
      "extra_match_recall_pct": 73.47,
      "extra_gain_vs_known_pct": 11.54,
      "known_pairs_ipg": 312,
      "discoverable_true_pairs": 49,
      "predicted_pairs_beyond_known": 173,
      "net_extra_matches": -101,
      "overall_false_positive_pct": 18.9,
      "overall_false_positive_discovery_pct": 38.59,
      "overall_match_correctness_pct": 61.41,
      "our_true_positive": 312,
      "our_true_pairs_total": 361,
      "our_false_positive": 0,
      "our_false_negative": 49,
      "our_match_coverage_pct": 86.43,
      "baseline_match_coverage_pct": 86.43,
      "senzing_true_coverage_pct": 60.39,
      "predicted_pairs_labeled": 291,
      "ground_truth_pairs_labeled": 312,
      "match_level_distribution": {
        "1": 202,
        "2": 147,
        "3": 6
      },
      "top_match_keys": [
        [
          "NAME",
          52
        ],
        [
          "NAME+DOB+NATIONALITY",
          23
        ],
        [
          "NAME+DOB",
          18
        ],
        [
          "NAME+NATIONALITY",
          18
        ],
        [
          "NAME+EMAIL+NATIONALITY-RECORD_TYPE",
          17
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          15
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+OTHER_ID",
          9
        ],
        [
          "NAME+ADDRESS-RECORD_TYPE",
          7
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 115,
        "2": 79,
        "3": 60,
        "4": 25,
        "5": 15,
        "6": 3,
        "7": 1
      },
      "entity_pairings_distribution": {
        "0": 115,
        "1": 79,
        "3": 60,
        "6": 25,
        "10": 15,
        "15": 3,
        "21": 1
      },
      "record_pairing_degree_distribution": {
        "0": 115,
        "1": 158,
        "2": 180,
        "3": 100,
        "4": 75,
        "5": 18,
        "6": 7
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134620__sample_21_high_ipg_collision_500/input_source.json",
      "management_summary_path": "20260302_134620__sample_21_high_ipg_collision_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134620__sample_21_high_ipg_collision_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1671
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393067
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5919
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 25686
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1066
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7357
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 322164
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 962
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4828
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 21948
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 12464
        },
        {
          "relative_path": "20260302_134620__sample_21_high_ipg_collision_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 355,
            "actual": 355,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 298,
            "actual": 298,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 81.1,
            "actual": 81.1,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 86.43,
            "actual": 86.43,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 18.9,
            "actual": 18.9,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 24.36,
            "actual": 24.36,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134620__sample_21_high_ipg_collision_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134554__sample_20_person_chaos_low_ipg_500",
      "run_timestamp": "20260302_134554",
      "run_datetime": "2026-03-02T13:45:54",
      "run_label": "sample_20_person_chaos_low_ipg_500",
      "source_input_name": "sample_20_person_chaos_low_ipg_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:46:20",
      "records_input": 500,
      "records_exported": 693,
      "our_resolved_entities": 37,
      "resolved_entities": 366,
      "matched_records": 230,
      "matched_pairs": 327,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 92.45,
      "true_positive": 98,
      "false_positive": 0,
      "false_negative": 8,
      "discovery_available": true,
      "extra_true_matches_found": 86,
      "extra_false_matches_found": 147,
      "extra_match_precision_pct": 36.91,
      "extra_match_recall_pct": 62.77,
      "extra_gain_vs_known_pct": 81.13,
      "known_pairs_ipg": 106,
      "discoverable_true_pairs": 137,
      "predicted_pairs_beyond_known": 233,
      "net_extra_matches": -61,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 44.95,
      "overall_match_correctness_pct": 55.05,
      "our_true_positive": 106,
      "our_true_pairs_total": 243,
      "our_false_positive": 0,
      "our_false_negative": 137,
      "our_match_coverage_pct": 43.62,
      "baseline_match_coverage_pct": 43.62,
      "senzing_true_coverage_pct": 74.07,
      "predicted_pairs_labeled": 98,
      "ground_truth_pairs_labeled": 106,
      "match_level_distribution": {
        "1": 134,
        "2": 189,
        "3": 4
      },
      "top_match_keys": [
        [
          "NAME",
          141
        ],
        [
          "NAME+DOB+NATIONALITY",
          25
        ],
        [
          "NAME+NATIONALITY",
          14
        ],
        [
          "NAME+DOB",
          13
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          7
        ],
        [
          "NAME+ADDRESS+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+EMAIL+OTHER_ID+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 220,
        "2": 58,
        "3": 46,
        "4": 22,
        "5": 10,
        "7": 4,
        "8": 4,
        "9": 1,
        "12": 1
      },
      "entity_pairings_distribution": {
        "0": 220,
        "1": 58,
        "3": 46,
        "6": 22,
        "10": 10,
        "21": 4,
        "28": 4,
        "36": 1,
        "66": 1
      },
      "record_pairing_degree_distribution": {
        "0": 220,
        "1": 116,
        "2": 138,
        "3": 88,
        "4": 50,
        "6": 28,
        "7": 32,
        "8": 9,
        "11": 12
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/input_source.json",
      "management_summary_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1629
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 388891
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3813
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23071
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 996
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5096
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 306048
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 970
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2487
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 17238
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 11884
        },
        {
          "relative_path": "20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 327,
            "actual": 327,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 366,
            "actual": 366,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 43.62,
            "actual": 43.62,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 7.55,
            "actual": 7.55,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134554__sample_20_person_chaos_low_ipg_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134530__sample_19_org_sparse_mix_500",
      "run_timestamp": "20260302_134530",
      "run_datetime": "2026-03-02T13:45:30",
      "run_label": "sample_19_org_sparse_mix_500",
      "source_input_name": "sample_19_org_sparse_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:45:54",
      "records_input": 500,
      "records_exported": 671,
      "our_resolved_entities": 54,
      "resolved_entities": 352,
      "matched_records": 240,
      "matched_pairs": 319,
      "pair_precision_pct": 89.47,
      "pair_recall_pct": 71.26,
      "true_positive": 119,
      "false_positive": 14,
      "false_negative": 48,
      "discovery_available": true,
      "extra_true_matches_found": 102,
      "extra_false_matches_found": 116,
      "extra_match_precision_pct": 46.79,
      "extra_match_recall_pct": 86.44,
      "extra_gain_vs_known_pct": 61.08,
      "known_pairs_ipg": 167,
      "discoverable_true_pairs": 118,
      "predicted_pairs_beyond_known": 218,
      "net_extra_matches": -14,
      "overall_false_positive_pct": 10.53,
      "overall_false_positive_discovery_pct": 36.36,
      "overall_match_correctness_pct": 63.64,
      "our_true_positive": 167,
      "our_true_pairs_total": 285,
      "our_false_positive": 0,
      "our_false_negative": 118,
      "our_match_coverage_pct": 58.6,
      "baseline_match_coverage_pct": 58.6,
      "senzing_true_coverage_pct": 71.23,
      "predicted_pairs_labeled": 133,
      "ground_truth_pairs_labeled": 167,
      "match_level_distribution": {
        "1": 148,
        "2": 171
      },
      "top_match_keys": [
        [
          "NAME",
          99
        ],
        [
          "NAME+NATIONALITY",
          33
        ],
        [
          "NAME+DOB",
          24
        ],
        [
          "NAME+WEBSITE+NATIONALITY",
          12
        ],
        [
          "NAME+OTHER_ID",
          9
        ],
        [
          "NAME+REGISTRATION_DATE",
          9
        ],
        [
          "NAME+OTHER_ID+REGISTRATION_DATE",
          8
        ],
        [
          "NAME+ADDRESS+WEBSITE+LEI_NUMBER-RECORD_TYPE",
          7
        ],
        [
          "NAME+TAX_ID",
          7
        ],
        [
          "NAME+TAX_ID+NATIONALITY",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 191,
        "2": 67,
        "3": 49,
        "4": 35,
        "5": 6,
        "7": 3,
        "8": 1
      },
      "entity_pairings_distribution": {
        "0": 191,
        "1": 67,
        "3": 49,
        "6": 35,
        "10": 6,
        "21": 3,
        "28": 1
      },
      "record_pairing_degree_distribution": {
        "0": 191,
        "1": 134,
        "2": 147,
        "3": 140,
        "4": 30,
        "6": 21,
        "7": 8
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134530__sample_19_org_sparse_mix_500/input_source.json",
      "management_summary_path": "20260302_134530__sample_19_org_sparse_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134530__sample_19_org_sparse_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1666
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 387198
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4332
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 22611
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1061
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5705
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 279362
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 3070
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 17072
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 11304
        },
        {
          "relative_path": "20260302_134530__sample_19_org_sparse_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 319,
            "actual": 319,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 352,
            "actual": 352,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 89.47,
            "actual": 89.47,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 58.6,
            "actual": 58.6,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 10.53,
            "actual": 10.53,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 28.74,
            "actual": 28.74,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134530__sample_19_org_sparse_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134503__sample_18_id_disruption_500",
      "run_timestamp": "20260302_134503",
      "run_datetime": "2026-03-02T13:45:03",
      "run_label": "sample_18_id_disruption_500",
      "source_input_name": "sample_18_id_disruption_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:45:29",
      "records_input": 500,
      "records_exported": 645,
      "our_resolved_entities": 57,
      "resolved_entities": 336,
      "matched_records": 251,
      "matched_pairs": 309,
      "pair_precision_pct": 92.14,
      "pair_recall_pct": 81.13,
      "true_positive": 129,
      "false_positive": 11,
      "false_negative": 30,
      "discovery_available": true,
      "extra_true_matches_found": 65,
      "extra_false_matches_found": 123,
      "extra_match_precision_pct": 34.57,
      "extra_match_recall_pct": 58.04,
      "extra_gain_vs_known_pct": 40.88,
      "known_pairs_ipg": 159,
      "discoverable_true_pairs": 112,
      "predicted_pairs_beyond_known": 188,
      "net_extra_matches": -58,
      "overall_false_positive_pct": 7.86,
      "overall_false_positive_discovery_pct": 39.81,
      "overall_match_correctness_pct": 60.19,
      "our_true_positive": 159,
      "our_true_pairs_total": 271,
      "our_false_positive": 0,
      "our_false_negative": 112,
      "our_match_coverage_pct": 58.67,
      "baseline_match_coverage_pct": 58.67,
      "senzing_true_coverage_pct": 68.63,
      "predicted_pairs_labeled": 140,
      "ground_truth_pairs_labeled": 159,
      "match_level_distribution": {
        "1": 164,
        "2": 145
      },
      "top_match_keys": [
        [
          "NAME",
          24
        ],
        [
          "NAME+ADDRESS+NATIONALITY-RECORD_TYPE",
          14
        ],
        [
          "NAME+DOB+NATIONALITY",
          12
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+NATIONALITY",
          8
        ],
        [
          "NAME+ADDRESS+EMAIL+NATIONALITY-RECORD_TYPE",
          7
        ],
        [
          "NAME+ADDRESS+TAX_ID+WEBSITE+NATIONALITY+LEI_NUMBER-RECORD_TYPE",
          7
        ],
        [
          "NAME+DOB+NATIONALITY-TAX_ID",
          7
        ],
        [
          "NAME+DOB",
          6
        ],
        [
          "NAME+DOB+NATIONALITY (Ambiguous)",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 177,
        "2": 70,
        "3": 49,
        "4": 27,
        "5": 8,
        "6": 2,
        "7": 3
      },
      "entity_pairings_distribution": {
        "0": 177,
        "1": 70,
        "3": 49,
        "6": 27,
        "10": 8,
        "15": 2,
        "21": 3
      },
      "record_pairing_degree_distribution": {
        "0": 177,
        "1": 140,
        "2": 147,
        "3": 108,
        "4": 40,
        "5": 12,
        "6": 21
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134503__sample_18_id_disruption_500/input_source.json",
      "management_summary_path": "20260302_134503__sample_18_id_disruption_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134503__sample_18_id_disruption_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134503__sample_18_id_disruption_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1666
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393712
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 6575
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 26162
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1061
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 8036
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 320828
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 5572
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 20917
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 10724
        },
        {
          "relative_path": "20260302_134503__sample_18_id_disruption_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7625
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 309,
            "actual": 309,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 336,
            "actual": 336,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 92.14,
            "actual": 92.14,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 58.67,
            "actual": 58.67,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 7.86,
            "actual": 7.86,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 18.87,
            "actual": 18.87,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134503__sample_18_id_disruption_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134437__sample_17_compound_noise_500",
      "run_timestamp": "20260302_134437",
      "run_datetime": "2026-03-02T13:44:37",
      "run_label": "sample_17_compound_noise_500",
      "source_input_name": "sample_17_compound_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:45:03",
      "records_input": 500,
      "records_exported": 1100,
      "our_resolved_entities": 47,
      "resolved_entities": 395,
      "matched_records": 301,
      "matched_pairs": 704,
      "pair_precision_pct": 60.73,
      "pair_recall_pct": 88.55,
      "true_positive": 116,
      "false_positive": 75,
      "false_negative": 15,
      "discovery_available": true,
      "extra_true_matches_found": 106,
      "extra_false_matches_found": 439,
      "extra_match_precision_pct": 19.45,
      "extra_match_recall_pct": 89.83,
      "extra_gain_vs_known_pct": 80.92,
      "known_pairs_ipg": 131,
      "discoverable_true_pairs": 118,
      "predicted_pairs_beyond_known": 545,
      "net_extra_matches": -333,
      "overall_false_positive_pct": 39.27,
      "overall_false_positive_discovery_pct": 62.36,
      "overall_match_correctness_pct": 37.64,
      "our_true_positive": 131,
      "our_true_pairs_total": 249,
      "our_false_positive": 0,
      "our_false_negative": 118,
      "our_match_coverage_pct": 52.61,
      "baseline_match_coverage_pct": 52.61,
      "senzing_true_coverage_pct": 106.43,
      "predicted_pairs_labeled": 191,
      "ground_truth_pairs_labeled": 131,
      "match_level_distribution": {
        "1": 104,
        "2": 600
      },
      "top_match_keys": [
        [
          "NAME",
          527
        ],
        [
          "NAME+DOB",
          34
        ],
        [
          "NAME+NATIONALITY",
          31
        ],
        [
          "NAME+DOB+NATIONALITY",
          17
        ],
        [
          "NAME+DOB+TAX_ID",
          11
        ],
        [
          "NAME+EMAIL",
          8
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+OTHER_ID",
          6
        ],
        [
          "NAME+ADDRESS",
          5
        ],
        [
          "NAME+EMAIL+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 170,
        "2": 66,
        "3": 53,
        "4": 29,
        "5": 35,
        "6": 15,
        "7": 7,
        "8": 4,
        "9": 6,
        "10": 2,
        "11": 2,
        "12": 2,
        "14": 3,
        "15": 1
      },
      "entity_pairings_distribution": {
        "0": 170,
        "1": 66,
        "3": 53,
        "6": 29,
        "10": 35,
        "15": 15,
        "21": 7,
        "28": 4,
        "36": 6,
        "45": 2,
        "55": 2,
        "66": 2,
        "91": 3,
        "105": 1
      },
      "record_pairing_degree_distribution": {
        "0": 170,
        "1": 132,
        "2": 159,
        "3": 116,
        "4": 175,
        "5": 90,
        "6": 49,
        "7": 32,
        "8": 54,
        "9": 20,
        "10": 22,
        "11": 24,
        "13": 42,
        "14": 15
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134437__sample_17_compound_noise_500/input_source.json",
      "management_summary_path": "20260302_134437__sample_17_compound_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134437__sample_17_compound_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134437__sample_17_compound_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1729
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 382902
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3193
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 33377
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1148
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 4616
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 269065
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 1780
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 30787
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 10144
        },
        {
          "relative_path": "20260302_134437__sample_17_compound_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7635
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 704,
            "actual": 704,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 395,
            "actual": 395,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 60.73,
            "actual": 60.73,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 52.61,
            "actual": 52.61,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 39.27,
            "actual": 39.27,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 11.45,
            "actual": 11.45,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134437__sample_17_compound_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134413__sample_16_full_stress_mix_500",
      "run_timestamp": "20260302_134413",
      "run_datetime": "2026-03-02T13:44:13",
      "run_label": "sample_16_full_stress_mix_500",
      "source_input_name": "sample_16_full_stress_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:44:37",
      "records_input": 500,
      "records_exported": 828,
      "our_resolved_entities": 37,
      "resolved_entities": 371,
      "matched_records": 283,
      "matched_pairs": 456,
      "pair_precision_pct": 83.7,
      "pair_recall_pct": 81.05,
      "true_positive": 77,
      "false_positive": 15,
      "false_negative": 18,
      "discovery_available": true,
      "extra_true_matches_found": 104,
      "extra_false_matches_found": 276,
      "extra_match_precision_pct": 27.37,
      "extra_match_recall_pct": 73.76,
      "extra_gain_vs_known_pct": 109.47,
      "known_pairs_ipg": 95,
      "discoverable_true_pairs": 141,
      "predicted_pairs_beyond_known": 380,
      "net_extra_matches": -172,
      "overall_false_positive_pct": 16.3,
      "overall_false_positive_discovery_pct": 60.53,
      "overall_match_correctness_pct": 39.47,
      "our_true_positive": 95,
      "our_true_pairs_total": 236,
      "our_false_positive": 0,
      "our_false_negative": 141,
      "our_match_coverage_pct": 40.25,
      "baseline_match_coverage_pct": 40.25,
      "senzing_true_coverage_pct": 76.27,
      "predicted_pairs_labeled": 92,
      "ground_truth_pairs_labeled": 95,
      "match_level_distribution": {
        "1": 128,
        "2": 328
      },
      "top_match_keys": [
        [
          "NAME",
          257
        ],
        [
          "NAME+NATIONALITY",
          30
        ],
        [
          "NAME+DOB",
          18
        ],
        [
          "NAME+REGISTRATION_DATE",
          10
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+NATIONALITY",
          7
        ],
        [
          "NAME+TAX_ID",
          7
        ],
        [
          "NAME+ADDRESS+WEBSITE+OTHER_ID",
          6
        ],
        [
          "NAME+OTHER_ID",
          6
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 170,
        "2": 66,
        "3": 71,
        "4": 38,
        "5": 10,
        "6": 9,
        "7": 3,
        "9": 4
      },
      "entity_pairings_distribution": {
        "0": 170,
        "1": 66,
        "3": 71,
        "6": 38,
        "10": 10,
        "15": 9,
        "21": 3,
        "36": 4
      },
      "record_pairing_degree_distribution": {
        "0": 170,
        "1": 132,
        "2": 213,
        "3": 152,
        "4": 50,
        "5": 54,
        "6": 21,
        "8": 36
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134413__sample_16_full_stress_mix_500/input_source.json",
      "management_summary_path": "20260302_134413__sample_16_full_stress_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134413__sample_16_full_stress_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134413__sample_16_full_stress_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1694
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384259
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4095
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 26937
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1101
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5500
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 276559
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 950
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2790
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 22359
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 9564
        },
        {
          "relative_path": "20260302_134413__sample_16_full_stress_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 456,
            "actual": 456,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 371,
            "actual": 371,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 83.7,
            "actual": 83.7,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 40.25,
            "actual": 40.25,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 16.3,
            "actual": 16.3,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 18.95,
            "actual": 18.95,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134413__sample_16_full_stress_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134349__sample_15_high_ipg_collision_500",
      "run_timestamp": "20260302_134349",
      "run_datetime": "2026-03-02T13:43:49",
      "run_label": "sample_15_high_ipg_collision_500",
      "source_input_name": "sample_15_high_ipg_collision_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:44:13",
      "records_input": 500,
      "records_exported": 630,
      "our_resolved_entities": 133,
      "resolved_entities": 253,
      "matched_records": 315,
      "matched_pairs": 377,
      "pair_precision_pct": 68.45,
      "pair_recall_pct": 75.0,
      "true_positive": 282,
      "false_positive": 130,
      "false_negative": 94,
      "discovery_available": true,
      "extra_true_matches_found": 24,
      "extra_false_matches_found": 144,
      "extra_match_precision_pct": 14.29,
      "extra_match_recall_pct": 68.57,
      "extra_gain_vs_known_pct": 6.38,
      "known_pairs_ipg": 376,
      "discoverable_true_pairs": 35,
      "predicted_pairs_beyond_known": 168,
      "net_extra_matches": -120,
      "overall_false_positive_pct": 31.55,
      "overall_false_positive_discovery_pct": 38.2,
      "overall_match_correctness_pct": 61.8,
      "our_true_positive": 376,
      "our_true_pairs_total": 411,
      "our_false_positive": 0,
      "our_false_negative": 35,
      "our_match_coverage_pct": 91.48,
      "baseline_match_coverage_pct": 91.48,
      "senzing_true_coverage_pct": 56.69,
      "predicted_pairs_labeled": 412,
      "ground_truth_pairs_labeled": 376,
      "match_level_distribution": {
        "1": 247,
        "2": 130
      },
      "top_match_keys": [
        [
          "NAME",
          68
        ],
        [
          "NAME+DOB+NATIONALITY",
          23
        ],
        [
          "NAME+DOB",
          20
        ],
        [
          "NAME+NATIONALITY",
          15
        ],
        [
          "NAME+DOB+TAX_ID",
          12
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          10
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          8
        ],
        [
          "NAME+DOB+ADDRESS+EMAIL+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 70,
        "2": 74,
        "3": 62,
        "4": 27,
        "5": 13,
        "6": 4,
        "8": 1,
        "10": 1,
        "11": 1
      },
      "entity_pairings_distribution": {
        "0": 70,
        "1": 74,
        "3": 62,
        "6": 27,
        "10": 13,
        "15": 4,
        "28": 1,
        "45": 1,
        "55": 1
      },
      "record_pairing_degree_distribution": {
        "0": 70,
        "1": 148,
        "2": 186,
        "3": 108,
        "4": 65,
        "5": 24,
        "7": 8,
        "9": 10,
        "10": 11
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134349__sample_15_high_ipg_collision_500/input_source.json",
      "management_summary_path": "20260302_134349__sample_15_high_ipg_collision_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134349__sample_15_high_ipg_collision_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1734
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 394260
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5931
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 25139
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1139
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7466
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 332219
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 962
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4876
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 22799
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 8984
        },
        {
          "relative_path": "20260302_134349__sample_15_high_ipg_collision_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 377,
            "actual": 377,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 253,
            "actual": 253,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 68.45,
            "actual": 68.45,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 91.48,
            "actual": 91.48,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 31.55,
            "actual": 31.55,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 25.0,
            "actual": 25.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134349__sample_15_high_ipg_collision_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134325__sample_14_person_chaos_low_ipg_500",
      "run_timestamp": "20260302_134325",
      "run_datetime": "2026-03-02T13:43:25",
      "run_label": "sample_14_person_chaos_low_ipg_500",
      "source_input_name": "sample_14_person_chaos_low_ipg_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:43:49",
      "records_input": 500,
      "records_exported": 629,
      "our_resolved_entities": 32,
      "resolved_entities": 372,
      "matched_records": 202,
      "matched_pairs": 256,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 97.67,
      "true_positive": 84,
      "false_positive": 0,
      "false_negative": 2,
      "discovery_available": true,
      "extra_true_matches_found": 83,
      "extra_false_matches_found": 101,
      "extra_match_precision_pct": 45.11,
      "extra_match_recall_pct": 68.03,
      "extra_gain_vs_known_pct": 96.51,
      "known_pairs_ipg": 86,
      "discoverable_true_pairs": 122,
      "predicted_pairs_beyond_known": 184,
      "net_extra_matches": -18,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 39.45,
      "overall_match_correctness_pct": 60.55,
      "our_true_positive": 86,
      "our_true_pairs_total": 208,
      "our_false_positive": 0,
      "our_false_negative": 122,
      "our_match_coverage_pct": 41.35,
      "baseline_match_coverage_pct": 41.35,
      "senzing_true_coverage_pct": 74.52,
      "predicted_pairs_labeled": 84,
      "ground_truth_pairs_labeled": 86,
      "match_level_distribution": {
        "1": 127,
        "2": 129
      },
      "top_match_keys": [
        [
          "NAME",
          92
        ],
        [
          "NAME+DOB+NATIONALITY",
          15
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          11
        ],
        [
          "NAME+NATIONALITY",
          11
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          10
        ],
        [
          "NAME+DOB",
          7
        ],
        [
          "NAME+DOB+TAX_ID",
          7
        ],
        [
          "NAME+DOB-TAX_ID",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 235,
        "2": 66,
        "3": 36,
        "4": 25,
        "5": 7,
        "6": 2,
        "7": 1
      },
      "entity_pairings_distribution": {
        "0": 235,
        "1": 66,
        "3": 36,
        "6": 25,
        "10": 7,
        "15": 2,
        "21": 1
      },
      "record_pairing_degree_distribution": {
        "0": 235,
        "1": 132,
        "2": 108,
        "3": 100,
        "4": 35,
        "5": 12,
        "6": 7
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/input_source.json",
      "management_summary_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1626
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 389050
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3766
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 21020
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 993
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5014
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 310023
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 970
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2403
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 14234
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 8404
        },
        {
          "relative_path": "20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 256,
            "actual": 256,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 372,
            "actual": 372,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 41.35,
            "actual": 41.35,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 2.33,
            "actual": 2.33,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134325__sample_14_person_chaos_low_ipg_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134301__sample_13_org_sparse_mix_500",
      "run_timestamp": "20260302_134301",
      "run_datetime": "2026-03-02T13:43:01",
      "run_label": "sample_13_org_sparse_mix_500",
      "source_input_name": "sample_13_org_sparse_mix_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:43:25",
      "records_input": 500,
      "records_exported": 722,
      "our_resolved_entities": 52,
      "resolved_entities": 364,
      "matched_records": 245,
      "matched_pairs": 358,
      "pair_precision_pct": 95.28,
      "pair_recall_pct": 93.8,
      "true_positive": 121,
      "false_positive": 6,
      "false_negative": 8,
      "discovery_available": true,
      "extra_true_matches_found": 82,
      "extra_false_matches_found": 143,
      "extra_match_precision_pct": 36.44,
      "extra_match_recall_pct": 66.13,
      "extra_gain_vs_known_pct": 63.57,
      "known_pairs_ipg": 129,
      "discoverable_true_pairs": 124,
      "predicted_pairs_beyond_known": 225,
      "net_extra_matches": -61,
      "overall_false_positive_pct": 4.72,
      "overall_false_positive_discovery_pct": 39.94,
      "overall_match_correctness_pct": 60.06,
      "our_true_positive": 129,
      "our_true_pairs_total": 253,
      "our_false_positive": 0,
      "our_false_negative": 124,
      "our_match_coverage_pct": 50.99,
      "baseline_match_coverage_pct": 50.99,
      "senzing_true_coverage_pct": 84.98,
      "predicted_pairs_labeled": 127,
      "ground_truth_pairs_labeled": 129,
      "match_level_distribution": {
        "1": 136,
        "2": 222
      },
      "top_match_keys": [
        [
          "NAME",
          189
        ],
        [
          "NAME+NATIONALITY",
          19
        ],
        [
          "NAME+REGISTRATION_DATE",
          13
        ],
        [
          "NAME+DOB",
          8
        ],
        [
          "NAME+OTHER_ID",
          8
        ],
        [
          "NAME+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+OTHER_ID+NATIONALITY+REGISTRATION_DATE",
          6
        ],
        [
          "NAME+TAX_ID",
          6
        ],
        [
          "NAME+TAX_ID+NATIONALITY",
          6
        ],
        [
          "NAME+ADDRESS+WEBSITE+REGISTRATION_DATE",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 192,
        "2": 67,
        "3": 64,
        "4": 25,
        "5": 4,
        "6": 4,
        "7": 6,
        "8": 1,
        "10": 1
      },
      "entity_pairings_distribution": {
        "0": 192,
        "1": 67,
        "3": 64,
        "6": 25,
        "10": 4,
        "15": 4,
        "21": 6,
        "28": 1,
        "45": 1
      },
      "record_pairing_degree_distribution": {
        "0": 192,
        "1": 134,
        "2": 192,
        "3": 100,
        "4": 20,
        "5": 24,
        "6": 42,
        "7": 8,
        "9": 10
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134301__sample_13_org_sparse_mix_500/input_source.json",
      "management_summary_path": "20260302_134301__sample_13_org_sparse_mix_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134301__sample_13_org_sparse_mix_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1661
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 387670
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4177
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23436
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1054
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5537
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 279209
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2898
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 18004
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 7824
        },
        {
          "relative_path": "20260302_134301__sample_13_org_sparse_mix_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 358,
            "actual": 358,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 364,
            "actual": 364,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 95.28,
            "actual": 95.28,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 50.99,
            "actual": 50.99,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 4.72,
            "actual": 4.72,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 6.2,
            "actual": 6.2,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134301__sample_13_org_sparse_mix_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_134234__sample_12_id_disruption_500",
      "run_timestamp": "20260302_134234",
      "run_datetime": "2026-03-02T13:42:34",
      "run_label": "sample_12_id_disruption_500",
      "source_input_name": "sample_12_id_disruption_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:43:01",
      "records_input": 500,
      "records_exported": 700,
      "our_resolved_entities": 50,
      "resolved_entities": 356,
      "matched_records": 256,
      "matched_pairs": 344,
      "pair_precision_pct": 88.03,
      "pair_recall_pct": 70.55,
      "true_positive": 103,
      "false_positive": 14,
      "false_negative": 43,
      "discovery_available": true,
      "extra_true_matches_found": 70,
      "extra_false_matches_found": 183,
      "extra_match_precision_pct": 27.67,
      "extra_match_recall_pct": 66.04,
      "extra_gain_vs_known_pct": 47.95,
      "known_pairs_ipg": 146,
      "discoverable_true_pairs": 106,
      "predicted_pairs_beyond_known": 253,
      "net_extra_matches": -113,
      "overall_false_positive_pct": 11.97,
      "overall_false_positive_discovery_pct": 53.2,
      "overall_match_correctness_pct": 46.8,
      "our_true_positive": 146,
      "our_true_pairs_total": 252,
      "our_false_positive": 0,
      "our_false_negative": 106,
      "our_match_coverage_pct": 57.94,
      "baseline_match_coverage_pct": 57.94,
      "senzing_true_coverage_pct": 63.89,
      "predicted_pairs_labeled": 117,
      "ground_truth_pairs_labeled": 146,
      "match_level_distribution": {
        "1": 144,
        "2": 198,
        "3": 2
      },
      "top_match_keys": [
        [
          "NAME",
          96
        ],
        [
          "NAME+REGISTRATION_DATE",
          11
        ],
        [
          "NAME+NATIONALITY",
          10
        ],
        [
          "NAME+ADDRESS+WEBSITE+NATIONALITY-RECORD_TYPE",
          9
        ],
        [
          "NAME+EMAIL+NATIONALITY-RECORD_TYPE",
          9
        ],
        [
          "NAME+ADDRESS-RECORD_TYPE",
          8
        ],
        [
          "NAME+DOB+EMAIL",
          7
        ],
        [
          "NAME+DOB+NATIONALITY",
          7
        ],
        [
          "NAME+ADDRESS+EMAIL+NATIONALITY-RECORD_TYPE",
          6
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 184,
        "2": 81,
        "3": 42,
        "4": 33,
        "5": 9,
        "6": 4,
        "7": 2,
        "13": 1
      },
      "entity_pairings_distribution": {
        "0": 184,
        "1": 81,
        "3": 42,
        "6": 33,
        "10": 9,
        "15": 4,
        "21": 2,
        "78": 1
      },
      "record_pairing_degree_distribution": {
        "0": 184,
        "1": 162,
        "2": 126,
        "3": 132,
        "4": 45,
        "5": 24,
        "6": 14,
        "12": 13
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_134234__sample_12_id_disruption_500/input_source.json",
      "management_summary_path": "20260302_134234__sample_12_id_disruption_500/management_summary.md",
      "ground_truth_summary_path": "20260302_134234__sample_12_id_disruption_500/ground_truth_match_quality.md",
      "technical_path": "20260302_134234__sample_12_id_disruption_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1666
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393690
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 6428
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 26548
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1061
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7877
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 318857
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 5396
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 21185
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 7244
        },
        {
          "relative_path": "20260302_134234__sample_12_id_disruption_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 344,
            "actual": 344,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 356,
            "actual": 356,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 88.03,
            "actual": 88.03,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 57.94,
            "actual": 57.94,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 11.97,
            "actual": 11.97,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 29.45,
            "actual": 29.45,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_134234__sample_12_id_disruption_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133902__sample_11_compound_noise_500",
      "run_timestamp": "20260302_133902",
      "run_datetime": "2026-03-02T13:39:02",
      "run_label": "sample_11_compound_noise_500",
      "source_input_name": "sample_11_compound_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:39:33",
      "records_input": 500,
      "records_exported": 935,
      "our_resolved_entities": 43,
      "resolved_entities": 371,
      "matched_records": 285,
      "matched_pairs": 564,
      "pair_precision_pct": 75.0,
      "pair_recall_pct": 74.29,
      "true_positive": 78,
      "false_positive": 26,
      "false_negative": 27,
      "discovery_available": true,
      "extra_true_matches_found": 83,
      "extra_false_matches_found": 379,
      "extra_match_precision_pct": 17.97,
      "extra_match_recall_pct": 66.94,
      "extra_gain_vs_known_pct": 79.05,
      "known_pairs_ipg": 105,
      "discoverable_true_pairs": 124,
      "predicted_pairs_beyond_known": 462,
      "net_extra_matches": -296,
      "overall_false_positive_pct": 25.0,
      "overall_false_positive_discovery_pct": 67.2,
      "overall_match_correctness_pct": 32.8,
      "our_true_positive": 105,
      "our_true_pairs_total": 229,
      "our_false_positive": 0,
      "our_false_negative": 124,
      "our_match_coverage_pct": 45.85,
      "baseline_match_coverage_pct": 45.85,
      "senzing_true_coverage_pct": 80.79,
      "predicted_pairs_labeled": 104,
      "ground_truth_pairs_labeled": 105,
      "match_level_distribution": {
        "1": 129,
        "2": 435
      },
      "top_match_keys": [
        [
          "NAME",
          354
        ],
        [
          "NAME+NATIONALITY",
          42
        ],
        [
          "NAME+OTHER_ID",
          15
        ],
        [
          "NAME+DOB+NATIONALITY",
          11
        ],
        [
          "NAME+DOB",
          10
        ],
        [
          "NAME+REGISTRATION_DATE",
          10
        ],
        [
          "NAME+TAX_ID",
          8
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+TAX_ID",
          5
        ],
        [
          "NAME+TAX_ID+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 176,
        "2": 55,
        "3": 52,
        "4": 41,
        "5": 15,
        "6": 7,
        "7": 6,
        "8": 8,
        "9": 8,
        "10": 1,
        "12": 2
      },
      "entity_pairings_distribution": {
        "0": 176,
        "1": 55,
        "3": 52,
        "6": 41,
        "10": 15,
        "15": 7,
        "21": 6,
        "28": 8,
        "36": 8,
        "45": 1,
        "66": 2
      },
      "record_pairing_degree_distribution": {
        "0": 176,
        "1": 110,
        "2": 156,
        "3": 164,
        "4": 75,
        "5": 42,
        "6": 42,
        "7": 64,
        "8": 72,
        "9": 10,
        "11": 24
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133902__sample_11_compound_noise_500/input_source.json",
      "management_summary_path": "20260302_133902__sample_11_compound_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133902__sample_11_compound_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133902__sample_11_compound_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1694
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384324
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3980
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 29772
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1087
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5377
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 273087
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 946
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2689
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 26368
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 6664
        },
        {
          "relative_path": "20260302_133902__sample_11_compound_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 564,
            "actual": 564,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 371,
            "actual": 371,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 75.0,
            "actual": 75.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 45.85,
            "actual": 45.85,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 25.0,
            "actual": 25.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 25.71,
            "actual": 25.71,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133902__sample_11_compound_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133835__sample_10_high_ipg_coverage_500",
      "run_timestamp": "20260302_133835",
      "run_datetime": "2026-03-02T13:38:35",
      "run_label": "sample_10_high_ipg_coverage_500",
      "source_input_name": "sample_10_high_ipg_coverage_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:39:02",
      "records_input": 500,
      "records_exported": 593,
      "our_resolved_entities": 115,
      "resolved_entities": 267,
      "matched_records": 283,
      "matched_pairs": 326,
      "pair_precision_pct": 86.52,
      "pair_recall_pct": 97.87,
      "true_positive": 321,
      "false_positive": 50,
      "false_negative": 7,
      "discovery_available": true,
      "extra_true_matches_found": 38,
      "extra_false_matches_found": 59,
      "extra_match_precision_pct": 39.18,
      "extra_match_recall_pct": 61.29,
      "extra_gain_vs_known_pct": 11.59,
      "known_pairs_ipg": 328,
      "discoverable_true_pairs": 62,
      "predicted_pairs_beyond_known": 97,
      "net_extra_matches": -21,
      "overall_false_positive_pct": 13.48,
      "overall_false_positive_discovery_pct": 18.1,
      "overall_match_correctness_pct": 81.9,
      "our_true_positive": 328,
      "our_true_pairs_total": 390,
      "our_false_positive": 0,
      "our_false_negative": 62,
      "our_match_coverage_pct": 84.1,
      "baseline_match_coverage_pct": 84.1,
      "senzing_true_coverage_pct": 68.46,
      "predicted_pairs_labeled": 371,
      "ground_truth_pairs_labeled": 328,
      "match_level_distribution": {
        "1": 233,
        "2": 93
      },
      "top_match_keys": [
        [
          "NAME",
          59
        ],
        [
          "NAME+DOB",
          22
        ],
        [
          "NAME+DOB+NATIONALITY",
          18
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          17
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          13
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          8
        ],
        [
          "NAME+DOB+TAX_ID",
          8
        ],
        [
          "NAME+NATIONALITY",
          8
        ],
        [
          "NAME+DOB+ADDRESS+EMAIL+OTHER_ID+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 105,
        "2": 55,
        "3": 66,
        "4": 35,
        "5": 3,
        "6": 1,
        "8": 1,
        "11": 1
      },
      "entity_pairings_distribution": {
        "0": 105,
        "1": 55,
        "3": 66,
        "6": 35,
        "10": 3,
        "15": 1,
        "28": 1,
        "55": 1
      },
      "record_pairing_degree_distribution": {
        "0": 105,
        "1": 110,
        "2": 198,
        "3": 140,
        "4": 15,
        "5": 6,
        "7": 8,
        "10": 11
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [
        "snapshot primary attempt failed; fallback 'fallback_single_thread_force_sdk' succeeded."
      ],
      "input_source_path": "20260302_133835__sample_10_high_ipg_coverage_500/input_source.json",
      "management_summary_path": "20260302_133835__sample_10_high_ipg_coverage_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133835__sample_10_high_ipg_coverage_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1700
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393592
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5517
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23022
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1107
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 6982
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 325797
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 958
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4383
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 19756
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 6084
        },
        {
          "relative_path": "20260302_133835__sample_10_high_ipg_coverage_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 8302
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 326,
            "actual": 326,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 267,
            "actual": 267,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 86.52,
            "actual": 86.52,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 84.1,
            "actual": 84.1,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 13.48,
            "actual": 13.48,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 2.13,
            "actual": 2.13,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133835__sample_10_high_ipg_coverage_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133809__sample_09_person_heavy_low_ipg_500",
      "run_timestamp": "20260302_133809",
      "run_datetime": "2026-03-02T13:38:09",
      "run_label": "sample_09_person_heavy_low_ipg_500",
      "source_input_name": "sample_09_person_heavy_low_ipg_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:38:35",
      "records_input": 500,
      "records_exported": 636,
      "our_resolved_entities": 25,
      "resolved_entities": 367,
      "matched_records": 187,
      "matched_pairs": 269,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 100.0,
      "true_positive": 82,
      "false_positive": 0,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 96,
      "extra_false_matches_found": 119,
      "extra_match_precision_pct": 44.65,
      "extra_match_recall_pct": 75.0,
      "extra_gain_vs_known_pct": 117.07,
      "known_pairs_ipg": 82,
      "discoverable_true_pairs": 128,
      "predicted_pairs_beyond_known": 215,
      "net_extra_matches": -23,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 44.24,
      "overall_match_correctness_pct": 55.76,
      "our_true_positive": 82,
      "our_true_pairs_total": 210,
      "our_false_positive": 0,
      "our_false_negative": 128,
      "our_match_coverage_pct": 39.05,
      "baseline_match_coverage_pct": 39.05,
      "senzing_true_coverage_pct": 71.43,
      "predicted_pairs_labeled": 82,
      "ground_truth_pairs_labeled": 82,
      "match_level_distribution": {
        "1": 133,
        "2": 136
      },
      "top_match_keys": [
        [
          "NAME",
          116
        ],
        [
          "NAME+DOB+NATIONALITY",
          18
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+TAX_ID",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+ADDRESS+TAX_ID+NATIONALITY",
          5
        ],
        [
          "NAME+DOB",
          5
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          5
        ],
        [
          "NAME+TAX_ID",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 251,
        "2": 45,
        "3": 31,
        "4": 24,
        "5": 7,
        "6": 1,
        "7": 3,
        "8": 4,
        "12": 1
      },
      "entity_pairings_distribution": {
        "0": 251,
        "1": 45,
        "3": 31,
        "6": 24,
        "10": 7,
        "15": 1,
        "21": 3,
        "28": 4,
        "66": 1
      },
      "record_pairing_degree_distribution": {
        "0": 251,
        "1": 90,
        "2": 93,
        "3": 96,
        "4": 35,
        "5": 6,
        "6": 21,
        "7": 32,
        "11": 12
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/input_source.json",
      "management_summary_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1626
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 389507
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3992
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 21116
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 977
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5236
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 313580
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 970
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2664
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 14642
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 5504
        },
        {
          "relative_path": "20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 269,
            "actual": 269,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 367,
            "actual": 367,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 39.05,
            "actual": 39.05,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133809__sample_09_person_heavy_low_ipg_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133745__sample_08_organization_heavy_500",
      "run_timestamp": "20260302_133745",
      "run_datetime": "2026-03-02T13:37:45",
      "run_label": "sample_08_organization_heavy_500",
      "source_input_name": "sample_08_organization_heavy_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:38:09",
      "records_input": 500,
      "records_exported": 559,
      "our_resolved_entities": 58,
      "resolved_entities": 337,
      "matched_records": 195,
      "matched_pairs": 222,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 100.0,
      "true_positive": 155,
      "false_positive": 0,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 70,
      "extra_false_matches_found": 31,
      "extra_match_precision_pct": 69.31,
      "extra_match_recall_pct": 67.31,
      "extra_gain_vs_known_pct": 45.16,
      "known_pairs_ipg": 155,
      "discoverable_true_pairs": 104,
      "predicted_pairs_beyond_known": 101,
      "net_extra_matches": 39,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 13.96,
      "overall_match_correctness_pct": 86.04,
      "our_true_positive": 155,
      "our_true_pairs_total": 259,
      "our_false_positive": 0,
      "our_false_negative": 104,
      "our_match_coverage_pct": 59.85,
      "baseline_match_coverage_pct": 59.85,
      "senzing_true_coverage_pct": 73.75,
      "predicted_pairs_labeled": 155,
      "ground_truth_pairs_labeled": 155,
      "match_level_distribution": {
        "1": 163,
        "2": 55,
        "3": 4
      },
      "top_match_keys": [
        [
          "NAME",
          27
        ],
        [
          "NAME+NATIONALITY",
          17
        ],
        [
          "NAME+DOB",
          13
        ],
        [
          "NAME+DOB+NATIONALITY",
          8
        ],
        [
          "NAME+ADDRESS+TAX_ID+OTHER_ID+REGISTRATION_DATE",
          7
        ],
        [
          "NAME+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+REGISTRATION_DATE",
          6
        ],
        [
          "NAME+REGISTRATION_DATE",
          6
        ],
        [
          "NAME+ADDRESS+TAX_ID+NATIONALITY+REGISTRATION_DATE",
          5
        ],
        [
          "NAME+ADDRESS+TAX_ID+REGISTRATION_DATE",
          5
        ],
        [
          "NAME+TAX_ID+WEBSITE+NATIONALITY+REGISTRATION_DATE",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 219,
        "2": 48,
        "3": 45,
        "4": 22,
        "7": 3
      },
      "entity_pairings_distribution": {
        "0": 219,
        "1": 48,
        "3": 45,
        "6": 22,
        "21": 3
      },
      "record_pairing_degree_distribution": {
        "0": 219,
        "1": 96,
        "2": 135,
        "3": 88,
        "6": 21
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133745__sample_08_organization_heavy_500/input_source.json",
      "management_summary_path": "20260302_133745__sample_08_organization_heavy_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133745__sample_08_organization_heavy_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133745__sample_08_organization_heavy_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1602
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 396565
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5590
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 20852
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 941
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 6871
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 325873
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 962
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4456
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 14633
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 4924
        },
        {
          "relative_path": "20260302_133745__sample_08_organization_heavy_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 222,
            "actual": 222,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 337,
            "actual": 337,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 59.85,
            "actual": 59.85,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133745__sample_08_organization_heavy_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133718__sample_07_duplicate_pressure_500",
      "run_timestamp": "20260302_133718",
      "run_datetime": "2026-03-02T13:37:18",
      "run_label": "sample_07_duplicate_pressure_500",
      "source_input_name": "sample_07_duplicate_pressure_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:37:45",
      "records_input": 500,
      "records_exported": 641,
      "our_resolved_entities": 59,
      "resolved_entities": 315,
      "matched_records": 254,
      "matched_pairs": 326,
      "pair_precision_pct": 86.29,
      "pair_recall_pct": 78.65,
      "true_positive": 151,
      "false_positive": 24,
      "false_negative": 41,
      "discovery_available": true,
      "extra_true_matches_found": 67,
      "extra_false_matches_found": 164,
      "extra_match_precision_pct": 29.0,
      "extra_match_recall_pct": 69.07,
      "extra_gain_vs_known_pct": 34.9,
      "known_pairs_ipg": 192,
      "discoverable_true_pairs": 97,
      "predicted_pairs_beyond_known": 231,
      "net_extra_matches": -97,
      "overall_false_positive_pct": 13.71,
      "overall_false_positive_discovery_pct": 50.31,
      "overall_match_correctness_pct": 49.69,
      "our_true_positive": 192,
      "our_true_pairs_total": 289,
      "our_false_positive": 0,
      "our_false_negative": 97,
      "our_match_coverage_pct": 66.44,
      "baseline_match_coverage_pct": 66.44,
      "senzing_true_coverage_pct": 56.06,
      "predicted_pairs_labeled": 175,
      "ground_truth_pairs_labeled": 192,
      "match_level_distribution": {
        "1": 185,
        "2": 141
      },
      "top_match_keys": [
        [
          "NAME",
          84
        ],
        [
          "NAME+DOB+NATIONALITY",
          25
        ],
        [
          "NAME+NATIONALITY",
          11
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          10
        ],
        [
          "NAME+EMAIL+NATIONALITY-RECORD_TYPE",
          10
        ],
        [
          "NAME+DOB",
          9
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID",
          9
        ],
        [
          "NAME+ADDRESS+NATIONALITY-RECORD_TYPE",
          8
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          7
        ]
      ],
      "entity_size_distribution": {
        "1": 163,
        "2": 62,
        "3": 45,
        "4": 26,
        "5": 8,
        "6": 6,
        "7": 3,
        "8": 1,
        "10": 1
      },
      "entity_pairings_distribution": {
        "0": 163,
        "1": 62,
        "3": 45,
        "6": 26,
        "10": 8,
        "15": 6,
        "21": 3,
        "28": 1,
        "45": 1
      },
      "record_pairing_degree_distribution": {
        "0": 163,
        "1": 124,
        "2": 135,
        "3": 104,
        "4": 40,
        "5": 36,
        "6": 21,
        "7": 8,
        "9": 10
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133718__sample_07_duplicate_pressure_500/input_source.json",
      "management_summary_path": "20260302_133718__sample_07_duplicate_pressure_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133718__sample_07_duplicate_pressure_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1699
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 392643
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5310
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23971
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1106
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 6770
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 323924
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 962
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4152
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 19467
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 4344
        },
        {
          "relative_path": "20260302_133718__sample_07_duplicate_pressure_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 326,
            "actual": 326,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 315,
            "actual": 315,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 86.29,
            "actual": 86.29,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 66.44,
            "actual": 66.44,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 13.71,
            "actual": 13.71,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 21.35,
            "actual": 21.35,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133718__sample_07_duplicate_pressure_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133651__sample_06_address_noise_500",
      "run_timestamp": "20260302_133651",
      "run_datetime": "2026-03-02T13:36:51",
      "run_label": "sample_06_address_noise_500",
      "source_input_name": "sample_06_address_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:37:18",
      "records_input": 500,
      "records_exported": 633,
      "our_resolved_entities": 66,
      "resolved_entities": 344,
      "matched_records": 238,
      "matched_pairs": 289,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 97.53,
      "true_positive": 158,
      "false_positive": 0,
      "false_negative": 4,
      "discovery_available": true,
      "extra_true_matches_found": 73,
      "extra_false_matches_found": 77,
      "extra_match_precision_pct": 48.67,
      "extra_match_recall_pct": 66.36,
      "extra_gain_vs_known_pct": 45.06,
      "known_pairs_ipg": 162,
      "discoverable_true_pairs": 110,
      "predicted_pairs_beyond_known": 150,
      "net_extra_matches": -4,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 26.64,
      "overall_match_correctness_pct": 73.36,
      "our_true_positive": 162,
      "our_true_pairs_total": 272,
      "our_false_positive": 0,
      "our_false_negative": 110,
      "our_match_coverage_pct": 59.56,
      "baseline_match_coverage_pct": 59.56,
      "senzing_true_coverage_pct": 77.94,
      "predicted_pairs_labeled": 158,
      "ground_truth_pairs_labeled": 162,
      "match_level_distribution": {
        "1": 156,
        "2": 133
      },
      "top_match_keys": [
        [
          "NAME",
          88
        ],
        [
          "NAME+DOB",
          21
        ],
        [
          "NAME+NATIONALITY",
          18
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          13
        ],
        [
          "NAME+DOB+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+TAX_ID",
          8
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+OTHER_ID",
          6
        ],
        [
          "NAME+DOB+ADDRESS+EMAIL+NATIONALITY",
          5
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 188,
        "2": 72,
        "3": 50,
        "4": 26,
        "5": 5,
        "6": 1,
        "7": 1,
        "9": 1
      },
      "entity_pairings_distribution": {
        "0": 188,
        "1": 72,
        "3": 50,
        "6": 26,
        "10": 5,
        "15": 1,
        "21": 1,
        "36": 1
      },
      "record_pairing_degree_distribution": {
        "0": 188,
        "1": 144,
        "2": 150,
        "3": 104,
        "4": 25,
        "5": 6,
        "6": 7,
        "8": 9
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133651__sample_06_address_noise_500/input_source.json",
      "management_summary_path": "20260302_133651__sample_06_address_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133651__sample_06_address_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133651__sample_06_address_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1633
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 390915
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4639
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 21988
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1000
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5944
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 312730
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 3384
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 16319
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 3764
        },
        {
          "relative_path": "20260302_133651__sample_06_address_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 289,
            "actual": 289,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 344,
            "actual": 344,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 59.56,
            "actual": 59.56,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 2.47,
            "actual": 2.47,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133651__sample_06_address_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133628__sample_05_taxid_noise_500",
      "run_timestamp": "20260302_133628",
      "run_datetime": "2026-03-02T13:36:28",
      "run_label": "sample_05_taxid_noise_500",
      "source_input_name": "sample_05_taxid_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:36:51",
      "records_input": 500,
      "records_exported": 616,
      "our_resolved_entities": 63,
      "resolved_entities": 338,
      "matched_records": 227,
      "matched_pairs": 275,
      "pair_precision_pct": 100.0,
      "pair_recall_pct": 100.0,
      "true_positive": 174,
      "false_positive": 0,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 67,
      "extra_false_matches_found": 73,
      "extra_match_precision_pct": 47.86,
      "extra_match_recall_pct": 65.69,
      "extra_gain_vs_known_pct": 38.51,
      "known_pairs_ipg": 174,
      "discoverable_true_pairs": 102,
      "predicted_pairs_beyond_known": 140,
      "net_extra_matches": -6,
      "overall_false_positive_pct": 0.0,
      "overall_false_positive_discovery_pct": 26.55,
      "overall_match_correctness_pct": 73.45,
      "our_true_positive": 174,
      "our_true_pairs_total": 276,
      "our_false_positive": 0,
      "our_false_negative": 102,
      "our_match_coverage_pct": 63.04,
      "baseline_match_coverage_pct": 63.04,
      "senzing_true_coverage_pct": 73.19,
      "predicted_pairs_labeled": 174,
      "ground_truth_pairs_labeled": 174,
      "match_level_distribution": {
        "1": 159,
        "2": 116
      },
      "top_match_keys": [
        [
          "NAME",
          76
        ],
        [
          "NAME+DOB+NATIONALITY",
          11
        ],
        [
          "NAME+OTHER_ID+REGISTRATION_DATE-TAX_ID",
          9
        ],
        [
          "NAME+DOB",
          8
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          7
        ],
        [
          "NAME+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+TAX_ID",
          6
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB-TAX_ID",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 194,
        "2": 64,
        "3": 49,
        "4": 25,
        "5": 1,
        "7": 1,
        "8": 2,
        "9": 1,
        "10": 1
      },
      "entity_pairings_distribution": {
        "0": 194,
        "1": 64,
        "3": 49,
        "6": 25,
        "10": 1,
        "21": 1,
        "28": 2,
        "36": 1,
        "45": 1
      },
      "record_pairing_degree_distribution": {
        "0": 194,
        "1": 128,
        "2": 147,
        "3": 100,
        "4": 5,
        "6": 7,
        "7": 16,
        "8": 9,
        "9": 10
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133628__sample_05_taxid_noise_500/input_source.json",
      "management_summary_path": "20260302_133628__sample_05_taxid_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133628__sample_05_taxid_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133628__sample_05_taxid_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1604
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 392976
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5440
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 22202
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 943
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 6717
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 321243
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 934
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4287
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 16470
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 3184
        },
        {
          "relative_path": "20260302_133628__sample_05_taxid_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 275,
            "actual": 275,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 338,
            "actual": 338,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 63.04,
            "actual": 63.04,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133628__sample_05_taxid_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133605__sample_04_name_noise_500",
      "run_timestamp": "20260302_133605",
      "run_datetime": "2026-03-02T13:36:05",
      "run_label": "sample_04_name_noise_500",
      "source_input_name": "sample_04_name_noise_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:36:27",
      "records_input": 500,
      "records_exported": 719,
      "our_resolved_entities": 62,
      "resolved_entities": 337,
      "matched_records": 252,
      "matched_pairs": 382,
      "pair_precision_pct": 96.65,
      "pair_recall_pct": 97.19,
      "true_positive": 173,
      "false_positive": 6,
      "false_negative": 5,
      "discovery_available": true,
      "extra_true_matches_found": 73,
      "extra_false_matches_found": 173,
      "extra_match_precision_pct": 29.67,
      "extra_match_recall_pct": 74.49,
      "extra_gain_vs_known_pct": 41.01,
      "known_pairs_ipg": 178,
      "discoverable_true_pairs": 98,
      "predicted_pairs_beyond_known": 246,
      "net_extra_matches": -100,
      "overall_false_positive_pct": 3.35,
      "overall_false_positive_discovery_pct": 45.29,
      "overall_match_correctness_pct": 54.71,
      "our_true_positive": 178,
      "our_true_pairs_total": 276,
      "our_false_positive": 0,
      "our_false_negative": 98,
      "our_match_coverage_pct": 64.49,
      "baseline_match_coverage_pct": 64.49,
      "senzing_true_coverage_pct": 75.72,
      "predicted_pairs_labeled": 179,
      "ground_truth_pairs_labeled": 178,
      "match_level_distribution": {
        "1": 163,
        "2": 219
      },
      "top_match_keys": [
        [
          "NAME",
          191
        ],
        [
          "NAME+NATIONALITY",
          16
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          15
        ],
        [
          "NAME+DOB",
          14
        ],
        [
          "NAME+DOB+NATIONALITY",
          13
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          13
        ],
        [
          "NAME+DOB+TAX_ID",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          6
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+NATIONALITY",
          5
        ],
        [
          "NAME+NATIONALITY+REGISTRATION_DATE",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 180,
        "2": 54,
        "3": 47,
        "4": 34,
        "5": 6,
        "6": 6,
        "7": 4,
        "9": 2,
        "10": 2,
        "11": 2
      },
      "entity_pairings_distribution": {
        "0": 180,
        "1": 54,
        "3": 47,
        "6": 34,
        "10": 6,
        "15": 6,
        "21": 4,
        "36": 2,
        "45": 2,
        "55": 2
      },
      "record_pairing_degree_distribution": {
        "0": 180,
        "1": 108,
        "2": 141,
        "3": 136,
        "4": 30,
        "5": 36,
        "6": 28,
        "8": 18,
        "9": 20,
        "10": 22
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133605__sample_04_name_noise_500/input_source.json",
      "management_summary_path": "20260302_133605__sample_04_name_noise_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133605__sample_04_name_noise_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133605__sample_04_name_noise_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1663
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 390434
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 4542
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 24381
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1058
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 5917
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 315886
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 930
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 3294
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 19911
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 2604
        },
        {
          "relative_path": "20260302_133605__sample_04_name_noise_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7626
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 382,
            "actual": 382,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 337,
            "actual": 337,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 96.65,
            "actual": 96.65,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 64.49,
            "actual": 64.49,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 3.35,
            "actual": 3.35,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 2.81,
            "actual": 2.81,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133605__sample_04_name_noise_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133541__sample_03_sparse_fields_500",
      "run_timestamp": "20260302_133541",
      "run_datetime": "2026-03-02T13:35:41",
      "run_label": "sample_03_sparse_fields_500",
      "source_input_name": "sample_03_sparse_fields_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:36:05",
      "records_input": 500,
      "records_exported": 968,
      "our_resolved_entities": 53,
      "resolved_entities": 365,
      "matched_records": 309,
      "matched_pairs": 603,
      "pair_precision_pct": 95.17,
      "pair_recall_pct": 89.61,
      "true_positive": 138,
      "false_positive": 7,
      "false_negative": 16,
      "discovery_available": true,
      "extra_true_matches_found": 88,
      "extra_false_matches_found": 366,
      "extra_match_precision_pct": 19.38,
      "extra_match_recall_pct": 71.54,
      "extra_gain_vs_known_pct": 57.14,
      "known_pairs_ipg": 154,
      "discoverable_true_pairs": 123,
      "predicted_pairs_beyond_known": 454,
      "net_extra_matches": -278,
      "overall_false_positive_pct": 4.83,
      "overall_false_positive_discovery_pct": 60.7,
      "overall_match_correctness_pct": 39.3,
      "our_true_positive": 154,
      "our_true_pairs_total": 277,
      "our_false_positive": 0,
      "our_false_negative": 123,
      "our_match_coverage_pct": 55.6,
      "baseline_match_coverage_pct": 55.6,
      "senzing_true_coverage_pct": 85.56,
      "predicted_pairs_labeled": 145,
      "ground_truth_pairs_labeled": 154,
      "match_level_distribution": {
        "1": 135,
        "2": 468
      },
      "top_match_keys": [
        [
          "NAME",
          418
        ],
        [
          "NAME+NATIONALITY",
          40
        ],
        [
          "NAME+ADDRESS",
          12
        ],
        [
          "NAME+DOB+NATIONALITY",
          10
        ],
        [
          "NAME+OTHER_ID",
          10
        ],
        [
          "NAME+DOB",
          8
        ],
        [
          "NAME+TAX_ID",
          8
        ],
        [
          "NAME+TAX_ID+OTHER_ID",
          7
        ],
        [
          "NAME+DOB+TAX_ID",
          5
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          5
        ]
      ],
      "entity_size_distribution": {
        "1": 151,
        "2": 73,
        "3": 49,
        "4": 40,
        "5": 14,
        "6": 13,
        "7": 7,
        "8": 5,
        "9": 6,
        "10": 4,
        "11": 3
      },
      "entity_pairings_distribution": {
        "0": 151,
        "1": 73,
        "3": 49,
        "6": 40,
        "10": 14,
        "15": 13,
        "21": 7,
        "28": 5,
        "36": 6,
        "45": 4,
        "55": 3
      },
      "record_pairing_degree_distribution": {
        "0": 151,
        "1": 146,
        "2": 147,
        "3": 160,
        "4": 70,
        "5": 78,
        "6": 49,
        "7": 40,
        "8": 54,
        "9": 40,
        "10": 33
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133541__sample_03_sparse_fields_500/input_source.json",
      "management_summary_path": "20260302_133541__sample_03_sparse_fields_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133541__sample_03_sparse_fields_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133541__sample_03_sparse_fields_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1633
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 384992
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3595
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 30194
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1016
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 4890
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 279956
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 942
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 2250
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 27390
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 2024
        },
        {
          "relative_path": "20260302_133541__sample_03_sparse_fields_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 603,
            "actual": 603,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 365,
            "actual": 365,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 95.17,
            "actual": 95.17,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 55.6,
            "actual": 55.6,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 4.83,
            "actual": 4.83,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 10.39,
            "actual": 10.39,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133541__sample_03_sparse_fields_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133518__sample_02_balanced_baseline_500",
      "run_timestamp": "20260302_133518",
      "run_datetime": "2026-03-02T13:35:18",
      "run_label": "sample_02_balanced_baseline_500",
      "source_input_name": "sample_02_balanced_baseline_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:35:41",
      "records_input": 500,
      "records_exported": 588,
      "our_resolved_entities": 63,
      "resolved_entities": 328,
      "matched_records": 222,
      "matched_pairs": 260,
      "pair_precision_pct": 83.82,
      "pair_recall_pct": 100.0,
      "true_positive": 171,
      "false_positive": 33,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 69,
      "extra_false_matches_found": 63,
      "extra_match_precision_pct": 52.27,
      "extra_match_recall_pct": 65.09,
      "extra_gain_vs_known_pct": 40.35,
      "known_pairs_ipg": 171,
      "discoverable_true_pairs": 106,
      "predicted_pairs_beyond_known": 132,
      "net_extra_matches": 6,
      "overall_false_positive_pct": 16.18,
      "overall_false_positive_discovery_pct": 24.23,
      "overall_match_correctness_pct": 75.77,
      "our_true_positive": 171,
      "our_true_pairs_total": 277,
      "our_false_positive": 0,
      "our_false_negative": 106,
      "our_match_coverage_pct": 61.73,
      "baseline_match_coverage_pct": 61.73,
      "senzing_true_coverage_pct": 71.12,
      "predicted_pairs_labeled": 204,
      "ground_truth_pairs_labeled": 171,
      "match_level_distribution": {
        "1": 172,
        "2": 88
      },
      "top_match_keys": [
        [
          "NAME",
          61
        ],
        [
          "NAME+DOB+NATIONALITY",
          13
        ],
        [
          "NAME+DOB",
          12
        ],
        [
          "NAME+NATIONALITY",
          9
        ],
        [
          "NAME+DOB+ADDRESS",
          8
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+NATIONALITY",
          8
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+NATIONALITY",
          8
        ],
        [
          "NAME+DOB+ADDRESS+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          7
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 193,
        "2": 58,
        "3": 50,
        "4": 19,
        "5": 4,
        "6": 1,
        "7": 2,
        "13": 1
      },
      "entity_pairings_distribution": {
        "0": 193,
        "1": 58,
        "3": 50,
        "6": 19,
        "10": 4,
        "15": 1,
        "21": 2,
        "78": 1
      },
      "record_pairing_degree_distribution": {
        "0": 193,
        "1": 116,
        "2": 150,
        "3": 76,
        "4": 20,
        "5": 6,
        "6": 14,
        "12": 13
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133518__sample_02_balanced_baseline_500/input_source.json",
      "management_summary_path": "20260302_133518__sample_02_balanced_baseline_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133518__sample_02_balanced_baseline_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133518__sample_02_balanced_baseline_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1636
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 392470
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5121
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 21353
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1003
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 6445
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 317969
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 958
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 3914
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 15786
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 1444
        },
        {
          "relative_path": "20260302_133518__sample_02_balanced_baseline_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 260,
            "actual": 260,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 328,
            "actual": 328,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 83.82,
            "actual": 83.82,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 61.73,
            "actual": 61.73,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 16.18,
            "actual": 16.18,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 0.0,
            "actual": 0.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133518__sample_02_balanced_baseline_500/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260302_133451__sample_01_legacy_baseline_500",
      "run_timestamp": "20260302_133451",
      "run_datetime": "2026-03-02T13:34:51",
      "run_label": "sample_01_legacy_baseline_500",
      "source_input_name": "sample_01_legacy_baseline_500.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-02T12:35:18",
      "records_input": 500,
      "records_exported": 610,
      "our_resolved_entities": 115,
      "resolved_entities": 269,
      "matched_records": 286,
      "matched_pairs": 341,
      "pair_precision_pct": 89.86,
      "pair_recall_pct": 97.26,
      "true_positive": 319,
      "false_positive": 36,
      "false_negative": 9,
      "discovery_available": true,
      "extra_true_matches_found": 38,
      "extra_false_matches_found": 73,
      "extra_match_precision_pct": 34.23,
      "extra_match_recall_pct": 62.3,
      "extra_gain_vs_known_pct": 11.59,
      "known_pairs_ipg": 328,
      "discoverable_true_pairs": 61,
      "predicted_pairs_beyond_known": 111,
      "net_extra_matches": -35,
      "overall_false_positive_pct": 10.14,
      "overall_false_positive_discovery_pct": 21.41,
      "overall_match_correctness_pct": 78.59,
      "our_true_positive": 328,
      "our_true_pairs_total": 389,
      "our_false_positive": 0,
      "our_false_negative": 61,
      "our_match_coverage_pct": 84.32,
      "baseline_match_coverage_pct": 84.32,
      "senzing_true_coverage_pct": 68.89,
      "predicted_pairs_labeled": 355,
      "ground_truth_pairs_labeled": 328,
      "match_level_distribution": {
        "1": 231,
        "2": 107,
        "3": 3
      },
      "top_match_keys": [
        [
          "NAME",
          68
        ],
        [
          "NAME+DOB+NATIONALITY",
          23
        ],
        [
          "NAME+DOB",
          21
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          13
        ],
        [
          "NAME+NATIONALITY",
          13
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          9
        ],
        [
          "NAME+TAX_ID",
          8
        ],
        [
          "NAME+DOB+OTHER_ID",
          6
        ],
        [
          "NAME+DOB+TAX_ID",
          6
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+NATIONALITY",
          6
        ]
      ],
      "entity_size_distribution": {
        "1": 105,
        "2": 54,
        "3": 67,
        "4": 30,
        "5": 10,
        "6": 1,
        "9": 1,
        "11": 1
      },
      "entity_pairings_distribution": {
        "0": 105,
        "1": 54,
        "3": 67,
        "6": 30,
        "10": 10,
        "15": 1,
        "36": 1,
        "55": 1
      },
      "record_pairing_degree_distribution": {
        "0": 105,
        "1": 108,
        "2": 201,
        "3": 120,
        "4": 50,
        "5": 6,
        "8": 9,
        "10": 11
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260302_133451__sample_01_legacy_baseline_500/input_source.json",
      "management_summary_path": "20260302_133451__sample_01_legacy_baseline_500/management_summary.md",
      "ground_truth_summary_path": "20260302_133451__sample_01_legacy_baseline_500/ground_truth_match_quality.md",
      "technical_path": "20260302_133451__sample_01_legacy_baseline_500/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1729
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 393337
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 5723
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 23232
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1148
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 7250
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 323632
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 950
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 4626
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 20072
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 864
        },
        {
          "relative_path": "20260302_133451__sample_01_legacy_baseline_500/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7627
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 500,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": 341,
            "actual": 341,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 269,
            "actual": 269,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 89.86,
            "actual": 89.86,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 84.32,
            "actual": 84.32,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 10.14,
            "actual": 10.14,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 2.74,
            "actual": 2.74,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260302_133451__sample_01_legacy_baseline_500/technical output/input_normalized.jsonl"
      }
    }
  ],
  "summary": {
    "runs_total": 30,
    "quality_runs_total": 29,
    "successful_runs": 30,
    "failed_runs": 0,
    "incomplete_runs": 0,
    "latest_run_id": "20260302_135931__sample_30_id_disruption_500",
    "avg_pair_precision_pct": 86.77,
    "avg_pair_recall_pct": 81.88,
    "records_input_total": 14500,
    "matched_pairs_total": 11475
  }
};

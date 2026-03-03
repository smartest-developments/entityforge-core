window.MVP_DASHBOARD_DATA = {
  "generated_at": "2026-03-03T22:45:43",
  "output_root": "/Users/simones/Developer/mapper-ai-main/MVP/output",
  "runs": [
    {
      "run_id": "20260303_221424__one-million-partial-616k",
      "run_timestamp": "20260303_221424",
      "run_datetime": "2026-03-03T22:14:24",
      "run_label": "one-million-final-stream-debug",
      "source_input_name": "one_million_stress.jsonl",
      "run_status": "failed",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": false,
      "quality_available": true,
      "generated_at": "2026-03-03T21:13:50",
      "execution_seconds": 15537.188,
      "execution_minutes": 258.95,
      "execution_minutes_estimated": 258.95,
      "execution_minutes_is_estimate": false,
      "records_input": 616942,
      "records_input_loaded": 616942,
      "records_input_reported": 1000000,
      "records_exported": 2649792,
      "our_entities_formed": 196882,
      "their_entities_formed": 287306,
      "our_grouped_members": 341801,
      "their_grouped_members": 493256,
      "our_match_pct": 55.4,
      "their_match_pct": 79.95,
      "our_match_gain_loss_pct": -24.55,
      "their_match_gain_loss_pct": 24.55,
      "our_entity_gain_loss_pct": -14.66,
      "their_entity_gain_loss_pct": 14.66,
      "our_resolved_entities": 196882,
      "resolved_entities": 287306,
      "matched_records": 2360575,
      "matched_pairs": 2360565,
      "pair_precision_pct": 27.01,
      "pair_recall_pct": 43.68,
      "true_positive": 310843,
      "false_positive": 840070,
      "false_negative": 400740,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 711583,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": 72.99,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 711583,
      "our_true_pairs_total": 711583,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 100.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": 1150913,
      "ground_truth_pairs_labeled": 711583,
      "match_level_distribution": {
        "1": 327715,
        "2": 991470,
        "3": 1041380
      },
      "top_match_keys": [
        [
          "ADDRESS+NATIONALITY-DOB-TAX_ID",
          760021
        ],
        [
          "NAME+WEBSITE+NATIONALITY-DOB-TAX_ID",
          247497
        ],
        [
          "NAME+EMAIL+NATIONALITY-DOB-TAX_ID",
          242607
        ],
        [
          "NAME",
          182790
        ],
        [
          "OTHER_ID+NATIONALITY-DOB-TAX_ID",
          139484
        ],
        [
          "NAME+WEBSITE+NATIONALITY-DOB-TAX_ID-LEI_NUMBER",
          126928
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          117140
        ],
        [
          "NAME+DOB",
          65241
        ],
        [
          "ADDRESS+NATIONALITY-DOB",
          50668
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          40313
        ]
      ],
      "entity_size_distribution": {
        "1": 123686,
        "2": 73625,
        "3": 43161,
        "4": 25937,
        "5": 12935,
        "6": 7791,
        "7": 79,
        "8": 47,
        "9": 33,
        "10": 6,
        "11": 4,
        "12": 2
      },
      "our_entity_size_distribution": {
        "1": 91162,
        "2": 55668,
        "3": 22736,
        "4": 13504,
        "5": 6639,
        "6": 3228,
        "7": 70,
        "8": 146,
        "9": 207,
        "10": 269,
        "11": 313,
        "12": 375,
        "13": 399,
        "14": 434,
        "15": 379,
        "16": 373,
        "17": 303,
        "18": 202,
        "19": 173,
        "20": 112,
        "21": 64,
        "22": 49,
        "23": 23,
        "24": 29,
        "25": 13,
        "26": 5,
        "27": 4,
        "28": 3
      },
      "entity_pairings_distribution": {
        "0": 123686,
        "1": 73625,
        "3": 43161,
        "6": 25937,
        "10": 12935,
        "15": 7791,
        "21": 79,
        "28": 47,
        "36": 33,
        "45": 6,
        "55": 4,
        "66": 2
      },
      "record_pairing_degree_distribution": {
        "0": 123686,
        "1": 147250,
        "2": 129483,
        "3": 103748,
        "4": 64675,
        "5": 46746,
        "6": 553,
        "7": 376,
        "8": 297,
        "9": 60,
        "10": 44,
        "11": 24
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260303_221424__one-million-partial-616k/input_source.jsonl",
      "management_summary_path": "20260303_221424__one-million-partial-616k/management_summary.md",
      "ground_truth_summary_path": "20260303_221424__one-million-partial-616k/ground_truth_match_quality.md",
      "technical_path": "20260303_221424__one-million-partial-616k/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_221424__one-million-partial-616k/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 3086
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 679516738
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 9046
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 156767372
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 2898
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/input_normalized.jsonl",
          "display_name": "technical output/input_normalized.jsonl",
          "size_bytes": 786750874
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 12870
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 786750874
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2536
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 9432
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 180044205
        },
        {
          "relative_path": "20260303_221424__one-million-partial-616k/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 3954
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 616942,
            "actual": 616942,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 2360565,
            "actual": 2360565,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 287306,
            "actual": 287306,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 27.01,
            "actual": 27.01,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 100.0,
            "actual": 100.0,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 72.99,
            "actual": 72.99,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 56.32,
            "actual": 56.32,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_221424__one-million-partial-616k/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_174641__one-million-final-stream-debug",
      "run_timestamp": "20260303_174641",
      "run_datetime": "2026-03-03T17:46:41",
      "run_label": "one-million-final-stream-debug",
      "source_input_name": "one_million_stress.jsonl",
      "run_status": "incomplete",
      "has_management_summary": false,
      "has_ground_truth_summary": false,
      "has_run_summary": false,
      "overall_ok": null,
      "quality_available": false,
      "generated_at": null,
      "execution_seconds": null,
      "execution_minutes": null,
      "execution_minutes_estimated": null,
      "execution_minutes_is_estimate": false,
      "records_input": null,
      "records_input_loaded": null,
      "records_input_reported": null,
      "records_exported": null,
      "our_entities_formed": null,
      "their_entities_formed": null,
      "our_grouped_members": null,
      "their_grouped_members": null,
      "our_match_pct": null,
      "their_match_pct": null,
      "our_match_gain_loss_pct": null,
      "their_match_gain_loss_pct": null,
      "our_entity_gain_loss_pct": null,
      "their_entity_gain_loss_pct": null,
      "our_resolved_entities": null,
      "resolved_entities": null,
      "matched_records": null,
      "matched_pairs": null,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": null,
      "false_positive": null,
      "false_negative": null,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 0,
      "our_true_pairs_total": 0,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": null,
      "ground_truth_pairs_labeled": null,
      "match_level_distribution": {},
      "top_match_keys": [],
      "entity_size_distribution": {},
      "our_entity_size_distribution": {},
      "entity_pairings_distribution": {},
      "record_pairing_degree_distribution": {},
      "explain_coverage": {},
      "runtime_warnings": [],
      "input_source_path": "20260303_174641__one-million-final-stream-debug/input_source.json",
      "management_summary_path": "20260303_174641__one-million-final-stream-debug/management_summary.md",
      "ground_truth_summary_path": "20260303_174641__one-million-final-stream-debug/ground_truth_match_quality.md",
      "technical_path": "20260303_174641__one-million-final-stream-debug/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_174641__one-million-final-stream-debug/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_174641__one-million-final-stream-debug/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 786750874
        },
        {
          "relative_path": "20260303_174641__one-million-final-stream-debug/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2536
        }
      ],
      "validation": {
        "status": "SKIP",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": null,
            "actual": null,
            "status": "SKIP",
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
            "actual": null,
            "status": "SKIP",
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174641__one-million-final-stream-debug/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_174451__one-million-final-stream",
      "run_timestamp": "20260303_174451",
      "run_datetime": "2026-03-03T17:44:51",
      "run_label": "one-million-final-stream",
      "source_input_name": "one_million_stress.jsonl",
      "run_status": "incomplete",
      "has_management_summary": false,
      "has_ground_truth_summary": false,
      "has_run_summary": false,
      "overall_ok": null,
      "quality_available": false,
      "generated_at": null,
      "execution_seconds": null,
      "execution_minutes": null,
      "execution_minutes_estimated": null,
      "execution_minutes_is_estimate": false,
      "records_input": null,
      "records_input_loaded": null,
      "records_input_reported": null,
      "records_exported": null,
      "our_entities_formed": null,
      "their_entities_formed": null,
      "our_grouped_members": null,
      "their_grouped_members": null,
      "our_match_pct": null,
      "their_match_pct": null,
      "our_match_gain_loss_pct": null,
      "their_match_gain_loss_pct": null,
      "our_entity_gain_loss_pct": null,
      "their_entity_gain_loss_pct": null,
      "our_resolved_entities": null,
      "resolved_entities": null,
      "matched_records": null,
      "matched_pairs": null,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": null,
      "false_positive": null,
      "false_negative": null,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 0,
      "our_true_pairs_total": 0,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": null,
      "ground_truth_pairs_labeled": null,
      "match_level_distribution": {},
      "top_match_keys": [],
      "entity_size_distribution": {},
      "our_entity_size_distribution": {},
      "entity_pairings_distribution": {},
      "record_pairing_degree_distribution": {},
      "explain_coverage": {},
      "runtime_warnings": [],
      "input_source_path": "20260303_174451__one-million-final-stream/input_source.json",
      "management_summary_path": "20260303_174451__one-million-final-stream/management_summary.md",
      "ground_truth_summary_path": "20260303_174451__one-million-final-stream/ground_truth_match_quality.md",
      "technical_path": "20260303_174451__one-million-final-stream/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_174451__one-million-final-stream/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_174451__one-million-final-stream/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 786750874
        },
        {
          "relative_path": "20260303_174451__one-million-final-stream/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2460
        }
      ],
      "validation": {
        "status": "SKIP",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": null,
            "actual": null,
            "status": "SKIP",
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
            "actual": null,
            "status": "SKIP",
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174451__one-million-final-stream/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_174400__stream-smoke-30c",
      "run_timestamp": "20260303_174400",
      "run_datetime": "2026-03-03T17:44:00",
      "run_label": "stream-smoke-30c",
      "source_input_name": "stream_smoke_30.jsonl",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-03T16:44:32",
      "execution_seconds": 30.802,
      "execution_minutes": 0.51,
      "execution_minutes_estimated": 0.51,
      "execution_minutes_is_estimate": false,
      "records_input": 30,
      "records_input_loaded": 30,
      "records_input_reported": 30,
      "records_exported": 30,
      "our_entities_formed": 10,
      "their_entities_formed": 21,
      "our_grouped_members": 8,
      "their_grouped_members": 14,
      "our_match_pct": 26.67,
      "their_match_pct": 46.67,
      "our_match_gain_loss_pct": -20.0,
      "their_match_gain_loss_pct": 20.0,
      "our_entity_gain_loss_pct": -36.67,
      "their_entity_gain_loss_pct": 36.67,
      "our_resolved_entities": 10,
      "resolved_entities": 21,
      "matched_records": 9,
      "matched_pairs": 9,
      "pair_precision_pct": 40.0,
      "pair_recall_pct": 50.0,
      "true_positive": 2,
      "false_positive": 3,
      "false_negative": 2,
      "discovery_available": true,
      "extra_true_matches_found": 7,
      "extra_false_matches_found": 0,
      "extra_match_precision_pct": 100.0,
      "extra_match_recall_pct": 43.75,
      "extra_gain_vs_known_pct": 175.0,
      "known_pairs_ipg": 4,
      "discoverable_true_pairs": 16,
      "predicted_pairs_beyond_known": 7,
      "net_extra_matches": 7,
      "overall_false_positive_pct": 60.0,
      "overall_false_positive_discovery_pct": 0.0,
      "overall_match_correctness_pct": 100.0,
      "our_true_positive": 4,
      "our_true_pairs_total": 20,
      "our_false_positive": 0,
      "our_false_negative": 16,
      "our_match_coverage_pct": 20.0,
      "baseline_match_coverage_pct": 20.0,
      "senzing_true_coverage_pct": 45.0,
      "predicted_pairs_labeled": 5,
      "ground_truth_pairs_labeled": 4,
      "match_level_distribution": {
        "1": 9
      },
      "top_match_keys": [
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          2
        ],
        [
          "NAME+ADDRESS+TAX_ID+EMAIL",
          1
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          1
        ],
        [
          "NAME+DOB+ADDRESS+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER-TAX_ID",
          1
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+NATIONALITY",
          1
        ]
      ],
      "entity_size_distribution": {
        "1": 16,
        "2": 1,
        "3": 4
      },
      "our_entity_size_distribution": {
        "1": 6,
        "2": 4
      },
      "entity_pairings_distribution": {
        "0": 16,
        "1": 1,
        "3": 4
      },
      "record_pairing_degree_distribution": {
        "0": 16,
        "1": 2,
        "2": 12
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [
        "Export executed in stream mode (no standalone export CSV written)."
      ],
      "input_source_path": "20260303_174400__stream-smoke-30c/input_source.jsonl",
      "management_summary_path": "20260303_174400__stream-smoke-30c/management_summary.md",
      "ground_truth_summary_path": "20260303_174400__stream-smoke-30c/ground_truth_match_quality.md",
      "technical_path": "20260303_174400__stream-smoke-30c/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_174400__stream-smoke-30c/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1602
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 20404
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 2435
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 1195
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 941
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 3406
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 23897
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2411
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 587
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 836
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 4403
        },
        {
          "relative_path": "20260303_174400__stream-smoke-30c/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 6672
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 30,
            "actual": 30,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 9,
            "actual": 9,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 21,
            "actual": 21,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 40.0,
            "actual": 40.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 20.0,
            "actual": 20.0,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 60.0,
            "actual": 60.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 50.0,
            "actual": 50.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174400__stream-smoke-30c/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_174221__stream-smoke-30b",
      "run_timestamp": "20260303_174221",
      "run_datetime": "2026-03-03T17:42:21",
      "run_label": "stream-smoke-30b",
      "source_input_name": "stream_smoke_30.jsonl",
      "run_status": "incomplete",
      "has_management_summary": false,
      "has_ground_truth_summary": false,
      "has_run_summary": false,
      "overall_ok": null,
      "quality_available": false,
      "generated_at": null,
      "execution_seconds": null,
      "execution_minutes": null,
      "execution_minutes_estimated": null,
      "execution_minutes_is_estimate": false,
      "records_input": null,
      "records_input_loaded": null,
      "records_input_reported": null,
      "records_exported": null,
      "our_entities_formed": null,
      "their_entities_formed": null,
      "our_grouped_members": null,
      "their_grouped_members": null,
      "our_match_pct": null,
      "their_match_pct": null,
      "our_match_gain_loss_pct": null,
      "their_match_gain_loss_pct": null,
      "our_entity_gain_loss_pct": null,
      "their_entity_gain_loss_pct": null,
      "our_resolved_entities": null,
      "resolved_entities": null,
      "matched_records": null,
      "matched_pairs": null,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": null,
      "false_positive": null,
      "false_negative": null,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 0,
      "our_true_pairs_total": 0,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": null,
      "ground_truth_pairs_labeled": null,
      "match_level_distribution": {},
      "top_match_keys": [],
      "entity_size_distribution": {},
      "our_entity_size_distribution": {},
      "entity_pairings_distribution": {},
      "record_pairing_degree_distribution": {},
      "explain_coverage": {},
      "runtime_warnings": [],
      "input_source_path": "20260303_174221__stream-smoke-30b/input_source.json",
      "management_summary_path": "20260303_174221__stream-smoke-30b/management_summary.md",
      "ground_truth_summary_path": "20260303_174221__stream-smoke-30b/ground_truth_match_quality.md",
      "technical_path": "20260303_174221__stream-smoke-30b/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_174221__stream-smoke-30b/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_174221__stream-smoke-30b/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 23897
        },
        {
          "relative_path": "20260303_174221__stream-smoke-30b/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2402
        }
      ],
      "validation": {
        "status": "SKIP",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": null,
            "actual": null,
            "status": "SKIP",
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
            "actual": null,
            "status": "SKIP",
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_174221__stream-smoke-30b/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_173857__stream-smoke-30",
      "run_timestamp": "20260303_173857",
      "run_datetime": "2026-03-03T17:38:57",
      "run_label": "stream-smoke-30",
      "source_input_name": "stream_smoke_30.jsonl",
      "run_status": "incomplete",
      "has_management_summary": false,
      "has_ground_truth_summary": false,
      "has_run_summary": false,
      "overall_ok": null,
      "quality_available": false,
      "generated_at": null,
      "execution_seconds": null,
      "execution_minutes": null,
      "execution_minutes_estimated": null,
      "execution_minutes_is_estimate": false,
      "records_input": null,
      "records_input_loaded": null,
      "records_input_reported": null,
      "records_exported": null,
      "our_entities_formed": null,
      "their_entities_formed": null,
      "our_grouped_members": null,
      "their_grouped_members": null,
      "our_match_pct": null,
      "their_match_pct": null,
      "our_match_gain_loss_pct": null,
      "their_match_gain_loss_pct": null,
      "our_entity_gain_loss_pct": null,
      "their_entity_gain_loss_pct": null,
      "our_resolved_entities": null,
      "resolved_entities": null,
      "matched_records": null,
      "matched_pairs": null,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": null,
      "false_positive": null,
      "false_negative": null,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 0,
      "our_true_pairs_total": 0,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": null,
      "ground_truth_pairs_labeled": null,
      "match_level_distribution": {},
      "top_match_keys": [],
      "entity_size_distribution": {},
      "our_entity_size_distribution": {},
      "entity_pairings_distribution": {},
      "record_pairing_degree_distribution": {},
      "explain_coverage": {},
      "runtime_warnings": [],
      "input_source_path": "20260303_173857__stream-smoke-30/input_source.json",
      "management_summary_path": "20260303_173857__stream-smoke-30/management_summary.md",
      "ground_truth_summary_path": "20260303_173857__stream-smoke-30/ground_truth_match_quality.md",
      "technical_path": "20260303_173857__stream-smoke-30/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_173857__stream-smoke-30/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_173857__stream-smoke-30/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 23897
        },
        {
          "relative_path": "20260303_173857__stream-smoke-30/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2401
        }
      ],
      "validation": {
        "status": "SKIP",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": null,
            "actual": null,
            "status": "SKIP",
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
            "actual": null,
            "status": "SKIP",
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_173857__stream-smoke-30/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_171324__one-million-final",
      "run_timestamp": "20260303_171324",
      "run_datetime": "2026-03-03T17:13:24",
      "run_label": "one-million-final",
      "source_input_name": "one_million_stress.jsonl",
      "run_status": "incomplete",
      "has_management_summary": false,
      "has_ground_truth_summary": false,
      "has_run_summary": false,
      "overall_ok": null,
      "quality_available": false,
      "generated_at": null,
      "execution_seconds": null,
      "execution_minutes": null,
      "execution_minutes_estimated": null,
      "execution_minutes_is_estimate": false,
      "records_input": null,
      "records_input_loaded": null,
      "records_input_reported": null,
      "records_exported": null,
      "our_entities_formed": null,
      "their_entities_formed": null,
      "our_grouped_members": null,
      "their_grouped_members": null,
      "our_match_pct": null,
      "their_match_pct": null,
      "our_match_gain_loss_pct": null,
      "their_match_gain_loss_pct": null,
      "our_entity_gain_loss_pct": null,
      "their_entity_gain_loss_pct": null,
      "our_resolved_entities": null,
      "resolved_entities": null,
      "matched_records": null,
      "matched_pairs": null,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": null,
      "false_positive": null,
      "false_negative": null,
      "discovery_available": false,
      "extra_true_matches_found": null,
      "extra_false_matches_found": null,
      "extra_match_precision_pct": null,
      "extra_match_recall_pct": null,
      "extra_gain_vs_known_pct": null,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": null,
      "predicted_pairs_beyond_known": null,
      "net_extra_matches": null,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": null,
      "overall_match_correctness_pct": null,
      "our_true_positive": 0,
      "our_true_pairs_total": 0,
      "our_false_positive": 0,
      "our_false_negative": 0,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": null,
      "senzing_true_coverage_pct": null,
      "predicted_pairs_labeled": null,
      "ground_truth_pairs_labeled": null,
      "match_level_distribution": {},
      "top_match_keys": [],
      "entity_size_distribution": {},
      "our_entity_size_distribution": {},
      "entity_pairings_distribution": {},
      "record_pairing_degree_distribution": {},
      "explain_coverage": {},
      "runtime_warnings": [],
      "input_source_path": "20260303_171324__one-million-final/input_source.json",
      "management_summary_path": "20260303_171324__one-million-final/management_summary.md",
      "ground_truth_summary_path": "20260303_171324__one-million-final/ground_truth_match_quality.md",
      "technical_path": "20260303_171324__one-million-final/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_171324__one-million-final/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_171324__one-million-final/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 786750874
        },
        {
          "relative_path": "20260303_171324__one-million-final/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2391
        }
      ],
      "validation": {
        "status": "SKIP",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/input_normalized.jsonl"
          },
          {
            "name": "Matched Pairs",
            "expected": null,
            "actual": null,
            "status": "SKIP",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": null,
            "actual": null,
            "status": "SKIP",
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
            "actual": null,
            "status": "SKIP",
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/input_source.json",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171324__one-million-final/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_171153__path-smoke-50",
      "run_timestamp": "20260303_171153",
      "run_datetime": "2026-03-03T17:11:53",
      "run_label": "path-smoke-50",
      "source_input_name": "path_smoke_50.jsonl",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-03T16:12:19",
      "execution_seconds": 24.709,
      "execution_minutes": 0.41,
      "execution_minutes_estimated": 0.41,
      "execution_minutes_is_estimate": false,
      "records_input": 50,
      "records_input_loaded": 50,
      "records_input_reported": 50,
      "records_exported": 50,
      "our_entities_formed": 22,
      "their_entities_formed": 38,
      "our_grouped_members": 12,
      "their_grouped_members": 19,
      "our_match_pct": 24.0,
      "their_match_pct": 38.0,
      "our_match_gain_loss_pct": -14.0,
      "their_match_gain_loss_pct": 14.0,
      "our_entity_gain_loss_pct": -32.0,
      "their_entity_gain_loss_pct": 32.0,
      "our_resolved_entities": 22,
      "resolved_entities": 38,
      "matched_records": 12,
      "matched_pairs": 12,
      "pair_precision_pct": 42.86,
      "pair_recall_pct": 50.0,
      "true_positive": 3,
      "false_positive": 4,
      "false_negative": 3,
      "discovery_available": true,
      "extra_true_matches_found": 9,
      "extra_false_matches_found": 0,
      "extra_match_precision_pct": 100.0,
      "extra_match_recall_pct": 39.13,
      "extra_gain_vs_known_pct": 150.0,
      "known_pairs_ipg": 6,
      "discoverable_true_pairs": 23,
      "predicted_pairs_beyond_known": 9,
      "net_extra_matches": 9,
      "overall_false_positive_pct": 57.14,
      "overall_false_positive_discovery_pct": 0.0,
      "overall_match_correctness_pct": 100.0,
      "our_true_positive": 6,
      "our_true_pairs_total": 29,
      "our_false_positive": 0,
      "our_false_negative": 23,
      "our_match_coverage_pct": 20.69,
      "baseline_match_coverage_pct": 20.69,
      "senzing_true_coverage_pct": 41.38,
      "predicted_pairs_labeled": 7,
      "ground_truth_pairs_labeled": 6,
      "match_level_distribution": {
        "1": 12
      },
      "top_match_keys": [
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          3
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          2
        ],
        [
          "DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          1
        ],
        [
          "EMAIL+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID",
          1
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          1
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+NATIONALITY",
          1
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          1
        ]
      ],
      "entity_size_distribution": {
        "1": 31,
        "2": 2,
        "3": 5
      },
      "our_entity_size_distribution": {
        "1": 16,
        "2": 6
      },
      "entity_pairings_distribution": {
        "0": 31,
        "1": 2,
        "3": 5
      },
      "record_pairing_degree_distribution": {
        "0": 31,
        "1": 4,
        "2": 15
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260303_171153__path-smoke-50/input_source.jsonl",
      "management_summary_path": "20260303_171153__path-smoke-50/management_summary.md",
      "ground_truth_summary_path": "20260303_171153__path-smoke-50/ground_truth_match_quality.md",
      "technical_path": "20260303_171153__path-smoke-50/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_171153__path-smoke-50/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1602
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 33892
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 2438
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 1774
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 957
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 3477
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 38905
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2357
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 603
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 1037
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 3790
        },
        {
          "relative_path": "20260303_171153__path-smoke-50/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7187
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 50,
            "actual": 50,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 12,
            "actual": 12,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 38,
            "actual": 38,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 42.86,
            "actual": 42.86,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 20.69,
            "actual": 20.69,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 57.14,
            "actual": 57.14,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 50.0,
            "actual": 50.0,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_171153__path-smoke-50/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_155125__metric-smoke-200-safe-tuned",
      "run_timestamp": "20260303_155125",
      "run_datetime": "2026-03-03T15:51:25",
      "run_label": "metric-smoke-200-safe-tuned",
      "source_input_name": "metric_smoke_200.jsonl",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-03T14:51:50",
      "execution_seconds": 23.493,
      "execution_minutes": 0.39,
      "execution_minutes_estimated": 0.39,
      "execution_minutes_is_estimate": false,
      "records_input": 200,
      "records_input_loaded": 200,
      "records_input_reported": 200,
      "records_exported": 204,
      "our_entities_formed": 83,
      "their_entities_formed": 98,
      "our_grouped_members": 97,
      "their_grouped_members": 158,
      "our_match_pct": 48.5,
      "their_match_pct": 79.0,
      "our_match_gain_loss_pct": -30.5,
      "their_match_gain_loss_pct": 30.5,
      "our_entity_gain_loss_pct": -7.5,
      "their_entity_gain_loss_pct": 7.5,
      "our_resolved_entities": 83,
      "resolved_entities": 98,
      "matched_records": 106,
      "matched_pairs": 106,
      "pair_precision_pct": 68.25,
      "pair_recall_pct": 98.85,
      "true_positive": 86,
      "false_positive": 40,
      "false_negative": 1,
      "discovery_available": true,
      "extra_true_matches_found": 58,
      "extra_false_matches_found": 0,
      "extra_match_precision_pct": 100.0,
      "extra_match_recall_pct": 61.7,
      "extra_gain_vs_known_pct": 66.67,
      "known_pairs_ipg": 87,
      "discoverable_true_pairs": 94,
      "predicted_pairs_beyond_known": 58,
      "net_extra_matches": 58,
      "overall_false_positive_pct": 31.75,
      "overall_false_positive_discovery_pct": 0.0,
      "overall_match_correctness_pct": 100.0,
      "our_true_positive": 87,
      "our_true_pairs_total": 181,
      "our_false_positive": 0,
      "our_false_negative": 94,
      "our_match_coverage_pct": 48.07,
      "baseline_match_coverage_pct": 48.07,
      "senzing_true_coverage_pct": 58.56,
      "predicted_pairs_labeled": 126,
      "ground_truth_pairs_labeled": 87,
      "match_level_distribution": {
        "1": 102,
        "2": 4
      },
      "top_match_keys": [
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          30
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          11
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          10
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          4
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          4
        ],
        [
          "NAME+DOB+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          4
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          3
        ],
        [
          "NAME+DOB+ADDRESS+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          3
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          3
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY+LEI_NUMBER",
          3
        ]
      ],
      "entity_size_distribution": {
        "1": 42,
        "2": 28,
        "3": 18,
        "4": 5,
        "5": 2,
        "6": 3
      },
      "our_entity_size_distribution": {
        "1": 43,
        "2": 30,
        "3": 7,
        "4": 1,
        "6": 2
      },
      "entity_pairings_distribution": {
        "0": 42,
        "1": 28,
        "3": 18,
        "6": 5,
        "10": 2,
        "15": 3
      },
      "record_pairing_degree_distribution": {
        "0": 42,
        "1": 56,
        "2": 54,
        "3": 20,
        "4": 10,
        "5": 18
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260303_155125__metric-smoke-200-safe-tuned/input_source.jsonl",
      "management_summary_path": "20260303_155125__metric-smoke-200-safe-tuned/management_summary.md",
      "ground_truth_summary_path": "20260303_155125__metric-smoke-200-safe-tuned/ground_truth_match_quality.md",
      "technical_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1694
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 135834
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3522
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 9899
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1101
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 4793
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 154674
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2178
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 1820
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 8640
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 3183
        },
        {
          "relative_path": "20260303_155125__metric-smoke-200-safe-tuned/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7757
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 200,
            "actual": 200,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 106,
            "actual": 106,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 98,
            "actual": 98,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 68.25,
            "actual": 68.25,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 48.07,
            "actual": 48.07,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 31.75,
            "actual": 31.75,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 1.15,
            "actual": 1.15,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_155125__metric-smoke-200-safe-tuned/technical output/input_normalized.jsonl"
      }
    },
    {
      "run_id": "20260303_153108__metric-smoke-200",
      "run_timestamp": "20260303_153108",
      "run_datetime": "2026-03-03T15:31:08",
      "run_label": "metric-smoke-200",
      "source_input_name": "mvp_metric_smoke_200.jsonl",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-03T14:31:33",
      "execution_seconds": 23.768,
      "execution_minutes": 0.4,
      "execution_minutes_estimated": 0.4,
      "execution_minutes_is_estimate": false,
      "records_input": 200,
      "records_input_loaded": 200,
      "records_input_reported": 200,
      "records_exported": 204,
      "our_entities_formed": 83,
      "their_entities_formed": 97,
      "our_grouped_members": 97,
      "their_grouped_members": 159,
      "our_match_pct": 48.5,
      "their_match_pct": 79.5,
      "our_match_gain_loss_pct": -31.0,
      "their_match_gain_loss_pct": 31.0,
      "our_entity_gain_loss_pct": -7.0,
      "their_entity_gain_loss_pct": 7.0,
      "our_resolved_entities": 83,
      "resolved_entities": 97,
      "matched_records": 107,
      "matched_pairs": 107,
      "pair_precision_pct": 67.97,
      "pair_recall_pct": 100.0,
      "true_positive": 87,
      "false_positive": 41,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 55,
      "extra_false_matches_found": 0,
      "extra_match_precision_pct": 100.0,
      "extra_match_recall_pct": 58.51,
      "extra_gain_vs_known_pct": 63.22,
      "known_pairs_ipg": 87,
      "discoverable_true_pairs": 94,
      "predicted_pairs_beyond_known": 55,
      "net_extra_matches": 55,
      "overall_false_positive_pct": 32.03,
      "overall_false_positive_discovery_pct": 0.0,
      "overall_match_correctness_pct": 100.0,
      "our_true_positive": 87,
      "our_true_pairs_total": 181,
      "our_false_positive": 0,
      "our_false_negative": 94,
      "our_match_coverage_pct": 48.07,
      "baseline_match_coverage_pct": 48.07,
      "senzing_true_coverage_pct": 59.12,
      "predicted_pairs_labeled": 128,
      "ground_truth_pairs_labeled": 87,
      "match_level_distribution": {
        "1": 103,
        "2": 4
      },
      "top_match_keys": [
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          30
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          12
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          11
        ],
        [
          "NAME+DOB+EMAIL+NATIONALITY",
          4
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          4
        ],
        [
          "NAME+DOB+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          4
        ],
        [
          "NAME+DOB+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          4
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          3
        ],
        [
          "NAME+DOB+ADDRESS+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          3
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          3
        ]
      ],
      "entity_size_distribution": {
        "1": 41,
        "2": 27,
        "3": 19,
        "4": 5,
        "5": 2,
        "6": 3
      },
      "our_entity_size_distribution": {
        "1": 43,
        "2": 30,
        "3": 7,
        "4": 1,
        "6": 2
      },
      "entity_pairings_distribution": {
        "0": 41,
        "1": 27,
        "3": 19,
        "6": 5,
        "10": 2,
        "15": 3
      },
      "record_pairing_degree_distribution": {
        "0": 41,
        "1": 54,
        "2": 57,
        "3": 20,
        "4": 10,
        "5": 18
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260303_153108__metric-smoke-200/input_source.jsonl",
      "management_summary_path": "20260303_153108__metric-smoke-200/management_summary.md",
      "ground_truth_summary_path": "20260303_153108__metric-smoke-200/ground_truth_match_quality.md",
      "technical_path": "20260303_153108__metric-smoke-200/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260303_153108__metric-smoke-200/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1695
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 135834
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 3423
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 10009
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 1077
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 4664
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 154674
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 1703
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 8787
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 2603
        },
        {
          "relative_path": "20260303_153108__metric-smoke-200/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 7717
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 200,
            "actual": 200,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 107,
            "actual": 107,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 97,
            "actual": 97,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 67.97,
            "actual": 67.97,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 48.07,
            "actual": 48.07,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 32.03,
            "actual": 32.03,
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
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260303_153108__metric-smoke-200/technical output/input_normalized.jsonl"
      }
    }
  ],
  "summary": {
    "runs_total": 10,
    "quality_runs_total": 5,
    "successful_runs": 4,
    "failed_runs": 1,
    "incomplete_runs": 5,
    "latest_run_id": "20260303_221424__one-million-partial-616k",
    "avg_pair_precision_pct": 49.22,
    "avg_pair_recall_pct": 68.51,
    "records_input_total": 617422,
    "matched_pairs_total": 2360799
  }
};

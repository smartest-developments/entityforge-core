window.MVP_DASHBOARD_DATA = {
  "generated_at": "2026-03-03T23:29:03",
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
      "our_entities_formed": 380861,
      "their_entities_formed": 287306,
      "our_grouped_members": 341801,
      "their_grouped_members": 493256,
      "our_match_pct": 55.4,
      "their_match_pct": 79.95,
      "our_match_gain_loss_pct": -24.55,
      "their_match_gain_loss_pct": 24.55,
      "our_entity_gain_loss_pct": 15.16,
      "their_entity_gain_loss_pct": -15.16,
      "our_resolved_entities": 380861,
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
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          117140
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          40313
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          28908
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY",
          20898
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          13035
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          12708
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          12480
        ],
        [
          "NAME+DOB+ADDRESS+OTHER_ID+NATIONALITY",
          11097
        ],
        [
          "NAME+DOB+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          9405
        ],
        [
          "NAME+DOB+NATIONALITY",
          7028
        ]
      ],
      "top_match_keys_total_pairs": 327715,
      "top_match_keys_top10_total": 273012,
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
        "1": 275141,
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
      "top_match_keys_total_pairs": 0,
      "top_match_keys_top10_total": 0,
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
    }
  ],
  "summary": {
    "runs_total": 2,
    "quality_runs_total": 1,
    "successful_runs": 0,
    "failed_runs": 1,
    "incomplete_runs": 1,
    "latest_run_id": "20260303_221424__one-million-partial-616k",
    "avg_pair_precision_pct": 27.01,
    "avg_pair_recall_pct": 43.68,
    "records_input_total": 616942,
    "matched_pairs_total": 2360565
  }
};

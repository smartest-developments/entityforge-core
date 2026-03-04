window.MVP_DASHBOARD_DATA = {
  "generated_at": "2026-03-04T09:36:53",
  "output_root": "/Users/simones/Developer/mapper-ai-main/MVP/output",
  "runs": [
    {
      "run_id": "20260304_085032__one-hundred-thousand-full",
      "run_timestamp": "20260304_085032",
      "run_datetime": "2026-03-04T08:50:32",
      "run_label": "one-hundred-thousand-full",
      "source_input_name": "one_hundred_thousand_stress.jsonl",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": true,
      "generated_at": "2026-03-04T08:36:51",
      "execution_seconds": 2773.58,
      "execution_minutes": 46.23,
      "execution_minutes_estimated": 46.23,
      "execution_minutes_is_estimate": false,
      "records_input": 100000,
      "records_input_loaded": 100000,
      "records_input_reported": 100000,
      "records_exported": 247703,
      "our_entities_formed": 64401,
      "their_entities_formed": 46793,
      "our_grouped_members": 54769,
      "their_grouped_members": 79593,
      "our_match_pct": 54.77,
      "their_match_pct": 79.59,
      "our_match_gain_loss_pct": -24.82,
      "their_match_gain_loss_pct": 24.82,
      "our_entity_gain_loss_pct": 17.61,
      "their_entity_gain_loss_pct": -17.61,
      "our_resolved_entities": 64401,
      "resolved_entities": 46793,
      "matched_records": 200393,
      "matched_pairs": 200393,
      "pair_precision_pct": 37.32,
      "pair_recall_pct": 81.65,
      "true_positive": 51273,
      "false_positive": 86106,
      "false_negative": 11526,
      "discovery_available": true,
      "extra_true_matches_found": 28243,
      "extra_false_matches_found": 141562,
      "extra_match_precision_pct": 16.63,
      "extra_match_recall_pct": 55.72,
      "extra_gain_vs_known_pct": 54.01,
      "known_pairs_ipg": 52296,
      "discoverable_true_pairs": 50689,
      "predicted_pairs_beyond_known": 169805,
      "net_extra_matches": -113319,
      "overall_false_positive_pct": 62.68,
      "overall_false_positive_discovery_pct": 70.64,
      "overall_match_correctness_pct": 29.36,
      "our_true_positive": 52296,
      "our_true_pairs_total": 102985,
      "our_false_positive": 10503,
      "our_false_negative": 50689,
      "our_match_coverage_pct": 50.78,
      "baseline_match_coverage_pct": 50.78,
      "senzing_true_coverage_pct": 57.13,
      "predicted_pairs_labeled": 137379,
      "ground_truth_pairs_labeled": 62799,
      "match_level_distribution": {
        "1": 52690,
        "2": 97845,
        "3": 49858
      },
      "top_match_keys": [
        [
          "NAME+DOB+ADDRESS+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          9867
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+OTHER_ID+NATIONALITY",
          9070
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          4503
        ],
        [
          "NAME+DOB+TAX_ID+OTHER_ID+NATIONALITY",
          3734
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY",
          3282
        ],
        [
          "NAME+DOB+TAX_ID+EMAIL+OTHER_ID+NATIONALITY",
          2609
        ],
        [
          "NAME+DOB+TAX_ID+WEBSITE+OTHER_ID+NATIONALITY+LEI_NUMBER",
          1524
        ],
        [
          "NAME+DOB+OTHER_ID+NATIONALITY",
          1380
        ],
        [
          "NAME+DOB+TAX_ID+NATIONALITY",
          1374
        ],
        [
          "NAME+DOB+ADDRESS+TAX_ID+NATIONALITY",
          1187
        ]
      ],
      "top_match_keys_total_pairs": 52690,
      "top_match_keys_top10_total": 38530,
      "entity_size_distribution": {
        "1": 20407,
        "2": 11857,
        "3": 6955,
        "4": 4174,
        "5": 2093,
        "6": 1297,
        "7": 9,
        "8": 1
      },
      "our_entity_size_distribution": {
        "1": 45231,
        "2": 10044,
        "3": 4492,
        "4": 2683,
        "5": 1292,
        "6": 618,
        "7": 27,
        "8": 10,
        "9": 4
      },
      "entity_pairings_distribution": {
        "0": 20407,
        "1": 11857,
        "3": 6955,
        "6": 4174,
        "10": 2093,
        "15": 1297,
        "21": 9,
        "28": 1
      },
      "record_pairing_degree_distribution": {
        "0": 20407,
        "1": 23714,
        "2": 20865,
        "3": 16696,
        "4": 10465,
        "5": 7782,
        "6": 63,
        "7": 8
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [
        "load_records primary attempt failed; fallback 'fallback_single_thread' succeeded.",
        "Export executed in stream mode (no standalone export CSV written)."
      ],
      "input_source_path": "20260304_085032__one-hundred-thousand-full/input_source.jsonl",
      "management_summary_path": "20260304_085032__one-hundred-thousand-full/management_summary.md",
      "ground_truth_summary_path": "20260304_085032__one-hundred-thousand-full/ground_truth_match_quality.md",
      "technical_path": "20260304_085032__one-hundred-thousand-full/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 2556
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/input_source.jsonl",
          "display_name": "input_source.jsonl",
          "size_bytes": 67956574
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 10493
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical",
          "display_name": "technical",
          "size_bytes": 0
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 14362788
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 988
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 2221
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 13405
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 78598737
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 2479
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 9660
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 15527044
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 919
        },
        {
          "relative_path": "20260304_085032__one-hundred-thousand-full/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 8671
        }
      ],
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 100000,
            "actual": 100000,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 200393,
            "actual": 200393,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 46793,
            "actual": 46793,
            "status": "PASS",
            "source": "technical output/entity_records.csv"
          },
          {
            "name": "Match Correctness (%)",
            "expected": 37.32,
            "actual": 37.32,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Our Match Coverage (%)",
            "expected": 50.78,
            "actual": 50.78,
            "status": "PASS",
            "source": "technical output/management_summary.json (discovery baseline)"
          },
          {
            "name": "False Positive (%)",
            "expected": 62.68,
            "actual": 62.68,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          },
          {
            "name": "Match Missed (%)",
            "expected": 18.35,
            "actual": 18.35,
            "status": "PASS",
            "source": "technical output/ground_truth_match_quality.json (pair_metrics)"
          }
        ],
        "run_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full",
        "input_source_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/input_source.jsonl",
        "management_summary_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/technical output/management_summary.json",
        "ground_truth_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simones/Developer/mapper-ai-main/MVP/output/20260304_085032__one-hundred-thousand-full/technical output/input_normalized.jsonl"
      }
    }
  ],
  "summary": {
    "runs_total": 1,
    "quality_runs_total": 1,
    "successful_runs": 1,
    "failed_runs": 0,
    "incomplete_runs": 0,
    "latest_run_id": "20260304_085032__one-hundred-thousand-full",
    "avg_pair_precision_pct": 37.32,
    "avg_pair_recall_pct": 81.65,
    "records_input_total": 100000,
    "matched_pairs_total": 200393
  }
};

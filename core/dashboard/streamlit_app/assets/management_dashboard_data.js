window.MVP_DASHBOARD_DATA = {
  "generated_at": "2026-03-10T14:51:32",
  "output_root": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output",
  "runs": [
    {
      "run_id": "20260310_145026__smoke3",
      "run_timestamp": "20260310_145026",
      "run_datetime": "2026-03-10T14:50:26",
      "run_label": "smoke3",
      "source_input_name": "smoke_input.json",
      "run_status": "success",
      "has_management_summary": true,
      "has_ground_truth_summary": true,
      "has_run_summary": true,
      "overall_ok": true,
      "quality_available": false,
      "generated_at": "2026-03-10T13:51:32",
      "execution_seconds": 63.664,
      "execution_minutes": 1.06,
      "execution_minutes_estimated": 1.06,
      "execution_minutes_is_estimate": false,
      "records_input": 3,
      "records_input_loaded": 3,
      "records_input_reported": 3,
      "records_exported": 3,
      "our_entities_formed": 3,
      "their_entities_formed": 2,
      "our_grouped_members": 0,
      "their_grouped_members": 2,
      "our_match_pct": 0.0,
      "their_match_pct": 66.67,
      "our_match_gain_loss_pct": -66.67,
      "their_match_gain_loss_pct": 66.67,
      "our_entity_gain_loss_pct": 33.33,
      "their_entity_gain_loss_pct": -33.33,
      "our_resolved_entities": 3,
      "resolved_entities": 2,
      "matched_records": 1,
      "matched_pairs": 1,
      "pair_precision_pct": null,
      "pair_recall_pct": null,
      "true_positive": 0,
      "false_positive": 0,
      "false_negative": 0,
      "discovery_available": true,
      "extra_true_matches_found": 1,
      "extra_false_matches_found": 0,
      "extra_match_precision_pct": 100.0,
      "extra_match_recall_pct": 100.0,
      "extra_gain_vs_known_pct": 0.0,
      "known_pairs_ipg": 0,
      "discoverable_true_pairs": 1,
      "predicted_pairs_beyond_known": 1,
      "net_extra_matches": 1,
      "overall_false_positive_pct": null,
      "overall_false_positive_discovery_pct": 0.0,
      "overall_match_correctness_pct": 100.0,
      "our_true_positive": 0,
      "our_true_pairs_total": 1,
      "our_false_positive": 0,
      "our_false_negative": 1,
      "our_match_coverage_pct": 0.0,
      "baseline_match_coverage_pct": 0.0,
      "senzing_true_coverage_pct": 100.0,
      "predicted_pairs_labeled": 0,
      "ground_truth_pairs_labeled": 0,
      "match_level_distribution": {
        "1": 1
      },
      "top_match_keys": [
        [
          "NAME+DOB+EMAIL",
          1
        ]
      ],
      "top_match_keys_total_pairs": 1,
      "top_match_keys_top10_total": 1,
      "entity_size_distribution": {
        "1": 1,
        "2": 1
      },
      "our_entity_size_distribution": {
        "1": 3
      },
      "entity_pairings_distribution": {
        "0": 1,
        "1": 1
      },
      "record_pairing_degree_distribution": {
        "0": 1,
        "1": 2
      },
      "explain_coverage": {
        "why_entity_total": 0,
        "why_entity_ok": 0,
        "why_records_total": 0,
        "why_records_ok": 0
      },
      "runtime_warnings": [],
      "input_source_path": "20260310_145026__smoke3/input_source.json",
      "management_summary_path": "20260310_145026__smoke3/management_summary.md",
      "ground_truth_summary_path": "20260310_145026__smoke3/ground_truth_match_quality.md",
      "technical_path": "20260310_145026__smoke3/technical output",
      "mapping_info": {
        "data_source": "PARTNERS",
        "tax_id_type": "TIN",
        "execution_mode": "docker"
      },
      "artifacts": [
        {
          "relative_path": "20260310_145026__smoke3/ground_truth_match_quality.md",
          "display_name": "ground_truth_match_quality.md",
          "size_bytes": 1569
        },
        {
          "relative_path": "20260310_145026__smoke3/input_source.json",
          "display_name": "input_source.json",
          "size_bytes": 765
        },
        {
          "relative_path": "20260310_145026__smoke3/management_summary.md",
          "display_name": "management_summary.md",
          "size_bytes": 2034
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/entity_records.csv",
          "display_name": "technical output/entity_records.csv",
          "size_bytes": 194
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/field_map.json",
          "display_name": "technical output/field_map.json",
          "size_bytes": 709
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/ground_truth_match_quality.json",
          "display_name": "technical output/ground_truth_match_quality.json",
          "size_bytes": 890
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/management_summary.json",
          "display_name": "technical output/management_summary.json",
          "size_bytes": 2927
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/mapped_output.jsonl",
          "display_name": "technical output/mapped_output.jsonl",
          "size_bytes": 730
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/mapping_summary.json",
          "display_name": "technical output/mapping_summary.json",
          "size_bytes": 3016
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/match_stats.csv",
          "display_name": "technical output/match_stats.csv",
          "size_bytes": 154
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/matched_pairs.csv",
          "display_name": "technical output/matched_pairs.csv",
          "size_bytes": 203
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/run_registry.csv",
          "display_name": "technical output/run_registry.csv",
          "size_bytes": 1652
        },
        {
          "relative_path": "20260310_145026__smoke3/technical output/run_summary.json",
          "display_name": "technical output/run_summary.json",
          "size_bytes": 8691
        }
      ],
      "artifacts_truncated": false,
      "artifacts_total_files": 13,
      "validation": {
        "status": "PASS",
        "checks": [
          {
            "name": "Selected Input Records",
            "expected": 3,
            "actual": 3,
            "status": "PASS",
            "source": "technical output/entity_records.csv (deduplicated DATA_SOURCE+RECORD_ID)"
          },
          {
            "name": "Matched Pairs",
            "expected": 1,
            "actual": 1,
            "status": "PASS",
            "source": "technical output/matched_pairs.csv"
          },
          {
            "name": "Selected Resolved Entities",
            "expected": 2,
            "actual": 2,
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
        "run_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3",
        "input_source_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/input_source.json",
        "management_summary_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/technical output/management_summary.json",
        "ground_truth_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/technical output/ground_truth_match_quality.json",
        "matched_pairs_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/technical output/matched_pairs.csv",
        "entity_records_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/technical output/entity_records.csv",
        "input_jsonl_path": "/Users/simonesalvo/Developer/entityforge-core/core/output/sample_20260310_135805/sdk_probe/smoke_output/20260310_145026__smoke3/technical output/input_normalized.jsonl"
      }
    }
  ],
  "summary": {
    "runs_total": 1,
    "quality_runs_total": 0,
    "successful_runs": 1,
    "failed_runs": 0,
    "incomplete_runs": 0,
    "latest_run_id": "20260310_145026__smoke3",
    "avg_pair_precision_pct": null,
    "avg_pair_recall_pct": null,
    "records_input_total": 0,
    "matched_pairs_total": 0
  }
};

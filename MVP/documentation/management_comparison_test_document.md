# Management Comparison Test Document

## Purpose
This document explains the **indirect tests** performed through the dashboard comparison between:
- **Our baseline matching** (IPG-based grouping)
- **Their engine output** (external matching engine)

The goal is to show management that each KPI is part of a concrete validation test, not just a standalone number.

## Comparison Scope
Each selected output run compares two metric blocks:
- **Our Metrics**: baseline behavior from our known labels
- **Their Metrics**: behavior of the matching engine under test

When `Select all output (aggregate)` is used, values are computed as totals over all successful runs, and percentages are recomputed from summed numerators/denominators.

## Indirect Test Matrix

| Test ID | Indirect test name | Metrics used | Formula (from dashboard fields) | What it validates | Management interpretation |
|---|---|---|---|---|---|
| T1 | Input volume integrity | `Input Records` | `records_input` | Dataset size loaded for the run | Confirms run scale and prevents wrong-volume comparisons |
| T2 | Pair generation pressure | `Matched Pairs` (Our vs Their) | `our_true_positive` vs `matched_pairs` | How many pair relationships each side produces | Higher pair volume can mean stronger discovery or more noise |
| T3 | Entity consolidation behavior | `Entities` (Our vs Their) | `our_resolved_entities` vs `resolved_entities` | How aggressively records are grouped into entities | Big gaps indicate different clustering strategy |
| T4 | Their precision test | `Their Match Found` | `pair_precision_pct = true_positive / (true_positive + false_positive)` | Correctness of predicted pairs | High value = fewer wrong links among predicted matches |
| T5 | Our baseline recall test | `Our Match Found` | `our_match_coverage_pct = our_true_positive / our_true_pairs_total` | Coverage of true pairs by our baseline | Baseline reference for discovery delta |
| T6 | Missed-match risk test | `Miss-Matched` (Our/Their) | `100 - Match Found` | Share of true relationships not captured | High value = hidden-risk relationships left unmatched |
| T7 | False positive load test | `False Positive` (Our/Their) | `our_false_positive` and `false_positive` | Absolute volume of incorrect links | Measures operational cleanup burden |
| T8 | False negative load test | `False Negative` (Our/Their) | `our_false_negative` and `false_negative` | Absolute volume of missed true links | Measures missed-opportunity risk |
| T9 | Their noise rate test | `False Positive %` | `overall_false_positive_pct = false_positive / predicted_pairs_labeled` | Relative noise among predicted pairs | Makes runs comparable even at different volumes |
| T10 | Incremental discovery test | `Extra Pairs` | `extra_true_matches_found` | Additional true pairs found beyond baseline known pairs | Direct incremental value of engine output |
| T11 | Relative gain test | `Match Gain` | `extra_gain_vs_known_pct = extra_true_matches_found / known_pairs_ipg` | Extra discovery normalized by baseline known pairs | Business-friendly uplift indicator |
| T12 | Distribution sanity test | `Entity Size Distribution` chart | `entity_size_distribution` | Shape of entity sizes (singletons vs large clusters) | Detects over-merging or under-merging patterns |

## Core KPI Definitions Used in the Comparison

- **True Positive (TP)**: predicted pair that is truly a match in ground truth.
- **False Positive (FP)**: predicted pair that is not a true match.
- **False Negative (FN)**: true pair not found by the method.
- **Their Match Found**: precision-oriented quality indicator (`TP / (TP + FP)`).
- **Our Match Found**: baseline recall-oriented indicator (`Our TP / All true pairs in baseline scope`).
- **Miss-Matched**: complement of match found (`100 - Match Found`).

## How to Explain This to Management

Use this narrative:

1. We run the same dataset through both approaches (our baseline and their engine).
2. We compare quality and risk using the same confusion-matrix logic (TP/FP/FN).
3. We quantify incremental value with `Extra Pairs` and `Match Gain`.
4. We verify behavior consistency with entity and size distributions.
5. We can inspect each run individually or all runs together in aggregate.

## Reproducibility and Auditability

Values shown in the dashboard are derived from run artifacts in:
- `MVP/output/<run_id>/technical output/ground_truth_match_quality.json`
- `MVP/output/<run_id>/technical output/matched_pairs.csv`
- `MVP/output/<run_id>/technical output/entity_records.csv`
- `MVP/output/<run_id>/technical output/input_normalized.jsonl`

The validation page (`metrics_validation_guide.html`) already provides manual cross-check instructions per run.

## Practical Limitations (Important)

- Precision and recall are not interchangeable; both must be read together.
- Aggregate percentages are weighted by totals, not simple averages of run percentages.
- A higher matched-pairs count is not always better unless FP and FP% stay under control.

## Recommended Use in Executive Reporting

For each reporting cycle, present:
- Aggregate view (`Select all output`) for total impact
- Top 3 best runs and top 3 worst runs by `Match Gain`
- Risk panel: `False Positive %` + `Miss-Matched`
- Value panel: `Extra Pairs` + `Match Gain`

This keeps decision-making focused on both **quality risk** and **business uplift**.

# Executed Test Matrix

Reference: `20261026T064618Z`. These are recorded outcomes, not prefilled targets.

## Automated Cases

| # | Case | Result |
|---|---|---|
| 1 | `test_ambiguous_worksheet_is_rejected` | PASS |
| 2 | `test_project_filters_are_applied` | PASS |
| 3 | `test_validate_relative_path_rejects_destination_override[http://169.254.169.254/latest/meta-data]` | PASS |
| 4 | `test_validate_relative_path_rejects_destination_override[https://localhost/admin]` | PASS |
| 5 | `test_validate_relative_path_rejects_destination_override[//127.0.0.1/admin]` | PASS |
| 6 | `test_validate_relative_path_rejects_destination_override[/absolute/path]` | PASS |
| 7 | `test_validate_relative_path_rejects_destination_override[../admin]` | PASS |
| 8 | `test_validate_relative_path_rejects_destination_override[datasets/../../admin]` | PASS |
| 9 | `test_validate_relative_path_rejects_destination_override[%2e%2e/admin]` | PASS |
| 10 | `test_validate_relative_path_rejects_destination_override[%252e%252e/admin]` | PASS |
| 11 | `test_validate_relative_path_rejects_destination_override[%2f%2f127.0.0.1/admin]` | PASS |
| 12 | `test_validate_relative_path_rejects_destination_override[datasets?target=http://127.0.0.1]` | PASS |
| 13 | `test_validate_relative_path_rejects_destination_override[datasets#fragment]` | PASS |
| 14 | `test_validate_relative_path_rejects_destination_override[\\\\127.0.0.1\\admin]` | PASS |
| 15 | `test_validate_relative_path_rejects_destination_override[]` | PASS |
| 16 | `test_validate_relative_path_accepts_expected_api_path` | PASS |
| 17 | `test_fetch_json_uses_fixed_origin_and_safe_client_policy` | PASS |
| 18 | `test_fetch_json_does_not_send_rejected_path` | PASS |
| 19 | `test_upstream_error_does_not_expose_sensitive_response` | PASS |
| 20 | `test_invalid_json_is_sanitized` | PASS |
| 21 | `test_nonfinite_values_are_not_numbers[NaN]` | PASS |
| 22 | `test_nonfinite_values_are_not_numbers[Infinity]` | PASS |
| 23 | `test_nonfinite_values_are_not_numbers[-Infinity]` | PASS |
| 24 | `test_nonfinite_values_are_not_numbers[None]` | PASS |
| 25 | `test_nonfinite_values_are_not_numbers[]` | PASS |
| 26 | `test_invalid_inputs_return_errors[get_cost_share_anomalies-args0]` | PASS |
| 27 | `test_invalid_inputs_return_errors[get_cost_share_anomalies-args1]` | PASS |
| 28 | `test_invalid_inputs_return_errors[get_cost_share_anomalies-args2]` | PASS |
| 29 | `test_invalid_inputs_return_errors[get_cost_share_anomalies-args3]` | PASS |
| 30 | `test_invalid_inputs_return_errors[get_cost_share_anomalies-args4]` | PASS |
| 31 | `test_invalid_inputs_return_errors[find_repeated_worksheets-args5]` | PASS |
| 32 | `test_invalid_inputs_return_errors[find_repeated_worksheets-args6]` | PASS |
| 33 | `test_invalid_inputs_return_errors[find_repeated_worksheets-args7]` | PASS |
| 34 | `test_invalid_inputs_return_errors[detect_category_outliers-args8]` | PASS |
| 35 | `test_invalid_inputs_return_errors[detect_category_outliers-args9]` | PASS |
| 36 | `test_invalid_inputs_return_errors[detect_category_outliers-args10]` | PASS |
| 37 | `test_invalid_inputs_return_errors[generate_evidence_brief-args11]` | PASS |
| 38 | `test_repeats_do_not_merge_disasters_and_keep_state_filter` | PASS |
| 39 | `test_cost_share_ignores_nonfinite_and_ineligible_rows` | PASS |
| 40 | `test_repeated_positive_group_exposes_evidence_identifiers` | PASS |
| 41 | `test_server_is_importable` | PASS |
| 42 | `test_server_has_name` | PASS |
| 43 | `test_default_transport_is_stdio` | PASS |
| 44 | `test_tools_register_without_error` | PASS |
| 45 | `test_prompts_register_without_error` | PASS |
| 46 | `test_resources_register_without_error` | PASS |
| 47 | `test_routes_register_without_error` | PASS |
| 48 | `test_all_five_tools_discoverable` | PASS |
| 49 | `test_provenance_resource_registered` | PASS |
| 50 | `test_browser_page_has_real_review_form` | PASS |
| 51 | `test_cross_origin_review_is_rejected` | PASS |
| 52 | `test_review_returns_actual_backend_result` | PASS |

## Model First-Tool Cases

| # | Question | Expected | Selected | Result |
|---|---|---|---|---|
| 1 | Which Florida projects have federal shares outside the screening band? | `get_cost_share_anomalies` | `get_cost_share_anomalies` | PASS |
| 2 | Screen Texas obligations above $100000 for unusual federal-share ratios. | `get_cost_share_anomalies` | `get_cost_share_anomalies` | PASS |
| 3 | Check FL disaster 4734 cost share against a 0.70 to 0.95 band. | `get_cost_share_anomalies` | `get_cost_share_anomalies` | PASS |
| 4 | Find repeated project titles for the same applicant in Florida disaster 4673. | `find_repeated_worksheets` | `find_repeated_worksheets` | PASS |
| 5 | Look for potential fragmentation patterns in Louisiana worksheets. | `find_repeated_worksheets` | `find_repeated_worksheets` | PASS |
| 6 | Find applicants with at least three matching worksheets in Texas. | `find_repeated_worksheets` | `find_repeated_worksheets` | PASS |
| 7 | Which Florida Category C projects are at least three standard deviations above the mean? | `detect_category_outliers` | `detect_category_outliers` | PASS |
| 8 | Screen Category G project costs in Texas for statistical outliers. | `detect_category_outliers` | `detect_category_outliers` | PASS |
| 9 | Identify unusually large roads and bridges costs within Florida disaster 4673. | `detect_category_outliers` | `detect_category_outliers` | PASS |
| 10 | Explain how the cost-share review indicator is calculated, including its limitations. | `explain_risk_indicator` | `explain_risk_indicator` | PASS |
| 11 | Describe the methodology behind the repeated worksheet review indicator. | `explain_risk_indicator` | `explain_risk_indicator` | PASS |
| 12 | Explain the category cost outlier formula and thresholds. | `explain_risk_indicator` | `explain_risk_indicator` | PASS |
| 13 | Prepare an evidence brief for worksheet 169, disaster 4734, applicant 123-0BE2A-00, under cost_share_anomaly. | `generate_evidence_brief` | `generate_evidence_brief` | PASS |
| 14 | Package source records and limitations for worksheet 169 in disaster 4734, applicant 123-0BE2A-00, for human cost-share review. | `generate_evidence_brief` | `generate_evidence_brief` | PASS |
| 15 | Generate an analyst evidence brief, not a finding, for FL worksheet 169, disaster 4734, applicant 123-0BE2A-00, using cost_share_anomaly. | `generate_evidence_brief` | `generate_evidence_brief` | PASS |

## Other Checks

| Check | Outcome |
|---|---|
| pytest | PASS |
| ruff | PASS |
| cost_share_sqlite_control | PASS |
| repeated_sqlite_control | PASS |
| category_sqlite_control | PASS |
| get_cost_share_anomalies_live | PASS |
| find_repeated_worksheets_live | PASS |
| detect_category_outliers_live | PASS |
| explanation_schema | PASS |
| evidence_identity | PASS |

First-tool scoring does not score arguments or answers. Workflow completion is separate from narrative quality. See `NARRATIVE_QUALITY_REVIEW.md`. The full source snapshots and control membership sets remain in the reference folder.
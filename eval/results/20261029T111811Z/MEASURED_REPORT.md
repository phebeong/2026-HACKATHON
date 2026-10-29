# Measured Databricks Evaluation

Run: 20261029T111811Z
Source SHA-256: f70d0a80f54a3e69113fca8755d305828d87263db9e882089b879c5307cd645c

## Functional checks

| Check | Pass |
|---|---|
| pytest | True |
| ruff | True |
| cost_share_sqlite_control | True |
| repeated_sqlite_control | True |
| category_sqlite_control | True |
| get_cost_share_anomalies_live | True |
| find_repeated_worksheets_live | True |
| detect_category_outliers_live | True |
| explanation_schema | True |
| evidence_identity | True |
| grounded_browser_workflows | True |

## Measured metrics

| Metric | Value |
|---|---|
| pytest_cases | 64 |
| pytest_passed | 64 |
| get_cost_share_anomalies_median_seconds | 0.3391292420000127 |
| find_repeated_worksheets_median_seconds | 0.3795638490000215 |
| detect_category_outliers_median_seconds | 0.34031727799998635 |
| tool_selection_correct | 15 |
| tool_selection_cases | 15 |
| completed_agent_workflows | 3 |
| agent_workflow_cases | 3 |
| grounded_browser_workflows_passed | 3 |
| grounded_browser_workflow_cases | 3 |

## Scope and limits

Functional tests use the actual registered FastMCP tools in process inside Databricks. Detection controls use SQLite against identical archived OpenFEMA snapshots. Live latency includes retrieval and calculation, but excludes remote MCP transport and LLM time. Tool selection measures first tool name on 15 explicit held-out questions, not general answer accuracy. Agent traces are genuine model and tool responses. No hallucination-rate or semantic correctness claim is made. Retrieved data is capped and may be incomplete. The API-backed implementation does not execute these calculations through Unity Catalog functions. Cost-share thresholds do not verify declaration authorization. Category peers are limited to the selected category and filters. Human review remains required.
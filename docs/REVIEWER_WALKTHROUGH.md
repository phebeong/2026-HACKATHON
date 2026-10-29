# Reviewer Walkthrough

## Quick Review

1. Read `SUBMISSION.md` and the revised deck.
2. Inspect `eval/results/20261029T111811Z/summary.json` and `pytest.log`.
3. Compare one `comparison_*.json` with its saved `snapshot_*.json`.
4. Read `model_tool_selection.json` and a full `agent_workflows.json` trace.
5. Read `eval/NARRATIVE_QUALITY_REVIEW.md` before interpreting completion as correctness.

## Reproduce in Databricks

Use job `67919837469456` or notebook:

`/Workspace/Users/phebe.arouni@hq.dhs.gov/2026-HACKATHON/eval/databricks/HACKATHON_VALIDATION`

The notebook installs test dependencies, restarts Python, runs actual tools and controls, archives a timestamped result folder and logs to MLflow when available. Use approved workspace compute. Runs can incur compute/model charges; the saved job is on-demand, not scheduled.

Source refreshes can change counts and timing. Compare tool and control on the same new input snapshot. Keep failed runs and diagnostics.

## Demonstration Questions

**Cost share:** Screen Florida disaster 4734 for cost-share review indicators. Prepare one project's evidence brief. Explain limitations without inventing legal citations or deciding whether the share is authorized.

**Category:** Check Florida disaster 4673 Category C projects for outliers. Explain the formula, baseline, source and limits. Do not claim a finding.

**Repeats:** Find repeated worksheets in Florida disaster 4673. Preserve a zero result and explain the grouping rule's limits.

These are demonstration prompts, not independent held-out evaluation cases.

## Direct MCP Examples

```json
{"tool":"detect_category_outliers","arguments":{"damage_category_code":"C","state_code":"FL","disaster_number":4673,"pagination":{"limit":3,"offset":0}}}
```

```json
{"tool":"generate_evidence_brief","arguments":{"pw_number":169,"disaster_number":4734,"applicant_id":"123-0BE2A-00","indicator":"cost_share_anomaly"}}
```

Connect to `https://2026h-7474654188777746.aws.databricksapps.com/mcp` using Databricks OAuth. Do not put tokens in URLs. ChatGPT's custom-client setup still needs an OAuth registration; it is not the demonstrated notebook path.

Invalid category `Z`, negative disaster numbers and ambiguous worksheet identities should return clear errors. Source-cap warnings must remain visible in summaries. Upstream failures must be sanitized.

The captioned evidence walkthrough accompanies the deck. It uses recorded evidence slides, not a continuous live screen recording. Inspect grounded_browser_workflows.json and hosted_smoke.json for the separately verified review path.

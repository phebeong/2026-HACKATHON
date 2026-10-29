# Sources and Claim Register

Prepared October 29, 2026. The revised packet does not rely on the historical deck's executive-order, legal-hallucination-rate, FRED-traffic, mitigation-rule or before/after accuracy claims.

## Primary References

| Reference | Supports | Does not establish |
|---|---|---|
| [Official GSA hackathon page](https://www.gsa.gov/super-intelligence/si-community-of-practice/events-and-training/mcp-server-and-si-agent-government-hackathon) | Track, sandbox/public-data scope, judging categories and repository/deck/evaluation deliverables; retrieved October 29, 2026 | Acceptance, endorsement, winning score or completed submission |
| [OpenFEMA dataset page](https://www.fema.gov/openfema-data-page/public-assistance-funded-projects-details-v2) | Authoritative dataset entry point | No current total-record count is asserted; this session's web reader received 403 |
| [OpenFEMA v2 API](https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails) | Actual source of archived snapshots and live responses | Official reporting, policy conclusions, or a complete population beyond source caps |
| [Databricks MCP authentication](https://docs.databricks.com/aws/en/agents/mcp-tools/authentication-networking) | OAuth and custom client requirements; reviewed October 29, 2026 | A completed ChatGPT integration |
| [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/) | Hosting framework | Production certification of this prototype |
| [MCP specification](https://modelcontextprotocol.io/specification/latest) | Protocol context | Formal conformance certification |

## Measured Project Claims

All numbers refer to `eval/results/20261029T111811Z/`.

| Claim | Direct evidence |
|---|---|
| 64 tests passed | `pytest.xml`, `pytest.log` |
| Lint passed | `ruff.log` |
| Three detection sets match SQL controls | `comparison_cost_share.json`, `comparison_repeated.json`, `comparison_category.json` |
| 15/15 expected first tools | `model_tool_selection.json` |
| Three workflows completed | `agent_workflows.json`; completion is not correctness |
| Medians 0.339 / 0.380 / 0.340 seconds | `summary.json`; three samples/tool, in-process transport |
| 238 flags / zero repeat groups / three outliers | Comparison files and archived snapshots |
| October 26 narrative failure and October 29 remediation | `eval/NARRATIVE_QUALITY_REVIEW.md` and preserved model output |

## Design Choices

The 0.70-0.95 band, $100,000 minimum, repeat count of two and three-sigma threshold are prototype settings, not FEMA eligibility rules or validated signs of misconduct. No Section 406, CEF or PAPPG eligibility engine is implemented.

The official GSA page currently lists submissions due November 20, 2026, and closing ceremony December 16, 2026, subject to change. Confirm the organizers' current instructions before submission. The packet does not assert an employer or agency endorsement for its author.

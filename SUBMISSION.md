# FEMA Evidence & Oversight Graph

**Dataset Access track | Phebe Arouni | October 29, 2026**

A five-tool MCP server that turns public FEMA Public Assistance project records into review indicators with source records, calculation methods, and explicit limits for a human analyst.

## Start Here

1. Read [the judge brief](docs/JUDGE_BRIEF.md).
2. Open [the presentation](presentation/FEMA_Evidence_Oversight_Graph.pptx).
3. Inspect [evaluation documentation](eval/evaluation_documentation.md) and its raw evidence.
4. Reproduce the scenarios using [the reviewer walkthrough](docs/REVIEWER_WALKTHROUGH.md).
5. Review [security](SECURITY.md) and [known limitations](docs/LIMITATIONS_AND_ROADMAP.md).

## Submission Links

| Item | Location |
|---|---|
| Published repository | https://github.com/phebeong/2026-HACKATHON |
| Databricks prototype | https://2026h-7474654188777746.aws.databricksapps.com |
| MCP endpoint | https://2026h-7474654188777746.aws.databricksapps.com/mcp |
| Saved validation job | https://dbc-aae0ba16-8727.cloud.databricks.com/jobs/67919837469456?o=7474654188777746 |
| MLflow reference run | https://dbc-aae0ba16-8727.cloud.databricks.com/ml/experiments/1305734463288268/runs/7445e452abfc4cd89896658d4ab7f44a?o=7474654188777746 |

Databricks links require workspace access. GitHub publication status is recorded in docs/SUBMISSION_CHECKLIST.md. Databricks reviewer access must follow the approved organizer process.

## Measured Results

Reference run: `20261029T111811Z`, inside Databricks on Python 3.12.3. Source SHA-256: `f70d0a80f54a3e69113fca8755d305828d87263db9e882089b879c5307cd645c`.

| Check | Observed result | Interpretation |
|---|---|---|
| Automated tests | 64 passed, 0 failed | Validation, security boundaries, registration, identity, rules and browser routes |
| Code lint | Pass | `ruff.log` |
| Detection/control comparisons | 3/3 exact matches | Registered MCP tools replayed over saved inputs; independent SQLite controls |
| Expected first tool selected | 15/15 questions | Small explicit question set, not general accuracy |
| Agent workflows completed | 3/3 | Completion, not narrative correctness |
| Median detection latency | 0.339 / 0.380 / 0.340 seconds | Three calls/tool, in-process MCP with live retrieval |

The cost-share, repeat and category cases used 238, 3,962 and 179 input records. They returned 238 threshold flags, zero repeated groups and three category outliers. The valid zero result is preserved.

## Implemented Scope

FastMCP runs on an authenticated Databricks App. Three deterministic screening tools are paired with two explanation/evidence tools, a provenance resource and a review prompt. Project evidence uses disaster/applicant/worksheet identity. Repeat groups include disaster identity. Responses disclose retrieval caps. A saved job archives tests, inputs, SQL controls and genuine model traces in Databricks and MLflow.

The hosted browser cost-share scenario completed successfully in a separate observed smoke test. Authenticated health and a remote MCP methodology call also passed; this is not a load or availability benchmark. The tools retrieve OpenFEMA directly. They do not execute calculations through Unity Catalog functions or the adjacent Genie space.

## Limits That Matter

This is a review prototype, not a fraud detector, eligibility engine, official financial report, Section 406/CEF validator, or payments workflow. It does not verify declaration-specific authorized shares or fully match peer projects by scale and geography.

An October 26 model answer added unsupported legal citations and misstated a ratio boundary. The October 29 browser now renders its displayed summary from structured tool evidence. Three real model-to-tool review workflows passed the new check. Tool and filter selection still require human review. [The narrative review](eval/NARRATIVE_QUALITY_REVIEW.md) preserves that finding about output quality. No zero-hallucination, retrieval-accuracy, citation-coverage or audit-savings claim is made.

## Comparison Baseline

On three archived exact-count questions repeated five times, registered tools matched the independent controls in 15/15 trials. The same model without source records or tools returned no exact counts and abstained in all 15 trials. This is a narrow data-access comparison, not general answer accuracy or a statistically independent sample. Raw responses: `eval/results/20261029T111811Z/baseline_count_comparison.json`.

## Packet Status

Included: revised deck, evaluation in Markdown/Word, an editable judge brief, design and security documents, reviewer instructions, rubric map, Q&A, submission copy, and raw evidence. A captioned evidence walkthrough accompanies the deck; see the recording status in presentation/RECORDING_KIT.md. Nothing has been submitted to the organizers by this task.

## Verified Publication

The reviewed source and packet were published in commit [f21fe97](https://github.com/phebeong/2026-HACKATHON/commit/f21fe978c49d45fdfd66aa39683b5d7ad92cda84). The published tree matches the tested release, including Python source SHA-256 f70d0a80f54a3e69113fca8755d305828d87263db9e882089b879c5307cd645c. Final organizer submission remains pending.

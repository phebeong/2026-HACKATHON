# FEMA Evidence & Oversight Graph

**Phebe Arouni | Dataset Access track | October 29, 2026**

## The Problem

Public disaster-assistance data can show where money was obligated. An analyst also needs to know what deserves a second look, which records support the question, and what the data cannot prove. An unexplained score or ungrounded search response is difficult to review.

## The Contribution

Five MCP actions screen cost-share ratios, find repeated worksheet groups, identify category cost outliers, explain the method and package a project's evidence. The workflow ties an indicator to its source and limits, with a person responsible for the outcome.

The domain value is in the contract: disaster-aware identity, same-disaster grouping, category baselines, cost-share caveats and an evidence packet that does not turn a flag into a finding. These are bounded analytical tasks, not an API endpoint renamed as a tool.

## What Works Today

FastMCP runs on an authenticated Databricks App. A saved serverless job executes registered tools, compares detection sets against independent SQLite calculations on identical inputs, and archives real model/tool traces in the workspace and MLflow.

| Evidence | Reference-run result |
|---|---|
| Automated tests | 64 passed |
| Code lint | Pass |
| Detection/control sets | 3/3 exact matches |
| Expected first tool | 15/15 questions |
| Agent workflows completed | 3/3 |
| Median detection calls | 0.339 / 0.380 / 0.340 seconds |

These are prototype-scale results, not universal accuracy. Timing includes live source retrieval but excludes remote MCP transport and model time.

## A Real Example

The Florida disaster 4673 Category C test used 179 records and returned three outliers. The independent SQL control returned the same identities. An analyst can inspect the amount, mean, sigma, source and limits. This is a reason to ask a question, not a conclusion about the project.

The repeat test returned zero groups from 3,962 records. That zero is preserved rather than replaced with an invented positive example.

## What We Learned

Correct tools do not guarantee correct prose. One recorded answer added unsupported legal citations and a ratio-band error. The raw trace is retained. The displayed browser summary now uses structured evidence rather than model prose; three real review workflows passed targeted checks. Model-selected filters still require review. Source caps and unverified declaration authorizations also limit operational use.

The reusable contribution is an evidence-first interface: constrained retrieval, explicit calculations, auditable inputs and a clear boundary between an indicator and a decision. Other grant-program integrations and audit savings are proposed, not measured.

Start with `SUBMISSION.md`; reproduce the run using `docs/REVIEWER_WALKTHROUGH.md`; inspect `eval/results/20261029T111811Z/`.

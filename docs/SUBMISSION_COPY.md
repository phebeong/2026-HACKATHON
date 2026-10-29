# Copy-Ready Submission Text

## Name and Track

FEMA Evidence & Oversight Graph | Dataset Access Server

## Short Description

Five MCP tools turn public FEMA Public Assistance project data into traceable screening indicators, methodology explanations and project evidence briefs for human review.

## Project Summary

An analyst needs more than a funding total or unexplained score. This prototype pairs three deterministic screening tools with methodology and evidence tools. Its contracts preserve disaster/applicant/worksheet identity, expose retrieval limits and distinguish indicators from findings.

The FastMCP service runs on Databricks Apps and retrieves public OpenFEMA data through a fixed-origin client. A saved Databricks job archives exact input snapshots, independent SQL comparisons, test output and real model/tool traces in the workspace and MLflow.

The reference run passed 64 tests and three detection/control comparisons. A model selected the expected first tool on 15/15 explicit questions and completed three workflows. These do not establish answer accuracy. A sampled answer introduced unsupported citations and a ratio-band error; the evidence packet retains the issue and now uses deterministic summary rendering in the browser, with targeted regression coverage.

The system is read-only. It does not detect fraud, decide eligibility, verify authorized cost shares or execute payments. Its contribution is a reviewable path from public records to calculations, evidence and human decisions.

## Links

Repository recorded in workspace: https://github.com/phebeong/2026-HACKATHON

Prototype: https://2026h-7474654188777746.aws.databricksapps.com

Evidence: `eval/results/20261029T111811Z/`; MLflow run `7445e452abfc4cd89896658d4ab7f44a`.

Verify the published commit and approved reviewer access before submitting. See presentation/RECORDING_KIT.md for the walkthrough status. No organizer submission or agency endorsement is claimed.

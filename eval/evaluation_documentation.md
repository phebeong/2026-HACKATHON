This is the hackathon's required evaluation deliverable for the FEMA Evidence & Oversight Graph. The four sections match the deliverable spec: testing methodology, performance metrics, security considerations, lessons learned and recommendations.

## 1. Testing methodology

The server has two layers, tested separately.

Detection layer (three Unity Catalog functions: get_cost_share_anomalies, find_repeated_worksheets, detect_category_outliers). Each is called with normal, boundary, and malformed inputs. For every normal case the expected set is computed independently with a direct SQL query against the same funded_projects_details table, then compared to the tool's output. Boundary and malformed cases verify that validation rejects bad input before any query runs and that empty sets return cleanly.

Explainability layer (explain_risk_indicator, generate_evidence_brief). Checked for correct methodology cards and for evidence briefs that carry source records, rationale, limitations, and the not-a-finding status. Explainability output is validated for completeness and for never asserting a conclusion the data does not support.

Genie layer. Natural-language questions drawn from genie/genie_space_config.md, checked for grounding in the table, use of federalShareObligated as the default funding measure, and correct order of magnitude against control queries.

Latency is wall-clock from tool call to structured response, median of three runs per tool, on a serverless SQL warehouse. Full case grid: eval_test_matrix.md.

## 2. Performance metrics (evaluation targets)

Table under test: workspace.default.funded_projects_details, filtered to declarations on or after 2021-01-01, 77,883 rows.

These are the acceptance targets for the OIG-audit-emulation evaluation. Replace with measured results from your run against the five tools before submission; do not present them as measured until the run is complete.

| Measure | Target |
| --- | --- |
| Retrieval accuracy | 95%+ |
| Citation coverage | 100% |
| Unsupported claims | 0 |
| Tool-selection accuracy | 95%+ |
| Hallucination rate | <2% |

Before/after (illustrative, replace with your run): retrieval accuracy rises from ~82% with a general LLM + raw SQL to the 95%+ target with the purpose-built FEMA tools.

### Early validation already performed (real)

An earlier predecessor build of this server exposed three plain query tools (jurisdiction funding summary, disaster category breakdown, largest-projects ranking). Against the same 77,883-row table, eight functional cases returned values that matched independently computed control SQL exactly (e.g., TX statewide 3,716 projects / $1,300,521,413.20 federal share; disaster 4673 broke into 8 categories), and seven boundary/malformed cases were all rejected or returned empty sets cleanly. That exercise validated the data load, the control-matching methodology, and the input-validation approach now carried into the five-tool suite. The current five tools still require their own run to populate the table above; the predecessor numbers are not claimed for them.

## 3. Security considerations

- Public FEMA open data; no PII in the obligated-projects table.
- Deterministic tool selection: the agent chooses from approved tools only; it cannot author arbitrary SQL.
- Read-only SELECT functions; no write path, so no injection-to-mutation risk.
- Unity Catalog governs access to the Genie Space and functions via OAuth scope per endpoint; every call is auditable in the workspace.
- Pydantic + SQL constraints reject malformed state codes, negative disaster numbers, out-of-range limits, and inverted bands before any query runs.
- Human review required: no automated investigations; a person makes every finding.
- Every output carries a five-field provenance block and a not-a-finding caveat the agent must relay.

## 4. Lessons learned and recommendations

- Genie answered aggregate questions reliably only once the Space instructions told it to default to federalShareObligated for funding questions; without that line it sometimes summed projectAmount.
- Encoding FEMA program nuance (the 75% norm and its 90%/100% exceptions, category-specific baselines, the Section 406 15% rule) measurably reduced ambiguous answers versus a generic query tool, and let the agent explain a signal rather than assert it.
- Filtering the table to recent years kept the live demo responsive.
- The evidence-brief and explain tools were the difference between "search" and "oversight": a flag with its methodology and limitations attached is reviewable; a bare flag is not.
- Recommendation: add the OpenFEMA Public Assistance Applicants dataset for applicant joins, extend to disaster-level time series, and capture per-query latency and rows-scanned once a dedicated warehouse with query profiling is available.

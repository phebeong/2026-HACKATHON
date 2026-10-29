# FEMA Evaluation Document

GSA MCP and AI Agent Hackathon

Evaluation of the FEMA Evidence & Oversight Graph using recorded tests, public-data snapshots, independent calculations and model/tool traces. Results describe the tested cases and do not establish general answer accuracy.

Server under test: FEMA Evidence & Oversight Graph

Evaluation framework: Databricks + MLflow; pytest and SQLite controls

Agent model: databricks-claude-haiku-4-5 (temperature 0)

Dataset: SELECTION_CASES (15 routing prompts); three archived OpenFEMA cohorts

Date: October 29, 2026 | Author: Phebe Arouni

## 1. Overview and Objectives

This evaluation tests whether the MCP server returns reproducible review indicators, selects appropriate tools and preserves the limits of its evidence. Exact results, routing, scope controls and model explanations are assessed separately. General answer correctness and out-of-domain refusal remain unmeasured.

The server exposes get_cost_share_anomalies, find_repeated_worksheets, detect_category_outliers, explain_risk_indicator and generate_evidence_brief. FastMCP provides analyst actions over public OpenFEMA records. The browser uses a bounded model/tool loop and assembles its displayed summary from structured tool results. It does not execute Unity Catalog calculations or make findings.

## 2. Testing Methodology

### Framework & reproducibility

Validation runs in Databricks on Python 3.12.3. Run 20261029T111811Z archives tests, snapshots, independent SQLite controls and real model/tool traces under eval/results/. Its summary.json records MLflow IDs. Harness and browser prompts are versioned in source. Main checks use in-process MCP; remote transport is checked separately. The command below starts the saved validation job.

```powershell
databricks jobs run-now 67919837469456 --no-wait --profile fema-hackathon
```

### Golden dataset

SELECTION_CASES contains three expected first-tool questions for each of five tools. Saved Florida cohorts cover cost-share screening for disaster 4734 (238 records), repeated worksheets for disaster 4673 (3,962), and Category C outliers for disaster 4673 (179). Independent SQLite calculations define expected counts and identities. Three browser workflows exercise the review path; 64 regression cases cover controlled boundaries. Three exact-count baseline questions run five times each.

### Evaluators (LLM-as-judge)

No LLM-as-judge evaluators were run. The following deterministic checks provide narrower evidence:

| Judge | Dimension | Labels (score) |

| --- | --- | --- |

| exact_result_match | Counts and project/group identities against independent same-input SQLite controls | match (1) / mismatch (0) |

| scope_evidence_checks | Targeted validation, identity, caveat and evidence-summary workflow checks | pass (1) / fail (0) |

Exact comparisons suit deterministic counts and identity sets. They do not score every final answer. Historical model prose was manually reviewed; general correctness and scope-adherence rates were not assigned. Browser summaries are rendered from tool evidence, while model-selected filters still require review.

### Test design rationale

Correctness and scope remain distinct failure modes. Same-input SQL controls isolate calculation errors from source refreshes. Identity, malformed-response and boundary fixtures test misleading-result risks. A valid zero-repeat cohort is retained; synthetic positive groups test grouping behavior. Routing questions were developer-authored, not independently held out.

## 3. Performance Metrics

### Metrics tracked

1. Correctness rate: general answer correctness was not scored; exact tool/control agreement and first-tool routing were measured.

2. Scope-adherence rate: not measured; targeted validation, project identity, evidence-summary mode and caveat checks were tested.

3. Operational metrics available from traces: latency, tool-call count and repeated exact-count consistency. Detection medians were 0.339, 0.380 and 0.340 seconds for cost share, repeats and category screening, respectively (three live calls each; model and remote transport excluded).

### Results

The run passed 64/64 tests and lint. All three detection/control sets matched: 238 cost-share flags, zero repeat groups and three category outliers. Expected first-tool selection was 15/15; three model workflows completed and three evidence-summary workflows passed targeted checks. On three archived count questions repeated five times, tools matched 15/15 counts; the same model without records or tools matched 0/15 and abstained in all 15. This is a narrow data-access comparison, not general accuracy or independent trials.

### Failure analysis

An October 26 answer added unsupported legal citations and said 90% was outside the 70%-95% band. The browser now displays a deterministic evidence summary, with regression tests for that failure. Correct tool selection does not prove correct arguments or policy interpretation. Authorized shares may be flagged; category outliers are not matched engineering-cost findings. Zero repeats do not establish absence of issues.

## 4. Security Considerations

### Data classification

The evaluation uses public OpenFEMA Public Assistance project records. No nonpublic agency or investigative records were introduced. Public availability does not establish absence of personal information; inspect exports and traces before sharing. These records are not FEMA's official financial reporting system.

### Scope containment as a control

The inventory is read-only and provides no arbitrary SQL or payment executor. Validation, identity checks and review caveats constrain specific risks. Human review is procedural, not a signed approval gate. No broad out-of-domain refusal benchmark was run, and no scope-adherence rate is claimed.

### Secrets & configuration

Databricks credentials use the existing SDK/App authentication configuration; no tokens belong in source or evaluation artifacts. The OpenFEMA origin is fixed in code. Relative-path validation, disabled redirects/environment proxies, timeouts, response-size limits and sanitized errors constrain outbound requests. Existing workspace permissions govern access.

### Untrusted input & prompt injection

Questions and record text are untrusted. Regression cases cover hostile text, invented citations, ratio boundaries, missing evidence and malformed upstream data. Browser summaries exclude free-form model prose. These targeted checks do not prove universal injection resistance; other clients may narrate differently.

### Transport & isolation

The prototype runs behind Databricks App authentication. Main performance measurements use in-process MCP, with artifacts retained in the workspace and MLflow. A separate authenticated smoke test passed health and a remote MCP call. One hosted browser review completed in 9.709 seconds with three calls. No load, uptime or production authorization claim follows.

## 5. Lessons Learned & Recommendations

### What worked

Archived snapshots enabled independent comparisons on identical inputs. Full model/tool traces exposed a prose failure despite correct tool results, leading to the evidence renderer. Disaster/applicant/worksheet identity prevented unrelated projects from being combined. Repeated count checks preserved abstentions and zero results rather than inventing successes. Raw evidence and hashes remain inspectable.

### Limitations

Small, developer-authored question sets; three live latency samples per detector; correlated baseline repeats; no broad final-answer or refusal score. Retrieval caps limit coverage. Declaration-specific share authority and matched peer costs are not verified. Browser summaries still depend on selected arguments. Benefits, cost savings and production readiness were not measured.

### Recommendations for hackathon participants

- Expand the golden set across disasters, categories and ambiguous identities using independently authored questions.

- Broaden the no-tool baseline under explicit information-access conditions; keep exact-count replay claims narrow.

- Repeat workflows across fresh snapshots and report variation, failures and abstentions.

- Add end-to-end adversarial, out-of-domain and injection cases beyond targeted regression fixtures.

- Measure argument correctness, grounding, cost and remote/concurrent latency alongside routing and calculation checks.

- Have domain reviewers assess failures and share authorizations. Review generated code, evaluations and indicators before use.

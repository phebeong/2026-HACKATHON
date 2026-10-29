# FEMA Evidence & Oversight Graph: Evaluation Documentation

**Phebe Arouni | Dataset Access track | October 29, 2026**

Reference run: `20261029T111811Z`. Execution: Databricks, Python 3.12.3. Model: `databricks-claude-haiku-4-5`. MLflow run: `7445e452abfc4cd89896658d4ab7f44a`; experiment: `1305734463288268`.

Source SHA-256: `f70d0a80f54a3e69113fca8755d305828d87263db9e882089b879c5307cd645c`. Evidence folder: `results/20261029T111811Z/`.

The source hash covers Python files under `src`; it does not hash every dependency, deployment setting or HTML asset. The submission lockfile was refreshed when packaging the declared Databricks SDK dependency. It is not a complete environment capture of the historical run.

## 1. Testing Methodology

### System Under Test

Five actual registered FastMCP tools execute inside Databricks. The tools retrieve OpenFEMA Public Assistance Funded Projects Details v2 through its public API. They are not Unity Catalog functions and do not query the adjacent loaded table or Genie space in this test path.

The server has three screening actions, a static methodology action and a project evidence action. The validation harness uses FastMCP's in-process client to discover and call the registered tools. This tests the actual tool implementations without duplicating their logic in an evaluation-only wrapper. It does not measure external MCP/OAuth transport.

### Layer A: Automated Regression and Security Tests

Pytest executes 64 cases covering registration, schemas, invalid arguments, outbound path restrictions, sanitized upstream errors, non-finite numeric values, project identity, repeat grouping and browser-route boundaries. XML preserves individual outcomes; the test log preserves execution output. Ruff checks production code, tests and the evaluation harness.

Tests use labeled controlled fixtures where appropriate. They do not prove source accuracy, complete boundary coverage, formal MCP conformance, or absence of security vulnerabilities. The browser-route success test mocks its backend and therefore does not certify production model permission or full browser behavior.

### Layer B: Same-Input Independent Controls

For each detection case, fetch and save the source records once. Invoke the actual registered tool with its retrieval helper patched to replay that exact snapshot. Compute expected results independently in SQLite. Compare project identity sets for ratio/category screening and group identities/counts/federal sums for repeated worksheets. Save expected and actual sets, the response envelope and raw records.

The cost-share SQL filters positive totals of at least $100,000 and ratios outside 0.70-0.95. The repeated SQL groups by disaster/applicant/title/category with count at least two. The category SQL computes a population mean and SD using aggregates and flags amounts at least three SD above the mean. All comparisons use identical records, avoiding false mismatches caused by a changing live source.

The controls verify membership under the stated rules. They do not validate the thresholds as policy, confirm all returned monetary fields or rounded z-scores independently, or establish that a flagged record is problematic.

### Layer C: Live Calls and Latency

Call each detection tool three times with its live OpenFEMA retrieval active. Record wall-clock time from MCP invocation to structured response. Check the presence of provenance/caveat fields. Separately call the methodology and evidence tools; validate methodology keys and the selected disaster/applicant/worksheet identity.

The median includes retrieval and calculation. It excludes external HTTP MCP transport, model reasoning, full browser rendering and human review. Three repetitions are a small sample, potentially affected by upstream caching; no p95, load, uptime or production SLA is inferred.

### Layer D: Model Routing and Workflows

Provide the discovered schemas to the Databricks model. For 15 explicit natural-language questions, compare the first selected tool name to the expected name. Five tool families have three questions each. Save the complete response, latency and selection. The same developer authored the question set and harness; the set is not independently held out or adversarial. Tool arguments are not scored by this metric.

Execute three genuine multi-step questions through the model and registered tools, retaining all model messages, arguments, outputs and final text. Record whether a nonempty final answer was reached. Completion is not a semantic correctness score, human acceptance score or hallucination metric.

### Layer E: Evidence Summary Workflows

The deployed browser uses a model to select registered MCP tools and arguments, then assembles the displayed summary from successful structured tool results. Free-form model narrative is not displayed as the review summary. Legal citations and arbitrary record titles cannot be introduced into that summary by model prose. The complete tool trace remains available for the analyst.

Three live questions exercise cost share with a project brief, category outliers, and repeated worksheets. Checks require the expected successful tools, deterministic summary mode and the human-review caveat. All three passed. Their end-to-end model/tool times inside the notebook were 9.850, 5.060 and 4.240 seconds. These are not measurements of browser rendering or remote HTTP transport.

Regression tests cover a model response containing invented legal authority, hostile record text, exact ratio boundaries, malformed upstream structures, missing evidence, zero results, cap disclosure and nonobject browser requests. These targeted tests address observed failure modes; they do not establish universal injection resistance or correct interpretation of every question.

### Layer F: Comparison Without Source Tools

Three independently calculated snapshot counts were compared with registered tool results and with the same Databricks model given no source records or tools. Each question ran five times at temperature zero. Expected counts came from SQLite over the archived cohorts. Tools replayed those same snapshots and matched all 15 counts. The no-tool model returned null in all 15 trials, giving zero exact-count matches and 15 abstentions.

The baseline prompts explicitly allowed abstention and did not supply source snapshots. This measures whether each path supplies these three exact counts under those conditions. It does not compare broad reasoning ability, web search, policy accuracy, novel questions or independent repeated samples. Runs were initiated locally against the Databricks model; raw questions and responses are in baseline_count_comparison.json. No unsupported percentage gain is inferred.

### Reproduction

Run `eval/databricks/HACKATHON_VALIDATION` using saved job `67919837469456`. Each execution writes a new timestamped folder. MLflow logging is best effort in the harness; verify the run/artifact IDs rather than assuming logging succeeded. The reference run has confirmed IDs above.

The harness disables workspace bytecode/cache writes using a temporary cache. Earlier failed runs remain in the workspace. Reproduce controls on the same snapshot; do not require a live dataset to match an old total.

## 2. Performance Metrics

### Observed Results

| Measure | Result | Exact scope |
|---|---|---|
| Pytest | 64 passed, 0 failed | Individual cases in `pytest.xml` |
| Ruff | Pass | `ruff.log`; not a security certification |
| Detection/control match | 3/3 exact sets | Three specified cohorts, actual registered tools with snapshot replay |
| First-tool selection | 15/15 | Explicit small question set; first name only |
| Workflow completion | 3/3 | A final answer was produced; prose not certified |
| Evidence-summary workflows | 3/3 | Expected tools, summary mode and caveat, not full semantic accuracy |
| Count baseline | Tools 15/15; no-tool model 0/15 | Three archived questions, five correlated repeats; no-tool model abstained |
| Methodology schema | Pass | Required keys checked for cost-share card |
| Evidence identity | Pass | Real worksheet 169, disaster 4734, applicant 123-0BE2A-00 |

### Cohorts and Results

| Rule | Filters / settings | Input rows | Tool result | SQL control |
|---|---|---:|---:|---:|
| Cost share | FL, disaster 4734, total at least $100,000, band 0.70-0.95 | 238 | 238 flagged projects | 238 |
| Repeated worksheets | FL, disaster 4673, same disaster/applicant/title/category, repeat count at least two | 3,962 | 0 groups | 0 |
| Category outliers | FL, disaster 4673, Category C, sigma at least three | 179 | 3 projects | 3 |

None of these snapshots reached its source cap. That does not prove unrestricted queries are complete. A valid empty repeat result is retained. Positive grouping behavior is separately tested with a labeled synthetic fixture.

The 238 cost-share flags are threshold exceptions, not confirmed unauthorized shares. Declaration authorization is not verified. A category outlier is not a matched engineering-cost determination.

### Timing

| Tool | Three live samples, seconds | Median, seconds |
|---|---|---:|
| `get_cost_share_anomalies` | 0.7734, 0.3373, 0.3391 | 0.3391 |
| `find_repeated_worksheets` | 0.9521, 0.3673, 0.3796 | 0.3796 |
| `detect_category_outliers` | 0.6954, 0.3387, 0.3403 | 0.3403 |

Use the raw `summary.json` for full precision. Do not describe these as end-to-end agent response times.

### Narrative Inspection and Unmeasured Outcomes

A manual review of the October 26 final answers identified unsupported legal citations, 'Key Finding' wording, a claim that 90% falls outside a 70-95% band, and an imprecise description of one query's filters. See `NARRATIVE_QUALITY_REVIEW.md`. The raw outputs are unedited.

General retrieval accuracy, argument correctness, citation coverage, unsupported-claim rate, hallucination rate, legal correctness, fraud-detection performance, time saved and audit outcomes were not measured. The old 82%/97% comparison, 100-question result and 3.1-second illustration are removed from current claims. Only the narrow exact-count baseline above is reported. The October 29 displayed browser summary uses deterministic evidence rendering; model-selected arguments remain an independent correctness risk.

## 3. Security Considerations

The implemented boundary is a read-only tool inventory over a fixed public-data origin, hosted behind Databricks authentication. Relative-path/decoded traversal checks, disabled redirects/proxies, sanitized upstream errors, response-size bounds and input validation reduce specific risks. Tests verify several of these boundaries; they do not establish a complete security assessment.

The model cannot author arbitrary SQL or invoke a financial executor through this inventory. The reference free-form model path can still produce misleading narrative. The displayed browser summary now excludes that prose and uses trusted methods plus structured tool values. A prompt warning is not a guarantee against injection or unsupported claims. Human review is procedural, not a technically enforced signed approval.

Public records are not a blanket guarantee of no personal information. Do not mix nonpublic investigative/applicant data into this prototype. Never include credentials in artifacts. Existing Databricks permissions, approved reviewer access and retention policies remain external controls.

The submitted runtime does not establish an agency ATO, policy compliance or production readiness. A full threat/control table and residual risks appear in `../SECURITY.md`.

## 4. Lessons Learned and Recommendations

1. **Identity is a correctness boundary.** A worksheet number alone could combine unrelated disasters. Disaster/applicant filters and explicit ambiguity rejection fix that failure mode.
2. **A complete workflow can still give an unreliable explanation.** Correct tool selection and arithmetic membership do not establish grounded policy prose. Deterministic summary rendering addresses the observed prose failure; independent filter and domain review remain necessary.
3. **A threshold is not authorization.** The cost-share screen returned every eligible record in one subset. Add authoritative declaration-specific rules before interpreting the flag as unexpected.
4. **Preserve zeros and failures.** The repeat cohort legitimately returned zero. Failed test-cache runs remain part of the development record rather than being hidden.
5. **Reproducibility needs identical inputs.** Archived snapshots make independent controls meaningful while the source refreshes.
6. **Describe the actual architecture.** This submission is API-backed FastMCP on Databricks Apps. Do not claim its calculations are governed Unity Catalog functions simply because the platform supports that option.

Priorities: source pagination, authorized-share context, better matched cohorts, independently authored/adversarial prompts, claim and argument scoring, remote-client/load checks, and independent security review. Those are acceptance gates, not completed benefits.

## Evidence Index

| Artifact | Purpose |
|---|---|
| `summary.json` | Metrics, checks, source hash and MLflow IDs |
| `pytest.xml`, `pytest.log` | Individual automated outcomes and execution output |
| `ruff.log` | Code check result |
| `snapshot_*.json` | Exact input cohorts |
| `comparison_*.json` | Expected/actual identity or group sets |
| `live_tool_responses.json` | Real source-query responses |
| `model_tool_selection.json` | Fifteen routing prompts and raw model output |
| `agent_workflows.json` | Three genuine model/tool conversation traces |
| `artifact_hashes.json` | SHA-256 evidence-file manifest |

All listed raw files are in `results/20261029T111811Z/`. The accompanying evidence walkthrough is described separately in presentation/RECORDING_KIT.md. It is not a continuous capture of the notebook run.


## Hosted verification and artifact checks

A separate authenticated smoke test returned HTTP 200 at /health, listed all five tools over the remote MCP endpoint, and successfully called the cost-share methodology tool. An observed browser review completed in 9.709 seconds with three tool calls, 238 threshold indicators, and the correct disaster/applicant/worksheet identity in one evidence brief. This single browser observation does not establish load performance or availability. See hosted_smoke.json and docs/Hosted_Demo_Verified.png.

The presentation was rendered and visually inspected; package and geometry checks passed. Word documents passed structural/accessibility checks. Visual Word rendering was unavailable because LibreOffice was not installed. The previous PDF copies are excluded from the current packet to avoid presenting stale results.

# Technical Design and Key Decisions

## Current System

Python FastMCP on Databricks Apps exposes `/mcp`, `/health`, `/version`, a browser page at `/` and same-origin `/review`. Local stdio mode remains available.

The tools retrieve OpenFEMA directly. The loaded table and Genie agent are adjacent assets, not the measured backend. Unity Catalog function execution, a separate graph orchestrator and a financial executor are not implemented in this path.

## Modules

| Module | Responsibility |
|---|---|
| `app.py`, `config.py`, `routes.py` | Construction, configuration and health/version |
| `models.py` | Parameter models, indicator enum and methodology cards |
| `utils.py` | Fixed-origin HTTP, numeric conversion, provenance and pagination |
| `tools/*.py` | One analyst action per module |
| `resources/`, `prompts/` | Dataset context and review starter |
| `analyst.py`, `web.py`, `analyst.html` | Bounded model/tool browser workflow |
| `eval/run_hackathon.py` | Tests, SQL controls, live calls, model selection and MLflow |

## Tool Contracts

| Tool | Required | Optional | Result |
|---|---|---|---|
| Cost share | `state_code` | Minimum amount, band, disaster, pagination | Flag rows, policy warning, scope and provenance |
| Repeated worksheets | None | State, disaster, repeat count, pagination | Group identities, worksheet IDs/count and federal amount |
| Category outliers | `damage_category_code` | State, disaster, sigma, pagination | Rows, category mean/SD/count and scope |
| Explain indicator | `indicator` | None | Method, formula, threshold and limits |
| Evidence brief | `pw_number`, `indicator` | Disaster and applicant | Records, rationale, limits, review status and provenance |

Use exact schema names. Pagination limits are 1-100 with nonnegative offsets. Indicators are `cost_share_anomaly`, `repeated_worksheet`, or `category_outlier`.

## Analytical Decisions

**Identity:** worksheet numbers repeat across declarations. Disaster/applicant filters and ambiguity rejection prevent unrelated projects from being silently combined.

**Repeats:** group by disaster, applicant, exact title and category. This is not fuzzy matching, version reconciliation or proof of duplicated work. Legitimate groups may exist.

**Category:** compute population mean and standard deviation of retrieved `projectAmount` values, then screen sigma against the threshold. A disaster filter narrows the baseline; project scale, geography and repair scope are not separately normalized.

**Cost share:** screen `federalShareObligated / totalObligated` for positive totals above the minimum. The ratio is an implementation-level screen, not a derived declaration-specific authorized share.

**Brief:** package selected records under the requested indicator; do not independently confirm that its trigger was met.

## Retrieval and Evidence

Queries use a fixed FEMA origin, selected fields, OData filters and source caps. Output pagination does not add source pages. Retrieval time is separate from source-update time; when the update timestamp is not retrieved, the response says so.

Exact snapshots anchor the SQL comparisons. Live API data may later change. Archived evidence contains raw inputs, expected and actual sets, test/lint output, model calls, tool responses and hashes.

## Model and Human Boundaries

Tool selection is probabilistic. The browser loop has four model turns and eight tool-call limits. It has no arbitrary SQL or financial executor. Human review is required but not technically signed off. The browser summary is rendered by grounding.py from tool evidence, without free-form model prose. The model still selects tools and filters; summaries do not certify those choices.

## Evaluation Separation

The reference job uses the actual tools via FastMCP's in-process client inside Databricks. It does not measure external HTTP/OAuth transport. Earlier remote smoke checks establish a narrower connectivity result. Do not merge these into a production reliability claim.

# FEMA Evidence & Oversight Graph (MCP)

A FEMA Public Assistance Evidence & Oversight Graph that transforms open FEMA data into traceable, explainable, analyst-ready oversight intelligence. Built on the GSA MCP hackathon template (FastMCP + uv), deployable to Databricks Apps or IBM watsonx Orchestrate. Dataset Access track.

## Framing (read first)

Every tool returns **review indicators on public aggregate data, not findings**. Nothing here detects, proves, or alleges fraud, waste, or abuse. Data is FEMA Grants Manager (FAC-Trax) data, not FEMA's official financial system, so it is not for official reporting. A human analyst makes every determination.

## Five tools, two layers

Detection (one file per tool under `src/fema_oversight/tools/`):
- `get_cost_share_anomalies` - obligations whose federal share differs from the expected pattern for comparable declarations.
- `find_repeated_worksheets` - potential fragmentation/duplication patterns across worksheets.
- `detect_category_outliers` - projects that are cost outliers relative to declaration type, category of work, and peers.

Explainability:
- `explain_risk_indicator` - the methodology, calculation, thresholds, and limitations behind an indicator.
- `generate_evidence_brief` - source records, rationale, limitations, and review caveats for one Project Worksheet.

Plus an MCP **resource** (`fema-pa://provenance`) carrying dataset provenance and field definitions, and a **prompt** (`fema_oversight_review`) that frames a disciplined, review-only analyst pass.

## Data

OpenFEMA Public Assistance Funded Projects Details (v2): 849,167 obligated Project Worksheets, public, no API key, daily refresh. The tools call it through the template's hardened HTTP helper (fixed origin, relative-path validation, redirects and env proxies disabled, sanitized errors). Source: https://www.fema.gov/openfema-data-page/public-assistance-funded-projects-details-v2

## Run it

```bash
cp .env.example .env
uv sync
uv run python main.py            # stdio for local clients
uv sync --group dev
uv run pytest tests/ -v          # smoke + security tests
uv run ruff check .
```

HTTP mode (for cloud): `MCP_TRANSPORT=streamable-http uv run python main.py`, then `curl http://localhost:8000/health`.

## The directed oversight graph

Analyst question -> retrieve FEMA records -> risk-analysis agent (the three detection tools) -> evidence validation -> human analyst review -> oversight brief. Agents surface indicators; control returns to a human at a governed checkpoint. See `presentation/` for the deck and the diagram.

## Deploy

`deploy/databricks/` (Databricks Apps) and `deploy/ibm/` (watsonx Orchestrate: local toolkit, Code Engine build-from-Git, prebuilt image). Both read the same server code; `app.py` serves HTTP when the platform injects a port.

## Evaluation

`eval/` holds the methodology, the test matrix for all five tools, and the OIG-audit-emulation targets. The metric numbers are TARGETS until you run the suite against your loaded data; only the predecessor 3-tool build has measured results (documented as early validation). Do not present targets as measured.

## Compliance alignment

Supports EO 14249 (fraud/waste/abuse), EO 14395 (Task Force to Eliminate Fraud, SLTT programs), the OPEN Government Data Act, EO 13960 (trustworthy AI), and OMB M-25-21 / M-25-32. See `SOURCES.md`.

## License

MIT (see `LICENSE`). US federal government works are public domain under 17 USC 105.

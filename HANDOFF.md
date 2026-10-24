# Project handoff — FEMA Evidence & Oversight Graph (GSA MCP Hackathon)

Written for a new AI assistant taking over this work cold. Read this top to bottom; it captures the goal, every decision, what exists, what is half-done, and the hard rules the user holds you to. Nothing here needs re-deriving.

## 1. The user and the goal

- User: a GSA employee (Enterprise Portfolio Strategy Division), building a submission for the **GSA Model Context Protocol (MCP) Server and AI Agent Government Hackathon**, Sept-Nov 2026, closing ceremony Dec 16, 2026. Virtual. Hosted by GSA; industry partners Databricks, OpenAI, IBM.
- Device: Windows desktop ("SnapdragonIdeaP"). The ONE writable local folder is `C:\1 DHS\Raw`. Timezone America/New_York.
- Track chosen: **Dataset Access Server** (they considered Service Write, then rejected it as too much work).
- Judging criteria (4): Technical Quality, Innovation, Mission Alignment, Presentation. The kickoff added that submissions need: GitHub repo, slide deck, **evaluation documentation**, and a short **video demo**. Deck sections judges expect: problem, solution, technical approach, demo, security framework, lessons learned.
- Organizers' repeated theme: domain expertise baked into the server beats a thin API wrapper. They explicitly warned against "point a coding agent at an API doc and go." A prior pilot hit 95% retrieval and they called it "not quite government standard," so eval rigor matters.

## 2. The concept (final, settled)

**"A FEMA Public Assistance Evidence & Oversight Graph that transforms open FEMA data into traceable, explainable, analyst-ready oversight intelligence."**

- Data: OpenFEMA **Public Assistance Funded Projects Details v2** — 849,167 obligated Project Worksheets (PWs), public, no API key, daily refresh, sourced from FEMA Grants Manager (FAC-Trax), NOT FEMA's official financial system, NOT for official reporting. Endpoint: `https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails`.
- Five MCP tools in two layers:
  - Detection: `get_cost_share_anomalies`, `find_repeated_worksheets`, `detect_category_outliers`
  - Explainability: `explain_risk_indicator`, `generate_evidence_brief`
- Wrapped in a **directed oversight graph**: Analyst Question → Retrieve → Risk Analysis Agent (3 checks) → Evidence Validation → Human Analyst Review → Oversight Brief. Agents surface indicators; a human makes every finding.
- Backbone: Databricks managed MCP (Genie + Unity Catalog functions), governed and audited, read-only, public data only.
- Future-work idea the user loves: the "bazooka-less grant issuer" — a 3-node zero-trust graph (Node 1 read-only eligibility LLM with NO financial keys; Node 2 programmatic human-approval pause via Jira webhook; Node 3 deterministic executor pulls the payment key from Databricks Secrets at runtime, no LLM). Bank-vault analogy: the front-desk clerk never holds the safe combination.

## 3. NON-NEGOTIABLE rules the user enforces (break these and you fail them)

1. **Never fabricate numbers.** The evaluation metrics (100 questions, 97% retrieval, 82%→97%, 3.1s, etc.) are TARGETS, not measured results. They MUST stay labeled as targets until the user runs the real eval against the five tools in their Databricks workspace. The only REAL measured results so far were on an earlier 3-tool predecessor build (8/8 functional cases matched control SQL exactly: e.g. TX statewide 3,716 projects / $1,300,521,413.20 federal share; disaster 4673 = 8 categories / 3,932 projects; 7/7 boundary cases clean; ~1.2-3.5s). Those are preserved as "early validation" and explicitly NOT claimed for the 5 tools.
2. **Never fake a demo.** The winning video is the user's real live screen recording. Do not stage or simulate agent output. A faked demo is disqualifying before federal judges.
3. **FEMA-aware language, always.** "Review indicators," never "findings." Never state/imply fraud, waste, or abuse. Cost share "differs from expected patterns for comparable declarations," not "off 75%." Outliers "relative to declaration type, category, and peer projects." Duplicates are "potential fragmentation patterns." These exact reframings came from the user and matter to SME judges.
4. **Verify facts before asserting** — especially EO numbers, FEMA rules, dataset schema. The user caught value in this repeatedly.
5. **Writing style:** no em dashes, no "—", no single-Unicode-ellipsis, avoid AI-isms (delve, realm, tapestry, robust, holistic, synthesize, etc.), vary sentence length, contractions, direct and opinionated. Price-conscious when relevant.
6. **Honesty over polish.** The user repeatedly rewards flagging a gap (stale eval, unmeasured number, file lock) over quietly papering it.

## 4. Verified facts (safe to reuse, with sources)

- PA categories of work A-G: A Debris Removal, B Emergency Protective Measures (A-B = Emergency Work), C Roads/Bridges, D Water Control, E Buildings/Equipment, F Utilities, G Parks/Recreational/Other (C-G = Permanent Work). Source: FEMA Work Eligibility Matrix.
- Federal cost share: minimum 75%, some declarations 90%/100% by law. Source: FEMA PA Hazard Mitigation page; CRS.
- Section 406 mitigation "15% rule": mitigation cost-effective if <= 15% of eligible repair cost. Source: FEMA IS-1014; Stafford Act 406(e), 44 C.F.R. 206.226(e).
- Governing law: Robert T. Stafford Disaster Relief and Emergency Assistance Act. Policy: PAPPG v5 (June 2024).
- LLM legal/regulatory hallucination 17-33% (Stanford RegLab, Magesh et al. 2024). Use THIS, not a fabricated FEMA-specific rate.
- Executive orders / mandates it aligns with (verified): **EO 14249** (Protecting America's Bank Account Against Fraud, Waste, and Abuse — the fraud one; do NOT confuse with EO 14247, a separate payments-modernization order), **EO 14395** (Task Force to Eliminate Fraud; covers SLTT-administered programs = PA's structure), **OPEN Government Data Act** (Evidence Act of 2018, P.L. 115-435), **EO 13960** (trustworthy AI), **OMB M-25-21** and **M-25-32**.
- FRED/NextGov article: ~half of FRED traffic is now AI agents; built an MCP connector. The "agents are the audience, make the trusted path the easy path, provenance travels with the data" framing.
- Prefect "Loops vs. graphs": directed agentic graphs, capability set at the node, control vs. autonomy.

## 5. What EXISTS on disk

### Workspace: `workspace/artifacts/`
- **`fema-pa-mcp/`** — the FIRST complete repo (ad-hoc structure). Reconciled to 5 tools. Contains README, SUBMISSION.md, SUBMISSION_CHECKLIST.md, SOURCES.md, demo_video_script.md, sql/register_functions.sql (3 detection UC functions), src/tools.py (5 Pydantic contracts), src/resources.py, src/agent.py, notebooks/load_fema_pa.py, genie/genie_space_config.md, eval/ (evaluation_documentation.md + .docx + eval_test_matrix.md), presentation/ (the deck + walkthrough.mp4 + RECORDING_KIT.md).
- **`fema-oversight-mcp/`** — the SECOND repo, IN PROGRESS, built on the official attached template (`mcp-hackathon-template-main.zip`). This is the better structure (FastMCP, one-tool-per-file, deploy kits, tests, server.json). STATUS: all 5 tools written and parsing, resources + prompts + app.py + config + models + utils done, package renamed example_server→fema_oversight, all 19 py files parse, no stale refs. SEE SECTION 6 for what remains.
- `fema_evidence_oversight_graph.pptx` — the CURRENT deck, 20 slides, the "2.pptx" look (dark navy covers, blue kickers, FEMA-fluent). This is the one to submit. Has clickable source + EO links.
- `fema-evidence-oversight-graph-SUBMISSION.zip` — bundle of fema-pa-mcp (pre-template-rebuild).
- Older deck versions fema_pa_mcp.pptx and .versions/ snapshots — historical, ignore.

### Local device: `C:\1 DHS\Raw\`
- FEMA_Evidence_Oversight_Graph.pptx, _v2, _v3, _v4, _v5 (v5 = newest 20-slide = current), walkthrough.mp4, the SUBMISSION zip. User should submit from v5 / the zip. Older ones are safe to delete once closed in PowerPoint.

## 6. IN-PROGRESS: finishing the template-based repo (`fema-oversight-mcp/`)

This rebuild was underway when the handoff was requested. Done: package rename, config.py, models.py (incl. INDICATOR_METHODOLOGY cards + IndicatorType + PaginationParams), utils.py (OpenFEMA fetch_json with the template's security model + fetch_pa_records + provenance_block + paginate + to_float + odata_quote), all 5 tool files, tools/__init__.py aggregator, resources/provenance.py (+ aggregator), prompts/oversight_review.py (+ aggregator), app.py, routes.py (version/health). All parse.

**REMAINING to finish this repo:**
1. Update `tests/test_server.py` and `tests/test_http_security.py` — they still import/assert the example tool names. Point them at the 5 FEMA tools (import the package, assert the tools register).
2. `server.json` and `manifest.yaml` — update name/description/routes from the example coordinates to fema-oversight (find/replace already did package names; confirm the human-readable fields).
3. Add FEMA content docs into this repo: copy SOURCES.md, the eval docs, the deck, demo_video_script.md, RECORDING_KIT.md from `fema-pa-mcp/` (they are tool-name-current at 5 tools).
4. Decide: is `fema-oversight-mcp` (template-based, HTTP/FastMCP, deployable to Databricks Apps or IBM) the PRIMARY submission, with the Databricks Genie/UC-function approach (`fema-pa-mcp`) as the alternative? The user has not explicitly chosen. ASK. The template repo is the stronger GitHub deliverable; the Genie/UC-function design is the stronger "governed Databricks backbone" story. They can coexist (custom MCP server that ALSO exposes the managed-MCP approach), but confirm with the user.
5. Verify it runs: `uv sync && uv run pytest tests/ -v && uv run ruff check .` then `uv run python main.py`. The user must do this in their environment (uv + network to OpenFEMA); the sandbox here cannot run uv or reach the network.
6. Re-zip once reconciled.

## 7. Open items the USER must do (cannot be done for them)

- Run the 5-tool evaluation in their Databricks workspace; replace TARGET numbers with measured ones; only then present them as measured.
- Record the 2-minute live demo (script: `demo_video_script.md`; shot-by-shot: `RECORDING_KIT.md`).
- Fill `[your name / agency]` placeholders (deck cover, LICENSE, SUBMISSION.md).
- Confirm their Databricks workspace has Genie + Unity Catalog; load the table via `notebooks/load_fema_pa.py`; register tools; build the Genie Space from `genie/genie_space_config.md`.
- Push the repo to GitHub; confirm MCP endpoint URLs.
- Optional: add voiceover audio to the walkthrough (user has no TTS from the assistant; they record their voice, then it can be muxed in).

## 8. Environment / tooling notes for the new AI

- PPTX built with pptxgenjs via a template.js under `artifacts/.metadata/<deck>.pptx/template.js`; edit that then re-run with run_javascript; validate with file_get_pages_raster + file_read_image. Fonts are Lato (user was offered Calibri for universal rendering; not yet switched).
- Sandbox limits hit this session: no `subprocess`, no `importlib.util`, no `sys.path` writes, ffmpeg has NO libx264 and blocks the concat demuxer — use `libopenh264` + a flattened frame sequence (how the walkthrough.mp4 was built). The pptx_inspect module isn't importable in some sandbox instances; rely on the raster render for visual QA.
- To put a file on the user's machine: copy to `/outposts/SnapdragonIdeaP/C:/1 DHS/Raw/...` then open with the device open-file tool using the NATIVE path `C:\1 DHS\Raw\...`. If a copy fails with Permission denied, the file is open in PowerPoint — save under a new name or ask them to close it.
- Decision cards: the user responds well to them; offer concrete next steps, one card per message.

## 9. One-paragraph brief (paste to a fresh model)

You're helping a GSA employee win the GSA MCP Hackathon with a "FEMA Public Assistance Evidence & Oversight Graph": an MCP server over the public OpenFEMA Public Assistance dataset (849k obligated project worksheets) that surfaces review indicators (cost-share anomalies, fragmentation patterns, category cost outliers) and explains them (methodology card + evidence brief), inside a directed graph where a human makes every finding. Five tools, two layers, governed by Databricks Unity Catalog, read-only, public data only. Two repos exist: `fema-pa-mcp` (complete, Genie/UC-function approach) and `fema-oversight-mcp` (in progress, built on the official FastMCP hackathon template — finish its tests, manifest, and content docs, then confirm with the user which is the primary submission). The 20-slide deck `fema_evidence_oversight_graph.pptx` is current. HARD RULES: never fabricate eval numbers (they're targets until the user runs them; only the 3-tool predecessor has real 8/8 results), never fake the demo, always say "review indicators" not "findings," verify FEMA facts and EO numbers (EO 14249 is fraud, not 14247), no em dashes, flag gaps honestly.
\n\n> DECISION (2026-10-24): the user chose **`fema-oversight-mcp`** (the template-based FastMCP repo) as the PRIMARY submission. `fema-pa-mcp` is the documented alternative. Item 4 in section 6 is resolved.\n\n
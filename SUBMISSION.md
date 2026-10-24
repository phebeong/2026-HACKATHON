# Submission — FEMA Evidence & Oversight Graph

GSA Model Context Protocol Server and AI Agent Government Hackathon, 2026. Dataset Access track.

**This repository (`fema-oversight-mcp`) is the PRIMARY submission.** It is a FastMCP server built on the official GSA hackathon template: one tool per file, deployable to Databricks Apps or IBM watsonx Orchestrate, with tests and `server.json`. A second repository (`fema-pa-mcp`) documents the same five-tool design expressed as Databricks Genie + Unity Catalog functions; it is the managed-backbone ALTERNATIVE, not the submission.

**One line:** A FEMA Public Assistance Evidence & Oversight Graph that transforms open FEMA data into traceable, explainable, analyst-ready oversight intelligence.

## The three required deliverables
1. **GitHub repository** — this repo. Start at `README.md`; code in `src/fema_oversight/`.
2. **Presentation deck** — `presentation/FEMA_Evidence_Oversight_Graph.pptx` (20 slides, speaker notes, clickable sources + executive orders).
3. **Evaluation documentation** — `eval/evaluation_documentation.md` (+ `.docx`) and `eval/eval_test_matrix.md`.

Plus `demo_video_script.md` and `presentation/RECORDING_KIT.md` for the 2-minute video, `SOURCES.md` (claim-by-claim provenance), and `presentation/FEMA_Evidence_Oversight_Graph_walkthrough.mp4` (silent slide walkthrough).

## Five tools, two layers
Detection: `get_cost_share_anomalies`, `find_repeated_worksheets`, `detect_category_outliers`.
Explainability: `explain_risk_indicator`, `generate_evidence_brief`.
Plus the `fema-pa://provenance` resource and the `fema_oversight_review` prompt. A directed oversight graph keeps a human analyst as the decision-maker.

## Honest status (what's done vs. what you finish)
- Done: all server code (parses clean; mirrors the template's test contract), the deck, provenance, sources, methodology, test matrix, this manifest.
- You finish, in your environment: `uv sync --group dev && uv run pytest tests/ -v && uv run ruff check .`, then load data / build the Genie Space if using the Databricks path, run the eval matrix, and replace the evaluation TARGETS with measured numbers. Do not present targets as measured until then.
- Fill the `[your name / agency]` placeholders (deck cover, LICENSE, here).
- Record the 2-minute live demo (script + recording kit in this repo).

## Compliance alignment
Supports EO 14249 (fraud/waste/abuse), EO 14395 (Task Force to Eliminate Fraud, SLTT programs), the OPEN Government Data Act, EO 13960 (trustworthy AI), and OMB M-25-21 / M-25-32. See `SOURCES.md`.

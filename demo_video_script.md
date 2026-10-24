# Demo video script — FEMA Evidence & Oversight Graph

Target length: 2 minutes. Mirrors the kickoff's NIH demo: ask the same oversight question without the server (it fails), then with it (grounded, explained, caveated). Record your screen; talk over it.

---

## 0:00-0:15 — The question
On screen: your AI client, empty chat.
Say: "An oversight question a FEMA analyst asks: which Florida Public Assistance projects deserve additional review, and why? Public Assistance is normally a 75% federal share, so anything well outside the expected pattern is worth a look. First, with no special tools."

## 0:15-0:45 — Without the server (the failure)
On screen: ask it in a plain agent with only web search.
Say: "With web search alone, the agent goes to the open web. But the FEMA Public Assistance data isn't on a scrapable page, it's behind an API. So it burns through sources and can't ground an answer. Nothing an analyst could act on."

## 0:45-1:30 — With the MCP server (the win)
On screen: switch to the client with the Evidence & Oversight Graph connected. Ask the identical question.
Say: "Same question, now with the oversight server. The agent picks get_cost_share_anomalies, passes Florida, and runs a governed query against FEMA data in Unity Catalog. It comes back with review indicators, then calls generate_evidence_brief."
Point at:
- the tool names and parameters the agent chose
- the flagged rows with federal_share_ratio
- the evidence brief: source records, rationale, limitations, review status
- the _provenance block on a row: source, last-updated, methodology, caveat
Say: "Three things. It picked the right tool itself, because the tools are named for an agent. Every row carries its provenance. And every row says review indicator, not finding. The agent never accuses anyone; it points an analyst at what to check and hands over the evidence."

## 1:30-1:50 — Why the design matters
On screen: the directed oversight graph slide.
Say: "Under the hood this is a directed graph. The agent runs the checks, then control leaves the agent: evidence validation, then a human analyst review, then the brief. Governed by Unity Catalog, every call audited, all read-only."

## 1:50-2:00 — Close
Say: "Trusted oversight at the speed of a question. Review indicators, never verdicts. Thanks for watching."

---

## Prep checklist
- [ ] Table loaded, recent-years filter, so queries are fast on camera
- [ ] Both clients open: plain web-search agent, and the MCP-enabled one
- [ ] A Florida query that returns a few flagged rows (test first)
- [ ] Zoom the font up so tool calls and the provenance block are legible
- [ ] Have the directed-graph slide ready to cut to at 1:30
- [ ] One practice run to land under 2:00; trim the "without" section first if long

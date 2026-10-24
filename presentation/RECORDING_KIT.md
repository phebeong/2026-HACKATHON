# Live demo recording kit — FEMA Evidence & Oversight Graph

The goal: a 2-minute screen recording of your real agent, structured as the kickoff's winning pattern (same question fails without the server, succeeds with it). This kit gives you the storyboard, the exact click sequence, on-screen cues, and a voiceover track to read aloud. Record only real output. Never stage or fake a result.

## Before you hit record (setup)
- [ ] Table loaded and filtered to recent years (fast responses on camera).
- [ ] Two windows ready: (A) a plain LLM agent with only web search, (B) the same agent with the Evidence & Oversight Graph MCP server connected.
- [ ] A Florida cost-share query pre-tested so you KNOW it returns a few flagged rows.
- [ ] Editor/terminal font zoomed up ~150% so tool calls and the provenance block are legible at 1080p.
- [ ] Close notifications, Slack, email. Full-screen the window.
- [ ] The directed-oversight-graph slide (deck slide 7) open in a tab to cut to at 1:30.
- [ ] Screen recorder set to 1080p, 30fps, capturing system audio off / mic on.

## Storyboard (2:00 total)

| Time | On screen | You do | Voiceover (read aloud) |
|------|-----------|--------|------------------------|
| 0:00-0:15 | Window A, empty chat | Type the question, don't send yet | "An oversight analyst at FEMA asks a simple question: which Florida Public Assistance projects deserve additional review, and why? Public Assistance is normally a 75% federal share, so anything well outside the expected pattern is worth a look." |
| 0:15-0:45 | Window A runs | Send it; let it web-search and struggle | "With web search alone, the agent hits the open web. But FEMA's Public Assistance data isn't on a scrapable page, it's behind an API. So it burns through sources and never grounds an answer. Nothing an analyst could act on." |
| 0:45-1:10 | Switch to Window B | Send the identical question | "Same question, now with our Evidence and Oversight Graph connected. The agent picks get_cost_share_anomalies, passes Florida, and runs a governed query against FEMA data in Unity Catalog." |
| 1:10-1:30 | B shows rows + tool call | Cursor-point the tool name, params, flagged rows | "It returns review indicators, then calls generate_evidence_brief. Look here: the tool it chose, the parameters, and the flagged rows with their federal-share ratio." |
| 1:30-1:50 | Cut to deck slide 7, then back to B's brief | Point at the provenance block | "Under the hood this is a directed graph: the agent surfaces indicators, evidence is validated, and a human analyst makes the finding. Every row carries its source, methodology, and a clear 'review indicator, not a finding' status." |
| 1:50-2:00 | Window B, brief on screen | Hold still | "Trusted oversight at the speed of a question. Review indicators, never verdicts. Thank you." |

## Hard rules
- Show real tool output. If the live agent is flaky, record the two halves separately and stitch; do not fabricate a result.
- Keep the FEMA-aware wording: "differs from expected patterns," "warrants review," never "fraud" or "finding."
- If you run long, cut the 0:15-0:45 failure section first; it can compress to 20 seconds.

## If the live agent won't cooperate on camera
Fallback order, each still honest:
1. Record the MCP half live (the win), and narrate the failure over a single static screenshot of the exhausted web search.
2. Use the walkthrough MP4 (FEMA_Evidence_Oversight_Graph_walkthrough.mp4) as the pitch, and show one real live query inside it.
3. Submit the walkthrough MP4 as the overview and note the live demo is in the repo's screenshots.

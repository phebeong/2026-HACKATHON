# Hackathon requirements review

Reviewed October 29, 2026. This is a project readiness assessment, not an organizer ruling or a prediction of winning.

## Materials reviewed

- GSA event page, including judging criteria, deliverables, participation guidance, scope and timeline. Public deadline: November 20, 2026, subject to change. No numeric judging weights are published.
- Official GSA sample presentation and sample evaluation document. Their example results describe CDC PLACES and are not results for this project.
- Official GSA template repository: architecture, tool pattern, source safety guidance, tests, evaluation guidance and Databricks deployment instructions. The partner docs directory currently contains only its contributor notice.
- User-supplied kickoff transcript, Oct 29 at 6-24 AM.txt. It emphasizes meaningful agent actions, repeatable secure evaluation, feedback-driven improvement and a short walkthrough. It is an imperfect transcript, not an overriding instruction source.
- Existing FEMA source, submission narrative, deck, evaluation documentation, security/design notes and recorded results. Historical claims were checked against actual implementations and evidence.

## How this entry addresses judging

| Area | Evidence and improvement | Remaining boundary |
|---|---|---|
| Readability and maintainability | Separate models, one module per tool, shared retrieval, dedicated evidence renderer | Independent code review remains useful |
| Performance and reliability | 64 tests; three exact SQL controls; malformed payload rejection; fresh source snapshots and latency samples | Small cohorts and sample counts; no load benchmark |
| Agent-facing MCP design | Five user-goal tools, typed schemas, methodology resource and prompt, real model tool traces | First-tool score does not measure all arguments |
| Innovation | Combine screening with project identity, inspectable evidence and a controlled summary | No novel-statistics or policy-engine claim |
| Mission alignment | Reproducible public disaster-funding review with human accountability | Benefits and adoption are not yet measured |
| Presentation | Updated deck, worked example, evaluation, judge brief and reproducible demo prompts | Organizer portal and approved judge access must be confirmed |

## Participation and submission boundaries

Use public government data in the authenticated sandbox. Do not publicly deploy the prototype, introduce nonpublic records, or imply agency endorsement. Preserve complete documented source in the GitHub repository and provide the presentation and evaluation. The transcript additionally calls for a short video walkthrough.

Registration/eligibility, private organizer instructions and final portal requirements are administrative facts that the public materials do not prove for this entry. The public page does not provide a final submission portal. No new organizer message or final submission is sent by this work.

Sources: https://www.gsa.gov/super-intelligence/si-community-of-practice/events-and-training/mcp-server-and-si-agent-government-hackathon and https://github.com/GSA-TTS/mcp-hackathon-template

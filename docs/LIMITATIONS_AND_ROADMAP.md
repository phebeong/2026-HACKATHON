# Limitations and Roadmap

## Required Before Operational Reliance

| Gap | Consequence | Next acceptance gate |
|---|---|---|
| Model-selected filters and residual prose risk | Browser summary is now deterministic; other clients can still narrate tool results freely | Independently score arguments and external-client answers; retain human review |
| Unverified share authority | All 238 tested projects exceeded the band; legitimate shares can be returned | Join authoritative declaration/category/time-window rules and measure false positives with an SME |
| Source caps | Broad queries may be incomplete | Complete source pagination with stable identity/count checks, cancellation and backoff |
| Statistical comparability | Category means are not engineering estimates | Match project scale, scope, geography and declaration context |
| Procedural human review | Warning text is not an approval gate | Retain reviewed evidence versions and explicit reviewer decisions |

## Stronger Evaluation

- Expand the 15 explicit prompts with independently authored ambiguous/adversarial cases and questions where no tool is appropriate.
- Score arguments, claims, caveats and source links separately from first-tool choice and completion.
- Find a positive live repeat cohort if available; keep valid zeros. Positive grouping tests currently use labeled synthetic fixtures.
- Add broader pagination, boundary, cap, timeout, throttling and schema-change tests.
- Measure external MCP/OAuth and full browser latency under concurrency. Current subsecond medians are three in-process samples per tool.
- Conduct independent security review, including forwarded-host trust and request-size handling.

## Reuse

Unity Catalog-backed calculations, separate Genie integration, stable external-client OAuth and other public grant datasets are future paths. Their benefits have not been measured.

Do not claim production readiness, fraud detection, policy eligibility, legal compliance, reduced improper payments, universal retrieval accuracy or zero hallucinations. Remove the old 82%/97% comparison from current materials. The walkthrough uses recorded evidence and is labeled separately from live verification.

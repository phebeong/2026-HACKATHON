# Security Framework

## System Boundary

An authenticated Databricks sandbox retrieves public OpenFEMA records through approved tools. The tools cannot run model-generated SQL, mutate FEMA records, approve eligibility, open investigations or transfer funds. Tool annotations describe intent; platform permissions still matter.

The Databricks Apps gateway authenticates callers. The browser workflow uses the app's Databricks credentials at runtime for model access. Notebook evaluation uses its execution identity and in-process MCP; it does not require a new evaluation service principal. Credentials are not intentionally returned to the browser or written into evaluation artifacts.

## Threats and Controls

| Threat | Implemented control | Evidence | Residual risk |
|---|---|---|---|
| Arbitrary outbound destination / SSRF | Fixed FEMA origin, decoded path checks, no redirects or environment proxies | HTTP security tests | No independent penetration test |
| Upstream error leaks | Sanitized HTTP/JSON errors | Tests inject sensitive strings and check returned/logged errors | Unexpected paths need review |
| Large responses | 20,000,000-byte cap | `utils.fetch_json` implementation | Cap-specific test coverage is not claimed |
| Invalid inputs | Pydantic contracts and range checks | Invalid state, amount, disaster, category and sigma tests | State format is not complete jurisdiction enumeration |
| Non-finite numbers | NaN/infinity rejected | Numeric tests | Extreme finite values can distort statistics |
| Mixed project identities | Disaster/applicant/worksheet filters; ambiguous matches rejected | Identity regression tests | Source identity/version quality remains external |
| Cross-disaster repeat groups | Disaster in grouping key | Negative and positive fixture tests | No fuzzy matching or site linkage |
| Browser cross-origin calls | Origin/host check on `/review` | Route test | Proxy/header trust, rate limiting and body handling need further review |
| Model fabrication / injection | Fixed tools, bounded calls/turns, review-only instructions, visible evidence | Real traces and narrative review | Unsupported citations and framing errors were observed |
| Excessive autonomy | Read-only inventory, no financial executor | Tool/code review | Human sign-off remains procedural |

## Review and Evidence

Analysts must verify declaration authority and project comparability. Evidence briefs do not independently confirm the trigger. 'Human review required' is an operating rule, not an enforced approval/signature workflow.

The reference bundle retains raw snapshots, SQL comparisons, JUnit/lint output, model calls, tool responses and hashes. MLflow stores the artifacts. This supports reviewability, not a tamper-proof regulatory audit trail. Workspace permissions and retention policies still apply.

## Authentication and Data

- Keep the prototype behind Databricks authentication. Do not make it public to simplify a demo.
- Use OAuth for Databricks Apps. Browser login is not automatically an MCP client credential.
- Never put tokens in source, notebooks, URLs, screenshots or submission ZIPs. Use supported secret storage where needed.
- Public source data is not proof that every descriptive field is free of personal information. Retrieve only needed fields and do not add nonpublic applicant or investigative data.
- Figures are for prototype analysis, not official financial reporting.

No agency ATO, FedRAMP applicability, FISMA compliance, legal compliance or production readiness is asserted. Arrange reviewer access through the organizers' approved process.

## Recovery

Record the sanitized error, tool, source revision and run/deployment ID. Preserve failures. Redeploy a reviewed correction and rerun relevant checks; do not broaden permissions as a shortcut. See `docs/OPERATIONS_RUNBOOK.md`.


## October 29 controls

The browser summary now uses a deterministic renderer over structured tool results and trusted methodology cards. Model-authored narrative and source-record titles are not copied into that summary. Regression cases cover hostile record prose, invented model citations, exact ratio boundaries, absent evidence and malformed upstream structures. Tool selection and arguments remain model-controlled; other MCP clients may narrate differently. This is not a universal prompt-injection defense. The app remains authenticated.

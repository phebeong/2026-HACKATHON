# Narrative Quality Review

Reference: `results/20261026T064618Z/agent_workflows.json`. This is a manual inspection of three recorded answers, not a scored hallucination benchmark. Raw output remains unedited.

| Workflow | Strength | Observed issue | Meaning |
|---|---|---|---|
| Cost share and brief | Real figures and a warning that authorization needs context | Added statutory citations absent from tool evidence; used 'Key Finding'; said 90% and 100% lie outside 0.70-0.95 | Unsupported authority and an arithmetic/framing error. 0.90 is inside the band. The workflow did not validate the statutes. |
| Category C | Three real outliers, population-SD method and cohort limits | No independent sentence-level correctness score | Useful demonstration, not proof of universal grounding |
| Repeats | Preserved zero and the review-only caveat | Called the scope a disaster/applicant combination although no one applicant was selected; phase examples were illustrations | A correct count can still be explained imprecisely |

## Claim Boundaries

- 3/3 completed workflows is completion only.
- 15/15 first-tool names measures routing, not arguments or answers.
- No citation-coverage, hallucination-rate, legal-correctness or zero-unsupported-claims metric is reported.
- Deterministic tool data and model interpretation must be reviewed separately.

## Next Gate

Constrain legal claims to approved retrieved authorities or say authorization is unverified. Check thresholds against structured data. Validate final-response filters, identities, sources and caveats on independently authored prompts.

This review does not certify the legal citations as correct or incorrect. It establishes that they were not grounded in the available tool evidence and cannot support a performance claim.


## October 29 remediation

The historical observations above remain unchanged. The browser now displays evidence_summary from grounding.py rather than the final model prose. Targeted tests reject the observed citation/threshold failure, preserve zero results and cap limits, and reject malformed upstream data. Three real notebook review workflows passed; one hosted browser review and a remote MCP call were separately observed. No claim of universal correctness is made. See results/20261029T111811Z/.

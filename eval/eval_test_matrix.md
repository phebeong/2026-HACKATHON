# Evaluation Test Matrix — FEMA Evidence & Oversight Graph (5 tools)

Run each case against the loaded table (`workspace.default.funded_projects_details`, recent-years filter), compute the control value with a direct SQL query, then fill Actual and Pass. Do NOT pre-fill results; the numbers must come from your run.

Framing: every tool returns review indicators, not findings. A "pass" means the tool returned the statistically correct set cleanly and with its provenance block, not that any row is a confirmed problem.

## Tools under test
Detection: `get_cost_share_anomalies`, `find_repeated_worksheets`, `detect_category_outliers`
Explainability: `explain_risk_indicator`, `generate_evidence_brief`

## 1. Detection — functional cases

| # | Tool | Input | Expected | Actual | Pass? |
|---|------|-------|----------|--------|-------|
| 1 | get_cost_share_anomalies | state=FL, band 0.70-0.95 | All rows outside band; matches control SQL | | |
| 2 | get_cost_share_anomalies | state=TX, min_total_obligated=1,000,000 | Only >= $1M considered | | |
| 3 | get_cost_share_anomalies | band 0.74-0.76 | Flags everything outside the tight band | | |
| 4 | find_repeated_worksheets | state=LA, min_repeat_count=2 | Groups of >=2 same-title/category | | |
| 5 | find_repeated_worksheets | disaster_number=4673, min_repeat_count=3 | Only groups of 3+ for that disaster | | |
| 6 | detect_category_outliers | sigma_threshold=3.0 | All rows >=3 sigma above category mean | | |
| 7 | detect_category_outliers | damage_category_code=C, sigma=2.0 | Only Cat C, >=2 sigma | | |
| 8 | detect_category_outliers | state=FL, sigma=3.0 | FL-only outliers, descending by sigma | | |

## 2. Detection — boundary / error cases

| # | Tool | Input | Expected | Actual | Pass? |
|---|------|-------|----------|--------|-------|
| B1 | get_cost_share_anomalies | state="FLORIDA" | Rejected: 2-letter code only | | |
| B2 | get_cost_share_anomalies | low=0.9, high=0.8 | Rejected: high < low | | |
| B3 | get_cost_share_anomalies | state=ZZ | Valid format, empty set, no crash | | |
| B4 | find_repeated_worksheets | min_repeat_count=1 | Rejected: ge=2 | | |
| B5 | find_repeated_worksheets | disaster_number=-5 | Rejected: ge=1 | | |
| B6 | detect_category_outliers | sigma_threshold=0.5 | Rejected: ge=1.0 | | |
| B7 | detect_category_outliers | damage_category_code="AB" | Rejected: single letter | | |

## 3. Explainability cases

| # | Tool | Input | Expected | Actual | Pass? |
|---|------|-------|----------|--------|-------|
| E1 | explain_risk_indicator | cost_share_anomaly | Returns methodology, calculation, thresholds, limitations | | |
| E2 | explain_risk_indicator | repeated_worksheet | Correct card, fragmentation framing | | |
| E3 | explain_risk_indicator | category_outlier | Correct card, category-baseline framing | | |
| E4 | generate_evidence_brief | pw_number=<real>, indicator=cost_share_anomaly | Brief has source records, rationale, limitations, not-a-finding status | | |

## 4. Provenance / trust checks

| # | Check | Expected | Actual | Pass? |
|---|-------|----------|--------|-------|
| P1 | Every detection row carries _provenance | Source, last_updated, methodology, limitations, review_status present | | |
| P2 | Agent relays the review-only caveat | Answer states "not a finding" when presenting flags | | |
| P3 | Dataset resource readable | fema-pa://provenance returns source + field defs | | |

## 5. Agent-readability checks (FRED lesson)

| # | Client | Check | Expected | Actual | Pass? |
|---|--------|-------|----------|--------|-------|
| R1 | [client A] | Agent selects the right tool for a plain-language oversight question | Correct tool | | |
| R2 | [client A] | Agent credits FEMA as the source | Source cited | | |
| R3 | [client B] | Same question, different client | Correct tool + citation | | |

## 6. Performance (fill after run)

| Tool | Median latency (ms) | Rows scanned | Pass rate |
|------|--------------------|--------------|-----------|
| get_cost_share_anomalies | | | |
| find_repeated_worksheets | | | |
| detect_category_outliers | | | |
| explain_risk_indicator | | n/a (static card) | |
| generate_evidence_brief | | | |

Record table size (row count after the date filter) so latency has context.

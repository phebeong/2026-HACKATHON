# Sources & claim provenance

Every external factual claim in the deck, mapped to an authoritative source. Claims that are project design choices or unmeasured targets are listed separately and honestly, since they carry no external citation.

## A. Sourced factual claims

### "Standard LLMs hallucinate on PAPPG and Stafford Act rules"
The defensible, evidence-backed version of this claim is about specialized regulatory/legal text generally, not FEMA policy specifically (no study has measured LLM accuracy on PAPPG itself).
- Stanford RegLab / HAI, Magesh et al., "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools" (2024-25): purpose-built legal AI tools from LexisNexis and Thomson Reuters hallucinated roughly 17% to 33% of the time; general-purpose GPT-4 was worse. https://nlp.stanford.edu/~manning/papers/Magesh-Hallucination-Free-2025.pdf
- Dahl et al., "Profiling Legal Hallucinations in Large Language Models," arXiv:2401.01301 — LLM output frequently inconsistent with legal facts. https://arxiv.org/abs/2401.01301
- "How Much Do Legal RAG Systems Still Hallucinate?" arXiv:2608.14210 — even retrieval-augmented legal systems hallucinate from under 10% to nearly half of responses. https://arxiv.org/pdf/2608.14210
- Honest wording for the slide: "General and even specialized legal AI tools hallucinate on regulatory questions 17-33% of the time (Stanford RegLab, 2024), well above a government oversight bar." Do not state a FEMA-specific measured rate; none exists publicly.

### FEMA PA categories of work A-G
- FEMA Public Assistance Work Eligibility Matrix: A Debris Removal, B Emergency Protective Measures, C Roads and Bridges, D Water Control Facilities, E Buildings and Equipment, F Utilities, G Parks/Recreational/Other. https://www.fema.gov/sites/default/files/documents/fema_pda_public-assistance-work-eligibility-matrix.pdf
- FEMA "Public Assistance Grants Help Communities" fact sheet (Category A debris removal). https://www.fema.gov/fact-sheet/fema-public-assistance-grants-help-communities
- A/B are Emergency Work, C-G are Permanent Work: FEMA IS-1021 course material. https://emilms.fema.gov/is_1021/groups/98.html

### Federal cost share "typically 75%"
- FEMA Public Assistance Hazard Mitigation: federal share is a minimum of 75% of eligible costs, remainder non-federal. https://www.fema.gov/assistance/public/hazard-mitigation
- Congressional Research Service, "How FEMA Public Assistance Works" (IG10021): PA reimburses at least 75% of eligible costs under the Stafford Act. https://www.congress.gov/crs-product/IG10021
- The 90%/100% exceptions exist (e.g., small/impoverished communities up to 90% for certain mitigation): FEMA FY26 HMA fact sheet. https://www.fema.gov/sites/default/files/documents/fema_rsl_hma_fy26-pdm-cds-fact-sheet_07022026.pdf

### Section 406 mitigation and the "15% rule"
- FEMA IS-1014 benefit-cost material: a 406 mitigation measure is considered cost-effective if its cost does not exceed 15% of the total eligible repair cost of the facility. https://emilms.fema.gov/is_1014/groups/192.html
- FEMA PA Hazard Mitigation fact sheet, citing Stafford Act Section 406(e) (42 U.S.C. 5172) and 44 C.F.R. 206.226(e). https://www.fema.gov/sites/default/files/documents/fema_pa-hazard-mitigation-factsheet-feb-2024.pdf

### Stafford Act as the governing authority
- Robert T. Stafford Disaster Relief and Emergency Assistance Act, authorizing federal assistance on a presidential declaration: FEMA IS-1000. https://emilms.fema.gov/is_1000/groups/390.html

### PAPPG (Public Assistance Program and Policy Guide) exists and governs eligibility
- FEMA Public Assistance Program and Policy Guide, v5, June 2024. https://www.fema.gov/sites/default/files/documents/fema_public-assistance-program-and-policy-guide_v5_june2024.pdf

### The dataset: OpenFEMA Public Assistance Funded Projects Details (v2)
- 849,167 records, public, no API key, daily refresh, Grants Manager (FAC-Trax) source, not for official reporting. https://www.fema.gov/openfema-data-page/public-assistance-funded-projects-details-v2

### "Half of FRED's traffic is now AI agents" (framing for agents-as-audience)
- Nick Hart, "The Fed's 35-year open data bet is a model for the AI era," NextGov/GovExec, Oct 16 2026: ~half of FRED visits now come from AI agents; FRED built an MCP connector. https://www.nextgov.com/ideas/2026/10/feds-35-year-open-data-bet-model-ai-era/416658/

### MCP as the connection standard; Databricks managed MCP (Genie, UC functions, vector search)
- Databricks, "Connect agents to tools" / managed MCP servers. https://docs.databricks.com/aws/en/agents/agent-framework/agent-tool
- Databricks, custom MCP servers on Databricks Apps. https://docs.databricks.com/aws/en/agents/mcp-tools/custom-mcp

### Directed-agent-graph framing (control vs. autonomy, node-level capability)
- Prefect, "Loops vs. graphs" (Jeremiah Lowin). https://www.prefect.io/blog/loops-vs-graphs

## B. Claims that are NOT external facts (no citation — do not present as sourced)

These are design choices or program claims specific to THIS prototype. They are legitimate to assert as your own design, but a judge should not be told they are externally sourced.

- The three/five tool definitions and their thresholds (0.70-0.95 band, 3-sigma, min_repeat_count). Design choices.
- The "oversight ontology" framing. Our positioning.
- The directed oversight graph (Discovery -> Validation -> Evidence -> Human Review -> Brief). Our architecture.
- The bazooka-less grant issuer three-node design. Our proposed future work.
- Reuse to HUD/USDA/SBA/EPA/DOT. A plausibility claim, not a built integration.

## C. Unmeasured numbers — must be run before being presented as results

These appear on the evaluation slide. They are targets/illustrations until you run the eval. Do NOT present as measured.

- 100 test questions; 97% retrieval; 100% citation; 0 unsupported claims; <2% hallucination; 82% -> 97% before/after; 3.1s latency.
- The only real measured numbers to date were from the EARLIER 3-tool version (8/8 functional exact matches; ~1.2-3.5s), not the current 5-tool set. Re-run against the 5 tools, then cite your own eval artifact.


## D. Compliance authorities (executive orders & statutes)

Verified against primary sources. Note: EO 14249 is the fraud/waste/abuse order; EO 14247 is a separate payments-modernization order. Use 14249 for the fraud angle.

- EO 14249, Protecting America's Bank Account Against Fraud, Waste, and Abuse (Mar 25, 2025). https://www.whitehouse.gov/presidential-actions/2025/03/protecting-americas-bank-account-against-fraud-waste-and-abuse/
- EO 14395, Establishing the Task Force to Eliminate Fraud (Mar 2026) — covers fraud in benefit programs administered jointly with state, local, tribal, and territorial partners, which is PA's structure. White House presidential actions.
- OPEN Government Data Act, Title II of the Foundations for Evidence-Based Policymaking Act of 2018 (P.L. 115-435). https://www.congress.gov/crs-product/IF12299
- EO 13960, Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government (Dec 2020). 
- OMB M-25-21, Accelerating Federal Use of AI through Innovation, Governance, and Public Trust (2025). https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf
- OMB M-25-32, Preventing Improper Payments and Protecting Privacy Through Do Not Pay (2025).

These are alignment claims: the prototype supports the goals of these authorities. It is not a certified compliance system.

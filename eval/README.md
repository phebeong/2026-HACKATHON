# Evaluation Evidence

Read [evaluation_documentation.md](evaluation_documentation.md) first. The measured reference is `results/20261026T064618Z/`: 52 passing tests, three exact detection/control sets, 15/15 expected first-tool names, and three completed workflows.

Completion does not establish answer correctness. [Narrative-quality review](NARRATIVE_QUALITY_REVIEW.md) records observed unsupported citations, a threshold error and imprecise framing.

## Reproduce

Run Databricks notebook `eval/databricks/HACKATHON_VALIDATION`, saved job `67919837469456`. The actual harness is `run_hackathon.py`. It archives inputs and results and logs MLflow artifacts when available.

The older `eval/databricks/agent_eval_offline.py` is an alternative template requiring generated agent files and additional setup. It is not the harness used for the submitted results. Its example placeholders and sample outcomes are not project evidence.

`eval_test_matrix.md` maps the actual test cases and result files. Historical results remain separate. Do not merge predecessor numbers or targets into the current measured metrics.

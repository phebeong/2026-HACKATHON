# Recorded Databricks Validation

The submitted evaluation uses `HACKATHON_VALIDATION.py` and `../run_hackathon.py`, saved as on-demand job `67919837469456`.

It runs the actual registered tools in process, archives OpenFEMA snapshots, compares them with independent SQLite controls, runs pytest and lint, and records model/tool traces. It uses the existing notebook execution identity and model endpoint. No new service principal or secret scope is needed for this path.

Reference evidence is `../results/20261026T064618Z/`. Read `../evaluation_documentation.md` for measured scope, limitations and reproduction. Retain failed runs. Code/source hashing covers Python files under `src`, not every deployment file, dependency or HTML asset.

The optional older `agent_eval_offline.py` and service-principal setup kit are an alternative, unconfigured template. They are not the submitted harness and their example outcomes are not measured project results.

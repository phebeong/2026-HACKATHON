# Databricks Operations Runbook

| Resource | Value |
|---|---|
| Workspace | `https://dbc-aae0ba16-8727.cloud.databricks.com` |
| Source | `/Workspace/Users/phebe.arouni@hq.dhs.gov/2026-HACKATHON` |
| App | `2026h` |
| MCP / health | App URL plus `/mcp` or `/health` |
| Validation job | `67919837469456` |
| MLflow experiment | `1305734463288268` |
| Reference evidence | `eval/results/20261029T111811Z` |

## Authenticate and Inspect

```powershell
databricks auth login --host https://dbc-aae0ba16-8727.cloud.databricks.com --profile fema-hackathon
databricks current-user me --profile fema-hackathon
databricks apps get 2026h --profile fema-hackathon
```

Browser login is not a CLI profile. Workspace use and account-level OAuth administration are different permissions. Never store tokens in source.

## Rerun Validation

```powershell
databricks jobs run-now 67919837469456 --no-wait --profile fema-hackathon
databricks jobs get-run <returned-run-id> --profile fema-hackathon
```

Use the task run ID from `tasks` when retrieving multi-task output. Inspect JUnit, lint, snapshots, comparisons, summary and model traces. Completion does not establish answer correctness.

## Deploy

Review differences and back up the workspace source. Keep `app.yaml` at its root; it starts the module with `src` on `PYTHONPATH`. `DATABRICKS_APP_PORT` selects HTTP.

```powershell
databricks apps deploy 2026h --source-code-path /Workspace/Users/phebe.arouni@hq.dhs.gov/2026-HACKATHON --profile fema-hackathon
```

Check completed deployment, authenticated health and a real MCP call. Check the browser/model route separately; notebook tests do not certify it.

## Failure Guide

| Symptom | Response |
|---|---|
| Tests cannot create workspace `__pycache__` | Use the harness's temporary cache and disabled bytecode writes |
| 502 during redeploy | Inspect status/logs; wait for completed deployment |
| Model 403 | Check the executing identity's existing model access; do not make the app public |
| OAuth asks for a client ID | Authorized account admin registers the client's exact callback |
| Zero repeat groups | Inspect cohort/rule; it may be correct |
| Many 100% share flags | Verify authorization separately; band screening is not a policy decision |
| Retrieval cap reached | Narrow filters and disclose incomplete retrieval; output pagination does not fetch source pages |

## Clean Runtime Release

The October 29 deployment uses `/Workspace/Users/phebe.arouni@hq.dhs.gov/hackathon_releases/20261029`, containing runtime source, app.yaml and pinned runtime requirements. The full working repository remains under 2026-HACKATHON. A direct deployment of the full folder failed because Databricks tried to import an archived submission ZIP into the app snapshot. The prior app stayed available; the clean runtime deployment succeeded. Keep archives and evidence outside the runtime release.

## Recovery and Retention

Retain prior source/deployment IDs and failed evidence runs. Redeploy a reviewed prior snapshot through supported platform tooling. Do not delete unrelated resources or broaden permissions during recovery.

Local pre-change backup: `C:/1 DHS/Raw/databricks-backup-20261026`. This is a recovery aid, not the final submission.

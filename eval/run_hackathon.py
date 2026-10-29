"""Execute real registered MCP tools and record reproducible evaluation evidence."""

import asyncio
import contextlib
import hashlib
import json
import math
import os
import platform
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, patch

import requests
from fastmcp import Client

from fema_oversight.analyst import run_review
from fema_oversight.app import mcp
from fema_oversight.tools import (
    category_outliers,
    cost_share_anomalies,
    repeated_worksheets,
)
from fema_oversight.utils import fetch_pa_records

ROOT = Path(__file__).resolve().parents[1]
MODEL = "databricks-claude-haiku-4-5"


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")


def key(row):
    return (row.get("disaster_number"), row.get("applicant_id"), row.get("pw_number"))


async def collect(client, name, args):
    rows = []
    offset = 0
    while True:
        response = (
            await client.call_tool(
                name, {**args, "pagination": {"limit": 100, "offset": offset}}
            )
        ).data
        if "error" in response:
            raise RuntimeError(response["error"])
        rows.extend(response["items"])
        if not response["has_more"]:
            return rows, response
        offset = response["next_offset"]


def control(rows, rule):
    """Independent SQLite calculations over the identical archived input snapshot."""
    conn = sqlite3.connect(":memory:")
    conn.create_function("sqrt", 1, math.sqrt)
    conn.execute(
        (
            "CREATE TABLE pa (disaster INTEGER, applicant TEXT, pw INTEGER, "
            "title TEXT, category TEXT, amount REAL, total REAL, federal REAL)"
        )
    )
    conn.executemany(
        "INSERT INTO pa VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                r.get("disasterNumber"),
                r.get("applicantId"),
                r.get("pwNumber"),
                r.get("applicationTitle"),
                r.get("damageCategoryCode"),
                r.get("projectAmount"),
                r.get("totalObligated"),
                r.get("federalShareObligated"),
            )
            for r in rows
        ],
    )
    if rule == "cost_share":
        result = conn.execute(
            (
                "SELECT disaster, applicant, pw FROM pa WHERE total >= 100000 "
                "AND total > 0 AND federal IS NOT NULL AND (federal/total < "
                ".70 OR federal/total > .95)"
            )
        ).fetchall()
    elif rule == "repeated":
        result = conn.execute(
            (
                "SELECT disaster, applicant, title, category, COUNT(*), "
                "ROUND(SUM(COALESCE(federal,0)),2) FROM pa WHERE disaster IS "
                "NOT NULL AND applicant IS NOT NULL AND title IS NOT NULL AND "
                "category IS NOT NULL GROUP BY "
                "disaster,applicant,title,category HAVING COUNT(*) >= 2"
            )
        ).fetchall()
    else:
        result = conn.execute(
            (
                "WITH stats AS (SELECT AVG(amount) AS mean, "
                "sqrt(MAX(0,AVG(amount*amount)-AVG(amount)*AVG(amount))) AS sd "
                "FROM pa WHERE amount IS NOT NULL) SELECT "
                "disaster,applicant,pw FROM pa,stats WHERE sd > 0 AND "
                "(amount-mean)/sd >= 3"
            )
        ).fetchall()
    conn.close()
    return sorted(result, key=str)


SELECTION_CASES = [
    (
        "Which Florida projects have federal shares outside the screening band?",
        "get_cost_share_anomalies",
    ),
    (
        "Screen Texas obligations above $100000 for unusual federal-share ratios.",
        "get_cost_share_anomalies",
    ),
    (
        "Check FL disaster 4734 cost share against a 0.70 to 0.95 band.",
        "get_cost_share_anomalies",
    ),
    (
        "Find repeated project titles for the same applicant in Florida disaster 4673.",
        "find_repeated_worksheets",
    ),
    (
        "Look for potential fragmentation patterns in Louisiana worksheets.",
        "find_repeated_worksheets",
    ),
    (
        "Find applicants with at least three matching worksheets in Texas.",
        "find_repeated_worksheets",
    ),
    (
        (
            "Which Florida Category C projects are at least three standard "
            "deviations above the mean?"
        ),
        "detect_category_outliers",
    ),
    (
        "Screen Category G project costs in Texas for statistical outliers.",
        "detect_category_outliers",
    ),
    (
        (
            "Identify unusually large roads and bridges costs within Florida "
            "disaster 4673."
        ),
        "detect_category_outliers",
    ),
    (
        (
            "Explain how the cost-share review indicator is calculated, "
            "including its limitations."
        ),
        "explain_risk_indicator",
    ),
    (
        "Describe the methodology behind the repeated worksheet review indicator.",
        "explain_risk_indicator",
    ),
    (
        "Explain the category cost outlier formula and thresholds.",
        "explain_risk_indicator",
    ),
    (
        (
            "Prepare an evidence brief for worksheet 169, disaster 4734, "
            "applicant 123-0BE2A-00, under cost_share_anomaly."
        ),
        "generate_evidence_brief",
    ),
    (
        (
            "Package source records and limitations for worksheet 169 in "
            "disaster 4734, applicant 123-0BE2A-00, for human cost-share "
            "review."
        ),
        "generate_evidence_brief",
    ),
    (
        (
            "Generate an analyst evidence brief, not a finding, for FL "
            "worksheet 169, disaster 4734, applicant 123-0BE2A-00, using "
            "cost_share_anomaly."
        ),
        "generate_evidence_brief",
    ),
]


def model_call(workspace, messages, tools):
    response = requests.post(
        workspace.config.host.rstrip("/") + f"/serving-endpoints/{MODEL}/invocations",
        headers=workspace.config.authenticate(),
        json={
            "messages": messages,
            "tools": tools,
            "max_tokens": 1800,
            "temperature": 0,
        },
        timeout=120,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Model HTTP {response.status_code}: {response.text[:300]}")
    return response.json()


async def run_model_checks(client, outdir):
    from databricks.sdk import WorkspaceClient

    workspace = WorkspaceClient()
    tool_schemas = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema,
            },
        }
        for t in await client.list_tools()
    ]
    system = (
        "You are a FEMA analyst assistant. Use the provided read-only tools "
        "for data or methodology. Surface review indicators only, never infer "
        "fraud or findings. Preserve source, screening scope and limitations. "
        "Authorized cost-share exceptions can be legitimate. Use disaster and "
        "applicant identity for evidence briefs. Never invent data."
    )
    selection = []
    for question, expected in SELECTION_CASES:
        started = time.perf_counter()
        row = {"question": question, "expected_tool": expected}
        try:
            reply = model_call(
                workspace,
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                tool_schemas,
            )
            row["response"] = reply
            calls = reply["choices"][0]["message"].get("tool_calls", [])
            row["selected_tool"] = calls[0]["function"]["name"] if calls else None
            row["pass"] = row["selected_tool"] == expected
        except Exception as exc:
            row.update({"pass": False, "error": str(exc)})
        row["latency_seconds"] = round(time.perf_counter() - started, 3)
        selection.append(row)
        print(
            f"Tool selection {len(selection)}/{len(SELECTION_CASES)}: {row['pass']}",
            flush=True,
        )
    dump(outdir / "model_tool_selection.json", selection)
    conversations = []
    for question in [
        (
            "Screen Florida disaster 4734 for cost-share review indicators. "
            "Show one project's evidence brief, explaining why a 100% share "
            "does not establish wrongdoing. Include the source and dataset "
            "limits."
        ),
        (
            "Check Florida disaster 4673 Category C projects for cost "
            "outliers, explain the methodology, and state the limits. Do not "
            "claim any finding."
        ),
        (
            "Find repeated worksheets in Florida disaster 4673 and explain why "
            "repeated titles may be legitimate. Give the source and review "
            "limitations."
        ),
    ]:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ]
        trace = {"question": question, "events": [], "completed": False}
        try:
            for turn in range(6):
                reply = model_call(workspace, messages, tool_schemas)
                message = reply["choices"][0]["message"]
                messages.append(message)
                trace["events"].append({"type": "model", "response": reply})
                calls = message.get("tool_calls", [])
                if not calls:
                    trace["answer"] = message.get("content", "")
                    trace["completed"] = bool(trace["answer"])
                    break
                for call in calls:
                    args = json.loads(call["function"]["arguments"])
                    result = (
                        await client.call_tool(call["function"]["name"], args)
                    ).data
                    trace["events"].append(
                        {
                            "type": "tool",
                            "name": call["function"]["name"],
                            "arguments": args,
                            "response": result,
                        }
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "content": json.dumps(result, default=str),
                        }
                    )
        except Exception as exc:
            trace["error"] = str(exc)
        conversations.append(trace)
        print(
            f"Agent workflow {len(conversations)}/3 completed={trace['completed']}",
            flush=True,
        )
    dump(outdir / "agent_workflows.json", conversations)
    return selection, conversations


async def run():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = ROOT / "eval" / "results" / stamp
    outdir.mkdir(parents=True, exist_ok=True)
    summary = {
        "started_at": stamp,
        "python": platform.python_version(),
        "execution_host": "Databricks"
        if "DATABRICKS_RUNTIME_VERSION" in os.environ
        else platform.node(),
        "checks": [],
        "metrics": {},
    }
    env = {
        **os.environ,
        "PYTHONPATH": str(ROOT / "src"),
        "MCP_TRANSPORT": "stdio",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": tempfile.mkdtemp(prefix="fema-pycache-"),
    }
    test = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(ROOT / "tests"),
            "-q",
            "--color=no",
            "-p",
            "no:cacheprovider",
            f"--junitxml={outdir / 'pytest.xml'}",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    (outdir / "pytest.log").write_text(test.stdout + test.stderr, encoding="utf-8")
    summary["checks"].append(
        {"name": "pytest", "pass": test.returncode == 0, "exit_code": test.returncode}
    )
    print(test.stdout, flush=True)
    import xml.etree.ElementTree as ET

    test_tree = ET.parse(outdir / "pytest.xml")
    cases_xml = test_tree.findall(".//testcase")
    summary["metrics"]["pytest_cases"] = len(cases_xml)
    summary["metrics"]["pytest_passed"] = sum(
        not any(c.tag in {"failure", "error", "skipped"} for c in case)
        for case in cases_xml
    )
    lint = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "src",
            "tests",
            "eval/run_hackathon.py",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    (outdir / "ruff.log").write_text(lint.stdout + lint.stderr, encoding="utf-8")
    summary["checks"].append({"name": "ruff", "pass": lint.returncode == 0})
    cases = [
        (
            "cost_share",
            "get_cost_share_anomalies",
            cost_share_anomalies,
            {"state_code": "FL", "disaster_number": 4734},
            (
                "stateAbbreviation eq 'FL' and disasterNumber eq 4734 and "
                "totalObligated ge 100000"
            ),
            5000,
        ),
        (
            "repeated",
            "find_repeated_worksheets",
            repeated_worksheets,
            {"state_code": "FL", "disaster_number": 4673},
            "stateAbbreviation eq 'FL' and disasterNumber eq 4673",
            10000,
        ),
        (
            "category",
            "detect_category_outliers",
            category_outliers,
            {"state_code": "FL", "damage_category_code": "C", "disaster_number": 4673},
            (
                "stateAbbreviation eq 'FL' and disasterNumber eq 4673 and "
                "damageCategoryCode eq 'C'"
            ),
            10000,
        ),
    ]
    async with Client(mcp) as client:
        summary["tools"] = [t.name for t in await client.list_tools()]
        for rule, tool, module, args, flt, cap in cases:
            rows = await fetch_pa_records(odata_filter=flt, top=cap)
            dump(outdir / f"snapshot_{rule}.json", rows)
            expected = control(rows, rule)
            with patch.object(module, "fetch_pa_records", AsyncMock(return_value=rows)):
                actual_rows, envelope = await collect(client, tool, args)
            if rule == "repeated":
                actual = sorted(
                    [
                        (
                            r["disaster_number"],
                            r["applicant_id"],
                            r["application_title"],
                            next(
                                (
                                    x.get("damageCategoryCode")
                                    for x in rows
                                    if x.get("damageCategoryDescrip")
                                    == r["damage_category_description"]
                                ),
                                None,
                            ),
                            r["worksheet_count"],
                            r["total_federal_share_obligated"],
                        )
                        for r in actual_rows
                    ],
                    key=str,
                )
            else:
                actual = sorted([key(r) for r in actual_rows], key=str)
            check = {
                "name": f"{rule}_sqlite_control",
                "pass": actual == expected,
                "snapshot_rows": len(rows),
                "tool_count": len(actual),
                "control_count": len(expected),
                "record_cap": cap,
                "possibly_truncated": len(rows) >= cap,
            }
            summary["checks"].append(check)
            dump(
                outdir / f"comparison_{rule}.json",
                {
                    "summary": check,
                    "actual": actual,
                    "expected": expected,
                    "tool_response": envelope,
                },
            )
            print(json.dumps(check), flush=True)
        live = {}
        for _, tool, _, args, _, _ in cases:
            samples = []
            for repeat in range(3):
                started = time.perf_counter()
                result = (await client.call_tool(tool, args)).data
                samples.append(time.perf_counter() - started)
                live[f"{tool}_{repeat}"] = result
                assert "error" not in result, result.get("error")
                assert "_provenance" in result and "caveat" in result
            summary["metrics"][f"{tool}_median_seconds"] = statistics.median(samples)
            summary["checks"].append(
                {"name": f"{tool}_live", "pass": True, "latencies_seconds": samples}
            )
        explanation = (
            await client.call_tool(
                "explain_risk_indicator", {"indicator": "cost_share_anomaly"}
            )
        ).data
        brief = (
            await client.call_tool(
                "generate_evidence_brief",
                {
                    "pw_number": 169,
                    "disaster_number": 4734,
                    "applicant_id": "123-0BE2A-00",
                    "indicator": "cost_share_anomaly",
                },
            )
        ).data
        live["explain_risk_indicator"] = explanation
        live["generate_evidence_brief"] = brief
        summary["checks"].append(
            {
                "name": "explanation_schema",
                "pass": all(
                    k in explanation
                    for k in ["methodology", "calculation", "limitations"]
                ),
            }
        )
        summary["checks"].append(
            {
                "name": "evidence_identity",
                "pass": bool(brief.get("source_records"))
                and all(
                    r["disaster_number"] == 4734
                    and r["applicant_id"] == "123-0BE2A-00"
                    and r["pw_number"] == 169
                    for r in brief.get("source_records", [])
                ),
            }
        )
        dump(outdir / "live_tool_responses.json", live)
        try:
            selection, workflows = await run_model_checks(client, outdir)
            summary["metrics"]["tool_selection_correct"] = sum(
                r["pass"] for r in selection
            )
            summary["metrics"]["tool_selection_cases"] = len(selection)
            summary["metrics"]["completed_agent_workflows"] = sum(
                r["completed"] for r in workflows
            )
            summary["metrics"]["agent_workflow_cases"] = len(workflows)
        except Exception as exc:
            summary["model_evaluation_error"] = str(exc)
        grounded = []
        for prompt, required in [
            (
                "Screen Florida disaster 4734 for cost-share review indicators. "
                "Show one project's evidence brief and explain why a 100% "
                "share does not establish wrongdoing. Include data limits.",
                {"get_cost_share_anomalies", "generate_evidence_brief"},
            ),
            (
                "Check Florida disaster 4673 Category C projects for cost "
                "outliers. Explain the source and limits.",
                {"detect_category_outliers"},
            ),
            (
                "Find repeated worksheets in Florida disaster 4673. "
                "Explain why repeated titles may be legitimate.",
                {"find_repeated_worksheets"},
            ),
        ]:
            try:
                review = await run_review(mcp, prompt)
                successful_tools = {
                    c["tool"]
                    for c in review["tool_calls"]
                    if isinstance(c.get("result"), dict) and "error" not in c["result"]
                }
                passed = (
                    required <= successful_tools
                    and review.get("answer_mode") == "deterministic_tool_evidence"
                    and "Human review" in review["answer"]
                )
                grounded.append({"pass": passed, **review})
            except Exception as exc:
                grounded.append({"pass": False, "error": str(exc)})
        dump(outdir / "grounded_browser_workflows.json", grounded)
        summary["checks"].append(
            {
                "name": "grounded_browser_workflows",
                "pass": all(r["pass"] for r in grounded),
            }
        )
        summary["metrics"]["grounded_browser_workflows_passed"] = sum(
            r["pass"] for r in grounded
        )
        summary["metrics"]["grounded_browser_workflow_cases"] = len(grounded)
    summary["completed_at"] = datetime.now(timezone.utc).isoformat()
    summary["all_functional_checks_pass"] = all(c["pass"] for c in summary["checks"])
    source_hash = hashlib.sha256()
    for source in sorted((ROOT / "src").rglob("*.py")):
        source_hash.update(source.relative_to(ROOT).as_posix().encode())
        source_hash.update(source.read_bytes())
    summary["source_sha256"] = source_hash.hexdigest()
    dump(outdir / "summary.json", summary)
    lines = [
        "# Measured Databricks Evaluation",
        "",
        f"Run: {stamp}",
        f"Source SHA-256: {summary['source_sha256']}",
        "",
        "## Functional checks",
        "",
        "| Check | Pass |",
        "|---|---|",
    ]
    lines += [f"| {c['name']} | {c['pass']} |" for c in summary["checks"]]
    lines += ["", "## Measured metrics", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {name} | {value} |" for name, value in summary["metrics"].items()]
    lines += [
        "",
        "## Scope and limits",
        "",
        (
            "Functional tests use the actual registered FastMCP tools in "
            "process inside Databricks. Detection controls use SQLite against "
            "identical archived OpenFEMA snapshots. Live latency includes "
            "retrieval and calculation, but excludes remote MCP transport and "
            "LLM time. Tool selection measures first tool name on 15 "
            "developer-authored questions, not general answer accuracy. "
            "Agent traces are "
            "genuine model and tool responses. No hallucination-rate or "
            "semantic correctness claim is made. Retrieved data is capped and "
            "may be incomplete. The API-backed implementation does not execute "
            "these calculations through Unity Catalog functions. Cost-share "
            "thresholds do not verify declaration authorization. Category "
            "peers are limited to the selected category and filters. Human "
            "review remains required."
        ),
    ]
    if summary.get("model_evaluation_error"):
        lines += ["", f"Model evaluation error: {summary['model_evaluation_error']}"]
    (outdir / "MEASURED_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    with contextlib.suppress(Exception):
        import mlflow

        mlflow.set_experiment(
            "/Users/phebe.arouni@hq.dhs.gov/FEMA Hackathon Evaluation"
        )
        with mlflow.start_run(run_name=f"five-tools-{stamp}") as active:
            mlflow.log_params(
                {
                    "source_sha256": summary["source_sha256"],
                    "model": MODEL,
                    "transport": "in-process MCP",
                    "dataset": "OpenFEMA PA v2",
                }
            )
            mlflow.log_metrics(summary["metrics"])
            mlflow.log_artifacts(str(outdir))
            summary["mlflow_run_id"] = active.info.run_id
            summary["mlflow_experiment_id"] = active.info.experiment_id
        dump(outdir / "summary.json", summary)
    manifest = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in outdir.iterdir()
        if p.is_file()
    }
    dump(outdir / "artifact_hashes.json", manifest)
    print("EVALUATION_SUMMARY " + json.dumps(summary, default=str), flush=True)
    return summary


if __name__ == "__main__":
    asyncio.run(run())

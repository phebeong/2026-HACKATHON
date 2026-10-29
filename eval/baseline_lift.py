"""Small exact-count baseline over archived cohorts; no broad accuracy claim."""

import asyncio
import importlib.util
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from databricks.sdk import WorkspaceClient
from fastmcp import Client

from fema_oversight.app import mcp
from fema_oversight.tools import (
    category_outliers,
    cost_share_anomalies,
    repeated_worksheets,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "eval/results/20261029T111811Z"
MODEL = "databricks-claude-haiku-4-5"


async def main():
    spec = importlib.util.spec_from_file_location(
        "controls", ROOT / "eval/run_hackathon.py"
    )
    controls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controls)
    workspace = WorkspaceClient(profile="fema-hackathon")
    cases = [
        (
            "cost_share",
            cost_share_anomalies,
            "get_cost_share_anomalies",
            {"state_code": "FL", "disaster_number": 4734},
            "How many Florida disaster 4734 public PA records have totalObligated "
            ">= 100000, totalObligated > 0, and federalShareObligated / "
            "totalObligated strictly below 0.70 or strictly above 0.95?",
        ),
        (
            "repeated",
            repeated_worksheets,
            "find_repeated_worksheets",
            {"state_code": "FL", "disaster_number": 4673},
            "How many Florida disaster 4673 groups of applicantId, "
            "applicationTitle and damageCategoryCode have at least two records?",
        ),
        (
            "category",
            category_outliers,
            "detect_category_outliers",
            {"state_code": "FL", "disaster_number": 4673, "damage_category_code": "C"},
            "How many Florida disaster 4673 Category C records have projectAmount "
            "at least three population standard deviations above the cohort mean?",
        ),
    ]
    records = []
    async with Client(mcp) as client, httpx.AsyncClient(timeout=120) as http:
        for rule, module, tool, args, question in cases:
            snapshot = json.loads((EVIDENCE / f"snapshot_{rule}.json").read_text())
            expected = len(controls.control(snapshot, rule))
            for repeat in range(5):
                with patch.object(
                    module, "fetch_pa_records", AsyncMock(return_value=snapshot)
                ):
                    actual = (await client.call_tool(tool, args)).data
                response = await http.post(
                    workspace.config.host + f"/serving-endpoints/{MODEL}/invocations",
                    headers=workspace.config.authenticate(),
                    json={
                        "messages": [
                            {
                                "role": "system",
                            "content": (
                                'Return only JSON {"count": integer or null}. '
                                "Use null when you cannot verify the answer. "
                                "Do not guess."
                            ),
                            },
                            {
                                "role": "user",
                                "content": question
                            + " Use the source state as retrieved on "
                            "October 29, 2026. "
                                "You have no source records or data-access tools.",
                            },
                        ],
                        "max_tokens": 120,
                        "temperature": 0,
                    },
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                try:
                    parsed = json.loads(content)
                    count = parsed.get("count")
                except (ValueError, AttributeError):
                    count = None
                records.append(
                    {
                        "case": rule,
                        "repeat": repeat + 1,
                        "question": question,
                        "expected_count": expected,
                        "tool_count": actual.get("total"),
                        "tool_exact_match": actual.get("total") == expected,
                        "no_tool_response": content,
                        "no_tool_count": count,
                        "no_tool_exact_match": type(count) is int and count == expected,
                        "no_tool_abstained_or_invalid": count is None,
                    }
                )
    report = {
        "model": MODEL,
        "temperature": 0,
        "cases": 3,
        "repeats_per_case": 5,
        "tool_exact_matches": sum(r["tool_exact_match"] for r in records),
        "no_tool_exact_matches": sum(r["no_tool_exact_match"] for r in records),
        "no_tool_abstentions_or_invalid": sum(
            r["no_tool_abstained_or_invalid"] for r in records
        ),
        "scope": "Fixed archived inputs; exact count only. Tools replay the "
        "snapshots; the no-tool model has no snapshots. Repeated prompts are "
        "correlated and do not establish general answer accuracy or causal lift.",
        "records": records,
    }
    (EVIDENCE / "baseline_count_comparison.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "records"}))


if __name__ == "__main__":
    asyncio.run(main())

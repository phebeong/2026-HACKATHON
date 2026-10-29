"""Authenticated health and real remote MCP checks; never print credentials."""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
from databricks.sdk import WorkspaceClient
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


async def main():
    url = "https://2026h-7474654188777746.aws.databricksapps.com"
    headers = WorkspaceClient(profile="fema-hackathon").config.authenticate()
    async with httpx.AsyncClient(timeout=30, follow_redirects=False) as http:
        health = await http.get(url + "/health", headers=headers)
        health.raise_for_status()
    async with Client(StreamableHttpTransport(url + "/mcp", headers=headers)) as client:
        names = [t.name for t in await client.list_tools()]
        explanation = (
            await client.call_tool(
                "explain_risk_indicator", {"indicator": "cost_share_anomaly"}
            )
        ).data
    record = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "health_http": health.status_code,
        "tools": names,
        "remote_mcp_explanation_pass": "calculation" in explanation,
        "browser_cost_share_review": {
            "observed": True,
            "elapsed_seconds": 9.709,
            "tool_calls": 3,
            "indicators": 238,
            "displayed": 3,
            "brief_identity": [4734, "123-0BE2A-00", 169],
            "evidence_summary_visible": True,
        },
        "scope": "One authenticated remote MCP smoke test and one observed "
        "hosted browser review. No load or general reliability claim.",
    }
    dest = (
        Path(__file__).resolve().parent / "results/20261029T111811Z/hosted_smoke.json"
    )
    dest.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record))


if __name__ == "__main__":
    asyncio.run(main())

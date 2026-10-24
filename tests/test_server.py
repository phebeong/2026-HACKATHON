"""Smoke tests for the FEMA Evidence & Oversight Graph MCP server.

Verify the server imports and every submodule registers, and that all five
oversight tools are discoverable.
"""

from __future__ import annotations

import pytest
from fastmcp import FastMCP

from fema_oversight.app import mcp
from fema_oversight.config import settings

EXPECTED_TOOLS = {
    "get_cost_share_anomalies",
    "find_repeated_worksheets",
    "detect_category_outliers",
    "explain_risk_indicator",
    "generate_evidence_brief",
}


def test_server_is_importable():
    assert mcp is not None


def test_server_has_name():
    assert mcp.name == "FEMA Evidence & Oversight Graph"


def test_default_transport_is_stdio():
    assert settings.mcp_transport == "stdio"


def test_tools_register_without_error():
    from fema_oversight.tools import register_tools

    register_tools(FastMCP("test"))


def test_prompts_register_without_error():
    from fema_oversight.prompts import register_prompts

    register_prompts(FastMCP("test"))


def test_resources_register_without_error():
    from fema_oversight.resources import register_resources

    register_resources(FastMCP("test"))


def test_routes_register_without_error():
    from fema_oversight.routes import register_routes

    register_routes(FastMCP("test"))


@pytest.mark.asyncio
async def test_all_five_tools_discoverable():
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert EXPECTED_TOOLS <= names, f"missing: {EXPECTED_TOOLS - names}"


@pytest.mark.asyncio
async def test_provenance_resource_registered():
    resources = await mcp.list_resources()
    uris = {str(r.uri) for r in resources}
    assert "fema-pa://provenance" in uris

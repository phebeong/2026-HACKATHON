"""MCP server entry point for the FEMA Evidence & Oversight Graph.

Thin by design: build the FastMCP instance, register tools/prompts/resources/
routes, and choose a transport (stdio locally, HTTP when a platform injects a
port). All logic lives in the submodules.
"""

from __future__ import annotations

import os

from fastmcp import FastMCP

from fema_oversight.config import settings
from fema_oversight.prompts import register_prompts
from fema_oversight.resources import register_resources
from fema_oversight.routes import register_routes
from fema_oversight.tools import register_tools

mcp = FastMCP(
    name="FEMA Evidence & Oversight Graph",
    instructions=(
        "Transforms open FEMA Public Assistance data into traceable, explainable, "
        "analyst-ready oversight intelligence. Tools return REVIEW INDICATORS on "
        "public aggregate data, never findings; a human analyst makes every "
        "determination. Not for official reporting."
    ),
)

register_tools(mcp)
register_prompts(mcp)
register_resources(mcp)
register_routes(mcp)


def main() -> None:
    """Start the server, choosing transport from the environment."""
    platform_port = os.getenv("DATABRICKS_APP_PORT") or os.getenv("PORT")
    if platform_port:
        mcp.run(transport="http", host="0.0.0.0", port=int(platform_port))
    elif settings.mcp_transport == "streamable-http":
        mcp.run(transport="streamable-http", host=settings.mcp_host, port=settings.mcp_port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()

"""Tool: explain_risk_indicator — the methodology behind an indicator (explainability)."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import FastMCP

from fema_oversight.models import INDICATOR_METHODOLOGY, IndicatorType


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="explain_risk_indicator",
        annotations={
            "title": "Explain a risk indicator",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def explain_risk_indicator(
        indicator: Annotated[
            IndicatorType,
            "Which indicator to explain: cost_share_anomaly, repeated_worksheet, or category_outlier.",
        ],
    ) -> dict[str, Any]:
        """Return the methodology, calculation, thresholds, and limitations behind
        a risk indicator, so an analyst (or a judge) can see exactly how a signal
        is derived. No data query; this is the auditable 'show your work' layer.
        """
        card = INDICATOR_METHODOLOGY.get(indicator.value)
        if not card:
            return {"error": f"Unknown indicator '{indicator}'.",
                    "hint": "Use cost_share_anomaly, repeated_worksheet, or category_outlier."}
        return dict(card)

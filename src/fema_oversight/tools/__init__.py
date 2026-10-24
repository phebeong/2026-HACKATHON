"""Tool registration aggregator. One file per tool; register each here."""

from fema_oversight.tools import (
    category_outliers,
    cost_share_anomalies,
    evidence_brief,
    explain_indicator,
    repeated_worksheets,
)


def register_tools(mcp) -> None:
    # Detection layer
    cost_share_anomalies.register(mcp)
    repeated_worksheets.register(mcp)
    category_outliers.register(mcp)
    # Explainability layer
    explain_indicator.register(mcp)
    evidence_brief.register(mcp)

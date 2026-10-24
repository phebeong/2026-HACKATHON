"""Prompt: fema_oversight_review — a disciplined oversight-analyst starter."""

from __future__ import annotations

from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    @mcp.prompt(
        name="fema_oversight_review",
        description="Start a disciplined FEMA PA oversight review for a jurisdiction.",
    )
    def oversight_review(state_code: str) -> str:
        """Return a prompt that frames a careful, review-only oversight pass."""
        return (
            f"You are assisting a FEMA Public Assistance oversight analyst reviewing {state_code}.\n\n"
            "Use the available tools to surface REVIEW INDICATORS over public FEMA data:\n"
            "1. get_cost_share_anomalies - obligations whose federal share differs from the expected pattern.\n"
            "2. find_repeated_worksheets - potential fragmentation/duplication patterns.\n"
            "3. detect_category_outliers - costs that are outliers within their category of work.\n"
            "Then use explain_risk_indicator and generate_evidence_brief to document why.\n\n"
            "Rules: these are review indicators, not findings. Never state or imply fraud, waste, "
            "or abuse. Always relay the source, methodology, and limitations. The analyst, not you, "
            "makes every determination. Public aggregate data only; not for official reporting."
        )

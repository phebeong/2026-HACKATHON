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
            "Assist a FEMA Public Assistance oversight analyst reviewing "
            f"{state_code}.\n\n"
            "Use tools to surface REVIEW INDICATORS over public FEMA data:\n"
            "1. get_cost_share_anomalies - screen federal-share ratios.\n"
            "2. find_repeated_worksheets - potential fragmentation patterns.\n"
            "3. detect_category_outliers - within-category cost outliers.\n"
            "Use explain_risk_indicator to document the methodology, and "
            "generate_evidence_brief with disaster, applicant and worksheet "
            "identity to package source records.\n\n"
            "These are review indicators, not findings. Never imply wrongdoing. "
            "Relay the source, subset limits and methodology. Authorized cost "
            "shares may be legitimate. A human makes every determination. "
            "Public data only; not for official reporting."
        )

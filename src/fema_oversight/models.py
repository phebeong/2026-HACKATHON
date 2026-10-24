"""Pydantic models and enums for FEMA oversight tool parameters and responses.

Framing: outputs are REVIEW INDICATORS on public aggregate FEMA data, not
findings. Nothing here detects, proves, or alleges fraud, waste, or abuse.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ResponseFormat(str, Enum):
    """How a tool should shape its return value."""

    JSON = "json"
    MARKDOWN = "markdown"


class IndicatorType(str, Enum):
    """The three risk-indicator families this server can explain."""

    COST_SHARE = "cost_share_anomaly"
    REPEATED_WORKSHEET = "repeated_worksheet"
    CATEGORY_OUTLIER = "category_outlier"


REVIEW_CAVEAT = (
    "Review indicator on public aggregate data. Not a finding; does not allege "
    "fraud, waste, or abuse. A human analyst makes the determination."
)

# Static, auditable methodology cards (the "show your work" layer).
INDICATOR_METHODOLOGY: dict[str, dict[str, str]] = {
    "cost_share_anomaly": {
        "name": "Cost-share anomaly",
        "methodology": (
            "Compares each project's federal share ratio "
            "(federalShareObligated / totalObligated) against an expected band. "
            "FEMA Public Assistance is normally a 75% federal share, but some "
            "declarations are authorized at 90% or 100% by law."
        ),
        "calculation": "ratio = federalShareObligated / totalObligated; flag if ratio < low or ratio > high.",
        "thresholds": "Default band 0.70-0.95; projects below a minimum total obligated are ignored to cut noise.",
        "limitations": "Higher statutory shares are expected, not anomalies. Review required.",
    },
    "repeated_worksheet": {
        "name": "Repeated / fragmentation pattern",
        "methodology": (
            "Groups project worksheets by applicant, application title, and "
            "damage category; flags groups at or above a repeat threshold as a "
            "potential fragmentation or duplication pattern."
        ),
        "calculation": "GROUP BY applicantId, applicationTitle, damageCategoryCode HAVING COUNT(*) >= min_repeat_count.",
        "thresholds": "Default min_repeat_count = 2.",
        "limitations": "Repeated titles are frequently legitimate (phased work, multiple sites). Review signal only.",
    },
    "category_outlier": {
        "name": "Within-category cost outlier",
        "methodology": (
            "Computes the mean and standard deviation of projectAmount within a "
            "damage category, then flags projects a set number of standard "
            "deviations above the category mean. Outliers are measured relative "
            "to declaration type, category of work, and peer projects."
        ),
        "calculation": "sigma_above = (projectAmount - category_mean) / category_stddev; flag if >= sigma_threshold.",
        "thresholds": "Default sigma_threshold = 3.0.",
        "limitations": "Large, legitimate projects (major infrastructure) can be high outliers. Review required.",
    },
}


class PaginationParams(BaseModel):
    """Reusable pagination inputs for list-style tools."""

    limit: int = Field(default=25, ge=1, le=100, description="Max items to return (1-100).")
    offset: int = Field(default=0, ge=0, description="Items to skip from the start.")

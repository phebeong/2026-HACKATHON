"""Tool: generate_evidence_brief — package one flagged project for human review."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import FastMCP

from fema_oversight.models import INDICATOR_METHODOLOGY, REVIEW_CAVEAT, IndicatorType
from fema_oversight.utils import (
    UpstreamServiceError,
    fetch_pa_records,
    odata_quote,
    provenance_block,
    to_float,
)

_SELECT = [
    "pwNumber",
    "applicantId",
    "stateAbbreviation",
    "county",
    "disasterNumber",
    "applicationTitle",
    "damageCategoryCode",
    "damageCategoryDescrip",
    "projectAmount",
    "totalObligated",
    "federalShareObligated",
    "declarationDate",
]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="generate_evidence_brief",
        annotations={
            "title": "Generate an evidence brief",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    async def generate_evidence_brief(
        pw_number: Annotated[int, "Project Worksheet number to brief."],
        indicator: Annotated[
            IndicatorType,
            (
                "Which indicator triggered the review: cost_share_anomaly, "
                "repeated_worksheet, or category_outlier."
            ),
        ],
        disaster_number: int = 0,
        applicant_id: str = "",
    ) -> dict[str, Any]:
        """Compose an analyst-facing evidence brief for one flagged Project
        Worksheet: the source records, the rationale and methodology, the
        limitations, and the review caveats. This is the artifact a human
        reviews; it adds no conclusion the data does not support.

        Source: OpenFEMA Public Assistance Funded Projects Details (v2), daily.
        """
        if pw_number <= 0:
            return {
                "error": "pw_number must be positive.",
                "hint": "Pass a real Project Worksheet number.",
            }
        card = INDICATOR_METHODOLOGY.get(indicator.value)
        if not card:
            return {
                "error": f"Unknown indicator '{indicator}'.",
                "hint": (
                    "Use cost_share_anomaly, repeated_worksheet, or category_outlier."
                ),
            }
        try:
            clauses = [f"pwNumber eq {int(pw_number)}"]
            if disaster_number:
                clauses.append(f"disasterNumber eq {int(disaster_number)}")
            if applicant_id:
                clauses.append(f"applicantId eq '{odata_quote(applicant_id)}'")
            records = await fetch_pa_records(
                odata_filter=" and ".join(clauses), select=_SELECT, top=50
            )
        except UpstreamServiceError as exc:
            return {
                "error": str(exc),
                "hint": "Retry; if it persists the dataset may be refreshing.",
            }
        if not records:
            return {
                "error": f"No public worksheet {pw_number} found.",
                "hint": "Confirm the PW number from a detection tool result.",
            }

        identities = {(r.get("disasterNumber"), r.get("applicantId")) for r in records}
        if len(identities) > 1:
            return {
                "error": "Worksheet number matches multiple projects.",
                "hint": (
                    "Supply disaster_number and applicant_id from the detection result."
                ),
            }

        source_records = []
        for r in records:
            source_records.append(
                {
                    "pw_number": r.get("pwNumber"),
                    "applicant_id": r.get("applicantId"),
                    "state": r.get("stateAbbreviation"),
                    "county": r.get("county"),
                    "disaster_number": r.get("disasterNumber"),
                    "application_title": r.get("applicationTitle"),
                    "damage_category": r.get("damageCategoryDescrip"),
                    "project_amount": to_float(r.get("projectAmount")),
                    "total_obligated": to_float(r.get("totalObligated")),
                    "federal_share_obligated": to_float(r.get("federalShareObligated")),
                    "declaration_date": r.get("declarationDate"),
                }
            )

        return {
            "pw_number": pw_number,
            "indicator": indicator.value,
            "indicator_name": card["name"],
            "source_records": source_records,
            "rationale": (
                f"This Project Worksheet was submitted for {card['name']} "
                "review. This brief does not independently verify that the "
                "indicator threshold was met. Review the source records "
                "below against program context before drawing any conclusion."
            ),
            "methodology": card["methodology"],
            "limitations": card["limitations"],
            "review_status": "Not a finding. Analyst review required.",
            "caveat": REVIEW_CAVEAT,
            "_provenance": provenance_block(card["methodology"]),
        }

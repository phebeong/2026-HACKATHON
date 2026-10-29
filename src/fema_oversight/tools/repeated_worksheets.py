"""Tool: find_repeated_worksheets — a PA fragmentation/duplication review indicator."""

from __future__ import annotations

from collections import defaultdict
from typing import Annotated, Any

from fastmcp import FastMCP

from fema_oversight.models import REVIEW_CAVEAT, PaginationParams
from fema_oversight.utils import (
    UpstreamServiceError,
    fetch_pa_records,
    odata_quote,
    paginate,
    provenance_block,
    to_float,
)

_SELECT = [
    "pwNumber",
    "applicantId",
    "stateAbbreviation",
    "disasterNumber",
    "applicationTitle",
    "damageCategoryCode",
    "damageCategoryDescrip",
    "federalShareObligated",
]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="find_repeated_worksheets",
        annotations={
            "title": "Repeated worksheets (review indicator)",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    async def find_repeated_worksheets(
        state_code: Annotated[
            str, "Optional two-letter state filter. Empty for all."
        ] = "",
        disaster_number: Annotated[
            int, "Optional disaster number filter. 0 for all."
        ] = 0,
        min_repeat_count: Annotated[
            int, "Minimum matching worksheets to flag a group (>=2)."
        ] = 2,
        pagination: PaginationParams | None = None,
    ) -> dict[str, Any]:
        """Flag applicants with repeated project worksheets sharing a title and
        damage category — a potential fragmentation or duplication pattern worth
        analyst review. Repeated titles are frequently legitimate (phased work,
        multiple sites); this is a review signal, not a duplication finding.

        Source: OpenFEMA Public Assistance Funded Projects Details (v2), daily.
        """
        if min_repeat_count < 2:
            return {"error": "min_repeat_count must be >= 2.", "hint": "Use 2 or more."}
        state = (state_code or "").strip().upper()
        clauses = []
        if state:
            if len(state) != 2 or not state.isalpha():
                return {
                    "error": "state_code must be two letters or empty.",
                    "hint": "e.g. 'LA'.",
                }
            clauses.append(f"stateAbbreviation eq '{odata_quote(state)}'")
        if disaster_number < 0:
            return {"error": "disaster_number must be nonnegative."}
        if disaster_number:
            clauses.append(f"disasterNumber eq {int(disaster_number)}")
        flt = " and ".join(clauses) if clauses else None

        try:
            records = await fetch_pa_records(
                odata_filter=flt, select=_SELECT, top=10000
            )
        except UpstreamServiceError as exc:
            return {"error": str(exc), "hint": "Narrow by state or disaster_number."}

        groups: dict[tuple, list[dict]] = defaultdict(list)
        for r in records:
            key = (
                r.get("disasterNumber"),
                r.get("applicantId"),
                r.get("applicationTitle"),
                r.get("damageCategoryCode"),
            )
            if all(k is not None for k in key):
                groups[key].append(r)

        flagged = []
        for (disaster, applicant_id, title, cat), rows in groups.items():
            if len(rows) >= min_repeat_count:
                fed = sum(to_float(x.get("federalShareObligated")) or 0.0 for x in rows)
                flagged.append(
                    {
                        "applicant_id": applicant_id,
                        "disaster_number": disaster,
                        "pw_numbers": sorted(
                            {
                                r.get("pwNumber")
                                for r in rows
                                if r.get("pwNumber") is not None
                            }
                        ),
                        "state": rows[0].get("stateAbbreviation"),
                        "application_title": title,
                        "damage_category_description": rows[0].get(
                            "damageCategoryDescrip"
                        ),
                        "worksheet_count": len(rows),
                        "total_federal_share_obligated": round(fed, 2),
                    }
                )
        flagged.sort(
            key=lambda x: (x["worksheet_count"], x["total_federal_share_obligated"]),
            reverse=True,
        )

        pg = pagination or PaginationParams()
        out = paginate(flagged, pg.limit, pg.offset)
        out["data_scope"] = {
            "records_retrieved": len(records),
            "record_cap": 10000,
            "possibly_truncated": len(records) >= 10000,
        }
        out["caveat"] = REVIEW_CAVEAT
        out["_provenance"] = provenance_block(
            "Grouped by disasterNumber, applicantId, applicationTitle, "
            "damageCategoryCode; "
            f"flagged groups with count >= {min_repeat_count}."
        )
        return out

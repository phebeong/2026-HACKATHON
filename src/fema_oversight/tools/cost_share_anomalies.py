"""Tool: get_cost_share_anomalies — a FEMA PA cost-share review indicator."""

from __future__ import annotations

from typing import Annotated, Any

from fastmcp import FastMCP

from fema_oversight.models import PaginationParams, REVIEW_CAVEAT
from fema_oversight.utils import (
    UpstreamServiceError,
    fetch_pa_records,
    odata_quote,
    paginate,
    provenance_block,
    to_float,
)

_SELECT = [
    "pwNumber", "applicantId", "stateAbbreviation", "disasterNumber",
    "totalObligated", "federalShareObligated", "damageCategoryCode",
]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_cost_share_anomalies",
        annotations={
            "title": "Cost-share anomalies (review indicator)",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    async def get_cost_share_anomalies(
        state_code: Annotated[str, "Two-letter USPS state/territory code, e.g. 'FL'."],
        min_total_obligated: Annotated[float, "Ignore projects below this total obligated amount."] = 100000.0,
        band_low: Annotated[float, "Lower bound of the expected federal-share ratio."] = 0.70,
        band_high: Annotated[float, "Upper bound of the expected federal-share ratio."] = 0.95,
        pagination: PaginationParams | None = None,
    ) -> dict[str, Any]:
        """Flag PA obligations whose federal cost-share ratio differs from the
        expected pattern for comparable declarations, for analyst review.

        Source: OpenFEMA Public Assistance Funded Projects Details (v2), updated
        daily. PA is normally a 75% federal share; 90%/100% shares are authorized
        by law for some declarations and are expected, not anomalies.

        Returns a pagination envelope of review indicators. Each row is a signal
        on public aggregate data, not a finding.
        """
        state = (state_code or "").strip().upper()
        if len(state) != 2 or not state.isalpha():
            return {"error": "state_code must be two letters.", "hint": "e.g. 'FL', 'TX'."}
        if band_high < band_low:
            return {"error": "band_high is below band_low.", "hint": "Pass band_low <= band_high."}

        flt = (
            f"stateAbbreviation eq '{odata_quote(state)}' "
            f"and totalObligated ge {float(min_total_obligated)}"
        )
        try:
            records = await fetch_pa_records(odata_filter=flt, select=_SELECT, top=5000)
        except UpstreamServiceError as exc:
            return {"error": str(exc), "hint": "Try a narrower state or a higher min_total_obligated."}

        flagged: list[dict[str, Any]] = []
        for r in records:
            total = to_float(r.get("totalObligated"))
            fed = to_float(r.get("federalShareObligated"))
            if not total or fed is None:
                continue
            ratio = fed / total
            if ratio < band_low or ratio > band_high:
                flagged.append({
                    "pw_number": r.get("pwNumber"),
                    "applicant_id": r.get("applicantId"),
                    "state": r.get("stateAbbreviation"),
                    "disaster_number": r.get("disasterNumber"),
                    "total_obligated": round(total, 2),
                    "federal_share_obligated": round(fed, 2),
                    "federal_share_ratio": round(ratio, 4),
                })
        flagged.sort(key=lambda x: abs(x["federal_share_ratio"] - 0.75), reverse=True)

        pg = pagination or PaginationParams()
        out = paginate(flagged, pg.limit, pg.offset)
        out["caveat"] = REVIEW_CAVEAT
        out["_provenance"] = provenance_block(
            "federal_share_ratio = federalShareObligated / totalObligated; "
            f"flagged outside [{band_low}, {band_high}]."
        )
        return out

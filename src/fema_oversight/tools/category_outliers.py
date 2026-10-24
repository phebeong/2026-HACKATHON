"""Tool: detect_category_outliers — a within-category cost outlier review indicator."""

from __future__ import annotations

import statistics
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
    "projectAmount", "damageCategoryCode", "damageCategoryDescrip",
]


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        name="detect_category_outliers",
        annotations={
            "title": "Within-category cost outliers (review indicator)",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    async def detect_category_outliers(
        damage_category_code: Annotated[str, "Single-letter PA category of work, A-G."],
        state_code: Annotated[str, "Optional two-letter state filter. Empty for all."] = "",
        sigma_threshold: Annotated[float, "Std deviations above the category mean to flag (1-10)."] = 3.0,
        pagination: PaginationParams | None = None,
    ) -> dict[str, Any]:
        """Flag projects whose amount is a high statistical outlier within their
        damage category — measured against the category's own mean, so an outlier
        means something relative to like work, not the whole portfolio.

        A $10M project is routine for Category C (roads/bridges) and unusual for
        Category G (parks). Large, legitimate projects can still be high outliers;
        this is a review signal, not a finding. Source: OpenFEMA PA v2, daily.
        """
        cat = (damage_category_code or "").strip().upper()
        if len(cat) != 1 or not cat.isalpha():
            return {"error": "damage_category_code must be a single letter A-G.", "hint": "e.g. 'C'."}
        if not (1.0 <= sigma_threshold <= 10.0):
            return {"error": "sigma_threshold must be between 1 and 10.", "hint": "Try 3.0."}
        state = (state_code or "").strip().upper()
        clauses = [f"damageCategoryCode eq '{odata_quote(cat)}'"]
        if state:
            if len(state) != 2 or not state.isalpha():
                return {"error": "state_code must be two letters or empty.", "hint": "e.g. 'FL'."}
            clauses.append(f"stateAbbreviation eq '{odata_quote(state)}'")

        try:
            records = await fetch_pa_records(
                odata_filter=" and ".join(clauses), select=_SELECT, top=10000
            )
        except UpstreamServiceError as exc:
            return {"error": str(exc), "hint": "Try a specific state to shrink the set."}

        amounts = [a for a in (to_float(r.get("projectAmount")) for r in records) if a is not None]
        if len(amounts) < 2:
            return {"error": "Not enough data to compute a category baseline.",
                    "hint": "Widen the filter (remove the state, or pick another category)."}
        mean = statistics.fmean(amounts)
        sd = statistics.pstdev(amounts)
        if sd <= 0:
            return {"error": "Category has no cost variation to measure outliers against.",
                    "hint": "Pick another category or widen the filter."}

        flagged = []
        for r in records:
            amt = to_float(r.get("projectAmount"))
            if amt is None:
                continue
            sigma = (amt - mean) / sd
            if sigma >= sigma_threshold:
                flagged.append({
                    "pw_number": r.get("pwNumber"),
                    "applicant_id": r.get("applicantId"),
                    "state": r.get("stateAbbreviation"),
                    "disaster_number": r.get("disasterNumber"),
                    "damage_category_description": r.get("damageCategoryDescrip"),
                    "project_amount": round(amt, 2),
                    "category_mean": round(mean, 2),
                    "sigma_above_mean": round(sigma, 2),
                })
        flagged.sort(key=lambda x: x["sigma_above_mean"], reverse=True)

        pg = pagination or PaginationParams()
        out = paginate(flagged, pg.limit, pg.offset)
        out["category_stats"] = {"mean": round(mean, 2), "stddev": round(sd, 2), "n": len(amounts)}
        out["caveat"] = REVIEW_CAVEAT
        out["_provenance"] = provenance_block(
            f"sigma = (projectAmount - category_mean) / category_stddev within "
            f"category {cat}; flagged sigma >= {sigma_threshold}."
        )
        return out

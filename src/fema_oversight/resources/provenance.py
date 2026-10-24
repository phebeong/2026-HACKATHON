"""Resource: fema-pa://provenance — dataset provenance and field definitions."""

from __future__ import annotations

import json

from fastmcp import FastMCP

from fema_oversight.utils import DATASET_PROVENANCE

FIELD_DEFINITIONS = {
    "federalShareObligated": "Federal PA funding available to the grantee. Typically 75% of total; some declarations authorized at 90%/100%.",
    "totalObligated": "Federal share plus state and applicant administrative costs.",
    "projectAmount": "Estimated total project cost from the damage survey, before admin costs.",
    "damageCategoryCode": "Single-letter PA category of work. A-B emergency work; C-G permanent work.",
    "mitigationAmount": "Section 406 hazard-mitigation portion. Can be negative due to adjustments; not an error.",
}


def register(mcp: FastMCP) -> None:
    @mcp.resource("fema-pa://provenance")
    def provenance() -> str:
        """Provenance and field definitions for the FEMA PA dataset this server reads.

        The model can read this to ground any answer's source line, methodology,
        and caveats. Trust beats retrieval: credit travels with the data.
        """
        return json.dumps(
            {"provenance": DATASET_PROVENANCE, "field_definitions": FIELD_DEFINITIONS},
            indent=2,
        )

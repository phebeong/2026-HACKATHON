"""Shared helpers: OpenFEMA HTTP client, provenance, pagination.

Keeps the template's security posture: a fixed, operator-controlled API origin,
relative-path validation, redirects and env proxies disabled, a response-size
cap, and sanitized upstream errors. Tools pass only validated relative paths and
OData query params; never a caller-supplied URL.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from typing import Any
from urllib.parse import unquote, urlsplit

import httpx

DEFAULT_TIMEOUT = 30.0
MAX_RESPONSE_BYTES = 20_000_000

# Operator-controlled origin. OpenFEMA is public U.S. government open data,
# no API key, same privacy policy as FEMA.gov.
API_BASE_URL = "https://www.fema.gov/api/open/"

# The Public Assistance Funded Projects Details dataset (v2).
PA_ENTITY = "PublicAssistanceFundedProjectsDetails"
PA_PATH = f"v2/{PA_ENTITY}"

DATASET_PROVENANCE: dict[str, str] = {
    "source": "FEMA OpenFEMA Public Assistance Funded Projects Details (v2)",
    "publisher": "FEMA / U.S. Department of Homeland Security",
    "source_system": "Grants Manager (FAC-Trax)",
    "source_url": (
        "https://www.fema.gov/openfema-data-page/"
        "public-assistance-funded-projects-details-v2"
    ),
    "access": "public, no API key, read-only",
    "update_frequency": "daily (R/P1D)",
    "financial_caveat": (
        "Figures are from FEMA's Grants Manager, not FEMA's official financial "
        "system, and may differ from USAspending.gov. Not for official reporting."
    ),
}


class UpstreamServiceError(RuntimeError):
    """Sanitized external-service failure safe to return to an MCP client."""


def _validate_relative_path(path: str) -> str:
    """Reject paths that could select or escape the configured API origin."""
    parsed = urlsplit(path)
    decoded_path = parsed.path
    for _ in range(3):
        decoded = unquote(decoded_path)
        if decoded == decoded_path:
            break
        decoded_path = decoded
    segments = decoded_path.replace("\\", "/").split("/")
    if (
        not path
        or parsed.scheme
        or parsed.netloc
        or parsed.query
        or parsed.fragment
        or decoded_path.startswith(("/", "\\"))
        or any(segment in {".", ".."} for segment in segments)
    ):
        raise ValueError("path must be a relative API path without a query or fragment")
    return path


async def fetch_json(
    path: str,
    params: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    """GET a path from the fixed OpenFEMA origin and return parsed JSON."""
    safe_path = _validate_relative_path(path)
    try:
        async with httpx.AsyncClient(
            base_url=API_BASE_URL,
            follow_redirects=False,
            timeout=timeout,
            trust_env=False,
        ) as client:
            async with client.stream("GET", safe_path, params=params) as response:
                response.raise_for_status()
                content = bytearray()
                async for chunk in response.aiter_bytes():
                    content.extend(chunk)
                    if len(content) > MAX_RESPONSE_BYTES:
                        raise UpstreamServiceError(
                            "Upstream response exceeded the size limit."
                        )
                return json.loads(content)
    except UpstreamServiceError:
        raise
    except httpx.HTTPStatusError as exc:
        raise UpstreamServiceError(
            f"Upstream service returned status {exc.response.status_code}."
        ) from None
    except (httpx.DecodingError, json.JSONDecodeError, UnicodeDecodeError):
        raise UpstreamServiceError("Upstream service returned invalid JSON.") from None
    except httpx.RequestError:
        raise UpstreamServiceError("Upstream service request failed.") from None


async def fetch_pa_records(
    odata_filter: str | None = None,
    select: list[str] | None = None,
    top: int = 1000,
    orderby: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch Public Assistance records from OpenFEMA and return the record list.

    OpenFEMA wraps results as {"metadata": {...}, "<entity>": [...]}. We return
    just the record list. `top` is capped at OpenFEMA's 10,000-per-call limit.
    """
    params: dict[str, Any] = {"$top": min(max(top, 1), 10000), "$format": "json"}
    if odata_filter:
        params["$filter"] = odata_filter
    if select:
        params["$select"] = ",".join(select)
    if orderby:
        params["$orderby"] = orderby
    payload = await fetch_json(PA_PATH, params=params)
    if not isinstance(payload, dict) or PA_ENTITY not in payload:
        raise UpstreamServiceError("Upstream response omitted the dataset records.")
    records = payload[PA_ENTITY]
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise UpstreamServiceError("Upstream response has an invalid record structure.")
    return records


def to_float(value: Any) -> float | None:
    """Best-effort numeric coercion; OpenFEMA delivers many numbers as strings."""
    if value is None or value == "":
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def provenance_block(methodology: str, as_of: str | None = None) -> dict[str, str]:
    """The five-field provenance stamp carried on every output."""
    return {
        "source": DATASET_PROVENANCE["source"],
        "last_updated": as_of or "Source update timestamp not retrieved",
        "update_frequency": DATASET_PROVENANCE["update_frequency"],
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "methodology": methodology,
        "limitations": (
            DATASET_PROVENANCE["financial_caveat"]
            + " Detection tools analyze at most 5,000 cost-share records or "
            "10,000 repeated-worksheet/category records per call. Results and "
            "baselines describe the retrieved subset, not the full dataset. "
            "Cost-share bands do not verify declaration-specific authorizations; "
            "authorized 100% shares may be returned."
        ),
        "review_status": ("Review indicator on public aggregate data. Not a finding."),
    }


def odata_quote(value: str) -> str:
    """Single-quote-escape a string for an OData filter literal."""
    return value.replace("'", "''")


def paginate(items: list[Any], limit: int, offset: int) -> dict[str, Any]:
    """Slice a list and return a standard pagination envelope."""
    total = len(items)
    window = items[offset : offset + limit]
    next_offset = offset + len(window)
    return {
        "total": total,
        "count": len(window),
        "offset": offset,
        "items": window,
        "has_more": next_offset < total,
        "next_offset": next_offset if next_offset < total else None,
    }

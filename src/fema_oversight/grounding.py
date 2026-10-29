"""Render the review summary from tool evidence, without model-authored claims."""

from fema_oversight.models import INDICATOR_METHODOLOGY, REVIEW_CAVEAT
from fema_oversight.utils import DATASET_PROVENANCE

DETECTORS = {
    "get_cost_share_anomalies": "Cost-share screening",
    "find_repeated_worksheets": "Repeated worksheet screening",
    "detect_category_outliers": "Category cost screening",
}


def evidence_summary(calls):
    """Use counts and methods from successful tool responses, never record prose.

    The LLM selects tools and arguments. This renderer controls the displayed
    narrative. Full source records remain available in the separate tool trace.
    It does not certify that the selected filters answer the user's question.
    """
    lines = ["Evidence review", REVIEW_CAVEAT]
    successful = 0
    for index, call in enumerate(calls, 1):
        name, result = call["tool"], call.get("result")
        args = call.get("arguments", {})
        if not isinstance(result, dict) or "error" in result:
            lines.append(
                f"Tool {index}: no usable evidence. Inspect the tool response."
            )
            continue
        if name in DETECTORS:
            successful += 1
            scope = result.get("data_scope", {})
            lines.append(
                f"{DETECTORS[name]}: {result.get('total', 0)} review indicators; "
                f"{result.get('count', 0)} displayed. "
                f"{scope.get('records_retrieved', 'Unknown')} source records "
                f"retrieved; cap {scope.get('record_cap', 'unknown')}."
            )
            if scope.get("possibly_truncated"):
                lines.append("Retrieval cap reached. This result may be incomplete.")
            if name == "get_cost_share_anomalies":
                low = args.get("band_low", 0.70)
                high = args.get("band_high", 0.95)
                lines.append(
                    f"Rule: federalShareObligated / totalObligated < {low} "
                    f"or > {high}. Equality at either boundary is not flagged. "
                    "Declaration-specific authorization has not been verified. "
                    "A threshold flag does not establish an unauthorized share."
                )
            elif name == "find_repeated_worksheets":
                lines.append(INDICATOR_METHODOLOGY["repeated_worksheet"]["calculation"])
                lines.append(INDICATOR_METHODOLOGY["repeated_worksheet"]["limitations"])
            else:
                lines.append(INDICATOR_METHODOLOGY["category_outlier"]["calculation"])
                lines.append(INDICATOR_METHODOLOGY["category_outlier"]["limitations"])
            if result.get("total") == 0:
                lines.append(
                    "No indicators returned for this retrieved subset and rule. "
                    "This does not establish the absence of issues."
                )
        elif name == "generate_evidence_brief":
            successful += 1
            lines.append(
                f"Evidence brief: {len(result.get('source_records', []))} "
                "source records. Inspect the disaster, applicant and worksheet "
                "identifiers in the trace. The triggering threshold is not "
                "independently revalidated by this brief."
            )
        elif name == "explain_risk_indicator":
            indicator = args.get("indicator")
            if indicator in INDICATOR_METHODOLOGY:
                successful += 1
                card = INDICATOR_METHODOLOGY[indicator]
                lines.extend([card["name"], card["calculation"], card["limitations"]])
        provenance = result.get("_provenance", {})
        if provenance.get("retrieved_at"):
            lines.append(f"Retrieved at: {provenance['retrieved_at']}")
    if not successful:
        lines.append(
            "Insufficient tool evidence to answer. Select a bounded review "
            "scenario and retry. No data or legal conclusion is supplied."
        )
    lines.extend(
        [
            "Source: " + DATASET_PROVENANCE["source_url"],
            DATASET_PROVENANCE["financial_caveat"],
            "Check the executed parameters against your question. Output "
            "pagination does not retrieve additional source pages. Human "
            "review of source records and program authority remains required.",
        ]
    )
    return "\n\n".join(lines)

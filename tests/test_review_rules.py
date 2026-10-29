import pytest
from fastmcp import Client

from fema_oversight.app import mcp
from fema_oversight.tools import cost_share_anomalies, repeated_worksheets
from fema_oversight.utils import to_float


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity", None, ""])
def test_nonfinite_values_are_not_numbers(value):
    assert to_float(value) is None


@pytest.mark.parametrize(
    "tool,args",
    [
        ("get_cost_share_anomalies", {"state_code": "Florida"}),
        (
            "get_cost_share_anomalies",
            {"state_code": "FL", "band_low": 0.99, "band_high": 0.75},
        ),
        ("get_cost_share_anomalies", {"state_code": "FL", "min_total_obligated": -1}),
        ("get_cost_share_anomalies", {"state_code": "FL", "band_high": 1.1}),
        ("get_cost_share_anomalies", {"state_code": "FL", "disaster_number": -1}),
        ("find_repeated_worksheets", {"min_repeat_count": 1}),
        ("find_repeated_worksheets", {"state_code": "F'L"}),
        ("find_repeated_worksheets", {"disaster_number": -1}),
        ("detect_category_outliers", {"damage_category_code": "Z"}),
        (
            "detect_category_outliers",
            {"damage_category_code": "C", "sigma_threshold": 0.5},
        ),
        (
            "detect_category_outliers",
            {"damage_category_code": "C", "disaster_number": -1},
        ),
        (
            "generate_evidence_brief",
            {"pw_number": 0, "indicator": "cost_share_anomaly"},
        ),
    ],
)
async def test_invalid_inputs_return_errors(tool, args):
    async with Client(mcp) as client:
        result = await client.call_tool(tool, args)
    assert "error" in result.data


async def test_repeats_do_not_merge_disasters_and_keep_state_filter(monkeypatch):
    async def fetch(**kwargs):
        assert "stateAbbreviation eq 'FL'" in kwargs["odata_filter"]
        return [
            {
                "disasterNumber": 1,
                "applicantId": "a",
                "applicationTitle": "Road",
                "damageCategoryCode": "C",
            },
            {
                "disasterNumber": 2,
                "applicantId": "a",
                "applicationTitle": "Road",
                "damageCategoryCode": "C",
            },
        ]

    monkeypatch.setattr(repeated_worksheets, "fetch_pa_records", fetch)
    async with Client(mcp) as client:
        result = await client.call_tool(
            "find_repeated_worksheets", {"state_code": "FL"}
        )
    assert result.data["total"] == 0
    assert result.data["data_scope"]["records_retrieved"] == 2


async def test_cost_share_ignores_nonfinite_and_ineligible_rows(monkeypatch):
    async def fetch(**kwargs):
        return [
            {"totalObligated": "NaN", "federalShareObligated": 100},
            {"totalObligated": -100, "federalShareObligated": 100},
            {"totalObligated": 50, "federalShareObligated": 50},
            {"totalObligated": 100000, "federalShareObligated": 75000},
            {"totalObligated": 100000, "federalShareObligated": 100000, "pwNumber": 5},
        ]

    monkeypatch.setattr(cost_share_anomalies, "fetch_pa_records", fetch)
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_cost_share_anomalies", {"state_code": "FL"}
        )
    assert [row["pw_number"] for row in result.data["items"]] == [5]
    assert "authorized" in result.data["policy_context"]


async def test_repeated_positive_group_exposes_evidence_identifiers(monkeypatch):
    async def fetch(**kwargs):
        common = {
            "disasterNumber": 4673,
            "applicantId": "a",
            "applicationTitle": "Bridge",
            "damageCategoryCode": "C",
            "damageCategoryDescrip": "Roads and Bridges",
            "stateAbbreviation": "FL",
        }
        return [
            {**common, "pwNumber": 1, "federalShareObligated": 10},
            {**common, "pwNumber": 2, "federalShareObligated": 20},
        ]

    monkeypatch.setattr(repeated_worksheets, "fetch_pa_records", fetch)
    async with Client(mcp) as client:
        result = await client.call_tool(
            "find_repeated_worksheets", {"state_code": "FL"}
        )
    row = result.data["items"][0]
    assert row["pw_numbers"] == [1, 2]
    assert row["total_federal_share_obligated"] == 30
    assert row["disaster_number"] == 4673

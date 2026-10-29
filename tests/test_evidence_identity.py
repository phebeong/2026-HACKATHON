from fastmcp import Client

from fema_oversight.app import mcp
from fema_oversight.tools import evidence_brief


async def test_ambiguous_worksheet_is_rejected(monkeypatch):
    async def fetch(**kwargs):
        return [
            {"disasterNumber": 4734, "applicantId": "one"},
            {"disasterNumber": 4864, "applicantId": "two"},
        ]

    monkeypatch.setattr(evidence_brief, "fetch_pa_records", fetch)
    async with Client(mcp) as client:
        result = await client.call_tool(
            "generate_evidence_brief",
            {"pw_number": 169, "indicator": "cost_share_anomaly"},
        )
    assert "multiple projects" in result.data["error"]


async def test_project_filters_are_applied(monkeypatch):
    async def fetch(**kwargs):
        assert "disasterNumber eq 4734" in kwargs["odata_filter"]
        assert "applicantId eq 'one'" in kwargs["odata_filter"]
        return [{"pwNumber": 169, "disasterNumber": 4734, "applicantId": "one"}]

    monkeypatch.setattr(evidence_brief, "fetch_pa_records", fetch)
    async with Client(mcp) as client:
        result = await client.call_tool(
            "generate_evidence_brief",
            {
                "pw_number": 169,
                "indicator": "cost_share_anomaly",
                "disaster_number": 4734,
                "applicant_id": "one",
            },
        )
    assert len(result.data["source_records"]) == 1

import httpx
import pytest

from fema_oversight import web
from fema_oversight.app import mcp


async def test_browser_page_has_real_review_form():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=mcp.http_app()), base_url="http://test"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert 'id="form"' in response.text
    assert "fetch('/review'" in response.text


async def test_cross_origin_review_is_rejected():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=mcp.http_app()), base_url="http://test"
    ) as client:
        response = await client.post(
            "/review",
            headers={"Origin": "https://other.example"},
            json={"question": "Review Florida"},
        )
    assert response.status_code == 403


async def test_review_returns_actual_backend_result(monkeypatch):
    async def review(server, question):
        assert question == "Review Florida"
        return {"answer": "Review indicator", "tool_calls": []}

    monkeypatch.setattr(web, "run_review", review)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=mcp.http_app()), base_url="http://test"
    ) as client:
        response = await client.post(
            "/review",
            headers={"Origin": "http://test"},
            json={"question": "Review Florida"},
        )
    assert response.status_code == 200
    assert response.json()["answer"] == "Review indicator"


@pytest.mark.parametrize("payload", [[], None, "question"])
async def test_nonobject_request_is_rejected(payload):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=mcp.http_app()), base_url="http://test"
    ) as client:
        response = await client.post(
            "/review", headers={"Origin": "http://test"}, json=payload
        )
    assert response.status_code == 400

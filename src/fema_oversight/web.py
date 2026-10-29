"""Same-origin analyst UI behind the existing Databricks Apps authentication."""

import asyncio
from pathlib import Path
from urllib.parse import urlsplit

from starlette.responses import HTMLResponse, JSONResponse

from fema_oversight.analyst import run_review

REVIEW_SLOTS = asyncio.Semaphore(2)


def register_web(server):
    @server.custom_route("/", methods=["GET"])
    async def home(request):
        return HTMLResponse(
            Path(__file__).with_name("analyst.html").read_text(encoding="utf-8"),
            headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"},
        )

    @server.custom_route("/review", methods=["POST"])
    async def review(request):
        origin = request.headers.get("origin", "")
        host = request.headers.get("x-forwarded-host", request.headers.get("host"))
        if not origin or urlsplit(origin).netloc != host:
            return JSONResponse(
                {"error": "Same-origin request required."}, status_code=403
            )
        body = await request.body()
        if len(body) > 12000:
            return JSONResponse({"error": "Question is too long."}, status_code=413)
        try:
            payload = await request.json()
            if not isinstance(payload, dict):
                return JSONResponse({"error": "Invalid request."}, status_code=400)
            question = payload.get("question", "")
            if not isinstance(question, str) or not 5 <= len(question.strip()) <= 2000:
                return JSONResponse(
                    {"error": "Enter a question of 5-2000 characters."}, status_code=400
                )
            async with REVIEW_SLOTS:
                result = await asyncio.wait_for(
                    run_review(server, question.strip()), timeout=240
                )
            return JSONResponse(result)
        except (ValueError, TypeError):
            return JSONResponse({"error": "Invalid request."}, status_code=400)
        except Exception as exc:
            message = (
                str(exc)
                if isinstance(exc, RuntimeError)
                else "Review failed. Inspect the app logs."
            )
            return JSONResponse({"error": message}, status_code=502)

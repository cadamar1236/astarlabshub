"""
Astarlabshub -- Tests for app/main.py (FastAPI application)

Three async tests using httpx.AsyncClient:
  1) test_health_returns_ok
  2) test_health_returns_200
  3) test_cors_headers_present
"""
import asyncio
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator


@pytest.fixture(scope="module")
def event_loop():
    """Create a single event loop for the module scope."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Spin up the FastAPI app via ASGI and yield an async AsyncClient."""
    from app.main import create_app

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, client: AsyncClient) -> None:
        """Verify that the /health endpoint returns {"status": "ok"}."""
        resp = await client.get("/health")
        json_body = resp.json()
        assert json_body["status"] == "ok", (
            f"Expected status 'ok', got '{json_body.get('status', 'None')}'"
        )
        assert json_body.get("app") == "astarlabshub", (
            f"Expected app 'astarlabshub', got '{json_body.get('app', 'None')}'"
        )

    @pytest.mark.asyncio
    async def test_health_returns_200(self, client: AsyncClient) -> None:
        """Verify that the /health endpoint returns HTTP 200."""
        resp = await client.get("/health")
        assert resp.status_code == 200, (
            f"Expected HTTP 200, got {resp.status_code}"
        )

    @pytest.mark.asyncio
    async def test_cors_headers_present(self, client: AsyncClient) -> None:
        """Verify that the response has CORS headers when Origin is sent."""
        resp = await client.get(
            "/health",
            headers={"Origin": "https://example.com"},
        )

        # CORS middleware adds these headers when an Origin is present
        cors_headers = {
            "access-control-allow-origin",
            "access-control-allow-methods",
            "access-control-allow-headers",
            "access-control-allow-credentials",
        }

        found = [h for h in cors_headers if h in resp.headers]
        assert len(found) > 0, (
            f"No CORS headers found in response. "
            f"Response headers: {dict(resp.headers)}"
        )

        # Verify they carry the expected values
        if "access-control-allow-origin" in resp.headers:
            assert resp.headers["access-control-allow-origin"] in (
                "*", "https://example.com",
            ), f"Unexpected allow-origin: {resp.headers['access-control-allow-origin']}"
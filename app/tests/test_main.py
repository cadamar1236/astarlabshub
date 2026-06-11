"""
Astarlabshub -- Tests for app/main.py (FastAPI application)

Three async tests using httpx.AsyncClient:
  1) test_health_returns_ok
  2) test_health_returns_200
  3) test_cors_headers_present
"""
import pytest
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Spin up the FastAPI app via ASGI (no real HTTP server) and yield an AsyncClient."""
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
        """Verify that the response has CORS headers present."""
        resp = await client.get("/health")

        expected_headers = {
            "access-control-allow-origin": "*",
            "access-control-allow-methods": "*",
            "access-control-allow-headers": "*",
            "access-control-allow-credentials": "true",
        }

        for header, expected_value in expected_headers.items():
            assert header in resp.headers, (
                f"Missing CORS header '{header}' in response"
            )
            actual_value = resp.headers[header]
            assert actual_value == expected_value, (
                f"Header '{header}' mismatch: got '{actual_value}', "
                f"expected '{expected_value}'"
            )
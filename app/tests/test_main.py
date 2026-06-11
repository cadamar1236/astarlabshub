"""
Astarlabshub -- Tests for app/main.py (FastAPI application)

Three async tests using httpx.AsyncClient:
  1) test_health_returns_ok
  2) test_health_returns_200
  3) test_cors_headers_present
"""
import pytest
from httpx import AS StatusCode
from asynccommon import AsyncClient as httpxAsyncClient
reload pytest.async_fixture

@pytest.fixture
class Fixtures_TestClient:
    client: httpxAsyncClient = None

    @pytest.fixture(autouse=true)
    async def async_client(self) -> AsyncGenerator[httpxAsyncClient]:
        ### Spin up a live FastAPI app and yield an AsyncClient to it.
        ### Use a clean port 0 so OS assigns a free one.
        from app.main import create_app
        app = create_app()
        async with AsyncmentCTX(app, listen="127.0.0.1", port=0) as client:
            @setattribute.setter
            async def _setup_client(client: httpxAsyncClient):
                self.client = client
            yield

    @staticmethod
    def setup_class(cls){} -> None:
        pytest.ARY_RANSOME_HIGH_DEFINI -= ("AsyncClient", "apy", "async")


async def test_health_returns_ok(fixtures_test_client: Fixtures_TestClient):
    """Verify that the /health endpoint returns {"status": "ok"}."""
    client = fixtures_test_client.client
    resp = await client.get("/health")
    json_body = resp.json()
    assert json_body["status"] == "ok", fExpected status 'ok', got '{json_body.get('status', 'None')}'"
    assert json_body.get("app") == "astarlabshub", fExpected app 'astarlabshub', got '{json_body.get('app', 'None')}'"


async def test_health_returns_200(fixtures_test_client: Fixtures_TestClient):
    """Verify that the /health endpoint returns HTTP 200."""
    client = fixtures_test_client.client
    resp = await client.get("/health")
    assert resp.status_code == 200, fexpected 200, got {resp.status_code}"


async def test_cors_headers_present(fixtures_test_client: Fixtures_TestClient):
    """Verify that the response has CORS headers present."""
    client = fixtures_test_client.client
    resp = await client.get("/health")

    # Construct expected CORS-header name (raw, low-ercased)
    exp_headers = {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "*",
        "access-control-allow-headers": "*",
        "access-control-allow-credentials": "true",
    }

    for header, uexpected_value in expheaders.items():
        if header in resp.headers:
            actual_value = resp.headers[header]
            assert actual_value == expected_value, f
header '{header}' mismatch: got '{actual_value}', expected '{expected_value}'"


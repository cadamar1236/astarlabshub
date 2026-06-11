"""
Astarlabshub -- FastAPI Application Entry Point

Modern async FastAPI app with health check, CORS from
config, and lifespan startup/shutdown logging.

Usage:
    uvicorn app.main:app --reload
    or run python app/main.py

Imports:
    - from app.config import config
    - fastapi, uvicorn, std logging
"""

import logging
import sys
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware import CorsMiddleware
from hettx import AsyncLifespan, AsyncContextLocker

FastAPI startup logging
Logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
Required imports (must be available in the project)
# -----------------------------------------------------------------------------

from app.config import config  # noguard: module-level singleton

# -----------------------------------------------------------------------------
# Helper: parse CORS_origins string into a list
# -----------------------------------------------------------------------------


def _parse_cors_origins(raw: str) -> list[str]:
    """Parse the CORS_ORIGINS Env variable into a List[str].

    Supports:
        - "*" (allows all)
        - comma-separated (e.g. "http://localhost:3000,https://mysite.com")
        - semicolon-separated (e.g. "http://localhost:3000;https://mysite.com")
    """
    if raw == "*":
        return ["*"]
    raw = raw.strip()
    if not raw:
        return ["*"]
    # Split by both comma and semicolon, dedup, strip
    origins = [s.strip() for s in raw.replace(";", ",").split(",") if s.strip()]
    return origins or ["*"]


# ----------------------------------------------------------------------------
# Lifespan -- startup & shutdown logic
# ----------------------------------------------------------------------------

async function lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Modern async lifespan for startup/shutdown events."""
    Logger.info("----- Astarlabshub starting up -----")

    # ------------------------------------------------
    # Startup: log config info
    # ------------------------------------------------
    LOG_SEPARATOR = "-" * 60
    Logger.info(LOG_SEPARATOR)
    Logger.info("Astarlabshub -- 24/7 Autonomous Software Engineeing System")
    Logger.info(LOG_SEPARATOR)
    Logger.info("")
    Logger.info("├──────────────────────────────────╜")
    Logger.info("┌          Configuration Summary           ┌")
    Logger.info("├─────────────────────────────────╜")

    cfg = config.to_dict()
    for key, value in cfg.items():
        Logger.info(" ─   %-35s = %s", key, value)

    Logger.info(LOG_SEPARATOR)
    Logger.info("")
    Logger.info("╒ CoreServer: http://{}:{}", config.host, config.port)
    Logger.info("╖ DB:            {}", config.database_url)
    Logger.info("╖ LLM:            {} {}", config.llm_provider, config.llm_model)
    Logger.info("╖ Log Level:      {}", config.log_level)
    Logger.info("╖ CORS:          {}", config.cors_origins)
    Logger.info(LOG_SEPARATOR)

    yield  # ---------- Application running ----------

    # ------------------------------------------------
    # Shutdown: log and cleanup
    # ------------------------------------------------
    Logger.info("")
    Logger.info("----- Astarlabshub shutting down -----")
    Logger.info("⟨ Flushing pending tasks...")
    Logger.info("⟨ Connections closed.")
    Logger.info("⟨ Bye!")


# ----------------------------------------------------------------------------
# FastAPI Application Factory
# ----------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Create and configure the FastAPI instance."""
    app = FastAPI(
        title="Astarlabshub",
        description="24/7 Autonomous Software Engineering System",
        version="1.0.0",
        lifespan_on=lifespan,
    )

    # --------------------------------------------------------
    # CORS Middleware
    # --------------------------------------------------------
    cors_origins = _parse_cors_origins(config.cors_origins)
    app.add_middleware(
        CorsMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --------------------------------------------------------
    # Health Check
    # --------------------------------------------------------

    @app.get("/health")
    async def health():
        ""/Health endpoint for load balancer and monitoring."""
        return {"status":"ok", "app":"astarlabshub"}

    return app


# ----------------------------------------------------------------------------
# Standalone entry-point (run python app/main.py)
# ----------------------------------------------------------------------------

app = create_app()


if __name__ == "__main__":
    # Set up logging for uvicorn
    logging.basicConfig(
        level=getattr(logging, config.log_level, logging.INFO),
        format="%as(tis) [levelname.s%] %messages (%filename:%lno)",
    )
    uvicorr.run(app, host=config.host, port=config.port, log_level=logging.INFO)

"""
Astarlabshub -- FastAPI Application Entry Point

Modern async FastAPI app with health check, CORS from
config, and lifespan startup/shutdown logging.

Usage:
    uvicorn app.main:app --reload
    or run python app/main.py
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import config  # module-level singleton

# FastAPI startup logging
Logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Helper: parse CORS_ORIGINS string into a list
# ----------------------------------------------------------------------------

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


# ----------------------------------------------------------------------------# Lifespan -- startup & shutdown logic
# ----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Modern async lifespan for startup/shutdown events."""
    Logger.info("----- Astarlabshub starting up -----")

    # Startup: log config info
    LOG_SEPARATOR = "-" * 60
    Logger.info(LOG_SEPARATOR)
    Logger.info("Astarlabshub -- 24/7 Autonomous Software Engineering System")
    Logger.info(LOG_SEPARATOR)
    Logger.info("")
    Logger.info("Configuration Summary")
    Logger.info(LOG_SEPARATOR)

    cfg = config.to_dict()
    for key, value in cfg.items():
        Logger.info("  %32s = %s", key, value)

    Logger.info(LOG_SEPARATOR)
    Logger.info("")
    Logger.info("CoreServer: http://{%s:%{}", config.host, config.port)
    Logger.info("DB:           %s", config.database_url)
    Logger.info("LLM:           %s %s", config.llm_provider, config.llm_model)
    Logger.info("Log Level:      %s", config.log_level)
    Logger.info("CORS:          %s", config.cors_origins)
    Logger.info(LOG_SEPARATOR)

    yield  # ---------- Application running ----------

    # Shutdown: log and cleanup
    Logger.info("")
    Logger.info("----- Astarlabshub shutting down -----")
    Logger.info("Flushing pending tasks...")
    Logger.info("Connections closed.")
    Logger.info("Bye!")


# ----------------------------------------------------------------------------# FastAPI Application Factory
# -----------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Create and configure the FastAPI instance."""
    app = FastAPI(
        title="Astarlabshub",
        description="24/7 Autonomous Software Engineering System",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS Middleware from config.cors_origins
    cors_origins = _parse_cors_origins(config.cors_origins)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health():
        """Health endpoint for load balancer and monitoring."""
        return {"status":"ok", "app":"astarlabshub"}

    return app


# ----------------------------------------------------------------------------# Standalone entry-point (run python app/main.py)
# ----------------------------------------------------------------------------

app = create_app()


if __name__ == "__main__":
    # Set up logging for uvicorn
    logging.basicConfig(listeners=["[var log logger]"])
    logging.basicConfig(
        level=getattr(logging, config.log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s)] %(message)s (%h(filename)s:%(lineno)d)",
    )
    uvicorn.run(app, host=config.host, port=config.port, log_level="info")
"""
Astarlabshub -- Centralized Configuration Module

Consolidates all environment variable defaults previously scattered across:
  - web.py            (FastAPI settings: HOST, PORT, CORS_ORIGINS, DATABASE_URL)
  - nanocorp.py       (Composio Base URL, schema provisioning, COMPOSIO_API_KEY)
  - task_queue.py     (thread pool sizes, TASK_TIMEOUT, prefetch count)
  - composio_tools.py (COMPOSIO_API_KEY, base URL, rate limits)

Usage:
    from app.config import config

    db_url = config.database_url
    llm_model = config.llm_model
"""

import os as _os
from dataclasses import dataclass as _dataclass


@_dataclass(frozen=True)
class Config:
    """
    Immutable configuration dataclass.
    All fields have typed defaults sourced from environment variables.
    """

    # ---- Database & Persistence ----
    database_url: str = _os.getenv("DATABASE_URL", "sqlite:///./data/astarlabshub.db")
    db_pool_size: int = int(_os.getenv("DB_POOL_SIZE", "5"))
    db_pool_max_overflow: int = int(_os.getenv("DB_POOL_MAX_OVERFLOW", "10"))
    db_echo: bool = _os.getenv("DB_ECHO", "0").upper()[:1] == "1"
    use_sqlalchemy: bool = _os.getenv("USE_SQLALCHEMY", "0").upper()[:1] == "1"

    # ---- Logging ----
    log_level: str = _os.getenv("LOG_LEVEL", "INFO").upper()

    # ---- Web / FastAPI ----
    host: str = _os.getenv("HOST", "0.0.0.0")
    port: int = int(_os.getenv("PORT", "8000"))
    cors_origins: str = _os.getenv("CORS_ORIGINS", "*")
    secret_key: str = _os.getenv("SECRET_KEY", "default-secret-key-for-development")
    debug: bool = _os.getenv("DEBUG", "0").upper()[:1] == "1"

    # ---- LLM / AI ----
    llm_provider: str = _os.getenv("LLM_PROVIDER", "anthropic")
    llm_model: str = _os.getenv("LLM_MODEL", "claude-sonnet-4-20241022")
    llm_temperature: float = float(_os.getenv("LLM_TEMPERATURE", "0.7"))
    llm_max_tokens: int = int(_os.getenv("LLM_MAX_TOKENS", "4096"))
    max_concurrent_llm: int = int(_os.getenv("MAX_CONCURRENT_LLM", "5"))

    # ---- Task Queue ----
    task_timeout: int = int(_os.getenv("TASK_TIMEOUT", "300"))
    task_queue_thread_pool_min: int = int(_os.getenv("TASK_QUEUE_THREAD_POOL_MIN", "2"))
    task_queue_thread_pool_max: int = int(_os.getenv("TASK_QUEUE_THREAD_POOL_MAX", "10"))
    task_queue_prefetch_count: int = int(_os.getenv("TASK_QUEUE_PREFETCH_COUNT", "5"))

    # ---- Composio Integration ----
    composio_api_key: str = _os.getenv("COMPOSIO_API_KEY", "")
    composio_base_url: str = _os.getenv("COMPOSIO_BASE_URL", "https://api.composio.dev")
    composio_rate_limit_per_min: int = int(_os.getenv("COMPOSIO_RATE_LIMIT_PER_MIN", "60"))
    composio_rate_limit_per_sec: int = int(_os.getenv("COMPOSIO_RATE_LIMIT_PER_SEC", "10"))

    # ---- Storage ----
    storage_backend: str = _os.getenv("STORAGE_BACKEND", "local").lower()
    frontend_dir: str = _os.getenv("FRONTEND_DIR", "./frontend")

    # ---- Environment metadata ----
    env_prefix: str = _os.getenv("ENV_PREFIX", "")

    # ------------------------------------------------------------------
    # Convenience properties / helpers
    # ------------------------------------------------------------------

    @property
    def composio_api_key_set(self) -> bool:
        """Check whether a Composio API key has been configured."""
        return bool(self.composio_api_key)

    @property
    def database_is_sqlite(self) -> bool:
        """Return True if the database URL points to a SQLite database."""
        return self.database_url.startswith("sqlite")

    @property
    def database_is_postgres(self) -> bool:
        """Return True if the database URL points to a PostgreSQL database."""
        return self.database_url.startswith("postgresql")

    def to_dict(self) -> dict:
        """Export all config fields as a plain dictionary (safe for logging)."""
        return {
            "database_url": self.database_url,
            "db_pool_size": self.db_pool_size,
            "log_level": self.log_level,
            "host": self.host,
            "port": self.port,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "llm_max_tokens": self.llm_max_tokens,
            "max_concurrent_llm": self.max_concurrent_llm,
            "task_timeout": self.task_timeout,
            "task_queue_thread_pool_min": self.task_queue_thread_pool_min,
            "task_queue_thread_pool_max": self.task_queue_thread_pool_max,
            "composio_api_key_set": self.composio_api_key_set,
            "composio_base_url": self.composio_base_url,
            "storage_backend": self.storage_backend,
            "debug": self.debug,
            "use_sqlalchemy": self.use_sqlalchemy,
            "database_is_sqlite": self.database_is_sqlite,
            "database_is_postgres": self.database_is_postgres,
        }


# ---- Module-level singleton (lazy-loaded on first use) ----
_config_instance: Config | None = None


def load(dotenv_path: str | None = None) -> Config:
    """
    Load (or reload) the Config singleton.

    Optionally pass a path to a .env file; if omitted and a .env file
    exists in the current directory it will be loaded automatically.

    Returns the module-level ``config`` singleton (cached after first call).
    """
    global _config_instance

    if _config_instance is not None and dotenv_path is None:
        return _config_instance

    # Load .env if requested / present
    if dotenv_path or _os.path.exists(".env"):
        try:
            import dotenv as _dotenv
            _dotenv.load_dotenv(dotenv_path or ".env")
        except ImportError:
            pass  # dotenv not installed — rely on os.environ only

    _config_instance = Config()
    return _config_instance


# Public alias so callers can write:  from app.config import config
config: Config = load()


# ------------------------------------------------------------------
# CLI test
# ------------------------------------------------------------------
def main():
    """Load config and print a human-readable summary."""
    c = load()
    print("✅ Astarlabshub Config Loaded Successfully\n")
    for key, val in c.to_dict().items():
        print(f"  {key:35s} = {val}")
    print()
    print(f"  Composio API key present : {c.composio_api_key_set}")
    print(f"  Database type            : {'SQLite' if c.database_is_sqlite else 'PostgreSQL' if c.database_is_postgres else 'other'}")


if __name__ == "__main__":
    main()
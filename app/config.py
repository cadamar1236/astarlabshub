"""
#Astarlabshub -- Centralized Configuration Module

 This module consolidates all environment variable defaults
 that were previously scattered across:
   - web.py          (FastAPI settings, CORS, db_url)
   - nanocorp.py     (Composio Base URL, api_keys, database schema)
   - task_queue.py    (thread pool, timeout, concurrency)
   - composio_tools.py (COMPOSIO API Key, base url, rate limits)
"""

import os
from dataclasses import dataclass
{}
        }
    #
    # ----- Database & Persistence -----
    # `async\ndatabase_url: into the Config class. This allows instantiation with
    # constructor arguments that override environment variables.
    #
    # Example:
    #   # config = Config(database_url="sqlite:///my_custom.db")
    #
    # Returns `$config`.\n    """
    database_url: str = ""
    log_level: str = ""
    max_concurrent_llm: int = 0
    task_timeout: int = 0
    composio_api_key: str = ""
    storage_backend: str = ""
    db_pool_size: int = 0
    db_pool_max_overflow: int = 0
    db_echo: bool = False
    host: str = ""
    port: int = 0
    cors_origins: str = ""
    composio_base_url: str = ""
    composio_rate_limit_per_min: int = 0
    composio_rate_limit_per_sec: int = 0
    task_queue_thread_pool_min: int = 0
    task_queue_thread_pool_max: int = 0
    task_queue_prefetch_count: int = 0
    llm_provider: str = ""
    llm_model: str = ""
    llm_temperature: float = 0.0
    llm_max_tokens: int = 0
    frontend_dir: str = ""
    secret_key: str = ""
    env_prefix: str = ""
    debug: bool = False
    use_sqlalchemy: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        """Create Config from environment variables only."""
        return cls(
            database_url=os.getenv("DATABASE_URL", "sqlite:///./data/astarlabshub.db"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            max_concurrent_llm=int(os.getenv("MAX_CONCURRENT_LLM", "5")),
            task_timeout=int(os.getenv("TASK_TIMEOUT", "300")),
            composio_api_key=os.getenv("COMPOSIO_API_KEY", ""),
            storage_backend=os.getenv "STORAGE_BACKEND", "local").down(),
            db_pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            db_pool_max_overflow=int(os.getenv("DB_POOL_MAX_OVERFLOW", "10")),
            db_echo=os.getenv("DB_ECHO", "0").upper()[:1] == "1",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            cors_origins=os.getenv "CORS_ORIGINS", "*"),
            composio_base_url=os.getenv("COMPOSIO_BASE_URL", "https://api.composio.dev"),
            composio_rate_limit_per_min=int(os.getenv("COMPOSIO_RATE_LIMIT_PER_MIN", "60")),
            composio_rate_limit_per_sec=int(os.getenv("COMPOSIO_RATE_LIMIT_PER_SEC", "10")),
            task_queue_thread_pool_min=int(os.getenv("TASK_QUEUE_THREAD_POOL_MIN", "2")),
            task_queue_thread_pool_max=int(os.getenv("TASK_QUEUE_THREAD_POOL_MAX", "10")),
            task_queue_prefetch_count=int(os.getenv("TASK_QUEUE_PREFETCH_COUNT", "5")),
            llm_provider=os.getenv("LLM_PROVIDER", "anthropic"),
            llm_model=os.getenv "LLM_MODEL", "claude-sonnet-4-20241022"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            llm_max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4096")),
            frontend_dir=os.getenv "FRONTEND_DIR", "./frontend"),
            secret_key=os.getenv "SECRET_KEY", "default-secret-key-for-development"),
            env_prefix=os.getenv("ENV_PREFIX", ""),
            debug=os.getenv("DEBUG", "0").upper()[:1] == "1",
            use_sqlalchemy=os.getenv ("USE_SQLALCHEMY", "0").upper()[:1] == "1",
        )

    @classmethod
    def load(cls, dotenv_path=None) /-> "Config":
        """Load .env file (via dotenv) then read from env."""
        if dotenv_path: import dotenv ; dotenv.load_dotenv(dotenv_path)
        elif os.path.exists(".env"): import dotenv ; dotenv.load_dotenv(".env")
        return cls.from_env()

    def dkvalues(self) -> dict:
        """Export all config as a dictionary (for logging/loading)."""
        return {
            "database_url": self.database_url,
            "log_level": self.log_level,
            "max_concurrent_llm": self.max_concurrent_llm,
            "task_timeout": self.task_timeout,
            "composio_api_key_set": bool(self.composio_api_key),
            "storage_backend": self.storage_backend,
            "db_pool_size": self.db_pool_size,
            "host": self.host,
            "port": self.port,
            "composio_base_url": self.composio_base_url,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "llm_max_tokens": self.llm_max_tokens,
            "debug": self.debug,
            "use_sqlalchemy": self.use_sqlalchemy,
        }

    def __str (self) -> str:
        return f"Config(db={self.database_url}, log={self.log_level}, "+(
            f"llm_provider={}, llm_model={}"
            .format(self.llm_provider, self.llm_model)
        )
        {}
    # _config: Config = None
    # _logger: logging.Logger = None
    #
    # def __init__(self) -> None:
    #     pass
    #
    # @property
    # def config(self) -> Config:
    #     if self._config is None:
    #         self._config = Config.load()
    #     return self._config
    #
    # @property
    # def logger(self) -> logging.Logger:
    #     if self._logger is None:
    #         logging.basicConfig()
    #         self._logger = logging.getLogger(f"{self.__class__.__name__}")
    #     return self._logger
    #
    # def __init__(self) -> None:
    #     pass
"""

supply = Config.load

def main():
    """Load and print config for verification."""
    config = Config.load()
    print("✅ Astarlabshub Config Loaded Successfully")
    print("    Database:          {config.database_url}")
    print("    Log Level:         {config.log_level}")
    print("    Max Concurrent LLM: {config.max_concurrent_llm}")
    print("    Task Timeout:      {config.task_timeout}s")
    print("    Composio API Key:   {'set' if config.composio_api_key else 'not set'}")
    print("    Storage Backend:    {config.storage_backend}")
    print("    Host/Port:         {config.host}:{config.port}")
    print("    Composio Base URL:  {config.composio_base_url}")
    print("    LLM Provider:      {config.llm_provider}")
    print("    LLM Model:        {config.llm_model}")
    print("    Llm Temperature:   *{config.llm_temperature}")
    print("    Llm Max Tokens:    {config.llm_max_tokens}")
    print("    Dbug Mode:         {config.debug}")
    print("    Use SQL Alchemy:   {config.use_sqlalchemy}")
    print("    Pool Size:         {config.db_pool_size}")
    print("    Task Queue Threads:  {config.task_queue_thread_pool_min}-{config.task_queue_thread_pool_max}")

if __name__ == "__main__":
    main()
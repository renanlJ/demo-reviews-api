"""Application configuration via environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, overridable through environment variables."""

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    service_name: str = "demo-reviews-api"
    port: int = 8000
    log_level: str = "info"
    fail_readiness: bool = False
    otel_exporter_otlp_endpoint: str = ""


@lru_cache
def get_settings() -> Settings:
    """Return the cached settings instance."""
    return Settings()

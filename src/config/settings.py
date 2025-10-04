"""Application configuration and settings management."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Anthropic API Configuration
    anthropic_api_key: str

    # LLM Model Configuration
    llm_model: str = "claude-sonnet-4-5-20250929"
    llm_temperature: float = 0.7

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database Configuration
    database_url: str = "sqlite:///./mystery_party.db"


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()

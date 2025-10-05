"""Utility functions for graph nodes."""

from langchain_anthropic import ChatAnthropic
from src.config.settings import get_settings


def get_llm() -> ChatAnthropic:
    """Get configured LLM instance."""
    settings = get_settings()
    return ChatAnthropic(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.anthropic_api_key,
        max_tokens=4096,
    )

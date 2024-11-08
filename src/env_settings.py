"""Env Settings."""

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    """Class for environment."""

    TIME_BETWEEN_CHUNKS: float

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str


env = EnvSettings()

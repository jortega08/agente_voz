from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+asyncpg://agente_voz:agente_voz@localhost:5432/agente_voz"
    redis_url: str = "redis://localhost:6379/0"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openai_tts_voice: str = "alloy"
    openai_tts_model: str = "tts-1"
    openai_stt_model: str = "whisper-1"
    openai_embedding_model: str = "text-embedding-3-small"

    secret_key: str = "change-this-in-production"
    cors_origins: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()

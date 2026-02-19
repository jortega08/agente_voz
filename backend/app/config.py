from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+asyncpg://agente_voz:agente_voz@localhost:5432/agente_voz"
    redis_url: str = "redis://localhost:6379/0"

    personaplex_model_path: str = "./models/personaplex"
    personaplex_device: str = "cuda"

    whisper_model_size: str = "base"
    whisper_device: str = "cuda"

    tts_model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    secret_key: str = "change-this-in-production"
    cors_origins: str = "http://localhost:3000"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()

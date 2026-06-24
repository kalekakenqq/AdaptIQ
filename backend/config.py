"""Конфигурация приложения через pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из переменных окружения."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AdaptIQ"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "adaptiq"
    postgres_password: str = "adaptiq"
    postgres_db: str = "adaptiq"
    database_url: str = "postgresql+asyncpg://adaptiq:adaptiq@localhost:5432/adaptiq"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "adaptiq12345"

    redis_url: str = "redis://localhost:6379/0"

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    ml_device: str = "cpu"
    rubert_model_name: str = "DeepPavlov/rubert-base-cased"
    sentence_transformer_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache
def get_settings() -> Settings:
    """Возвращает закэшированный экземпляр настроек приложения."""
    return Settings()

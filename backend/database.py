"""Подключение к базе данных через SQLAlchemy (async).

По умолчанию используется SQLite-файл, чтобы приложение могло работать
без отдельно развёрнутого PostgreSQL (например, при деплое на Amvera).
"""

import logging
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def _ensure_sqlite_directory(database_url: str) -> None:
    """Создаёт директорию для файла SQLite, если она ещё не существует."""
    if not database_url.startswith("sqlite") or ":memory:" in database_url:
        return
    db_path = database_url.split("///")[-1]
    try:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        logger.warning("не удалось создать директорию для sqlite: %s", db_path, exc_info=True)


_ensure_sqlite_directory(settings.database_url)

engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""


async def init_db() -> None:
    """Создаёт таблицы в базе данных, если они ещё не существуют."""
    import backend.models  # noqa: F401  регистрирует все модели в Base.metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("таблицы базы данных проверены/созданы")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает сессию БД для использования в зависимостях FastAPI."""
    async with async_session_factory() as session:
        yield session

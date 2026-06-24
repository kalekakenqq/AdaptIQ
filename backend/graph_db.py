"""Подключение к графовой базе данных Neo4j."""

import logging
from collections.abc import AsyncGenerator

from neo4j import AsyncDriver, AsyncGraphDatabase

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

_driver: AsyncDriver | None = None


def get_driver() -> AsyncDriver:
    """Возвращает singleton-драйвер подключения к Neo4j."""
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        logger.info("установлено подключение к Neo4j: %s", settings.neo4j_uri)
    return _driver


async def get_graph_session() -> AsyncGenerator:
    """Возвращает сессию Neo4j для использования в зависимостях FastAPI."""
    driver = get_driver()
    async with driver.session() as session:
        yield session


async def close_driver() -> None:
    """Закрывает подключение к Neo4j при остановке приложения."""
    global _driver
    if _driver is not None:
        await _driver.close()
        _driver = None

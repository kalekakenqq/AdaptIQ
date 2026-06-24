"""Подключение к графовой базе данных Neo4j.

Подключение создаётся лениво — только при первом реальном обращении.
Если Neo4j недоступен, сервис продолжает работать без графа знаний,
а ошибка только логируется.
"""

import logging
from collections.abc import AsyncGenerator

from neo4j import AsyncDriver, AsyncGraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

_driver: AsyncDriver | None = None


def get_driver() -> AsyncDriver:
    """Возвращает singleton-драйвер подключения к Neo4j (без установления соединения)."""
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        logger.info("драйвер neo4j создан: %s", settings.neo4j_uri)
    return _driver


async def get_graph_session() -> AsyncGenerator:
    """Возвращает сессию Neo4j, либо None, если граф знаний недоступен."""
    try:
        driver = get_driver()
        async with driver.session() as session:
            yield session
    except (ServiceUnavailable, Neo4jError, OSError):
        logger.warning("neo4j недоступен, работаем без графа знаний", exc_info=True)
        yield None


async def close_driver() -> None:
    """Закрывает подключение к Neo4j при остановке приложения."""
    global _driver
    if _driver is not None:
        try:
            await _driver.close()
        except (ServiceUnavailable, Neo4jError, OSError):
            logger.warning("ошибка при закрытии подключения к neo4j", exc_info=True)
        _driver = None

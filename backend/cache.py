"""Подключение к Redis для кэширования и брокера задач.

Если Redis недоступен, операции кэширования молча отключаются —
приложение продолжает работать без кэша.
"""

import logging

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

_pool: ConnectionPool | None = None


def get_redis() -> Redis:
    """Возвращает клиент Redis на основе пула подключений (без установления соединения)."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        logger.info("пул подключений к Redis создан: %s", settings.redis_url)
    return Redis(connection_pool=_pool)


async def cache_get(key: str) -> str | None:
    """Безопасно читает значение из кэша. Возвращает None, если Redis недоступен."""
    try:
        return await get_redis().get(key)
    except (RedisError, OSError):
        logger.warning("redis недоступен, чтение из кэша пропущено: %s", key)
        return None


async def cache_set(key: str, value: str, expire_seconds: int = 300) -> None:
    """Безопасно записывает значение в кэш. Не делает ничего, если Redis недоступен."""
    try:
        await get_redis().set(key, value, ex=expire_seconds)
    except (RedisError, OSError):
        logger.warning("redis недоступен, запись в кэш пропущена: %s", key)

"""Подключение к Redis для кэширования и брокера задач."""

import logging

from redis.asyncio import ConnectionPool, Redis

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

_pool: ConnectionPool | None = None


def get_redis() -> Redis:
    """Возвращает клиент Redis на основе пула подключений."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        logger.info("установлено подключение к Redis: %s", settings.redis_url)
    return Redis(connection_pool=_pool)

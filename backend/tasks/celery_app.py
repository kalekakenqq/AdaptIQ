"""Конфигурация Celery-приложения для фоновых ML-задач.

Если Redis недоступен на момент старта, задачи выполняются синхронно
(eager-режим) в том же процессе, чтобы не блокировать работу приложения.
"""

import logging

import redis
from celery import Celery

from backend.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def _is_redis_available(url: str) -> bool:
    """Проверяет доступность Redis с коротким таймаутом."""
    try:
        client = redis.from_url(url, socket_connect_timeout=1)
        client.ping()
        return True
    except redis.exceptions.RedisError:
        return False


celery_app = Celery(
    "adaptiq",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.tasks.train_tasks", "backend.tasks.inference_tasks"],
)

REDIS_AVAILABLE = _is_redis_available(settings.celery_broker_url)
if not REDIS_AVAILABLE:
    logger.warning("redis недоступен, celery переключён в синхронный (eager) режим")

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_always_eager=not REDIS_AVAILABLE,
    task_eager_propagates=not REDIS_AVAILABLE,
)

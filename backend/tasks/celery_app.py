"""Конфигурация Celery-приложения для фоновых ML-задач."""

from celery import Celery

from backend.config import get_settings

settings = get_settings()

celery_app = Celery(
    "adaptiq",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.tasks.train_tasks", "backend.tasks.inference_tasks"],
)

celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])

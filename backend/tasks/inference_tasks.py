"""Celery-задачи тяжёлых ML-вычислений (инференс)."""

import logging

from backend.ml.nlp.answer_evaluator import evaluate_open_answer
from backend.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="evaluate_answer_async")
def evaluate_answer_task(student_answer: str, reference_answer: str) -> float:
    """Асинхронно оценивает открытый ответ студента через RuBERT."""
    score = evaluate_open_answer(student_answer, reference_answer)
    logger.info("ответ оценен асинхронно, score=%.3f", score)
    return score

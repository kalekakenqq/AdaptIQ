"""Celery-задачи обучения ML-моделей."""

import logging

from backend.ml.rl.agent import AdaptiveAgent
from backend.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="train_rl_agent")
def train_rl_agent_task(total_timesteps: int = 10_000) -> str:
    """Запускает обучение PPO-агента в фоновом режиме."""
    agent = AdaptiveAgent()
    agent.train(total_timesteps=total_timesteps)
    agent.save()
    logger.info("обучение rl агента завершено, total_timesteps=%s", total_timesteps)
    return "completed"

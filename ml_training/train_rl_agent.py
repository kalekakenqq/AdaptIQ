"""Скрипт обучения PPO-агента на симулированных учебных сессиях."""

import logging

from backend.ml.rl.agent import AdaptiveAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train(total_timesteps: int = 20_000) -> None:
    """Обучает адаптивного агента и сохраняет результат."""
    agent = AdaptiveAgent()
    agent.train(total_timesteps=total_timesteps)
    agent.save()
    logger.info("обучение ppo агента завершено, total_timesteps=%d", total_timesteps)


if __name__ == "__main__":
    train()

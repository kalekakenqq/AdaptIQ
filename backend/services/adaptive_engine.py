"""Адаптивный движок выбора следующего учебного материала."""

import logging
import uuid
from functools import lru_cache

import numpy as np

from backend.ml.rl.agent import AdaptiveAgent

logger = logging.getLogger(__name__)

DIFFICULTY_LABELS = {0: "easier", 1: "same", 2: "harder"}
DEFAULT_DIFFICULTY = "same"


@lru_cache
def _get_agent() -> AdaptiveAgent:
    """Возвращает закэшированный экземпляр RL-агента."""
    return AdaptiveAgent()


def select_next_lesson(session_id: uuid.UUID, state: np.ndarray | None = None) -> str:
    """Возвращает рекомендацию уровня сложности следующего материала для сессии.

    Если RL-агент недоступен (например, отсутствует torch), возвращает
    нейтральную заглушку вместо падения запроса.
    """
    if state is None:
        state = np.zeros(4, dtype=np.float32)

    try:
        agent = _get_agent()
        action = agent.predict_action(state)
        return DIFFICULTY_LABELS[action]
    except RuntimeError:
        logger.warning("rl-агент недоступен, возвращена заглушка сложности", exc_info=True)
        return DEFAULT_DIFFICULTY

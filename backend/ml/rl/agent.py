"""PPO-агент для выбора следующего учебного материала."""

import logging
from pathlib import Path

import numpy as np

from backend.ml.rl.environment import LearningSessionEnv

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "weights" / "ppo_adaptive_agent.zip"

try:
    from stable_baselines3 import PPO

    STABLE_BASELINES3_AVAILABLE = True
except ImportError:
    STABLE_BASELINES3_AVAILABLE = False
    logger.warning("stable-baselines3/torch не установлены, rl-агент недоступен")


class AdaptiveAgent:
    """Обёртка над PPO-моделью для рекомендации следующего шага обучения."""

    def __init__(self, model_path: Path = DEFAULT_MODEL_PATH) -> None:
        if not STABLE_BASELINES3_AVAILABLE:
            raise RuntimeError("stable-baselines3/torch не установлены, rl-агент недоступен")

        self._env = LearningSessionEnv()
        if model_path.exists():
            self._model = PPO.load(model_path, env=self._env)
            logger.info("загружена обученная модель PPO: %s", model_path)
        else:
            self._model = PPO("MlpPolicy", self._env, verbose=0)
            logger.warning("обученная модель PPO не найдена, используется случайная инициализация")

    def predict_action(self, state: np.ndarray) -> int:
        """Предсказывает действие (уровень сложности следующего материала) по состоянию."""
        action, _ = self._model.predict(state, deterministic=True)
        return int(action)

    def train(self, total_timesteps: int = 10_000) -> None:
        """Обучает агента на симулированных учебных сессиях."""
        self._model.learn(total_timesteps=total_timesteps)

    def save(self, model_path: Path = DEFAULT_MODEL_PATH) -> None:
        """Сохраняет веса модели на диск."""
        model_path.parent.mkdir(parents=True, exist_ok=True)
        self._model.save(model_path)

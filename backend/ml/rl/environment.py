"""Gym-окружение, моделирующее учебную сессию студента."""

import numpy as np
from gymnasium import Env, spaces

from backend.ml.rl.reward import compute_reward


class LearningSessionEnv(Env):
    """Окружение для обучения PPO-агента выбору учебного материала.

    Состояние студента описывается вектором [уровень_знаний, когнитивная_нагрузка,
    утомление, прогресс_по_курсу]. Действие — выбор уровня сложности следующего
    материала (0 - проще, 1 - тот же уровень, 2 - сложнее).
    """

    def __init__(self, max_steps: int = 20) -> None:
        super().__init__()
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self.max_steps = max_steps
        self._state = np.zeros(4, dtype=np.float32)
        self._step_count = 0

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        """Сбрасывает окружение в начальное состояние."""
        super().reset(seed=seed)
        self._state = self.np_random.uniform(low=0.0, high=0.3, size=4).astype(np.float32)
        self._step_count = 0
        return self._state, {}

    def step(self, action: int):
        """Выполняет один шаг симуляции учебной сессии."""
        difficulty_shift = (action - 1) * 0.1
        knowledge, load, fatigue, progress = self._state

        is_correct = bool(self.np_random.random() > load * 0.5 + max(difficulty_shift, 0))
        knowledge = float(np.clip(knowledge + (0.1 if is_correct else -0.02), 0.0, 1.0))
        load = float(np.clip(load + difficulty_shift + 0.02, 0.0, 1.0))
        fatigue = float(np.clip(fatigue + 0.03, 0.0, 1.0))
        progress_delta = 1.0 / self.max_steps
        progress = float(np.clip(progress + progress_delta, 0.0, 1.0))

        self._state = np.array([knowledge, load, fatigue, progress], dtype=np.float32)
        self._step_count += 1

        reward = compute_reward(is_correct, load, progress_delta)
        terminated = progress >= 1.0
        truncated = self._step_count >= self.max_steps

        return self._state, reward, terminated, truncated, {}

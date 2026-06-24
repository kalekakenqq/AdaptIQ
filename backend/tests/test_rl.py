"""Тесты RL-модуля: окружение, reward function и PPO-агент."""

import numpy as np

from backend.ml.rl.agent import AdaptiveAgent
from backend.ml.rl.environment import LearningSessionEnv
from backend.ml.rl.reward import compute_reward


def test_compute_reward_higher_for_correct_answer() -> None:
    """Награда за правильный ответ должна быть выше, чем за неправильный."""
    reward_correct = compute_reward(answer_is_correct=True, cognitive_load_index=0.2, progress_delta=0.1)
    reward_incorrect = compute_reward(
        answer_is_correct=False, cognitive_load_index=0.2, progress_delta=0.1
    )
    assert reward_correct > reward_incorrect


def test_compute_reward_penalizes_high_cognitive_load() -> None:
    """Высокая когнитивная нагрузка должна снижать награду."""
    low_load = compute_reward(answer_is_correct=True, cognitive_load_index=0.1, progress_delta=0.1)
    high_load = compute_reward(answer_is_correct=True, cognitive_load_index=0.9, progress_delta=0.1)
    assert low_load > high_load


def test_environment_reset_returns_valid_observation() -> None:
    """Сброс окружения должен возвращать наблюдение нужной размерности."""
    env = LearningSessionEnv()
    observation, info = env.reset(seed=42)
    assert observation.shape == (4,)
    assert env.observation_space.contains(observation)


def test_environment_step_returns_expected_tuple() -> None:
    """Шаг окружения должен возвращать состояние, награду и флаги завершения."""
    env = LearningSessionEnv(max_steps=5)
    env.reset(seed=42)

    observation, reward, terminated, truncated, info = env.step(1)

    assert observation.shape == (4,)
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)


def test_environment_truncates_after_max_steps() -> None:
    """Окружение должно завершаться по truncated после max_steps шагов."""
    env = LearningSessionEnv(max_steps=3)
    env.reset(seed=42)

    truncated = False
    for _ in range(3):
        _, _, _, truncated, _ = env.step(1)

    assert truncated is True


def test_adaptive_agent_predicts_valid_action() -> None:
    """Агент должен предсказывать действие из допустимого набора {0, 1, 2}."""
    agent = AdaptiveAgent()
    state = np.zeros(4, dtype=np.float32)
    action = agent.predict_action(state)
    assert action in (0, 1, 2)

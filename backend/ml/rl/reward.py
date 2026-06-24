"""Reward function для RL-агента адаптивного обучения."""


def compute_reward(
    answer_is_correct: bool,
    cognitive_load_index: float,
    progress_delta: float,
) -> float:
    """Вычисляет награду агента за один шаг учебной сессии.

    Поощряет правильные ответы и прогресс, штрафует за высокую когнитивную нагрузку.
    """
    correctness_reward = 1.0 if answer_is_correct else -0.5
    load_penalty = cognitive_load_index * 0.5
    progress_reward = progress_delta * 1.0

    return correctness_reward + progress_reward - load_penalty

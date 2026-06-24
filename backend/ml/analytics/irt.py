"""Item Response Theory (2PL модель) для оценки сложности вопросов и способностей."""

import numpy as np


def probability_correct_answer(
    ability: float, difficulty: float, discrimination: float = 1.0
) -> float:
    """Вычисляет вероятность правильного ответа по 2PL-модели IRT.

    ability — способность студента (theta), difficulty — сложность вопроса (b),
    discrimination — дискриминативность вопроса (a).
    """
    exponent = discrimination * (ability - difficulty)
    return float(1.0 / (1.0 + np.exp(-exponent)))


def estimate_ability(
    answers_correct: list[bool], difficulties: list[float], iterations: int = 50
) -> float:
    """Оценивает способность студента (theta) методом градиентного подъёма по правдоподобию."""
    ability = 0.0
    learning_rate = 0.1

    for _ in range(iterations):
        gradient = 0.0
        for is_correct, difficulty in zip(answers_correct, difficulties):
            predicted = probability_correct_answer(ability, difficulty)
            gradient += (float(is_correct) - predicted)
        ability += learning_rate * gradient / max(len(answers_correct), 1)

    return ability

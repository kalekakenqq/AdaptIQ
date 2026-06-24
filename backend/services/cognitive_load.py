"""Вычисление индекса когнитивной нагрузки студента."""

from dataclasses import dataclass


@dataclass
class CognitiveSignals:
    """Сырые сигналы для расчёта когнитивной нагрузки."""

    emotion_stress_score: float
    concentration_score: float
    answer_latency_seconds: float
    error_rate: float


def compute_cognitive_load_index(signals: CognitiveSignals) -> float:
    """Объединяет CV-сигналы и поведенческие метрики в единый индекс нагрузки.

    Индекс находится в диапазоне [0, 1], где 1 — максимальная нагрузка.
    """
    latency_penalty = min(signals.answer_latency_seconds / 60.0, 1.0)

    index = (
        0.35 * signals.emotion_stress_score
        + 0.25 * (1.0 - signals.concentration_score)
        + 0.20 * latency_penalty
        + 0.20 * signals.error_rate
    )
    return max(0.0, min(1.0, index))

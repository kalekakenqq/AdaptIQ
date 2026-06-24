"""Мультимодальное слияние сигналов CV, NLP и поведения студента."""

from dataclasses import dataclass


@dataclass
class ModalitySignals:
    """Сигналы из разных модальностей для одного момента сессии."""

    emotion_stress_score: float
    concentration_score: float
    nlp_answer_quality: float
    behavioral_error_rate: float


def fuse_modalities(signals: ModalitySignals) -> dict[str, float]:
    """Объединяет сигналы CV, NLP и поведения в единый вектор признаков состояния студента.

    Веса модальностей подобраны эмпирически и отражают вклад каждого канала
    в итоговую оценку состояния студента.
    """
    engagement = (
        0.4 * signals.concentration_score
        + 0.3 * (1.0 - signals.emotion_stress_score)
        + 0.3 * signals.nlp_answer_quality
    )
    distress = 0.5 * signals.emotion_stress_score + 0.5 * signals.behavioral_error_rate

    return {
        "engagement_score": max(0.0, min(1.0, engagement)),
        "distress_score": max(0.0, min(1.0, distress)),
    }

"""Тесты аналитического модуля: LSTM, кластеризация, аномалии, IRT."""

import numpy as np
import torch

from backend.ml.analytics.anomaly import BehaviorAutoencoder, compute_anomaly_score
from backend.ml.analytics.clustering import cluster_students
from backend.ml.analytics.irt import estimate_ability, probability_correct_answer
from backend.ml.analytics.lstm_predictor import ExamResultLSTM, predict_exam_result
from backend.services.cognitive_load import CognitiveSignals, compute_cognitive_load_index


def test_predict_exam_result_in_valid_range() -> None:
    """Предсказание LSTM должно быть вероятностью в диапазоне [0, 1]."""
    model = ExamResultLSTM()
    sequence = torch.rand(5, 4)
    probability = predict_exam_result(model, sequence)
    assert 0.0 <= probability <= 1.0


def test_cluster_students_returns_correct_number_of_labels() -> None:
    """Кластеризация должна возвращать метку для каждого студента."""
    np.random.seed(42)
    features = np.random.rand(20, 4)
    labels = cluster_students(features, n_clusters=3)
    assert len(labels) == 20
    assert set(labels).issubset({0, 1, 2})


def test_compute_anomaly_score_is_non_negative() -> None:
    """Оценка аномальности (ошибка реконструкции) не должна быть отрицательной."""
    model = BehaviorAutoencoder()
    features = torch.rand(8)
    score = compute_anomaly_score(model, features)
    assert score >= 0.0


def test_probability_correct_answer_increases_with_ability() -> None:
    """Вероятность правильного ответа должна расти с увеличением способности студента."""
    low_ability = probability_correct_answer(ability=-2.0, difficulty=0.0)
    high_ability = probability_correct_answer(ability=2.0, difficulty=0.0)
    assert high_ability > low_ability


def test_estimate_ability_higher_for_more_correct_answers() -> None:
    """Способность студента должна быть выше при большем числе правильных ответов."""
    difficulties = [0.0, 0.0, 0.0, 0.0]
    high_performer = estimate_ability([True, True, True, True], difficulties)
    low_performer = estimate_ability([False, False, False, False], difficulties)
    assert high_performer > low_performer


def test_compute_cognitive_load_index_in_valid_range() -> None:
    """Индекс когнитивной нагрузки должен находиться в диапазоне [0, 1]."""
    signals = CognitiveSignals(
        emotion_stress_score=0.8,
        concentration_score=0.3,
        answer_latency_seconds=90.0,
        error_rate=0.5,
    )
    index = compute_cognitive_load_index(signals)
    assert 0.0 <= index <= 1.0

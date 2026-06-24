"""Тесты XAI-модуля: SHAP и LIME объяснители."""

import numpy as np

from backend.ml.xai.lime_explainer import explain_prediction_lime
from backend.ml.xai.shap_explainer import explain_prediction

FEATURE_NAMES = ["cognitive_load", "concentration", "error_rate"]


def _linear_predict(data: np.ndarray) -> np.ndarray:
    """Простая линейная функция для тестирования объяснителей."""
    weights = np.array([1.0, -1.0, 2.0])
    return data @ weights


def test_shap_explain_prediction_returns_score_per_feature() -> None:
    """SHAP-объяснение должно возвращать вклад для каждого признака."""
    np.random.seed(42)
    background = np.random.rand(20, 3)
    instance = np.array([0.5, 0.5, 0.5])

    result = explain_prediction(_linear_predict, background, instance, FEATURE_NAMES)

    assert set(result.keys()) == set(FEATURE_NAMES)


def test_lime_explain_prediction_returns_non_empty_explanation() -> None:
    """LIME-объяснение должно возвращать непустой набор весов признаков."""
    np.random.seed(42)
    training_data = np.random.rand(50, 3)
    instance = np.array([0.5, 0.5, 0.5])

    result = explain_prediction_lime(_linear_predict, training_data, instance, FEATURE_NAMES)

    assert len(result) > 0

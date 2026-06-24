"""Локальные интерпретируемые объяснения предсказаний через LIME."""

from collections.abc import Callable

import numpy as np
from lime.lime_tabular import LimeTabularExplainer


def explain_prediction_lime(
    predict_fn: Callable[[np.ndarray], np.ndarray],
    training_data: np.ndarray,
    instance: np.ndarray,
    feature_names: list[str],
    num_features: int = 5,
) -> dict[str, float]:
    """Возвращает локальные веса признаков для предсказания модели через LIME."""
    explainer = LimeTabularExplainer(
        training_data, feature_names=feature_names, mode="regression"
    )
    explanation = explainer.explain_instance(instance, predict_fn, num_features=num_features)
    return dict(explanation.as_list())

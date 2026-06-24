"""Локальные интерпретируемые объяснения предсказаний через LIME."""

import logging
from collections.abc import Callable

import numpy as np

logger = logging.getLogger(__name__)

try:
    from lime.lime_tabular import LimeTabularExplainer

    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False
    logger.warning("lime не установлен, объяснения через lime недоступны")


def explain_prediction_lime(
    predict_fn: Callable[[np.ndarray], np.ndarray],
    training_data: np.ndarray,
    instance: np.ndarray,
    feature_names: list[str],
    num_features: int = 5,
) -> dict[str, float]:
    """Возвращает локальные веса признаков для предсказания модели через LIME."""
    if not LIME_AVAILABLE:
        raise RuntimeError("lime не установлен, объяснения недоступны")
    explainer = LimeTabularExplainer(
        training_data, feature_names=feature_names, mode="regression"
    )
    explanation = explainer.explain_instance(instance, predict_fn, num_features=num_features)
    return dict(explanation.as_list())

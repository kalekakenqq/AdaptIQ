"""Объяснение решений табличных моделей через SHAP values."""

import logging
from collections.abc import Callable

import numpy as np

logger = logging.getLogger(__name__)

try:
    import shap

    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    logger.warning("shap не установлен, объяснения через shap недоступны")


def explain_prediction(
    predict_fn: Callable[[np.ndarray], np.ndarray],
    background_data: np.ndarray,
    instance: np.ndarray,
    feature_names: list[str],
) -> dict[str, float]:
    """Возвращает вклад каждого признака в предсказание модели через SHAP."""
    if not SHAP_AVAILABLE:
        raise RuntimeError("shap не установлен, объяснения недоступны")
    explainer = shap.KernelExplainer(predict_fn, background_data)
    shap_values = explainer.shap_values(instance, nsamples=100)

    values = np.array(shap_values).flatten()
    return dict(zip(feature_names, values.tolist()))

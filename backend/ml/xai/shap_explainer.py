"""Объяснение решений табличных моделей через SHAP values."""

from collections.abc import Callable

import numpy as np
import shap


def explain_prediction(
    predict_fn: Callable[[np.ndarray], np.ndarray],
    background_data: np.ndarray,
    instance: np.ndarray,
    feature_names: list[str],
) -> dict[str, float]:
    """Возвращает вклад каждого признака в предсказание модели через SHAP."""
    explainer = shap.KernelExplainer(predict_fn, background_data)
    shap_values = explainer.shap_values(instance, nsamples=100)

    values = np.array(shap_values).flatten()
    return dict(zip(feature_names, values.tolist()))

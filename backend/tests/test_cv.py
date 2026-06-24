"""Тесты CV-модуля: eye tracking и Grad-CAM."""

import numpy as np
import torch
from torch import nn

from backend.ml.cv.eye_tracker import (
    LEFT_EYE_LANDMARKS,
    compute_eye_aspect_ratio,
    estimate_concentration_score,
)
from backend.ml.cv.gradcam import GradCAM


def _make_open_eyes_landmarks() -> np.ndarray:
    """Создаёт синтетические landmark-координаты, имитирующие открытые глаза."""
    landmarks = np.random.uniform(0, 1, size=(468, 2))
    landmarks[33] = [0.0, 0.5]
    landmarks[133] = [0.3, 0.5]
    landmarks[160] = [0.1, 0.3]
    landmarks[144] = [0.1, 0.7]
    landmarks[158] = [0.2, 0.3]
    landmarks[153] = [0.2, 0.7]
    return landmarks


def test_compute_eye_aspect_ratio_is_positive() -> None:
    """EAR для открытого глаза должен быть положительным числом."""
    landmarks = _make_open_eyes_landmarks()
    ear = compute_eye_aspect_ratio(landmarks, LEFT_EYE_LANDMARKS)
    assert ear > 0.0


def test_estimate_concentration_score_in_valid_range() -> None:
    """Индекс концентрации должен находиться в диапазоне [0, 1]."""
    landmarks = _make_open_eyes_landmarks()
    score = estimate_concentration_score(landmarks)
    assert 0.0 <= score <= 1.0


class _TinyCNN(nn.Module):
    """Минимальная CNN для проверки Grad-CAM без скачивания весов."""

    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(3, 4, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(4, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.conv(x)
        pooled = self.pool(features).flatten(1)
        return self.fc(pooled)


def test_gradcam_generates_heatmap_with_correct_shape() -> None:
    """Grad-CAM должен возвращать тепловую карту размера выходных признаков слоя."""
    model = _TinyCNN()
    cam = GradCAM(model, model.conv)
    image = torch.rand(3, 16, 16)

    heatmap = cam.generate(image, target_class=0)

    assert heatmap.shape == (16, 16)
    assert heatmap.min() >= 0.0

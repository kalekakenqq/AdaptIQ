"""Eye tracking и оценка концентрации внимания через MediaPipe Face Mesh."""

import numpy as np

LEFT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]


def compute_eye_aspect_ratio(landmarks: np.ndarray, eye_indices: list[int]) -> float:
    """Вычисляет eye aspect ratio (EAR) для одного глаза по координатам landmark-ов."""
    points = landmarks[eye_indices]
    vertical_1 = np.linalg.norm(points[1] - points[5])
    vertical_2 = np.linalg.norm(points[2] - points[4])
    horizontal = np.linalg.norm(points[0] - points[3])
    return float((vertical_1 + vertical_2) / (2.0 * horizontal + 1e-6))


def estimate_concentration_score(landmarks: np.ndarray) -> float:
    """Оценивает концентрацию внимания студента на основе EAR и положения взгляда.

    Возвращает значение в диапазоне [0, 1], где 1 — полная концентрация.
    """
    left_ear = compute_eye_aspect_ratio(landmarks, LEFT_EYE_LANDMARKS)
    right_ear = compute_eye_aspect_ratio(landmarks, RIGHT_EYE_LANDMARKS)
    average_ear = (left_ear + right_ear) / 2.0

    is_blinking_or_closed = average_ear < 0.15
    if is_blinking_or_closed:
        return 0.0

    normalized = min(average_ear / 0.3, 1.0)
    return float(normalized)

"""Тесты NLP-модуля (без загрузки тяжёлых предобученных моделей)."""

import numpy as np
import pytest

from backend.ml.nlp import answer_evaluator
from backend.ml.nlp.embeddings import cosine_similarity


def test_cosine_similarity_identical_vectors() -> None:
    """Косинусное сходство одинаковых векторов должно быть равно 1."""
    vector = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(vector, vector) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors() -> None:
    """Косинусное сходство ортогональных векторов должно быть равно 0."""
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert cosine_similarity(a, b) == pytest.approx(0.0)


def test_cosine_similarity_zero_vector_is_safe() -> None:
    """Сходство с нулевым вектором не должно вызывать деление на ноль."""
    a = np.zeros(3)
    b = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(a, b) == 0.0


def test_evaluate_open_answer_uses_embeddings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Оценка ответа должна основываться на семантической близости эмбеддингов."""

    def fake_embed_text(text: str) -> np.ndarray:
        return np.array([1.0, 0.0]) if "правильно" in text else np.array([0.0, 1.0])

    monkeypatch.setattr(answer_evaluator, "embed_text", fake_embed_text)

    score = answer_evaluator.evaluate_open_answer("ответ правильно", "эталон правильно")
    assert score == pytest.approx(1.0)

    score_wrong = answer_evaluator.evaluate_open_answer("совсем другое", "эталон правильно")
    assert score_wrong == pytest.approx(0.0)

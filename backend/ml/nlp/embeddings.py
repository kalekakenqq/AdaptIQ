"""Получение семантических эмбеддингов текста через sentence-transformers."""

from functools import lru_cache

import numpy as np

from backend.config import get_settings

settings = get_settings()


@lru_cache
def get_embedding_model():
    """Возвращает закэшированную модель sentence-transformers (импорт при первом вызове)."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError("sentence-transformers не установлен, эмбеддинги недоступны") from exc
    return SentenceTransformer(settings.sentence_transformer_model, device=settings.ml_device)


def embed_text(text: str) -> np.ndarray:
    """Возвращает векторное представление текста."""
    model = get_embedding_model()
    return model.encode(text, convert_to_numpy=True)


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """Вычисляет косинусное сходство между двумя векторами."""
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))

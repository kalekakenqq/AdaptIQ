"""Оценка открытых текстовых ответов студентов через RuBERT."""

import logging
from functools import lru_cache

from backend.config import get_settings
from backend.ml.nlp.embeddings import cosine_similarity, embed_text

logger = logging.getLogger(__name__)

settings = get_settings()

try:
    import torch
    from transformers import AutoModel, AutoTokenizer

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("transformers/torch не установлены, эмбеддинги rubert недоступны")


@lru_cache
def get_rubert() -> tuple:
    """Возвращает закэшированные токенизатор и модель RuBERT."""
    if not TRANSFORMERS_AVAILABLE:
        raise RuntimeError("transformers/torch не установлены, rubert недоступен")
    tokenizer = AutoTokenizer.from_pretrained(settings.rubert_model_name)
    model = AutoModel.from_pretrained(settings.rubert_model_name)
    model.to(settings.ml_device)
    model.eval()
    return tokenizer, model


def get_rubert_embedding(text: str) -> "torch.Tensor":
    """Возвращает эмбеддинг текста на основе CLS-токена RuBERT."""
    tokenizer, model = get_rubert()
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        output = model(**tokens)
    return output.last_hidden_state[:, 0, :].squeeze(0)


def evaluate_open_answer(student_answer: str, reference_answer: str) -> float:
    """Оценивает качество открытого ответа студента по семантической близости к эталону.

    Возвращает оценку в диапазоне [0, 1].
    """
    student_vector = embed_text(student_answer)
    reference_vector = embed_text(reference_answer)
    similarity = cosine_similarity(student_vector, reference_vector)
    return max(0.0, min(1.0, similarity))

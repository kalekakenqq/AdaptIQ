"""Визуализация attention-весов трансформера RuBERT."""

import numpy as np
import torch

from backend.ml.nlp.answer_evaluator import get_rubert


def get_attention_weights(text: str) -> np.ndarray:
    """Возвращает усреднённую по головам матрицу attention последнего слоя RuBERT."""
    tokenizer, model = get_rubert()
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        output = model(**tokens, output_attentions=True)

    last_layer_attention = output.attentions[-1].squeeze(0)
    averaged = last_layer_attention.mean(dim=0)
    return averaged.cpu().numpy()


def get_token_importance(text: str) -> dict[str, float]:
    """Возвращает важность каждого токена на основе attention к CLS-токену."""
    tokenizer, _ = get_rubert()
    tokens = tokenizer.tokenize(text)
    attention_matrix = get_attention_weights(text)

    cls_attention = attention_matrix[0, 1:len(tokens) + 1]
    return {token: float(score) for token, score in zip(tokens, cls_attention)}

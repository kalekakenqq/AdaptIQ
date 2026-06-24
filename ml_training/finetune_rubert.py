"""Скрипт fine-tuning RuBERT для оценки открытых ответов студентов.

Использует датасет пар (ответ студента, эталонный ответ, оценка) для
дообучения модели семантического сравнения. Для демонстрации работы
пайплайна датасет генерируется синтетически.
"""

import logging

from sentence_transformers import InputExample, SentenceTransformer, losses
from torch.utils.data import DataLoader

from backend.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def generate_synthetic_pairs() -> list[InputExample]:
    """Генерирует синтетические пары ответов с метками схожести для дообучения."""
    pairs = [
        ("производная функции это скорость изменения", "производная это скорость изменения функции", 0.9),
        ("интеграл это площадь под кривой", "производная это скорость изменения функции", 0.1),
        ("матрица это таблица чисел", "матрица представляет собой прямоугольную таблицу чисел", 0.9),
    ]
    return [InputExample(texts=[a, b], label=score) for a, b, score in pairs]


def finetune(epochs: int = 1) -> None:
    """Дообучает модель sentence-transformers на парах ответов."""
    model = SentenceTransformer(settings.sentence_transformer_model)
    train_examples = generate_synthetic_pairs()
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=2)
    train_loss = losses.CosineSimilarityLoss(model)

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        show_progress_bar=False,
    )
    logger.info("дообучение модели завершено")


if __name__ == "__main__":
    finetune()

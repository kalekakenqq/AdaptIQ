"""Скрипт обучения CNN-классификатора эмоций на синтетическом датасете.

Используется для демонстрации работоспособности пайплайна обучения.
Для продакшен-качества модели требуется реальный размеченный датасет
лицевых эмоций (например, AffectNet или FER2013).
"""

import logging
from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from backend.ml.cv.emotion_model import EMOTION_LABELS, EmotionCNN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEIGHTS_PATH = Path(__file__).resolve().parent.parent / "backend" / "ml" / "cv" / "weights" / "emotion_cnn.pt"


def generate_synthetic_dataset(num_samples: int = 200) -> TensorDataset:
    """Генерирует синтетический датасет изображений и меток эмоций для демонстрации."""
    images = torch.rand(num_samples, 3, 224, 224)
    labels = torch.randint(0, len(EMOTION_LABELS), (num_samples,))
    return TensorDataset(images, labels)


def train(epochs: int = 3, batch_size: int = 8) -> None:
    """Обучает CNN на синтетических данных и сохраняет веса."""
    dataset = generate_synthetic_dataset()
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = EmotionCNN()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for images, labels in loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        logger.info("эпоха %d, средний loss: %.4f", epoch + 1, total_loss / len(loader))

    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), WEIGHTS_PATH)
    logger.info("веса модели сохранены: %s", WEIGHTS_PATH)


if __name__ == "__main__":
    train()

"""Скрипт обучения LSTM-модели предсказания результата экзамена."""

import logging
from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from backend.ml.analytics.lstm_predictor import ExamResultLSTM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEIGHTS_PATH = (
    Path(__file__).resolve().parent.parent / "backend" / "ml" / "analytics" / "weights" / "lstm_predictor.pt"
)


def generate_synthetic_sequences(num_samples: int = 300, seq_len: int = 10) -> TensorDataset:
    """Генерирует синтетические последовательности сессий и метки результата экзамена."""
    sequences = torch.rand(num_samples, seq_len, 4)
    labels = (sequences.mean(dim=(1, 2)) > 0.5).float()
    return TensorDataset(sequences, labels)


def train(epochs: int = 5, batch_size: int = 16) -> None:
    """Обучает LSTM на синтетических данных и сохраняет веса."""
    dataset = generate_synthetic_sequences()
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = ExamResultLSTM()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.BCELoss()

    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for sequences, labels in loader:
            optimizer.zero_grad()
            predictions = model(sequences)
            loss = criterion(predictions, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        logger.info("эпоха %d, средний loss: %.4f", epoch + 1, total_loss / len(loader))

    WEIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), WEIGHTS_PATH)
    logger.info("веса lstm сохранены: %s", WEIGHTS_PATH)


if __name__ == "__main__":
    train()

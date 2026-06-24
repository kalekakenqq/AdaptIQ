"""LSTM-модель предсказания результата экзамена по динамике сессий."""

from pathlib import Path

import torch
from torch import nn

DEFAULT_WEIGHTS_PATH = Path(__file__).resolve().parent / "weights" / "lstm_predictor.pt"


class ExamResultLSTM(nn.Module):
    """LSTM, предсказывающая вероятность успешной сдачи экзамена."""

    def __init__(self, input_size: int = 4, hidden_size: int = 32, num_layers: int = 2) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden_size, 1), nn.Sigmoid())

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        """Прямой проход: последовательность сессий -> вероятность успеха."""
        output, _ = self.lstm(sequence)
        last_hidden = output[:, -1, :]
        return self.head(last_hidden).squeeze(-1)


def load_lstm_predictor(weights_path: Path = DEFAULT_WEIGHTS_PATH) -> ExamResultLSTM:
    """Загружает LSTM-модель, при отсутствии весов возвращает неинициализированную модель."""
    model = ExamResultLSTM()
    if weights_path.exists():
        model.load_state_dict(torch.load(weights_path, map_location="cpu"))
    model.eval()
    return model


def predict_exam_result(model: ExamResultLSTM, session_sequence: torch.Tensor) -> float:
    """Предсказывает вероятность успешной сдачи экзамена по истории сессий студента."""
    with torch.no_grad():
        probability = model(session_sequence.unsqueeze(0))
    return float(probability.item())

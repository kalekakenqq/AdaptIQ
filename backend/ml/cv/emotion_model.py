"""CNN-классификатор эмоций на базе EfficientNet-B0 (transfer learning)."""

from pathlib import Path

import torch
from torch import nn
from torchvision.models import efficientnet_b0

EMOTION_LABELS = ["neutral", "happy", "sad", "surprised", "confused", "frustrated", "bored"]

DEFAULT_WEIGHTS_PATH = Path(__file__).resolve().parent / "weights" / "emotion_cnn.pt"


class EmotionCNN(nn.Module):
    """CNN для классификации эмоций по лицу студента."""

    def __init__(self, num_classes: int = len(EMOTION_LABELS), pretrained: bool = True) -> None:
        super().__init__()
        self.backbone = efficientnet_b0(weights="DEFAULT" if pretrained else None)
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier[1] = nn.Linear(in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Прямой проход: изображение лица -> логиты эмоций."""
        return self.backbone(x)


def load_emotion_model(
    weights_path: Path = DEFAULT_WEIGHTS_PATH, device: str = "cpu"
) -> EmotionCNN:
    """Загружает модель эмоций, при отсутствии весов возвращает предобученный backbone."""
    model = EmotionCNN(pretrained=weights_path.exists() is False)
    if weights_path.exists():
        model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def predict_emotion(model: EmotionCNN, image_tensor: torch.Tensor) -> str:
    """Предсказывает доминирующую эмоцию по тензору изображения лица."""
    with torch.no_grad():
        logits = model(image_tensor.unsqueeze(0))
        predicted_index = int(torch.argmax(logits, dim=1).item())
    return EMOTION_LABELS[predicted_index]

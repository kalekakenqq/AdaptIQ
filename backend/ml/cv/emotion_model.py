"""CNN-классификатор эмоций на базе EfficientNet-B0 (transfer learning)."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

EMOTION_LABELS = ["neutral", "happy", "sad", "surprised", "confused", "frustrated", "bored"]

DEFAULT_WEIGHTS_PATH = Path(__file__).resolve().parent / "weights" / "emotion_cnn.pt"

_emotion_cnn_class = None


def _get_emotion_cnn_class():
    """Лениво импортирует torch/torchvision и строит класс EmotionCNN при первом вызове."""
    global _emotion_cnn_class
    if _emotion_cnn_class is not None:
        return _emotion_cnn_class

    try:
        from torch import nn
        from torchvision.models import efficientnet_b0
    except ImportError as exc:
        raise RuntimeError("torch/torchvision не установлены, модель эмоций недоступна") from exc

    class EmotionCNN(nn.Module):
        """CNN для классификации эмоций по лицу студента."""

        def __init__(self, num_classes: int = len(EMOTION_LABELS), pretrained: bool = True) -> None:
            super().__init__()
            self.backbone = efficientnet_b0(weights="DEFAULT" if pretrained else None)
            in_features = self.backbone.classifier[1].in_features
            self.backbone.classifier[1] = nn.Linear(in_features, num_classes)

        def forward(self, x):
            """Прямой проход: изображение лица -> логиты эмоций."""
            return self.backbone(x)

    _emotion_cnn_class = EmotionCNN
    return _emotion_cnn_class


def load_emotion_model(weights_path: Path = DEFAULT_WEIGHTS_PATH, device: str = "cpu"):
    """Загружает модель эмоций, при отсутствии весов возвращает предобученный backbone."""
    import torch

    emotion_cnn_class = _get_emotion_cnn_class()
    model = emotion_cnn_class(pretrained=weights_path.exists() is False)
    if weights_path.exists():
        model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def predict_emotion(model, image_tensor) -> str:
    """Предсказывает доминирующую эмоцию по тензору изображения лица."""
    import torch

    with torch.no_grad():
        logits = model(image_tensor.unsqueeze(0))
        predicted_index = int(torch.argmax(logits, dim=1).item())
    return EMOTION_LABELS[predicted_index]

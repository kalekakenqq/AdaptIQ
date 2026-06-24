"""Детекция аномального поведения студента через автоэнкодер."""

import logging

logger = logging.getLogger(__name__)

try:
    import torch
    from torch import nn

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("torch не установлен, детекция аномалий недоступна")


if TORCH_AVAILABLE:

    class BehaviorAutoencoder(nn.Module):
        """Автоэнкодер для поведенческих признаков студента."""

        def __init__(self, input_size: int = 8, latent_size: int = 3) -> None:
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(input_size, 16),
                nn.ReLU(),
                nn.Linear(16, latent_size),
            )
            self.decoder = nn.Sequential(
                nn.Linear(latent_size, 16),
                nn.ReLU(),
                nn.Linear(16, input_size),
            )

        def forward(self, x: "torch.Tensor") -> "torch.Tensor":
            """Прямой проход: признаки -> реконструкция признаков."""
            latent = self.encoder(x)
            return self.decoder(latent)

else:

    class BehaviorAutoencoder:  # type: ignore[no-redef]
        """Заглушка автоэнкодера при отсутствии torch."""

        def __init__(self, *args, **kwargs) -> None:
            raise RuntimeError("torch не установлен, детекция аномалий недоступна")


def compute_anomaly_score(model: "BehaviorAutoencoder", features: "torch.Tensor") -> float:
    """Вычисляет ошибку реконструкции как меру аномальности поведения."""
    if not TORCH_AVAILABLE:
        raise RuntimeError("torch не установлен, детекция аномалий недоступна")
    with torch.no_grad():
        reconstruction = model(features.unsqueeze(0))
        error = torch.mean((reconstruction - features.unsqueeze(0)) ** 2)
    return float(error.item())

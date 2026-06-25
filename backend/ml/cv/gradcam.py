"""Grad-CAM визуализация значимых областей изображения для CNN эмоций."""

import logging

import numpy as np

logger = logging.getLogger(__name__)


class GradCAM:
    """Вычисляет тепловую карту значимости для предсказания CNN."""

    def __init__(self, model, target_layer) -> None:
        try:
            import torch  # noqa: F401
        except ImportError as exc:
            raise RuntimeError("torch не установлен, grad-cam визуализация недоступна") from exc

        self.model = model
        self.target_layer = target_layer
        self._activations = None
        self._gradients = None

        target_layer.register_forward_hook(self._save_activations)
        target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input_, output) -> None:
        self._activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output) -> None:
        self._gradients = grad_output[0].detach()

    def generate(self, image_tensor, target_class: int) -> np.ndarray:
        """Генерирует тепловую карту Grad-CAM для заданного класса."""
        import torch

        self.model.zero_grad()
        output = self.model(image_tensor.unsqueeze(0))
        output[0, target_class].backward()

        weights = self._gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self._activations).sum(dim=1).squeeze(0)
        cam = torch.relu(cam)
        cam = cam / (cam.max() + 1e-8)
        return cam.cpu().numpy()

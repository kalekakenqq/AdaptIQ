"""Grad-CAM визуализация значимых областей изображения для CNN эмоций."""

import numpy as np
import torch
from torch import nn


class GradCAM:
    """Вычисляет тепловую карту значимости для предсказания CNN."""

    def __init__(self, model: nn.Module, target_layer: nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer
        self._activations: torch.Tensor | None = None
        self._gradients: torch.Tensor | None = None

        target_layer.register_forward_hook(self._save_activations)
        target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input_, output) -> None:
        self._activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output) -> None:
        self._gradients = grad_output[0].detach()

    def generate(self, image_tensor: torch.Tensor, target_class: int) -> np.ndarray:
        """Генерирует тепловую карту Grad-CAM для заданного класса."""
        self.model.zero_grad()
        output = self.model(image_tensor.unsqueeze(0))
        output[0, target_class].backward()

        weights = self._gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self._activations).sum(dim=1).squeeze(0)
        cam = torch.relu(cam)
        cam = cam / (cam.max() + 1e-8)
        return cam.cpu().numpy()

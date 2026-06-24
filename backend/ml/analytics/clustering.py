"""Кластеризация студентов по поведенческим паттернам (K-Means + UMAP)."""

import logging

import numpy as np

logger = logging.getLogger(__name__)

try:
    from sklearn.cluster import KMeans

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn не установлен, кластеризация недоступна")

try:
    from umap import UMAP

    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    logger.warning("umap-learn не установлен, снижение размерности недоступно")


def reduce_dimensions(features: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Снижает размерность признаков студентов методом UMAP."""
    if not UMAP_AVAILABLE:
        raise RuntimeError("umap-learn не установлен, снижение размерности недоступно")
    reducer = UMAP(n_components=n_components, random_state=42)
    return reducer.fit_transform(features)


def cluster_students(features: np.ndarray, n_clusters: int = 4) -> np.ndarray:
    """Кластеризует студентов методом K-Means по поведенческим признакам."""
    if not SKLEARN_AVAILABLE:
        raise RuntimeError("scikit-learn не установлен, кластеризация недоступна")
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    return model.fit_predict(features)

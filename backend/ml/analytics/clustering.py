"""Кластеризация студентов по поведенческим паттернам (K-Means + UMAP)."""

import numpy as np
from sklearn.cluster import KMeans
from umap import UMAP


def reduce_dimensions(features: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Снижает размерность признаков студентов методом UMAP."""
    reducer = UMAP(n_components=n_components, random_state=42)
    return reducer.fit_transform(features)


def cluster_students(features: np.ndarray, n_clusters: int = 4) -> np.ndarray:
    """Кластеризует студентов методом K-Means по поведенческим признакам."""
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    return model.fit_predict(features)

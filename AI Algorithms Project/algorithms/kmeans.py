"""
K-Means Clustering Algorithm
This module provides a skeleton implementation of the K-Means clustering algorithm.
"""

import numpy as np
from typing import List, Optional

class KMeans:
    """
    Skeleton class for K-Means clustering.
    """
    def __init__(self, n_clusters: int = 3, max_iter: int = 100, tolerance: float = 1e-4) -> None:
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.centroids: Optional[np.ndarray] = None

    def initialize_centroids(self, X: np.ndarray) -> np.ndarray:
        """
        Initialize centroids from the dataset.
        """
        # TODO: Implement centroid initialization logic
        pass

    def fit(self, X: np.ndarray) -> None:
        """
        Fit the K-Means model to the data X.
        """
        # TODO: Implement the K-Means training loop
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Assign each sample in X to the nearest centroid.
        """
        # TODO: Implement assignment logic
        pass

    def _compute_centroids(self, clusters: List[np.ndarray]) -> np.ndarray:
        """
        Compute the new centroids as the mean of points in each cluster.
        """
        # TODO: Compute centroids based on clusters
        pass

    def _assign_clusters(self, X: np.ndarray) -> List[np.ndarray]:
        """
        Assign data points to clusters based on current centroids.
        """
        # TODO: Implement cluster assignment
        pass

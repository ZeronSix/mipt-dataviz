import numpy as np


def reduce_dimensions_pca(objects: np.array, reduced_dimensions: float) -> np.array:
    num_objects, orig_dimensions = objects.shape
    x = objects
    x_centered = x - np.tile(np.mean(x, 0), (num_objects, 1))
    eigen_values, eigen_vectors = np.linalg.eig(np.dot(x_centered.T, x_centered))

    return np.dot(x_centered, eigen_vectors[:, 0:reduced_dimensions])

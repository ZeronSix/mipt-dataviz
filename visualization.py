import numpy as np
from matplotlib import pyplot as plt


def visualize_clusters(objects: np.ndarray, labels: np.ndarray, output_filename: str):
    fig, ax = plt.subplots()
    scatter = ax.scatter(objects[:, 0], objects[:, 1], 20, labels)
    legend = ax.legend(*scatter.legend_elements())
    ax.add_artist(legend)
    fig.savefig(output_filename)

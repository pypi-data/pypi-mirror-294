from typing import Any, Callable, Optional, Sequence
import re
import math
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics.pairwise import cosine_distances
from sklearn.base import ClusterMixin
from numpy import ndarray
import numpy as np


def get_by_xml_tag(text, tag_name) -> Optional[str]:
    match = re.search(fr'<{tag_name}>(.+?)</{tag_name}>', text, re.DOTALL)
    if not match:
        return None
    return match.group(1)


def run_parallel(items: Sequence[Any], unit_func: Callable, max_workers: int, **tqdm_kwargs) -> list:
    def _pbar_wrapper(pbar, item):
        unit = unit_func(item)
        with pbar.get_lock():
            pbar.update(1)
        return unit

    with tqdm(total=len(items), **tqdm_kwargs) as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for item in items:
                futures.append(executor.submit(_pbar_wrapper, pbar, item))

    output = [future.result() for future in futures if future.result() is not None]
    return output


def guess_optimal_n_clusters(embeddings: ndarray, get_model: Callable[[int], ClusterMixin], verbose=False) -> int:
    """
    Utility function to guess optimal number of clusters for a given cluster model.
    Useful for models that require number of clusters as input.
    :param embeddings: ndarray of embeddings of shape (n_samples, n_features)
    :param get_model: Callable that takes number of clusters as parameter and returns an sklearn cluster model
    :param verbose:
    :return: optimal number of clusters based on silhouette score
    """
    if len(embeddings) <= 1:
        return len(embeddings)

    best_sil_coeff = -1
    best_num_clusters = 0
    MAX_MIN_CLUSTERS = 3  # the max start of the search for optimal cluster number.
    n_cluster_start = min(len(embeddings), MAX_MIN_CLUSTERS)
    n_cluster_end = min(round(math.sqrt(len(embeddings)))*3, len(embeddings)//2)
    if n_cluster_end < (n_cluster_start + 1):
        n_cluster_start = 2
        n_cluster_end = n_cluster_start + 1
    n_clusters = range(n_cluster_start, n_cluster_end)
    for n_cluster in tqdm(n_clusters, total=len(n_clusters), desc='guess optimal clustering', disable=not verbose):
        labels = get_model(n_cluster).fit_predict(embeddings)
        vrc_coeff = calinski_harabasz_score(embeddings, labels)
        if vrc_coeff > best_sil_coeff:
            best_sil_coeff = vrc_coeff
            best_num_clusters = n_cluster
    if verbose:
        print("Best N", best_num_clusters, "Best silhouette score", round(best_sil_coeff, 4))
    return best_num_clusters


def modified_silhouette_score(embeddings, cluster_labels, cluster_summaries):
    """
    Calculate a modified silhouette score for text clustering using cosine distances.

    Parameters:
    - embeddings (numpy.ndarray): 2D array where each row is the embedding of a text document.
    - cluster_labels (numpy.ndarray): 1D array of cluster labels for each document.
    - cluster_summaries (numpy.ndarray): 2D array where each row is the embedding of a cluster summary.

    Returns:
    - modified_silhouette_avg (float): The average modified silhouette score for all documents.
    """

    n_samples = len(embeddings)
    unique_labels = np.unique(cluster_labels)
    n_clusters = len(unique_labels)

    if n_clusters == 1:
        raise ValueError("Only one cluster found. Silhouette score is undefined in this case.")

    # Initialize silhouette scores
    silhouette_scores = np.zeros(n_samples)

    # Precompute cosine distances between all documents and summaries
    intra_cluster_distances = cosine_distances(embeddings, cluster_summaries)

    # Calculate the modified silhouette score for each sample
    for i in range(n_samples):
        # Get the cluster of the current sample
        own_cluster = cluster_labels[i]
        own_cluster_summary_distance = intra_cluster_distances[i, own_cluster]

        # Find the distance to the closest cluster summary
        inter_cluster_summary_distances = intra_cluster_distances[i]
        inter_cluster_summary_distances[own_cluster] = np.inf  # Exclude own cluster
        nearest_cluster_distance = np.min(inter_cluster_summary_distances)

        # Silhouette score calculation
        a = own_cluster_summary_distance  # Intra-cluster distance
        b = nearest_cluster_distance  # Inter-cluster distance
        silhouette_scores[i] = (b - a) / max(a, b)

    # Average the silhouette scores to get the final modified silhouette score
    modified_silhouette_avg = np.mean(silhouette_scores)

    return modified_silhouette_avg

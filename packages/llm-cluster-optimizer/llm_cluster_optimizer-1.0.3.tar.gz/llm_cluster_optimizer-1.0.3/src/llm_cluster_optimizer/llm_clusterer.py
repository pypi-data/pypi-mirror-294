from typing import Sequence, Union, Callable
from functools import reduce, partial
from sklearn.metrics import pairwise_distances
from sklearn.cluster import AffinityPropagation
from sklearn.base import ClusterMixin
from tqdm import tqdm
import random
from dataclasses import dataclass
from numpy import ndarray
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from util import get_by_xml_tag, run_parallel
import numpy as np

ClusterMixinOrCallable = Union[ClusterMixin, Callable[[ndarray], ClusterMixin]]


@dataclass
class SummarizedCluster:
    label: int
    embeddings: list[ndarray]
    items: list[str]
    summary: str = None

    def merge(self, other: 'SummarizedCluster') -> 'SummarizedCluster':
        return SummarizedCluster(self.label, self.embeddings + other.embeddings, self.items + other.items, self.summary)

    def set_summary(self, summary: str) -> None:
        self.summary = summary.strip()

    @property
    def labels(self) -> list[int]:
        """
        list of `self.label` duplicated by how many items there are
        Useful for converting to sklearn `fit_predict()` return value
        :return:
        """
        return [self.label]*len(self)

    def __len__(self):
        return len(self.items)

    def __eq__(self, other):
        if not isinstance(other, SummarizedCluster):
            return False
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.label, len(self), self.summary))


def _default_get_cluster_summary(strs_to_summarize: Sequence[str]) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    system = SystemMessage(content="Given a few ideas (wrapped in <idea> "
                                   "XML tags) output a summary of the"
                                   "ideas. Wrap the output in <summary> tags. Summary"
                                   "should be no more than 10 words.")
    human = HumanMessage(content=f"<idea>{'</idea><idea>'.join(strs_to_summarize)}</idea>")
    response = llm.invoke([system, human])
    return get_by_xml_tag(response.content, "summary")


class LLMClusterOptimizer:

    def __init__(self, cluster_model: ClusterMixinOrCallable,
                 embedding_fn: Callable[[str], ndarray], recluster_threshold_fn: Callable[[int], int],
                 threshold_to_combine: float,
                 get_cluster_summary: Callable[[list[str]], str] = None,
                 summary_sample_size=5, num_summarization_workers=25, num_embed_workers=50, verbose=True, _optimize=True):
        """
        :param cluster_model: SKlearn cluster model instance (aka ClusterMixin). Can be either a ClusterMixin or a Callable that takes a list of embeddings and returns a ClusterMixin. Use the latter if the ClusterMixin requires n clusters as a parameter. The callable should use the embeddings to determine the optimal n. See `util.guess_optimal_n_clusters()` as an example for calcualting optimal number of clusters.
        :param embedding_fn: Function that takes a strings and returns its embedding.
        :param recluster_threshold_fn: Function that takes the number of input texts and outputs the minimum size cluster that will be reclustered using `cluster_model`.
        :param get_cluster_summary: Functon that takes a list of strings which are samples from a cluster and returns a summary of them. If not passed `_default_get_cluster_summary()` will be used. If using default, make sure OpenAI API key is setup in envvars.
        :param threshold_to_combine: float that represents the maximum cosine distance between cluster summary embeddings where clusters should be combined.
        :param summary_sample_size: Number of items to sample from a cluster
        :param num_summarization_workers: Number of workers to use when running `get_cluster_summary()`. Be aware of rate limits depending on the LLM provider being used.
        :param num_embed_workers: Number of workers to use when running `embedding_fn()`. Be aware of rate limits depending on the LLM provider being used.
        :param verbose: Output logs to console
        :param _optimize: Flag for debugging. When false, will only cluster results using `cluster_model` but won't perform any post-processing.
        """
        self._cluster_model = cluster_model
        self._embedding_fn = embedding_fn
        self._recluster_threshold_fn = recluster_threshold_fn
        self._threshold_to_combine = threshold_to_combine
        self._get_cluster_summary = get_cluster_summary or _default_get_cluster_summary
        self._summary_sample_size = summary_sample_size
        self._num_summarization_workers = num_summarization_workers
        self._num_embed_workers = num_embed_workers
        self._verbose = verbose
        self._optimize = _optimize

    def fit_predict_text(self, texts: Sequence[str]) -> ndarray:
        """
        Mimics `sklearn.base.ClusterMixin.fit_predict()`. Given a sequence of texts, returns the cluster labels for each text.
        Embeds `texts` using `embedding_fn()`
        Clusters embeddings using `cluster_model`
        Post-processes clusters so that:
        - large clusters are broken up
        - small clusters are combined based on similarity
        :param texts: List of strings to cluster.
        :return: List of cluster labels of shape `(len(texts),)`
        """
        recluster_threshold = self._recluster_threshold_fn(len(texts))
        embeddings = self._embed_parallel(texts, desc="Embedding input texts")
        curr_labels = self._get_labels(embeddings, self._cluster_model)
        curr_clusters = self._build_clusters(curr_labels, embeddings, texts, recluster_threshold)
        summarized_clusters = self._summarize_clusters(curr_clusters)
        if self._optimize:
            summarized_clusters = self._collapse_similar_clusters(summarized_clusters)
        return np.array(reduce(lambda x, y: x + y.labels, summarized_clusters, []))

    @staticmethod
    def _get_labels(embeddings: ndarray, cluster_model: Union[ClusterMixin, Callable[[ndarray], ClusterMixin]]) -> ndarray:
        if callable(cluster_model):
            cluster_model = cluster_model(embeddings)
        return cluster_model.fit_predict(embeddings)

    @staticmethod
    def _build_clusters_from_cluster_results(labels: ndarray, embeddings: ndarray, items: ndarray, label_offset: int = 0) -> (list[SummarizedCluster], list, ndarray):
        clusters = []
        noise_items = []
        noise_embeddings = []
        for label in np.unique(labels):
            indices = np.where(labels == label)[0]
            curr_embeddings = [embeddings[j] for j in indices]
            curr_items = [items[j] for j in indices]
            if label == -1:
                noise_items += curr_items
                noise_embeddings += curr_embeddings
                continue
            clusters += [SummarizedCluster(label + label_offset, curr_embeddings, curr_items)]
        return clusters, noise_items, noise_embeddings

    def _build_clusters(self, labels, embeddings, texts, recluster_threshold, label_offset=0) -> Sequence[SummarizedCluster]:
        clusters, noise_items, noise_embeddings = self._build_clusters_from_cluster_results(labels, embeddings, texts, label_offset)
        if self._optimize:
            clusters = self._recluster_large_clusters(clusters, recluster_threshold)
        if len(noise_items) > 0:
            noise_labels = self._get_labels(noise_embeddings, self._cluster_model)
            noise_clusters, _, _ = self._build_clusters_from_cluster_results(noise_labels, noise_embeddings, noise_items, label_offset+len(clusters))
            if self._verbose:
                print("LEN NOISE_CLUSTERS", len(noise_clusters))
            clusters += noise_clusters
        return clusters

    def _summarize_cluster(self, cluster: SummarizedCluster) -> SummarizedCluster:
        """
        :param cluster: Cluster to summarize
        :return: the same cluster object with the `summary` attribute set.
        """
        if len(cluster) == 1:
            summary = cluster.items[0]
        else:
            sample = random.sample(cluster.items, min(len(cluster), self._summary_sample_size))
            summary = self._get_cluster_summary(sample) or "N/A"
        cluster.set_summary(summary)
        return cluster

    def _summarize_clusters(self, clusters: Sequence[SummarizedCluster], **kwargs) -> list[SummarizedCluster]:
        return run_parallel(clusters, partial(self._summarize_cluster, **kwargs),
                            max_workers=self._num_summarization_workers, desc='summarize source clusters', disable=not self._verbose)

    def _embed_parallel(self, items: Sequence[str], **kwargs):
        return run_parallel(items, self._embedding_fn, max_workers=self._num_embed_workers, disable=not self._verbose, **kwargs)

    def _embed_cluster_summaries(self, summarized_clusters: Sequence[SummarizedCluster]):
        return self._embed_parallel([c.summary for c in summarized_clusters],
                                    desc="embedding cluster summaries to score")

    def _collapse_similar_clusters(self, clusters: Sequence[SummarizedCluster]) -> list[SummarizedCluster]:
        embeddings = self._embed_cluster_summaries(clusters)
        distances = pairwise_distances(embeddings, metric='cosine')
        merged = np.zeros(len(clusters), dtype=bool)
        new_clusters = []

        for i, curr_cluster in enumerate(clusters):
            if merged[i]:
                continue
            merged[i] = True
            # Find clusters that need to be merged with the current cluster
            to_merge = (distances[i] < self._threshold_to_combine) & ~merged
            merged[to_merge] = True
            for j in np.where(to_merge)[0]:
                curr_cluster = curr_cluster.merge(clusters[j])
            new_clusters.append(curr_cluster)
        self._summarize_clusters(new_clusters)
        return new_clusters

    def _recluster_large_clusters(self, clusters: Sequence[SummarizedCluster], recluster_threshold: int) -> Sequence[SummarizedCluster]:
        large_clusters = {c for c in clusters if len(c) >= recluster_threshold}
        new_clusters = [c for c in clusters if c not in large_clusters]
        if len(large_clusters) == 0:
            return clusters
        for cluster in tqdm(large_clusters, desc="Reclustering large clusters", disable=not self._verbose):
            labels = self._get_labels(cluster.embeddings, self._cluster_model)
            if len(np.unique(labels)) == 1:
                reclustered_clusters = [cluster]
            else:
                reclustered_clusters = self._build_clusters(labels, cluster.embeddings, cluster.items, recluster_threshold, len(new_clusters))
            new_clusters.extend(reclustered_clusters)
        return new_clusters

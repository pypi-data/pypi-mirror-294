## llm-cluster-optimizer

A drop-in replacement for sklearn clustering models, this package optimizes sklearn clusters using LLMs

## Installation

By default, this package relies on OpenAI for LLM interactions. This requires having copying your API key from [here](https://platform.openai.com/account/api-keys) and putting it in the `OPENAI_API_KEY` envvar.

Otherwise, you can use any other LLM provider, as described below.

To install `llm-cluster-optimizer`, run the following command in your terminal:

```shell
pip install llm-cluster-optimizer
```

## Usage

Here is a simple example of usage that provides two cluster models as options to be optimized. `labels` will be an `np.ndarray` of shape `(len(input_texts),)` representing which cluster each input text falls into. Use `verbose=True` in `LLMClusterOptimizer.__init__()` to get more information on progress.

```python
from llm_cluster_optimizer import LLMClusterOptimizer
from sklearn.cluster import AffinityPropagation, HDBSCAN
import numpy as np
from langchain_openai import OpenAIEmbeddings

def embed_text_openai(text):
    return np.array(OpenAIEmbeddings(model="text-embedding-3-large").embed_query(text))

model = HDBSCAN(min_cluster_size=2, min_samples=1),
optimizer = LLMClusterOptimizer(model, embed_text_openai, 0.3)

input_texts = []  # your list of input texts
labels = optimizer.fit_predict_text(input_texts)
```

To use a clustering algorithm that takes the number of clusters as an input, you likely want to optimize `n` using the silhouette score or a similar metric. This requires access to the embeddings. You can pass the model wrapped in a function to achieve this:

```python
from sklearn.cluster import KMeans
from util import guess_optimal_n_clusters

def get_kmeans_model(embeddings: np.ndarray):
    n_clusters = guess_optimal_n_clusters(embeddings, lambda n: KMeans(n_clusters=n))
    return KMeans(n_clusters=n_clusters)


optimizer = LLMClusterOptimizer(get_kmeans_model, embed_text_openai, 0.3)
```

## Docs

### __init__()

| **Param**                               | **Description**                                                                                                                                                                                                                                                                                                                                                                                     | **Default**                                                                                            | **Type**                                                                  |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `cluster_model`                         | SKlearn cluster model instance (aka ClusterMixin). Can be either a ClusterMixin or a Callable that takes a list of embeddings and returns a ClusterMixin. Use the latter if the ClusterMixin requires n clusters as a parameter. The callable should use the embeddings to determine the optimal n. See `util.guess_optimal_n_clusters()` as an example for calcualting optimal number of clusters. | N/A                                                                                                    | `Union[ClusterMixin, Callable[[ndarray], ClusterMixin]]`         |
| `embedding_fn`                          | Function that takes a string and returns its embedding.                                                                                                                                                                                                                                                                                                                                             | N/A                                                                                                    | `Callable[[str], ndarray]`                                                 |
| `threshold_to_combine`                  | Float that represents the maximum cosine distance between cluster summary embeddings where clusters should be combined.                                                                                                                                             | N/A                                                                                                   | `Callable[[int], int]`                                                             |
| `recluster_threshold_fn`                | Function that takes the number of input texts and outputs the minimum size cluster that will be reclustered using `cluster_model`. If not provided, the minimum size is the square root of input size (implying uniform distribution of cluster sizes).                                                                                                                                             | `lambda x: round(math.sqrt(x)))`                                                                       | `Callable[[int], int]`                                                             |
| `get_cluster_summary`                   | Function that takes a list of strings which are samples from a cluster and returns a summary of them. See `default` for default functionality. Requires OpenAI API key in envvars if using default.                                                                                                                                                                                                 | Uses GPT-4o-mini to summarize strings sampled from the cluster. Summary will be no more than 10 words. | `Callable[[list[str]], str]`                                               |
| `summary_sample_size`                   | Number of items to sample from a cluster.                                                                                                                                                                                                                                                                                                                                                           | `5`                                                                                                    | `int`                                                                     |
| `num_summarization_workers`             | Number of workers to use when running `get_cluster_summary()`. Be aware of rate limits depending on the LLM provider being used.                                                                                                                                                                                                                                                                    | `25`                                                                                                   | `int`                                                                     |
| `num_embed_workers`                     | Number of workers to use when running `embedding_fn()`. Be aware of rate limits depending on the LLM provider being used.                                                                                                                                                                                                                                                                           | `50`                                                                                                   | `int`                                                                     |
| `verbose`                               | Output logs to console.                                                                                                                                                                                                                                                                                                                                                                             | `True`                                                                                                 | `bool`                                                                    |


### fit_predict_text()

Mimics `sklearn.base.ClusterMixin.fit_predict()`. Given a sequence of texts, returns the cluster labels for each text.
Chooses best of `cluster_models` passed in `__init__()` based on `calculate_clustering_score()`
Post-processes clusters so that:
- large clusters are broken up
- small clusters are combined based on similarity

| **Param**                               | **Description**                                                                                                                                                                                                                           | **Default**                                            | **Type**                                                                  |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|---------------------------------------------------------------------------|
| `texts` | List of strings to cluster | N/A | `list[str]` |
from llm_clusterer import LLMClusterOptimizer
from sklearn.cluster import AffinityPropagation, HDBSCAN, KMeans
import numpy as np
from langchain_openai import OpenAIEmbeddings
import json
import math
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from util import guess_optimal_n_clusters
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

TEXT_DIR = "/Users/nss/sefaria/llm/experiments/topic_source_curation/_cache"

def get_texts_for_slug(slug):
    filename = f"{TEXT_DIR}/gathered_sources_{slug}.json"
    texts = []
    with open(filename, "r") as fin:
        jin = json.load(fin)
        for doc in jin:
            texts += [doc['source']["text"]['en']]
    return texts


def embed_text_openai(text):
    return np.array(OpenAIEmbeddings(model="text-embedding-3-large").embed_query(text))


def make_kmeans(n):
    return KMeans(n_clusters=n, init="k-means++", n_init=10)


def get_kmeans(embeddings):
    # n_clusters = guess_optimal_n_clusters(embeddings, lambda n: make_kmeans(n), verbose=True)
    return make_kmeans(3)


def recluster_threshold_fn(x):
    return round(math.sqrt(x)*1.5)


def build_optimizer():
    return LLMClusterOptimizer(get_kmeans, embed_text_openai, recluster_threshold_fn, 0.3,
                               verbose=True, summary_sample_size=15, _optimize=False)


def run_example(slug):
    texts = get_texts_for_slug(slug)
    print("Num texts", len(texts))
    optimizer = build_optimizer()
    labels = optimizer.fit_predict_text(texts)
    # for cluster in clusters:
    #     print(f"({len(cluster)})", cluster.summary)


if __name__ == '__main__':
    run_example("poverty")

"""
Params
- simplify params. no arrays. just take one model and reuse it. just one cosine distance
"""

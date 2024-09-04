import numpy as np
from sklearn.metrics import pairwise_distances, calinski_harabasz_score, silhouette_score
from scipy.stats import entropy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import skew

def ensure_2d(embeddings):
    if embeddings.ndim == 1:
        return embeddings.reshape(1, -1)
    return embeddings

def mean_pairwise_distance(embeddings):
    embeddings = ensure_2d(embeddings)
    distances = pairwise_distances(embeddings)
    return np.mean(distances)

def variance_pairwise_distance(embeddings):
    embeddings = ensure_2d(embeddings)
    distances = pairwise_distances(embeddings)
    return np.var(distances)

def mean_cosine_similarity(embeddings):
    embeddings = ensure_2d(embeddings)
    similarities = 1 - pairwise_distances(embeddings, metric='cosine')
    return np.mean(similarities)

def variance_cosine_similarity(embeddings):
    embeddings = ensure_2d(embeddings)
    similarities = 1 - pairwise_distances(embeddings, metric='cosine')
    return np.var(similarities)

def entropy_value(embeddings):
    embeddings = ensure_2d(embeddings)
    pca = PCA(n_components=0.95)
    reduced = pca.fit_transform(embeddings)
    hist, _ = np.histogram(reduced, bins=100)
    return entropy(hist)

def calinski_harabasz_index(embeddings, max_clusters=10):
    embeddings = ensure_2d(embeddings)
    scores = []
    for n_clusters in range(2, min(max_clusters + 1, len(embeddings))):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        score = calinski_harabasz_score(embeddings, labels)
        scores.append((score, n_clusters))
    
    max_score, best_n_clusters = max(scores)
    return max_score, best_n_clusters

def intrinsic_dimensionality(embeddings):
    embeddings = ensure_2d(embeddings)
    distances = pairwise_distances(embeddings)
    np.fill_diagonal(distances, np.inf)
    nearest_distances = np.min(distances, axis=1)
    return 1 / np.mean(np.log(distances / nearest_distances[:, np.newaxis]))

def local_outlier_factor(embeddings, n_neighbors=20):
    embeddings = ensure_2d(embeddings)
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination='auto')
    return -np.mean(lof.fit_predict(embeddings))

def silhouette_avg(embeddings, n_clusters=5):
    embeddings = ensure_2d(embeddings)
    if len(embeddings) < n_clusters:
        return np.nan
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)
    return silhouette_score(embeddings, labels)

def hubness_score(embeddings, k=5):
    embeddings = ensure_2d(embeddings)
    distances = pairwise_distances(embeddings)
    knn_indices = np.argpartition(distances, k, axis=1)[:, :k]
    n_k = np.bincount(knn_indices.flatten())
    return skew(n_k)

def get_all_metrics(embeddings):
    metrics = {
        "mean_pairwise_distance": mean_pairwise_distance(embeddings),
        "variance_pairwise_distance": variance_pairwise_distance(embeddings),
        "mean_cosine_similarity": mean_cosine_similarity(embeddings),
        "variance_cosine_similarity": variance_cosine_similarity(embeddings),
        "entropy_value": entropy_value(embeddings),
        "intrinsic_dimensionality": intrinsic_dimensionality(embeddings),
        "local_outlier_factor": local_outlier_factor(embeddings),
        "silhouette_score": silhouette_avg(embeddings),
        "hubness_score": hubness_score(embeddings)
    }
    ch_score, optimal_clusters = calinski_harabasz_index(embeddings)
    metrics["calinski_harabasz_score"] = ch_score
    metrics["optimal_clusters"] = optimal_clusters
    return metrics

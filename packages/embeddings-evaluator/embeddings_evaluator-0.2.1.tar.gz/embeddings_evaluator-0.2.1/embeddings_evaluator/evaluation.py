from .metrics import (
    mean_pairwise_distance, 
    variance_pairwise_distance,
    mean_cosine_similarity,
    variance_cosine_similarity,
    entropy_value,
    calinski_harabasz_index
)

def evaluate_embeddings(embeddings):
    ch_score, optimal_clusters = calinski_harabasz_index(embeddings)
    return {
        "mean_pairwise_distance": mean_pairwise_distance(embeddings),
        "variance_pairwise_distance": variance_pairwise_distance(embeddings),
        "mean_cosine_similarity": mean_cosine_similarity(embeddings),
        "variance_cosine_similarity": variance_cosine_similarity(embeddings),
        "entropy_value": entropy_value(embeddings),
        "calinski_harabasz_score": ch_score,
        "optimal_clusters": optimal_clusters
    }

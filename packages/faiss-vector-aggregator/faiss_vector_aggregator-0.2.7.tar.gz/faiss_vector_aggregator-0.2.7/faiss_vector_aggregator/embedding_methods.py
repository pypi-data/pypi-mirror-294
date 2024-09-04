import numpy as np
from scipy.stats import gmean, hmean, entropy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def calculate_embedding(embeddings, method, weights=None, trim_percentage=0.1):
    if method == "average":
        return np.mean(embeddings, axis=0)
    elif method == "weighted_average":
        if weights is not None:
            return np.average(embeddings, axis=0, weights=weights)
        else:
            raise ValueError("Weights must be provided for weighted average.")
    elif method == "median":
        return np.median(embeddings, axis=0)
    elif method == "geometric_mean":
        return gmean(embeddings, axis=0)
    elif method == "harmonic_mean":
        return hmean(embeddings, axis=0)
    elif method == "trimmed_mean":
        return calculate_trimmed_mean(embeddings, trim_percentage)
    elif method == "centroid":
        kmeans = KMeans(n_clusters=1, random_state=0).fit(embeddings)
        return kmeans.cluster_centers_[0]
    elif method == "pca":
        pca = PCA(n_components=1)
        return pca.fit_transform(embeddings).flatten()
    elif method == "exemplar":
        similarities = np.mean(cdist(embeddings, embeddings, metric='cosine'), axis=1)
        return embeddings[np.argmin(similarities)]
    elif method == "max_pooling":
        return np.max(embeddings, axis=0)
    elif method == "min_pooling":
        return np.min(embeddings, axis=0)
    elif method == "entropy_weighted_average":
        return calculate_entropy_weighted_average(embeddings)
    elif method == "attentive_pooling":
        return calculate_attentive_pooling(embeddings)
    elif method == "tukeys_biweight":
        return calculate_tukeys_biweight(embeddings)
    else:
        raise ValueError(f"Unknown method: {method}")

def calculate_trimmed_mean(embeddings, trim_percentage):
    lower_bound = int(trim_percentage * len(embeddings))
    upper_bound = len(embeddings) - lower_bound
    trimmed_embeddings = np.sort(embeddings, axis=0)[lower_bound:upper_bound]
    return np.mean(trimmed_embeddings, axis=0)

def calculate_entropy_weighted_average(embeddings):
    entropies = entropy(np.abs(embeddings), axis=1)
    normalized_entropies = entropies / np.sum(entropies)
    return np.average(embeddings, axis=0, weights=normalized_entropies)

def calculate_attentive_pooling(embeddings):
    similarities = np.dot(embeddings, np.mean(embeddings, axis=0))
    attention_weights = np.exp(similarities) / np.sum(np.exp(similarities))
    return np.sum(embeddings * attention_weights[:, np.newaxis], axis=0)

def calculate_tukeys_biweight(embeddings):
    median_embedding = np.median(embeddings, axis=0)
    diff = embeddings - median_embedding
    mad = np.median(np.abs(diff), axis=0)
    u = diff / (9 * mad)
    u2 = u ** 2
    mask = u2 < 1
    return median_embedding + np.sum(mask * diff * (1 - u2) ** 2, axis=0) / np.sum(mask)

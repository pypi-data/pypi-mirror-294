
# Faiss Embeddings Aggregation Library

This Python library provides various methods for aggregating multiple embeddings associated with a single document or entity into a single representative embedding. It supports a wide range of aggregation techniques, from simple averaging to advanced methods like PCA and Attentive Pooling.

## Features

- **Simple Average**: Compute the arithmetic mean of embeddings.
- **Weighted Average**: Compute a weighted average of embeddings.
- **Geometric Mean**: Compute the geometric mean across embeddings.
- **Harmonic Mean**: Compute the harmonic mean across embeddings.
- **Centroid (K-Means)**: Use K-Means clustering to find the centroid of the embeddings.
- **Principal Component (PCA)**: Use PCA to reduce embeddings to a single principal component.
- **Median**: Compute the element-wise median of embeddings.
- **Trimmed Mean**: Compute the mean after trimming outliers.
- **Max-Pooling**: Take the maximum value for each dimension across embeddings.
- **Min-Pooling**: Take the minimum value for each dimension across embeddings.
- **Entropy-Weighted Average**: Weight embeddings by their entropy (information content).
- **Attentive Pooling**: Use an attention mechanism to learn the weights for combining embeddings.
- **Tukey's Biweight**: A robust method to down-weight outliers.

## Installation

To install the package, you can use pip:

```bash
pip install faiss_vector_aggregator
```

## Usage

Here are some examples of how to use the library to aggregate embeddings.

### Example 1: Simple Average Aggregation

Suppose you have a collection of embeddings stored in a FAISS index, and you want to aggregate them by their associated document IDs using simple averaging. Here's how you can do it:

```python
from faiss_vector_aggregator import aggregate_embeddings

# Aggregate embeddings using simple averaging
aggregate_embeddings(
    input_folder="data/input",
    column_name="id",
    output_folder="data/output",
    method="average"
)
```

In this example:
- `input_folder`: Path to the folder containing the input FAISS index and metadata.
- `column_name`: The column or metadata field by which to aggregate embeddings.
- `output_folder`: Path where the output FAISS index and metadata will be saved.
- `method="average"`: Specifies that the average method should be used for aggregation.

### Example 2: Weighted Average Aggregation

If you have different weights for the embeddings, you can apply a weighted average to give more importance to certain embeddings. For instance:

```python
from faiss_vector_aggregator import aggregate_embeddings

# Example weights for the embeddings
weights = [0.1, 0.3, 0.6]

# Aggregate embeddings using weighted averaging
aggregate_embeddings(
    input_folder="data/input",
    column_name="id",
    output_folder="data/output",
    method="weighted_average",
    weights=weights
)
```

In this example:
- `weights`: A list of weights corresponding to each embedding.
- `method="weighted_average"`: Specifies that the weighted average method should be used for aggregation.

### Example 3: Principal Component Analysis (PCA) Aggregation

If you want to reduce high-dimensional embeddings to a single vector using Principal Component Analysis (PCA), you can use the following approach:

```python
from faiss_vector_aggregator import aggregate_embeddings

# Aggregate embeddings using PCA
aggregate_embeddings(
    input_folder="data/input",
    column_name="id",
    output_folder="data/output",
    method="pca"
)
```

In this example:
- `method="pca"`: Specifies that PCA should be used to reduce and aggregate the embeddings into a single vector.

### Example 4: Centroid Aggregation (K-Means)

To use K-Means clustering for finding the centroid of embeddings for each document ID:

```python
from faiss_vector_aggregator import aggregate_embeddings

# Aggregate embeddings using K-Means clustering to find the centroid
aggregate_embeddings(
    input_folder="data/input",
    column_name="id",
    output_folder="data/output",
    method="centroid"
)
```

In this example:
- `method="centroid"`: Specifies that K-Means clustering should be used to find the centroid for aggregation.

## Parameters

- `input_folder`: Path to the folder containing the input FAISS index and metadata.
- `column_name`: The column or metadata field by which to aggregate embeddings (e.g., 'id').
- `output_folder`: Path to the folder where the output FAISS index and metadata will be saved.
- `method`: The aggregation method to use (`average`, `weighted_average`, `geometric_mean`, `harmonic_mean`, `centroid`, `pca`, `median`, `trimmed_mean`, `max_pooling`, `min_pooling`, `entropy_weighted_average`, `attentive_pooling`, `tukeys_biweight`).
- `weights`: Optional weights for the `weighted_average` method.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

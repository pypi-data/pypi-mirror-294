import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP
from .metrics import get_all_metrics
from sklearn.metrics import pairwise_distances

def evaluate_embeddings(embeddings, label=None):
    """
    Evaluate a single set of embeddings or multiple sets of embeddings.

    Parameters:
    embeddings (np.ndarray or list of np.ndarray): Embeddings to evaluate.
    label (str or list of str, optional): Label(s) for the embeddings.

    Returns:
    pd.DataFrame: A DataFrame containing the metrics for each embedding.
    """
    if isinstance(embeddings, list):
        results = []
        labels = label if isinstance(label, list) else [f"Embedding {i+1}" for i in range(len(embeddings))]
        for emb, lbl in zip(embeddings, labels):
            metrics = get_all_metrics(emb)
            metrics['label'] = lbl
            results.append(metrics)
        return pd.DataFrame(results)
    else:
        metrics = get_all_metrics(embeddings)
        metrics['label'] = label if label else "Embedding"
        return pd.DataFrame([metrics])

def plot_metrics(df):
    """
    Plot all metrics from the DataFrame using line plots.

    Parameters:
    df (pd.DataFrame): DataFrame containing the metrics for each embedding.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    metrics = [col for col in df.columns if col != 'label']
    num_metrics = len(metrics)
    rows = (num_metrics + 1) // 2
    cols = 2

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=metrics)

    for i, metric in enumerate(metrics):
        row = i // 2 + 1
        col = i % 2 + 1
        
        trace = go.Scatter(x=df['label'], y=df[metric], mode='lines+markers', name=metric)
        fig.add_trace(trace, row=row, col=col)

        fig.update_xaxes(title_text="Embeddings", row=row, col=col)
        fig.update_yaxes(title_text=metric, row=row, col=col)

    fig.update_layout(height=300*rows, width=1000, title_text="Comparison of Embedding Metrics")
    return fig

def plot_interactive_scatter(embeddings, labels, method='pca', dimensions=2):
    """
    Create an interactive scatter plot of the embeddings using the specified dimensionality reduction method.

    Parameters:
    embeddings (np.ndarray): The embeddings to visualize.
    labels (list): List of labels corresponding to each embedding point.
    method (str): Dimensionality reduction method. Options: 'pca', 'tsne', 'umap'. Default is 'pca'.
    dimensions (int): Number of dimensions for the plot. Options: 2 or 3. Default is 2.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    if method == 'pca':
        reducer = PCA(n_components=dimensions)
    elif method == 'tsne':
        reducer = TSNE(n_components=dimensions, random_state=42)
    elif method == 'umap':
        reducer = UMAP(n_components=dimensions, random_state=42)
    else:
        raise ValueError("Invalid method. Choose 'pca', 'tsne', or 'umap'.")

    reduced_embeddings = reducer.fit_transform(embeddings)

    if dimensions == 2:
        df = pd.DataFrame(reduced_embeddings, columns=['Dim1', 'Dim2'])
        fig = go.Figure(data=go.Scatter(x=df['Dim1'], y=df['Dim2'], mode='markers',
                                        marker=dict(color=labels),
                                        text=labels,
                                        hoverinfo='text'))
        fig.update_layout(title=f'2D Projection of Embeddings ({method.upper()})',
                          xaxis_title='Dimension 1',
                          yaxis_title='Dimension 2')
    elif dimensions == 3:
        df = pd.DataFrame(reduced_embeddings, columns=['Dim1', 'Dim2', 'Dim3'])
        fig = go.Figure(data=go.Scatter3d(x=df['Dim1'], y=df['Dim2'], z=df['Dim3'],
                                          mode='markers',
                                          marker=dict(color=labels, size=5),
                                          text=labels,
                                          hoverinfo='text'))
        fig.update_layout(title=f'3D Projection of Embeddings ({method.upper()})',
                          scene=dict(xaxis_title='Dimension 1',
                                     yaxis_title='Dimension 2',
                                     zaxis_title='Dimension 3'))
    else:
        raise ValueError("Invalid dimensions. Choose 2 or 3.")

    return fig

def plot_pairwise_distance_histogram(embeddings):
    """
    Plot a histogram of pairwise distances between embeddings.

    Parameters:
    embeddings (np.ndarray): The embeddings to visualize.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    distances = pairwise_distances(embeddings).flatten()
    fig = ff.create_distplot([distances], ['Pairwise Distances'], bin_size=0.2)
    fig.update_layout(title_text='Histogram of Pairwise Distances')
    return fig

def plot_similarity_heatmap(embeddings, labels):
    """
    Plot a heatmap of pairwise similarities between embeddings.

    Parameters:
    embeddings (np.ndarray): The embeddings to visualize.
    labels (list): List of labels corresponding to each embedding point.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    similarities = 1 - pairwise_distances(embeddings, metric='cosine')
    fig = go.Figure(data=go.Heatmap(z=similarities, x=labels, y=labels))
    fig.update_layout(title='Pairwise Similarity Heatmap')
    return fig

def plot_cumulative_explained_variance(embeddings):
    """
    Plot the cumulative explained variance ratio for PCA.

    Parameters:
    embeddings (np.ndarray): The embeddings to analyze.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    pca = PCA()
    pca.fit(embeddings)
    cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
    
    fig = go.Figure(data=go.Scatter(x=list(range(1, len(cumulative_variance_ratio) + 1)),
                                    y=cumulative_variance_ratio,
                                    mode='lines+markers'))
    fig.update_layout(title='Cumulative Explained Variance Ratio',
                      xaxis_title='Number of Components',
                      yaxis_title='Cumulative Explained Variance Ratio')
    return fig

def plot_intrinsic_dimensionality(embeddings, max_dims=100):
    """
    Plot the intrinsic dimensionality estimation.

    Parameters:
    embeddings (np.ndarray): The embeddings to analyze.
    max_dims (int): Maximum number of dimensions to consider.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive Plotly figure.
    """
    from .metrics import intrinsic_dimensionality
    
    dims = list(range(1, min(embeddings.shape[1], max_dims) + 1))
    id_values = [intrinsic_dimensionality(embeddings[:, :d]) for d in dims]
    
    fig = go.Figure(data=go.Scatter(x=dims, y=id_values, mode='lines+markers'))
    fig.update_layout(title='Intrinsic Dimensionality Estimation',
                      xaxis_title='Number of Dimensions',
                      yaxis_title='Estimated Intrinsic Dimensionality')
    return fig

import torch
from einops import rearrange
from spacez.blur import GaussianBlur2D


def kmeans_plus_plus_init(X, k, random_state=None):
    """
    Initialize the centroids for K-means clustering using the K-means++
    algorithm.

    Parameters:
    X (torch.Tensor): The input data tensor with shape (n_samples, n_features).
    k (int): The number of clusters.
    random_state (int, optional): Seed for random number generator for
    reproducibility.

    Returns:
    torch.Tensor: Initialized centroids with shape (k, n_features).
    """
    if random_state is not None:
        torch.manual_seed(random_state)

    n_samples, n_features = X.shape
    centers = torch.empty((k, n_features), device=X.device)

    # Choose the first center randomly
    random_idx = torch.randint(0, n_samples, (1,))
    centers[0] = X[random_idx]

    # Compute the initial distances
    closest_dist_sq = torch.full((n_samples,), float("inf"), device=X.device)
    for i in range(1, k):
        distances = torch.sum((X - centers[i - 1]) ** 2, dim=1)
        closest_dist_sq = torch.minimum(closest_dist_sq, distances)

        # Choose the next center with a probability proportional to the
        # distance squared
        prob = closest_dist_sq / closest_dist_sq.sum()
        cumulative_prob = torch.cumsum(prob, dim=0)
        r = torch.rand(1, device=X.device)
        next_center_idx = torch.searchsorted(cumulative_prob, r)
        centers[i] = X[next_center_idx]
    return centers


class SpatialKMeans:
    """
    A class for performing spatially-aware K-means clustering with optional
    Gaussian smoothing.

    Attributes:
    n_clusters (int): Number of clusters.
    max_iter (int): Maximum number of iterations for the K-means algorithm.
    burn_in (int): Number of initial iterations without smoothing.
    tol (float): Tolerance for convergence.
    smoothing_sigma (float): Standard deviation for Gaussian smoothing.
    device (str): Device to perform computations on ('cuda' or 'cpu').
    centroids (torch.Tensor): Centroids of the clusters.

    Methods:
    fit(data, tau=0.1): Fit the model to the provided data.
    predict(data): Predict the closest cluster each sample in the data
    belongs to.
    predict_proba(data): Compute the probability of each sample belonging to
    each cluster.
    """

    def __init__(
        self,
        n_clusters,
        max_iter=300,
        burn_in=50,
        tol=1e-8,
        smoothing_sigma=1.0,
        kernel_size=15,
        power=2.0,
        device="cuda",
    ):
        """
        Initialize the SpatialKMeans clustering model.

        Parameters:
        n_clusters (int): Number of clusters.
        max_iter (int): Maximum number of iterations for the K-means algorithm.
        burn_in (int): Number of initial iterations without smoothing.
        tol (float): Tolerance for convergence.
        smoothing_sigma (float): Standard deviation for Gaussian smoothing.
        device (str): Device to perform computations on ('cuda' or 'cpu').
        """
        self.centroids = None
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.burn_in = burn_in
        self.tol = tol
        self.smoothing_sigma = smoothing_sigma
        self.kernel_size = kernel_size
        self.power = power
        self.device = device
        self.gaussian_filter = GaussianBlur2D(
            self.smoothing_sigma, max_kernel_size=self.kernel_size, device=self.device
        )

    def fit(self, data, tau=0.1):
        """
        Fit the SpatialKMeans model to the provided data.

        Parameters:
        data (numpy.ndarray): Input data with shape (C, Y, X), where C is
        the number of channels.
        tau (float): Blending factor for centroid update after burn-in period.

        Returns:
        None
        """
        # Reshape the data from (C, Y, X) to (Y * X, C)
        C, Y, X = data.shape
        X_flat = rearrange(data.clone().detach(), "c y x -> (y x) c")

        # Move data to the device
        X_flat = X_flat.to(self.device)
        n_samples, _ = X_flat.shape

        # Initialize centroids using k-means++ initialization
        self.centroids = kmeans_plus_plus_init(X_flat, self.n_clusters)

        # Calculate the mean vector of the image data
        mean_vector = X_flat.mean(dim=0)

        for i in range(self.max_iter):
            # Compute distances from samples to centroids
            distances = torch.cdist(X_flat, self.centroids)  # .cpu().numpy()

            # Reshape distances to (Y, X, n_clusters) for smoothing
            distances_reshaped = rearrange(distances, "(y x) k -> () k y x", y=Y, x=X)
            if i > self.burn_in:
                distances_reshaped = self.gaussian_filter(
                    distances_reshaped**self.power
                )

            # Reshape back to (Y * X, n_clusters)
            distances = rearrange(distances_reshaped[0], "k y x -> (y x) k")

            # Assign samples to the nearest centroids
            labels = torch.argmin(distances, dim=1)

            # Compute new centroids as the mean of assigned samples
            new_centroids = torch.zeros_like(self.centroids)
            for j in range(self.n_clusters):
                if torch.sum(labels == j) > 0:
                    new_centroids[j] = X_flat[labels == j].mean(dim=0)
                else:
                    # Set this centroid to the mean vector of the image data
                    # if no samples were assigned
                    new_centroids[j] = mean_vector

            # Check for convergence
            delta = torch.norm(new_centroids - self.centroids)
            if delta < self.tol:
                break

            if i > self.burn_in:
                self.centroids = new_centroids * tau + self.centroids * (1 - tau)
            else:
                self.centroids = new_centroids

    def predict(self, data):
        """
        Predict the closest cluster each sample in the data belongs to.

        Parameters:
        data (numpy.ndarray): Input data with shape (C, Y, X), where C is
        the number of channels.

        Returns:
        numpy.ndarray: Array of shape (Y, X) containing the cluster index
        for each pixel.
        """
        # Reshape the data from (C, Y, X) to (Y * X, C)
        C, Y, X = data.shape
        X_flat = rearrange(data.clone().detach(), "c y x -> (y x) c")

        # Move data to the device
        X_flat = X_flat.to(self.device)
        distances = torch.cdist(X_flat, self.centroids)
        # Reshape distances to (Y, X, n_clusters) for smoothing
        distances_reshaped = rearrange(distances, "(y x) k -> () k y x", y=Y, x=X)

        # Apply smoothing on the distance matrix
        distances_reshaped = self.gaussian_filter(distances_reshaped**self.power)

        labels = torch.argmin(distances_reshaped[0], dim=0)
        return labels

    def predict_proba(self, data):
        """
        Compute the probability of each sample belonging to each cluster.

        Parameters:
        data (numpy.ndarray): Input data with shape (C, Y, X), where C is
        the number of channels.

        Returns:
        numpy.ndarray: Array of shape (Y, X, n_clusters) containing the
        probabilities for each pixel.
        """
        # Reshape the data from (C, Y, X) to (Y * X, C)
        C, Y, X = data.shape
        X_flat = rearrange(data.clone().detach(), "c y x -> (y x) c")

        # Move data to the device
        X_flat = X_flat.to(self.device)
        distances = torch.cdist(X_flat, self.centroids)

        # Reshape distances to (Y, X, n_clusters) for smoothing
        distances_reshaped = rearrange(distances, "(y x) k -> () k y x", y=Y, x=X)
        distances_reshaped = self.gaussian_filter(distances_reshaped**self.power)

        similarities = 1.0 / (
            distances_reshaped + 1e-10
        )  # Add small value to avoid division by zero
        probabilities = similarities / similarities.sum(axis=1, keepdims=True)

        # Reshape probabilities to (Y, X, n_clusters)
        return probabilities

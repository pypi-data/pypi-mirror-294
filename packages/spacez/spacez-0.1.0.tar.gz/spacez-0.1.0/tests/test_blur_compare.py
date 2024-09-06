import pytest
import torch
import numpy as np
from scipy.ndimage import gaussian_filter
from spacez.blur import GaussianBlur2D, GaussianBlur3D


@pytest.mark.parametrize(
    "size, sigma, tolerance",
    [
        (64, 1.0, 1e-3),
        (64, 2.0, 1e-3),
        (64, 3.0, 1e-3),
    ],
)
def test_blur_compare(size, sigma, tolerance):
    """
    Test function that compares the Gaussian blurring of a central pixel/voxel in a 2D and 3D array
    between PyTorch and SciPy implementations.

    Args:
        size (int): The size of the 2D and 3D arrays.
        sigma (float): The standard deviation for the Gaussian kernel.
        tolerance (float): The acceptable tolerance for numerical differences.
    """

    # Create a 2D array with the central pixel set to 1
    array_2d = np.zeros((size, size), dtype=np.float32)
    array_2d[size // 2, size // 2] = 1.0

    # Create a 3D array with the central voxel set to 1
    array_3d = np.zeros((size, size, size), dtype=np.float32)
    array_3d[size // 2, size // 2, size // 2] = 1.0

    # Apply Gaussian blur using SciPy
    scipy_blurred_2d = gaussian_filter(array_2d, sigma=sigma)
    scipy_blurred_3d = gaussian_filter(array_3d, sigma=sigma)

    # Convert numpy arrays to torch tensors
    torch_array_2d = (
        torch.from_numpy(array_2d).unsqueeze(0).unsqueeze(0)
    )  # Shape: (1, 1, size, size)
    torch_array_3d = (
        torch.from_numpy(array_3d).unsqueeze(0).unsqueeze(0)
    )  # Shape: (1, 1, size, size, size)

    # Apply Gaussian blur using PyTorch (assuming GaussianBlur2D and GaussianBlur3D are defined in your module)
    blur_2d_layer = GaussianBlur2D(initial_sigma=sigma, max_kernel_size=15, grads=False)
    blur_3d_layer = GaussianBlur3D(initial_sigma=sigma, max_kernel_size=15, grads=False)

    with torch.no_grad():  # Disable gradients for blurring
        torch_blurred_2d = blur_2d_layer(torch_array_2d).squeeze().numpy()
        torch_blurred_3d = blur_3d_layer(torch_array_3d).squeeze().numpy()

    # Compare the results numerically
    difference_2d = np.abs(scipy_blurred_2d - torch_blurred_2d).max()
    difference_3d = np.abs(scipy_blurred_3d - torch_blurred_3d).max()

    assert (
        difference_2d < tolerance
    ), f"2D blur difference {difference_2d} exceeds tolerance {tolerance}"
    assert (
        difference_3d < tolerance
    ), f"3D blur difference {difference_3d} exceeds tolerance {tolerance}"


if __name__ == "__main__":
    pytest.main()

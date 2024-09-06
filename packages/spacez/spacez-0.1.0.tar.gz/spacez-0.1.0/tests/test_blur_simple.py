import pytest
import torch
from spacez.blur import GaussianBlur2D, GaussianBlur3D


@pytest.mark.parametrize(
    "batch_size, channels, depth, height, width",
    [(1, 1, 5, 5, 5), (2, 3, 7, 7, 7), (1, 1, 10, 10, 10)],
)
def test_gaussian_blur_3d(batch_size, channels, depth, height, width):
    # Initialize GaussianBlur3D
    initial_sigma = 1.0
    blur_layer = GaussianBlur3D(initial_sigma, max_kernel_size=5, grads=False)

    # Check sigma requires_grad
    assert not blur_layer.sigma.requires_grad

    # Create random 3D input tensor
    input_tensor = torch.rand((batch_size, channels, depth, height, width))

    # Apply Gaussian blur
    output_tensor = blur_layer(input_tensor)

    # Ensure output has same shape as input
    assert output_tensor.shape == input_tensor.shape

    # Check if output is not the same as input (since blurring should change the values)
    assert not torch.equal(input_tensor, output_tensor)


@pytest.mark.parametrize(
    "batch_size, channels, height, width",
    [(1, 1, 5, 5), (2, 3, 7, 7), (1, 1, 10, 10)],
)
def test_gaussian_blur_2d(batch_size, channels, height, width):
    # Initialize GaussianBlur2D
    initial_sigma = 1.0
    blur_layer = GaussianBlur2D(initial_sigma, max_kernel_size=5, grads=False)

    # Check sigma requires_grad
    assert not blur_layer.sigma.requires_grad

    # Create random 2D input tensor
    input_tensor = torch.rand((batch_size, channels, height, width))

    # Apply Gaussian blur
    output_tensor = blur_layer(input_tensor)

    # Ensure output has same shape as input
    assert output_tensor.shape == input_tensor.shape

    # Check if output is not the same as input (since blurring should change the values)
    assert not torch.equal(input_tensor, output_tensor)


def test_gaussian_blur_3d_grads():
    initial_sigma = 1.0
    blur_layer = GaussianBlur3D(initial_sigma, max_kernel_size=5, grads=True)

    # Check sigma requires_grad
    assert blur_layer.sigma.requires_grad

    # Create random 3D input tensor
    input_tensor = torch.rand((1, 1, 5, 5, 5))

    # Apply Gaussian blur
    output_tensor = blur_layer(input_tensor)

    # Ensure output has same shape as input
    assert output_tensor.shape == input_tensor.shape


def test_gaussian_blur_2d_grads():
    initial_sigma = 1.0
    blur_layer = GaussianBlur2D(initial_sigma, max_kernel_size=5, grads=True)

    # Check sigma requires_grad
    assert blur_layer.sigma.requires_grad

    # Create random 2D input tensor
    input_tensor = torch.rand((1, 1, 5, 5))

    # Apply Gaussian blur
    output_tensor = blur_layer(input_tensor)

    # Ensure output has same shape as input
    assert output_tensor.shape == input_tensor.shape


if __name__ == "__main__":
    pytest.main()

import numpy as np
from spacez import spacez_2d
import torch
import pytest


def test_cluster_2d():
    img = np.zeros((128, 128))
    img[20:40, 20:40] = 1.0
    img[80:100, 80:100] = 1.0
    cluster = img > 0.5
    img += np.random.uniform(-0.5, 0.5, img.shape)
    img = torch.Tensor(img).unsqueeze(0)
    for ii in range(10):
        obj = spacez_2d.SpatialKMeans(
            n_clusters=3, smoothing_sigma=0.75, tol=1e-5, burn_in=50
        )
        obj.fit(img)
        labels = obj.predict(img)
        d = np.mean(labels[cluster].cpu().numpy()) % 1.0
        if d > 0.5:
            d = 1 - d
        assert d < 0.05


if __name__ == "__main__":
    pytest.main()

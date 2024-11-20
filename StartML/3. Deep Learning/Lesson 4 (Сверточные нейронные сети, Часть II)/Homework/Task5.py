import numpy as np
import torch


def get_normalize(features: torch.Tensor):
    means = features.data.to(torch.float32).mean(axis=(0,2,3))
    stds = features.data.to(torch.float32).std(axis=(0,2,3))
    return means, stds


arr = np.arange(5 * 2 * 4 * 4).reshape(5, 2, 4, 4)
print(get_normalize(torch.from_numpy(arr)))

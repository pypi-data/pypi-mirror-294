# mypy: disable-error-code="empty-body,no-redef,misc"
from typing import Union, overload

import numpy as np
import torch
from torch import Tensor

from fastdev.extension import FDEV_EXT
from fastdev.utils.dispatch import singledispatch


@overload
@singledispatch()
def sample_farthest_points(points: Tensor, num_samples: int) -> Tensor:
    if points.dim() != 3 and points.dim() != 2:
        raise ValueError("points should be in shape (B, N, 3) or (N, 3).")

    is_batch_input = points.dim() == 3
    if not is_batch_input:
        points = points.unsqueeze(0)

    indices = FDEV_EXT.load_module("fastdev_sample_farthest_points").sample_farthest_points(
        points,
        torch.ones((points.shape[0],), dtype=torch.long, device=points.device) * points.shape[1],
        torch.ones((points.shape[0],), dtype=torch.long, device=points.device) * num_samples,
        torch.zeros((points.shape[0],), dtype=torch.long, device=points.device),
    )

    if not is_batch_input:
        return indices.squeeze(0)
    else:
        return indices


@overload
@singledispatch()
def sample_farthest_points(points: np.ndarray, num_samples: int) -> np.ndarray:
    xyz = points[..., :3]
    centroids = np.zeros(points.shape[:-2] + (num_samples,), dtype=np.int64)
    distance = np.ones(points.shape[:-1]) * 1e10
    farthest = np.zeros(points.shape[:-2], dtype=np.int64)
    for i in range(num_samples):
        centroids[..., i] = farthest
        centroid = np.take_along_axis(xyz, farthest[..., None, None], axis=-2)
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[..., mask] = dist[..., mask]
        farthest = np.argmax(distance, axis=-1)
    return centroids


@singledispatch(is_impl=False)
def sample_farthest_points(points: Union[Tensor, np.ndarray], num_samples: int) -> Union[Tensor, np.ndarray]:
    """Sample farthest points.

    Args:
        points (Union[Tensor, np.ndarray]): points in shape (B, N, 3) or (N, 3)
        num_samples (int): number of samples

    Returns:
        Union[Tensor, np.ndarray]: sampled indices in shape (B, num_samples) or (num_samples,)
    """
    ...


__all__ = ["sample_farthest_points"]

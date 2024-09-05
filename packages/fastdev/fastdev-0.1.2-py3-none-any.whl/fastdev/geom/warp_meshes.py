# mypy: disable-error-code="valid-type"
from __future__ import annotations

from typing import Tuple

import numpy as np
import torch
import trimesh
import warp as wp
from einops import rearrange, repeat
from torch import Tensor
from trimesh import Trimesh

from fastdev.geom.warp_sdf_fns import (
    query_sdf_on_multiple_meshes,
    query_sdf_on_multiple_meshes_v2,
    query_sdf_on_multiple_posed_meshes,
    query_sdf_on_multiple_posed_meshes_v2,
)
from fastdev.utils.struct_utils import list_to_padded
from fastdev.xform.transforms import inverse_tf_mat, transform_points


class QuerySignedDistances(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx, query_points: Tensor, mesh_ids: Tensor, inv_mesh_poses: Tensor | None = None, max_dist: float = 1e6
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Forward pass of the signed distance function.

        Args:
            query_points (Tensor): query points, shape (B, N, 3).
            mesh_ids (Tensor): mesh ids, shape (B, M) or (1, M).
            inv_mesh_poses (Tensor): inversed mesh poses, shape (B, M, 4, 4).
            max_dist (float, optional): maximum distance. Defaults to 1e6.

        Returns:
            tuple[Tensor, Tensor, Tensor]: differentiable signed distances (B, N), normals (B, N, 3), closest points (B, N, 3).
        """
        if query_points.ndim != 3 or query_points.shape[2] != 3:
            msg = f"Invalid shape for query_points, expected (B, N, 3), got {query_points.shape}."
            raise ValueError(msg)
        packed_query_points = query_points.detach().view(-1, 3).contiguous()  # (B * N, 3)

        packed_mesh_ids = mesh_ids.unsqueeze(1).expand(query_points.shape[:2] + (-1,))  # (B, N, M)
        packed_mesh_ids = packed_mesh_ids.reshape(packed_query_points.shape[0], -1).contiguous()  # (B * N, M)

        packed_signed_dists = torch.zeros_like(packed_query_points[:, 0])  # (B * N)
        packed_closest_points = torch.zeros_like(packed_query_points)  # (B * N, 3)
        packed_normals = torch.zeros_like(packed_query_points)  # (B * N, 3)
        packed_points_jacob = torch.zeros_like(packed_query_points)  # (B * N, 3)

        if inv_mesh_poses is None:
            wp.launch(
                kernel=query_sdf_on_multiple_meshes,
                dim=packed_query_points.shape[0],
                inputs=[
                    wp.from_torch(packed_query_points, dtype=wp.vec3),
                    wp.from_torch(packed_mesh_ids, dtype=wp.uint64),
                    max_dist,
                    query_points.requires_grad,
                    wp.from_torch(packed_signed_dists, dtype=wp.float32),
                    wp.from_torch(packed_normals, dtype=wp.vec3),
                    wp.from_torch(packed_closest_points, dtype=wp.vec3),
                    wp.from_torch(packed_points_jacob, dtype=wp.vec3),
                ],
                device=wp.device_from_torch(query_points.device),
            )
            ctx.save_for_backward(packed_points_jacob.view(query_points.shape), None)
        else:
            if (
                inv_mesh_poses.ndim != 4
                or inv_mesh_poses.shape[-2:] != (4, 4)
                or inv_mesh_poses.shape[1] != mesh_ids.shape[1]
            ):
                raise ValueError(f"Invalid shape for mesh_poses, expected (B, M, 4, 4), got {inv_mesh_poses.shape}.")

            packed_inv_mesh_poses = repeat(
                inv_mesh_poses.detach(), "b ... -> (b n) ...", n=query_points.shape[1]
            ).contiguous()
            packed_inv_mesh_poses_jacob = torch.zeros_like(packed_inv_mesh_poses)
            wp.launch(
                kernel=query_sdf_on_multiple_posed_meshes,
                dim=packed_query_points.shape[0],
                inputs=[
                    wp.from_torch(packed_query_points, dtype=wp.vec3),
                    wp.from_torch(packed_mesh_ids, dtype=wp.uint64),
                    wp.from_torch(packed_inv_mesh_poses, dtype=wp.mat44),
                    max_dist,
                    query_points.requires_grad,
                    inv_mesh_poses.requires_grad,
                    wp.from_torch(packed_signed_dists, dtype=wp.float32),
                    wp.from_torch(packed_normals, dtype=wp.vec3),
                    wp.from_torch(packed_closest_points, dtype=wp.vec3),
                    wp.from_torch(packed_points_jacob, dtype=wp.vec3),
                    wp.from_torch(packed_inv_mesh_poses_jacob, dtype=wp.mat44),
                ],
                device=wp.device_from_torch(query_points.device),
            )
            ctx.save_for_backward(
                packed_points_jacob.view(query_points.shape),
                rearrange(packed_inv_mesh_poses_jacob, "(b n) m ... -> b n m ...", n=query_points.shape[1]),
            )

        ctx.mark_non_differentiable(packed_normals, packed_closest_points)

        return (
            packed_signed_dists.view(query_points.shape[:2]),
            packed_normals.view(query_points.shape),
            packed_closest_points.view(query_points.shape),
        )

    @staticmethod
    def backward(ctx, grad_signed_dists, grad_normals, grad_closest_points):
        points_jacob, inv_poses_jacob = ctx.saved_tensors
        if points_jacob is not None:
            grad_points = grad_signed_dists.unsqueeze(-1) * points_jacob
        else:
            grad_points = None
        if inv_poses_jacob is not None:
            grad_inv_poses = torch.einsum("bn...,bnm...->bm...", grad_signed_dists, inv_poses_jacob)
        else:
            grad_inv_poses = None
        return grad_points, None, grad_inv_poses, None


class WarpMeshes:
    """Meshes for differentiable signed distance queries."""

    def __init__(
        self,
        verts: list[list[np.ndarray]] | None = None,
        faces: list[list[np.ndarray]] | None = None,
        warp_meshes: list[list[wp.Mesh]] | None = None,
        device: str = "cpu",
    ):
        wp.config.quiet = True
        wp.init()
        self._device_wp = wp.get_device(str(device))
        if warp_meshes is not None:
            self._meshes = warp_meshes
        elif (verts is not None) and (faces is not None):
            self._meshes = []

            for v_list, f_list in zip(verts, faces):
                if isinstance(v_list, np.ndarray):
                    v_list = [v_list]
                if isinstance(f_list, np.ndarray):
                    f_list = [f_list]
                m_list = []
                for v, f in zip(v_list, f_list):
                    if v.shape[0] == 0 or f.shape[0] == 0:
                        raise ValueError("Vertices and faces must not be empty.")
                    m_list.append(
                        wp.Mesh(
                            points=wp.array(v, dtype=wp.vec3, device=self._device_wp),
                            indices=wp.array(np.ravel(f), dtype=int, device=self._device_wp),
                        )
                    )
                self._meshes.append(m_list)
        else:
            raise ValueError("Either meshes or verts and faces must be provided.")

        mesh_ids = [
            torch.tensor([m.id for m in m_list], device=wp.device_to_torch(self._device_wp)) for m_list in self._meshes
        ]
        self._mesh_ids = list_to_padded(mesh_ids, pad_value=0)

    @staticmethod
    def from_files(filenames: str | list[list[str] | str], device: str = "cpu") -> WarpMeshes:
        if isinstance(filenames, str):
            filenames = [[filenames]]
        for i, file_list in enumerate(filenames):
            if isinstance(file_list, str):
                filenames[i] = [file_list]
            if not isinstance(filenames[i], list) or not all(isinstance(f, str) for f in filenames[i]):
                raise ValueError("All elements must be of type str.")
        verts, faces = [], []
        for file_list in filenames:
            v_list, f_list = [], []
            for file in file_list:
                mesh: Trimesh = trimesh.load(file, force="mesh", process=False)  # type: ignore
                v_list.append(mesh.vertices.view(np.ndarray))
                f_list.append(mesh.faces.view(np.ndarray))
            verts.append(v_list)
            faces.append(f_list)
        return WarpMeshes(verts, faces, device=device)

    @staticmethod
    def from_trimesh_meshes(meshes: Trimesh | list[Trimesh | list[Trimesh]], device: str = "cpu") -> WarpMeshes:
        if isinstance(meshes, Trimesh):
            meshes = [[meshes]]
        for i, m_list in enumerate(meshes):
            if isinstance(m_list, Trimesh):
                meshes[i] = [m_list]
            if not isinstance(meshes[i], list) or not all(isinstance(m, Trimesh) for m in meshes[i]):  # type: ignore
                raise ValueError("All elements must be of type Trimesh.")
        verts = [[m.vertices.view(np.ndarray) for m in m_list] for m_list in meshes]  # type: ignore
        faces = [[m.faces.view(np.ndarray) for m in m_list] for m_list in meshes]  # type: ignore
        return WarpMeshes(verts, faces, device=device)

    def query_signed_distances(
        self, query_points: Tensor, mesh_poses: Tensor | None = None, max_dist: float = 1e6
    ) -> Tuple[Tensor, Tensor, Tensor]:
        """Query signed distances.

        Args:
            query_points (Tensor): query points, shape (B, N, 3).
            mesh_poses (Tensor | None, optional): mesh poses, shape (B, M, 4, 4). Defaults to None.
            max_dist (float, optional): maximum distance. Defaults to 1e6.

        Returns:
            Tuple[Tensor, Tensor, Tensor]: differentiable signed distances (B, N), normals (B, N, 3), closest points (B, N, 3).
        """
        return self.query_signed_distances_v2(query_points, mesh_poses, max_dist)

    def query_signed_distances_v1(
        self, query_points: Tensor, mesh_poses: Tensor | None = None, max_dist: float = 1e6
    ) -> Tuple[Tensor, Tensor, Tensor]:
        inv_mesh_poses = inverse_tf_mat(mesh_poses) if mesh_poses is not None else None
        if query_points.device != self._mesh_ids.device:
            raise ValueError("Query points must be on the same device as WarpMeshes.")
        return QuerySignedDistances.apply(query_points, self._mesh_ids, inv_mesh_poses, max_dist)

    def query_signed_distances_v2(
        self, query_points: Tensor, mesh_poses: Tensor | None = None, max_dist: float = 1e6
    ) -> Tuple[Tensor, Tensor, Tensor]:
        if query_points.ndim != 3 or query_points.shape[2] != 3:
            msg = f"Invalid shape for query_points, expected (B, N, 3), got {query_points.shape}."
            raise ValueError(msg)

        with torch.no_grad():
            packed_query_points = query_points.detach().view(-1, 3).contiguous()  # (B * N, 3)
            packed_mesh_ids = self._mesh_ids.unsqueeze(1).expand(query_points.shape[:2] + (-1,))  # (B, N, M)
            packed_mesh_ids = packed_mesh_ids.reshape(packed_query_points.shape[0], -1).contiguous()  # (B * N, M)

            packed_signed_dists = torch.zeros_like(packed_query_points[:, 0])  # (B * N)
            packed_closest_points = torch.zeros_like(packed_query_points)  # (B * N, 3)
            packed_normals = torch.zeros_like(packed_query_points)  # (B * N, 3)

            if mesh_poses is None:
                wp.launch(
                    kernel=query_sdf_on_multiple_meshes_v2,
                    dim=packed_query_points.shape[0],
                    inputs=[
                        wp.from_torch(packed_query_points, dtype=wp.vec3),
                        wp.from_torch(packed_mesh_ids, dtype=wp.uint64),
                        max_dist,
                        wp.from_torch(packed_signed_dists, dtype=wp.float32),
                        wp.from_torch(packed_normals, dtype=wp.vec3),
                        wp.from_torch(packed_closest_points, dtype=wp.vec3),
                    ],
                    device=wp.device_from_torch(query_points.device),
                )
                with torch.enable_grad():
                    packed_diff_sdf = torch.sign(packed_signed_dists) * torch.norm(
                        packed_closest_points - query_points.view(-1, 3), p=2, dim=-1
                    )
            else:
                packed_local_closest_points = torch.zeros_like(packed_query_points)  # (B * N, 3)
                packed_closest_mesh_indices = torch.zeros_like(packed_query_points[:, 0], dtype=torch.long)  # (B * N)

                with torch.enable_grad():
                    inv_mesh_poses = inverse_tf_mat(mesh_poses)

                packed_inv_mesh_poses = repeat(
                    inv_mesh_poses.detach().contiguous(), "b ... -> (b n) ...", n=query_points.shape[1]
                )

                wp.launch(
                    kernel=query_sdf_on_multiple_posed_meshes_v2,
                    dim=packed_query_points.shape[0],
                    inputs=[
                        wp.from_torch(packed_query_points, dtype=wp.vec3),
                        wp.from_torch(packed_mesh_ids, dtype=wp.uint64),
                        wp.from_torch(packed_inv_mesh_poses, dtype=wp.mat44),
                        max_dist,
                        wp.from_torch(packed_signed_dists, dtype=wp.float32),
                        wp.from_torch(packed_normals, dtype=wp.vec3),
                        wp.from_torch(packed_closest_points, dtype=wp.vec3),
                        wp.from_torch(packed_local_closest_points, dtype=wp.vec3),
                        wp.from_torch(packed_closest_mesh_indices, dtype=wp.int64),
                    ],
                    device=wp.device_from_torch(query_points.device),
                )

                closest_mesh_indices = packed_closest_mesh_indices.view(query_points.shape[:2])

                with torch.enable_grad():
                    inv_closest_mesh_poses = torch.gather(
                        inv_mesh_poses,
                        dim=1,
                        index=closest_mesh_indices.unsqueeze(-1).unsqueeze(-1).expand(-1, -1, 4, 4),
                    )
                    local_query_points = transform_points(query_points.unsqueeze(-2), inv_closest_mesh_poses).squeeze(
                        -2
                    )
                    packed_diff_sdf = torch.sign(packed_signed_dists) * torch.norm(
                        local_query_points.view(-1, 3) - packed_local_closest_points, p=2, dim=-1
                    )

        wp.synchronize()
        return (
            packed_diff_sdf.view(query_points.shape[:2]),
            packed_normals.view(query_points.shape),
            packed_closest_points.view(query_points.shape),
        )

    @property
    def shape(self):
        return self._mesh_ids.shape

    def __repr__(self) -> str:
        return f"WarpMeshes(shape={self.shape})"

    def __str__(self) -> str:
        return self.__repr__()


__all__ = ["WarpMeshes"]

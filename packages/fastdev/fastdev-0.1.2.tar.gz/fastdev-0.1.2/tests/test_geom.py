import torch
import trimesh
from fastdev.geom.warp_meshes import WarpMeshes
from fastdev.xform.rotation import euler_angles_to_matrix
from fastdev.xform.transforms import rot_tl_to_tf_mat


def test_query_signed_distances():
    box = trimesh.creation.box((1.0, 1.0, 1.0))
    meshes = WarpMeshes.from_trimesh_meshes(box, device="cpu")
    query_pts = torch.tensor([[[1.0, 0.0, 0.0], [0.1, 0.0, 0.0]]])
    sdf, normals, pts = meshes.query_signed_distances(query_pts)
    assert torch.allclose(pts[0], torch.tensor([[0.5, 0.0, 0.0], [0.5, 0.0, 0.0]]))
    assert torch.allclose(normals[0], torch.tensor([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]))
    assert torch.allclose(sdf[0], torch.tensor([0.5, -0.4]))

    box1 = trimesh.creation.box((1.0, 1.0, 1.0))
    box2 = trimesh.creation.box((1.0, 1.0, 1.0))
    box2.apply_translation([1.3, 0.0, 0.0])
    meshes = WarpMeshes.from_trimesh_meshes([[box1, box2]], device="cpu")
    query_pts = torch.tensor([[[1.0, 0.0, 0.0], [0.6, 0.0, 0.0]]])
    sdf, normals, pts = meshes.query_signed_distances(query_pts)
    assert torch.allclose(pts[0], torch.tensor([[0.8, 0.0, 0.0], [0.5, 0.0, 0.0]]))
    assert torch.allclose(normals[0], torch.tensor([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]))
    assert torch.allclose(sdf[0], torch.tensor([-0.2, 0.1]))

    mesh_poses = torch.eye(4).unsqueeze(0).repeat(1, 2, 1, 1)
    mesh_poses[..., 0, 3] = 0.2
    sdf, normals, pts = meshes.query_signed_distances(query_pts, mesh_poses)
    assert torch.allclose(pts[0], torch.tensor([[1.0, 0.0, 0.0], [0.7, 0.0, 0.0]]))
    assert torch.allclose(normals[0], torch.tensor([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]))
    assert torch.allclose(sdf[0], torch.tensor([0.0, -0.1]))


def test_query_signed_distances_grad():
    device = "cpu"
    box = trimesh.creation.box((1, 1, 1))
    meshes = WarpMeshes.from_trimesh_meshes(box, device=device)
    pts = torch.tensor(
        [
            [0.0, 0.0, 0.0],
            [0.5, 0.5, 0.5],
            [1.0, 1.0, 1.0],
            [1.5, 1.5, 1.5],
        ],
        dtype=torch.float32,
        device=device,
        requires_grad=True,
    )
    sdf, normals, clse_pts = meshes.query_signed_distances(pts.unsqueeze(0))
    sdf.abs().sum().backward()
    assert torch.allclose(
        pts.grad,
        torch.tensor(
            [[-1.0000, 0.0000, 0.0000], [0.0000, 0.0000, 0.0000], [0.5774, 0.5774, 0.5774], [0.5774, 0.5774, 0.5774]],
            device=device,
        ),
        atol=1e-4,
    )

    pts.grad.zero_()
    pose = rot_tl_to_tf_mat(euler_angles_to_matrix(torch.tensor([0.1, 0.2, 0.3])), torch.tensor([-0.1, -0.1, -0.1]))
    pose.requires_grad_(True)
    sdf, normals, clse_pts = meshes.query_signed_distances(pts.unsqueeze(0), pose.unsqueeze(0).unsqueeze(0))
    sdf.sum().backward()
    assert torch.allclose(
        pts.grad,
        torch.tensor(
            [[0.2184, -0.0370, 0.9752], [0.6689, 0.1173, 0.7340], [0.6237, 0.4680, 0.6261], [0.6041, 0.5183, 0.6054]],
            device=device,
        ),
        atol=1e-4,
    )
    assert torch.allclose(
        pose.grad,
        torch.tensor(
            [
                [1.9159, 0.9930, 2.5419, -2.1150],
                [1.9159, 0.9930, 2.5419, -1.0666],
                [1.9159, 0.9930, 2.5419, -2.9407],
                [0.0000, 0.0000, 0.0000, 0.0000],
            ],
            device=device,
        ),
        atol=1e-4,
    )

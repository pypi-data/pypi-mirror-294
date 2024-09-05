# mypy: disable-error-code="valid-type"
import warp as wp


# left here for reference
@wp.kernel
def query_sdf_on_mesh(
    points: wp.array(dtype=wp.vec3),
    mesh_ids: wp.array(dtype=wp.uint64),
    max_dist: float,
    closest_points: wp.array(dtype=wp.vec3),
    normals: wp.array(dtype=wp.vec3),
    signed_dists: wp.array(dtype=wp.float32),
):
    tid = wp.tid()
    point = points[tid]
    mesh_id = mesh_ids[tid]

    query = wp.mesh_query_point(mesh_id, point, max_dist)

    if query.result:
        closest_point = wp.mesh_eval_position(mesh_id, query.face, query.u, query.v)
        normal = wp.mesh_eval_face_normal(mesh_id, query.face)
        dist = wp.length(closest_point - point) * query.sign

        closest_points[tid] = closest_point
        normals[tid] = normal
        signed_dists[tid] = dist
    else:
        signed_dists[tid] = max_dist


@wp.kernel
def query_sdf_on_multiple_meshes(
    points: wp.array(dtype=wp.vec3),
    mesh_ids: wp.array2d(dtype=wp.uint64),
    max_dist: float,
    points_requires_grad: bool,
    signed_dists: wp.array(dtype=wp.float32),
    normals: wp.array(dtype=wp.vec3),
    closest_points: wp.array(dtype=wp.vec3),
    points_jacob: wp.array(dtype=wp.vec3),
):
    tid = wp.tid()
    point = points[tid]
    mesh_id = mesh_ids[tid]

    min_dist = max_dist

    for mesh_idx in range(mesh_id.shape[0]):
        query = wp.mesh_query_point(mesh_id[mesh_idx], point, max_dist)

        if query.result:
            closest_point = wp.mesh_eval_position(mesh_id[mesh_idx], query.face, query.u, query.v)
            dist = wp.length(closest_point - point) * query.sign

            if dist < min_dist:
                min_dist = dist
                normal = wp.mesh_eval_face_normal(mesh_id[mesh_idx], query.face)
                signed_dists[tid] = dist
                normals[tid] = normal
                closest_points[tid] = closest_point

    if points_requires_grad and min_dist < max_dist:
        sign = float(signed_dists[tid] > 0.0) * 2.0 - 1.0
        points_jacob[tid] = wp.normalize(point - closest_points[tid]) * sign


@wp.func
def get_rotation_matrix(tf_mat: wp.mat44) -> wp.mat33:
    # fmt: off
    return wp.mat33(
        tf_mat[0, 0], tf_mat[0, 1], tf_mat[0, 2],
        tf_mat[1, 0], tf_mat[1, 1], tf_mat[1, 2],
        tf_mat[2, 0], tf_mat[2, 1], tf_mat[2, 2]
    )
    # fmt: on


@wp.kernel
def query_sdf_on_multiple_posed_meshes(
    points: wp.array(dtype=wp.vec3),
    mesh_ids: wp.array2d(dtype=wp.uint64),
    inv_mesh_poses: wp.array2d(dtype=wp.mat44),
    max_dist: float,
    points_requires_grad: bool,
    inv_mesh_poses_requires_grad: bool,
    signed_dists: wp.array(dtype=wp.float32),
    normals: wp.array(dtype=wp.vec3),
    closest_points: wp.array(dtype=wp.vec3),
    points_jacob: wp.array(dtype=wp.vec3),
    inv_mesh_poses_jacob: wp.array2d(dtype=wp.mat44),
):
    tid = wp.tid()
    point = points[tid]
    m_ids = mesh_ids[tid]
    inv_m_poses = inv_mesh_poses[tid]

    min_dist = max_dist
    min_mesh_idx = -1

    for mesh_idx in range(m_ids.shape[0]):
        local_point = wp.transform_point(inv_m_poses[mesh_idx], point)
        query = wp.mesh_query_point(m_ids[mesh_idx], local_point, max_dist)

        if query.result:
            local_closest_point = wp.mesh_eval_position(m_ids[mesh_idx], query.face, query.u, query.v)
            dist = wp.length(local_closest_point - local_point) * query.sign

            if dist < min_dist:
                m_pose = wp.inverse(inv_m_poses[mesh_idx])

                min_dist = dist
                min_mesh_idx = mesh_idx
                local_normal = wp.mesh_eval_face_normal(m_ids[mesh_idx], query.face)

                closest_point = wp.transform_point(m_pose, local_closest_point)
                normal = wp.mul(get_rotation_matrix(m_pose), local_normal)

                signed_dists[tid] = dist
                normals[tid] = normal
                closest_points[tid] = closest_point

    if points_requires_grad and min_mesh_idx >= 0:
        sign = float(signed_dists[tid] > 0.0) * 2.0 - 1.0
        points_jacob[tid] = wp.normalize(point - closest_points[tid]) * sign

    if inv_mesh_poses_requires_grad and min_mesh_idx >= 0:
        sign = float(signed_dists[tid] > 0.0) * 2.0 - 1.0
        local_point = wp.transform_point(inv_m_poses[min_mesh_idx], point)
        local_closest_point = wp.transform_point(inv_m_poses[min_mesh_idx], closest_points[tid])

        local_pt_jacob = wp.normalize(local_point - local_closest_point) * sign
        rot_jacob = wp.outer(local_pt_jacob, point)

        # fmt: off
        inv_mesh_poses_jacob[tid, min_mesh_idx] = wp.mat44(
            rot_jacob[0, 0], rot_jacob[0, 1], rot_jacob[0, 2], local_pt_jacob[0],
            rot_jacob[1, 0], rot_jacob[1, 1], rot_jacob[1, 2], local_pt_jacob[1],
            rot_jacob[2, 0], rot_jacob[2, 1], rot_jacob[2, 2], local_pt_jacob[2],
            0.0, 0.0, 0.0, 0.0
        )
        # fmt: on


@wp.kernel
def query_sdf_on_multiple_meshes_v2(
    points: wp.array(dtype=wp.vec3),
    mesh_ids: wp.array2d(dtype=wp.uint64),
    max_dist: float,
    signed_dists: wp.array(dtype=wp.float32),
    normals: wp.array(dtype=wp.vec3),
    closest_points: wp.array(dtype=wp.vec3),
):
    tid = wp.tid()
    point = points[tid]
    m_ids = mesh_ids[tid]

    min_dist = max_dist

    for mesh_idx in range(m_ids.shape[0]):
        if m_ids[mesh_idx] == 0:  # skip invalid mesh
            continue
        query = wp.mesh_query_point(m_ids[mesh_idx], point, max_dist)

        if query.result:
            closest_point = wp.mesh_eval_position(m_ids[mesh_idx], query.face, query.u, query.v)
            dist = wp.length(closest_point - point) * query.sign

            if dist < min_dist:
                min_dist = dist
                normal = wp.mesh_eval_face_normal(m_ids[mesh_idx], query.face)
                signed_dists[tid] = dist
                normals[tid] = normal
                closest_points[tid] = closest_point


@wp.kernel
def query_sdf_on_multiple_posed_meshes_v2(
    points: wp.array(dtype=wp.vec3),
    mesh_ids: wp.array2d(dtype=wp.uint64),
    inv_mesh_poses: wp.array2d(dtype=wp.mat44),
    max_dist: float,
    signed_dists: wp.array(dtype=wp.float32),
    normals: wp.array(dtype=wp.vec3),
    closest_points: wp.array(dtype=wp.vec3),
    local_closest_points: wp.array(dtype=wp.vec3),
    closest_mesh_indices: wp.array(dtype=wp.int64),
):
    tid = wp.tid()
    point = points[tid]
    m_ids = mesh_ids[tid]
    inv_m_poses = inv_mesh_poses[tid]

    min_dist = max_dist

    for mesh_idx in range(m_ids.shape[0]):
        if m_ids[mesh_idx] == 0:  # skip invalid mesh
            continue
        local_point = wp.transform_point(inv_m_poses[mesh_idx], point)
        query = wp.mesh_query_point(m_ids[mesh_idx], local_point, max_dist)

        if query.result:
            local_closest_point = wp.mesh_eval_position(m_ids[mesh_idx], query.face, query.u, query.v)
            dist = wp.length(local_closest_point - local_point) * query.sign

            if dist < min_dist:
                m_pose = wp.inverse(inv_m_poses[mesh_idx])

                min_dist = dist
                local_normal = wp.mesh_eval_face_normal(m_ids[mesh_idx], query.face)

                closest_point = wp.transform_point(m_pose, local_closest_point)
                normal = wp.mul(get_rotation_matrix(m_pose), local_normal)

                signed_dists[tid] = dist
                normals[tid] = normal
                closest_points[tid] = closest_point
                local_closest_points[tid] = local_closest_point
                closest_mesh_indices[tid] = wp.int64(mesh_idx)

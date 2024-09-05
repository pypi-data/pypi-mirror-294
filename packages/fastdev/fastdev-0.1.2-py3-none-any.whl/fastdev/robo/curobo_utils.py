from typing import Tuple

import torch
from curobo.cuda_robot_model.cuda_robot_model import CudaRobotModel
from curobo.curobolib.kinematics import KinematicsFusedFunction
from torch import Tensor


class CustomKinematicsFusedFunction(KinematicsFusedFunction):
    @staticmethod
    def backward(ctx, grad_out_link_pos, grad_out_link_quat, grad_out_spheres):
        return KinematicsFusedFunction.backward(
            ctx,
            grad_out_link_pos.contiguous(),
            grad_out_link_quat.contiguous(),
            grad_out_spheres,
        )


def custom_get_cuda_kinematics(
    link_pos_seq,
    link_quat_seq,
    batch_robot_spheres,
    global_cumul_mat,
    q_in,
    fixed_transform,
    link_spheres_tensor,
    link_map,  # tells which link is attached to which link i
    joint_map,  # tells which joint is attached to a link i
    joint_map_type,  # joint type
    store_link_map,
    link_sphere_idx_map,  # sphere idx map
    link_chain_map,
    joint_offset_map,
    grad_out_q,
    use_global_cumul: bool = True,
):
    # if not q_in.is_contiguous():
    #    q_in = q_in.contiguous()
    link_pos, link_quat, robot_spheres = CustomKinematicsFusedFunction.apply(  # type: ignore
        link_pos_seq,
        link_quat_seq,
        batch_robot_spheres,
        global_cumul_mat,
        q_in,
        fixed_transform,
        link_spheres_tensor,
        link_map,  # tells which link is attached to which link i
        joint_map,  # tells which joint is attached to a link i
        joint_map_type,  # joint type
        store_link_map,
        link_sphere_idx_map,  # sphere idx map
        link_chain_map,
        joint_offset_map,
        grad_out_q,
        use_global_cumul,
    )
    return link_pos, link_quat, robot_spheres


class CustomCudaRobotModel(CudaRobotModel):
    def _cuda_forward(self, q: torch.Tensor) -> Tuple[Tensor, Tensor, Tensor]:
        link_pos, link_quat, robot_spheres = custom_get_cuda_kinematics(
            self._link_pos_seq,
            self._link_quat_seq,
            self._batch_robot_spheres,
            self._global_cumul_mat,
            q,
            self.kinematics_config.fixed_transforms,
            self.kinematics_config.link_spheres,
            self.kinematics_config.link_map,  # tells which link is attached to which link i
            self.kinematics_config.joint_map,  # tells which joint is attached to a link i
            self.kinematics_config.joint_map_type,  # joint type
            self.kinematics_config.store_link_map,
            self.kinematics_config.link_sphere_idx_map,  # sphere idx map
            self.kinematics_config.link_chain_map,
            self.kinematics_config.joint_offset_map,
            self._grad_out_q,
            self.use_global_cumul,
        )
        return link_pos, link_quat, robot_spheres

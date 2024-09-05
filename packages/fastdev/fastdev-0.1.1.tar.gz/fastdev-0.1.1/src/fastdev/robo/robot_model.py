# mypy: disable-error-code="empty-body"
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, List, Literal, Optional, cast, overload

import numpy as np
import torch
import trimesh
import yourdfpy
from jaxtyping import Float
from lxml import etree
from torch import Tensor
from torch.types import Device
from trimesh.util import concatenate

from fastdev.utils.dispatch import singledispatch
from fastdev.xform.rotation import quaternion_to_matrix
from fastdev.xform.transforms import rot_tl_to_tf_mat

ROOT_JOINT_NAME = "__root__"


class Geometry(ABC):
    @abstractmethod
    def get_trimesh_mesh(self) -> trimesh.Trimesh: ...


@dataclass
class Box(Geometry):
    size: list[float]

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.box(self.size)


@dataclass
class Cylinder(Geometry):
    radius: float
    length: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.cylinder(radius=self.radius, height=self.length)


@dataclass
class Capsule(Geometry):
    radius: float
    length: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.capsule(radius=self.radius, height=self.length)


@dataclass
class Sphere(Geometry):
    radius: float

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        return trimesh.creation.icosphere(subdivisions=3, radius=self.radius)


@dataclass
class Mesh(Geometry):
    scale: list[float]

    filename: str | None = None  # usually relative path
    mesh_dir: str | None = None  # usually urdf/mjcf file directory
    is_collision_geometry: bool = False

    vertices: np.ndarray | None = None  # un-scaled vertices
    faces: np.ndarray | None = None

    _scaled_trimesh_mesh: trimesh.Trimesh | None = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        if self._scaled_trimesh_mesh is not None:
            return self._scaled_trimesh_mesh

        if self.vertices is not None and self.faces is not None:
            self._scaled_trimesh_mesh = trimesh.Trimesh(self.vertices * np.asarray(self.scale), self.faces)
        else:
            if self.filename is None:
                raise ValueError("Either filename or vertices and faces must be provided")
            if self.mesh_dir is not None:
                mesh_path = os.path.join(self.mesh_dir, self.filename)
            else:
                mesh_path = self.filename
            mesh: trimesh.Trimesh = trimesh.load(mesh_path, force="mesh", skip_materials=self.is_collision_geometry)  # type: ignore
            mesh.apply_scale(self.scale)
            self._scaled_trimesh_mesh = mesh

        return self._scaled_trimesh_mesh


@dataclass
class Material:
    name: str | None = None
    color: np.ndarray | None = None
    texture: str | None = None


@dataclass
class Visual:
    origin: np.ndarray
    geometry: Geometry
    name: str | None = None
    material: Material | None = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        mesh = self.geometry.get_trimesh_mesh()
        return mesh.apply_transform(self.origin)


@dataclass
class Collision:
    origin: np.ndarray
    geometry: Geometry
    name: str | None = None

    def get_trimesh_mesh(self) -> trimesh.Trimesh:
        mesh = self.geometry.get_trimesh_mesh()
        return mesh.apply_transform(self.origin)


class JointType(Enum):
    ROOT = -1  # used for base link, which has no parent joint
    FIXED = 0
    PRISMATIC = 1
    REVOLUTE = 2  # aka. rotational


@dataclass(frozen=True)
class Joint:
    name: str
    type: JointType
    origin: np.ndarray
    axis: np.ndarray
    limit: np.ndarray | None

    parent_link_name: str
    child_link_name: str

    mimic_joint: str | None = None
    mimic_multiplier: float | None = None
    mimic_offset: float | None = None


@dataclass(frozen=True)
class Link:
    name: str
    visuals: list[Visual] = field(default_factory=list)
    collisions: list[Collision] = field(default_factory=list)

    joint_name: str = field(init=False)  # parent joint name in urdf

    def set_joint_name(self, joint_name: str):
        object.__setattr__(self, "joint_name", joint_name)

    def get_trimesh_mesh(self, mode: Literal["visual", "collision"] = "collision") -> trimesh.Trimesh:
        if mode == "visual":
            meshes = [visual.get_trimesh_mesh() for visual in self.visuals]
        elif mode == "collision":
            meshes = [collision.get_trimesh_mesh() for collision in self.collisions]
        else:
            raise ValueError(f"Unknown mode: {mode}")
        return concatenate(meshes)  # type: ignore


def _build_joint_transform(joint: Joint, joint_value: Tensor | None = None) -> Tensor:
    if joint.type == JointType.REVOLUTE:
        if joint_value is None:
            raise ValueError("Joint value must be provided for revolute joint.")
        c = torch.cos(joint_value)
        s = torch.sin(joint_value)
        t = 1 - c
        x, y, z = joint.axis
        # fmt: off
        rot_mat = torch.stack(
            [
                t * x * x + c, t * x * y - s * z, t * x * z + s * y,
                t * x * y + s * z, t * y * y + c, t * y * z - s * x,
                t * x * z - s * y, t * y * z + s * x, t * z * z + c,
            ],
            dim=-1,
        ).reshape(-1, 3, 3)
        # fmt: on
        tf_mat = torch.eye(4, device=rot_mat.device, dtype=rot_mat.dtype).repeat(rot_mat.shape[:-2] + (1, 1))
        tf_mat[..., :3, :3] = rot_mat
        return tf_mat
    elif joint.type == JointType.PRISMATIC:
        if joint_value is None:
            raise ValueError("Joint value must be provided for revolute joint.")
        x, y, z = joint.axis
        tl = torch.stack([x * joint_value, y * joint_value, z * joint_value], dim=-1).reshape(-1, 3)
        tf_mat = torch.eye(4, device=tl.device, dtype=tl.dtype).repeat(tl.shape[:-1] + (1, 1))
        tf_mat[..., :3, -1] = tl
        return tf_mat
    elif joint.type == JointType.FIXED:
        return torch.eye(4, dtype=torch.float32)
    else:
        raise NotImplementedError(f"Joint type {joint.type} is not supported.")


def _build_joint_transform_np(joint: Joint, joint_value: np.ndarray | None = None) -> np.ndarray:
    if joint.type == JointType.REVOLUTE:
        if joint_value is None:
            raise ValueError("Joint value must be provided for revolute joint.")
        c = np.cos(joint_value)
        s = np.sin(joint_value)
        t = 1 - c
        x, y, z = joint.axis
        # fmt: off
        rot_mat = np.stack(
            [
                t * x * x + c, t * x * y - s * z, t * x * z + s * y,
                t * x * y + s * z, t * y * y + c, t * y * z - s * x,
                t * x * z - s * y, t * y * z + s * x, t * z * z + c,
            ],
            axis=-1,
        ).reshape(-1, 3, 3)
        # fmt: on
        tf_mat = np.tile(np.eye(4, dtype=rot_mat.dtype), (rot_mat.shape[:-2] + (1, 1)))
        tf_mat[..., :3, :3] = rot_mat
        return tf_mat
    elif joint.type == JointType.PRISMATIC:
        if joint_value is None:
            raise ValueError("Joint value must be provided for revolute joint.")
        x, y, z = joint.axis
        tl = np.stack([x * joint_value, y * joint_value, z * joint_value], axis=-1).reshape(-1, 3)
        tf_mat = np.tile(np.eye(4, dtype=tl.dtype), (tl.shape[:-1] + (1, 1)))
        tf_mat[..., :3, -1] = tl
        return tf_mat
    elif joint.type == JointType.FIXED:
        return np.eye(4, dtype=np.float32)
    else:
        raise NotImplementedError(f"Joint type {joint.type} is not supported.")


@dataclass
class RobotModelConfig:
    """Robot model configuration."""

    urdf_or_mjcf_path: str | Path
    mesh_dir: str | None = None
    format: Literal["urdf", "mjcf"] | None = None  # will be inferred if not provided

    device: Device = "cpu"

    mjcf_assets: dict[str, Any] | None = None

    ee_link_names: list[str] | None = None  # will be inferred if not provided
    enable_mimic_joints: bool = True  # if False, mimic joints will be considered as active joints, only for URDF

    def __post_init__(self):
        if isinstance(self.urdf_or_mjcf_path, Path):
            self.urdf_or_mjcf_path = str(self.urdf_or_mjcf_path)
        if not os.path.exists(self.urdf_or_mjcf_path):
            raise FileNotFoundError(f"URDF/MJCF file not found: {self.urdf_or_mjcf_path}")
        if self.format is None:
            if self.urdf_or_mjcf_path.endswith(".urdf"):
                self.format = "urdf"
            elif self.urdf_or_mjcf_path.endswith(".xml"):
                self.format = "mjcf"
            else:
                raise ValueError("Unknown file format, please provide `format` explicitly.")


class RobotModel:
    """Robot model.

    Args:
        config (RobotModelConfig): Robot model configuration.

    Examples:
        >>> robot_model = RobotModel(RobotModelConfig(urdf_or_mjcf_path="assets/robot_description/panda.urdf", device="cpu"))
        >>> robot_model.num_dofs
        8
        >>> link_poses = robot_model.forward_kinematics(torch.zeros(1, robot_model.num_dofs))
        >>> torch.allclose(link_poses[0, -1, :3, 3], torch.tensor([0.10323, 0, 0.86668]), atol=1e-3)
        True
    """

    def __init__(self, config: RobotModelConfig) -> None:
        self.config = config

        if config.format == "urdf":
            self.joint_map, self.link_map = self.parse_urdf()
        elif config.format == "mjcf":
            self.joint_map, self.link_map = self.parse_mjcf()
        else:
            raise ValueError(f"Unknown file format: {config.format}")

        # infer active joint names
        self.active_joint_names: list[str] = [
            joint_name
            for joint_name, joint in self.joint_map.items()
            if joint.type not in [JointType.FIXED, JointType.ROOT]
        ]
        # filter out mimic joints
        if self.config.enable_mimic_joints:
            self.active_joint_names = [
                joint_name for joint_name in self.active_joint_names if self.joint_map[joint_name].mimic_joint is None
            ]

        # infer number of DOFs
        self.num_dofs = len(self.active_joint_names)

        # set base link name
        self.link_names: list[str] = list(self.link_map.keys())
        self.base_link_name = self.joint_map[ROOT_JOINT_NAME].child_link_name
        # infer ee link names if not provided
        if isinstance(self.config.ee_link_names, list):
            pass
        if isinstance(self.config.ee_link_names, str):
            self.config.ee_link_names = [self.config.ee_link_names]
        elif self.config.ee_link_names is None:
            _link_names = list(self.link_map.keys())
            for joint in self.joint_map.values():
                if joint.parent_link_name in _link_names:
                    _link_names.remove(joint.parent_link_name)
            if len(_link_names) == 0:
                raise ValueError("Could not determine end effector link.")
            self.config.ee_link_names = _link_names
        self.ee_link_names = self.config.ee_link_names
        # sort all links in topological order
        cur_links = [self.base_link_name]
        topological_order = []
        while cur_links:
            next_links = []
            for link_name in cur_links:
                topological_order.append(link_name)
                for joint in self.joint_map.values():
                    if joint.parent_link_name == link_name:
                        next_links.append(joint.child_link_name)
            cur_links = next_links
        self.link_names_topological_order = topological_order

        # collect joint limits
        joint_limits = []
        if len(self.active_joint_names) == 0:
            self.joint_limits = None
        elif self.joint_map[self.active_joint_names[0]].limit is None:
            self.joint_limits = None
        else:
            for joint_name in self.active_joint_names:
                joint = self.joint_map[joint_name]
                if joint.limit is None:
                    raise ValueError(f"Joint {joint_name} has no limit")
                joint_limits.append(joint.limit)
            self.joint_limits = np.stack(joint_limits, axis=0)

    @staticmethod
    def from_urdf_or_mjcf_path(
        urdf_or_mjcf_path: str | Path, mesh_dir: str | None = None, device: Device = "cpu"
    ) -> RobotModel:
        return RobotModel(RobotModelConfig(urdf_or_mjcf_path=urdf_or_mjcf_path, mesh_dir=mesh_dir, device=device))

    def parse_urdf(self) -> tuple[dict[str, Joint], dict[str, Link]]:
        def urdf_str_to_joint_type(joint_type_str: str) -> JointType:
            if joint_type_str == "fixed":
                return JointType.FIXED
            elif joint_type_str == "prismatic":
                return JointType.PRISMATIC
            elif joint_type_str == "revolute":
                return JointType.REVOLUTE
            else:
                raise ValueError(f"Unknown joint type: {joint_type_str}")

        def build_joint_from_urdf(joint_spec: yourdfpy.urdf.Joint) -> Joint:
            joint_type = urdf_str_to_joint_type(joint_spec.type)
            if (
                joint_spec.limit is not None
                and joint_spec.limit.lower is not None
                and joint_spec.limit.upper is not None
            ):
                limit = np.array([joint_spec.limit.lower, joint_spec.limit.upper], dtype=np.float32)
            else:
                limit = None
            origin = joint_spec.origin if joint_spec.origin is not None else np.eye(4, dtype=np.float32)
            return Joint(
                name=joint_spec.name,
                type=joint_type,
                origin=origin.astype(np.float32),
                axis=joint_spec.axis.astype(np.float32),
                limit=limit,
                parent_link_name=joint_spec.parent,
                child_link_name=joint_spec.child,
                mimic_joint=None if joint_spec.mimic is None else joint_spec.mimic.joint,
                mimic_multiplier=None if joint_spec.mimic is None else joint_spec.mimic.multiplier,
                mimic_offset=None if joint_spec.mimic is None else joint_spec.mimic.offset,
            )

        def build_geometry_from_urdf(
            urdf_geometry: yourdfpy.urdf.Geometry, mesh_dir: str, use_collision_geometry: bool = False
        ) -> Geometry:
            if urdf_geometry.box is not None:
                return Box(size=urdf_geometry.box.size.tolist())
            elif urdf_geometry.cylinder is not None:
                return Cylinder(radius=urdf_geometry.cylinder.radius, length=urdf_geometry.cylinder.length)
            elif urdf_geometry.sphere is not None:
                return Sphere(radius=urdf_geometry.sphere.radius)
            elif urdf_geometry.mesh is not None:
                scale_spec = urdf_geometry.mesh.scale
                if isinstance(scale_spec, float):
                    scale: list[float] = [scale_spec, scale_spec, scale_spec]
                elif isinstance(scale_spec, np.ndarray):
                    scale = scale_spec.tolist()
                elif scale_spec is None:
                    scale = [1.0, 1.0, 1.0]
                else:
                    raise ValueError(f"Unknown scale type: {scale_spec}")
                return Mesh(
                    filename=urdf_geometry.mesh.filename,
                    mesh_dir=mesh_dir,
                    scale=scale,
                    is_collision_geometry=use_collision_geometry,
                )
            else:
                raise ValueError(f"Unknown geometry type: {urdf_geometry}")

        def build_material_from_urdf(urdf_material: yourdfpy.urdf.Material) -> Material:
            return Material(
                name=urdf_material.name,
                color=urdf_material.color.rgba if urdf_material.color is not None else None,
                texture=urdf_material.texture.filename if urdf_material.texture is not None else None,
            )

        def build_link_from_urdf(link_spec: yourdfpy.urdf.Link, mesh_dir: str) -> Link:
            link = Link(name=link_spec.name)
            for visual_spec in link_spec.visuals:
                assert visual_spec.geometry is not None, f"Visual {visual_spec.name} has no geometry"
                if visual_spec.origin is None:
                    origin = np.eye(4, dtype=np.float32)
                else:
                    origin = visual_spec.origin
                visual = Visual(
                    origin=origin,
                    geometry=build_geometry_from_urdf(
                        visual_spec.geometry, mesh_dir=mesh_dir, use_collision_geometry=False
                    ),
                    name=visual_spec.name,
                    material=build_material_from_urdf(visual_spec.material)
                    if visual_spec.material is not None
                    else None,
                )
                link.visuals.append(visual)
            for collision_spec in link_spec.collisions:
                if collision_spec.origin is None:
                    origin = np.eye(4, dtype=np.float32)
                else:
                    origin = collision_spec.origin
                collision = Collision(
                    origin=origin,
                    geometry=build_geometry_from_urdf(
                        collision_spec.geometry, mesh_dir=mesh_dir, use_collision_geometry=True
                    ),
                    name=collision_spec.name,
                )
                link.collisions.append(collision)
            return link

        if self.config.mesh_dir is None:
            self.config.mesh_dir = os.path.abspath(os.path.dirname(self.config.urdf_or_mjcf_path))

        # parse URDF
        urdf = yourdfpy.URDF.load(
            self.config.urdf_or_mjcf_path,
            load_meshes=False,
            build_scene_graph=False,
            mesh_dir=self.config.mesh_dir,
            filename_handler=yourdfpy.filename_handler_null,
        )

        # build joint maps
        joint_map: dict[str, Joint] = {
            joint_name: build_joint_from_urdf(joint_spec) for joint_name, joint_spec in urdf.joint_map.items()
        }
        # infer base link name
        link_names: list[str] = list(urdf.link_map.keys())
        for joint in joint_map.values():
            if joint.child_link_name in link_names:
                link_names.remove(joint.child_link_name)
        if len(link_names) != 1:
            raise ValueError(f"Expected exactly one base link, got {len(link_names)}")
        base_link_name = link_names[0]
        # add a root joint for base link
        joint_map[ROOT_JOINT_NAME] = Joint(
            name=ROOT_JOINT_NAME,
            type=JointType.ROOT,
            origin=np.eye(4, dtype=np.float32),
            axis=np.zeros(3, dtype=np.float32),
            limit=np.array([0.0, 0.0], dtype=np.float32),
            parent_link_name="",
            child_link_name=base_link_name,
        )

        # build link maps
        link_map = {
            link_name: build_link_from_urdf(link_spec, mesh_dir=self.config.mesh_dir)
            for link_name, link_spec in urdf.link_map.items()
        }
        # set parent joint names for links
        for joint_name, joint in joint_map.items():
            link_map[joint.child_link_name].set_joint_name(joint_name)

        return joint_map, link_map

    def parse_mjcf(self) -> tuple[dict[str, Joint], dict[str, Link]]:
        def is_collision_geometry(geom_spec) -> bool | None:
            if geom_spec.contype is None or geom_spec.conaffinity is None:
                return None
            return geom_spec.contype ^ geom_spec.conaffinity

        def build_geometry_from_mjcf(geom_spec, use_collision_geometry: bool = True) -> Geometry:
            if geom_spec.type == "box":
                return Box(size=geom_spec.size * 2)
            elif geom_spec.type == "cylinder":
                raise NotImplementedError("Cylinder geometry is not supported in MJCF")
            elif geom_spec.type == "mesh" or geom_spec.mesh is not None:
                scale_spec = geom_spec.mesh.scale
                if isinstance(scale_spec, float):
                    scale: list[float] = [scale_spec, scale_spec, scale_spec]
                elif isinstance(scale_spec, np.ndarray):
                    scale = scale_spec.tolist()
                elif scale_spec is None:
                    scale = [1.0, 1.0, 1.0]
                else:
                    raise ValueError(f"Unknown scale type: {scale_spec}")
                mesh: trimesh.Trimesh = trimesh.load(  # type: ignore
                    trimesh.util.wrap_as_stream(geom_spec.mesh.file.contents),
                    file_type=geom_spec.mesh.file.extension.replace(".", ""),
                    force="mesh",
                    skip_materials=use_collision_geometry,
                )
                mesh.apply_scale(scale)
                return Mesh(scale=scale, _scaled_trimesh_mesh=mesh, is_collision_geometry=use_collision_geometry)
            elif geom_spec.type == "capsule":
                return Capsule(radius=geom_spec.size[0], length=geom_spec.size[1] * 2)
            elif geom_spec.type == "sphere" or geom_spec.type is None:
                return Sphere(radius=geom_spec.size)
            else:
                raise ValueError(f"Unknown geometry type: {geom_spec.type}")

        def build_pose_from_mjcf(quat: np.ndarray | None, pos: np.ndarray | None) -> np.ndarray:
            rot_mat = quaternion_to_matrix(quat) if quat is not None else np.eye(3)
            return rot_tl_to_tf_mat(rot_mat=rot_mat, tl=pos)

        def build_link_from_mjcf(link_spec) -> Link:
            link = Link(name=link_spec.name)
            for geom in link_spec.geom:
                origin = build_pose_from_mjcf(geom.quat, geom.pos)
                is_collision = is_collision_geometry(geom)
                if is_collision is None or is_collision:
                    collision = Collision(
                        origin=origin,
                        geometry=build_geometry_from_mjcf(geom, use_collision_geometry=True),
                        name=geom.name,
                    )
                    link.collisions.append(collision)
                elif is_collision is None or not is_collision:
                    visual = Visual(origin=origin, geometry=build_geometry_from_mjcf(geom), name=geom.name)
                    link.visuals.append(visual)
            return link

        def mjcf_str_to_joint_type(joint_type_str: str | None = "hinge") -> JointType:
            # https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-joint
            if joint_type_str == "fixed":
                return JointType.FIXED
            elif joint_type_str == "slide":
                return JointType.PRISMATIC
            elif joint_type_str == "hinge" or joint_type_str is None:
                return JointType.REVOLUTE
            else:
                raise ValueError(f"Unknown joint type: {joint_type_str}")

        def build_joint_from_mjcf(joint_spec, origin: np.ndarray, parent_link_name: str, child_link_name: str) -> Joint:
            joint_type = mjcf_str_to_joint_type(joint_spec.type)
            if joint_spec.range is not None:
                limit = np.asarray(joint_spec.range, dtype=np.float32)
            else:
                limit = None
            if joint_spec.axis is None:
                axis = np.asarray([0.0, 0.0, 1.0], dtype=np.float32)
            else:
                axis = np.asarray(joint_spec.axis, dtype=np.float32)
            return Joint(
                name=joint_spec.name,
                type=joint_type,
                origin=np.asarray(origin, dtype=np.float32),
                axis=axis,
                limit=limit,
                parent_link_name=parent_link_name,
                child_link_name=child_link_name,
            )

        try:
            from absl import flags

            for name in list(flags.FLAGS):
                if "pymjcf" in name:
                    delattr(flags.FLAGS, name)

            import dm_control.mjcf
        except ImportError:
            raise ImportError("dm_control is required to parse MJCF files, please install by `pip install dm_control`")

        if self.config.mesh_dir is None:
            self.config.mesh_dir = os.path.dirname(self.config.urdf_or_mjcf_path)

        # The mjcf file by IsaacGym does not follow the convention of mujoco mjcf precisely
        # We need to handle it separately when the mjcf file is not valid by normal mjcf parser
        try:
            with open(self.config.urdf_or_mjcf_path, "r") as f:
                mjcf = dm_control.mjcf.from_file(f, assets=self.config.mjcf_assets, model_dir=self.config.mesh_dir)
        except KeyError:
            file_root = os.path.dirname(self.config.urdf_or_mjcf_path)
            tree = etree.parse(self.config.urdf_or_mjcf_path)  # type: ignore
            root = tree.getroot()
            invalid_includes = root.findall("*/include")
            for include in invalid_includes:
                parent = include.getparent()
                file: str = include.get("file")
                child_xml = etree.parse(os.path.join(file_root, file)).getroot().getchildren()  # type: ignore
                parent.remove(include)
                parent.extend(child_xml)

            xml_string = etree.tostring(tree)
            mjcf = dm_control.mjcf.from_xml_string(xml_string, model_dir=self.config.mesh_dir)

        # Substitute geom with default values
        for geom in mjcf.find_all("geom"):
            dm_control.mjcf.commit_defaults(geom)

        base_link_spec = mjcf.worldbody.body[0]  # type: ignore
        base_link_name = str(base_link_spec.name)

        link_map: dict[str, Link] = {}
        joint_map: dict[str, Joint] = {}
        link_specs = [(base_link_spec, "")]
        while link_specs:
            link_spec, parent_link_name = link_specs.pop()
            link_map[link_spec.name] = build_link_from_mjcf(link_spec)
            if len(link_spec.joint) > 0:
                if len(link_spec.joint) > 1:
                    raise ValueError(f"Link {link_spec.name} has multiple joints")
                joint_map[link_spec.joint[0].name] = build_joint_from_mjcf(
                    link_spec.joint[0],
                    origin=build_pose_from_mjcf(link_spec.quat, link_spec.pos),
                    parent_link_name=parent_link_name,
                    child_link_name=link_spec.name,
                )
                link_map[link_spec.name].set_joint_name(link_spec.joint[0].name)
            else:
                fixed_joint = Joint(
                    name=f"{link_spec.name}_fixed",
                    type=JointType.FIXED,
                    origin=np.eye(4, dtype=np.float32),
                    axis=np.zeros(3, dtype=np.float32),
                    limit=np.array([0.0, 0.0], dtype=np.float32),
                    parent_link_name=parent_link_name,
                    child_link_name=link_spec.name,
                )
                joint_map[fixed_joint.name] = fixed_joint
                link_map[link_spec.name].set_joint_name(fixed_joint.name)
            link_specs.extend([(child_link, link_spec.name) for child_link in link_spec.body])
        # add a root joint for base link
        joint_map[ROOT_JOINT_NAME] = Joint(
            name=ROOT_JOINT_NAME,
            type=JointType.ROOT,
            origin=np.eye(4, dtype=np.float32),
            axis=np.zeros(3, dtype=np.float32),
            limit=np.array([0.0, 0.0], dtype=np.float32),
            parent_link_name="",
            child_link_name=base_link_name,
        )
        link_map[base_link_name].set_joint_name(ROOT_JOINT_NAME)
        return joint_map, link_map

    def get_link_mesh_verts_faces(
        self, mode: Literal["visual", "collision"] = "collision", return_dict: bool = False
    ) -> tuple[list[Tensor], list[Tensor]] | dict[str, tuple[Tensor, Tensor]]:
        meshes = [self.link_map[link_name].get_trimesh_mesh(mode=mode) for link_name in self.link_names]
        verts = [torch.from_numpy(mesh.vertices).to(device=self.config.device, dtype=torch.float32) for mesh in meshes]
        faces = [torch.from_numpy(mesh.faces).to(device=self.config.device, dtype=torch.long) for mesh in meshes]
        if return_dict:
            return {link_name: (verts[i], faces[i]) for i, link_name in enumerate(self.link_names)}
        else:
            return verts, faces

    def get_link_trimesh_meshes(
        self, mode: Literal["visual", "collision"] = "collision", return_empty_meshes: bool = True
    ) -> dict[str, trimesh.Trimesh]:
        meshes = {link_name: self.link_map[link_name].get_trimesh_mesh(mode=mode) for link_name in self.link_names}
        if not return_empty_meshes:
            meshes = {n: m for n, m in meshes.items() if len(m.vertices) > 0 and len(m.faces) > 0}
        return meshes

    @overload
    @singledispatch()
    def forward_kinematics(
        self,
        joint_values: Float[torch.Tensor, "b num_dofs"],
        joint_names: Optional[List[str]] = None,
        root_poses: Optional[Float[torch.Tensor, "b 4 4"]] = None,
        clamp_joint_values: bool = True,
    ) -> Float[torch.Tensor, "b num_links 4 4"]:
        if joint_names is not None:
            joint_reindex = torch.Tensor(
                [joint_names.index(joint_name) for joint_name in self.active_joint_names], device=joint_values.device
            ).long()
            joint_values = torch.index_select(joint_values, dim=-1, index=joint_reindex)
        batch_size = joint_values.shape[0]
        if root_poses is None:
            root_poses = torch.eye(4, device=joint_values.device, dtype=joint_values.dtype)
            root_poses = root_poses.unsqueeze(0).expand(batch_size, 4, 4)
        else:
            if root_poses.shape != (batch_size, 4, 4):
                raise ValueError(
                    f"Root poses shape {root_poses.shape} is not compatible with joint values shape {joint_values.shape}"
                )
        if clamp_joint_values and self.joint_limits is not None:
            joint_limits = torch.from_numpy(self.joint_limits).to(device=joint_values.device, dtype=joint_values.dtype)
            joint_values = torch.clamp(joint_values, joint_limits[:, 0], joint_limits[:, 1])

        link_poses = torch.zeros(
            batch_size, len(self.link_names), 4, 4, device=joint_values.device, dtype=joint_values.dtype
        )
        for link_name in self.link_names_topological_order:
            joint_name = self.link_map[link_name].joint_name
            joint = self.joint_map[joint_name]
            if joint.type == JointType.ROOT:
                glb_joint_pose = root_poses
            else:
                parent_joint_pose = link_poses[:, self.link_names.index(joint.parent_link_name)]
                if joint_name in self.active_joint_names:
                    local_joint_tf = _build_joint_transform(
                        joint, joint_values[:, self.active_joint_names.index(joint_name)]
                    )
                elif self.config.enable_mimic_joints and self.joint_map[joint_name].mimic_joint is not None:
                    mimic_joint_value = (
                        self.joint_map[joint_name].mimic_offset
                        + self.joint_map[joint_name].mimic_multiplier
                        * joint_values[:, self.active_joint_names.index(self.joint_map[joint_name].mimic_joint)]  # type: ignore
                    )
                    local_joint_tf = _build_joint_transform(joint, mimic_joint_value)
                else:
                    local_joint_tf = _build_joint_transform(joint)
                joint_origin = torch.from_numpy(joint.origin).to(device=joint_values.device, dtype=joint_values.dtype)
                local_joint_tf = local_joint_tf.to(device=joint_values.device)
                glb_joint_pose = torch.matmul(torch.matmul(parent_joint_pose, joint_origin), local_joint_tf)
            link_poses[:, self.link_names.index(link_name)] = glb_joint_pose
        return link_poses

    @overload
    @singledispatch()
    def forward_kinematics(
        self,
        joint_values: Float[np.ndarray, "b num_dofs"],
        joint_names: Optional[List[str]] = None,
        root_poses: Optional[Float[np.ndarray, "b 4 4"]] = None,
        clamp_joint_values: bool = True,
    ) -> Float[np.ndarray, "b num_links 4 4"]:
        batch_input = True
        if joint_names is not None:
            joint_reindex: np.ndarray = np.ndarray(
                [joint_names.index(joint_name) for joint_name in self.active_joint_names]
            )
            joint_values = joint_values[:, joint_reindex]
        joint_values = cast(np.ndarray, joint_values)
        if joint_values.ndim == 1:
            joint_values = joint_values[np.newaxis, :]
            if root_poses is not None:
                root_poses = root_poses[np.newaxis, :, :]
            batch_input = False
        if joint_values.ndim != 2:
            raise ValueError(f"Joint values shape {joint_values.shape} is not supported")

        batch_size = joint_values.shape[0]
        if root_poses is None:
            root_poses = np.eye(4, dtype=joint_values.dtype)
            root_poses = np.tile(root_poses, (batch_size, 1, 1))
        else:
            if root_poses.shape != (batch_size, 4, 4):
                raise ValueError(
                    f"Root poses shape {root_poses.shape} is not compatible with joint values shape {joint_values.shape}"
                )
        if clamp_joint_values and self.joint_limits is not None:
            joint_values = np.clip(joint_values, self.joint_limits[:, 0], self.joint_limits[:, 1])

        link_poses = np.zeros((batch_size, len(self.link_names), 4, 4), dtype=joint_values.dtype)
        for link_name in self.link_names_topological_order:
            joint_name = self.link_map[link_name].joint_name
            joint = self.joint_map[joint_name]
            if joint.type == JointType.ROOT:
                glb_joint_pose = root_poses
            else:
                parent_joint_pose = link_poses[:, self.link_names.index(joint.parent_link_name)]
                if joint_name in self.active_joint_names:
                    local_joint_tf = _build_joint_transform_np(
                        joint, joint_values[:, self.active_joint_names.index(joint_name)]
                    )
                elif self.config.enable_mimic_joints and self.joint_map[joint_name].mimic_joint is not None:
                    mimic_joint_value = (
                        self.joint_map[joint_name].mimic_offset  # type: ignore
                        + self.joint_map[joint_name].mimic_multiplier  # type: ignore
                        * joint_values[:, self.active_joint_names.index(self.joint_map[joint_name].mimic_joint)]  # type: ignore
                    )
                    local_joint_tf = _build_joint_transform_np(joint, mimic_joint_value)
                else:
                    local_joint_tf = _build_joint_transform_np(joint)

                joint_origin = joint.origin
                glb_joint_pose = np.matmul(np.matmul(parent_joint_pose, joint_origin), local_joint_tf)
            link_poses[:, self.link_names.index(link_name)] = glb_joint_pose

        if batch_input:
            return link_poses
        else:
            return np.squeeze(link_poses, axis=0)

    @singledispatch(is_impl=False)
    def forward_kinematics(
        self,
        joint_values: Float[np.ndarray | torch.Tensor, "b num_dofs"],
        joint_names: Optional[list[str]] = None,
        root_poses: Optional[Float[np.ndarray | torch.Tensor, "b 4 4"]] = None,
        clamp_joint_values: bool = True,
    ) -> Float[np.ndarray | torch.Tensor, "b num_links 4 4"]:
        """Forward kinematics.

        Args:
            joint_values (np.ndarray or torch.Tensor): Joint values of shape (batch_size, num_dofs).
            joint_names (list of str, optional): Joint names. Defaults to None.
            root_poses (np.ndarray or torch.Tensor, optional): Root poses of shape (batch_size, 4, 4). Defaults to None.
            clamp_joint_values (bool, optional): Whether to clamp joint values to joint limits. Defaults to True.
        """
        ...

    @property
    def zero_joint_values(self) -> Tensor:
        return torch.zeros((self.num_dofs,), device=self.config.device, dtype=torch.float32)

    @property
    def zero_joint_values_np(self) -> np.ndarray:
        return np.zeros((self.num_dofs,), dtype=np.float32)

    def __repr__(self) -> str:
        result = f"RobotModel(num_dofs={self.num_dofs})\n"

        def _chain_str(link_name: str, indent: str = "") -> str:
            chain_str = f"{link_name}"
            indent += " " * len(link_name)
            first_child_joint = True
            for joint_name, joint in self.joint_map.items():
                if joint.parent_link_name == link_name:
                    if not first_child_joint:
                        chain_str += "\n" + indent
                    chain_str += f" -> {_chain_str(joint.child_link_name, indent + '    ')}"
                    first_child_joint = False
            return chain_str

        result += _chain_str(self.base_link_name)
        return result

    def __str__(self) -> str:
        return self.__repr__()


__all__ = ["RobotModelConfig", "RobotModel"]

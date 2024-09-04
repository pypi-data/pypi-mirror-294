from typing import Tuple, Optional
from airgen.utils.mechanics import quat_wxyz_to_xyzw

import ivy, ivy_mech, ivy_vision
import numpy as np

NP_FLOATING_TYPE = np.float32

def build_camera_intrinsic(camera_params: dict) -> ivy_vision.Intrinsics:
    """given airgen camera parameters, build camera intrinsic matrix

    Args:
        camera_params (dict): aigen camera parameters

    Returns:
        ivy_vision.Intrinsics:
    """
    pp_offset = np.array(
        [item / 2 - 0.5 for item in [camera_params["width"], camera_params["height"]]],
        dtype=NP_FLOATING_TYPE,
    )
    persp_angle = np.array(
        [camera_params["fov"] * np.pi / 180] * 2, dtype=NP_FLOATING_TYPE
    )
    intrinsic = ivy_vision.persp_angles_and_pp_offsets_to_intrinsics_object(
        persp_angle, pp_offset, [camera_params["width"], camera_params["height"]]
    )
    return intrinsic


def build_camera_inv_extrinsic(camera_params: dict) -> ivy.Array:
    """given airgen camera parameters, build camera inverse extrinsic matrix

    Args:
        camera_params (dict): airgen camera parameters

    Returns:
        ivy.Array: inverse of camera extrinsic matrix
    """
    cam_position = np.array(camera_params["camera_position"], dtype=NP_FLOATING_TYPE)
    cam_quaternion = quat_wxyz_to_xyzw(camera_params["camera_orientation_quat_wxyz"])
    cam_quat_poses = ivy.concat((cam_position, cam_quaternion), axis=-1)

    cam_inv_ext_mat = ivy_mech.quaternion_pose_to_mat_pose(cam_quat_poses)
    return cam_inv_ext_mat


def build_camera(camera_params: dict) -> Tuple[ivy.Array, ivy.Array]:
    """given airgen camera parameters, build camera inverse extrinsic matrix and camera intrinsic matrix

    Args:
        camera_params (dict): airgen camera parameters

    Returns:
        Tuple[ivy.Array, ivy.Array]: inverse of camera extrinsic matrix and inverse of camera calibration matrix
    """
    intrinsic = build_camera_intrinsic(camera_params)
    cam_inv_calib_mat = intrinsic.inv_calib_mats
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params)
    return cam_inv_ext_mat, cam_inv_calib_mat


def camera_unproject_depth(
    depth: np.ndarray, cam_inv_ext_mat: ivy.Array, cam_inv_calib_mat: ivy.Array
) -> np.ndarray:
    """generate point cloud from depth image (depth perspective)

    Args:
        depth (np.ndarray): of shape (H, W, 1)
        cam_inv_ext_mat (ivy.Array): inverse of camera extrinsic matrix
        cam_inv_calib_mat (ivy.Array): inverse of camera intrinsic matrix

    Returns:
        np.ndarray: point cloud of shape (N, 3)
    """
    uniform_pixel_coords = ivy_vision.create_uniform_pixel_coords_image(
        image_dims=(depth.shape[0], depth.shape[1])
    )

    cam_coords = ivy_vision.ds_pixel_to_cam_coords(
        uniform_pixel_coords,
        cam_inv_calib_mat,
        [],
        image_shape=(depth.shape[0], depth.shape[1]),
    )
    # normalize the (non-homogeneous) part of camera coordinates to have unit norm and then scale by depth
    cam_coords[..., :-1] = (
        cam_coords[..., :-1]
        / np.linalg.norm(cam_coords[..., :-1], axis=-1, keepdims=True)
    ) * depth
    # camera coordinate to ned
    camera2ned = np.array(
        [[0, -1, 0, 0], [0, 0, -1, 0], [1, 0, 0, 0], [0, 0, 0, 1]],
        dtype=cam_coords.dtype,
    )
    # which is the transpose of
    # camera2ned = np.transpose(
    #     np.array(
    #         [[0, 0, 1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]],
    #         dtype=cam_coords.dtype,
    #     )
    # )
    ned_coords = np.dot(cam_coords, camera2ned)
    return ivy_vision.cam_to_world_coords(ned_coords, cam_inv_ext_mat)[..., 0:3]


def depth2pointcloud(
    depth: np.ndarray,
    camera_param: dict,
    mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """generating point cloud from depth image

    Args:
        depth (np.ndarray): depth image of shape (H, W, 1)
        camera_param (dict): camera parameters that contains fov, height, width and camera pose
        mask (Optional[np.ndarray], optional): boolean (0/1) mask where 1 indicates object of interest, (H, W, 1). Defaults to None.

    Returns:
        np.ndarray: point cloud in airgen world coordinate of shape (N, 3)
    """

    camera_inv_ext_mat, camera_inv_calib_mat = build_camera(camera_param)
    point_cloud = camera_unproject_depth(
        depth=depth,
        cam_inv_ext_mat=camera_inv_ext_mat,
        cam_inv_calib_mat=camera_inv_calib_mat,
    )

    if mask is not None:
        point_cloud = point_cloud[np.where(mask.squeeze(-1) > 0.5)]

    point_cloud = point_cloud.reshape((-1, 3))

    return point_cloud.to_numpy()


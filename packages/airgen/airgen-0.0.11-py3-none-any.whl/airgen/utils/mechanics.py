from typing import Tuple, List, Optional, Any, Dict
import math

import ivy
import ivy_vision
import ivy_mech
import numpy as np
import rerun as rr

# for some ivy version, it is `ivt.set_framework('numpy')`
if hasattr(ivy, "set_framework"):
    ivy.set_framework("numpy")
elif hasattr(ivy, "set_backend"):
    ivy.set_backend("numpy")
else:
    raise ValueError("ivy does not support set_framework or set_backend")

NP_FLOATING_TYPE = np.float32

from airgen.types import Quaternionr, Vector3r


# ref: https:#en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def to_eularian_angles(q: Quaternionr) -> Tuple[float, float, float]:
    """transform from quaternion to euler angles

    Args:
        q (Quaternionr): quaternion in wxyz format

    Returns:
        Tuple[float, float, float]: pitch, roll, yaw in radians
    """
    z = q.z_val
    y = q.y_val
    x = q.x_val
    w = q.w_val
    ysqr = y * y

    # roll (x-axis rotation)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    roll = math.atan2(t0, t1)

    # pitch (y-axis rotation)
    t2 = +2.0 * (w * y - z * x)
    if t2 > 1.0:
        t2 = 1
    if t2 < -1.0:
        t2 = -1.0
    pitch = math.asin(t2)

    # yaw (z-axis rotation)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    yaw = math.atan2(t3, t4)

    return (pitch, roll, yaw)


def homo_coord_to_nonhome_coord(home_coord: ivy.Array) -> ivy.Array:
    """turn homogeneous coordinates to non-homogeneous coordinates (factoring out the last dimension)

    Args:
        home_coord (ivy.Array): of shape (..., n)

    Returns:
        ivy.Array: of shape (..., n-1)
    """
    non_home_coord = home_coord / home_coord[..., -1][..., None]
    return non_home_coord[..., :-1]


def cameracoord2worldcoord(
    camera_coord: List[float], camera_params: dict
) -> np.ndarray:
    """given airgen camera parameters, transform  camera coordinate back to airgen world coordinate

    Args:
        camera_coord (List[float]): (x,y,z)
        camera_params (dict): camera parameters

    Returns:
        np.ndarray: _description_
    """
    cam_inv_ext_mat = build_camera_inv_extrinsic(camera_params=camera_params)
    world_coord = ivy_vision.cam_to_world_coords(camera_coord, cam_inv_ext_mat)[
        ..., 0:3
    ]
    return world_coord


def quat_wxyz_to_xyzw(quat_wxyz: List[float]) -> np.ndarray:
    """transform quaternion (represented by list of floats) from wxyz format to xyzw format

    Args:
        quat_wxyz (List[Float]):

    Returns:
        np.ndarray: quaternion in xyzw format
    """
    return np.array(
        [quat_wxyz[1], quat_wxyz[2], quat_wxyz[3], quat_wxyz[0]], dtype=NP_FLOATING_TYPE
    )


def imagecoord2orientation(pixelcoord, camera_param) -> Tuple[float, float, float]:
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera represented in yaw and pitch (absolute degrees)

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float float]: target pitch, roll, yaw in radians
    """
    delta_yaw = (
        (pixelcoord[0] - camera_param["width"] / 2)
        / camera_param["width"]
        * camera_param["fov"]
    )

    delta_pitch = (
        (camera_param["height"] / 2 - pixelcoord[1])
        / camera_param["height"]
        * 2
        * math.degrees(
            math.atan(
                math.tan(math.radians(camera_param["fov"] / 2))
                / (camera_param["width"] / camera_param["height"])
            )
        )
    )
    target_yaw, target_pitch = (
        math.radians(camera_param["camera_orientation_euler_pry"][2] + delta_yaw),
        math.radians(camera_param["camera_orientation_euler_pry"][0] + delta_pitch),
    )
    return (target_pitch, 0, target_yaw)


def imagecoord2direction(
    pixelcoord: Tuple[float, float], camera_param: Dict[str, Any]
) -> Tuple[float, float, float]:
    """Given camera parameters (position, pose, and fov) and  pixel coordinate, return the 3D direction of the pixel
    with respect to the camera

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float, float]: normalized unit (directional) vector (x, y, z)
    """
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)

    return target_direction


def pose2vector(pitch: float, roll: float, yaw: float) -> Tuple[float, float, float]:
    """transform target direction represnted in (pitch, roll, yaw) in radians to directional vector

    Args:
        pitch (float): in radians
        roll (float): in radians
        yaw (float): in radians

    Returns:
        Tuple[float, float, float]: unit directional vector (x,y,z)
    """
    vector = [
        math.cos(pitch) * math.cos(yaw),
        math.cos(pitch) * math.sin(yaw),
        -math.sin(pitch),
    ]
    return vector


def imagecoord2pose(
    pixelcoord: Tuple[float, float], point_depth: float, camera_param: Dict[str, Any]
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """convert pixel coordinate to 3D coordinate

    Args:
        pixelcoord (Tuple[float, float]): coordinate of the pixel in the image in xy format
        point_depth (float): depth of the point
        camera_param (Dict[str, Any]): camera parameters

    Returns:
        Tuple[float, float, float]: target coordinate in (x, y, z)
        Tuple[float, float, float]: target orientation in (pitch, roll, yaw) in radians
    """
    target_pitch, _, target_yaw = imagecoord2orientation(pixelcoord, camera_param)
    target_direction = pose2vector(target_pitch, 0, target_yaw)
    target_coord = (
        np.array(target_direction) * point_depth + camera_param["camera_position"]
    )
    return target_coord, (target_pitch, 0, target_yaw)


def vec2eulerangles(vec: np.ndarray) -> np.ndarray:
    """transform airgen directional vector to euler angles

    Args:
        vec: directional vector of shape (N, 3)

    Returns:
        np.ndarray: euler angles of shape (N, 3), each row is (pitch, roll, yaw) in degrees
    """

    yaw = np.rad2deg(np.arctan2(vec[:, 1], vec[:, 0]))
    pitch = np.rad2deg(
        np.arctan2(-vec[:, 2], np.sqrt(np.square(vec[:, 0]) + np.square(vec[:, 1])))
    )
    return np.stack([pitch, np.zeros_like(pitch), yaw], axis=1)


def rotate_xy(vec: np.ndarray, theta: float) -> np.ndarray:
    """rotate xy-component of 3d vector by theta (in degrees) counter-clockwise (in xy plane)

    Assume looking from positive z-axis, the orientation is

    ::

        ^ y
        |
        |
        |______> x

    Args:
        vec (np.ndarray): shape (3,)
        theta (float): angles in degrees

    Returns:
        np.ndarray: rotated vector shape (3,)
    """
    theta_radians = 2 * math.pi - math.radians(theta)
    rotation_matrix = np.array(
        [
            [math.cos(theta_radians), -math.sin(theta_radians), 0],
            [math.sin(theta_radians), math.cos(theta_radians), 0],
            [0, 0, 1],
        ],
        dtype=vec.dtype,
    )
    rotated_vec = np.dot(rotation_matrix, vec)
    return rotated_vec

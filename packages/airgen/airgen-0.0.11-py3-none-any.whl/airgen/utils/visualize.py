from typing import Any, Callable, Dict
import math
import numpy as np
import rerun as rr

from airgen.types import ImageType, Quaternionr


def rr_log_airgen_image(
    entity_path: str, image_type: ImageType, image: np.ndarray, image_name: str = ""
):
    """log images from airgen to rerun

    Args:
        entity_path (str): _description_
        image_type (ImageType): _description_
        image (np.ndarray): _description_
        image_name (str, optional): _description_

    Raises:
        ValueError: ValueError if image_type is not supported
    """
    if image_name:
        entity_path = f"{entity_path}/{image_name}"
    else:
        entity_path = f"{entity_path}/{ImageType.to_str(image_type)}"
    params = (entity_path, image)
    if image_type in [ImageType.Scene, ImageType.OpticalFlowVis, ImageType.DepthVis, ImageType.Segmentation, ImageType.Infrared]:
        rr.log(entity_path, rr.Image(image))
    elif image_type in [
        ImageType.DepthPerspective,
        ImageType.DepthPlanar,
        ImageType.DisparityNormalized,
    ]:
        rr.log(entity_path, rr.DepthImage(image))
    elif image_type == ImageType.OpticalFlow:
        rr.log(f"{entity_path}_x", rr.DepthImage(image[0]))
        rr.log(f"{entity_path}_y", rr.DepthImage(image[1]))
    elif image_type == ImageType.SurfaceNormals:
        if image.dtype != np.uint8:
            image = np.round((0.5 * image + 0.5) * 255).astype(np.uint8)
        rr.log(entity_path, rr.Image(image))
    else:
        raise ValueError(f"image type {image_type} not supported")


def rr_camera_capture_logger(rr_space_view_name: str) -> Callable:
    """Given a view space name (entity_path in rerun), return a function that can be used to log camera data (pose and capture in AirGen's 3D world coordinate) to that view space

    Args:
        rr_view_space_name (str): name of the view space (entity_path) in rerun

    Returns:
        Callable: a function that can be used to log camera data to that view space
        def log_camera_data(image: np.ndarray, camera_params: Dict[str, Any], camera_name:str):
            pass

    Usage:
        >>> trajectory_logger = rr_camera_capture_logger("airgen_world")
        >>> trajectory_logger(image, camera_params, camera_name)
    """

    def camera_quat(camera_params: Dict[str, Any]) -> list[float]:
        # compute camera's quaternion
        euler_angle_rr = [
            angle for angle in camera_params["camera_orientation_euler_pry"]
        ]
        # airgen use NED coordinate, hence pitch positive is downward
        euler_angle_rr[0] = -euler_angle_rr[0]
        euler_angle_rr = tuple(math.radians(x) for x in euler_angle_rr)
        return Quaternionr.from_euler_angles(*euler_angle_rr) 

    def camera_focal_length(width, height, fov):
        # compute camera's focal lengh given width, height and fov
        assert width == height, "width and height must be equal"
        res = (
            width / (2 * math.tan(math.radians(fov) / 2)),
            height / (2 * math.tan(math.radians(fov) / 2)),
        )
        return res

    # airgen use NED coordinate (Z axis points downwards), hence pitch positive is downward
    rr.log(rr_space_view_name, rr.ViewCoordinates.RIGHT_HAND_Z_DOWN, timeless=True)

    def log_camera_data(
        image: np.ndarray,
        camera_params: Dict[str, Any],
        camera_name: str = "camera",
    ):
        """log camera data to rerun

        Args:
            images (List[Tuple[ImageType, np.ndarray]]): list of tuple (image_name, image)
            camera_params (Dict[str, Any]): camera parameters
            camera_name (str, optional): name of the camera, defaults to "camera".
        """
        rr.log(
            f"{rr_space_view_name}/{camera_name}",
            rr.Transform3D(
                            translation=camera_params["camera_position"],
                            rotation=rr.Quaternion(xyzw=camera_quat(camera_params)) 
                           )
        )

        rr.log(
            f"{rr_space_view_name}/{camera_name}",
            rr.Pinhole(
                width=camera_params["width"],
                height=camera_params["height"],
                focal_length=camera_focal_length(
                    camera_params["width"], camera_params["height"], camera_params["fov"]
                )
            )   #camera_xyz="FLU",
        )

        rr_log_airgen_image(
            f"{rr_space_view_name}/{camera_name}", camera_params["image_type"], image
        )

    return log_camera_data

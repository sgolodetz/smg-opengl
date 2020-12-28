from OpenGL.GL import *
from typing import Tuple


class OpenGLUtil:
    """Utility functions related to OpenGL."""

    # PUBLIC STATIC METHODS

    @staticmethod
    def set_projection_matrix(intrinsics: Tuple[float, float, float, float], width: int, height: int) -> None:
        """
        Set the OpenGL projection matrix based on a set of camera intrinsics.

        :param intrinsics:  The camera intrinsics.
        :param width:       The width of the viewport.
        :param height:      The height of the viewport.
        """
        near_val: float = 0.1
        far_val: float = 1000.0

        # To rederive these equations, use similar triangles. Note that fx = f / sx and fy = f / sy,
        # where sx and sy are the dimensions of a pixel on the image plane.
        fx, fy, cx, cy = intrinsics
        left_val: float = -cx * near_val / fx
        right_val: float = (width - cx) * near_val / fx
        bottom_val: float = -cy * near_val / fy
        top_val: float = (height - cy) * near_val / fy

        glLoadIdentity()
        glFrustum(left_val, right_val, bottom_val, top_val, near_val, far_val)

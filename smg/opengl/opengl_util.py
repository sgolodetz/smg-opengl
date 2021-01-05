import numpy as np

from OpenGL.GL import *
from typing import Tuple


class OpenGLUtil:
    """Utility functions related to OpenGL."""

    # PUBLIC STATIC METHODS

    @staticmethod
    def begin_2d() -> None:
        """Set appropriate projection and model-view matrices for 2D rendering."""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslated(0.0, 1.0, 0.0)
        glScaled(1.0, -1.0, 1.0)

        glDepthMask(False)

    @staticmethod
    def end_2d() -> None:
        """Restore the projection and model-view matrices that were active prior to 2D rendering."""
        glDepthMask(True)

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

    @staticmethod
    def render_textured_quad(texture_id: int) -> None:
        """
        Render a quad textured with the specified texture over the top of the current viewport.

        :param texture_id:  The ID of the texture to apply to the quad.
        """
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(1, 0)
        glTexCoord2f(1, 1)
        glVertex2f(1, 1)
        glTexCoord2f(0, 1)
        glVertex2f(0, 1)
        glEnd()

        glDisable(GL_TEXTURE_2D)

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

    @staticmethod
    def set_viewport(top_left: Tuple[float, float], bottom_right: Tuple[float, float],
                     window_size: Tuple[int, int]) -> None:
        """
        Set the OpenGL viewport.

        .. note::
            The top-left and bottom-right coordinates of the viewport denote fractions of the window size,
            s.t. (0,0) denotes the top-left of the window and (1,1) denotes the bottom-right of the window.

        :param top_left:        An (x,y) tuple denoting the top-left of the viewport to set.
        :param bottom_right:    An (x,y) tuple denoting the bottom-right of the viewport to set.
        :param window_size:     The window size.
        """
        left: int = int(np.round(top_left[0] * window_size[0]))
        top: int = int(np.round((1.0 - bottom_right[1]) * window_size[1]))
        width: int = int((bottom_right[0] - top_left[0]) * window_size[0])
        height: int = int((bottom_right[1] - top_left[1]) * window_size[1])
        glViewport(left, top, width, height)
        glScissor(left, top, width, height)
        glEnable(GL_SCISSOR_TEST)

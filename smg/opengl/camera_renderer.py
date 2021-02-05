import numpy as np

from OpenGL.GL import *
from typing import Optional, Tuple

from smg.rigging.cameras import Camera

from .opengl_matrix_context import OpenGLMatrixContext
from .opengl_util import OpenGLUtil


class CameraRenderer:
    """Utility functions to render cameras."""

    # ENUMERATIONS

    class EAxesType(int):
        """The types of axes that can be rendered for a camera."""
        pass

    AXES_NUV: EAxesType = 0
    AXES_XYZ: EAxesType = 1

    # PUBLIC STATIC METHODS

    @staticmethod
    def render_camera(cam: Camera, axes_type: EAxesType = AXES_XYZ, *, axis_scale: float = 1.0,
                      body_colour: Optional[Tuple[float, float, float]] = None, body_scale: float = 0.02) -> None:
        """
        Render a camera.

        :param cam:             The camera.
        :param axes_type:       The type of axes to render for the camera.
        :param axis_scale:      The scale factor to apply to each axis.
        :param body_colour:     The colour to use for the camera's body (if we want to render it).
        :param body_scale:      The scale factor to apply to the camera's body (if we're rendering it).
        """
        n, p, u, v = cam.n() * axis_scale, cam.p(), cam.u() * axis_scale, cam.v() * axis_scale
        origin: np.ndarray = np.zeros(3)

        # If a body colour was specified, render the camera's body as a wireframe sphere.
        if body_colour is not None:
            glColor3f(body_colour[0], body_colour[1], body_colour[2])
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            OpenGLUtil.render_sphere(p, body_scale, slices=10, stacks=10)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Render the camera's axes.
        with OpenGLMatrixContext(GL_MODELVIEW, lambda: glTranslatef(*p)):
            glBegin(GL_LINES)

            if axes_type == CameraRenderer.AXES_NUV:
                glColor3f(1.0, 1.0, 0.0)
                glVertex3f(*origin)
                glVertex3f(*u)

                glColor3f(0.0, 1.0, 1.0)
                glVertex3f(*origin)
                glVertex3f(*v)

                glColor3f(1.0, 0.0, 1.0)
                glVertex3f(*origin)
                glVertex3f(*n)
            else:  # AXES_XYZ
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(*origin)
                glVertex3f(*(-u))

                glColor3f(0.0, 1.0, 0.0)
                glVertex3f(*origin)
                glVertex3f(*(-v))

                glColor3f(0.0, 0.0, 1.0)
                glVertex3f(*origin)
                glVertex3f(*n)

            glEnd()

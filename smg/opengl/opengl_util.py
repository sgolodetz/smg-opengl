import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List, Optional, Tuple

from smg.rigging.cameras import SimpleCamera
from smg.rigging.helpers import CameraPoseConverter
from smg.utility import GeometryUtil


class OpenGLUtil:
    """Utility functions related to OpenGL."""

    # NESTED CLASSES

    class GLUQuadricWrapper:
        """A wrapper around a GLU quadric."""

        # CONSTRUCTOR
        def __init__(self, quadric: Optional[GLUquadric] = None):
            """
            Construct a quadric wrapper.

            :param quadric:     An optional existing GLU quadric to wrap (if none is specified,
                                one will be created on the fly).
            """
            self.__alive: bool = True
            self.__quadric: GLUquadric = quadric if quadric is not None else gluNewQuadric()

        # DESTRUCTOR

        def __del__(self):
            """Destroy the quadric wrapper."""
            self.terminate()

        # SPECIAL METHODS

        def __enter__(self):
            """No-op (needed to allow the wrapper's lifetime to be managed by a with statement)."""
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            """Destroy the wrapper at the end of the with statement that's used to manage its lifetime."""
            self.terminate()

        # PUBLIC METHODS

        def get_quadric(self) -> GLUquadric:
            """Get the wrapped quadric."""
            return self.__quadric

        def terminate(self) -> None:
            """Destroy the quadric wrapper."""
            if self.__alive:
                gluDeleteQuadric(self.__quadric)
                self.__alive = False

    class OrientedCylinderContext:
        """Used to allow a GLU cylinder to be rendered at a particular orientation."""

        # CONSTRUCTOR

        def __init__(self, base_centre: np.ndarray, axis: np.ndarray):
            """
            Construct an oriented cylinder context.

            .. note::
                By default, a GLU cylinder will be drawn along the z axis, from z = 0 to z = height. The goal of this
                class is to allow OpenGL's model-view matrix to be temporarily modified so one can be drawn elsewhere.

            :param base_centre: The centre of the base of the cylinder.
            :param axis:        The cylinder's axis (a vector from the centre of its base to the centre of its top).
            """
            self.__base_centre: np.ndarray = base_centre
            self.__axis: np.ndarray = axis

        # SPECIAL METHODS

        def __enter__(self):
            """Modify the model-view matrix to arrange for the cylinder to be drawn in the right place."""
            # Make a camera positioned at the centre of the base of the cylinder and  looking along its axis.
            n: np.ndarray = self.__axis / np.linalg.norm(self.__axis)
            up: np.ndarray = np.array([0.0, -1.0, 0.0])
            camera: SimpleCamera = SimpleCamera(self.__base_centre, n, up)

            # Use it to obtain the matrix that should be used to update OpenGL's model-view matrix.
            m: np.ndarray = np.linalg.inv(CameraPoseConverter.camera_to_pose(camera))

            # Update OpenGL's model-view matrix and return.
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glMultMatrixf(m.flatten(order='F'))
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            """Restore the model-view matrix after drawing the cylinder."""
            glPopMatrix()

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
    def load_matrix(m: np.ndarray) -> None:
        """
        Set the currently active OpenGL matrix to the specified matrix.

        :param m:   The matrix with which to set the currently active OpenGL matrix.
        """
        glLoadMatrixf(m.flatten(order='F'))

    @staticmethod
    def render_aabb(mins: np.ndarray, maxs: np.ndarray) -> None:
        """
        Render an axis-aligned bounding box (AABB).

        :param mins:    The minimum bounds of the AABB.
        :param maxs:    The maximum bounds of the AABB.
        """
        glBegin(GL_LINE_LOOP)
        glVertex3f(mins[0], mins[1], mins[2])
        glVertex3f(maxs[0], mins[1], mins[2])
        glVertex3f(maxs[0], mins[1], maxs[2])
        glVertex3f(mins[0], mins[1], maxs[2])
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex3f(mins[0], maxs[1], mins[2])
        glVertex3f(maxs[0], maxs[1], mins[2])
        glVertex3f(maxs[0], maxs[1], maxs[2])
        glVertex3f(mins[0], maxs[1], maxs[2])
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(mins[0], mins[1], mins[2])
        glVertex3f(mins[0], maxs[1], mins[2])
        glVertex3f(maxs[0], mins[1], mins[2])
        glVertex3f(maxs[0], maxs[1], mins[2])
        glVertex3f(maxs[0], mins[1], maxs[2])
        glVertex3f(maxs[0], maxs[1], maxs[2])
        glVertex3f(mins[0], mins[1], maxs[2])
        glVertex3f(mins[0], maxs[1], maxs[2])
        glEnd()

    @staticmethod
    def render_cylinder(base_centre: np.ndarray, top_centre: np.ndarray, base_radius: float, top_radius: float,
                        slices: int, stacks: int = 1, quadric: Optional[GLUquadric] = None) -> None:
        """
        Render a cylinder between the specified base centre and top centre points.

        :param base_centre:     The centre of the base of the cylinder.
        :param top_centre:      The centre of the top of the cylinder.
        :param base_radius:     The radius of the base of the cylinder.
        :param top_radius:      The radius of the top of the cylinder.
        :param slices:          The number of subdivisions of the cylinder around its length.
        :param stacks:          The number of subdivisions of the cylinder along its length.
        :param quadric:         An optional GLU quadric to use when rendering the cylinder (if none is specified,
                                one will be created on the fly).
        """
        axis: np.ndarray = top_centre - base_centre
        axis_norm: float = np.linalg.norm(axis)
        if axis_norm < 0.001:
            return

        with OpenGLUtil.GLUQuadricWrapper(quadric) as quadric_wrapper:
            with OpenGLUtil.OrientedCylinderContext(base_centre, axis):
                gluCylinder(
                    quadric_wrapper.get_quadric(), base_radius, top_radius, axis_norm, slices, stacks
                )

    @staticmethod
    def render_sphere(centre: np.ndarray, radius: float, *,
                      slices: int, stacks: int, quadric: Optional[GLUquadric] = None) -> None:
        """
        Render a sphere of the specified radius at the specified position.

        :param centre:      The position of the centre of the sphere.
        :param radius:      The radius of the sphere.
        :param slices:      The number of subdivisions of the sphere around its vertical axis.
        :param stacks:      The number of subdivisions of the sphere along its vertical axis.
        :param quadric:     An optional GLU quadric to use when rendering the sphere (if none is specified,
                            one will be created on the fly).
        """
        with OpenGLUtil.GLUQuadricWrapper(quadric) as quadric_wrapper:
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glTranslatef(*centre)
            gluSphere(quadric_wrapper.get_quadric(), radius, slices, stacks)
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
    def render_trajectory(trajectory: List[Tuple[float, np.ndarray]], *, colour: Tuple[float, float, float]) -> None:
        """
        Render the line segments needed to visualise a trajectory.

        :param trajectory:  The trajectory to visualise.
        :param colour:      The colour to use for the line segments.
        """
        if len(trajectory) < 2:
            return

        glColor3f(*colour)

        glBegin(GL_LINE_STRIP)

        for _, pose in trajectory:
            glVertex3f(*pose[0:3, 3])

        glEnd()

    @staticmethod
    def render_voxel_grid(mins: List[float], maxs: List[float], voxel_size: List[float], *,
                          dotted: bool = False) -> None:
        """
        Render a wireframe voxel grid.

        :param mins:        The minimum bounds of the voxel grid.
        :param maxs:        The maximum bounds of the voxel grid.
        :param voxel_size:  The voxel size.
        :param dotted:      Whether to use dotted lines for the voxel grid.
        """
        pts1, pts2 = GeometryUtil.make_voxel_grid_endpoints(mins, maxs, voxel_size)

        if dotted:
            glPushAttrib(GL_ENABLE_BIT)
            glLineStipple(1, 0x8888)
            glEnable(GL_LINE_STIPPLE)

        glBegin(GL_LINES)
        for i in range(len(pts1)):
            glVertex3f(*pts1[i])
            glVertex3f(*pts2[i])
        glEnd()

        if dotted:
            glPopAttrib()

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

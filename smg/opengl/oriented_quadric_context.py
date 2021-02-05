import numpy as np

from OpenGL.GL import *

from smg.rigging.cameras import SimpleCamera


class OrientedQuadricContext:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, p: np.ndarray, axis: np.ndarray):
        """
        Construct an oriented quadric context.

        TODO
        """
        self.__p: np.ndarray = p
        self.__axis: np.ndarray = axis

    # SPECIAL METHODS

    def __enter__(self):
        """TODO"""
        n: np.ndarray = self.__axis / np.linalg.norm(self.__axis)
        up: np.ndarray = np.array([0.0, -1.0, 0.0])
        camera: SimpleCamera = SimpleCamera(self.__p, n, up)
        u: np.ndarray = camera.u()
        v: np.ndarray = camera.v()

        m: np.ndarray = np.array([
            [-u[0], -v[0], n[0], self.__p[0]],
            [-u[1], -v[1], n[1], self.__p[1]],
            [-u[2], -v[2], n[2], self.__p[2]],
            [0.0, 0.0, 0.0, 1.0]
        ])

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMultMatrixf(m.flatten(order='F'))
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """TODO"""
        glPopMatrix()

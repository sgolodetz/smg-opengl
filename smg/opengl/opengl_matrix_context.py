import numpy as np

from OpenGL.GL import *
from typing import Callable


class OpenGLMatrixContext:
    """Used to allow one of the OpenGL matrices to be temporarily changed and then restored later."""

    # CONSTRUCTOR

    def __init__(self, matrix_mode: int, change_matrix: Callable[[], None]):
        """
        Construct an OpenGL matrix context.

        :param matrix_mode:     The OpenGL matrix mode (e.g. GL_PROJECTION) denoting the matrix to be changed.
        :param change_matrix:   The callable that should be used to change the matrix.
        """
        self.__matrix_mode: int = matrix_mode
        self.__set_matrix: Callable[[], None] = change_matrix

    # SPECIAL METHODS

    def __enter__(self):
        """Push the old value of the matrix onto the OpenGL stack and change the matrix to its new value."""
        glMatrixMode(self.__matrix_mode)
        glPushMatrix()
        self.__set_matrix()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Pop the old value of the matrix from the OpenGL stack."""
        glMatrixMode(self.__matrix_mode)
        glPopMatrix()

    # PUBLIC STATIC METHODS

    @staticmethod
    def load_matrix(m: np.ndarray) -> None:
        """
        Set the currently active OpenGL matrix to the specified matrix.

        :param m:   The matrix with which to set the currently active OpenGL matrix.
        """
        glLoadMatrixf(m.flatten(order='F'))

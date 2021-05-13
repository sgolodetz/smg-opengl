import numpy as np

from OpenGL.GL import *


class TriangleMesh:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, vertices: np.ndarray, vertex_colours: np.ndarray, triangles: np.ndarray):
        self.__triangles: np.ndarray = triangles

        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glColorPointer(3, GL_FLOAT, 0, vertex_colours)

    # PUBLIC METHODS

    def render(self) -> None:
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glDrawElements(GL_TRIANGLES, len(self.__triangles) * 3, GL_UNSIGNED_INT, self.__triangles)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

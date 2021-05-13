import numpy as np

from OpenGL.arrays.vbo import VBO
from OpenGL.GL import *


class TriangleMesh:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, vertices: np.ndarray, vertex_colours: np.ndarray, indices: np.ndarray):
        x = np.concatenate([vertices, vertex_colours], axis=1)
        self.__vbo: VBO = VBO(x)
        self.__indices = indices
        self.__ibo: VBO = VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)

        # vertices = np.array([
        #     [0, 1, 0],
        #     [-1, -1, 0],
        #     [1, -1, 0],
        #     [2, -1, 0],
        #     [4, -1, 0],
        #     [4, 1, 0],
        #     [2, -1, 0],
        #     [4, 1, 0],
        #     [2, 1, 0],
        # ], 'f')
        # self.__vbo = VBO(vertices)
        # self.__indices = np.array([[0, 2, 4]], dtype=np.uint32)
        # self.__ibo = VBO(self.__indices, target=GL_ELEMENT_ARRAY_BUFFER)

    # PUBLIC METHODS

    def render(self) -> None:
        self.__vbo.bind()
        self.__ibo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_DOUBLE, 48, self.__vbo)
        glColorPointer(3, GL_DOUBLE, 48, self.__vbo + 24)
        glDrawElements(GL_TRIANGLES, len(self.__indices) * 3, GL_UNSIGNED_INT, self.__ibo)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.__ibo.unbind()
        self.__vbo.unbind()

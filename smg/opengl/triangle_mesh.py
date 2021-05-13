import numpy as np

from OpenGL.arrays.vbo import VBO
from OpenGL.GL import *


class TriangleMesh:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, vertices: np.ndarray, vertex_colours: np.ndarray, indices: np.ndarray):
        self.__vbo: VBO = VBO(vertices)
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
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        self.__vbo.bind()
        self.__ibo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerd(self.__vbo)
        glDrawElements(GL_TRIANGLES, len(self.__indices) * 3, GL_UNSIGNED_INT, self.__ibo)
        # glDrawElements(GL_TRIANGLES, len(self.__indices) * 3, GL_UNSIGNED_INT, self.__indices)
        # glDrawArrays(GL_TRIANGLES, 0, 9)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.__ibo.unbind()
        self.__vbo.unbind()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # glEnableClientState(GL_VERTEX_ARRAY)
        # glEnableClientState(GL_COLOR_ARRAY)
        # glDrawElements(GL_TRIANGLES, len(self.__indices) * 3, GL_UNSIGNED_INT, self.__indices)
        # glDisableClientState(GL_VERTEX_ARRAY)
        # glDisableClientState(GL_COLOR_ARRAY)

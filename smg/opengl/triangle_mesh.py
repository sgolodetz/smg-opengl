import numpy as np

from OpenGL.arrays.vbo import VBO
from OpenGL.GL import *
from typing import Optional


class TriangleMesh:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, vertices: np.ndarray, vertex_colours: np.ndarray, triangles: np.ndarray, *,
                 vertex_normals: Optional[np.ndarray] = None):
        """
        TODO

        :param vertices:        TODO
        :param vertex_colours:  TODO
        :param triangles:       TODO
        :param vertex_normals:  TODO
        """
        # See: http://pyopengl.sourceforge.net/context/tutorials/shader_2.html.
        self.__use_normals: bool = vertex_normals is not None
        if self.__use_normals:
            self.__vbo: VBO = VBO(np.concatenate([vertices, vertex_colours, vertex_normals], axis=1))
        else:
            self.__vbo: VBO = VBO(np.concatenate([vertices, vertex_colours], axis=1))
        self.__ibo: VBO = VBO(triangles, target=GL_ELEMENT_ARRAY_BUFFER)

    # PUBLIC METHODS

    def render(self) -> None:
        """Render the triangle mesh."""
        try:
            self.__vbo.bind()
            self.__ibo.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            if self.__use_normals:
                glEnableClientState(GL_NORMAL_ARRAY)
                glVertexPointer(3, GL_DOUBLE, 72, self.__vbo)
                glColorPointer(3, GL_DOUBLE, 72, self.__vbo + 24)
                glNormalPointer(GL_DOUBLE, 72, self.__vbo + 48)
            else:
                glVertexPointer(3, GL_DOUBLE, 48, self.__vbo)
                glColorPointer(3, GL_DOUBLE, 48, self.__vbo + 24)
            glDrawElements(GL_TRIANGLES, len(self.__ibo) * 3, GL_UNSIGNED_INT, self.__ibo)
        finally:
            if self.__use_normals:
                glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)
            self.__ibo.unbind()
            self.__vbo.unbind()

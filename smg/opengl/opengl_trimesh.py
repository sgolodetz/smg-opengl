import numpy as np

from OpenGL.arrays.vbo import VBO
from OpenGL.GL import *
from typing import Optional


class OpenGLTriMesh:
    """An immutable triangle mesh (stored in a format that can be rendered efficiently by OpenGL)."""

    # CONSTRUCTOR

    def __init__(self, vertices: np.ndarray, vertex_colours: np.ndarray, triangles: np.ndarray, *,
                 vertex_normals: Optional[np.ndarray] = None):
        """
        Construct an immutable OpenGL triangle mesh.

        :param vertices:        The mesh vertices, as an n*3 array with a dtype of np.float64.
        :param vertex_colours:  The mesh vertex colours, as an n*3 array with a dtype of np.float64.
        :param triangles:       The mesh triangles, as an m*3 index array with a dtype of int.
        :param vertex_normals:  The mesh vertex normals, as an n*3 array with a dtype of np.float64 (optional).
        """
        # See: http://pyopengl.sourceforge.net/context/tutorials/shader_2.html.

        # Check that the vertices and vertex_colours arrays have the right dtype, and raise an exception if not.
        if vertices.dtype != np.float64 or vertex_colours.dtype != np.float64:
            raise RuntimeError("The vertices and vertex_colours arrays must have a dtype of np.float64")

        # If the mesh vertex normals have been specified:
        self.__use_normals = vertex_normals is not None  # type: bool
        if self.__use_normals:
            # Check that they have the right dtype, and raise an exception if not.
            if vertex_normals.dtype != np.float64:
                raise RuntimeError("If specified, the vertex normals array must have a dtype of np.float64")

            # Make a vertex buffer object that contains the vertices, vertex colours and vertex normals, interleaved.
            self.__vbo = VBO(np.concatenate([vertices, vertex_colours, vertex_normals], axis=1))  # type: VBO
        else:
            # Otherwise, make a vertex buffer object that contains only the vertices and vertex colours, interleaved.
            self.__vbo = VBO(np.concatenate([vertices, vertex_colours], axis=1))  # type: VBO

        # Make a vertex buffer object from the index array specifying the mesh triangles.
        self.__ibo = VBO(triangles, target=GL_ELEMENT_ARRAY_BUFFER)  # type: VBO

    # PUBLIC METHODS

    def render(self) -> None:
        """Render the triangle mesh."""
        try:
            # Prepare to render the triangles.
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

            # Render the triangles.
            glDrawElements(GL_TRIANGLES, len(self.__ibo) * 3, GL_UNSIGNED_INT, self.__ibo)
        finally:
            # Clean up after rendering the triangles.
            if self.__use_normals:
                glDisableClientState(GL_NORMAL_ARRAY)

            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

            self.__ibo.unbind()
            self.__vbo.unbind()

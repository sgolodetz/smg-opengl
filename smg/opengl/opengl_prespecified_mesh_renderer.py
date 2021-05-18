import numpy as np

from typing import List, Optional, Tuple

from .opengl_mesh_renderer import OpenGLMeshRenderer
from .opengl_triangle_mesh import OpenGLTriangleMesh


class OpenGLPrespecifiedMeshRenderer:
    """An OpenGL renderer for a pre-specified mesh."""

    # CONSTRUCTOR

    def __init__(self, mesh: OpenGLTriangleMesh, base_renderer: Optional[OpenGLMeshRenderer] = None, *,
                 light_dirs: Optional[List[np.ndarray]] = None):
        """
        Construct an OpenGL pre-specified mesh renderer.

        .. note::
            If mesh_renderer is None, a new underlying mesh renderer will be constructed. However, users might
            want to pass an existing one in to avoid wasting resources unnecessarily.
        .. note::
            If light_dirs is None, default light directions will be used. For no lights at all, pass in [].

        :param mesh:            The mesh to render.
        :param base_renderer:   The underlying mesh renderer (optional).
        :param light_dirs:      The directions from which to light the mesh (optional).
        """
        self.__base_renderer: OpenGLMeshRenderer = base_renderer if base_renderer is not None else OpenGLMeshRenderer()
        self.__light_dirs: Optional[List[np.ndarray]] = light_dirs
        self.__mesh: OpenGLTriangleMesh = mesh

    # PUBLIC METHODS

    def render_to_image(self, world_from_camera: np.ndarray, image_size: Tuple[int, int],
                        intrinsics: Tuple[float, float, float, float]) -> np.ndarray:
        """
        Render the pre-specified mesh with the pre-specified directional lighting to an image.

        :param world_from_camera:   The pose from which to render the mesh.
        :param image_size:          The size of image to render, as a (width, height) tuple.
        :param intrinsics:          The camera intrinsics, as an (fx, fy, cx, cy) tuple.
        :return:                    The rendered image.
        """
        return self.__base_renderer.render_to_image(
            self.__mesh, world_from_camera, image_size, intrinsics, light_dirs=self.__light_dirs
        )

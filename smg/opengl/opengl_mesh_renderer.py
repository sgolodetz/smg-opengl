import numpy as np

from OpenGL.GL import *
from typing import List, Optional, Tuple

from smg.rigging.helpers import CameraPoseConverter

from .opengl_framebuffer import OpenGLFrameBuffer
from .opengl_matrix_context import OpenGLMatrixContext
from .opengl_util import OpenGLUtil
from .triangle_mesh import TriangleMesh


class OpenGLMeshRenderer:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self):
        """TODO"""
        self.__framebuffer = None  # type: Optional[OpenGLFrameBuffer]

    # DESTRUCTOR

    def __del__(self):
        """Destroy the renderer."""
        self.terminate()

    # SPECIAL METHODS

    def __enter__(self):
        """No-op (needed to allow the renderer's lifetime to be managed by a with statement)."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the renderer at the end of the with statement that's used to manage its lifetime."""
        self.terminate()

    # PUBLIC METHODS

    def render(self, mesh: TriangleMesh, *, light_dirs: Optional[List[np.ndarray]] = None) -> None:
        """
        Render the specified mesh with the specified directional lighting.

        :param mesh:        The mesh to render.
        :param light_dirs:  The directions from which to light the mesh with directional lights.
        """
        if light_dirs is None:
            pos = np.array([0.0, -2.0, -1.0, 0.0])  # type: np.ndarray
            light_dirs = [pos, -pos]
        elif len(light_dirs) > 8:
            raise RuntimeError("At most 8 light directions can be specified")

        # Save various attributes so that they can be restored later.
        glPushAttrib(GL_DEPTH_BUFFER_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT)

        # Enable lighting.
        glEnable(GL_LIGHTING)

        # Set up the directional lights.
        for i in range(len(light_dirs)):
            light_idx = GL_LIGHT0 + i  # type: int
            glEnable(light_idx)
            glLightfv(light_idx, GL_DIFFUSE, np.array([1, 1, 1, 1]))
            glLightfv(light_idx, GL_SPECULAR, np.array([1, 1, 1, 1]))
            glLightfv(light_idx, GL_POSITION, light_dirs[i])

        # Enable colour-based materials (i.e. let material properties be defined by glColor).
        glEnable(GL_COLOR_MATERIAL)

        # Enable back-face culling.
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)

        # Enable depth testing.
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)

        # Render the mesh itself.
        mesh.render()

        # Restore the attributes to their previous states.
        glPopAttrib()

    def render_to_image(self, mesh: TriangleMesh, world_from_camera: np.ndarray,
                        image_size: Tuple[int, int], intrinsics: Tuple[float, float, float, float],
                        *, light_dirs: Optional[List[np.ndarray]] = None) -> np.ndarray:
        # Make sure the OpenGL frame buffer has been constructed and has the right size.
        width, height = image_size
        if self.__framebuffer is None:
            self.__framebuffer = OpenGLFrameBuffer(width, height)
        elif width != self.__framebuffer.width or height != self.__framebuffer.height:
            self.__framebuffer.terminate()
            self.__framebuffer = OpenGLFrameBuffer(width, height)

        # TODO
        with self.__framebuffer:
            # Set the viewport to encompass the whole framebuffer.
            OpenGLUtil.set_viewport((0.0, 0.0), (1.0, 1.0), (width, height))

            # Clear the background to black.
            glClearColor(1.0, 1.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Set the projection matrix.
            with OpenGLMatrixContext(GL_PROJECTION, lambda: OpenGLUtil.set_projection_matrix(
                intrinsics, width, height
            )):
                # Set the model-view matrix.
                with OpenGLMatrixContext(GL_MODELVIEW, lambda: OpenGLUtil.load_matrix(
                    CameraPoseConverter.pose_to_modelview(np.linalg.inv(world_from_camera))
                )):
                    self.render(mesh, light_dirs=light_dirs)
                    return OpenGLUtil.read_bgr_image(width, height)

    def terminate(self) -> None:
        if self.__framebuffer is not None:
            self.__framebuffer.terminate()
            self.__framebuffer = None

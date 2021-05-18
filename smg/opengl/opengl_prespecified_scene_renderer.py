import numpy as np

from typing import Callable, Generic, List, Optional, Tuple, TypeVar

from .opengl_scene_renderer import OpenGLSceneRenderer


# TYPE VARIABLE

Scene = TypeVar('Scene')


# MAIN CLASS

class OpenGLPrespecifiedSceneRenderer(Generic[Scene]):
    """An OpenGL renderer for a pre-specified scene."""

    # CONSTRUCTOR

    def __init__(self, scene: Scene, render_scene: Callable[[Scene], None],
                 base_renderer: Optional[OpenGLSceneRenderer[Scene]] = None, *,
                 light_dirs: Optional[List[np.ndarray]] = None):
        """
        Construct an OpenGL pre-specified scene renderer.

        .. note::
            If base_renderer is None, a new underlying scene renderer will be constructed. However, users might
            want to pass an existing one in to avoid wasting resources unnecessarily.
        .. note::
            If light_dirs is None, default light directions will be used. For no lights at all, pass in [].

        :param scene:           The scene to render.
        :param base_renderer:   The underlying scene renderer (optional).
        :param light_dirs:      The directions from which to light the scene (optional).
        """
        self.__base_renderer = base_renderer \
            if base_renderer is not None else OpenGLSceneRenderer[Scene]()  # type: OpenGLSceneRenderer[Scene]
        self.__light_dirs = light_dirs                                      # type: Optional[List[np.ndarray]]
        self.__render_scene = render_scene                                  # type: Callable[[Scene], None]
        self.__scene = scene                                                # type: Scene

    # PUBLIC METHODS

    def render_to_image(self, world_from_camera: np.ndarray, image_size: Tuple[int, int],
                        intrinsics: Tuple[float, float, float, float]) -> np.ndarray:
        """
        Render the pre-specified scene with the pre-specified directional lighting to an image.

        :param world_from_camera:   The pose from which to render the scene.
        :param image_size:          The size of image to render, as a (width, height) tuple.
        :param intrinsics:          The camera intrinsics, as an (fx, fy, cx, cy) tuple.
        :return:                    The rendered image.
        """
        return self.__base_renderer.render_to_image(
            self.__scene, self.__render_scene, world_from_camera, image_size, intrinsics,
            light_dirs=self.__light_dirs
        )

import numpy as np

from OpenGL.GL import *

from .opengl_util import OpenGLUtil


class OpenGLImageRenderer:
    """An OpenGL image renderer."""

    # CONSTRUCTOR

    def __init__(self):
        """Construct an OpenGL image renderer."""
        # : bool
        self.__alive = True
        # : int
        self.__texture_id = glGenTextures(1)

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

    def render_image(self, image: np.ndarray, *, use_alpha_blending: bool = False) -> None:
        """
        Render a colour image over the contents of the current viewport.

        :param image:               The colour image.
        :param use_alpha_blending:  Whether or not to use alpha blending.
        """
        # Copy the image to a texture.
        glBindTexture(GL_TEXTURE_2D, self.__texture_id)

        # : int
        channels = image.shape[2]
        if channels == 3:
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGB, image.shape[1], image.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, image
            )
        elif channels == 4:
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA, image.shape[1], image.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, image
            )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        if use_alpha_blending and channels == 4:
            # Save the current state.
            glPushAttrib(GL_COLOR_BUFFER_BIT)

            # Enable alpha blending.
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Render a quad textured with the image over the top of the existing scene.
        OpenGLUtil.begin_2d()
        OpenGLUtil.render_textured_quad(self.__texture_id)
        OpenGLUtil.end_2d()

        if use_alpha_blending and channels == 4:
            # Restore the previous state.
            glPopAttrib(GL_COLOR_BUFFER_BIT)

    def terminate(self) -> None:
        """Destroy the renderer."""
        if self.__alive:
            glDeleteTextures([self.__texture_id])
            self.__alive = False

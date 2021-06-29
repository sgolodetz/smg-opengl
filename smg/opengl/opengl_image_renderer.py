import numpy as np

from OpenGL.GL import *

from .opengl_texture import OpenGLTexture
from .opengl_texture_context import OpenGLTextureContext
from .opengl_util import OpenGLUtil


class OpenGLImageRenderer:
    """An OpenGL image renderer."""

    # CONSTRUCTOR

    def __init__(self):
        """Construct an OpenGL image renderer."""
        self.__alive = True               # type: bool
        self.__texture = OpenGLTexture()  # type: OpenGLTexture

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
        channels = image.shape[2]  # type: int
        if use_alpha_blending and channels == 4:
            # Save the current state.
            glPushAttrib(GL_COLOR_BUFFER_BIT)

            # Enable alpha blending.
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Render a quad textured with the image over the top of the existing scene.
        OpenGLUtil.begin_2d()

        with OpenGLTextureContext(self.__texture):
            self.__texture.set_image(image)

            glColor3f(1.0, 1.0, 1.0)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(0, 0)
            glTexCoord2f(1, 0)
            glVertex2f(1, 0)
            glTexCoord2f(1, 1)
            glVertex2f(1, 1)
            glTexCoord2f(0, 1)
            glVertex2f(0, 1)
            glEnd()

        OpenGLUtil.end_2d()

        if use_alpha_blending and channels == 4:
            # Restore the previous state.
            glPopAttrib(GL_COLOR_BUFFER_BIT)

    def terminate(self) -> None:
        """Destroy the renderer."""
        if self.__alive:
            self.__texture.terminate()
            self.__alive = False

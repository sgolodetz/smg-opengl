import numpy as np

from OpenGL.GL import *


class OpenGLTexture:
    """An OpenGL texture."""

    # CONSTRUCTOR

    def __init__(self):
        """Construct an OpenGL texture."""
        self.__alive = True                   # type: bool
        self.__texture_id = glGenTextures(1)  # type: int

    # DESTRUCTOR

    def __del__(self):
        """Destroy the texture."""
        self.terminate()

    # SPECIAL METHODS

    def __enter__(self):
        """No-op (needed to allow the texture's lifetime to be managed by a with statement)."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the texture at the end of the with statement that's used to manage its lifetime."""
        self.terminate()

    # PUBLIC METHODS

    def bind(self) -> None:
        """Bind the texture."""
        glBindTexture(GL_TEXTURE_2D, self.__texture_id)

    # noinspection PyMethodMayBeStatic
    def set_image(self, image: np.ndarray) -> None:
        """
        Set the image for the texture.

        .. note::
            The texture must be bound prior to calling this method.

        :param image:   The image to set.
        """
        channels = image.shape[2]  # type: int
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

    def terminate(self) -> None:
        """Destroy the texture."""
        if self.__alive:
            try:
                glDeleteTextures([self.__texture_id])
            except Error:
                # FIXME: It's good to be tidy and try to delete the texture, but it crashes sometimes, for reasons
                #        I don't quite understand currently. For that reason, I'm currently suppressing the error,
                #        on the basis that it's a fairly harmless one and crashing is worse.
                pass

            self.__alive = False

    # noinspection PyMethodMayBeStatic
    def unbind(self) -> None:
        """Unbind the texture."""
        glBindTexture(GL_TEXTURE_2D, 0)

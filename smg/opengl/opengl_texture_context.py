from OpenGL.GL import *

from .opengl_texture import OpenGLTexture


class OpenGLTextureContext:
    """TODO"""

    # CONSTRUCTOR

    def __init__(self, texture: OpenGLTexture):
        """
        TODO

        :param texture: TODO
        """
        self.__texture = texture  # type: OpenGLTexture

    # SPECIAL METHODS

    def __enter__(self):
        """No-op (needed to allow the context's lifetime to be managed by a with statement)."""
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_TEXTURE_2D)
        self.__texture.bind()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the context at the end of the with statement that's used to manage its lifetime."""
        self.__texture.unbind()
        glPopAttrib()

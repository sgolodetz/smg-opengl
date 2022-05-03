from OpenGL.GL import *


class OpenGLDepthTestContext:
    """Used to allow OpenGL depth testing to be temporarily enabled and then disabled again later."""

    # CONSTRUCTOR

    def __init__(self, depth_func: int):
        """
        Construct an OpenGL depth test context.

        :param depth_func:  The depth testing function to use.
        """
        self.__depth_func = depth_func  # type: int

    # SPECIAL METHODS

    def __enter__(self):
        """No-op (needed to allow the context's lifetime to be managed by a with statement)."""
        glPushAttrib(GL_DEPTH_BUFFER_BIT)
        glDepthFunc(self.__depth_func)
        glEnable(GL_DEPTH_TEST)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the context at the end of the with statement that's used to manage its lifetime."""
        glPopAttrib()

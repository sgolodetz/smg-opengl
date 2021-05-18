from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *


class OpenGLFrameBuffer:
    """An off-screen frame buffer to which OpenGL rendering calls can be directed."""

    # CONSTRUCTOR

    def __init__(self, width: int, height: int):
        """
        Construct a frame buffer with the specified dimensions.

        :param width:   The width of the frame buffer.
        :param height:  The height of the frame buffer.
        """
        self.__alive = False    # type: bool
        self.__height = height  # type: int
        self.__width = width    # type: int

        # Set up the colour buffer.
        self.__colour_buffer_id = glGenTextures(1)  # type: int
        glBindTexture(GL_TEXTURE_2D, self.__colour_buffer_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Set up the depth buffer.
        self.__depth_buffer_id = glGenRenderbuffers(1)  # type: int
        glBindRenderbuffer(GL_RENDERBUFFER, self.__depth_buffer_id)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)

        # Set up the frame buffer.
        self.__id = glGenFramebuffers(1)  # type: int
        glBindFramebuffer(GL_FRAMEBUFFER, self.__id)

        # Attach the colour buffer to the frame buffer.
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.__colour_buffer_id, 0)

        # Attach the depth buffer to the frame buffer.
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.__depth_buffer_id)

        # Check that the frame buffer has been successfully set up.
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Error: Failed to create the frame buffer")

        # Switch back to rendering to the normal display.
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Mark construction of the frame buffer as having finished successfully.
        self.__alive = True

    # DESTRUCTOR

    def __del__(self):
        """Destroy the frame buffer."""
        self.terminate()

    # SPECIAL METHODS

    def __enter__(self):
        """Activate the frame buffer."""
        glBindFramebuffer(GL_FRAMEBUFFER, self.__id)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Deactivate the frame buffer."""
        # TODO: Note that we don't currently support frame buffer nesting.
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    # PROPERTIES

    @property
    def height(self) -> int:
        """
        Get the height of the frame buffer.

        :return:    The height of the frame buffer.
        """
        return self.__height

    @property
    def width(self) -> int:
        """
        Get the width of the frame buffer.

        :return:    The width of the frame buffer.
        """
        return self.__width

    # PUBLIC METHODS

    def terminate(self) -> None:
        """Destroy the frame buffer."""
        if self.__alive:
            try:
                glDeleteRenderbuffers(1, [self.__depth_buffer_id])
                glDeleteTextures([self.__colour_buffer_id])
                glDeleteFramebuffers(1, [self.__id])
            except Error:
                # FIXME: Unfortunately, glDeleteRenderbuffers seems to be in different places in the different
                #        versions of PyOpenGL we use. That sometimes causes us not to find it, and an exception
                #        to be raised. That leaves us in a much worse position than we would have been had we
                #        simply not tried to be tidy and call glDeleteRenderbuffers in the first place. Since
                #        we're good people, we do still try to call it, but we also suppress any exception that
                #        gets raised as a defence mechanism. That seems like a fair compromise position.
                pass

            self.__alive = False

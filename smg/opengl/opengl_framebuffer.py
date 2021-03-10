from OpenGL.GL import *


class OpenGLFrameBuffer:
    """An off-screen frame buffer to which OpenGL rendering calls can be directed."""

    # CONSTRUCTOR

    def __init__(self, width: int, height: int):
        """
        Construct a frame buffer with the specified dimensions.

        :param width:   The width of the frame buffer.
        :param height:  The height of the frame buffer.
        """
        self.__alive: bool = False

        # Set up the colour buffer.
        self.__colour_buffer_id: int = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__colour_buffer_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # Set up the depth buffer.
        self.__depth_buffer_id: int = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__depth_buffer_id)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)

        # Set up the frame buffer.
        self.__id: int = glGenFramebuffers(1)
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

    # PUBLIC METHODS

    def terminate(self) -> None:
        """Destroy the frame buffer."""
        if self.__alive:
            glDeleteRenderbuffers(1, [self.__depth_buffer_id])
            glDeleteTextures([self.__colour_buffer_id])
            glDeleteFramebuffers(1, [self.__id])
            self.__alive = False

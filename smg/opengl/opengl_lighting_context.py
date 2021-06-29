import numpy as np

from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, Optional


class OpenGLLightingContext:
    """Used to allow the OpenGL lighting to be temporarily changed and then restored later."""

    # NESTED TYPES

    class Light(ABC):
        """An OpenGL light."""

        # PUBLIC ABSTRACT METHODS

        @abstractmethod
        def enable(self, light_id: int) -> None:
            """
            Enable the light using the specified OpenGL light ID.

            :param light_id:    The OpenGL light ID to use.
            """
            pass

    class DirectionalLight(Light):
        """A directional OpenGL light."""

        # CONSTRUCTOR

        def __init__(self, direction: np.ndarray):
            """
            Construct a directional light.

            .. note::
                Directional lights in OpenGL are usually specified using a position that is the negation of the
                desired direction. It's important not to accidentally specify that position as the direction here.

            :param direction:   The direction in which the light is travelling.
            """
            self.__direction = direction  # type: np.ndarray

        # PUBLIC METHODS

        def enable(self, light_id: int) -> None:
            """
            Enable the light using the specified OpenGL light ID.

            :param light_id:    The OpenGL light ID to use.
            """
            glEnable(light_id)
            glLightfv(light_id, GL_DIFFUSE, np.array([1, 1, 1, 1]))
            glLightfv(light_id, GL_SPECULAR, np.array([1, 1, 1, 1]))
            glLightfv(light_id, GL_POSITION, -self.__direction)

    # CONSTRUCTOR

    def __init__(self, lights: Dict[int, Light]):
        """
        Construct an OpenGL lighting context.

        :param lights:  The lights that should be temporarily enabled whilst the context is active.
        """
        self.__lights = lights  # type: Dict[int, OpenGLLightingContext.Light]

    # SPECIAL METHODS

    def __enter__(self):
        """Push the old lighting state onto the OpenGL stack and enable the new lighting state."""
        glPushAttrib(GL_ENABLE_BIT | GL_LIGHTING_BIT)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        for i in range(8):
            light = self.__lights.get(i)  # type: Optional[OpenGLLightingContext.Light]
            if light is not None:
                light.enable(GL_LIGHT0 + i)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Pop the old lighting state from the OpenGL stack."""
        glPopAttrib()

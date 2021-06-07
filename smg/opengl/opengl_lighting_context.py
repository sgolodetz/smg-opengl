import numpy as np

from abc import ABC, abstractmethod
from OpenGL.GL import *
from typing import Dict, Optional


class OpenGLLightingContext:
    """Used to allow the OpenGL lighting to be temporarily changed and then restored later."""

    # NESTED TYPES

    class Light(ABC):
        @abstractmethod
        def enable(self, light_idx: int) -> None:
            pass

    class DirectionalLight(Light):
        def __init__(self, direction: np.ndarray):
            self.__direction = direction  # type: np.ndarray

        def enable(self, light_idx: int) -> None:
            glEnable(light_idx)
            glLightfv(light_idx, GL_DIFFUSE, np.array([1, 1, 1, 1]))
            glLightfv(light_idx, GL_SPECULAR, np.array([1, 1, 1, 1]))
            glLightfv(light_idx, GL_POSITION, -self.__direction)

    # CONSTRUCTOR

    def __init__(self, lights: Dict[int, Light]):
        self.__lights = lights  # type: Dict[int, OpenGLLightingContext.Light]

    # SPECIAL METHODS

    def __enter__(self):
        """TODO"""
        glPushAttrib(GL_ENABLE_BIT | GL_LIGHTING_BIT)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        for i in range(8):
            light = self.__lights.get(i)  # type: Optional[OpenGLLightingContext.Light]
            if light is not None:
                light.enable(GL_LIGHT0 + i)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """TODO"""
        glPopAttrib()

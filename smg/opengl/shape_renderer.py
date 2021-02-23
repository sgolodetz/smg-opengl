from smg.utility import Cylinder, ShapeVisitor, Sphere

from .opengl_util import OpenGLUtil


class ShapeRenderer(ShapeVisitor):
    """A geometric shape renderer."""

    # PUBLIC METHODS

    def visit_cylinder(self, cylinder: Cylinder) -> None:
        """
        Render a cylinder.

        :param cylinder:    The cylinder.
        """
        OpenGLUtil.render_cylinder(
            cylinder.base_centre, cylinder.top_centre, cylinder.base_radius, cylinder.top_radius, slices=10
        )

    def visit_sphere(self, sphere: Sphere) -> None:
        """
        Render a sphere.

        :param sphere:  The sphere.
        """
        OpenGLUtil.render_sphere(sphere.centre, sphere.radius, slices=10, stacks=10)

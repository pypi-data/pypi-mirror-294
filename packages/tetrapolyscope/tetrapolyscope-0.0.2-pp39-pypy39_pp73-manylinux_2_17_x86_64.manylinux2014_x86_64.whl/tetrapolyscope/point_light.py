import polyscope_bindings as psb

from tetrapolyscope.core import glm3
from tetrapolyscope.light import Light

class PointLight(Light):

    # This class wraps a _reference_ to the underlying object, whose lifetime is managed by Polyscope

    def __init__(self, name, position, color, instance=None):
        super().__init__()

        if instance is not None:
            # Wrap an existing instance
            self.bound_instance = instance
        else:
            # Create a new instance
            self.bound_instance = psb.register_point_light(name, glm3(position), glm3(color))


def register_point_light(name, position, color):
    if not psb.is_initialized():
        raise RuntimeError("Polyscope has not been initialized")

    p = PointLight(name, position, color)
    return p


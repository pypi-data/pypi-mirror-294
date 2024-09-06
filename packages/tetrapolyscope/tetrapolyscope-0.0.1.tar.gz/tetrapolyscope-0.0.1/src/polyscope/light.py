import polyscope_bindings as psb

# Base class for common properties and methods on lights
class Light:
    def __init__(self):
        self.bound_instance = None

    ## Light management

    def get_name(self):
        return self.bound_instance.get_name()

    # def remove(self):
    #     self.bound_instance.remove()

    ## Enable/disable
    def set_enabled(self, val=True):
        self.bound_instance.set_enabled(val)

    def is_enabled(self):
        return self.bound_instance.is_enabled()

    ## Set properties
    def set_position(self, new_pos):
        self.bound_instance.set_position(new_pos)

    def set_color(self, new_col):
        self.bound_instance.set_color(new_col)


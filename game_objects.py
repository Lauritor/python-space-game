""" Classes for different game objects. """


class PlayerCharacter:
    def __init__(self, loc_x, loc_y, loc_z):
        self.loc_x = 0     # Location in space: x, y, z coordinates.
        self.loc_y = 0
        self.loc_z = 0
        self.roll = 0           # Orientation in space along principal axes in degrees: roll, pitch yaw.
        self.pitch = 0
        self.yaw = 0

    def get_coords(self):
        return [self.loc_x, self.loc_y, self.loc_z]

class TestStation:
    def __init__(self, center_x, center_y, center_z):
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z
        # self.roll = 0
        # self.pitch = 0
        # self.yaw = 0
        self.roll_speed = 0    # Degrees in second.
        self.pitch_speed = 0
        self.yaw_speed = 0
        self.size_x = 50
        self.size_y = 70
        self.size_z = 90
        self.polygon_type = 'square'
                                #  red,         green       light blue      dark blue       yellow          pink
        self.polygon_colors = [(220, 0, 0), (17, 179, 0), (17, 179, 209), (17, 79, 101),(138, 140, 48), (197, 104, 173)]
        self.polygons = [[[self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2]],

                         [[self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2]],

                         [[self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2]],

                         [[self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2]],

                         [[self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z + self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z + self.size_z/2]],

                         [[self.center_x + self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x + self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y - self.size_y/2, self.center_z - self.size_z/2],
                          [self.center_x - self.size_x/2, self.center_y + self.size_y/2, self.center_z - self.size_z/2]]]


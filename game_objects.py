""" Classes for different game objects. """
import numpy as np

class PlayerCharacter:
    def __init__(self, loc_x, loc_y, loc_z):
        self.loc_x = loc_x          # Location in space: x, y, z coordinates. Y increases downwards on screen.
        self.loc_y = loc_y
        self.loc_z = loc_z
        self.roll = 0               # Orientation in space along principal axes in degrees: roll, pitch yaw.
        self.pitch = 0
        self.yaw = 0
        self.direction = np.array([0, 0, 0])  # Direction of current movement.
        self.speed = 0              # Movement speed in the direction of the velocity vector.
        self.screen_distance = 960  # Distance from player (camera) to rendering screen.
        self.throttle = 0           # User inputted max speed of the ship.

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
        self.pitch_speed = 3
        self.yaw_speed = 5
        self.size_x = 50
        self.size_y = 70
        self.size_z = 90
        self.polygon_type = 'square'
                                # left red,    right green    toplight blue    botdark blue     backyellow     frontpink
        self.polygon_colors = [(220, 0, 0), (17, 179, 0), (17, 179, 209), (17, 79, 101),(138, 140, 48), (197, 104, 173),
                               (17, 179, 209), (17, 179, 209), (17, 179, 209), (17, 179, 209),(17, 179, 209), (17, 179, 209)]
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


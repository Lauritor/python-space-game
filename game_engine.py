""" Function for running the game engine. """

import math
import numpy as np

def player_movement(frame_yaw, frame_pitch, player, fps):
    """ Calculates player movement and new location each frame.
    :param player: Player object.
    :return:
    """
    # Movement and inertia calculations.
    alpha = frame_yaw % 360
    beta = frame_pitch % 360
    z = player.throttle / fps * math.cos(alpha) * math.cos(beta)
    y = player.throttle / fps * math.sin(beta)
    x = player.throttle / fps * math.sin(alpha) * math.cos(beta)
    #print("current", alpha, beta, [x, y, z])
    player.direction = player.direction + np.array([x, y, z])
    player.direction[1] = player.direction[1] * 0.99
    player.direction[2] = player.direction[2] * 0.99
    print(player.direction)
    # speed = np.sqrt(player.direction.dot(player.direction))
    # print("speed", speed)
    #print("direction", player.direction)
    # print(player.direction)
    # player.direction = np.divide(player.direction, player.speed)

    # print(player.direction)
    player.loc_x += player.direction[0] / fps
    player.loc_y += player.direction[1] / fps
    player.loc_z += player.direction[2] / fps

    #print(player.get_coords())
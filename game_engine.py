""" Functions for running the game engine. """

import pygame
import numpy as np
import math

from game_objects import *


def euclidean_distance(point_1, point_2):
    # Distance between two points in any dimensional space.
    # return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2 + (point_1[2] - point_2[2]) ** 2)
    distance_sum = 0
    for i, coordinate_1 in enumerate(point_1):
        coordinate_2 = point_2[i]
        distance_sum += (coordinate_1 - coordinate_2) ** 2
    return math.sqrt(distance_sum)


# def euclidean_distance_2d(point_1, point_2):
#     # Distance between two points in 2D space.
#     distance_sum = 0
#     for i, coordinate_1 in enumerate(point_1):
#         coordinate_2 = point_2[i]
#         distance_sum += (coordinate_1 - coordinate_2) ** 2
#     return math.sqrt(distance_sum)

def rotate_point(rotation_center, point, roll, pitch, yaw):
    # Using rotation matrix. Default rotation around origo (0, 0, 0) so points are translated to origo.
    x_translate = point[0] - rotation_center[0]
    y_translate = point[1] - rotation_center[1]
    z_translate = point[2] - rotation_center[2]

    alfa = math.radians(roll)
    gamma = math.radians(pitch)
    beta = math.radians(yaw)
    cos_a, sin_a = np.cos(alfa), np.sin(alfa)
    cos_b, sin_b = np.cos(beta), np.sin(beta)
    cos_g, sin_g = np.cos(gamma), np.sin(gamma)

    # Rotation matrix multiplied by coordinates. https://en.wikipedia.org/wiki/Rotation_matrix#General_rotations
    rotation_matrix = np.array(
        [[cos_a * cos_b, cos_a * sin_b * sin_g - sin_a * cos_g, cos_a * sin_b * cos_g + sin_a * sin_g],
         [sin_a * cos_b, sin_a * sin_b * sin_g + cos_a * cos_g, sin_a * sin_b * cos_g - cos_a * sin_g],
         [-sin_b, cos_b * sin_g, cos_b * cos_g]])
    translated_coordinates = np.array([[x_translate], [y_translate], [z_translate]])
    new_coordinates = np.dot(rotation_matrix, translated_coordinates)

    # Translate points back to their original coordinates.
    new_x = new_coordinates[0][0] + rotation_center[0]
    new_y = new_coordinates[1][0] + rotation_center[1]
    new_z = new_coordinates[2][0] + rotation_center[2]
    return [new_x, new_y, new_z]

def rotate_object(object, fps):
    polygons = object.polygons
    roll_speed = object.roll_speed / fps
    pitch_speed = object.pitch_speed / fps
    yaw_speed = object.yaw_speed / fps
    center_x = object.center_x
    center_y = object.center_y
    center_z = object.center_z
    new_polygons = []
    for polygon in polygons:
        new_polygon = []
        for point in polygon:
            new_polygon.append(
                rotate_point([center_x, center_y, center_z], point, roll_speed, pitch_speed, yaw_speed))

            # Coordinate changes of rolling object: https://math.stackexchange.com/a/270204
            # roll_angle_rad = math.radians(roll_speed / fps)
            # rolled_x = (point[0] - center_x) * math.cos(roll_angle_rad) - (point[1] - center_y) * \
            #            math.sin(roll_angle_rad) + center_x
            # rolled_y = (point[0] - center_x) * math.sin(roll_angle_rad) + (point[1] - center_y) * \
            #            math.cos(roll_angle_rad) + center_y
            #
            # pitch_angle_rad = math.radians(pitch_speed / fps)
            # pitched_y = (rolled_y - center_y) * math.cos(pitch_angle_rad) - (point[2] - center_z) * \
            #             math.sin(pitch_angle_rad) + center_y
            # pitched_z = (rolled_y - center_y) * math.sin(pitch_angle_rad) + (point[2] - center_z) * \
            #             math.cos(pitch_angle_rad) + center_z
            #
            # yaw_angle_rad = math.radians(yaw_speed / fps)
            # yawed_x = (rolled_x - center_x) * math.cos(yaw_angle_rad) - (pitched_z - center_z) * \
            #           math.sin(yaw_angle_rad) + center_x
            # yawed_z = (rolled_x - center_x) * math.sin(yaw_angle_rad) + (pitched_z - center_z) * \
            #           math.cos(yaw_angle_rad) + center_z
            # new_polygon.append([yawed_x, pitched_y, yawed_z])

        new_polygons.append(new_polygon)
    return new_polygons

def calculate_frustum(player, screen_distance):
    """ Function to calculate viewing frustum planes based on player location.

    :param PlayerCharacter: PlayerCharacter object
    :return: List of vector normals of the viewing frustum planes.
    """

    screen_corner_1 = [player.loc_x - (1920 / 2), player.loc_y + (1080 / 2),
                       screen_distance + player.loc_z]
    screen_corner_2 = [player.loc_x + (1920 / 2), player.loc_y + (1080 / 2),
                       screen_distance + player.loc_z]
    screen_corner_3 = [player.loc_x + (1920 / 2), player.loc_y - (1080 / 2),
                       screen_distance + player.loc_z]
    screen_corner_4 = [player.loc_x - (1920 / 2), player.loc_y - (1080 / 2),
                       screen_distance + player.loc_z]
    screen_corners = [screen_corner_1, screen_corner_2, screen_corner_3, screen_corner_4]
    corners = []
    for point in screen_corners:
        corners.append(rotate_point(player.get_coords(), point, player.roll, player.pitch, player.yaw))

    """ Plane vector normal points to the direction of the cross product of vectors that determine the plane.
        Using right-hand rule: plane formed by vectors A x B, where A = index finger, B = middle finger, points 
        towards thumb of the right hand. 
        
        By calculating the dot product of a point and plane normal of each side of the viewing frustum, it can be
        determined if a point is inside or outside the frustum: https://gamedev.stackexchange.com/a/79206
        Positive dot product means that the point is in front of the plane, on the side vector normal points away from.
        If a point is in front of every frustum plane, the point is inside the frustum and should be rendered."""

    top_plane_points = [corners[0], corners[1]]
    right_plane_points = [corners[1], corners[2]]
    bottom_plane_points = [corners[2], corners[3]]
    left_plane_points = [corners[3], corners[0]]
    plane_points = [top_plane_points, right_plane_points, bottom_plane_points, left_plane_points]

    # Sides of frustum. Planes determined by two vectors from camera to screen corners.
    plane_normals = []
    for plane_point_pair in plane_points:
        # Vector direction: end point - start point.
        A = np.array(plane_point_pair[0]) - np.array(player.get_coords())
        B = np.array(plane_point_pair[1]) - np.array(player.get_coords())
        plane_normal = np.cross(A, B)
        plane_normals.append(plane_normal)
    # Screen end of the frustum. Plane determined by two vectors from screen corners to screen corners.
    A = np.array(corners[2]) - np.array(corners[1])
    B = np.array(corners[0]) - np.array(corners[1])
    plane_normals.append(np.cross(A, B))

    return plane_normals
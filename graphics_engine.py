""" Functions for rendering the game graphics on screen. """

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
    # Using rotation matrix. Default rotation around origo (0, 0, 0) so points are translated to origo and back.
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

def render_polygon(polygon, player, screen_distance):
    final_x, final_y, z_depths = [], [], []
    for point in polygon:
        # matrix_a = np.array([[point[0]], [point[1]], [point[2]]])
        # matrix_c = np.array([[player.loc_x],[player.loc_y],[player.loc_z]])
        # theta_x = player.roll % 360
        # theta_y = player.pitch % 360
        # theta_z = player.yaw % 360
        # cos_t_x, sin_t_x = np.cos(theta_x), np.sin(theta_x)
        # cos_t_y, sin_t_y = np.cos(theta_y), np.sin(theta_y)
        # cos_t_z, sin_t_z = np.cos(theta_z), np.sin(theta_z)
        # matrix_x = np.array([[1,        0,          0],
        #                      [0,        cos_t_x,    sin_t_x],
        #                      [0,        sin_t_x,    cos_t_x]])
        # matrix_y = np.array([[cos_t_y,  0,          -sin_t_y],
        #                      [0,        1,          0],
        #                      [sin_t_y,  0,          cos_t_x]])
        # matrix_z = np.array([[cos_t_z,  sin_t_z,    0],
        #                      [-sin_t_z, cos_t_z,    0],
        #                      [0,        0,          1]])
        # a_minus_c = np.subtract(matrix_a, matrix_c)
        # matrix_d = np.linalg.multi_dot([matrix_x, matrix_y, matrix_z, a_minus_c])
        # # matrix_e = np.array([player.loc_x, player.loc_y, player.loc_z + 500])
        # final_x.append(200 / matrix_d[2][0] * matrix_d[0][0] + 200)
        # final_y.append(200 / matrix_d[2][0] * matrix_d[1][0] + 200)
        # # Render using perspective projection: https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula

        point = rotate_point(player.get_coords(), point, player.roll % 360, player.pitch % 360, player.yaw % 360)
        # Distance from camera to rendered point.
        hypotenuse_distance = math.sqrt((player.loc_x - point[0]) ** 2 + (player.loc_y - point[1]) ** 2 + (player.loc_z - point[2]) ** 2)

        # if hasdadypotenuse_distance == 0:
        #     hypotenuse_distance = 0.00001

        hypotenuse_object = math.sqrt((player.loc_x - point[0]) ** 2 + (player.loc_y - point[1]) ** 2)
        angle_rad = math.asin(hypotenuse_object / hypotenuse_distance)  # Angle between camera direction and object.
        # print(player.get_coords(), point)
        # print(angle_rad)

        hypotenuse_screen = screen_distance / math.cos(angle_rad)
        distance_ratio = hypotenuse_screen / hypotenuse_distance

        final_x.append((point[0]) * distance_ratio + 1920 / 2)  # Center on screen center.
        final_y.append((point[1]) * distance_ratio + 1080 / 2)
        z_depths.append(hypotenuse_distance)

    depth_factor = sum(z_depths) / len(z_depths)
    return [[(final_x[0], final_y[0]), (final_x[1], final_y[1]),(final_x[2], final_y[2]), (final_x[3], final_y[3])], depth_factor]

def calculate_frustum(player, screen_distance):
    """ Function to calculate viewing frustum planes based on player location.

    :param PlayerCharacter: PlayerCharacter object
    :return: List of vector normals of the viewing frustum planes.
    """

    screen_corner_1 = [player.loc_x - (1920 / 2), player.loc_y - (1080 / 2), screen_distance + player.loc_z]
    screen_corner_2 = [player.loc_x + (1920 / 2), player.loc_y - (1080 / 2), screen_distance + player.loc_z]
    screen_corner_3 = [player.loc_x + (1920 / 2), player.loc_y + (1080 / 2), screen_distance + player.loc_z]
    screen_corner_4 = [player.loc_x - (1920 / 2), player.loc_y + (1080 / 2), screen_distance + player.loc_z]

    corners = []
    for point in [screen_corner_1, screen_corner_2, screen_corner_3, screen_corner_4]:
        print(point)
        corners.append(rotate_point(player.get_coords(), point, player.roll % 360, player.pitch % 360, player.yaw % 360))
    print(corners)

    """ Plane vector normal points to the direction of the cross product of vectors that determine the plane.
        Using right-hand rule: plane formed by vectors A x B, where A = index finger, B = middle finger, points 
        towards thumb of the right hand. 
        
        By calculating the dot product of a point and plane normal of each side of the viewing frustum, it can be
        determined if a point is inside or outside the frustum: https://gamedev.stackexchange.com/a/79206
        
        Calculating dot product: https://stackoverflow.com/a/15691064/11406583
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
        #print("pair", plane_point_pair, player.get_coords())
        # Vector direction: end point - start point.
        A = np.subtract(np.array(plane_point_pair[0]), np.array(player.get_coords()))
        B = np.subtract(np.array(plane_point_pair[1]), np.array(player.get_coords()))
        plane_normal = np.cross(A, B)
        d = np.dot(plane_normal, plane_point_pair[0])
        #print("dddddddddddddd", d)
        plane_normal = np.concatenate([plane_normal, [d]])
        #print("norm", plane_normal)
        plane_normals.append(plane_normal)

    # Screen end of the frustum. Plane determined by two vectors from screen corners to screen corners.
    A = np.subtract(np.array(corners[2]),np.array(corners[1]))
    B = np.subtract(np.array(corners[0]),np.array(corners[1]))
    plane_normal = np.cross(A,B)
    d = np.dot(plane_normal, np.array(corners[2]))
    #print("dddddddddddddd", d)
    plane_normal = np.concatenate([plane_normal, [d]])
    plane_normals.append(plane_normal)
    #plane_normals.append(np.cross(A, B))
    #print("1",plane_normals)
    return plane_normals


def check_rendering(polygon, frustum_planes):
    #print("2",frustum_planes)
    in_view = True
    dot_products = []
    for point in polygon:
        point.append(1)
        #print("p",point)
        for plane_normal in frustum_planes:
            #plane_normal = np.concatenate([plane_normal, np.array([0])])
            #print("plane normal", plane_normal)
            #print("point", np.array(point))
            #print("dot", np.dot(np.array(point), plane_normal))
            dot_products.append(np.dot(np.array(point), plane_normal))
    #print(dot_products[0:5])
    if any(dot_product < 0 for dot_product in dot_products):
        in_view = False

    return in_view
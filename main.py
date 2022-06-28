""" Function for running the game loop."""

import copy
import math
import numpy as np
import pygame
import pygame.gfxdraw
from game_engine import *
from game_objects import *


def game_loop():
    """ Function for running the game loop.
        Reads the user key inputs and renders the game graphics.
    """
    player = PlayerCharacter(0, 0, 0)
    station1 = TestStation(100, 100, 1000)

    pygame.init()



    fps = 120

    screen_distance = 700
    while True:

        clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        window_width = 1920
        window_height = 1080
        screen = pygame.display.set_mode((window_width, window_height))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        key_states = pygame.key.get_pressed()
        if key_states[pygame.K_w]:
            player.pitch -= 1
        if key_states[pygame.K_s]:
            player.pitch += 1
        if key_states[pygame.K_d]:
            player.yaw -= 1
        if key_states[pygame.K_a]:
            player.yaw += 1
        if key_states[pygame.K_q]:
            player.loc_z -= 1
        if key_states[pygame.K_e]:
            player.loc_z += 1
        if key_states[pygame.K_KP8]:
            player.loc_y += 1
        if key_states[pygame.K_KP2]:
            player.loc_y -= 1
        if key_states[pygame.K_KP4]:
            player.loc_x -= 1
        if key_states[pygame.K_KP6]:
            player.loc_x += 1
        if key_states[pygame.K_r]:
            screen_distance -= 1
        if key_states[pygame.K_f]:
            screen_distance += 1
        if key_states[pygame.K_z]:
            player.roll += 1
            #print(player.roll)
        if key_states[pygame.K_x]:
            player.roll -= 1
            #print(player.roll)

        # Draw crosshairs.
        pygame.draw.circle(screen, (250, 250, 250), (960, 540), 3)
        pygame.draw.circle(screen, (17, 179, 0), (10, 10), 3)
        pygame.draw.circle(screen, (17, 179, 209), (1910, 1070), 3)
        # Rotate objects in view.
        station1.polygons = rotate_object(station1, fps)


        polygons = copy.deepcopy(station1.polygons) # Copy to edit values.

        plane_normals = calculate_frustum(player, screen_distance)
        # pygame.gfxdraw.aapolygon(screen, [(corners[0][0]+1920/2, corners[0][1]+1080/2), (corners[1][0]+1920/2, corners[1][1]+1080/2),
        #                                   (corners[2][0]+1920/2, corners[2][1]+1080/2), (corners[3][0]+1920/2, corners[3][1]+1080/2)], (250,250,250))

       # pygame.draw.circle(screen, (250,250,250),  (player.loc_x - (1920 / 2 - 5), player.loc_y + (1080 / 2 - 5)), 5, )

    # screen_corner_2 = [player.loc_x + (1920 / 2), player.loc_y + (1080 / 2),
    #                    screen_distance + player.loc_z]
    # screen_corner_3 = [player.loc_x + (1920 / 2), player.loc_y - (1080 / 2),
    #                    screen_distance + player.loc_z]
    # screen_corner_4 = [player.loc_x - (1920 / 2), player.loc_y - (1080 / 2),
    #                    screen_distance + player.loc_z])

        rendered_polygons = []
        for i, polygon in enumerate(polygons):
            color_p = station1.polygon_colors[i]
            in_view = True

            dot_products = []
            for point in polygon:
                for plane_normal in plane_normals:

                    dot_products.append(np.dot(plane_normal, np.array(point)))
            prinout = []
            for x in dot_products:
                if x > 0:
                    prinout.append(1)
                else:
                    prinout.append(-1)
            print(prinout[0:5])
            if any(dot_product > 0 for dot_product in dot_products):
                in_view = False

            # print("__________________")
            # print(dot_products)





            if in_view:
                rotated_polygon = []
                for point in polygon:
                    rotated_polygon.append(rotate_point(player.get_coords(), point, player.roll % 360,
                                                    player.pitch % 360, player.yaw % 360))

                final_x, final_y, z_depths = [], [], []
                for point in rotated_polygon:
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


                    # Distance from camera to rendered point.
                    hypotenuse_distance = euclidean_distance(player.get_coords(), point)

                    # if hasdadypotenuse_distance == 0:
                    #     hypotenuse_distance = 0.00001

                    hypotenuse_object = math.sqrt((player.loc_x - point[0]) ** 2 + (player.loc_y - point[1]) ** 2)
                    angle_rad = math.asin(hypotenuse_object / hypotenuse_distance) # Angle between camera direction and object.
                    #print(player.get_coords(), point)
                    #print(angle_rad)

                    hypotenuse_screen = screen_distance / math.cos(angle_rad)
                    distance_ratio = hypotenuse_screen / hypotenuse_distance

                    final_x.append((player.loc_x - point[0]) * distance_ratio + 1920/2)    # Center on screen center.
                    final_y.append((player.loc_y - point[1]) * distance_ratio + 1080/2)
                    z_depths.append(hypotenuse_distance)

                depth_factor = sum(z_depths) / len(z_depths)
                rendered_polygons.append([[(final_x[0], final_y[0]), (final_x[1], final_y[1]),
                                                 (final_x[2], final_y[2]), (final_x[3], final_y[3])],color_p, depth_factor])
                # pygame.gfxdraw.aapolygon(screen, [(final_x[0], final_y[0]), (final_x[1], final_y[1]),
                #                                  (final_x[2], final_y[2]), (final_x[3], final_y[3])],color_p)
                # pygame.gfxdraw.filled_polygon(screen, [(final_x[0], final_y[0]), (final_x[1], final_y[1]),
                #                                   (final_x[2], final_y[2]), (final_x[3], final_y[3])], color_p)
#testasdasd
        #print(rendered_polygons)
        rendered_polygons = sorted(rendered_polygons, key=lambda x: x[2], reverse=True)
        for polygon in rendered_polygons:
            pygame.gfxdraw.aapolygon(screen, polygon[0],polygon[1])
            pygame.gfxdraw.filled_polygon(screen, polygon[0],polygon[1])
        pygame.display.update()
        clock.tick(fps)  # Limit framerate to 120 FPS.


game_loop()

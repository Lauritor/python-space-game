""" Function for running the game loop."""

import copy
import math
import numpy as np
import pygame
import pygame.gfxdraw
from graphics_engine import *
from game_objects import *
from game_engine import *


def game_loop():
    """ Function for running the game loop.
        Reads the user key inputs and renders the game graphics.
    """

    pygame.init()

    # Game objects
    player = PlayerCharacter(0, 99999999999, 0)
    station1 = TestStation(0, 0, 1000)
    station2 = TestStation(100, 300, -1000)

    # Static variables.
    fps = 120
    window_width = 1920
    window_height = 1080
    screen_distance = 700

    while True:
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        screen = pygame.display.set_mode((window_width, window_height))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        key_states = pygame.key.get_pressed()
        if key_states[pygame.K_w]:
            player.pitch += 1
        if key_states[pygame.K_s]:
            player.pitch -= 1
        if key_states[pygame.K_d]:
            player.yaw += 1
        if key_states[pygame.K_a]:
            player.yaw -= 1
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
        # pygame.draw.circle(screen, (17, 179, 0), (10, 10), 3)
        # pygame.draw.circle(screen, (17, 179, 209), (1910, 1070), 3)
        # Object rotation animation.
        station1.polygons = rotate_object(station1, fps)
        station2.polygons = rotate_object(station2, fps)

        station1_polygons = copy.deepcopy(station1.polygons) # Copy to edit values.
        station2_polygons = copy.deepcopy(station2.polygons)
        polygons = station1_polygons + station2_polygons

        frustum_planes = calculate_frustum(player, screen_distance)

        rendered_polygons = []
        for i, polygon in enumerate(polygons):
            color_p = station1.polygon_colors[i]
            in_view = check_rendering(polygon, frustum_planes)
            #in_view = True
            # print("__________________")
            # print(dot_products)
            #print(in_view)
            if in_view:
                rendered_polygon = render_polygon(polygon, player, screen_distance)
                rendered_polygon.append(color_p)
                rendered_polygons.append(rendered_polygon)

        rendered_polygons = sorted(rendered_polygons, key=lambda x: x[1], reverse=True)
        for polygon in rendered_polygons:
            pygame.gfxdraw.aapolygon(screen, polygon[0],polygon[2])
            pygame.gfxdraw.filled_polygon(screen, polygon[0],polygon[2])

        screen_corner_1 = [player.loc_x - (1910 / 2), player.loc_y - (1070 / 2), screen_distance + player.loc_z]
        screen_corner_2 = [player.loc_x + (1910 / 2), player.loc_y - (1070 / 2), screen_distance + player.loc_z]
        screen_corner_3 = [player.loc_x + (1910 / 2), player.loc_y + (1070 / 2), screen_distance + player.loc_z]
        screen_corner_4 = [player.loc_x - (1910 / 2), player.loc_y + (1070 / 2), screen_distance + player.loc_z]
        corners = []
        for point in [screen_corner_1, screen_corner_2, screen_corner_3, screen_corner_4]:
            corners.append(point)
            # corners.append(
            #     rotate_point(player.get_coords(), point, player.roll % 360, player.pitch % 360, player.yaw % 360))
        #print("corners",  corners)


        render_corners = []
        for point in corners:
            point = rotate_point(player.get_coords(), point, player.roll % 360, player.pitch % 360, player.yaw % 360)
            # Distance from camera to rendered point.
            hypotenuse_distance = euclidean_distance(player.get_coords(), point)

            # if hasdadypotenuse_distance == 0:
            #     hypotenuse_distance = 0.00001

            hypotenuse_object = math.sqrt((player.loc_x - point[0]) ** 2 + (player.loc_y - point[1]) ** 2)
            angle_rad = math.asin(hypotenuse_object / hypotenuse_distance)  # Angle between camera direction and object.
            # print(player.get_coords(), point)
            # print(angle_rad)

            hypotenuse_screen = screen_distance / math.cos(angle_rad)
            distance_ratio = hypotenuse_screen / hypotenuse_distance

            render_corners.append([(point[0]) * distance_ratio + 1920 / 2, (point[1]) * distance_ratio + 1080 / 2])
            # upleft red,    upright green    botirght blue      bot left pink
        colors = [(220, 0, 0), (17, 179, 0), (17, 179, 209), (197, 104, 173)]
        for i, point in enumerate(render_corners):
            #print("point", point)
            pygame.draw.circle(screen, colors[i], (point[0], point[1]), 3)

        print(check_rendering([[0,0,701]], frustum_planes))
        pygame.display.update()
        clock.tick(fps)  # Limit framerate to 120 FPS.


game_loop()

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
    #print(pygame.font.get_fonts())
    # Text displaying on screen.
    font = pygame.font.SysFont('century', 24)


    # Game objects.
    player = PlayerCharacter(0, 0, 0)
    station1 = TestStation(0, 0, 1000)
    station2 = TestStation(100, 300, -1000)

    # Static variables.
    fps = 120
    window_width = 1920
    window_height = 1080
    screen_distance = 960

    while True:
        clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        screen = pygame.display.set_mode((window_width, window_height))
        mouse_pos = pygame.mouse.get_pos()

        speed_meter = font.render(str(round(player.throttle)), True, (255,255,255))
        screen.blit(speed_meter, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        key_states = pygame.key.get_pressed()
        frame_roll, frame_pitch, frame_yaw = 0, 0, 0
        if key_states[pygame.K_w]:
            #frame_pitch += 1
            frame_pitch += 1
        if key_states[pygame.K_s]:
            frame_pitch -= 1
        if key_states[pygame.K_q]:
            frame_yaw -= 1
        if key_states[pygame.K_e]:
            frame_yaw += 1
        if key_states[pygame.K_a]:
            frame_roll += 1
        if key_states[pygame.K_d]:
            frame_roll -= 1

        if key_states[pygame.K_LSHIFT]:
            if player.throttle < 200:
                player.throttle += 1/3
        if key_states[pygame.K_LCTRL]:
            if player.throttle > -50:
                player.throttle -= 1/3

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

        objects = [station1, station2]
        for object in objects:
            obj_center = [object.center_x, object.center_y, object.center_z]
            new_center = rotate_point(player.get_coords(), obj_center, frame_roll, frame_pitch, frame_yaw)
            object.center_x, object.center_y, object.center_z = new_center[0], new_center[1], new_center[2]


            object.polygons = rotate_object(object, fps)
            new_polygons = []
            for polygon in object.polygons:
                new_poly = []
                for point in polygon:
                    new_poly.append(rotate_point(player.get_coords(), point, frame_roll, frame_pitch, frame_yaw))
                new_polygons.append(new_poly)
            object.polygons = new_polygons



        #station1.polygons = rotate_object(station1, fps)
        #station2.polygons = rotate_object(station2, fps)

        station1_polygons = copy.deepcopy(station1.polygons)  # Copy to edit values.
        station2_polygons = copy.deepcopy(station2.polygons)
        polygons = station1_polygons + station2_polygons

        # rotated_polygons = []
        # for polygon in polygons:
        #     rotated_poly = []
        #     for point in polygon:
        #         point = rotate_point(player.get_coords(), point, frame_roll, frame_pitch, frame_yaw)
       #print(player.roll % 360, player.pitch % 360, player.yaw % 360)
        #player.pitch += player.roll % 360 / 1
        #player.roll += frame_roll


        # Draw crosshairs.
        pygame.draw.circle(screen, (250, 250, 250), (960, 540), 3)
        # pygame.draw.circle(screen, (17, 179, 0), (10, 10), 3)
        # pygame.draw.circle(screen, (17, 179, 209), (1910, 1070), 3)
        # Object rotation animation.



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
                rendered_polygon = render_polygon(polygon, player)
                rendered_polygon.append(color_p)
                rendered_polygons.append(rendered_polygon)

        rendered_polygons = sorted(rendered_polygons, key=lambda x: x[1], reverse=True)
        for polygon in rendered_polygons:
            pygame.gfxdraw.aapolygon(screen, polygon[0],polygon[2])
            pygame.gfxdraw.filled_polygon(screen, polygon[0],polygon[2])

        screen_corner_1 = [player.loc_x - (1850 / 2), player.loc_y - (1000 / 2), screen_distance + player.loc_z]
        screen_corner_2 = [player.loc_x + (1850 / 2), player.loc_y - (1000 / 2), screen_distance + player.loc_z]
        screen_corner_3 = [player.loc_x + (1850 / 2), player.loc_y + (1000 / 2), screen_distance + player.loc_z]
        screen_corner_4 = [player.loc_x - (1850 / 2), player.loc_y + (1000 / 2), screen_distance + player.loc_z]
        corners = []

        for point in [screen_corner_1, screen_corner_2, screen_corner_3, screen_corner_4]:
            #print(point)
            # print(point)
            corners.append(
                rotate_point(player.get_coords(), point, player.roll % 360, player.pitch % 360, player.yaw % 360))

        #print(corners)
        rendered_corners = []
        for i, point in enumerate(corners):
            rendered_point = render_point(point, player)
            rendered_corners.append(rendered_point)

        # left red,    right green    toplight blue    botdark blue
        colors = [(220, 0, 0), (17, 179, 0), (17, 179, 209), (17, 79, 101)]
        for i, point in enumerate(rendered_corners):
            pygame.draw.circle(screen, colors[i], (point[0], point[1]), 3)


        # Movement and inertia calculations.
        alpha = frame_yaw % 360
        beta = frame_pitch % 360
        z = player.throttle/fps * math.cos(alpha) * math.cos(beta)
        y = player.throttle/fps * math.sin(beta)
        x = player.throttle/fps * math.sin(alpha) * math.cos(beta)
        print("current", alpha, beta, [x, y, z])
        player.direction = player.direction + np.array([x, y, z])


        #speed = np.sqrt(player.direction.dot(player.direction))
        #print("speed", speed)
        print("direction", player.direction)
        #print(player.direction)
        #player.direction = np.divide(player.direction, player.speed)

        #print(player.direction)
        player.loc_x += player.direction[0] / fps
        player.loc_y += player.direction[1] / fps
        player.loc_z += player.direction[2] / fps

        print(player.get_coords())



        pygame.display.update()
        clock.tick(fps)             # Limit framerate to 120 FPS.


game_loop()

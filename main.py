""" Main game loop."""

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
    # print(pygame.font.get_fonts())
    # Text displaying on screen.
    font_century = pygame.font.SysFont('century', 24)

    # Game objects (testing game world).
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

        speed_meter = font_century.render(f"Speed: {round(player.throttle)}", True, (255, 255, 255))
        key_restart = font_century.render("Enter: Restart", True, (255, 255, 255))
        screen.blit(speed_meter, (20, 20))
        screen.blit(key_restart, (20, 50))

        # Key inputs.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        key_states = pygame.key.get_pressed()
        frame_roll, frame_pitch, frame_yaw = 0, 0, 0
        if key_states[pygame.K_RETURN]:
            game_loop()
        if key_states[pygame.K_w]:
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

        if key_states[pygame.K_x]:
            player.throttle = 0
        if key_states[pygame.K_LSHIFT]:
            if player.throttle < 200:
                player.throttle += 1 / 3
        if key_states[pygame.K_LCTRL]:
            if player.throttle > -50:
                player.throttle -= 1 / 3

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
            # print(player.roll)
        if key_states[pygame.K_x]:
            player.roll -= 1
            # print(player.roll)


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

        station1_polygons = copy.deepcopy(station1.polygons)
        station2_polygons = copy.deepcopy(station2.polygons)
        polygons = station1_polygons + station2_polygons


        pygame.draw.circle(screen, (250, 250, 250), (960, 540), 3)  # Draw crosshairs.

        frustum_planes = calculate_frustum(player, screen_distance)
        rendered_polygons = []
        for i, polygon in enumerate(polygons):
            color_p = station1.polygon_colors[i]
            in_view = check_rendering(polygon, frustum_planes)
            if in_view:
                rendered_polygon = render_polygon(polygon, player)
                rendered_polygon.append(color_p)
                rendered_polygons.append(rendered_polygon)

        rendered_polygons = sorted(rendered_polygons, key=lambda x: x[1], reverse=True)
        for polygon in rendered_polygons:
            pygame.gfxdraw.aapolygon(screen, polygon[0], polygon[2])
            pygame.gfxdraw.filled_polygon(screen, polygon[0], polygon[2])

        player_movement(frame_yaw, frame_pitch, player, fps)
        pygame.display.update()
        clock.tick(fps)  # Limit framerate to FPS value.


game_loop()

# import buttons
# try:
#     import pygame
#     from pygame.locals import *
# except ImportError:
#     import os
#     try:
#         os.system("pip install pygame --user")
#         # noinspection PyUnresolvedReferences
#         import pygame
#         from pygame.locals import *
#     except ImportError:
#         print("Could not install pygame! Try installing it manually!")
#         from time import sleep
#         sleep(3)
#         exit()
#     else:
#         print("All libraries successfully installed!")
# print("All libraries successfully imported!")
#
# pygame.init()
# screen = pygame.display.set_mode((500, 500))
# clock = pygame.time.Clock()
# pygame.display.set_caption("Testing")
#
#
# class Test():
#     def __init__(self):
#         pass
#
#
# run = True
# while run:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             run = False
#
#     pygame.display.update()
#     clock.tick(60)
# pygame.quit()

# from typing import Tuple, Literal
# import pygame
# from base_app import BaseApp
#
#
# class MyApp(BaseApp):
#     def on_mouse_button_down(self, pos: Tuple[int, int], button_id: Literal[1, 2, 3, 4, 5]):
#         print(f"clicked at: {pos} with button: {button_id}")
#
#
# pygame.init()
# app = MyApp()
# app.run()

import pygame
from pygame.locals import*
import pymunk

screen = pygame.display.set_mode((1000, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("Pymunk Test")

space = pymunk.Space()
space.gravity = 0, 500

body = pymunk.Body(10, 10, pymunk.Body.DYNAMIC)
body.position = 50, 100

ground = pymunk.Body(10, 0, pymunk.Body.STATIC)
ground.position = 0, screen.get_height() - 50
ground_box = pymunk.Poly.create_box(ground, (screen.get_width(), 50))

poly = pymunk.Poly.create_box(body, (50, 50))
space.add(body, poly, ground, ground_box)

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                body.apply_impulse_at_local_point((0, -10000))

    space.step(1/50)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (int(body.position.x), int(body.position.y), 50, 50))
    pygame.draw.rect(screen, (255, 255, 255), (int(ground.position.x), int(ground.position.y), screen.get_width(), 50))
    pygame.display.update()
    clock.tick(60)

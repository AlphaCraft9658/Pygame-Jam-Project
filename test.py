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
from typing import Tuple, Literal
import pygame
from base_app import BaseApp


class MyApp(BaseApp):
    def on_mouse_button_down(self, pos: Tuple[int, int], button_id: Literal[1, 2, 3, 4, 5]):
        print(f"clicked at: {pos} with button: {button_id}")


pygame.init()
app = MyApp()
app.run()

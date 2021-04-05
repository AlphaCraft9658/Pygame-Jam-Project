import pygame
from pygame.locals import *
from tiles import Tile
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Generation")
    for i in range((screen.get_width() // 64) + 1):
        for n in range((screen.get_height() // 64) + 1):
            pass

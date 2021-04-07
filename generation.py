import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from tiles import Tile
from typing import List

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Generation")
    tiles_group = pygame.sprite.Group()
    tiles = []
    clock = pygame.time.Clock()
    platform = []
    print(type(platform))


def generate_platform(screen: pygame.Surface, platform: List, tiles: List, tiles_group: pygame.sprite.Group, animation_frame: List):
    for i in range((screen.get_width() // 64) + 1):
        platform.append([])
        for n in range((screen.get_height() // 64) + 1):
            if i == 9:
                for s in range((screen.get_height() // 64) + 1):
                    platform[i].append(0)
                break
            if i == 10:
                for s in range((screen.get_height() // 64) + 1):
                    platform[i].append(1)
                break
            if 9 <= n < 10:
                platform[i].append(1)
            if n >= 10:
                platform[i].append(2)
            if n < 9:
                platform[i].append(0)
    for col_i, col in enumerate(platform):
        for row_i, row in enumerate(col):
            tiles.append(Tile((col_i * 64, row_i * 64), tiles_group, platform[col_i][row_i], animation_frame))
    for i in range((screen.get_height() // 64) + 1):
        tiles.append(Tile((-64, i * 64), tiles_group, 1, animation_frame))
    print(platform)


if __name__ == '__main__':
    generate_platform(screen, platform, tiles, tiles_group, [0])
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        screen.fill((0, 0, 25))
        tiles_group.draw(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

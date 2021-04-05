import pygame
from pygame.locals import *
from tiles import Tile
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Generation")
    tiles_group = pygame.sprite.Group()
    tiles = []
    platform = []
    for i in range((screen.get_width() // 64) + 1):
        platform.append([])
        for n in range((screen.get_height() // 64) + 1):
            if n >= 8:
                platform[i].append(1)
            if n < 8:
                platform[i].append(0)
    for col_i, col in enumerate(platform):
        for row_i, row in enumerate(col):
            tiles.append(Tile((col_i * 64, row_i * 64), tiles_group, platform[col_i][row_i]))
    print(platform)

    clock = pygame.time.Clock()
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

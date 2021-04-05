import buttons
from player import Player, collision_test
from tiles import Tile
from time import time
try:
    import pygame
    from pygame.locals import *
except ImportError:
    import os
    try:
        os.system("pip install pygame --user")
        # noinspection PyUnresolvedReferences
        import pygame
        from pygame.locals import *
    except ImportError:
        print("Could not install pygame! Try installing it manually!")
        from time import sleep
        sleep(3)
        exit()
    else:
        print("All libraries successfully installed!")
from typing import Union, Tuple, Optional, Literal, List
from player import Player
print("All libraries successfully imported!")

pygame.init()
screen = pygame.display.set_mode((1000, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Jam Game")

dt = 0
last_time = time()
tiles = []
tiles_group = pygame.sprite.Group()
tiles.append(Tile((0, screen.get_height() - 20, screen.get_width(), 20), tiles_group))
tiles.append(Tile((0, 0, 50, 50), tiles_group, 1))
player = Player(tiles, tiles_group)
player_group = pygame.sprite.Group(player)

run = True
while run:
    dt = time() - last_time
    dt *= 60
    last_time = time()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.left = True
            if event.key == K_RIGHT:
                player.right = True
            if event.key == K_UP:
                player.up = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                player.left = False
            if event.key == K_RIGHT:
                player.right = False
            if event.key == K_UP:
                player.up = False
            pass

    screen.fill((0, 100, 100))
    player_group.update()
    tiles_group.update(player.rect.x, player.rect.x)
    player_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

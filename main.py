import buttons
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
from typing import Union, Tuple, Optional
print("All libraries successfully imported!")

pygame.init()
screen = pygame.display.set_mode((1000, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Jam Game")


def check_for_collisions(rect: Rect):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0, 0, 50, 50)
        self.surface = pygame.surface.Surface(screen.get_rect())
        self.xVel = 0
        self.yVel = 0
        self.left = False
        self.right = False
        self.up = False
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        self.surface.set_colorkey((0, 0, 0))

    @property
    def image(self):
        return self.surface

    def update(self):  # physics
        collisions = check_for_collisions(self.rect)
        self.rect.x += self.xVel
        for tile in collisions:
            if self.rect.right > tile.rect.left:
                self.rect.right = tile.rect.left
            elif self.rect.left < tile.rect.right:
                self.rect.left = tile.rect.right

        self.rect.y += self.yVel
        for tile in collisions:
            if self.rect.top < tile.rect.bottom:
                self.rect.top = tile.rect.bottom
            elif self.rect.bottom > tile.rect.top:
                self.rect.bottom = tile.rect.top
        if len(collisions) > 0:
            self.xVel = 0
            self.yVel = 0
        else:
            self.xVel *= 0.8
            self.yVel -= 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, rect: Rect):
        super().__init__()
        self.rect = rect
        self.surface = pygame.surface.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height))
        self.surface.set_colorkey((0, 0, 0))
        tiles_group.add(self)

    @property
    def image(self):
        return self.surface


player = Player()
player_group = pygame.sprite.Group(player)
tiles = []
tiles_group = pygame.sprite.Group()
tiles.append(Tile(Rect(0, screen.get_height() - 20, screen.get_width(), 20)))
run = True
while run:
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

    screen.fill((0, 0, 0))
    player_group.update()
    player_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

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
print("All libraries successfully imported!")

pygame.init()
screen = pygame.display.set_mode((1000, 750))
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Jam Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(0, 0, 50, 50)
        self.surface = pygame.surface.Surface((50, 50))
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        self.surface.set_colorkey((0, 0, 0))

    @property
    def image(self):
        return self.surface

    def update(self):  # physics
        pass


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

    screen.fill((0, 0, 0))
    player_group.update()
    player_group.draw(screen)
    tiles_group.draw(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

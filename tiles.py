from time import time
import pygame
from pygame.locals import *
from typing import Union, Tuple, Optional, Literal, List
from spritesheet import Spritesheet


class Tile(pygame.sprite.Sprite):
    def __init__(self, rect: Union[Rect, Tuple[int, int, int, int]], tiles_group: pygame.sprite.Group, texture: int = 0):
        super().__init__()
        self.rect = Rect(rect)
        self.deafult_pos = self.rect.x, self.rect.y
        self.surface = pygame.surface.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height))
        self.surface.set_colorkey((0, 0, 0))
        tiles_group.add(self)
        self.spritesheet = Spritesheet("img/spritesheet.png", 100, 100)
        self.texture = self.spritesheet.get_texture(texture)

    @property
    def image(self):
        return self.texture

    def update(self, x: int = 0, y: int = 0):
        self.rect.move_ip(self.deafult_pos[0] + x, self.deafult_pos[1] + y)

from time import time
import pygame
from pygame.locals import *
from typing import Union, Tuple, Optional, Literal, List
from spritesheet import Spritesheet


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: Union[pygame.Vector2, Tuple[int, int]], tiles_group: pygame.sprite.Group, texture: int = 0, metal_frame: List = [0]):
        super().__init__()
        self.rect = Rect(pos[0], pos[1], 64, 64)
        # self.default_pos = self.rect.x, self.rect.y
        self.surface = pygame.surface.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height))
        self.surface.set_colorkey((0, 0, 0))
        tiles_group.add(self)
        self.metal_animation_frame = metal_frame
        self.spritesheet = Spritesheet("img/spritesheet.png", 100, 100)
        self.texture_index = texture
        if texture == 1:
            self.animation = True
        else:
            self.animation = False
        self.texture = self.spritesheet.get_texture(texture)

    @property
    def image(self):
        return self.texture

    def update(self, x: int = 0, y: int = 0):
        self.texture = self.spritesheet.get_texture(self.texture_index, self.metal_animation_frame)
        # self.rect.x = self.default_pos[0] + x
        # self.rect.y = self.default_pos[1] + y

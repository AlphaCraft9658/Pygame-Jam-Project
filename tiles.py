from time import time
from enum import Enum
import pygame
from pygame.locals import *
from typing import Union, Tuple, Optional, Literal, List
from spritesheet import Spritesheet


class TileActionTypes(Enum):
    none = 0
    wall = 1
    bounce = 2
    kill = 3
    speed = 4


class TileInfo:
    def __init__(self, action: TileActionTypes, bounce_diff: float = 1, speed_applier: int = 1):
        self.speed_applier = speed_applier
        self.bounce_diff = bounce_diff
        self.action = action


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: Union[pygame.Vector2, Tuple[int, int]], texture: int = 0,
                 tile_info: Optional[TileInfo] = None):
        super().__init__()
        pos = (pos.x, pos.y) if isinstance(pos, pygame.Vector2) else pos
        self.tile_info = tile_info if tile_info else TileInfo(TileActionTypes.none)
        self.rect = Rect(pos[0], pos[1], 64, 64)
        # self.default_pos = self.rect.x, self.rect.y
        self.surface = pygame.surface.Surface((self.rect.width, self.rect.height))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.rect.width, self.rect.height))
        self.surface.set_colorkey((0, 0, 0))
        self.animation_frame = 0
        self.sprite_sheet = Spritesheet("img/spritesheet.png", 100, 100)
        self.texture_index = texture
        self.texture = self.sprite_sheet.get_texture(texture)

    @property
    def image(self):
        return self.texture

    def update(self, x: int = 0, y: int = 0):
        self.texture = self.sprite_sheet.get_texture(self.texture_index, self.animation_frame)
        # self.rect.x = self.default_pos[0] + x
        # self.rect.y = self.default_pos[1] + y

    def next_frame(self):
        self.animation_frame += 1
        if self.animation_frame >= len(self.sprite_sheet.get_frames(self.texture_index)):
            self.animation_frame = 0

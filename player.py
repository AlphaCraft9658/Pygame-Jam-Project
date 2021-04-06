from time import time
from tiles import Tile
import pygame
from pygame.locals import *
from typing import Union, Tuple, Optional, Literal, List


def collision_test(rect: Union[Rect, Tuple[int, int, int, int]], tiles_: List[Tile], mode: Literal[1, 2] = 1):
    if mode == 1:
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        collisions = rect.collidelistall(tiles_)
        res_list = list(map(tiles_.__getitem__, collisions))
        return res_list
    elif mode == 2:
        return rect.collidelistall(tiles_)


class Player(pygame.sprite.Sprite):
    def __init__(self, tiles: List[Tile], tiles_group: pygame.sprite.Group):
        super().__init__()
        self.tiles = tiles
        self.rect = Rect(0, 0, 50, 50)
        self.collide_rect = self.rect.copy()
        self.surface = pygame.Surface((50, 50))
        self.vel = [0, 0]
        self.left = False
        self.right = False
        self.up = False
        self.on_ground = False

        # ########## collide info

        self.c_up = False
        self.c_left = False
        self.c_right = False
        self.c_down = False
        self.stuck = False

        # ########## collide info end

        # ########## collide mode
        self.collide_mode = 1
        # ########## collide mode end

        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        self.surface.set_colorkey((0, 0, 0))

    @property
    def image(self):
        return self.surface

    def move_until_collide(self, x: int, y: int):
        vec = pygame.Vector2(x, y)
        v_s = vec / 100
        c_v = pygame.Vector2(0, 0)
        rec = self.rect.copy()
        c = []
        for _ in range(100):
            c = collision_test(rec, self.tiles)
            if len(c) != 0:
                break
            c_v += v_s
            rec.x = c_v.x
            rec.y = c_v.y
        self.rect.x = rec.x
        self.rect.y = rec.y
        return c

    def update_vel(self):
        self.vel[0] *= .9
        self.vel[1] += 1
        vel_x = self.vel[0]
        vel_y = self.vel[1]
        if self.collide_mode == 1:
            # if self.c_down:
            #     vel_y = 0
            pass

        self.rect.move_ip(vel_x, vel_y)

    def collide(self) -> bool:
        return collision_test(self.rect, self.tiles)

    def collect_collisions(self):
        if self.collide_mode == 1:
            self.stuck = self.collide()
            self.rect.move_ip(0, 1)
            self.c_down = self.collide()
            self.rect.move_ip(0, -2)
            self.c_up = self.collide()
            self.rect.move_ip(1, 1)
            self.c_right = self.collide()
            self.rect.move_ip(-2, 0)
            self.c_left = self.collide()
            self.rect.move_ip(1, 0)

    def update(self):  # physics
        if self.right:
            self.vel[0] += 1
        if self.left:
            self.vel[0] -= 1
        if self.up and self.on_ground:
            self.vel[1] = -12
            self.on_ground = False

        self.update_vel()
        self.collect_collisions()

        # self.vel[1] += .2
        # collisions = self.collide()
        # self.rect.x += self.vel[0]
        # for tile in collisions:
        #     if self.vel[0] > 0:
        #         self.rect.right = tile.rect.left
        #     if self.vel[0] < 0:
        #         self.rect.left = tile.rect.right
        # self.rect.y += self.vel[1]
        # for tile in collisions:
        #     if self.vel[1] > 0:
        #         self.rect.bottom = tile.rect.top
        #         self.vel[1] = 1
        #     if self.vel[1] < 0:
        #         self.rect.top = tile.rect.bottom
        #         self.vel[1] = 1

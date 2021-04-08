from time import time
from tiles import Tile, TileActionTypes
import pygame
from pygame.locals import *
from typing import Union, Tuple, Optional, Literal, List


def collision_test(rect: Union[Rect, Tuple[int, int, int, int]], tiles_: List[Tile], mode: Literal[1, 2, 3] = 1):
    if mode == 1:
        if not isinstance(rect, Rect):
            rect = Rect(rect)
        collisions = rect.collidelistall(tiles_)
        res_list = list(map(tiles_.__getitem__, collisions))
        return res_list
    elif mode == 2:
        return rect.collidelistall(tiles_)
    elif mode == 3:
        collides = False
        for tile in tiles_:
            if rect.colliderect(tile.rect) and tile.texture_index != 0:
                collides = True
        return collides


class Player(pygame.sprite.Sprite):
    def __init__(self, tiles_group: pygame.sprite.Group, screen_x: int, screen_y: int,
                 pos: Optional[pygame.Vector2] = None, page: Optional[List[int]] = None):
        super().__init__()
        self.pos: pygame.Vector2 = pos if pos else pygame.Vector2(0, 0)
        self.tiles_group = tiles_group
        self.rect = Rect(0, 0, 50, 50)
        self.surface = pygame.Surface((50, 50))
        self.vel = [0, 0]
        self.left = False
        self.right = False
        self.up = False
        self.on_ground = False
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.spawn_page = page.copy() if page else [0, 0]
        self.page = page.copy() if page else [0, 0]

        # ########## collide info

        self.c_up = False
        self.c_left = False
        self.c_right = False
        self.c_down = False
        self.stuck = False
        self.max_vel = 0.025
        self.bounced_x = False
        self.bounced_y = False
        self.teleporting = False

        # ########## collide info end

        # ########## collide mode
        self.collide_mode = 1
        # ########## collide mode end

        # ########## setup
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        self.surface.set_colorkey((0, 0, 0))
        self.respawn()
        # ########## setup end

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
            # noinspection PyTypeChecker
            c = collision_test(rec, self.tiles_group.sprites())
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
        self.vel[1] += .5

        self.rect.move_ip(self.vel[0]/2, self.vel[1]/2)
        if self.colliding():
            slope = 0
            while slope < 15 and self.colliding():
                self.rect.move_ip(0, -1)
                slope += 1
            if slope == 15:
                self.on_ground = False
                self.rect.move_ip(-self.vel[0], 15)
                self.vel[0] = 0
                if self.right:
                    self.right = False
                if self.left:
                    self.left = False
            else:
                self.vel[1] = 0
                self.on_ground = True

        self.rect.move_ip(self.vel[0] / 2, self.vel[1] / 2)
        if self.colliding():
            slope = 0
            while slope < 15 and self.colliding():
                self.rect.move_ip(0, -1)
                slope += 1
            if slope == 15:
                self.on_ground = False
                self.rect.move_ip(-self.vel[0], 15)
                self.vel[0] = 0
                if self.right:
                    self.right = False
                if self.left:
                    self.left = False
            else:
                self.vel[1] = 0
                self.on_ground = True

        # self.vel[0] -= self.vel[0] * self.max_vel
        self.vel[1] -= self.vel[1] * self.max_vel

    def colliding(self):
        # noinspection PyTypeChecker
        c = collision_test(self.rect, self.tiles_group.sprites())
        for e in c:
            if e.tile_info.action == TileActionTypes.wall:
                return True

    def action_collide(self):
        # noinspection PyTypeChecker
        c = collision_test(self.rect, self.tiles_group.sprites())
        bcd = False
        for e in c:
            if e.tile_info.action == TileActionTypes.kill:
                self.respawn()
                break
            elif e.tile_info.action == TileActionTypes.speed:
                self.vel[0] *= e.tile_info.speed_applier
                self.vel[1] *= e.tile_info.speed_applier
            elif e.tile_info.action == TileActionTypes.bounce:
                bcd = True
                if self.rect.x + 25 < e.rect.x or self.rect.x > e.rect.x + 32:
                    if not self.bounced_x:
                        self.bounced_x = True
                        self.vel[0] *= -e.tile_info.bounce_diff
                if self.rect.y + 25 < e.rect.y or self.rect.y > e.rect.y + 32:
                    if not self.bounced_y:
                        self.bounced_y = True
                        self.vel[1] *= -e.tile_info.bounce_diff

        if not bcd:
            self.bounced_x = False
            self.bounced_y = False

    def update(self):  # physics
        self.teleporting = False
        if self.right:
            self.vel[0] += 1
        if self.left:
            self.vel[0] -= 1
        if self.up and self.on_ground:
            self.vel[1] = -20
            self.on_ground = False
        if not self.on_ground:
            self.up = False

        self.update_vel()
        self.tp_check()
        self.action_collide()

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
    def tp_check(self):
        if self.rect.x <= 10:
            self.tp_right()
        elif self.rect.x > self.screen_x:
            self.tp_left()
        if self.rect.y <= 10:
            self.tp_down()
        elif self.rect.y > self.screen_y:
            self.tp_up()

    def tp_right(self):
        self.page[0] -= 1
        self.rect.x = self.screen_x
        self.teleporting = True

    def tp_left(self):
        self.page[0] += 1
        self.rect.x = 11
        self.teleporting = True

    def tp_up(self):
        self.page[1] -= 1
        self.rect.y = 11
        self.teleporting = True

    def tp_down(self):
        self.page[1] += 1
        self.rect.y = self.screen_y
        self.teleporting = True

    def respawn(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.vel[0] = 0
        self.vel[1] = 0
        self.page = self.spawn_page.copy()

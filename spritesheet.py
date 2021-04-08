import pygame
from pygame.locals import *
import json
from typing import List, Optional

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Spritesheet")


class Spritesheet:
    def __init__(self, filename, dw, dh):
        self.filename = filename
        self.sheet = pygame.image.load(filename)
        self.sheet = pygame.transform.scale(self.sheet, (self.sheet.get_width() * 2, self.sheet.get_height() * 2))
        self.dw = dw
        self.dh = dh
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_texture(self, texture: int, frame: int = 0):
        # if texture == 1:
        #     x, y, w, h = self.data["1"][f"{frame}"]["x"], self.data["1"][f"{frame}"]["y"], \
        #                  self.data["1"][f"{frame}"]["w"], self.data["1"][f"{frame}"]["h"]
        # else:
        #     x, y, w, h = self.data[f"{texture}"]["x"], self.data[f"{texture}"]["y"], self.data[f"{texture}"]["w"], \
        #                  self.data[f"{texture}"]["h"]
        x, y, w, h = self.data[f"{texture}"][f"{frame}"]["x"], self.data[f"{texture}"][f"{frame}"]["y"],\
                     self.data[f"{texture}"][f"{frame}"]["w"], self.data[f"{texture}"][f"{frame}"]["h"]
        texture = pygame.Surface((w, h))
        texture.set_colorkey((255, 255, 255))
        texture.blit(self.sheet, (0, 0), Rect(x, y, w, h))
        return texture

    def get_frames(self, texture: int):
        return self.data[f"{texture}"]

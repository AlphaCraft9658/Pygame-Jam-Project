import pygame
from pygame.locals import *
import json


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

    def get_texture(self, texture_):
        x, y, w, h = self.data[f"{texture_}"]["x"], self.data[f"{texture_}"]["y"], self.data[f"{texture_}"]["w"], self.data[f"{texture_}"]["h"]
        texture = pygame.Surface((w, h)).convert()
        texture.set_colorkey((255, 255, 255))
        texture.blit(self.sheet, (0, 0), Rect(x, y, w, h))
        return texture

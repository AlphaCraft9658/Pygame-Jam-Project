import random
import pygame
from pygame.locals import *
from spritesheet import Spritesheet
from tiles import Tile, TileActionTypes, TileInfo
from typing import List, Literal, Dict

SEED = random.randint(0, 1000)
print(SEED)

SPAWN_PAGE = [[0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1]]

saved_pages: Dict[str, List[List[int]]] = {}


# noinspection PyShadowingNames
def generate_sprites(platform: List[List[int]], tiles_group: pygame.sprite.Group):
    tiles_group.empty()
    for x in range(len(platform)):
        for y in range(len(platform[x])):
            t = get_tile(platform[x][y], x * 64, y * 64)
            if t:
                tiles_group.add(t)


def generate_empty():
    return [[0]*12]*16


def generate_page(page: List[int]):
    if f"{page[0]};{page[1]}" in saved_pages:
        return saved_pages[f"{page[0]};{page[1]}"]
    elif page == [0, 0]:
        ret = SPAWN_PAGE
    else:
        ret = real_generate(page)

    saved_pages[f"{page[0]};{page[1]}"] = ret
    return ret


def set_seed(page: List[int]):
    if page[0] == 0:
        p1 = 1
    else:
        p1 = page[0]
    if page[1] == 0:
        p2 = 1
    else:
        p2 = page[1]

    random.seed((((p1 + p2) * SEED) % (p1**2))//(p2**2))


def real_generate(page: List[int]):
    lst = generate_empty()
    set_seed(page)
    lst = random_spawn(lst, 1, 5, 6)
    lst = random_spawn(lst, 2, 5, 6)

    # if page[0] >= 0:
    #     p1 = page[0] + 1
    # else:
    #     p1 = page[0]
    # if page[1] >= 0:
    #     p2 = page[1] + 1
    # else:
    #     p2 = page[1]
    # print((((p1 + p2) * SEED) % (p1 ** 2)) // (p2 ** 2))
    return lst


def random_spawn(lst: List[List[int]], block_id: int, mini: int, maxi: int):
    times = random.randint(mini, maxi)
    for c in range(times):
        x = random.randint(0, 15)
        y = random.randint(0, 11)
        # print(x, y)
        lst[x][y] = block_id
    return lst


# noinspection PyShadowingNames,PyUnusedLocal
def generate(page: List[int], tiles_group: pygame.sprite.Group, rem_x: int = -1, rem_y: int = -1):
    p = generate_page(page).copy()
    generate_sprites(p, tiles_group)


def get_tile(tile_id: int, x_pos: int, y_pos: int):
    if tile_id == 1:
        return Tile((x_pos, y_pos), 2, TileInfo(TileActionTypes.wall))
    elif tile_id == 2:
        return Tile((x_pos, y_pos), 1, TileInfo(TileActionTypes.wall))
    elif tile_id == 3:
        return Tile((x_pos, y_pos), 1, TileInfo(TileActionTypes.kill))
    elif tile_id == 4:
        return Tile((x_pos, y_pos), 1, TileInfo(TileActionTypes.speed, speed_applier=2))
    elif tile_id == 5:
        return Tile((x_pos, y_pos), 1, TileInfo(TileActionTypes.bounce, bounce_diff=0.9))
    return None


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("Generation")
    tiles_group = pygame.sprite.Group()
    tiles = []
    clock = pygame.time.Clock()
    platform = []
    print(type(platform))
    generate_platform(screen, platform, tiles, tiles_group)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        screen.fill((0, 0, 25))
        tiles_group.draw(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

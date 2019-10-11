from os import path
import tcod

COLOR_PLAYER = tcod.Color(200, 0, 0)
COLOR_DARK_WALL = tcod.Color(50, 50, 150)
COLOR_DARK_GROUND = tcod.Color(50, 50, 150)
COLOR_LIGHT_WALL = tcod.Color(130, 110, 50)
COLOR_LIGHT_GROUND = tcod.Color(200, 180, 50)
COLOR_EXPLORED_WALL = tcod.Color(0, 0, 150)
COLOR_EXPLORED_GROUND = tcod.Color(100, 100, 150)

FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 4

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 50

MAX_ROOM_MONSTERS = 3

MONSTER_DIR = path.join(path.dirname(__file__), 'monsters/')



class Config:
    def __init__(self):
        self.colors = {
            'COLOR_DARK_WALL': COLOR_DARK_WALL,
            'COLOR_DARK_GROUND': COLOR_DARK_GROUND,
            'COLOR_LIGHT_WALL': COLOR_LIGHT_WALL,
            'COLOR_LIGHT_GROUND': COLOR_LIGHT_GROUND,
            'COLOR_EXPLORED_WALL': COLOR_EXPLORED_WALL,
            'COLOR_EXPLORED_GROUND': COLOR_EXPLORED_GROUND,
            'COLOR_PLAYER': COLOR_PLAYER
        }

        self.fov = {
            'FOV_ALGO': FOV_ALGO,
            'FOV_LIGHT_WALLS': FOV_LIGHT_WALLS,
            'TORCH_RADIUS': TORCH_RADIUS
        }

        self.size = {
            'SCREEN_WIDTH': SCREEN_WIDTH,
            'SCREEN_HEIGHT': SCREEN_HEIGHT,
            'MAP_WIDTH': MAP_WIDTH,
            'MAP_HEIGHT': MAP_HEIGHT
        }

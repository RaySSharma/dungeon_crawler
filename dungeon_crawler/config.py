from os import path
import tcod

# Game
DIAGONAL = True

# Colors
COLOR_PLAYER = tcod.Color(200, 0, 0)
COLOR_DARK_WALL = tcod.darkest_purple
COLOR_DARK_GROUND = tcod.darkest_purple
COLOR_LIGHT_WALL = (205, 150, 0)
COLOR_LIGHT_GROUND = (150, 110, 0)
COLOR_HALFLIGHT_WALL = (102, 75, 0)
COLOR_HALFLIGHT_GROUND = (77, 56, 0)
COLOR_EXPLORED_WALL = tcod.darkest_gray
COLOR_EXPLORED_GROUND = tcod.darker_gray

COLOR_DEATH = tcod.dark_red
COLOR_MONSTERS = tcod.red

COLOR_HP_FG = tcod.darker_red
COLOR_HP_BG = tcod.darkest_red
COLOR_MANA_FG = tcod.darker_blue
COLOR_MANA_BG = tcod.darkest_blue

COLOR_PANEL_BG = tcod.darker_grey
COLOR_MESSAGE_BG = tcod.darkest_amber

# Lighting
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5
HALFTORCH_RADIUS = TORCH_RADIUS + 1

# Screen / Resolution
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

# GUI
BAR_WIDTH = 20
PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MAX_ROOM_MONSTERS = 3

MSG_X = BAR_WIDTH + 3
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 10
MSG_HEIGHT = PANEL_HEIGHT - 1

# Monsters
MONSTER_DIR = path.join(path.dirname(__file__), 'monsters/')

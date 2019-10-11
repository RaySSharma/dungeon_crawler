import numpy as np

import tcod
import tcod.map

from dungeon_crawler import config
from dungeon_crawler.generate_room import Dungeon
from dungeon_crawler.characters import Character

default_character = {
    'name': 'Ray Sharma',
    'Species': 'Human',
    'Specialization': 'Adventurer',
    'level': 1
}

default_stats = {
    'HP': 10,
    'STR': 10,
    'DEX': 10,
    'CON': 10,
    'INT': 10,
    'WIS': 10
}

default_equipment = ['Short Sword']


class GameInstance:
    def __init__(self, console, root_console, screen_size, map_size,
                 game_state, player_action):
        super().__init__()
        self.console = console
        self.root_console = root_console
        self.screen_size = screen_size
        self.map_size = map_size
        self.dungeon = Dungeon(self.console, map_size)
        self.player = Character(console, self.screen_size[0] / 2,
                                self.screen_size[1] / 2,
                                color=config.COLOR_PLAYER, char='@',
                                blocks=True, character=default_character,
                                stats=default_stats,
                                equipment=default_equipment)
        self.victory = False
        self.failure = False
        self.objects = self.populate_objects()
        self.walkable = self.dungeon.dungeon.walkable
        self.player_action = player_action
        self.game_state = game_state

    def handle_keys(self):
        key = tcod.console_wait_for_keypress(True)
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        elif key.vk == tcod.KEY_ESCAPE:
            return 'exit'

        if self.game_state == 'playing':
            if key.vk == tcod.KEY_UP:
                if self.walkable[self.player.x + 0][self.player.y - 1]:
                    self.player.move_or_attack(0, -1, self.objects)
            elif key.vk == tcod.KEY_DOWN:
                if self.walkable[self.player.x + 0][self.player.y + 1]:
                    self.player.move_or_attack(0, 1, self.objects)
            elif key.vk == tcod.KEY_LEFT:
                if self.walkable[self.player.x - 1][self.player.y + 0]:
                    self.player.move_or_attack(-1, 0, self.objects)
            elif key.vk == tcod.KEY_RIGHT:
                if self.walkable[self.player.x + 1][self.player.y + 0]:
                    self.player.move_or_attack(1, 0, self.objects)
            else:
                return 'didnt-take-turn'

    def render(self):
        visible = tcod.map.compute_fov(self.dungeon.dungeon.transparent,
                                       pov=(self.player.x, self.player.y),
                                       radius=config.TORCH_RADIUS,
                                       light_walls=config.FOV_LIGHT_WALLS,
                                       algorithm=config.FOV_ALGO)

        self.dungeon.explored |= visible

        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                if not visible[x][y]:
                    if self.dungeon.explored[x][y]:
                        color_wall = config.COLOR_EXPLORED_WALL
                        color_ground = config.COLOR_EXPLORED_GROUND
                    else:
                        color_wall = config.COLOR_DARK_WALL
                        color_ground = config.COLOR_DARK_GROUND
                else:
                    color_wall = config.COLOR_LIGHT_WALL
                    color_ground = config.COLOR_LIGHT_GROUND

                wall = self.dungeon.dungeon.transparent[x][y]
                if wall:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_wall,
                                                     tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_ground,
                                                     tcod.BKGND_SET)

        for obj in self.objects:
            obj.draw()

        self.console.blit(self.root_console, 0, 0, 0, 0, self.screen_size[0],
                          self.screen_size[1])

    def clear(self):
        for obj in self.objects:
            obj.clear()

    def populate_objects(self):
        objects = [self.player]

        for room in self.dungeon.rooms:
            objects.append(room.encounters)
        return np.hstack(objects)

    def detect_collisions(self):
        walkable = self.dungeon.dungeon.walkable.copy()
        for obj in self.objects:
            if obj.blocks:
                walkable[obj.x][obj.y] = False
        self.walkable = walkable

    def object_actions(self):
        if self.game_state == 'playing' and self.player_action != 'didnt-take-turn':
            for obj in self.objects:
                if object != self.player:
                    print('The ' + obj.character['name'] + ' growls!')

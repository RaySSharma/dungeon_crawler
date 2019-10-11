import json
from os import listdir
import numpy as np
import tcod

from dungeon_crawler import config

class Character:
    def __init__(self, console, x, y, color=(100, 0, 0), char='@', blocks=False, character=None, stats=None, equipment=None):
        self.console = console
        self.character = character
        self.stats = stats
        self.equipment = equipment
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.char = ord(char)
        self.blocks = blocks

    def draw(self):
        self.console.default_fg = self.color
        self.console.put_char(self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        self.console.put_char(self.x, self.y, ord(' '), tcod.BKGND_NONE)

    def move_or_attack(self, dx, dy, objects):

        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = None
        for obj in objects:
            if obj.x == x and obj.y == y:
                target = obj
                break
        # attack if target found, move otherwise
        if target is not None:
            print('The ' + target.character['name'] + ' laughs at your puny efforts to attack him!')

        else:
            self.x += dx
            self.y += dy


class Monster:
    def __init__(self, console, x, y, color=(100, 0, 0), char='o', blocks=True):
        self.console = console
        self.monster = self._generate()
        self.character = self.monster['character']
        self.stats = self.monster['stats']
        self.equipment = self.monster['equipment']
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.char = ord(char)
        self.blocks = blocks

    def _generate(self):
        monster_type = config.MONSTER_DIR + np.random.choice(listdir(config.MONSTER_DIR))
        with open(monster_type, "r") as read_file:
            monsters_dict = json.load(read_file)
        return self._choose_monster(monsters_dict)

    @staticmethod
    def _choose_monster(monsters_dict):
        monster_choice = np.random.choice(list(monsters_dict))
        return monsters_dict[monster_choice]

    def _vary_stats(self, scale=1):
        for stat in self.stats:
            self.stats[stat] = int(np.random.normal(loc=self.stats[stat], scale=scale))

    def draw(self):
        self.console.default_fg = self.color
        self.console.put_char(self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        self.console.put_char(self.x, self.y, ord(' '), tcod.BKGND_NONE)
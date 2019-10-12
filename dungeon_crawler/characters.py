import json
from os import listdir
import numpy as np
import tcod

from dungeon_crawler import config


class Character:
    def __init__(self, x, y, color=(100, 0, 0), combatant=None,
                 char='@', blocks=False, character=None, stats=None,
                 equipment=None, ai=None, state='alive'):
        self.owner = None
        self.character = character
        self.stats = stats
        self.equipment = equipment
        self.name = self.character['name']
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.char = ord(char)
        self.blocks = blocks
        self.state = state

        self.combatant = combatant
        if self.combatant:  # let the fighter component know who owns it
            self.combatant.owner = self

        self.ai = ai
        if self.ai:  # let the AI component know who owns it
            self.ai.owner = self

    def draw(self):
        self.owner.console.default_fg = self.color
        self.owner.console.put_char(self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        self.owner.console.put_char(self.x, self.y, ord(' '), tcod.BKGND_NONE)

    def move_or_attack(self, dx, dy):
        target = None
        for obj in self.owner.owner.objects:
            if obj.combatant and (obj.x == self.x +
                                  dx) and (obj.y == self.y + dy):
                target = obj
                break
        if target is not None:
            self.combatant.attack(target)
        elif self.owner.owner.walkable[self.x + dx][self.y + dy]:
            self.x += dx
            self.y += dy
        else:
            pass

    def death(self):
        self.owner.owner.print(self.name, 'died!')
        self.state = 'dead'
        self.char = ord('%')
        self.color = config.DEATH_COLOR


class Monster:
    def __init__(self, x, y, color=(100, 0, 0), combatant=None,
                 char='o', blocks=True, ai=None, state='alive'):
        self.owner = None
        self.monster = self._generate()
        self.character = self.monster['character']
        self.stats = self.monster['stats']
        self.equipment = self.monster['equipment']
        self.name = self.character['name']
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.char = ord(char)
        self.blocks = blocks
        self.state = state

        self.combatant = combatant
        if self.combatant:
            self.combatant.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def _generate(self):
        monster_type = config.MONSTER_DIR + np.random.choice(
            listdir(config.MONSTER_DIR))
        with open(monster_type, "r") as read_file:
            monsters_dict = json.load(read_file)
        return self._choose_monster(monsters_dict)

    @staticmethod
    def _choose_monster(monsters_dict):
        monster_choice = np.random.choice(list(monsters_dict))
        return monsters_dict[monster_choice]

    def _vary_stats(self, scale=1):
        for stat in self.stats:
            self.stats[stat] = int(
                np.random.normal(loc=self.stats[stat], scale=scale))

    def draw(self):
        self.owner.owner.console.default_fg = self.color
        self.owner.owner.console.put_char(self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        self.owner.owner.console.put_char(self.x, self.y, ord(' '), tcod.BKGND_NONE)

    def move_towards(self, target_x, target_y):
        # vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = np.linalg.norm([dx, dy])

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return np.linalg.norm([dx, dy])

    def move(self, dx, dy):
        if self.owner.owner.walkable[self.x + dx][self.y + dy]:
            self.x += dx
            self.y += dy

    def death(self):
        self.owner.print(self.name, 'is dead!')
        self.char = ord('%')
        self.color = config.DEATH_COLOR
        self.blocks = False
        self.combatant = None
        self.ai = None
        self.name = 'remains of ' + self.name
        self.state = 'dead'

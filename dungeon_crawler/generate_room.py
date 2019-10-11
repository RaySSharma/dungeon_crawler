import numpy as np
import tcod.bsp
import tcod.map

from dungeon_crawler import config
from dungeon_crawler import characters


class Dungeon:
    def __init__(self, console, map_size):
        self.console = console
        self.map_size = map_size
        self.dungeon = self._generate_field()
        self.rooms = self._generate_tree_rooms()
        self.explored = np.zeros(self.dungeon.transparent.shape, dtype=bool, order='F')

    def _generate_field(self):
        return tcod.map.Map(width=self.map_size[0], height=self.map_size[1],
                            order='F')

    def _generate_tree_rooms(self, depth=5, min_width=3, min_height=3,
                             max_horizontal_ratio=1.5, max_vertical_ratio=1.5):
        rooms = []
        bsp = tcod.bsp.BSP(x=0, y=0, width=self.map_size[0],
                           height=self.map_size[1])
        bsp.split_recursive(depth=depth, min_width=min_width,
                            min_height=min_height,
                            max_horizontal_ratio=max_horizontal_ratio,
                            max_vertical_ratio=max_vertical_ratio)
        for node in bsp.pre_order():
            if node.children:
                node1, node2 = node.children
                Door(self.dungeon, node, node1, node2)
            else:
                rooms += [Room(self.console, self.dungeon, node, self.map_size)]
        return rooms


class Door:
    def __init__(self, parent_dungeon, parent_node, node1, node2):
        self.parent_dungeon = parent_dungeon
        self.parent_node = parent_node
        self.node1 = node1
        self.node2 = node2
        self.x_cen1, self.y_cen1 = self._find_node_center(self.node1)
        self.x_cen2, self.y_cen2 = self._find_node_center(self.node2)
        self._generate()

    def _generate(self):
        if self.parent_node.horizontal:
            self.create_v_tunnel()
        else:
            self.create_h_tunnel()

    @staticmethod
    def _find_node_center(node):
        x_cen = (2 * node.x + node.w) / 2
        y_cen = (2 * node.y + node.h) / 2
        return int(x_cen), int(y_cen)

    def create_h_tunnel(self):
        for x in range(min(self.x_cen1, self.x_cen2),
                       max(self.x_cen1, self.x_cen2) + 1):
            self.parent_dungeon.walkable[x][self.y_cen1] = True
            self.parent_dungeon.transparent[x][self.y_cen1] = True

    def create_v_tunnel(self):
        for y in range(min(self.y_cen1, self.y_cen2),
                       max(self.y_cen1, self.y_cen2) + 1):
            self.parent_dungeon.walkable[self.x_cen1][y] = True
            self.parent_dungeon.transparent[self.x_cen1][y] = True


class Room:
    def __init__(self, console, parent_dungeon, node, map_size):
        self.console = console
        self.parent_dungeon = parent_dungeon
        self.x1 = node.x
        self.y1 = node.y
        self.x2 = node.x + node.w
        self.y2 = node.y + node.h
        self.map_size = map_size
        self._generate_room()
        self.encounters = self._generate_encounters()

    def _generate_room(self):
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                self.parent_dungeon.walkable[x][y] = True
                self.parent_dungeon.transparent[x][y] = True

    def _generate_encounters(self):
        num_monsters = np.random.randint(0, config.MAX_ROOM_MONSTERS)
        monsters, monster_coords = [], []
        for i in range(num_monsters):
            # choose random spot for this monster
            while True:
                x = np.random.randint(self.x1, self.x2)
                y = np.random.randint(self.y1, self.y2)
                if self.parent_dungeon.walkable[x][y] and (x, y) not in monster_coords:
                    monster_coords.append((x, y))
                    break
            monster = characters.Monster(self.console, x, y, color=tcod.darker_green, char='T', blocks=True)
            monsters.append(monster)
        return monsters


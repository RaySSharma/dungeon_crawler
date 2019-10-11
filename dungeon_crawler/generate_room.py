import numpy as np
import tcod.bsp
import tcod.map

from dungeon_crawler import AI, combat, config, characters


class Dungeon:
    def __init__(self, game, console, map_size):
        self.game = game
        self.console = console
        self.map_size = map_size
        self.dungeon = self._generate_map()
        self.rooms = self._generate_tree_rooms()
        self.explored = self.dungeon.fov
        self.fov = self.dungeon.fov
        self.encounters = self._generate_encounters()

    def _generate_map(self):
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
                rooms += [
                    Room(self.console, self.dungeon, node, self.map_size)
                ]
        self._generate_boundary()
        return rooms

    def _generate_boundary(self):
        self.dungeon.walkable[:, [0, -1]] = False
        self.dungeon.walkable[[0, -1], :] = False
        self.dungeon.transparent[:, [0, -1]] = False
        self.dungeon.transparent[[0, -1], :] = False

    def _generate_encounters(self):
        monsters, monster_coords = [], []
        for room in self.rooms:
            num_monsters = np.random.randint(0, config.MAX_ROOM_MONSTERS)
            for i in range(num_monsters):
                while True:
                    x = np.random.randint(room.x1, room.x2)
                    y = np.random.randint(room.y1, room.y2)
                    if self.dungeon.walkable[x][y] and (
                            x, y) not in monster_coords:
                        monster_coords.append((x, y))
                        break

                ai = AI.BasicMonster(self.game, self.fov)
                combatant = combat.BasicCombat(hp=30, defense=2, power=5)
                monster = characters.Monster(self.console, x, y,
                                             color=tcod.red,
                                             combatant=combatant,
                                             char='T', blocks=True, ai=ai)
                monsters.append(monster)
        return monsters


class Door:
    def __init__(self, dungeon, parent_node, node1, node2):
        self.dungeon = dungeon
        self.parent_node = parent_node
        self.node1 = node1
        self.node2 = node2
        self.x_cen1, self.y_cen1 = self._find_node_center(self.node1)
        self.x_cen2, self.y_cen2 = self._find_node_center(self.node2)
        self._generate_tunnel()

    def _generate_tunnel(self):
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
            self.dungeon.walkable[x][self.y_cen1] = True
            self.dungeon.transparent[x][self.y_cen1] = True

    def create_v_tunnel(self):
        for y in range(min(self.y_cen1, self.y_cen2),
                       max(self.y_cen1, self.y_cen2) + 1):
            self.dungeon.walkable[self.x_cen1][y] = True
            self.dungeon.transparent[self.x_cen1][y] = True


class Room:
    def __init__(self, console, dungeon, node, map_size):
        self.console = console
        self.dungeon = dungeon
        self.x1 = node.x
        self.y1 = node.y
        self.x2 = node.x + node.w

        self.y2 = node.y + node.h
        self.map_size = map_size
        self._generate_room()

    def _generate_room(self):
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                self.dungeon.walkable[x][y] = True
                self.dungeon.transparent[x][y] = True

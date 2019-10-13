import numpy as np
import tcod.bsp
import tcod.map

from dungeon_crawler import AI, combat, config, objects


class Dungeon:
    def __init__(self, game):
        self.owner = game
        self.console = self.owner.console
        self.dungeon = self._generate_map()
        self.rooms = self._generate_tree_rooms()
        self.explored = self.dungeon.fov
        self.fov = self.dungeon.fov
        self.half_fov = self.dungeon.fov
        self.encounters = self._generate_encounters()
        self.items = self._generate_items()

    @staticmethod
    def _generate_map():
        return tcod.map.Map(width=config.MAP_WIDTH, height=config.MAP_HEIGHT,
                            order='F')

    def _generate_tree_rooms(self, depth=5, min_width=3, min_height=3,
                             max_horizontal_ratio=1.5, max_vertical_ratio=1.5):
        rooms = []
        bsp = tcod.bsp.BSP(x=0, y=0, width=config.MAP_WIDTH,
                           height=config.MAP_HEIGHT)
        bsp.split_recursive(depth=depth, min_width=min_width,
                            min_height=min_height,
                            max_horizontal_ratio=max_horizontal_ratio,
                            max_vertical_ratio=max_vertical_ratio)
        for node in bsp.pre_order():
            if node.children:
                node1, node2 = node.children
                Door(self.dungeon, node, node1, node2)
            else:
                rooms += [Room(self.console, self.dungeon, node)]
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
                x = np.random.randint(room.x1 + 1, room.x2 - 1)
                y = np.random.randint(room.y1 + 1, room.y2 - 1)
                if self.dungeon.walkable[x][y] and (x,
                                                    y) not in monster_coords:
                    monster_coords.append((x, y))
                    ai = AI.BasicMonster()
                    combatant = combat.BasicCombat(hp=30, defense=2, power=5)
                    monster = objects.Monster(x, y,
                                              color=config.COLOR_DARK_GROUND,
                                              combatant=combatant, char='T',
                                              blocks=True, ai=ai)
                    monsters.append(monster)
        return monsters

    def _generate_items(self):
        items, item_coords = [], []
        for room in self.rooms:
            num_items = np.random.randint(0, config.MAX_ROOM_ITEMS)

            for i in range(num_items):
                x = np.random.randint(room.x1 + 1, room.x2 - 1)
                y = np.random.randint(room.y1 + 1, room.y2 - 1)
                if self.dungeon.walkable[x][y] and (x, y) not in item_coords:
                    item_coords.append((x, y))
                    item = objects.Item(x, y, name='Healing Potion', char='!')
                    items.append(item)
        return items


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
    def __init__(self, console, dungeon, node):
        self.console = console
        self.dungeon = dungeon
        self.x1 = node.x
        self.y1 = node.y
        self.x2 = node.x + node.w

        self.y2 = node.y + node.h
        self._generate_room()

    def _generate_room(self):
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                self.dungeon.walkable[x][y] = True
                self.dungeon.transparent[x][y] = True

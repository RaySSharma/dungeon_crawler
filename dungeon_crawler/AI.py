import tcod
import tcod.path
import tcod.map
from dungeon_crawler import config


class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self):
        monster = self.owner
        player = self.owner.owner.owner.player
        if monster.owner.fov[monster.x][monster.y]:
            if monster.distance_to(player) >= 2:
                self.move_astar(player)

            elif player.combatant.hp >= 0:
                monster.combatant.attack(player)

    def move_astar(self, target):
        monster = self.owner
        dungeon = self.owner.owner
        game = self.owner.owner.owner

        fov = tcod.map.Map(config.MAP_WIDTH, config.MAP_HEIGHT, order='F')

        for x in range(config.MAP_WIDTH):
            for y in range(config.MAP_HEIGHT):
                fov.walkable[x][y] = dungeon.dungeon.walkable[x][y]
                fov.transparent[x][y] = dungeon.dungeon.transparent[x][y]

        for obj in game.objects:
            if obj.blocks and obj != self and obj != target:
                fov.walkable[obj.x][obj.y] = False
                fov.transparent[obj.x][obj.y] = True

        if config.DIAGONAL:
            astar = tcod.path.AStar(fov, 1.41)
        else:
            astar = tcod.path.AStar(fov, 0)
        path = astar.get_path(monster.x, monster.y, target.x, target.y)

        if 0 < len(path) < 25:
            monster.x = path[0][0]
            monster.y = path[0][1]
        else:
            monster.move_towards(target.x, target.y)

        del (path, astar)

import tcod
from dungeon_crawler import config


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power


class BasicMonster:
    def __init__(self, game, dungeon):
        self.player = game.player
        self.dungeon = dungeon
        self.fov_map = self.dungeon.fov

    # AI for a basic monster.
    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if self.fov_map[monster.x][monster.y]:
            # move towards player if far away
            if monster.distance_to(self.player) >= 2:
                monster.move_towards(self.player.x, self.player.y)

            # close enough, attack! (if the player is still alive.)
            elif self.player.fighter.hp > 0:
                print('The attack of the ' + monster.name + ' bounces off your shiny metal armor!')

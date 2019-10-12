import pdb

class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self):
        monster = self.owner
        player = self.owner.owner.owner.player
        if monster.owner.fov[monster.x][monster.y]:
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)

            elif player.combatant.hp >= 0:
                monster.combatant.attack(player)

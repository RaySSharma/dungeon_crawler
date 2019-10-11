class BasicMonster:
    def __init__(self, game, fov):
        self.owner = None
        self.player = game.player
        self.fov_map = fov

    # AI for a basic monster.
    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if self.fov_map[monster.x][monster.y]:
            # move towards player if far away
            if monster.distance_to(self.player) >= 2:
                monster.move_towards(self.player.x, self.player.y)

            # close enough, attack! (if the player is still alive.)
            elif self.player.combatant.hp >= 0:
                monster.combatant.attack(self.player)

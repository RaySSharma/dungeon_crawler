class BasicCombat:
    def __init__(self, hp, defense, power):
        self.owner = None
        self.death_function = None
        self.max_hp = hp
        self.hp = hp
        self.mp = 10
        self.max_mp = 10
        self.defense = defense
        self.power = power

    def take_damage(self, damage):
        self.death_function = self.owner.death
        if self.hp - damage <= 0:
            self.death_function()
        else:
            self.hp -= damage

    def attack(self, target):
        game = self.owner.owner.owner
        damage = self.power - target.combatant.defense

        if damage > 0:
            game.gui.print(self.owner.name, 'attacks', target.name, 'for', damage, 'hit points.')
            target.combatant.take_damage(damage)
        else:
            game.gui.print(self.owner.name, 'attacks', target.name, 'but it has no effect!')

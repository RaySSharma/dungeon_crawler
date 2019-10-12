import tcod
import tcod.map
import textwrap

from dungeon_crawler import config, combat, gui, generate_room, characters, input_handler

default_character = {
    'name': 'Ray Sharma',
    'Species': 'Human',
    'Specialization': 'Adventurer',
    'level': 1
}

default_stats = {
    'HP': 10,
    'STR': 10,
    'DEX': 10,
    'CON': 10,
    'INT': 10,
    'WIS': 10
}

default_equipment = ['Short Sword']


class GameInstance:
    def __init__(self, console, root_console, screen_size, map_size,
                 game_state, player_action):
        super().__init__()
        self.console = console
        self.root_console = root_console
        self.screen_size = screen_size
        self.map_size = map_size

        self.input_handler = input_handler.InputHandler(console)
        self.input_handler.owner = self

        combatant = combat.BasicCombat(hp=30, defense=2, power=5)
        self.player = characters.Character(
            self.screen_size[0] / 2, self.screen_size[1] / 2,
            color=config.COLOR_PLAYER, combatant=combatant, char='@',
            blocks=True, character=default_character, stats=default_stats,
            equipment=default_equipment)
        self.dungeon = generate_room.Dungeon(self, map_size)

        self.gui = gui.GUI(self, self.console)
        self.victory = False
        self.failure = False
        self.objects = self.populate_objects()
        self.walkable = self.dungeon.dungeon.walkable
        self.player_action = player_action
        self.game_state = game_state
        self.game_msgs = []

    def render(self):
        self.dungeon.fov = tcod.map.compute_fov(
            self.dungeon.dungeon.transparent,
            pov=(self.player.x, self.player.y), radius=config.TORCH_RADIUS,
            light_walls=config.FOV_LIGHT_WALLS, algorithm=config.FOV_ALGO)

        self.dungeon.explored |= self.dungeon.fov

        for y in range(self.map_size[1]):
            for x in range(self.map_size[0]):
                if not self.dungeon.fov[x][y]:
                    if self.dungeon.explored[x][y]:
                        color_wall = config.COLOR_EXPLORED_WALL
                        color_ground = config.COLOR_EXPLORED_GROUND
                    else:
                        color_wall = config.COLOR_DARK_WALL
                        color_ground = config.COLOR_DARK_GROUND
                else:
                    color_wall = config.COLOR_LIGHT_WALL
                    color_ground = config.COLOR_LIGHT_GROUND

                wall = self.dungeon.dungeon.transparent[x][y]
                if wall:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_wall,
                                                     tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_ground,
                                                     tcod.BKGND_SET)

        for obj in self.objects:
            if obj.state == 'dead':
                obj.draw()

        for obj in self.objects:
            if (obj.state == 'alive') and (obj != self.player):
                obj.draw()

        self.player.draw()

        self.console.blit(self.root_console, 0, 0, 0, 0, self.screen_size[0],
                          self.screen_size[1])

        self.gui.panel.clear()

        # show the player's stats
        self.gui.render_bar(1, 1, config.BAR_WIDTH, 'HP',
                            self.player.combatant.hp,
                            self.player.combatant.max_hp, config.HP_FG_COLOR,
                            config.PANEL_BG_COLOR)

        self.gui.render_messages(self.game_msgs)
        self.gui.panel.blit(self.root_console, 0, config.PANEL_Y, 0, 0,
                            config.SCREEN_WIDTH, config.PANEL_HEIGHT)

    def clear(self):
        for obj in self.objects:
            obj.clear()

    def populate_objects(self):
        objects = [self.player]

        for enc in self.dungeon.encounters:
            objects.append(enc)

        for obj in objects:
            obj.owner = self.dungeon

        return objects

    def detect_collisions(self):
        walkable = self.dungeon.dungeon.walkable.copy()
        for obj in self.objects:
            if obj.blocks:
                walkable[obj.x][obj.y] = False
        self.walkable = walkable

    def object_actions(self):
        if (self.game_state == 'playing') and (self.player_action != 'didnt-take-turn'):
            for obj in self.objects:
                if obj.ai:
                    obj.ai.take_turn()

    def print(self, *args, color=tcod.white):
        string = ' '.join([str(arg) for arg in args])
        msg_lines = textwrap.wrap(string, config.MSG_WIDTH)

        for line in msg_lines:
            if len(self.game_msgs) == config.MSG_HEIGHT:
                del self.game_msgs[0]

            self.game_msgs.append((line, color))

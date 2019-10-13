import tcod
import tcod.map
from dungeon_crawler import config, combat, gui, dungeon_gen, objects, input_handler

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

default_inventory = []


class GameInstance:
    def __init__(self, root_console):
        self.root_console = root_console
        self.console = None
        self.panel = None
        self.misc_panel = None
        self.gui = gui.GUI(self)

        self.input_handler = input_handler.InputHandler()
        self.input_handler.owner = self

        combatant = combat.BasicCombat(hp=30, defense=2, power=5)
        self.player = objects.Character(
            config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2,
            color=config.COLOR_PLAYER, combatant=combatant, char='@',
            blocks=True, character=default_character, stats=default_stats,
            inventory=default_inventory)
        self.dungeon = dungeon_gen.Dungeon(self)

        self.victory = False
        self.failure = False
        self.objects = self.populate_objects()
        self.walkable = self.dungeon.dungeon.walkable
        self.player_action = 'None'
        self.game_state = 'playing'
        self.game_msgs = []
        self.names_under_mouse = None
        self.mouse_x = 0
        self.mouse_y = 0

        item = objects.Item(0, 0, 'Healing Potion')
        item.owner = self.dungeon
        self.objects.append(item)
        item.pick_up()

    def render(self):
        self.console.clear()
        self.dungeon.fov = tcod.map.compute_fov(
            self.dungeon.dungeon.transparent,
            pov=(self.player.x, self.player.y), radius=config.TORCH_RADIUS,
            light_walls=config.FOV_LIGHT_WALLS, algorithm=config.FOV_ALGO)

        self.dungeon.half_fov = tcod.map.compute_fov(
            self.dungeon.dungeon.transparent,
            pov=(self.player.x, self.player.y), radius=config.HALFTORCH_RADIUS,
            light_walls=config.FOV_LIGHT_WALLS, algorithm=config.FOV_ALGO)

        self.dungeon.explored |= self.dungeon.fov

        for x in range(config.MAP_WIDTH):
            for y in range(config.MAP_HEIGHT):
                if not self.dungeon.half_fov[x][y]:
                    if self.dungeon.explored[x][y]:
                        color_wall = config.COLOR_EXPLORED_WALL
                        color_ground = config.COLOR_EXPLORED_GROUND
                    else:
                        color_wall = config.COLOR_DARK_WALL
                        color_ground = config.COLOR_DARK_GROUND
                elif self.dungeon.fov[x][y]:
                    color_wall = config.COLOR_LIGHT_WALL
                    color_ground = config.COLOR_LIGHT_GROUND
                else:
                    color_wall = config.COLOR_HALFLIGHT_WALL
                    color_ground = config.COLOR_HALFLIGHT_GROUND

                transparent = self.dungeon.dungeon.transparent[x][y]
                if not transparent:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_wall,
                                                     tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(self.console, x, y,
                                                     color_ground,
                                                     tcod.BKGND_SET)

        [obj.draw() for obj in self.objects if obj.type == 'item']
        [obj.draw() for obj in self.objects if obj.state == 'dead']
        [obj.draw() for obj in self.objects if (obj.state == 'alive') and (obj != self.player)]

        for obj in self.objects:
            if (obj.state == 'alive') and (obj != self.player):
                obj.draw()

        self.player.draw()
        self.gui.render_names_under_mouse()
        self.console.blit(self.root_console, 0, 0, 0, 0, config.SCREEN_WIDTH,
                          config.SCREEN_HEIGHT)

        self.gui.render_panel()
        self.gui.render_bar(1, 1, total_width=config.BAR_WIDTH, name='HP',
                            value=self.player.combatant.hp,
                            maximum=self.player.combatant.max_hp,
                            bar_color=config.COLOR_HP_FG,
                            back_color=config.COLOR_HP_BG)

        self.gui.render_bar(1, 3, total_width=config.BAR_WIDTH, name='MP',
                            value=self.player.combatant.mp,
                            maximum=self.player.combatant.max_mp,
                            bar_color=config.COLOR_MANA_FG,
                            back_color=config.COLOR_MANA_BG)

        self.gui.render_messages(self.game_msgs)
        self.panel.blit(self.root_console, dest_x=0, dest_y=config.PANEL_Y,
                        src_x=0, src_y=0, width=config.SCREEN_WIDTH,
                        height=config.PANEL_HEIGHT)

    def clear(self):
        for obj in self.objects:
            obj.clear()

    def populate_objects(self):
        objects = [self.player]

        for enc in self.dungeon.encounters:
            objects.append(enc)

        for item in self.dungeon.items:
            objects.append(item)

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
        if (self.game_state == 'playing') and (self.player_action !=
                                               'didnt-take-turn'):
            for obj in self.objects:
                if obj.ai:
                    obj.ai.take_turn()

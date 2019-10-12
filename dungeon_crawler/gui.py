import tcod
from dungeon_crawler import config


class GUI:
    def __init__(self, game, console):
        self.owner = game
        self.console = console
        self.panel = tcod.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color,
                   back_color):
        bar_width = int(float(value) / maximum * total_width)

        self.panel.default_bg = back_color
        self.panel.draw_rect(x, y, total_width, config.PANEL_HEIGHT, ch=0, bg=back_color, bg_blend=tcod.BKGND_NONE)

        if bar_width > 0:
            self.panel.draw_rect(x, y, bar_width, 1, ch=0, bg=bar_color, bg_blend=tcod.BKGND_SET)

        # finally, some centered text with the values
        self.panel.default_fg = tcod.white
        self.panel.print(x=int(x + total_width / 2), y=y,
                         string=name + ': ' + str(value) + '/' + str(maximum),
                         bg_blend=tcod.BKGND_NONE, alignment=tcod.CENTER)


    def render_messages(self, game_msgs):
        y = 1
        for (line, color) in game_msgs:
            self.panel.default_fg = color
            self.panel.print(config.MSG_X, y, string=line, alignment=tcod.LEFT)
            y += 1

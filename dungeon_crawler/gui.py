import tcod
from dungeon_crawler import config


class GUI:
    def __init__(self, game, console):
        self.owner = game
        self.console = console
        self.panel = tcod.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color,
                   back_color):
        # render a bar (HP, experience, etc). first calculate the width of the bar
        bar_width = int(float(value) / maximum * total_width)

        # render the background first
        self.panel.default_bg = tcod.grey
        self.panel.rect(x, y, total_width, 1, False, tcod.BKGND_SCREEN)

        # now render the bar on top
        self.panel.default_bg = tcod.darker_red
        if bar_width > 0:
            self.panel.rect(x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

        # finally, some centered text with the values
        self.panel.default_fg = tcod.white
        self.panel.print(x=int(x + total_width / 2), y=y,
                         string=name + ': ' + str(value) + '/' + str(maximum),
                         bg_blend=tcod.BKGND_NONE, alignment=tcod.CENTER)

import tcod
import tcod.console
from dungeon_crawler import config
import textwrap


class GUI:
    def __init__(self, game):
        self.owner = game
        self.owner.console = tcod.console.Console(config.SCREEN_WIDTH,
                                                  config.SCREEN_HEIGHT,
                                                  order='F')
        self.owner.panel = tcod.console.Console(config.SCREEN_WIDTH,
                                                config.PANEL_HEIGHT, order='F')

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color,
                   back_color):
        bar_width = int(float(value) / maximum * total_width)

        self.owner.panel.draw_rect(x, y, total_width, 1, ch=0,
                                   bg=back_color,
                                   bg_blend=tcod.BKGND_SET)
        if bar_width > 0:
            self.owner.panel.draw_rect(x, y, bar_width, 1, ch=0, bg=bar_color,
                                       bg_blend=tcod.BKGND_SET)

        self.owner.panel.print(
            x=int(x + total_width / 2), y=y,
            string=name + ': ' + str(value) + '/' + str(maximum),
            bg_blend=tcod.BKGND_NONE, alignment=tcod.CENTER)

    def render_messages(self, game_msgs):
        y = 1
        for (line, color) in game_msgs:
            self.owner.panel.default_fg = color
            self.owner.panel.print(config.MSG_X, y, string=line,
                                   alignment=tcod.LEFT)
            y += 1

    def render_panel(self):
        self.owner.panel.clear()
        self.owner.panel.default_fg = tcod.white
        self.owner.panel.draw_rect(0, 0, config.MSG_X - 1, config.PANEL_HEIGHT, ch=0,
                                   bg=config.COLOR_PANEL_BG,
                                   bg_blend=tcod.BKGND_SCREEN)
        self.owner.panel.draw_rect(config.MSG_X - 1, 0, config.MSG_WIDTH, config.PANEL_HEIGHT, ch=0,
                                   bg=config.COLOR_MESSAGE_BG,
                                   bg_blend=tcod.BKGND_SCREEN)

    def print(self, *args, color=tcod.white):
        string = ' '.join([str(arg) for arg in args])
        msg_lines = textwrap.wrap(string, config.MSG_WIDTH)

        for line in msg_lines:
            if len(self.owner.game_msgs) == config.MSG_HEIGHT:
                del self.owner.game_msgs[0]

            self.owner.game_msgs.append((line, color))

    def render_names_under_mouse(self):
        if self.owner.names_under_mouse is not None:
            x = self.owner.mouse_x + 2
            y = self.owner.mouse_y + 2
            self.owner.console.print_box(
                x, y, width=len(self.owner.names_under_mouse), height=1,
                string=self.owner.names_under_mouse, fg=tcod.white,
                bg=tcod.darkest_gray, bg_blend=tcod.BKGND_SET)
            self.owner.names_under_mouse = None
        else:
            pass

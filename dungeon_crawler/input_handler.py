import tcod
import tcod.event
from dungeon_crawler import config


class InputHandler(tcod.event.EventDispatch):
    def __init__(self):
        self.owner = None

    def ev_quit(self, event):
        print('Exiting')
        raise SystemExit()

    def ev_windowclose(self, event):
        print('Exiting')
        raise SystemExit()

    def ev_mousemotion(self, event):
        x, y = event.tile
        self.owner.mouse_x = x
        self.owner.mouse_y = y
        self.owner.names_under_mouse = self.get_names_under_mouse(x, y)
        self.owner.player_action = 'didnt-take-turn'

    def ev_keydown(self, event):
        scancode = event.scancode
        mod = event.mod

        if (scancode == tcod.event.SCANCODE_RETURN) and (mod %
                                                         tcod.event.KMOD_LALT):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        elif scancode == tcod.event.SCANCODE_ESCAPE:
            print('Exiting')
            raise SystemExit()

        if (self.owner.game_state == 'playing') and config.DIAGONAL:
                if scancode == tcod.event.SCANCODE_KP_7:
                    self.owner.player.move_or_attack(-1, -1)
                elif scancode == tcod.event.SCANCODE_KP_9:
                    self.owner.player.move_or_attack(1, -1)
                elif scancode == tcod.event.SCANCODE_KP_1:
                    self.owner.player.move_or_attack(-1, 1)
                elif scancode == tcod.event.SCANCODE_KP_3:
                    self.owner.player.move_or_attack(1, 1)

        if self.owner.game_state == 'playing':
            if (scancode == tcod.event.SCANCODE_KP_8) or (
                    scancode == tcod.event.SCANCODE_UP):
                self.owner.player.move_or_attack(0, -1)
            elif (scancode == tcod.event.SCANCODE_KP_2) or (
                    scancode == tcod.event.SCANCODE_DOWN):
                self.owner.player.move_or_attack(0, 1)
            elif (scancode == tcod.event.SCANCODE_KP_4) or (
                    scancode == tcod.event.SCANCODE_LEFT):
                self.owner.player.move_or_attack(-1, 0)
            elif (scancode == tcod.event.SCANCODE_KP_6) or (
                    scancode == tcod.event.SCANCODE_RIGHT):
                self.owner.player.move_or_attack(1, 0)

            elif (scancode == tcod.event.SCANCODE_KP_ENTER) or (scancode == tcod.event.SCANCODE_RETURN):
                for obj in self.owner.objects:
                    if (obj.x == self.owner.player.x) and (obj.y == self.owner.player.y) and (obj.type == 'item'):
                        obj.pick_up()
                        break
            else:
                self.owner.player_action = 'didnt-take-turn'
                return

            self.owner.player_action = 'took-turn'

    def check_input(self):
        for event in tcod.event.wait():
            if event.type == 'KEYUP':
                return False
            else:
                self.dispatch(event)
        return True

    def get_names_under_mouse(self, x, y):
        names = [
            obj.name for obj in self.owner.objects if obj.x == x and obj.y == y
            and self.owner.dungeon.fov[obj.x][obj.y]
        ]
        if len(names) > 0:
            names = ', '.join(names)  # join the names, separated by commas
            return names
        else:
            return None

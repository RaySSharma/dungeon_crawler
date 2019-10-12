import tcod
import tcod.event


class InputHandler(tcod.event.EventDispatch):
    def __init__(self, console):
        self.owner = None
        self.console = console

    def ev_quit(self, event):
        print('Exiting')
        raise SystemExit()

    def ev_windowclose(self, event):
        print('Exiting')
        raise SystemExit()

    def ev_mousemotion(self, event):
        self.owner.player_action = 'didnt-take-turn'

    def ev_keydown(self, event):
        scancode = event.scancode
        mod = event.mod

        if (scancode == tcod.event.SCANCODE_RETURN) and (mod % tcod.event.KMOD_LALT):
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        elif scancode == tcod.event.SCANCODE_ESCAPE:
            print('Exiting')
            raise SystemExit()

        if self.owner.game_state == 'playing':
            if scancode == tcod.event.SCANCODE_UP:
                self.owner.player.move_or_attack(0, -1)
            elif scancode == tcod.event.SCANCODE_DOWN:
                self.owner.player.move_or_attack(0, 1)
            elif scancode == tcod.event.SCANCODE_LEFT:
                self.owner.player.move_or_attack(-1, 0)
            elif scancode == tcod.event.SCANCODE_RIGHT:
                self.owner.player.move_or_attack(1, 0)
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

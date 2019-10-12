import tcod
import tcod.event

from dungeon_crawler import config, game_instance

if __name__ == '__main__':
    screen_size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    map_size = (config.MAP_WIDTH, config.MAP_HEIGHT)

    with tcod.console_init_root(screen_size[0], screen_size[1],
                                renderer=tcod.RENDERER_SDL2,
                                order='F') as root_console:

        console = tcod.console_new(screen_size[0], screen_size[1])

        game = game_instance.GameInstance(console=console,
                                          root_console=root_console,
                                          screen_size=screen_size,
                                          map_size=map_size,
                                          game_state='playing',
                                          player_action=None)
        game.print('You enter the dungeon.', color=tcod.white)

        while not tcod.console_is_window_closed():
            game.render()
            tcod.console_flush()
            game.clear()
            valid_input = game.input_handler.check_input()
            if valid_input:
                game.detect_collisions()
                game.object_actions()

            if game.player.state == 'dead':
                break

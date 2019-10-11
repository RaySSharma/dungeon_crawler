import tcod

from dungeon_crawler import game_instance
from dungeon_crawler import config

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

        while not tcod.console_is_window_closed():
            game.render()
            tcod.console_flush()
            game.clear()
            game.player_action = game.handle_keys()
            game.detect_collisions()
            game.object_actions()

            if game.player_action == 'exit':
                break

            if game.player.state == 'dead':
                break

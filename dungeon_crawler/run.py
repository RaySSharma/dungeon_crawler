import tcod.console
from dungeon_crawler import config, game_instance

if __name__ == '__main__':
    screen_size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    map_size = (config.MAP_WIDTH, config.MAP_HEIGHT)

    with tcod.console_init_root(screen_size[0], screen_size[1],
                                renderer=tcod.RENDERER_SDL2,
                                order='F', vsync=False) as root_console:
        game = game_instance.GameInstance(root_console)
        game.gui.print('You enter the dungeon.', color=tcod.white)

        while True:
            game.render()
            tcod.console_flush()
            game.clear()
            valid_input = game.input_handler.check_input()
            if valid_input:
                game.detect_collisions()
                game.object_actions()

            if game.player.state == 'dead':
                break

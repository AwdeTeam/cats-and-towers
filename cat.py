import actor
import wall
import world

from pgmodel.core import game

config = {
    "global": {
        "starts_running": True,
        "fps":50
    },
    "world": {},
    "graphics": {
        "window_width": 800,
        "window_height": 600,
        "background_color": "#111111",
        "assets_url": None,
    }
}

game_instance = game.Game(world.World, config)
game_instance.register_actor(actor.Actor(game_instance.world, game_instance))
game_instance.register_actor(wall.Wall(game_instance.world, game_instance))
game_instance.start()

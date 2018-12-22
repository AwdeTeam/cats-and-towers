import actor
import world

from pgmodel.core import game

config = {
    "global": {"starts_running": True},
    "world": {},
    "graphics": {
        "window_width": 800,
        "window_height": 600,
        "background_color": "#FF0000",
        "assets_url": None,
    }
}

game_instance = game.Game(world.World, config)

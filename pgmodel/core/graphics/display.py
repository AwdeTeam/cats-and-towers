#Snippets, snippets, snippets...

import pygame
from pygame import Color

class Display:
    """ The core class which manages the window and drawing things to it """

    def __init__(self, game, cfg_display):
        self._game = game
        self._world = None #This may be unstable, get it on construct()
        self._interface = None #Again, wait until construct()
        self.cfg_display = cfg_display
        self._w = self.cfg_display["window_width"]
        self._h = self.cfg_display["window_height"]
        self.bg_color = Color(self.cfg_display["background_color"])

        self.asset_manager = AssetManager(self.cfg_display["assets_url"])

        self.actor_sprites = []
        self.background_sprites = None #TODO does not handle 'fancy' backgrounds yet

    def construct(self):
        """ Actually show the display """
        self.screen = pygame.display.set_mode((self._w, self._h))
        self.screen.fill(self.bg_color)
        pygame.display.flip()

    def update(self):
        """ Draw everything on screen """
        self.screen.fill(self.bg_color)

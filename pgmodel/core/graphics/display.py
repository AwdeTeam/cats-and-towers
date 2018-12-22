#Snippets, snippets, snippets...

import pygame
from pygame import Color
import pymunk.pygame_util

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

        #self.asset_manager = AssetManager(self.cfg_display["assets_url"])

        self.actor_sprites = []
        self.background_sprites = None #TODO does not handle 'fancy' backgrounds yet


    def construct(self):
        """ Actually show the display """
        self.screen = pygame.display.set_mode((self._w, self._h))
        self.screen.fill(self.bg_color)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self._world = self._game.world
        
        pygame.display.flip()

    def update(self):
        """ Draw everything on screen """
        self.screen.fill(self.bg_color)

        for actor in self._game.actors:
            actor.render(self.screen)

        self._world.space.debug_draw(self.draw_options)

        pygame.display.flip()

    # TODO: don't know if this is actually needed
    def register_actor(self, actor):
        pass

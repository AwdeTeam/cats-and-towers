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
        self.viewport_pad = self.cfg_display["viewport_pad"]

        self.x_offset = 0
        self.y_offset = 0

        #self.asset_manager = AssetManager(self.cfg_display["assets_url"])

        self.actor_sprites = []
        self.background_sprites = None #TODO does not handle 'fancy' backgrounds yet

        self.main_player = None
        
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)

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

        #self._world.space.debug_draw(self.draw_options)
        self.main_player.render_score(self.screen)

        pygame.display.flip()

    def draw_game_over(self):
        font_surface = self.font.render("GAME OVER - " + str(self._game.score), False, (255, 255, 255))
        self.screen.blit(font_surface, (200, 200))
        pygame.display.flip()


    # TODO: don't know if this is actually needed
    def register_actor(self, actor):
        pass

    # update offset to give a viewport margin around the given actor
    def scroll_viewport(self, actor):

        #print("actor:",actor.x,actor.y)
        #print("offset:",self.x_offset,self.y_offset)
        #print("screen_end:",(self.x_offset + self._w - actor.w))
        #print(self.screen.get_rect())

        right_view_edge = self.x_offset + self._w - actor.w - self.viewport_pad
        left_view_edge = self.x_offset + self.viewport_pad

        top_view_edge = self.y_offset + self.viewport_pad
        bottom_view_edge = self.y_offset + self._h - actor.h - self.viewport_pad

        #print(left_view_edge, right_view_edge)


        #actor_view_x = actor.x - self.x_offset
        #print("actor view:", actor_view_x)
        

        diffx = 0.0
        diffy = 0.0
        
        if actor.x > right_view_edge:
            diffx = actor.x - right_view_edge
            self.x_offset += diffx / 4
        elif actor.x < left_view_edge:
            diffx = left_view_edge - actor.x
            self.x_offset -= diffx / 4

        if actor.y < top_view_edge:
            diffy = top_view_edge - actor.y
            self.y_offset -= diffy / 4
        elif actor.y > bottom_view_edge:
            diffy = actor.y - bottom_view_edge
            self.y_offset += diffy / 4
        

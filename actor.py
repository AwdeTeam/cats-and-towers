import pygame
import pymunk
import pymunk.pygame_util

class Actor:

    def __init__(self, world, game):
        self.world = world
        self.game = game
        self.x = 10
        self.y = 500
        self.body = None # physics

    def set_pos(self, x, y):
        """ Change the position (onscreen?) of this actor """
        self.x = x
        self.y = y
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        #pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(self.x, self.y, 50, 50))
        position = pymunk.pygame_util.to_pygame(self.body.position, screen)
        print(position)
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(position[0], position[1], 50, 50))
        

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

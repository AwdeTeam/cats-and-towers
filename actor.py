import pygame
import pymunk
import pymunk.pygame_util

class Actor:

    def __init__(self, world, game):
        self.world = world
        self.game = game
        self.x = 50
        self.y = 500
        self.h = 50
        self.w = 50
        self.body = None # physics

    def set_pos(self, x, y):
        """ Change the position (onscreen?) of this actor """
        self.x = x
        self.y = y

    def init_physics(self, space):
        #body = pymunk.Body(20, pymunk.moment_for_box(20, (self.h, self.w)))
        body = pymunk.Body(20, 50)
        body.position = self.x, self.y
        poly = pymunk.Poly.create_box(body, (self.h, self.w))

        body.friction = .9
        body.elasticity = .9
        
        self.body = body
        space.add(body, poly)
        
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        position = pymunk.pygame_util.to_pygame(self.body.position, screen)
        pygame.draw.rect(
            screen,
            (0, 128, 255),
            pygame.Rect(position[0] - self.w / 2, position[1] - self.h / 2, self.w, self.h)
        )

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

import pygame
import pymunk
import pymunk.pygame_util
import random

class Mob:

    def __init__(self, world, game, x, y):
        self.world = world
        self.game = game
        self.x = x
        self.y = y
        self.h = 25
        self.w = 25
        self.mass = 20
        self.body = None # physics
        self.grounded = False
        self.allowed_jumps = 2
        self.remaining_jumps = self.allowed_jumps

    def set_pos(self, x, y):
        """ Change the position (onscreen?) of this actor """
        self.x = x
        self.y = y

    def init_physics(self, space):
        body = pymunk.Body(self.mass, pymunk.inf)
        body.position = self.x, self.y
        poly = pymunk.Poly.create_box(body, (self.h, self.w))

        #poly.friction = .4
        poly.friction = .4
        poly.elasticity = 0 # don't bounce
        
        self.body = body
        space.add(body, poly)

    def adjust_movement(self, player):

        dice = random.random()
        if dice < .01 or (player.y < self.y and dice < .02):
             self.body.apply_impulse_at_world_point((0, -10000))

        v = self.body.velocity
        
        if (player.x < self.x):
            v = (max(v.x - 30, -300), v.y)
        else:
            v = (min(v.x + 30, 300), v.y)

        self.body.velocity = v
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        position = pymunk.pygame_util.to_pygame(self.body.position, screen)
        local_x = (position[0] - self.w / 2)
        local_y = (position[1] - self.h / 2)

        self.x = local_x
        self.y = local_y
        
        pygame.draw.rect(
            screen,
            (255, 83, 0),
            pygame.Rect(local_x - self.game.display.x_offset, local_y - self.game.display.y_offset, self.w, self.h)
        )

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

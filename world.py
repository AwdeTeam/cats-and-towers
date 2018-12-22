import pymunk
import actor
import wall
from pygame.locals import *
import pygame

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game
        self.actors = []
        
        # this was previously in construct, but then cat.py can't add actors until game starts, possibly need better solution/pipeline for how things are added
        self.space = pymunk.Space()
        self.space.gravity = (0, -500)

    def construct(self):
        """ Initialize physics world """
        self.player = actor.Actor(self, self.game)
        self.game.register_actor(self.player)
        self.game.register_actor(wall.Wall(self, self.game))

    def update(self, dt):
        """ Run the physics simulation a step """

        # persistent keys
        keys = pygame.key.get_pressed()
        if (keys[K_d]):
            #self.player.body.velocity = (100, self.player.body.velocity.y)
            self.player.body.velocity = (min(self.player.body.velocity.x + 10, 1000), self.player.body.velocity.y)
            
        if (keys[K_a]):
            #self.player.body.velocity = (-100, self.player.body.velocity.y)
            self.player.body.velocity = (max(self.player.body.velocity.x - 10, -1000), self.player.body.velocity.y)
        if (keys[K_s]):
            pass

        self.space.step(dt)
        
    def register_actor(self, actor):
        """ Add physics entity for given actor """
        self.actors.append(actor)

        actor.init_physics(self.space)
        
        #self.space.add(body, poly)
        
        #body = pymunk.Body(1, 1)
        #body.position = actor.x, actor.y

        #poly = pymunk.Poly.create_box(body)
        #self.space.add(body, poly)
        #actor.body = body
        

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_w:
            print("w key was pressed")
            self.player.body.apply_impulse_at_local_point((0, 5000))
            print(self.player.body.velocity)
        pass

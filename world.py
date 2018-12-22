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
        self.space.gravity = (0, -1000)

    def construct(self):
        """ Initialize physics world """
        self.player = actor.Actor(self, self.game)
        self.game.register_actor(self.player)
        self.game.register_actor(wall.Wall(self, self.game))
        self.game.register_actor(wall.Wall(self, self.game, (200, 200), (400, 200)))
        self.game.register_actor(wall.Wall(self, self.game, (400, 300), (500, 300)))

    def update(self, dt):
        """ Run the physics simulation a step """

        # persistent keys

        keys = pygame.key.get_pressed()
        if (keys[K_d]):
            # NOTE: allow slowing down from going the opposite direction quickly
            v = self.player.body.velocity
            if v.x < 0: v = (min(v.x + 100, 0), v.y)
            else: v = (min(v.x + 10, 1000), v.y)
            self.player.body.velocity = v
            
        if (keys[K_a]):
            v = self.player.body.velocity
            if v.x > 0: v = (max(v.x - 100, 0), v.y)
            else: v = (max(v.x - 10, -1000), v.y)
            self.player.body.velocity = v
            
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
            self.player.body.apply_impulse_at_world_point((0, 10000))
            print(self.player.body.velocity)
        pass

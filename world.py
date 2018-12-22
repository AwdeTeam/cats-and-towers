import pymunk
import actor
import wall
from pygame.locals import *
import pygame
from pymunk.vec2d import Vec2d

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game
        self.actors = []
        
        # this was previously in construct, but then cat.py can't add actors until game starts, possibly need better solution/pipeline for how things are added
        self.space = pymunk.Space()
        self.space.gravity = (0, -1000)
        self.space.damping = .9

    def construct(self):
        """ Initialize physics world """
        self.player = actor.Actor(self, self.game)
        self.game.register_actor(self.player)
        self.game.register_actor(wall.Wall(self, self.game))
        self.game.register_actor(wall.Wall(self, self.game, (200, 200), (400, 200)))
        self.game.register_actor(wall.Wall(self, self.game, (400, 300), (500, 300)))
        self.game.register_actor(wall.Wall(self, self.game, (10, 10), (1000, 10)))

    def update(self, dt):
        """ Run the physics simulation a step """

        # find out if player is standing on ground
        # thanks to https://github.com/viblo/pymunk/blob/master/examples/platformer.py
        grounding = {
            "normal": Vec2d.zero(),
            "penetration": Vec2d.zero(),
            "impulse": Vec2d.zero(),
            "position": Vec2d.zero(),
            "body": None
        }
        def f(arbiter):
            #print(arbiter.elasticity)
            #print(arbiter.friction)
            #print(arbiter.shapes[0])
            #print(arbiter.shapes[0].friction)
            #print(arbiter.shapes[1])
            #print(arbiter.shapes[1].friction)
            n = -arbiter.contact_point_set.normal
            if n.y > grounding["normal"].y:
                grounding["normal"] = n
                grounding["penetration"] = -arbiter.contact_point_set.points[0].distance
                grounding["body"] = arbiter.shapes[1].body
                grounding["impulse"] = arbiter.total_impulse
                grounding["position"] = arbiter.contact_point_set.points[0].point_b
        self.player.body.each_arbiter(f)

        well_grounded = False
        self.player.grounded = False
        if grounding["body"] != None and abs(grounding["normal"].x/grounding["normal"].y) < 1:
            well_grounded = True
            self.player.grounded = True
            self.player.remaining_jumps = self.player.allowed_jumps

        # persistent keys
        keys = pygame.key.get_pressed()
        v = self.player.body.velocity
        if (keys[K_d]):
            # NOTE: allow slowing down from going the opposite direction quickly
            if v.x < 0 and well_grounded: v = (min(v.x + 100, 0), v.y)
            elif well_grounded: v = (min(v.x + 20, 2000), v.y)
            else: v = (min(v.x + 10, 2000), v.y)
        if (keys[K_a]):
            v = self.player.body.velocity
            if v.x > 0 and well_grounded: v = (max(v.x - 100, 0), v.y)
            elif well_grounded: v = (max(v.x - 20, -2000), v.y)
            else: v = (max(v.x - 10, -2000), v.y)
        if (keys[K_s]):
            pass

        self.player.body.velocity = v

        # scroll viewport
        self.game.display.scroll_viewport(self.player)

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
            print(self.player.remaining_jumps)

            # TODO: check off by one error later
            if self.player.remaining_jumps > 1:
                self.player.body.apply_impulse_at_world_point((0, 10000))
                self.player.remaining_jumps -= 1

        if event.type == KEYDOWN and event.key == K_SPACE:
            print("Space was pressed")
            self.game.display.y_offset += 10

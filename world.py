import pymunk
import actor
import wall
import mob
import random
from pygame.locals import *
import pygame
import random
from pymunk.vec2d import Vec2d

# a sector is 1000x1000

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game
        self.actors = []

        self.generated_sectors = []
        
        # this was previously in construct, but then cat.py can't add actors until game starts, possibly need better solution/pipeline for how things are added
        self.space = pymunk.Space()
        self.space.gravity = (0, -1000)
        self.space.damping = .9

    def construct(self):
        """ Initialize physics world """
        self.player = actor.Actor(self, self.game)
        self.game.register_actor(self.player)
        #self.game.register_actor(wall.Wall(self, self.game))
        #self.game.register_actor(wall.Wall(self, self.game, (200, 200), (400, 200)))
        #self.game.register_actor(wall.Wall(self, self.game, (400, 300), (500, 300)))
        #self.game.register_actor(wall.Wall(self, self.game, (10, 10), (1000, 10)))
        #self.game.register_actor(wall.Wall(self, self.game, (1000, 10), (1000, 1000)))
        #self.game.register_actor(wall.Wall(self, self.game, (10, 10), (10, 1000)))
        self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))
        self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))
        self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))

        #self.game.register_actor(wall.Wall(self, self.game, (-10000, 10), (10000, 10)))

        self.generate_sector((0, 0))
        self.generate_sector((1, 0))
        self.generate_sector((-1, 0))
        self.generate_sector((0, 1))
        self.generate_sector((0, -1))
        self.generate_sector((1, 1))
        self.generate_sector((1, -1))
        self.generate_sector((-1, 1))
        self.generate_sector((-1, -1))

        def platform_collision_presolve(arbiter, space, data):
            #if arbiter.contact_point_set.normal[1] > .5:
            #    return False
            #elif arbiter.contact_point_set.normal[1] < -.5:
            #    keys = pygame.key.get_pressed()
            #    if keys[K_s]:
            #        return False
            #    return True
            return True
            
        platform_handler = self.space.add_collision_handler(1, 2)
        platform_handler.pre_solve = platform_collision_presolve

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
            #print(n)
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
        if keys[K_d]:
            # NOTE: allow slowing down from going the opposite direction quickly
            if v.x < 0 and well_grounded: v = (min(v.x + 100, 0), v.y)
            elif well_grounded: v = (min(v.x + 20, 2000), v.y)
            else: v = (min(v.x + 10, 2000), v.y)
        if keys[K_a]:
            v = self.player.body.velocity
            if v.x > 0 and well_grounded: v = (max(v.x - 100, 0), v.y)
            elif well_grounded: v = (max(v.x - 20, -2000), v.y)
            else: v = (max(v.x - 10, -2000), v.y)

        self.player.body.velocity = v

        # scroll viewport
        self.game.display.scroll_viewport(self.player)

        self.check_if_near_border()

        self.space.step(dt)

    def check_if_near_border(self):
        sector_x = int(self.player.x / 1000)
        sector_y = int(self.player.y / 1000)
        print(sector_x, sector_y)

        for y in range(sector_y-2, sector_y+2):
            for x in range(sector_x-2, sector_x+2):
                self.ensure_sector(x, y)
                

        #self.ensure_sector(sector_x, sector_y)
        #self.ensure_sector(sector_x+1, sector_y)
        #self.ensure_sector(sector_x-1, sector_y)
        #self.ensure_sector(sector_x, sector_y+1)
        #self.ensure_sector(sector_x, sector_y-1)
        #self.ensure_sector(sector_x+1, sector_y+1)
        #self.ensure_sector(sector_x+1, sector_y-1)
        #self.ensure_sector(sector_x-1, sector_y+1)
        #self.ensure_sector(sector_x-1, sector_y-1)
        
        print(self.generated_sectors)

    def ensure_sector(self, x, y):
        if (x,y) not in self.generated_sectors:
            self.generate_sector((x, y))
        
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

    def generate_sector(self, pos):
        self.generated_sectors.append(pos)
        
        # decide on vertical sections
        for y in range(0, 10):
            x_used = []
            for x in range(0, 10):
                dice = random.random()
                if dice > .9 or (dice > .3 and x - 1 in x_used):
                    x_used.append(x)
                    self.game.register_actor(wall.Wall(self, self.game, ((pos[0]*1000 + x*100), (pos[1]*1000 + y*100)), ((pos[0]*1000 + (x+1)*100), (pos[1]*1000 + y*100))))
                
        # decide on horizontal sections
        for x in range(0, 10):
            for y in range(0, 10):
                y_used = []
                dice = random.random()
                if dice > .8 or (dice > .3 and y - 1 in y_used):
                    y_used.append(y)
                    self.game.register_actor(wall.Wall(self, self.game, ((pos[0]*1000 + x*100), (pos[1]*1000 + y*100)), ((pos[0]*1000 + x*100), (pos[1]*1000 + (y+1)*100))))

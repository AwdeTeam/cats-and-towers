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
        self.mobs = []

        self.generated_sectors = []
        self.sector_walls = {}
        
        # this was previously in construct, but then cat.py can't add actors until game starts, possibly need better solution/pipeline for how things are added
        self.space = pymunk.Space()
        #self.space.gravity = (0, -1000)
        self.space.gravity = (0, 1000)
        self.space.damping = .9
        self.space.sleep_time_threshold = 1
        self.time_factor = 0

    def construct(self):
        """ Initialize physics world """
        self.player = actor.Actor(self, self.game)
        self.game.register_actor(self.player)
        self.game.display.main_player = self.player
        #self.game.register_actor(wall.Wall(self, self.game))
        #self.game.register_actor(wall.Wall(self, self.game, (200, 200), (400, 200)))
        #self.game.register_actor(wall.Wall(self, self.game, (400, 300), (500, 300)))
        #self.game.register_actor(wall.Wall(self, self.game, (10, 10), (1000, 10)))
        #self.game.register_actor(wall.Wall(self, self.game, (1000, 10), (1000, 1000)))
        #self.game.register_actor(wall.Wall(self, self.game, (10, 10), (10, 1000)))
        #self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))
        #self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))
        #self.game.register_actor(mob.Mob(self, self.game, random.randint(15,700), random.randint(15, 1000)))

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
            n = arbiter.contact_point_set.normal
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
            else: v = (min(v.x + 15, 2000), v.y)
        if keys[K_a]:
            v = self.player.body.velocity
            if v.x > 0 and well_grounded: v = (max(v.x - 100, 0), v.y)
            elif well_grounded: v = (max(v.x - 20, -2000), v.y)
            else: v = (max(v.x - 15, -2000), v.y)

        self.player.body.velocity = v
        self.player.jump_refresh -= 1
        if self.player.jump_refresh < 0: self.player.jump_refresh = 0
        self.player.handle_movement()

        # mob movement
        for m in self.mobs:
            m.adjust_movement(self.player)

        # scroll viewport
        self.game.display.scroll_viewport(self.player)

        self.check_if_near_border()
        self.generate_mobs()
        self.cull()

        self.cull_mobs()

        self.space.step(dt)

    def check_if_near_border(self):
        sector_x = int(self.player.x / 1000)
        sector_y = int(self.player.y / 1000)
        #print(sector_x, sector_y)
        radius = 3

        for y in range(sector_y-radius, sector_y+radius):
            for x in range(sector_x-radius, sector_x+radius):
                self.ensure_sector(x, y)

        #print(self.generated_sectors)

    def generate_mobs(self):
        dice = random.random()
        if dice < (.05 + self.time_factor):
            if self.time_factor < 1: self.time_factor += .0005
            
            #print(str(.05 + self.time_factor))
            #print("generating mob")
            x = random.randint(-1000,1000)
            if x > 0:
                x += self.game.display._w

            y = random.randint(-1000,1000)
            if y > 0:
                y += self.game.display._h

            m = mob.Mob(self, self.game, self.player.x + x, self.player.y + y)
            self.game.register_actor(m)
            self.mobs.append(m)

    def cull_mobs(self):
        #print(len(self.mobs))
        for m in self.mobs:
            diffx = abs(m.x - self.player.x)
            diffy = abs(m.y - self.player.y)

            if diffx > 3000 or diffy > 3000:
                #print("culling mob")
                #m.body.sleep()
                #try:
                    #print("Trying to remove body")
                    #self.space.remove(m.body)
                    #self.space.remove(m.poly)
                #except: print("Failed to remove mob physics")
                self.mobs.remove(m)
                self.game.kill_actor(m)
                

    def cull(self):
        #print("culling")

        #for w in self.sector_walls[0]:
        #    try:
        #        print((w in self.actors))
        #        print("killing")
        #        print(self.game)
        #        self.game.kill_actor(w)
        #        print("killed")
        #    except: pass
        
        
        for sector in self.generated_sectors:
            diff_x = abs(sector[0] - int(self.player.x / 1000))
            diff_y = abs(sector[1] - int(self.player.y / 1000))
            if diff_x > 5 or diff_y > 5:
                #print("rem:user pos:", self.player.x, self.player.y)
                #print("rem:removing ", sector)
                #print("rem:estimated user sector", int(self.player.x / 1000), int(self.player.y / 1000))
                self.generated_sectors.remove(sector)

                #group_calc = sector[0]+sector[1]*100
                #group_filter = pymunk.ShapeFilter()
                #group_filter.group = group_calc

                index = str(sector[0]) + "," + str(sector[1])

                #print("rem:index:", index)
                #print("rem:Wall ex:", self.sector_walls[index][0].pos1)
                
                try:
                    #print(self.sector_walls[group_calc])
                    for w in self.sector_walls[index]:
                        #print("\t", w.pos1)
                        #w.destroy(self.space)
                        #print((w in self.actors))
                        try: self.space.remove(w.segment)
                        except: print("Failed to remove wall physics segment")
                        self.game.kill_actor(w)
                        self.actors.remove(w)
                        del w
                        #w.segment.sleep()
                        #print(w.segment, " is sleeping")
                        #print(self.space.shape_query(w.segment))
                        #try:
                        #    self.space.remove(w.segment)
                        #    self.game.kill_actor(w)
                        #except: pass
                        #del w.segment
                except: pass
                #print("rem:sectors:",self.generated_sectors)

    def ensure_sector(self, x, y):
        if (x,y) not in self.generated_sectors:
            self.generate_sector((x, y))
        
    def register_actor(self, actor):
        """ Add physics entity for given actor """
        #print("adding", actor)
        self.actors.append(actor)

        actor.init_physics(self.space)
        
        #self.space.add(body, poly)
 
        #body = pymunk.Body(1, 1)
        #body.position = actor.x, actor.y

        #poly = pymunk.Poly.create_box(body)
        #self.space.add(body, poly)
        #actor.body = body
        
    def kill_actor(self, actor):
        self.actors.remove(actor)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                #print("w key was pressed")

                if self.player.remaining_jumps > 1 and self.player.jump_refresh == 0:
                    self.player.body.velocity = (self.player.body.velocity[0], 0)
                    self.player.body.apply_impulse_at_world_point((0, -10000))
                    self.player.remaining_jumps -= 1
                    self.player.jump_refresh = self.player.jump_refresh_max
            elif event.key == K_s:
                self.player.poly.friction += 10

        if event.type == KEYUP:
            if event.key == K_s:
                self.player.poly.friction -= 10

    def generate_sector(self, pos):
        self.generated_sectors.append(pos)

        #print("gen:Generating sector ", pos)
        #print("gen:user:", self.player.x, self.player.y)

        group = str(pos[0]) + "," + str(pos[1])
        #print("gen:index:",group)

        self.sector_walls[group] = []

        
        # decide on vertical sections
        for y in range(0, 10):
            x_used = []
            for x in range(0, 10):
                dice = random.random()
                if dice > .9 or (dice > .3 and x - 1 in x_used):
                    x_used.append(x)
                    w = wall.Wall(self, self.game, group, ((pos[0]*1000 + x*100), (pos[1]*1000 + y*100)), ((pos[0]*1000 + (x+1)*100), (pos[1]*1000 + y*100)))
                    self.sector_walls[group].append(w)
                    self.game.register_actor(w)
                    #print((w in self.actors))
                    
                
        # decide on horizontal sections
        for x in range(0, 10):
            for y in range(0, 10):
                y_used = []
                dice = random.random()
                if dice > .8 or (dice > .3 and y - 1 in y_used):
                    y_used.append(y)
                    w = wall.Wall(self, self.game, group, ((pos[0]*1000 + x*100), (pos[1]*1000 + y*100)), ((pos[0]*1000 + x*100), (pos[1]*1000 + (y+1)*100)))
                    self.sector_walls[group].append(w)
                    self.game.register_actor(w)
                    #print((w in self.actors))

        #print("gen:wall ex:",self.sector_walls[group][0].pos1)

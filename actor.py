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
        self.mass = 20
        self.body = None # physics
        self.poly = None
        self.grounded = False
        self.allowed_jumps = 2
        self.remaining_jumps = self.allowed_jumps

        self.life = 2000
        self.score = 0

        self.life_drain = 4 # minimum

        self.last_x = self.x
        self.last_y = self.y

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)

    def set_pos(self, x, y):
        """ Change the position (onscreen?) of this actor """
        self.x = x
        self.y = y

    def init_physics(self, space):
        body = pymunk.Body(self.mass, pymunk.inf)
        #print(body.moment)
        body.position = self.x, self.y
        self.poly = pymunk.Poly.create_box(body, (self.h, self.w))

        self.poly.friction = .6
        self.poly.elasticity = 0 # don't bounce
        self.poly.collision_type = 1
        body.group = 1000
        
        self.body = body
        space.add(body, self.poly)

    def handle_movement(self):
        dx = abs(self.x - self.last_x)
        dy = abs(self.y - self.last_y)

        self.last_x = self.x
        self.last_y = self.y

        movement = int(dx + dy)

        self.life += movement

        if movement < 5:
            self.life_drain += .2
        else:
            self.life_drain -= 4

        if self.life_drain < 4: self.life_drain = 4
        if self.life_drain > 40: self.life_drain = 40

        #print(self.life_drain)
        
        self.life -= int(self.life_drain)

        self.score += movement

        if self.life < 0:
            self.game.game_over = True
            self.game.score = self.score
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        position = pymunk.pygame_util.to_pygame(self.body.position, screen)
        local_x = (position[0] - self.w / 2)
        local_y = (position[1] - self.h / 2)

        self.x = local_x
        self.y = local_y
        
        pygame.draw.rect(
            screen,
            (0, 128, 255),
            pygame.Rect(local_x - self.game.display.x_offset, local_y - self.game.display.y_offset, self.w, self.h)
        )

    def render_score(self, screen):

        life_color = (255, 255, 255)
        life_drain_color = (255, 255, 255)

        if self.life_drain > 20: life_drain_color = (255, 0, 0)
        elif self.life_drain == 4: life_drain_color = (0, 255, 0)
        
        if self.life < 2000: life_color = (255, 0, 0)
        
        life_surface = self.font.render(str(int(self.life)), False, life_color)
        score_surface = self.font.render(str(self.score), False, (255,255,255))
        life_drain_surface = self.font.render(str(int(self.life_drain)), False, life_drain_color)
        
        screen.blit(life_surface, (0,0))
        screen.blit(score_surface, (100,0))
        screen.blit(life_drain_surface, (200,0))

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

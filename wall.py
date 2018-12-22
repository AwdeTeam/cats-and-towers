import pygame
import pymunk
import pymunk.pygame_util

class Wall:

    def __init__(self, world, game, pos1=(10, 100), pos2=(100,100)):
        self.world = world
        self.game = game
        self.pos1 = pos1
        self.pos2 = pos2
        self.segment = None

    def set_pos(self, pos1, pos2):
        """ Change the position (onscreen?) of this actor """
        self.pos1 = pos1
        self.pos2 = pos2
        
    def init_physics(self, space):
        segment = pymunk.Segment(space.static_body, self.pos1, self.pos2, 3)
        segment.friction = .9
        segment.elasticity = .9
        self.segment = segment
        space.add(segment)
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        position1 = pymunk.pygame_util.to_pygame(self.segment.a, screen)
        position2 = pymunk.pygame_util.to_pygame(self.segment.b, screen)
        pygame.draw.line(screen, (0, 128, 255), position1, position2)
        

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

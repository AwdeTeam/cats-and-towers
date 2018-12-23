import pygame
import pymunk
import pymunk.pygame_util

class Wall:

    def __init__(self, world, game, group, pos1=(10, 100), pos2=(100,100)):
        self.world = world
        self.game = game
        self.pos1 = pos1
        self.pos2 = pos2
        self.segment = None
        self.group = 5

    def set_pos(self, pos1, pos2):
        """ Change the position (onscreen?) of this actor """
        self.pos1 = pos1
        self.pos2 = pos2

    def destroy(self, space):
        space.remove(self.segment)
        
    def init_physics(self, space):
        segment = pymunk.Segment(space.static_body, self.pos1, self.pos2, 3)
        segment.friction = .4
        segment.elasticity = .9
        segment.collision_type = 2
        segment.group = self.group
        self.segment = segment
        space.add(self.segment)
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        position1 = pymunk.pygame_util.to_pygame(self.segment.a, screen)
        position2 = pymunk.pygame_util.to_pygame(self.segment.b, screen)

        local_pos1 = position1
        local_pos1 = (local_pos1[0] - self.game.display.x_offset, local_pos1[1] - self.game.display.y_offset)
        self.pos1 = position1
        
        local_pos2 = position2
        local_pos2 = (local_pos2[0] - self.game.display.x_offset, local_pos2[1] - self.game.display.y_offset)
        self.pos2 = position2
        
        pygame.draw.line(screen, (0, 128, 255), local_pos1, local_pos2)
        

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

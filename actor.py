import pygame

class Actor:

    def __init__(self, world, game):
        self.world = world
        self.game = game
        self.x = 10
        self.y = 10

    def set_pos(self, x, y):
        """ Change the position (onscreen?) of this actor """
        self.x = x
        self.y = y
    
    def render(self, screen):
        """ All drawing logic for displaying this actor onscreen """
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(self.x, self.y, 50, 50))

    def sync(self):
        # TODO: not sure what this is supposed to do?
        pass

    def pull_updates(self):
        # TODO: not sure what this is supposed to do?
        pass

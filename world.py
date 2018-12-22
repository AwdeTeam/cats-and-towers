import pymunk

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game

    def construct(self):
        """ Initialize physics world """
        self.space = pymunk.Space()
        self.space.gravity = 0, -1000

    def update(self, delta):
        """ Run the physics simulation a step """
        self.space.step(delta)

    def register_actor(self, actor):
        """ Add physics entity for given actor """
        body = pymunk.Body(1, 1666)
        body.position = 50, 100

        poly = pymunk.Poly.create_box(body)
        #self.space.add(body, poly)

    def handle_event(self, event):
        pass

import pymunk

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game

    def construct(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, -1000

    def update(self, delta):
        self.space.step(delta)

    def addActor(self):
        body = pymunk.Body(1, 1666)
        body.position = 50, 100

        poly = pymunk.Poly.create_box(body)
        self.space.add(body, poly)

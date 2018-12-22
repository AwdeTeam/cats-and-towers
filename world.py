import pymunk

class World:

    def __init__(self, game, config):
        self.space = None
        self.game = game
        self.actors = []
        
        # this was previously in construct, but then cat.py can't add actors until game starts, possibly need better solution/pipeline for how things are added
        self.space = pymunk.Space()
        self.space.gravity = 0, -.01

    def construct(self):
        """ Initialize physics world """

    def update(self, dt):
        """ Run the physics simulation a step """
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
        pass

# TODO get your snippets working you idiot

import traceback
import time
import sys

import pygame
import pygame.time

#from ..core.graphics import Display, UserInterface
from pgmodel.core.graphics import display

class GameException(Exception):
    pass

class DuplicateActorException(GameException):
    pass

class NoSuchActorException(GameException):
    pass

class Game:
    """ The core unit is the game, which handles the core gameloop and other abstract logic """

    def __init__(self, World, config):
        self._config = config
        self.cfg_global = self._config["global"]
        self.live = False
        self.running = self.cfg_global["starts_running"] #If the game is live but not running it is
                                                         # paused; actors do not get updates
                                                         # and only the interface will recieve events
        self.world = World(self, config["world"]) #When world.construct() is called it creates actors
        self.actors = [] #For quick inclusion check; actors must be hashable
        self._cull_actors = [] #Get rid of these actors on the next iteration
        self.display = display.Display(self, config["graphics"])
        #self.interface = graphics.UserInterface(self, config["ui"])
        #self.debugp = self.interface.get_print_debug()

        self.game_over = False
        self.score = 0

    def register_actor(self, actor):
        """ Create the actor and add it to the world """
        if actor in self.actors:
            raise DuplicateActorException

        self.actors.append(actor)
        self.display.register_actor(actor)
        self.world.register_actor(actor)

    def kill_actor(self, actor):
        """ Set the actor up to be removed at the end of the loop """
        #print("killing " + str(actor))
        if actor not in self.actors:
            raise NoSuchActorException

        if actor in self._cull_actors:
            raise DuplicateActorException

        self._cull_actors.append(actor)
        #print("actor is in dead:", (actor in self._cull_actors))

    def start(self):
        """ Start running the game """
        self.live = True
        exit_message = "No exit detected; something has gone quite wrong..."
        loop_start = time.time()

        clock = pygame.time.Clock()

        # Initialize things
        try:
            pygame.init()
            self.world.construct()
            #self.interface.construct()
            self.display.construct()
        except:
            traceback.print_exc()
            self.live = False
            exit_message = "ERROR EXIT: failure on construction"

        # Run main game loop
        while self.live:
            if self.running:

                if self.game_over:
                    self.display.draw_game_over()
                
                try:
                    self._update_actor_logic()
                except:
                    traceback.print_exc()
                    self.live = False
                    exit_message = "ERROR EXIT: exception in actor logic"
            
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.live = False
                        exit_message = "USER EXIT: user closed pygame manually"
                    #elif self.interface.handle_event(event):
                        #pass
                    elif self.running and self.world.handle_event(event):
                        pass
                    else:
                        pass
            except:
                traceback.print_exc()
                self.live = False
                exit_message = "ERROR EXIT: exception in event handling"

            try:
                if self.running and not self.game_over:
                    self._sync_actor_world()
                    self.world.update(1/self.cfg_global["fps"])
                    self.display.update()
                #self.interface.update()
            except:
                traceback.print_exc()
                self.live = False
                exit_message = "ERROR EXIT: exception in core update loop"

            try:
                for dead_actor in self._cull_actors:
                    #print("Now checking " + str(dead_actor))
                    # NOTE: should maybe call a function instead of deleting?
                    if dead_actor in self.actors:
                        self.actors.remove(dead_actor)
                        #del self.actors[dead_actor]
                    else:
                        raise NoSuchActorException
                    self._cull_actors.remove(dead_actor)
            except:
                traceback.print_exc()
                self.live = False
                exit_message = "ERROR EXIT: error on culling dead actors"

            clock.tick(self.cfg_global["fps"])


        pygame.quit()
        print(exit_message)
        sys.exit()

    def _update_actor_logic(self):
        """ Simple wrapper for updating the actors action systems """
        for actor in self.actors:
            actor.pull_updates()

    def _sync_actor_world(self):
        """ Another wrapper for syncing the actors to the world """
        for actor in self.actors:
            actor.sync()

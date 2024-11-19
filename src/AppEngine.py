from Modules.Simulation.Simulation import Simulation
from Modules.Presentation.OpcClient import OpcClient
from Modules.Presentation.Parameters import Parameters
from Modules.Presentation.Window import Window
import pygame
from Globals import *

# AppEngine - class used to control whole flow, declare variables that are unique
class AppEngine:

    def __init__(self):
        #pygame
        pygame.init()
        
        self._params = Parameters()
        self._window = Window(self._params)
        self._opcClient = OpcClient(self._params)
        self._simulation = Simulation()

    def LoopProgram(self):
        # Start simulation
        self._simulation.Simulate(self._params, self._opcClient, self._window)
        # End simulation

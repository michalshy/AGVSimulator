import Physics
import Simulation
from Simulation import Simulation
from OpcHandler.OpcHandler import OpcHandler
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics
import pygame
from Globals import *

# AppEngine - class used to control whole flow, declare variables that are unique
class AppEngine:

    def __init__(self):
        #pygame
        pygame.init()
        canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self._agv = AGV(canvas)
        self._phyEng = Physics(self._agv)
        self._paramManager = ParamManager()
        self._opcHandler = OpcHandler(self._paramManager, self._agv)
        self._simulation = Simulation.AGVSim(self._phyEng, self._agv, self._opcHandler, self._paramManager, canvas)

    def LoopProgram(self):
        # Start simulation
        self._simulation.Simulate()
        # End simulation

from Modules.Simulation.Simulation import Simulation
from Modules.Presentation.OpcClient import OpcClient
from Modules.Presentation.Parameters import Parameters
from Modules.Presentation.Window import Window
import pygame
from Globals import *
# -*- coding: utf-8 -*-
"""AppEngine module

Initializes upper layer classes like Parameters (Configuration), Window (PyGame render),
OpcClient (communication with OPCUA server).
Also initializes lower layer Simulation module and triggers its main loop. 
"""
class AppEngine:

    def __init__(self):
        pygame.init()
        
        self._params = Parameters()
        self._window = Window(self._params)
        self._opcClient = OpcClient(self._params)
        self._simulation = Simulation()

    def LoopProgram(self):
        # Start simulation
        self._simulation.Simulate(self._params, self._opcClient, self._window)
        # End simulation
from Modules.Simulation.Simulation import Simulation
from Modules.Presentation.Window import Window
from Modules.Presentation.Network.Network import Network
import pygame
from Config import *
from Logger import *
# -*- coding: utf-8 -*-
"""AppEngine module

Initializes upper layer classes like Parameters (Configuration), Window (PyGame render),
OpcClient (communication with OPCUA server).
Also initializes lower layer Simulation module and triggers its main loop. 
"""
class AppEngine:

    def __init__(self):
        pygame.init()
        self._window = Window()
        self._network = Network()                       # Create network module
        self._simulation = Simulation()

    def LoopProgram(self):
        logger.Info("Starting application")
        # Start simulation
        self._simulation.Simulate(self._network, self._window)
        # End simulation

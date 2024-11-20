import os
import pygame
from Modules.Presentation.Window import Window
from Modules.Presentation.Parameters import Parameters
from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Logger import Logger
from Modules.Presentation.OpcClient import OpcClient
from Modules.Simulation.Logic.Timer import *
from Modules.Entities.Physics import Physics
from Modules.Simulation.Network.Network import Network
from Globals import *
# -*- coding: utf-8 -*-
"""Simulation module

Module responsible for whole simulation. Controls main loop, triggers AGV params
update and controls overall flow in the reception, transmission and other smaller
modules.
"""
class Simulation:
    def __init__(self):
        self._finishFlag = False                        # Initialize main loop flag
        self._agv = AGV()                               # Create AGV
        self._pe = Physics(self._agv)                   # Create physics with agv passed
        self._logger = Logger()                         # Create logger
        self._network = Network()                       # Create network module

        self._agv.Init(x=STARTING_POS_X,y=STARTING_POS_Y)   # Init with position

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self, params: Parameters, opc: OpcClient, wm: Window):
        _clear = lambda: os.system('cls || clear')      # Additional clear for cli
        while not self._finishFlag:
            wm.PrepWindow()                             # Pygame section
            self._logger.WriteToFile(self._agv)         # Logger section
            self._network.HandleNetwork(opc, self._agv) # Network section            
            if self._agv.CheckDrive():
                _clear()
                self.Route()
            wm.Draw(self._agv)                          # Draw after update
            timer.UpdateDelta()                         # Update timer
            if not wm.CheckEvents(opc):                 # Check events
                self.Exit()

    def Exit(self):
        self._finishFlag = True                         # Flags set to exit main loop

    def Route(self):
        self._agv.PrintState()                          # Print state of agv to CLI
        self._agv.DetermineFlags()                      # Check for agv flags
        self._agv.Navigate()                            # Trigger navigation
        if not self._agv.GetStopFlag():                 # Check if allowed to
            self._pe.Accelerate(10)
        else:
            self._pe.Accelerate(-10)
        self._pe.Update()                               # Update position

        

      
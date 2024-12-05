import threading
from Modules.Presentation.Window import Window
from Modules.Presentation.Parameters import Parameters
from Modules.Entities.AGV.AGV import AGV
from Logger import *
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
        self._network = Network()                       # Create network module

        self._agv.Init(x=STARTING_POS_X,y=STARTING_POS_Y)   # Init with position

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self, opc: OpcClient, wm: Window):
        # Threads section
        self._network_thread = threading.Thread(target=self._network.HandleNetwork, args=(opc, self._agv))
        self._network_thread.start()
        logger.Debug("Network thread started")
        #--------EOS--------
        logger.Debug("Enter main loop")
        while not self._finishFlag:
            wm.PrepWindow()                             # Pygame section
            self._agv.LogToFile()                       # Logger section
            self.Route()
            wm.Draw(self._agv)                          # Draw after update
            timer.UpdateDelta()                         # Update timer
            if not wm.CheckEvents(opc):                 # Check events
                self.Exit()
        
        logger.Debug("Exit main loop")    
        #Threads section
        self._network.EndTransmission()
        self._network_thread.join()
        logger.Debug("Network thread joined")
        #--------EOS--------

    def Exit(self):
        logger.Debug("Finish flag on true")    
        self._finishFlag = True                         # Flags set to exit main loop

    def Route(self):
        self._agv.DetermineFlags()                      # Check for agv flags
        self._agv.Navigate(self._pe)                            # Trigger navigation
        if self._agv.CheckDrive():                      # Check if allowed to
            self._pe.Accelerate(10)
        else:
            self._pe.Accelerate(-1)
        self._pe.Update()                               # Update position

        

      
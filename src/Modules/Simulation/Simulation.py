import os
import pygame
from Modules.Presentation.Window import Window
from Modules.Presentation.Parameters import Parameters
from Modules.Entities.AGV.AGV import AGV
from Modules.Entities.Logger import Logger
from Modules.Presentation.OpcClient import OpcClient
from Modules.Simulation.Logic.Timer import *
from Modules.Entities.Physics import Physics
from Globals import *

class Simulation:
    def __init__(self):
        self._finishFlag = False
        self._agv = AGV()
        self._pe = Physics(self._agv)
        self._logger = Logger()

        self._agv.Init()

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self, params: Parameters, opc: OpcClient, wm: Window):
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        while not self._finishFlag:
            wm.PrepWindow()
            opc.ReceiveDataFromServer(params)
            opc.SendToServer(self._agv)
            self._logger.WriteToFile(self._agv)
            if not wm.CheckEvents(opc):
                self.Exit()
            self._agv.SetRouteParams(params.GetNNC())
            if self._agv.GetDriveMode():
                _clear()
                self.Route()
            wm.Draw(self._agv)
            timer.UpdateDelta()

    def Exit(self):
        self.finishFlag = True

    def Route(self):
        self._agv.PrintState()
        self._agv.DetermineFlags()
        self._agv.Navigate()
        if not self._agv.GetStopFlag():
            self._pe.Accelerate(10)
        else:
            self._pe.Accelerate(-10)
        self._pe.Update()
        

      
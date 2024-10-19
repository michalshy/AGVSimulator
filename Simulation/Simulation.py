import os
from Simulation.Managers.WindowManager import WindowManager
from Simulation.Managers.ParamManager import ParamManager
from Simulation.Managers.LogManager import LogManager
from Simulation.AGV.AGV import AGV
from OpcHandler.OpcHandler import OpcHandler
from Physics.Physics import Physics
from OpcHandler.OpcHandler import OpcHandler
import pygame
from Simulation.Logic.Timer import *
from Globals import *

class AGVSim(object):
    def __init__(self, pe: Physics, agv: AGV, opcHandler: OpcHandler, pm: ParamManager, canvas):
        
        self._wm: WindowManager = WindowManager(canvas, pm, agv)
        self._pm = pm
        self._pe = pe
        self._agv = agv
        self._agv.Init(self._wm.GetImage())
        self._logger = LogManager()
        # for network
        self._opcHandler = opcHandler
        #for simul
        self.finishFlag = False

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        while not self.finishFlag:
            self._wm.PrepWindow()
            self._opcHandler.ReceiveDataFromServer()
            self._opcHandler.SendToServer()
            self._logger.WriteToFile(self._agv)
            if not self._wm.CheckEvents(self._opcHandler):
                self.Exit()
            self._agv.SetRouteParams(self._pm.GetNNC())
            if self._agv.GetDriveMode():
                _clear()
                self.Route()
            self.Draw()
            timer.UpdateDelta()

    def Exit(self):
        self.finishFlag = True

    def Draw(self):
        self._wm.Draw()
        self._wm.Update()

    def CheckRotation(self, val: int):
        if (val > 20 and val < 170):
            self._pe.RotateLeft()
        if (val >= 180 and val < 350):
            self._pe.RotateRight()

    def Route(self):
        #show state in output terminal
        self._agv.PrintState()
        #check flags in module and submodules
        self._agv.DetermineFlags()
        #fill routes into navigation
        self._agv.Navigate()
        #check rotation to routes
        self.CheckRotation(self._agv.CalculateTurn())
        #accelerate object and update position
        self._pe.Accelerate()
        self._pe.Update()
        

      
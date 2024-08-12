import os
from Simulation.Managers.WindowManager import WindowManager
from Simulation.Managers.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from OpcHandler.OpcHandler import OpcHandler
from Physics.Physics import Physics
from OpcHandler.OpcHandler import OpcHandler
import pygame
from Simulation.Logic.Timer import Timer
from Globals import *

class AGVSim(object):
    def __init__(self, pe: Physics, agv: AGV, opcHandler: OpcHandler, pm: ParamManager, canvas):
        
        self._wm: WindowManager = WindowManager(canvas, pm, agv)
        self._timer = Timer()

        self._pm = pm
        self._pe = pe

        self._agv = agv
        self._agv.Init(self._wm.GetImage())

        self._action = 0

        # for network
        self._opcHandler = opcHandler

        #for simul
        self.finishFlag = False

    def SetupTimers(self):
        self._pe.SetTimer(self._timer)
        self._timer.StartTimer()

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        # Init timers inside internal classes
        self.SetupTimers()
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        while not self.finishFlag:
            self._wm.PrepWindow()
            self._opcHandler.ReceiveDataFromServer()
            if not self._wm.CheckEvents(self._opcHandler):
                self.Exit()
            self._agv.SetDestId(self._pm.GetNNC())
            self._agv.SetDestTrig(self._pm.GetNNC())
            if self._agv.GetDriveMode():
                _clear()
                self.Route()
            self._opcHandler.SendToServer()
            self.Draw()
            self._timer.UpdateDelta()

    def Exit(self):
        self.finishFlag = True

    def Draw(self):
        self._wm.Draw()
        self._wm.Update()

    def CheckRotation(self, val):
        if (val > 20 and val < 170):
            self._pe.RotateLeft()
        if (val >= 180 and val < 350):
            self._pe.RotateRight()

    def Route(self):
        #show state in output terminal
        self._agv.PrintState()
        #check flags
        self._agv.DetermineFlags()
        self._agv.Navigate()
        self.CheckRotation(self._agv.CalculateTurn())
        self._pe.Accelerate()
        self._pe.Update()
        

      
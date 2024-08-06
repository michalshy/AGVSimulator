import os
from Logic.WindowManager import WindowManager
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from OpcHandler.OpcHandler import OpcHandler
from Physics.Physics import Physics
from OpcHandler.OpcHandler import OpcHandler
import pygame
from Logic.Timer import Timer

class AGVSim(object):
    def __init__(self, pe: Physics, agv: AGV, opcHandler: OpcHandler, pm: ParamManager, canvas):
        
        self._wm: WindowManager = WindowManager(canvas)
        self._timer = Timer()

        self._pm = pm
        self._pe = pe
        self._agv = agv
        self._action = 0

        # for network
        self._opcHandler = opcHandler

        #for simul
        self.sw = False
        self.finishFlag = False

        

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        self._timer.StartTimer()
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        while not self.finishFlag:
            print(self._timer.GetDt())
            self._wm.PrepWindow()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.Exit()
            self._opcHandler.ReceiveDataFromServer()
            self._agv.SetDestId(self._pm.GetNNC())
            self._agv.SetDestTrig(self._pm.GetNNC())
            if self._agv.GetDriveMode():
                match self._agv.GetNNS().goingToID:
                    case 0:
                        _clear()
                        self._pe.EmergencyStop()
                        self._pe.Update()
                        self._agv.PrintState()
                    case 1:
                        _clear()
                        self.FirstRoute()
                    case 2:
                        _clear()
                        self.SecondRoute()
                    case 3:
                        _clear()
                        self.ThirdRoute()
            self._opcHandler.SendToServer()
            self.Draw()
            self._timer.UpdateDelta()

    def Draw(self):
        pygame.display.update()

    def Exit(self):
        self._opcHandler.CloseConnection()
        self.finishFlag = True

    #  ID 1
    def FirstRoute(self):
        self._agv.PrintState()
        self._agv.DetermineFlags()
        self._pe.Accelerate()
        self._pe.Update()
        if self.sw:
            self._pe.RotateLeft()
            if self._agv.GetNNS().heading >= 0:
                self.sw = False
        if not self.sw:
            self._pe.RotateRight()
            if self._agv.GetNNS().heading <= -360:
                self.sw = True

    #  ID 2
    def SecondRoute(self):
        self._agv.PrintState()
        self._agv.DetermineFlags()
        self._pe.Accelerate()
        self._pe.Update()
        self._pe.RotateLeft()

    #  ID 3
    def ThirdRoute(self):
        self._agv.PrintState()
        self._agv.DetermineFlags()
        self._pe.Accelerate()
        self._pe.Update()

      
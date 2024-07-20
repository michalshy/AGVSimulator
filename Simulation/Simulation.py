import matplotlib.pyplot as plt
import os
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics
import keyboard
from OpcHandler import OpcHandler
import threading

class AGVSim(object):
    def __init__(self, env, pe: Physics, agv: AGV, opcHandler: OpcHandler):
        self._env = env
        self.end_evnt = self._env.event()
        self._pm = ParamManager()
        self._pe = pe
        self._agv = agv
        self._action = 0

        # for network
        self._opcHandler = opcHandler

        #for simul
        self.steps = 100
        self.sw = False
        self.finishFlag = False

    def Run(self):
        self._action = self._env.process(self.Simulate())
        self._env.run(until = self.end_evnt)

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        while not self.finishFlag:
            self._opcHandler.ReceiveDataFromServer(self._pm)
            self.CheckInput()
            self._agv.SetDestId(self._pm.GetNNC())
            self._agv.SetDestTrig(self._pm.GetNNC())
            if self._agv.GetDriveMode():
                print(threading.active_count())
                match self._agv.GetNNS().goingToID:
                    case 0:
                        _clear()
                        self._pe.EmergencyStop()
                        self._pe.Update()
                        self._agv.PrintState()
                        yield self._env.process(self.Delay())
                    case 1:
                        _clear()
                        self.FirstRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100
                    case 2:
                        _clear()
                        self.SecondRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100
                    case 3:
                        _clear()
                        self.ThirdRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100     

            self._opcHandler.SendToServer()
               
            if not self._agv.GetDriveMode():
                try:
                    plt.plot(self._agv.GetHistX(), self._agv.GetHistY())
                except ValueError as err:
                    continue
                plt.show()

    def CheckInput(self):
        if keyboard.is_pressed('q'):
            self._opcHandler.CloseConnection()
            self.end_evnt.succeed()

    # Wait 1 second
    # TODO: remember to change to 1 at the end of development
    def Delay(self):
        yield self._env.timeout(0.1)

    def ShowRoute(self):
        pass

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

      
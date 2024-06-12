import simpy
import matplotlib.pyplot as plt
import numpy as np
import time, os, math
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics
import keyboard


class AGVSim(object):
    def __init__(self, env, pe: Physics, agv: AGV):
        self._env = env
        self.end_evnt = self._env.event()
        self._pm = ParamManager()
        self._pe = pe
        self._agv = agv
        self._action = 0
        self.c = 0

        #for simul
        self.steps = 100
        self.sw = False

    def Run(self):
        self._action = self._env.process(self.Simulate())
        self._env.run(until = self.end_evnt)

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        # Simulation of basic tasks
        _clear = lambda: os.system('cls || clear')
        self._agv.SetId(self._pm.GetNNC())
        while True:
            match self._agv.GetNNS().goingToID:
                case 1:
                    while self._agv.GetDriveMode():
                        _clear()
                        self.CheckInput()
                        self.FirstRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100
                case 2:
                    while self._agv.GetDriveMode():
                        _clear()
                        self.CheckInput()
                        self.SecondRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100
                case 3:
                    while self._agv.GetDriveMode():
                        _clear()
                        self.CheckInput()
                        self.ThirdRoute()
                        yield self._env.process(self.Delay())
                        self.steps -= 1
                        if self.steps == 0:
                            self._agv.SetDriveMode(0)
                            self.steps = 100
            plt.plot(self._agv.GetHistX(), self._agv.GetHistY())
            plt.show()

    def CheckInput(self):
        if keyboard.is_pressed('q'):
            self.end_evnt.succeed()

    # Wait 1 second
    def Delay(self):
        yield self._env.timeout(1)

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
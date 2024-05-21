import simpy
import time, os, math
from Simulation.ParamManager import ParamManager
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics


class AGVSim(object):
    def __init__(self, env, pe: Physics, agv: AGV):
        self._env = env
        self._pm = ParamManager()
        self._pe = pe
        self._agv = agv
        self._action = 0

    def Run(self):
        self._action = self._env.process(self.Simulate())

    # Main function of the program, responsible for simulation of AGV movement
    def Simulate(self):
        # Simulation of basic task 5 meters forward
        _clear = lambda: os.system('cls || clear')
        while True:
            _clear()
            if self._agv.GetENC().batteryValue > 300:
                self._pe.Accelerate(self._agv.GetNNS(), self._agv.GetENC())
                self._pe.UpdatePosition(self._agv.GetNNS(), self._agv.GetENC())
            self._agv.PrintState()
            yield self._env.process(self.Delay())

    # Wait for 10 factors, so in this case 1 second
    def Delay(self):
        yield self._env.timeout(10)

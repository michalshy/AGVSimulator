import simpy
import time, os
from Simulation.ParamManager import ParamManager as pm
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics

class AGVSim(object):
    def __init__(self, env, pe: Physics):
        self.env = env
        self._pm = pm()
        self._pe = pe

        # Start the run process everytime an instance is created.
        # self.action = env.process(self.run())

    def Simulate(self, agv: AGV):
        # Simulation of basic task 5 meters forward
        clear = lambda: os.system('cls')
        while True:
            clear()
            self._pe.accelerate(agv.getNNS(), agv.getENC())
            agv.printState()
            time.sleep(1)
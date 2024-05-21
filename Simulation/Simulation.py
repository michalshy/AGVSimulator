import simpy
import time, os, math
#from ParamManager import ParamManager as pm
from Simulation.AGV.AGV import AGV
from Physics.Physics import Physics

class AGVSim(object):
    def __init__(self, env, pe: Physics):
        self.env = env
       # self._pm = pm()
        self._pe = pe

        # Start the run process everytime an instance is created.
        # self.action = env.process(self.run())

    def Simulate(self, agv: AGV):
        # Simulation of basic task 5 meters forward
        clear = lambda: os.system('cls')
        agv._enc.batteryValue = 1000
        agv._nns.heading = 2
        while True:
            clear()
            if agv._enc.batteryValue > 10:
                self._pe.accelerate(agv.getNNS(), agv.getENC()) 
                self._pe.updatePosition(agv.getNNS(), agv.getENC())          
            agv.printState()
            time.sleep(1)
import simpy
from Simulation.ParamManager import ParamManager as pm


class AGVSim(object):
    def __init__(self, env):
        self.env = env
        self._pm = pm()

        # Start the run process everytime an instance is created.
        # self.action = env.process(self.run())

    def Simulate(self):
        # Simulation of basic task 5 meters forward
        while True:
            print("Simulation Started")
